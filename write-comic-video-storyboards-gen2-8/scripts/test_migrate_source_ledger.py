from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("migrate_source_ledger_v2_to_v3.py")


class LedgerMigrationTests(unittest.TestCase):
    def test_migration_preserves_source_data_and_requires_review(self) -> None:
        source_data = {
            "version": 2,
            "source_language": "zh",
            "panels": [{
                "image": "panel.jpg",
                "bubbles": [
                    {"id": "b1", "speaker": "甲", "kind": "dialogue", "status": "mapped", "target": "片段1/分镜1"},
                    {"id": "b2", "speaker": "乙", "kind": "dialogue", "status": "mapped", "target": "片段1/分镜2"},
                ],
            }],
            "shots": [{
                "target": "片段1/分镜2",
                "role": "uncited_coverage",
                "source_images": [],
            }],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "v2.json"
            destination = root / "v3.json"
            source.write_text(json.dumps(source_data, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), str(destination)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            migrated = json.loads(destination.read_text(encoding="utf-8"))
            self.assertEqual(migrated["version"], 3)
            self.assertEqual(migrated["panels"][0]["image"], "panel.jpg")
            self.assertEqual([t["bubble_ids"] for t in migrated["panels"][0]["dialogue_turns"]], [["b1"], ["b2"]])
            self.assertTrue(migrated["migration_review_required"])
            self.assertEqual(migrated["shots"][0]["coverage_type"], "MIGRATION_REVIEW")


if __name__ == "__main__":
    unittest.main()
