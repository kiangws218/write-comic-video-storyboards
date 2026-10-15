#!/usr/bin/env python3
"""Structurally migrate a V2 source ledger to V3 without fabricating visual audit facts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def mapped_targets(bubble: dict[str, object]) -> list[str]:
    mappings = bubble.get("segments", [bubble])
    if not isinstance(mappings, list):
        return []
    return list(dict.fromkeys(
        str(item.get("target"))
        for item in mappings
        if isinstance(item, dict) and isinstance(item.get("target"), str)
    ))


def dialogue_plan(panel: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    bubbles = panel.get("bubbles")
    if not isinstance(bubbles, list):
        return [], []
    turns: list[dict[str, object]] = []
    for bubble in bubbles:
        if not isinstance(bubble, dict) or bubble.get("status") != "mapped" or bubble.get("kind") == "narration":
            continue
        bubble_id = bubble.get("id")
        speaker = bubble.get("speaker")
        if not isinstance(bubble_id, str) or not bubble_id.strip():
            continue
        if turns and turns[-1].get("speaker") == speaker:
            turns[-1]["bubble_ids"].append(bubble_id)
            turns[-1]["candidate_targets"] = list(dict.fromkeys(
                [*turns[-1]["candidate_targets"], *mapped_targets(bubble)]
            ))
        else:
            turns.append({
                "id": f"t{len(turns) + 1}",
                "bubble_ids": [bubble_id],
                "function": "MIGRATION_REVIEW",
                "speaker": speaker,
                "candidate_targets": mapped_targets(bubble),
            })

    groups: list[dict[str, object]] = []
    for turn in turns:
        targets = turn.pop("candidate_targets")
        turn.pop("speaker", None)
        if groups and groups[-1]["targets"] == targets:
            groups[-1]["turn_ids"].append(turn["id"])
            groups[-1]["merge_basis"] = "MIGRATION_REVIEW:旧台账共用目标，仅作候选分组"
        else:
            groups.append({
                "id": f"g{len(groups) + 1}",
                "turn_ids": [turn["id"]],
                "targets": targets,
            })
    return turns, groups


def migrate(data: dict[str, object]) -> dict[str, object]:
    if data.get("version") != 2:
        raise ValueError("input ledger must use version 2")
    result = json.loads(json.dumps(data, ensure_ascii=False))
    result["version"] = 3
    review: list[str] = []

    for panel in result.get("panels", []):
        if not isinstance(panel, dict):
            continue
        locks = panel.pop("locks", {})
        panel["composition_lock"] = locks.get("composition", "MIGRATION_REVIEW") if isinstance(locks, dict) else "MIGRATION_REVIEW"
        panel["source_facts"] = {
            "entities": locks.get("visible_subjects", []) if isinstance(locks, dict) else [],
            "actions": [],
            "relations": locks.get("relations", []) if isinstance(locks, dict) else [],
        }
        panel["story_context"] = []
        panel["non_renderable_terms"] = []
        panel["renderable_visual"] = True
        panel["page_overlays"] = []
        review.append(f"{panel.get('image')}:重新看图拆分source_facts/story_context/non_renderable_terms/page_overlays")
        bubbles = panel.get("bubbles")
        speakers = {
            bubble.get("speaker")
            for bubble in bubbles or []
            if isinstance(bubble, dict) and bubble.get("status") == "mapped"
        }
        mapped_count = sum(
            isinstance(bubble, dict) and bubble.get("status") == "mapped" and bubble.get("kind") != "narration"
            for bubble in bubbles or []
        )
        if mapped_count >= 2 and (len(speakers) >= 2 or mapped_count >= 3):
            turns, groups = dialogue_plan(panel)
            panel["dialogue_turns"] = turns
            panel["coverage_groups"] = groups
            review.append(f"{panel.get('image')}:复核语义轮次、覆盖分组与合镜依据")

    for shot in result.get("shots", []):
        if not isinstance(shot, dict):
            continue
        shot["fact_claims"] = {"entities": [], "actions": [], "relations": []}
        shot["action_admissions"] = []
        review.append(f"{shot.get('target')}:复核fact_claims与主要动作三问准入")
        if shot.get("role") != "uncited_coverage":
            continue
        shot.setdefault("derived_from", [])
        shot.setdefault("coverage_type", "MIGRATION_REVIEW")
        shot.setdefault("coverage_changes", [])
        shot.setdefault("coverage_evidence", "MIGRATION_REVIEW")
        shot.setdefault("next_source_image", "MIGRATION_REVIEW")
        shot.setdefault("next_source_changes", [])
        shot.setdefault("next_source_evidence", "MIGRATION_REVIEW")
        review.append(f"{shot.get('target')}:复核增镜所属原格、前镜差异、下一原格差异与证据")

    result["migration_review_required"] = review
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8-sig"))
    migrated = migrate(data)
    args.destination.write_text(
        json.dumps(migrated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "destination": str(args.destination.resolve()),
        "review_items": len(migrated.get("migration_review_required", [])),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
