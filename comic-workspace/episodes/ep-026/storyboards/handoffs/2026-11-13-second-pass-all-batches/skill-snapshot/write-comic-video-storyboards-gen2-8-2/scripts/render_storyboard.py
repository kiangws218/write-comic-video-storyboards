#!/usr/bin/env python3
"""Render actual planned fields; do not invent roles, text, evidence, cards or approvals."""
import argparse
import json
import re
from pathlib import Path
from validate_director import FIELDS, POLICY
from authoring import check_confirmations, expand, duration_seconds, format_seconds, action_timeline_errors


def render(ledger):
    if not isinstance(ledger, dict):
        raise ValueError("台账根须为对象")
    check_confirmations(ledger)
    ledger = expand(ledger)
    if ledger.get("skill_version") != POLICY:
        raise ValueError("只渲染2.8.2；不能自动升级旧审查记录")
    look = ledger.get("look")
    if not isinstance(look, str) or not look.strip():
        raise ValueError("缺少实际场景色彩基准look")
    lines = ["## 场景色彩基准", look, ""]
    unknown = [p for p in ledger.get("character_registry", [])
               if isinstance(p, dict) and p.get("identity_status") == "unidentified"]
    if unknown:
        lines += ["## 新角色上色提示词", ""]
        for person in unknown:
            if not all(isinstance(person.get(k), str) and person[k].strip()
                       for k in ("id", "canonical_name", "color_prompt")):
                raise ValueError("未识别角色须有稳定ID、统一称呼和实际上色提示词")
            lines += [f"- {person['id']}｜{person['canonical_name']}：{person['color_prompt']}"]
        lines.append("")
    clip_totals = {}
    for shot in ledger.get("shots", []):
        clip = str(shot.get("target", "")).split("/", 1)[0]
        clip_totals[clip] = clip_totals.get(clip, 0) + duration_seconds(shot.get("duration"))
    last_clip, last_shot = 0, 0
    for shot in ledger.get("shots", []):
        m = re.fullmatch(r"片段(\d+)/分镜(\d+)", str(shot.get("target", "")))
        if not m:
            raise ValueError("每个真实切镜须有片段N/分镜N目标")
        clip, number = map(int, m.groups())
        duration = shot.get("duration")
        if not isinstance(duration, (int, float)):
            raise ValueError("镜头duration须为数值，不自动填满片段")
        duration_seconds(duration)
        if clip != last_clip:
            if clip != last_clip + 1 or number != 1:
                raise ValueError("片段须连续，分镜从1开始")
            lines += [f"## 【片段{clip}】（{format_seconds(clip_totals[f'片段{clip}'])}秒）", ""]
            last_clip, last_shot = clip, 0
        if number != last_shot + 1:
            raise ValueError("分镜须连续编号")
        last_shot = number
        fields = shot.get("fields")
        if not isinstance(fields, dict) or any(not isinstance(fields.get(k), str) or not fields[k].strip() for k in FIELDS):
            raise ValueError(f"{shot['target']}缺少实际六字段，拒绝套模板补表演")
        timeline_errors = action_timeline_errors(fields["可见动作"], duration, shot["target"])
        if timeline_errors:
            raise ValueError("；".join(timeline_errors))
        lines.append(f"**分镜{number}（{format_seconds(duration)}秒）：**")
        if shot.get("role") == "source_locked":
            refs = shot.get("source_images")
            if not isinstance(refs, list) or not refs or any(not isinstance(r, str) for r in refs):
                raise ValueError("原作镜头须登记真实源画面；连续原格可按阶段合并")
            lines.append("分镜参考 " + "、".join(f"`[{r}]`" for r in refs))
        elif shot.get("role") not in {"source_supported_phase", "uncited_coverage"}:
            raise ValueError("必须提供真实role，不默认设置source_locked")
        lines += [f"【{k}】：{fields[k]}" for k in FIELDS] + [""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        text = render(json.loads(args.ledger.read_text(encoding="utf-8-sig")))
        args.output.write_text(text, encoding="utf-8")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, f"无法渲染：{exc}\n")


if __name__ == "__main__":
    main()
