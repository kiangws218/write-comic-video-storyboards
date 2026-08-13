#!/usr/bin/env python3
"""Audit Seedance execution-prompt Markdown produced by the Gen2 storyboard skill."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SEGMENT_RE = re.compile(r"^#{1,6}\s*【片段\s*(\d+)】[^\r\n]*", re.MULTILINE)
FENCE_RE = re.compile(r"```(?:text)?\s*\r?\n(.*?)\r?\n```", re.DOTALL | re.IGNORECASE)
TIMECODE_RE = re.compile(r"(?:^|\n)\s*(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)秒[：:]", re.MULTILINE)
MUSIC_RE = re.compile(r"BGM|背景音乐|配乐|旋律|弦乐|木琴|主题曲|配器|音乐贯穿", re.IGNORECASE)
PRODUCTION_NOTE_RE = re.compile(
    r"一次性场景|不单独生成环境图|后期添加|用于衔接|"
    r"预计发声|字符数[：:]|审查说明|合规说明"
)
EVASION_RE = re.compile(
    r"绕过(?:审核|审查|检测)|规避(?:审核|审查|检测)|骗过(?:审核|审查|检测)|"
    r"敏感词替换|平台识别不到|无视平台规则|过审黑话"
)
SHOT_LABEL_RE = re.compile(r"(?:Shot\s*\d+|镜头\s*\d+)\s*[：:]", re.IGNORECASE)
NEGATIVE_CAMERA_RE = re.compile(r"不使用环绕镜头|不环绕|不推拉|不增加其他|不出现其他")


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
        if "〖时间轴〗" in prompt and SHOT_LABEL_RE.search(prompt):
            errors.append(f"片段{number}混用了时间轴与Shot/镜头编号骨架。")
        if NEGATIVE_CAMERA_RE.search(prompt):
            warnings.append(f"片段{number}含否定式控制，建议改写为正向可见结果。")

        timecodes = list(TIMECODE_RE.finditer(prompt))
        if not timecodes:
            errors.append(f"片段{number}没有整数时间轴。")
            continue

        previous_end: int | None = None
        for match in timecodes:
            start_raw, end_raw = match.groups()
            if "." in start_raw or "." in end_raw:
                errors.append(f"片段{number}含小数时间码：{match.group(0).strip()}")
                continue
            start, end = int(start_raw), int(end_raw)
            if start > end:
                errors.append(f"片段{number}时间倒置：{match.group(0).strip()}")
            if end > args.max_seconds:
                errors.append(
                    f"片段{number}超过{args.max_seconds}秒：{match.group(0).strip()}"
                )
            if previous_end is None and start != 0:
                errors.append(f"片段{number}没有从0秒开始。")
            if previous_end is not None and start != previous_end + 1:
                errors.append(
                    f"片段{number}时间不连续：上一段结束于{previous_end}秒，"
                    f"下一段开始于{start}秒。"
                )
            previous_end = end

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
