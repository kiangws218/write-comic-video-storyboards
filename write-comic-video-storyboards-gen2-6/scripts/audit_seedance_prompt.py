#!/usr/bin/env python3
"""Audit Seedance execution-prompt Markdown produced by the Gen2 storyboard skill."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SEGMENT_RE = re.compile(r"^#{1,6}\s*【片段\s*(\d+)】[^\r\n]*", re.MULTILINE)
FENCE_RE = re.compile(r"```(?:text)?\s*\r?\n(.*?)\r?\n```", re.DOTALL | re.IGNORECASE)
SHOT_RE = re.compile(
    r"(?:^|\n)\s*分镜\s*(\d+)\s*[（(]\s*(\d+(?:\.\d+)?)\s*秒\s*[）)]\s*[：:]",
    re.MULTILINE,
)
LEGACY_TIMECODE_RE = re.compile(
    r"(?:^|\n)\s*\d+(?:\.\d+)?-\d+(?:\.\d+)?秒[：:]", re.MULTILINE
)
MUSIC_RE = re.compile(r"BGM|背景音乐|配乐|旋律|弦乐|木琴|主题曲|配器|音乐贯穿", re.IGNORECASE)
PRODUCTION_NOTE_RE = re.compile(
    r"一次性场景|不单独生成环境图|后期添加|用于衔接|"
    r"预计发声|字符数[：:]|审查说明|合规说明"
)
EVASION_RE = re.compile(
    r"绕过(?:审核|审查|检测)|规避(?:审核|审查|检测)|骗过(?:审核|审查|检测)|"
    r"敏感词替换|平台识别不到|无视平台规则|过审黑话"
)
REFERENCE_META_RE = re.compile(
    r"保持原格(?:姿势|构图|表情)?|与原格一致|原格中|原格般|原格原则|"
    r"(?:按照|依照|按)(?:原格|原图|参考图)(?:进行)?(?:处理|呈现|还原)?|"
    r"(?:背景|画面)(?:按照|依照|按)(?:原格|原图|参考图)(?:进行)?(?:处理|呈现|还原)?"
)
NEGATIVE_CONTROL_RE = re.compile(
    r"不增加|不使用|不推拉|不环绕|不出现|不进入|不显示|不改变|"
    r"不穿透|不继续|不做|不要|避免|无需"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_file", type=Path)
    parser.add_argument("--max-seconds", type=int, default=15)
    parser.add_argument("--max-chars", type=int, default=1900)
    return parser.parse_args()


def chunks(text: str) -> list[tuple[int, str]]:
    matches = list(SEGMENT_RE.finditer(text))
    return [
        (
            int(match.group(1)),
            text[
                match.end() : matches[index + 1].start()
                if index + 1 < len(matches)
                else len(text)
            ],
        )
        for index, match in enumerate(matches)
    ]


def main() -> int:
    args = parse_args()
    text = args.prompt_file.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    parsed = chunks(text)

    if not parsed:
        errors.append("未找到形如‘## 【片段1】’的执行稿标题。")

    numbers = [number for number, _ in parsed]
    if numbers and numbers != list(range(numbers[0], numbers[0] + len(numbers))):
        errors.append(f"片段编号不连续：{numbers}")

    for number, chunk in parsed:
        fences = FENCE_RE.findall(chunk)
        if len(fences) != 1:
            errors.append(f"片段{number}必须且只能包含一个 text 提示词代码块。")
            continue

        prompt = fences[0].strip()
        char_count = len(prompt)
        print(f"片段{number}字符数：{char_count}")
        if char_count > args.max_chars:
            errors.append(
                f"片段{number}为{char_count}字符，超过上限{args.max_chars}。"
            )

        if MUSIC_RE.search(prompt):
            errors.append(f"片段{number}含BGM或音乐提示。")
        if PRODUCTION_NOTE_RE.search(prompt):
            errors.append(f"片段{number}含制作、审查或内部说明。")
        if EVASION_RE.search(prompt):
            errors.append(f"片段{number}含规避平台审查的措辞。")
        if REFERENCE_META_RE.search(prompt):
            errors.append(f"片段{number}含参考分析元表述，应改写为正向可见画面。")
        if NEGATIVE_CONTROL_RE.search(prompt):
            errors.append(f"片段{number}含否定式控制，应改写为正向可见结果。")

        shots = list(SHOT_RE.finditer(prompt))
        if not shots:
            if LEGACY_TIMECODE_RE.search(prompt):
                errors.append(f"片段{number}仍使用旧时间段，应改为‘分镜1（3秒）’格式。")
            else:
                errors.append(f"片段{number}没有整数分镜时长。")
            continue

        shot_numbers: list[int] = []
        total_duration = 0
        for match in shots:
            shot_raw, duration_raw = match.groups()
            shot_numbers.append(int(shot_raw))
            if "." in duration_raw:
                errors.append(f"片段{number}含小数时长：{match.group(0).strip()}")
                continue
            duration = int(duration_raw)
            if duration <= 0:
                errors.append(f"片段{number}时长必须大于0秒：{match.group(0).strip()}")
            total_duration += duration

        expected = list(range(1, len(shot_numbers) + 1))
        if shot_numbers != expected:
            errors.append(f"片段{number}分镜编号应从1连续递增：{shot_numbers}")
        if total_duration > args.max_seconds:
            errors.append(
                f"片段{number}总时长{total_duration}秒，超过{args.max_seconds}秒。"
            )

    for warning in warnings:
        print(f"警告：{warning}")
    for error in errors:
        print(f"错误：{error}")

    if errors:
        print(f"审计失败：{len(errors)}个错误，{len(warnings)}个警告。")
        return 1
    print(f"审计通过：0个错误，{len(warnings)}个警告。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
