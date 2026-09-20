from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_storyboard.py")
SHORT_LINE = "あの……お客さん？"
BACKGROUND = "暖象牙色向淡天蓝渐变铺满背景"


def storyboard(line: str | None = SHORT_LINE, background: str = BACKGROUND) -> str:
    performance = (
        "人物手指轻微收紧。"
        if line is None
        else f"人物：“{line}”（清晰的中性音色，平静语气）。"
    )
    return f"""## 场景色彩基准
二维手绘质感，中等对比。

## 【片段1】测试

**分镜1（5秒）：**
分镜参考 `[panel.jpg]`
平视手部特写，固定镜头。{performance}{background}，深蓝灰放射线向外扩张。
"""


def valid_ledger(line: str = SHORT_LINE) -> dict:
    return {
        "version": 2,
        "panels": [
            {
                "image": "panel.jpg",
                "viewed_at_drafting": True,
                "source_bubble_count": 1,
                "bubble_audit": "pass",
                "background": {
                    "type": "graphic",
                    "description": BACKGROUND,
                    "evidence": "current_panel",
                },
                "locks": {
                    "composition": "平视手部特写",
                    "visible_subjects": ["一只手"],
                    "relations": ["手位于画面下方"],
                    "forbidden_inferences": ["第二只手"],
                },
                "coverage": "shared",
                "coverage_reason": "单句台词与手部动作同步",
                "bubbles": [
                    {
                        "id": "b1",
                        "speaker": "店员",
                        "kind": "dialogue",
                        "source_text": "那个……客人？",
                        "status": "mapped",
                        "script_text": line,
                        "seconds": 2,
                        "target": "片段1/分镜1",
                    }
                ],
            }
        ],
        "shots": [
            {
                "target": "片段1/分镜1",
                "role": "source_locked",
                "source_images": ["panel.jpg"],
                "evidence": "current_panel",
                "purpose": "原格手部与台词节点",
                "background_excerpt": BACKGROUND,
                "viewed_while_writing": True,
                "source_audit": "pass",
                "unsupported_additions": [],
            }
        ],
        "performance": [],
    }


class ValidatorTests(unittest.TestCase):
    def run_validator(
        self,
        text: str,
        ledger: dict | None = None,
        require_ledger: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            storyboard_path = root / "storyboard.md"
            storyboard_path.write_text(text, encoding="utf-8")
            image_path = root / "panel.jpg"
            image_path.write_bytes(b"fixture")
            command = [
                sys.executable,
                str(SCRIPT),
                str(storyboard_path),
                "--image-dir",
                str(root),
            ]
            if ledger is not None:
                ledger_path = root / "source-ledger.json"
                ledger_path.write_text(
                    json.dumps(ledger, ensure_ascii=False), encoding="utf-8"
                )
                command.extend(["--source-ledger", str(ledger_path)])
            if require_ledger:
                command.append("--require-source-ledger")
            environment = os.environ.copy()
            environment["PYTHONUTF8"] = "1"
            return subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=environment,
                check=False,
            )

    def test_valid_v2_grounded_storyboard_passes(self) -> None:
        result = self.run_validator(storyboard(), valid_ledger(), require_ledger=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bare_background_label_fails(self) -> None:
        text = storyboard(background="背景").replace("，深蓝灰放射线向外扩张", "")
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("缺少可见背景", result.stdout)

    def test_official_template_quote_is_counted(self) -> None:
        long_line = "あ" * 50
        result = self.run_validator(storyboard(line=long_line))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("含50个有意义的台词字符", result.stdout)

    def test_required_ledger_cannot_be_omitted(self) -> None:
        result = self.run_validator(storyboard(), require_ledger=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--source-ledger版本2", result.stdout)

    def test_long_turn_requires_split_or_exception(self) -> None:
        long_line = "あ" * 50
        ledger = valid_ledger(long_line)
        result = self.run_validator(storyboard(line=long_line), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("必须至少两个目标分镜或登记long_take_reason", result.stdout)

    def test_source_locked_shot_requires_open_image_attestation(self) -> None:
        ledger = deepcopy(valid_ledger())
        ledger["shots"][0]["viewed_while_writing"] = False
        result = self.run_validator(storyboard(), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("未确认在原图打开时写作", result.stdout)

    def test_background_excerpt_must_appear_in_shot(self) -> None:
        ledger = deepcopy(valid_ledger())
        ledger["shots"][0]["background_excerpt"] = "不存在的深紫色墙面"
        result = self.run_validator(storyboard(), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("background_excerpt未出现在分镜正文", result.stdout)

    def test_panel_without_dialogue_uses_none_coverage(self) -> None:
        ledger = deepcopy(valid_ledger())
        panel = ledger["panels"][0]
        panel["source_bubble_count"] = 0
        panel["coverage"] = "none"
        panel["bubbles"] = []
        result = self.run_validator(storyboard(line=None), ledger, True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_three_bubbles_two_speakers_need_split_or_shared_reason(self) -> None:
        lines = [("甲", "はい"), ("乙", "いいえ"), ("甲", "そうです")]
        spoken = "".join(
            f"{speaker}：“{line}”（清晰的中性音色，平静语气）。"
            for speaker, line in lines
        )
        original = f"人物：“{SHORT_LINE}”（清晰的中性音色，平静语气）。"
        text = storyboard().replace(original, spoken)
        ledger = deepcopy(valid_ledger())
        panel = ledger["panels"][0]
        panel["source_bubble_count"] = 3
        panel.pop("shared_reason", None)
        panel["bubbles"] = [
            {
                "id": f"b{index}",
                "speaker": speaker,
                "speaker_evidence": f"气泡尾指向{speaker}",
                "kind": "dialogue",
                "source_text": line,
                "status": "mapped",
                "script_text": line,
                "seconds": 1,
                "target": "片段1/分镜1",
            }
            for index, (speaker, line) in enumerate(lines, start=1)
        ]
        result = self.run_validator(text, ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("单镜需shared_reason", result.stdout)


if __name__ == "__main__":
    unittest.main()
