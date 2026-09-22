#!/usr/bin/env python3
"""Reproduce Gen2.6/Gen2.7 rule and storyboard comparison metrics."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def token_proxy(text: str) -> int:
    """Estimate mixed Chinese/Japanese/English tokens; not an API bill."""
    cjk = sum(1 for c in text if "\u3400" <= c <= "\u9fff" or "\u3040" <= c <= "\u30ff")
    remainder = re.sub(r"[\u3400-\u9fff\u3040-\u30ff]", " ", text)
    ascii_runs = re.findall(r"[A-Za-z0-9_]+", remainder)
    punctuation = sum(1 for c in re.sub(r"[A-Za-z0-9_\s]", "", remainder))
    return cjk + sum(math.ceil(len(run) / 4) for run in ascii_runs) + math.ceil(punctuation / 2)


def load_many(paths: list[str]) -> str:
    return "\n".join((ROOT / path).read_text(encoding="utf-8") for path in paths)


def storyboard_metrics(path: str, ledger_path: str) -> dict[str, int | float]:
    text = (ROOT / path).read_text(encoding="utf-8")
    ledger = json.loads((ROOT / ledger_path).read_text(encoding="utf-8"))
    durations = [int(v) for v in re.findall(r"分镜\d+（(\d+)秒）", text)]
    shots = len(durations)
    result: dict[str, int | float] = {
        "characters": len(text),
        "token_proxy": token_proxy(text),
        "clips": len(re.findall(r"^## 【片段", text, re.MULTILINE)),
        "shots": shots,
        "runtime_seconds": sum(durations),
        "characters_per_shot": round(len(text) / shots, 1),
        "source_panels": len(ledger["panels"]),
        "mapped_bubbles": sum(len(panel["bubbles"]) for panel in ledger["panels"]),
        "head_face_signals": len(re.findall(r"视线|目光|瞳孔|眼睑|眉|嘴角|嘴唇|下巴|侧脸|正脸", text)),
        "light_material_signals": len(re.findall(r"轮廓|高光|反射|折射|漫射|背光|侧逆光|二分|材质|颗粒|暗部", text)),
    }
    for field in ("场景环境", "环境音", "镜头设计", "可见动作", "光影布光", "声音设计"):
        values = re.findall(rf"^{field}：(.*)$", text, re.MULTILINE)
        result[f"avg_{field}"] = round(sum(map(len, values)) / len(values), 1)
    return result


def main() -> None:
    rule_sets = {
        "gen2.6_cinematic": [
            "write-comic-video-storyboards-gen2-6/SKILL.md",
            "write-comic-video-storyboards-gen2-6/references/source-grounding.md",
            "write-comic-video-storyboards-gen2-6/references/dialogue-coverage.md",
            "write-comic-video-storyboards-gen2-6/references/performance-choreography.md",
            "write-comic-video-storyboards-gen2-6/references/audio-design.md",
            "write-comic-video-storyboards-gen2-6/references/storyboard-format.md",
            "write-comic-video-storyboards-gen2-6/references/cinematic-quality.md",
            "write-comic-video-storyboards-gen2-6/references/cinematic-rendering.md",
        ],
        "gen2.7_cinematic": [
            "write-comic-video-storyboards-gen2-7/SKILL.md",
            "write-comic-video-storyboards-gen2-7/references/core-authoring.md",
            "write-comic-video-storyboards-gen2-7/references/dialogue-performance.md",
            "write-comic-video-storyboards-gen2-7/references/cinematic-rendering.md",
        ],
        "gen2.7_cinematic_source_risk": [
            "write-comic-video-storyboards-gen2-7/SKILL.md",
            "write-comic-video-storyboards-gen2-7/references/core-authoring.md",
            "write-comic-video-storyboards-gen2-7/references/dialogue-performance.md",
            "write-comic-video-storyboards-gen2-7/references/cinematic-rendering.md",
            "write-comic-video-storyboards-gen2-7/references/source-risk.md",
        ],
    }
    rules = {}
    for name, paths in rule_sets.items():
        text = load_many(paths)
        rules[name] = {"characters": len(text), "token_proxy": token_proxy(text)}
    storyboards = {
        "gen2.6": storyboard_metrics(
            "tests/results/gen2.6-cinematic/ch15-first8/storyboard.md",
            "tests/results/gen2.6-cinematic/ch15-first8/source-ledger.json",
        ),
        "gen2.7": storyboard_metrics(
            "tests/results/gen2.7/ch15-first8/storyboard.md",
            "tests/results/gen2.7/ch15-first8/source-ledger.json",
        ),
    }
    print(json.dumps({"rules": rules, "storyboards": storyboards}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
