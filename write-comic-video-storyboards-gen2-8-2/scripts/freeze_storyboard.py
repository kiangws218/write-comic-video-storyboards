#!/usr/bin/env python3
"""Freeze checked second-reading facts/text, or print a review digest (never approve)."""
import argparse
import json
from pathlib import Path
from validate_director import POLICY, make_source_lock, review_digest
from authoring import check_routes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--review-digest", type=Path, help="Print only; does not create or approve a review.")
    parser.add_argument("--correction-reason", help="Explicit source/translation correction; keep prior lock in audit.")
    args = parser.parse_args()
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8-sig"))
        if not isinstance(ledger, dict) or ledger.get("version") != 3 or ledger.get("skill_version") != POLICY:
            raise ValueError("须为version:3、skill_version:2.8.2的真实台账；本工具不迁移或补审查状态")
        check_routes(ledger)
        if args.review_digest:
            print(review_digest(ledger, args.review_digest.read_text(encoding="utf-8")))
            return 0
        old = ledger.get("source_lock")
        if old and not args.correction_reason:
            raise ValueError("已有来源锁，拒绝覆盖；真实纠错须--correction-reason并回图核对")
        if args.correction_reason:
            if not args.correction_reason.strip():
                raise ValueError("纠错原因不能为空")
            history = ledger.setdefault("source_lock_history", [])
            if not isinstance(history, list):
                raise ValueError("source_lock_history须为数组")
            history.append({"previous_lock": old, "reason": args.correction_reason})
        ledger["source_lock"] = make_source_lock(ledger)
        # A new lock invalidates a former final review, without pretending it was rerun.
        ledger.pop("director_review", None)
        args.ledger.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("已记录来源／全文一致性锁；未创建任何看图、导演或视觉审查通过状态。")
        return 0
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f"无法冻结：{exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
