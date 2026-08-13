#!/usr/bin/env python3
"""Validate Markdown storyboards produced from sequential comic panels."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SEGMENT_RE = re.compile(r"^#{1,6}\s*【片段\s*(\d+)】", re.MULTILINE)
TIMECODE_RE = re.compile(r"\*\*(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)s[：:]\*\*")
REFERENCE_RE = re.compile(
    r"(?:分镜参考|参考)?\s*`?\[([^\]\r\n]+\.(?:png|jpe?g|webp))\]`?",
    re.IGNORECASE,
)
FORBIDDEN_RE = re.compile(r"预计发声|约\s*\d+(?:\.\d+)?\s*秒")
PRODUCTION_NOTE_RE = re.compile(
    r"一次性场景|不单独生成环境图|不建立独立背景|视频生成时|"
    r"后期添加|用于衔接|为下一片段(?:对白)?衔接|避免乱码"
)
FIELD_NAMES = ("景别", "构图", "运镜", "画面内容")
ENVIRONMENT_RE = re.compile(r"^环境参考[：:]", re.MULTILINE)
MUSIC_RE = re.compile(
    r"音效[：:][^\r\n]*(?:BGM|配乐|音乐|旋律|弦乐|木琴|主题曲|配器)",
    re.IGNORECASE,
)
NEGATIVE_PROMPT_RE = re.compile(
    r"^(?:构图|运镜)[：:][^\r\n]*(?:不增加|不使用|不推拉|不环绕|"
    r"不出现|不进入|不显示|不改变|不穿透|不继续)",
    re.MULTILINE,
)
QUOTE_RE = re.compile(r"“([^”]+)”")
SPEECH_HINT_RE = re.compile(
    r"旁白|说道|说着|说|喊道|喊|问道|问|答道|回答|解释|嘟囔|"
    r"低声|高声|叫道|念道|宣布|开口"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--max-seconds", type=int, default=15)
    parser.add_argument("--image-dir", type=Path)
    return parser.parse_args()


def segment_chunks(text: str) -> list[tuple[int, str]]:
    matches = list(SEGMENT_RE.finditer(text))
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
        if not line.startswith("画面内容："):
            continue
        for match in QUOTE_RE.finditer(line):
            prefix = line[: match.start()]
            # Ignore quoted keywords inside an existing voice-direction parenthesis.
            if prefix.count("（") > prefix.count("）"):
                continue
            nearby = prefix[max(0, len(prefix) - 40) :]
            if not SPEECH_HINT_RE.search(nearby):
                continue
            suffix = line[match.end() :]
            if not re.match(r"\s*[。！？!?]?\s*（", suffix):
                missing.append(match.group(1))
    return missing


def main() -> int:
    args = parse_args()
    text = args.storyboard.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    chunks = segment_chunks(text)
    if not chunks:
        errors.append("未找到形如‘## 【片段1】’的片段标题。")

    numbers = [number for number, _ in chunks]
    if numbers and numbers != list(range(numbers[0], numbers[0] + len(numbers))):
        errors.append(f"片段编号不连续：{numbers}")

    for number, chunk in chunks:
        timecodes = list(TIMECODE_RE.finditer(chunk))
        if not timecodes:
            errors.append(f"片段{number}没有时间码。")
            continue

        previous_end: int | None = None
        for match in timecodes:
            start_raw, end_raw = match.groups()
            if "." in start_raw or "." in end_raw:
                errors.append(f"片段{number}含小数时间码：{match.group(0)}")
                continue
            start, end = int(start_raw), int(end_raw)
            if start > end:
                errors.append(f"片段{number}时间倒置：{match.group(0)}")
            if end > args.max_seconds:
                errors.append(f"片段{number}超过{args.max_seconds}秒：{match.group(0)}")
            if previous_end is None and start != 0:
                errors.append(f"片段{number}没有从0秒开始：{match.group(0)}")
            if previous_end is not None and start != previous_end + 1:
                errors.append(
                    f"片段{number}时间不连续：上一段结束于{previous_end}s，"
                    f"下一段开始于{start}s。"
                )
            previous_end = end

        if previous_end is not None and previous_end < args.max_seconds:
            warnings.append(
                f"片段{number}在{previous_end}s结束，未使用完整{args.max_seconds}秒。"
            )

        for match in PRODUCTION_NOTE_RE.finditer(chunk):
            errors.append(
                f"片段{number}含制作流程说明，不是可直接生成的提示词：{match.group(0)}"
            )

        environment_matches = list(ENVIRONMENT_RE.finditer(chunk))
        if len(environment_matches) > 1:
            errors.append(f"片段{number}重复写了环境参考，应只在片段标题下写一次。")
        if timecodes and any(match.start() > timecodes[0].start() for match in environment_matches):
            errors.append(f"片段{number}把环境参考写进了时间块。")

        for index, timecode in enumerate(timecodes):
            block_end = (
                timecodes[index + 1].start()
                if index + 1 < len(timecodes)
                else len(chunk)
            )
            block = chunk[timecode.end() : block_end]
            positions: list[int] = []
            for field in FIELD_NAMES:
                field_match = re.search(rf"^{field}[：:]", block, re.MULTILINE)
                if field_match is None:
                    errors.append(
                        f"片段{number}的{timecode.group(0)}缺少‘{field}：’字段。"
                    )
                else:
                    positions.append(field_match.start())
            if len(positions) == len(FIELD_NAMES) and positions != sorted(positions):
                errors.append(
                    f"片段{number}的{timecode.group(0)}字段顺序应为"
                    "景别、构图、运镜、画面内容。"
                )

        for match in MUSIC_RE.finditer(chunk):
            errors.append(f"片段{number}含BGM或音乐提示：{match.group(0)}")

        for match in NEGATIVE_PROMPT_RE.finditer(chunk):
            errors.append(
                f"片段{number}含否定式构图/运镜限制，请改为正向描述：{match.group(0)}"
            )

        for quote in missing_voice_directions(chunk):
            errors.append(
                f"片段{number}的语音后缺少音色、语气、情绪括号说明：{quote}"
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

    print(f"片段数：{len(chunks)}")
    print(f"参考图数：{len(references)}")
    for message in warnings:
        print(f"警告：{message}")
    for message in errors:
        print(f"错误：{message}")

    if errors:
        print(f"验证失败：{len(errors)}个错误，{len(warnings)}个警告。")
        return 1
    print(f"验证通过：0个错误，{len(warnings)}个警告。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
