#!/usr/bin/env python3
"""Validate Markdown storyboards produced from sequential comic panels."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


SEGMENT_RE = re.compile(r"^#{1,6}\s*【片段\s*(\d+)】", re.MULTILINE)
SAFE_SEGMENT_RE = re.compile(
    r"^#{1,6}\s*【平台安全替换[·・\s]*片段\s*(\d+)】", re.MULTILINE
)
SHOT_RE = re.compile(
    r"\*\*分镜\s*(\d+)\s*[（(]\s*(\d+(?:\.\d+)?)\s*秒\s*[）)]\s*[：:]\*\*"
)
COMBAT_SEQUENCE_RE = re.compile(
    r"\*\*战斗段\s*(\d+)\s*[（(]\s*(\d+(?:\.\d+)?)\s*秒\s*[·・\s]*自动分镜\s*[）)]\s*[：:]\*\*"
)
LEGACY_TIMECODE_RE = re.compile(r"\*\*\d+(?:\.\d+)?-\d+(?:\.\d+)?s[：:]\*\*")
REFERENCE_RE = re.compile(
    r"(?:分镜参考|参考)?\s*`?\[([^\]\r\n]+\.(?:png|jpe?g|webp))\]`?",
    re.IGNORECASE,
)
FORBIDDEN_RE = re.compile(r"预计发声|约\s*\d+(?:\.\d+)?\s*秒")
PRODUCTION_NOTE_RE = re.compile(
    r"一次性场景|不单独生成环境图|不建立独立背景|视频生成时|"
    r"后期添加|用于衔接|为下一片段(?:对白)?衔接|避免乱码"
)
LEGACY_FIELD_RE = re.compile(r"^(?:景别|构图|运镜|画面内容)[：:]", re.MULTILINE)
ENVIRONMENT_RE = re.compile(r"^环境参考[：:]", re.MULTILINE)
AUDIO_RE = re.compile(
    r"(?:音效|环境声|动作声|拟音|BGM|配乐|背景音乐)[：:]",
    re.IGNORECASE,
)
META_RE = re.compile(
    r"保持原格(?:姿势|构图|表情)?|与原格一致|原格中|原格般|原格原则|"
    r"(?:按照|依照|按)(?:原格|原图|参考图)(?:进行)?(?:处理|呈现|还原)?|"
    r"(?:背景|画面)(?:按照|依照|按)(?:原格|原图|参考图)(?:进行)?(?:处理|呈现|还原)?|"
    r"无(?:实体|独立)?背景|原(?:格|画|图)[^。；\r\n]{0,16}(?:没有|不呈现|弱化)[^。；\r\n]{0,12}(?:实景|环境|背景|景物)|"
    r"盒外环境不可见|(?:不补画|不另加|不加入|不出现|不恢复|不保留|不切换|不自行)"
    r"[^。；\r\n]{0,20}(?:背景|实景|环境|林景|树林|树木|天空|城市|建筑)"
)
BACKGROUND_VISUAL_RE = re.compile(
    r"背景|天空|云(?:层|影|体)?|树(?:冠|林|木|影)?|森林|草(?:地|坡|丛|叶)?|地面|地板|"
    r"墙(?:面|壁)?|室内|走廊|房间|街道|屋顶|山(?:体|坡|脊)?|灌木|"
    r"水面|湖面|海面|河面|岩(?:壁|地|石)?|洞穴|速度(?:线|带|场)|"
    r"放射线|冲击底|渐变|纯色|留白|光幕|雾|烟尘|尘土|雨幕|雪地|"
    r"箱壁|盒壁|内衬|布面|衣料[^。；\r\n]{0,12}(?:铺满|填满|遮满)|"
    r"(?:铺满|填满|遮满)(?:画面|背景)"
)
NEGATIVE_PROMPT_RE = re.compile(
    r"^(?:景别|构图|运镜|画面内容)[：:][^\r\n]*(?:不增加|不使用|不推拉|不环绕|"
    r"不出现|不进入|不显示|不改变|不穿透|不继续|不做|不要|避免|无需)",
    re.MULTILINE,
)
QUOTE_RE = re.compile(r"“([^”]+)”")
SPEECH_HINT_RE = re.compile(
    r"旁白|说道|说着|说|喊道|喊|问道|问|答道|回答|解释|嘟囔|"
    r"低声|高声|叫道|念道|宣布|开口"
)
SPEAKER_QUOTE_RE = re.compile(
    r"([A-Za-z0-9\u3400-\u9fff·]+?)(?:画外)?"
    r"(?:说道|说|喊道|喊|问道|问|答道|回答|嘟囔|叫道|念道|宣布|开口)"
    r"[：:]\s*“([^”]+)”"
)
HIDDEN_CUT_RE = re.compile(
    r"(?:画面|镜头)?(?:末尾|随后|然后|再)?切(?:换)?(?:到|至|为)?"
    r"(?=\s*(?:平视|仰视|俯视|斜俯视|低机位|高位|正面|侧面|背面|"
    r"近景|中景|远景|特写|全景|反打|插入|手部|脸部|眼部|物件))"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--max-seconds", type=int, default=15)
    parser.add_argument("--image-dir", type=Path)
    parser.add_argument(
        "--dialogue-ledger",
        type=Path,
        help="Internal JSON mapping source bubbles to storyboard shots.",
    )
    return parser.parse_args()


def segment_chunks(
    text: str, segment_re: re.Pattern[str] = SEGMENT_RE
) -> list[tuple[int, str]]:
    matches = list(segment_re.finditer(text))
    return [
        (
            int(match.group(1)),
            text[
                match.start() : matches[index + 1].start()
                if index + 1 < len(matches)
                else len(text)
            ],
        )
        for index, match in enumerate(matches)
    ]


def missing_voice_directions(chunk: str) -> list[str]:
    """Return spoken/narrated quotes not followed by a full-width voice note."""
    missing: list[str] = []
    for line in chunk.splitlines():
        for match in QUOTE_RE.finditer(line):
            prefix = line[: match.start()]
            # Ignore quoted keywords inside an existing voice-direction parenthesis.
            if prefix.count("（") > prefix.count("）"):
                continue
            nearby = prefix[max(0, len(prefix) - 40) :]
            suffix = line[match.end() :]
            # A quoted keyword inside narration is not a separate spoken line.
            if not SPEECH_HINT_RE.search(nearby) or re.match(r"[^（）]*?(?:时|处)", suffix):
                continue
            if not re.match(r"\s*[。！？!?]?\s*（", suffix):
                missing.append(match.group(1))
    return missing


def compact_text(value: str) -> str:
    """Normalize whitespace for exact dialogue-presence checks."""
    return re.sub(r"\s+", "", value)


def coverage_dialogue_metrics(block: str) -> tuple[int, int]:
    """Return meaningful dialogue characters and distinct explicit speakers."""
    matches = list(SPEAKER_QUOTE_RE.finditer(block))
    meaningful_characters = sum(
        sum(character.isalnum() for character in match.group(2)) for match in matches
    )
    speakers = {match.group(1) for match in matches}
    return meaningful_characters, len(speakers)


def build_shot_map(main_text: str) -> dict[str, tuple[int, str]]:
    """Return timed target key -> (duration, full block)."""
    shot_map: dict[str, tuple[int, str]] = {}
    for segment_number, chunk in segment_chunks(main_text):
        shots = list(SHOT_RE.finditer(chunk))
        for index, match in enumerate(shots):
            end = shots[index + 1].start() if index + 1 < len(shots) else len(chunk)
            shot_number = int(match.group(1))
            duration = int(float(match.group(2)))
            shot_map[f"片段{segment_number}/分镜{shot_number}"] = (
                duration,
                chunk[match.start() : end],
            )
        combat_sequences = list(COMBAT_SEQUENCE_RE.finditer(chunk))
        for index, match in enumerate(combat_sequences):
            end = (
                combat_sequences[index + 1].start()
                if index + 1 < len(combat_sequences)
                else len(chunk)
            )
            sequence_number = int(match.group(1))
            duration = int(float(match.group(2)))
            shot_map[f"片段{segment_number}/战斗段{sequence_number}"] = (
                duration,
                chunk[match.start() : end],
            )
    return shot_map


def validate_dialogue_ledger(
    ledger_path: Path,
    main_text: str,
    image_dir: Path | None,
) -> list[str]:
    errors: list[str] = []
    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"对白台账无法读取：{exc}"]

    if ledger.get("version") != 1:
        errors.append("对白台账version必须为1。")
    panels = ledger.get("panels")
    if not isinstance(panels, list):
        return errors + ["对白台账panels必须是数组。"]

    allowed_coverage = {"shared", "reverse", "insert", "mixed"}
    allowed_kinds = {"dialogue", "inner", "narration"}
    shot_map = build_shot_map(main_text)
    seconds_by_target: dict[str, float] = {}
    acting_chars_by_target: dict[str, int] = {}
    seen_images: set[str] = set()
    available_images = (
        {path.name.casefold() for path in image_dir.iterdir() if path.is_file()}
        if image_dir
        else None
    )

    for panel_index, panel in enumerate(panels, start=1):
        label = f"对白台账panels[{panel_index}]"
        if not isinstance(panel, dict):
            errors.append(f"{label}必须是对象。")
            continue
        image = panel.get("image")
        if not isinstance(image, str) or not image.strip():
            errors.append(f"{label}缺少image。")
            image = f"#{panel_index}"
        else:
            key = Path(image).name.casefold()
            if key in seen_images:
                errors.append(f"对白台账重复登记图片：{image}")
            seen_images.add(key)
            if available_images is not None and key not in available_images:
                errors.append(f"对白台账图片不存在：{image}")

        coverage = panel.get("coverage")
        if coverage not in allowed_coverage:
            errors.append(
                f"{image}的coverage必须是shared/reverse/insert/mixed之一。"
            )
        bubbles = panel.get("bubbles")
        if not isinstance(bubbles, list) or not bubbles:
            errors.append(f"{image}的bubbles必须是非空数组。")
            continue
        declared_count = panel.get("source_bubble_count")
        if not isinstance(declared_count, int) or declared_count != len(bubbles):
            errors.append(
                f"{image}的source_bubble_count与bubbles行数不一致："
                f"{declared_count} != {len(bubbles)}"
            )

        seen_ids: set[str] = set()
        panel_speakers = {
            bubble.get("speaker")
            for bubble in bubbles
            if isinstance(bubble, dict)
            and isinstance(bubble.get("speaker"), str)
            and bubble["speaker"].strip()
        }
        for bubble_index, bubble in enumerate(bubbles, start=1):
            bubble_label = f"{image}气泡{bubble_index}"
            if not isinstance(bubble, dict):
                errors.append(f"{bubble_label}必须是对象。")
                continue
            bubble_id = bubble.get("id")
            if not isinstance(bubble_id, str) or not bubble_id.strip():
                errors.append(f"{bubble_label}缺少id。")
            elif bubble_id in seen_ids:
                errors.append(f"{image}内气泡id重复：{bubble_id}")
            else:
                seen_ids.add(bubble_id)
            if not isinstance(bubble.get("speaker"), str) or not bubble["speaker"].strip():
                errors.append(f"{bubble_label}缺少speaker。")
            if len(panel_speakers) >= 2 and (
                not isinstance(bubble.get("speaker_evidence"), str)
                or not bubble["speaker_evidence"].strip()
            ):
                errors.append(f"{bubble_label}属于多说话人面板但缺少speaker_evidence。")
            if bubble.get("kind") not in allowed_kinds:
                errors.append(f"{bubble_label}的kind必须是dialogue/inner/narration之一。")
            if not isinstance(bubble.get("source_text"), str) or not bubble["source_text"].strip():
                errors.append(f"{bubble_label}缺少source_text。")

            status = bubble.get("status")
            if status == "omitted":
                if not isinstance(bubble.get("omission_reason"), str) or not bubble[
                    "omission_reason"
                ].strip():
                    errors.append(f"{bubble_label}标记omitted但缺少omission_reason。")
                continue
            if status != "mapped":
                errors.append(f"{bubble_label}的status必须是mapped或omitted。")
                continue

            mappings = bubble.get("segments", [bubble])
            if not isinstance(mappings, list) or not mappings or any(not isinstance(m, dict) for m in mappings):
                errors.append(f"{bubble_label}的segments必须是非空对象数组。")
                continue
            if "segments" in bubble and bubble.get("script_text") != "".join(str(m.get("script_text", "")) for m in mappings):
                errors.append(f"{bubble_label}的完整script_text与segments拼接不一致。")
            for mapping in mappings:
                target = mapping.get("target")
                script_text = mapping.get("script_text")
                seconds = mapping.get("seconds")
                if not isinstance(target, str) or target not in shot_map:
                    errors.append(f"{bubble_label}的target不存在：{target}")
                    continue
                if not isinstance(script_text, str) or not script_text.strip():
                    errors.append(f"{bubble_label}缺少script_text。")
                else:
                    block = shot_map[target][1]
                    spoken = "".join(re.findall(r"“([^”]+)”\s*（[^）]*）", block))
                    if compact_text(script_text) not in compact_text(block) and compact_text(script_text) not in compact_text(spoken):
                        errors.append(f"{bubble_label}的script_text未出现在{target}。")
                    if bubble.get("kind") != "narration":
                        count = sum(char.isalnum() for char in script_text)
                        acting_chars_by_target[target] = acting_chars_by_target.get(target, 0) + count
                if not valid_seconds(seconds) or seconds <= 0:
                    errors.append(f"{bubble_label}的seconds必须是正数。")
                else:
                    seconds_by_target[target] = seconds_by_target.get(target, 0.0) + float(seconds)

    for target, required_seconds in seconds_by_target.items():
        shot_seconds = shot_map[target][0]
        if math.ceil(required_seconds) > shot_seconds:
            errors.append(
                f"{target}映射对白预计{required_seconds:g}秒，向上取整后超过"
                f"分镜时长{shot_seconds}秒。"
            )
    performance = ledger.get("performance", [])
    if not isinstance(performance, list):
        errors.append("对白台账performance必须是数组。")
        performance = []
    seen_performance: set[str] = set()
    for entry in performance:
        if not isinstance(entry, dict):
            errors.append("performance条目必须是对象。")
            continue
        target = entry.get("target")
        if not isinstance(target, str) or target not in shot_map:
            errors.append(f"performance目标不存在：{target}")
            continue
        if target in seen_performance:
            errors.append(f"performance重复目标：{target}")
        seen_performance.add(target)
        if not isinstance(entry.get("evidence"), str) or not entry["evidence"].strip():
            errors.append(f"{target}缺少表演依据。")
        count = acting_chars_by_target.get(target, 0)
        minimum, maximum = (3, 4) if count >= 42 else (2, 3) if count > 20 else (1, 2)
        details = entry.get("details")
        if not isinstance(details, list) or not minimum <= len(details) <= maximum:
            errors.append(f"{target}台词{count}字，需登记{minimum}–{maximum}个表演细节。")
        else:
            normalized = []
            for detail in details:
                if not isinstance(detail, str) or not detail.strip():
                    errors.append(f"{target}表演细节必须是非空正文摘录。")
                elif compact_text(detail) not in compact_text(shot_map[target][1]):
                    errors.append(f"{target}登记的表演未写入正文：{detail}")
                else:
                    normalized.append(compact_text(detail))
            if len(set(normalized)) != len(normalized):
                errors.append(f"{target}重复登记同一表演细节。")
        if count >= 42 and (not isinstance(entry.get("long_take_reason"), str) or not entry["long_take_reason"].strip()):
            errors.append(f"{target}长台词保留单镜但缺少已兑现的长镜头理由。")
        intervals = entry.get("intervals")
        if not isinstance(intervals, list) or not intervals:
            errors.append(f"{target}缺少串行/并行表演估时间隔。")
            continue
        duration, speech = 0.0, 0.0
        for interval in intervals:
            if not isinstance(interval, dict) or not all(valid_seconds(interval.get(k)) for k in ("speech_seconds", "acting_seconds")):
                errors.append(f"{target}间隔估时必须为有限非负数。")
                continue
            speaking, acting = interval["speech_seconds"], interval["acting_seconds"]
            duration += max(speaking, acting)
            speech += speaking
        if speech + 1e-6 < seconds_by_target.get(target, 0):
            errors.append(f"{target}表演估时未覆盖全部映射对白。")
        if math.ceil(duration) > shot_map[target][0]:
            errors.append(f"{target}对白与表演共需{duration:g}秒，超过镜头时长。")
    for target, count in acting_chars_by_target.items():
        if count > 20 and target not in seen_performance:
            errors.append(f"{target}台词合计{count}字，缺少表演与估时记录。")
    return errors


def valid_seconds(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def main() -> int:
    args = parse_args()
    text = args.storyboard.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    safe_section_marker = text.find("# 附录：平台安全替换稿")
    if safe_section_marker >= 0:
        main_text = text[:safe_section_marker]
        safe_text = text[safe_section_marker:]
    else:
        main_text = text
        safe_text = ""

    chunks = segment_chunks(main_text)
    if not chunks:
        errors.append("未找到形如‘## 【片段1】’的片段标题。")

    numbers = [number for number, _ in chunks]
    if numbers and numbers != list(range(numbers[0], numbers[0] + len(numbers))):
        errors.append(f"片段编号不连续：{numbers}")

    def validate_chunks(
        labeled_chunks: list[tuple[str, int, str]], require_contiguous_numbers: bool
    ) -> None:
        if require_contiguous_numbers:
            numbers = [number for _, number, _ in labeled_chunks]
            if numbers and numbers != list(range(numbers[0], numbers[0] + len(numbers))):
                errors.append(f"片段编号不连续：{numbers}")

        for label, number, chunk in labeled_chunks:
            validate_chunk(label, number, chunk)

    def validate_chunk(label: str, number: int, chunk: str) -> None:
        shots = list(SHOT_RE.finditer(chunk))
        combat_sequences = list(COMBAT_SEQUENCE_RE.finditer(chunk))
        if shots and combat_sequences:
            errors.append(f"{label}{number}混用了逐镜时长与战斗自动分镜模式。")
            return
        if not shots and not combat_sequences:
            if LEGACY_TIMECODE_RE.search(chunk):
                errors.append(f"{label}{number}仍使用旧时间段，应改为‘分镜1（3秒）’格式。")
            else:
                errors.append(f"{label}{number}没有分镜时长块。")
            return

        if combat_sequences:
            sequence_numbers: list[int] = []
            total_duration = 0
            for match in combat_sequences:
                sequence_raw, duration_raw = match.groups()
                sequence_numbers.append(int(sequence_raw))
                if "." in duration_raw:
                    errors.append(f"{label}{number}含小数时长：{match.group(0)}")
                    continue
                duration = int(duration_raw)
                if duration <= 0:
                    errors.append(f"{label}{number}时长必须大于0秒：{match.group(0)}")
                total_duration += duration
            if sequence_numbers != [1]:
                errors.append(
                    f"{label}{number}自动分镜模式必须只含战斗段1：{sequence_numbers}"
                )
            if total_duration > args.max_seconds:
                errors.append(
                    f"{label}{number}总时长{total_duration}秒，超过{args.max_seconds}秒。"
                )
            if "开局状态：" not in chunk or "战斗过程：" not in chunk or "结束状态：" not in chunk:
                errors.append(
                    f"{label}{number}战斗自动分镜缺少开局状态、战斗过程或结束状态。"
                )
            if len(re.findall(r"(?m)^\s*\d+[.、]\s*【[^】]+】", chunk)) < 2:
                errors.append(
                    f"{label}{number}战斗自动分镜至少需要两个带节奏/覆盖提示的有序动作节点。"
                )
            if not BACKGROUND_VISUAL_RE.search(chunk):
                errors.append(
                    f"{label}{number}的战斗段缺少可见背景；请写出实体环境、图形背景或填满画面的近景表面。"
                )

        shot_numbers: list[int] = []
        total_duration = 0
        for match in shots:
            shot_raw, duration_raw = match.groups()
            shot_number = int(shot_raw)
            shot_numbers.append(shot_number)
            if "." in duration_raw:
                errors.append(f"{label}{number}含小数时长：{match.group(0)}")
                continue
            duration = int(duration_raw)
            if duration <= 0:
                errors.append(f"{label}{number}时长必须大于0秒：{match.group(0)}")
            total_duration += duration

        if shots:
            expected = list(range(1, len(shot_numbers) + 1))
            if shot_numbers != expected:
                errors.append(f"{label}{number}分镜编号应从1连续递增：{shot_numbers}")
            if total_duration > args.max_seconds:
                errors.append(
                    f"{label}{number}总时长{total_duration}秒，超过{args.max_seconds}秒。"
                )

        for match in PRODUCTION_NOTE_RE.finditer(chunk):
            errors.append(
                f"{label}{number}含制作流程说明，不是可直接生成的提示词：{match.group(0)}"
            )

        environment_matches = list(ENVIRONMENT_RE.finditer(chunk))
        if len(environment_matches) > 1:
            errors.append(f"{label}{number}重复写了环境参考，应只在片段标题下写一次。")
        first_timed_block = shots[0] if shots else combat_sequences[0]
        if any(match.start() > first_timed_block.start() for match in environment_matches):
            errors.append(f"{label}{number}把环境参考写进了分镜块。")

        previous_references: tuple[str, ...] = ()
        for index, shot in enumerate(shots):
            block_end = (
                shots[index + 1].start()
                if index + 1 < len(shots)
                else len(chunk)
            )
            block = chunk[shot.end() : block_end]
            current_references = tuple(
                reference.casefold() for reference in REFERENCE_RE.findall(block)
            )
            shot_label = f"{label}{number}的分镜{shot.group(1)}"
            duration = int(float(shot.group(2)))
            dialogue_characters, speaker_count = coverage_dialogue_metrics(block)
            hidden_cut = HIDDEN_CUT_RE.search(block)
            if hidden_cut:
                errors.append(
                    f"{shot_label}在一个编号块内隐藏了机位切换：{hidden_cut.group(0)}；"
                    "请把新机位改为下一个编号分镜。"
                )
            if duration >= 7:
                warnings.append(
                    f"{shot_label}时长为{duration}秒；请确认存在持续可读的表演或连续动作，"
                    "否则按视觉焦点拆镜。"
                )
            if dialogue_characters >= 42:
                warnings.append(
                    f"{shot_label}含{dialogue_characters}个有意义的台词字符；"
                    "默认应按语义节点拆镜，保留长镜头需通过long_take_reason与表演发展审计。"
                )
            if speaker_count >= 2:
                warnings.append(
                    f"{shot_label}含{speaker_count}名明确说话人；"
                    "请检查回答、反驳、揭示、包袱或态度变化是否需要反打或听者反应。"
                )
            if len(current_references) >= 2:
                warnings.append(
                    f"{shot_label}引用了{len(current_references)}张原图；"
                    "请确认它们是同一机位的连续阶段，否则拆成独立编号分镜。"
                )
            if current_references and current_references == previous_references:
                warnings.append(
                    f"{label}{number}的相邻{shot.group(0)}重复同一参考图；"
                    "请确认存在新的主体、景别、视角、构图、画面信息或戏剧功能，否则合并。"
                )
            previous_references = current_references
            if LEGACY_FIELD_RE.search(block):
                errors.append(
                    f"{label}{number}的{shot.group(0)}仍使用景别/构图/运镜/画面内容独立字段。"
                )
            if not BACKGROUND_VISUAL_RE.search(block):
                errors.append(
                    f"{shot_label}缺少可见背景；请写出实体环境、图形背景或填满画面的近景表面。"
                )

        for match in AUDIO_RE.finditer(chunk):
            errors.append(f"{label}{number}含音效或音乐字段：{match.group(0)}")

        for match in META_RE.finditer(chunk):
            errors.append(
                f"{label}{number}含参考分析元表述，请改写为可见画面：{match.group(0)}"
            )

        for match in NEGATIVE_PROMPT_RE.finditer(chunk):
            errors.append(
                f"{label}{number}含否定式构图/运镜限制，请改为正向描述：{match.group(0)}"
            )

        for quote in missing_voice_directions(chunk):
            errors.append(
                f"{label}{number}的语音后缺少音色、语气、情绪括号说明：{quote}"
            )

    validate_chunks(
        [("片段", number, chunk) for number, chunk in chunks],
        require_contiguous_numbers=True,
    )

    safe_chunks = segment_chunks(safe_text, SAFE_SEGMENT_RE) if safe_text else []
    if safe_text and not safe_chunks:
        errors.append("存在平台安全替换稿附录，但未找到替换片段。")
    if safe_chunks:
        safe_numbers = [number for number, _ in safe_chunks]
        duplicates = sorted({n for n in safe_numbers if safe_numbers.count(n) > 1})
        if duplicates:
            errors.append(f"平台安全替换片段编号重复：{duplicates}")
        main_numbers = {number for number, _ in chunks}
        for number in safe_numbers:
            if number not in main_numbers:
                errors.append(f"平台安全替换片段{number}在正文中没有对应片段。")
        validate_chunks(
            [("平台安全替换片段", number, chunk) for number, chunk in safe_chunks],
            require_contiguous_numbers=False,
        )

    for match in FORBIDDEN_RE.finditer(text):
        errors.append(f"发现内部估时说明：{match.group(0)}")

    references = sorted(set(REFERENCE_RE.findall(text)))
    if args.image_dir:
        available = {
            path.name.casefold() for path in args.image_dir.iterdir() if path.is_file()
        }
        for reference in references:
            if Path(reference).name.casefold() not in available:
                errors.append(f"参考图不存在：{reference}")

    if args.dialogue_ledger:
        errors.extend(
            validate_dialogue_ledger(args.dialogue_ledger, main_text, args.image_dir)
        )

    print(f"片段数：{len(chunks)}")
    if safe_chunks:
        print(f"平台安全替换片段数：{len(safe_chunks)}")
    print(f"参考图数：{len(references)}")
    for message in warnings:
        print(f"警告：{message}")
    for message in errors:
        print(f"错误：{message}")

    if errors:
        print(f"验证失败：{len(errors)}个错误，{len(warnings)}个警告。")
        return 1
    print(f"结构验证通过：0个错误，{len(warnings)}个警告。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
