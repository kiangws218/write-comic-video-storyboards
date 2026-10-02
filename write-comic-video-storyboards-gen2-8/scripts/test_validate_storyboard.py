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
    action = "人物手指轻微收紧后停住。" if line is None else "人物手掌朝上托住物件，手指先放松再轻微收紧。"
    speech = "无台词。" if line is None else f"人物：“{line}”（清晰的中性音色，平静语气）。"
    return f"""## 场景色彩基准
二维手绘质感，中等对比。

## 【片段1】测试

**分镜1（5秒）：**
分镜参考 `[panel.jpg]`
【镜头设计】：50mm平视手部特写，手腕被下缘裁切，掌心占中央前景；固定镜头。
【可见动作】：{action}
【可见背景】：{background}，深蓝灰放射线向外扩张。
【台词与语气】：{speech}
【光影布光】：柔和侧光照亮手指轮廓，掌心保留浅影。
【声音设计】：低环境底噪从画面后方持续传来，手指收紧时衣料轻响。
"""


def valid_ledger(line: str = SHORT_LINE) -> dict:
    return {
        "version": 3,
        "source_language": "zh",
        "panels": [
            {
                "image": "panel.jpg",
                "viewed_at_drafting": True,
                "drafting_resolution": "720p",
                "source_bubble_count": 1,
                "bubble_audit": "pass",
                "background": {
                    "type": "graphic",
                    "description": BACKGROUND,
                    "evidence": "current_panel",
                },
                "composition_lock": "平视手部特写，手腕从画面下缘裁切，掌心占中央前景",
                "source_facts": {
                    "entities": ["一只手"],
                    "actions": [],
                    "relations": ["手位于画面下方"],
                },
                "story_context": ["店员正在向画外客人说话"],
                "non_renderable_terms": ["客人"],
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
                "fact_claims": {
                    "entities": ["一只手"],
                    "actions": [],
                    "relations": ["手位于画面下方"],
                },
                "action_admissions": [],
                "risk_flags": [],
                "risk_basis": "单气泡短句；手部关系清楚，无脆弱几何",
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
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("含50个有意义的台词字符", result.stdout)

    def test_required_ledger_cannot_be_omitted(self) -> None:
        result = self.run_validator(storyboard(), require_ledger=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--source-ledger版本3", result.stdout)

    def test_long_turn_requires_split_without_exception(self) -> None:
        long_line = "あ" * 50
        ledger = valid_ledger(long_line)
        ledger["panels"][0]["long_take_reason"] = "单镜内持续表演"
        ledger["performance"] = [{
            "target": "片段1/分镜1",
            "evidence": "当前面板",
            "details": ["手掌朝上", "手指稳定", "托住画外物件"],
            "intervals": [{"speech_seconds": 2, "acting_seconds": 2}],
            "long_take_reason": "单镜内持续表演",
        }]
        result = self.run_validator(storyboard(line=long_line), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("long_take_reason不能豁免", result.stdout)

    def test_multiple_short_quotes_over_shot_limit_require_split(self) -> None:
        line = "あ" * 22
        original = f'人物：“{SHORT_LINE}”（清晰的中性音色，平静语气）。'
        replacement = (
            f'人物：“{line}”（清晰的中性音色，平静语气）。\n'
            f'人物：“{line}”（清晰的中性音色，平静语气）。'
        )
        result = self.run_validator(storyboard().replace(original, replacement))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("含44个有意义的台词字符", result.stdout)

    def test_source_locked_shot_requires_open_image_attestation(self) -> None:
        ledger = deepcopy(valid_ledger())
        ledger["shots"][0]["viewed_while_writing"] = False
        result = self.run_validator(storyboard(), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("未确认在原图打开时写作", result.stdout)

    def test_story_context_term_cannot_leak_into_renderable_fields(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物手指先放松再轻微收紧，随后看向客人。",
        )
        result = self.run_validator(text, valid_ledger(), True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("仅属story_context的内容泄漏", result.stdout)

    def test_fact_claim_outside_source_allowlist_fails(self) -> None:
        ledger = valid_ledger()
        ledger["shots"][0]["fact_claims"]["entities"].append("矮人")
        result = self.run_validator(storyboard(), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("不在源图允许表中", result.stdout)

    def test_dialogue_meaning_cannot_admit_major_action(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物先转身，随后停住。",
        )
        ledger = valid_ledger()
        ledger["panels"][0]["source_facts"]["actions"] = ["人物:转身"]
        ledger["shots"][0]["fact_claims"]["actions"] = ["人物:转身"]
        ledger["shots"][0]["action_admissions"] = [{
            "claim": "转身", "source_image": "panel.jpg",
            "visual_evidence": "台词说现在快跑",
            "visible_in_framing": True, "anchor_safe": True,
        }]
        result = self.run_validator(text, ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("仅用台词/剧情作证", result.stdout)

    def test_visual_three_gate_action_admission_passes(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物先转身，随后停住。",
        )
        ledger = valid_ledger()
        ledger["panels"][0]["source_facts"]["actions"] = ["人物:转身"]
        ledger["shots"][0]["fact_claims"]["actions"] = ["人物:转身"]
        ledger["shots"][0]["action_admissions"] = [{
            "claim": "转身", "source_image": "panel.jpg",
            "visual_evidence": "当前格肩线与头部朝向发生连续变化",
            "visible_in_framing": True, "anchor_safe": True,
        }]
        result = self.run_validator(text, ledger, True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_background_excerpt_must_appear_in_shot(self) -> None:
        ledger = deepcopy(valid_ledger())
        ledger["shots"][0]["background_excerpt"] = "不存在的深紫色墙面"
        result = self.run_validator(storyboard(), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("background_excerpt未出现在分镜正文", result.stdout)

    def test_p_risk_requires_compact_performance_card(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物先看向掌心，眉尾先抬起，嘴角随后压平；手指跟着收紧，袖口迟半拍回落，最后视线停在掌心。",
        )
        ledger = valid_ledger()
        ledger["shots"][0]["risk_flags"] = ["P"]
        ledger["performance"] = [{
            "target": "片段1/分镜1",
            "evidence": "当前面板可见脸部、手掌和袖口",
            "details": ["眉尾先抬起", "袖口迟半拍回落"],
            "intervals": [{"speech_seconds": 2.1, "acting_seconds": 3}],
        }]
        result = self.run_validator(text, ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("标记P但缺少performance.card", result.stdout)

    def test_p_risk_with_card_and_rendered_chain_passes(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物先看向掌心，眉尾先抬起，嘴角随后压平；手指跟着收紧，袖口迟半拍回落，最后视线停在掌心。",
        )
        ledger = valid_ledger()
        ledger["shots"][0]["risk_flags"] = ["P"]
        ledger["performance"] = [{
            "target": "片段1/分镜1",
            "evidence": "当前面板可见脸部、手掌和袖口",
            "card": {
                "opening": "视线落在掌心",
                "beats": ["眉尾先抬", "嘴角随后压平"],
                "coupling": "手指收紧带动袖口迟落",
                "landing": "视线停在掌心，固定镜头",
            },
            "details": ["眉尾先抬起", "袖口迟半拍回落"],
            "intervals": [{"speech_seconds": 2.1, "acting_seconds": 3}],
        }]
        result = self.run_validator(text, ledger, True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_panel_without_dialogue_uses_none_coverage(self) -> None:
        ledger = deepcopy(valid_ledger())
        panel = ledger["panels"][0]
        panel["source_bubble_count"] = 0
        panel["coverage"] = "none"
        panel["bubbles"] = []
        result = self.run_validator(storyboard(line=None), ledger, True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_multi_turn_panel_requires_coverage_groups(self) -> None:
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
        panel["bubbles"] = [
            {
                "id": f"b{index}",
                "speaker": speaker,
                "speaker_evidence": f"气泡尾指向{speaker}",
                "kind": "dialogue",
                "source_text": f"原文{index}",
                "status": "mapped",
                "script_text": line,
                "seconds": 1,
                "target": "片段1/分镜1",
            }
            for index, (speaker, line) in enumerate(lines, start=1)
        ]
        panel["dialogue_turns"] = [
            {
                "id": f"t{index}",
                "bubble_ids": [f"b{index}"],
                "function": function,
            }
            for index, function in enumerate(["提问", "回答", "反驳"], start=1)
        ]
        result = self.run_validator(text, ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("缺少coverage_groups", result.stdout)

    def test_three_semantic_turns_pass_with_three_shots_in_one_clip(self) -> None:
        text = storyboard(line="えっ。") + """
**分镜2（3秒）：**
【镜头设计】：85mm侧向脸部特写，乙占画面右侧，固定镜头。
【可见动作】：乙先抬眼，嘴唇张开后停住。
【可见背景】：暖象牙色向淡天蓝渐变铺满背景，深蓝灰放射线向外扩张。
【台词与语气】：乙：“何してるの。”（清晰女声，直接质问）。
【光影布光】：柔和侧光照亮眼缘，脸侧保留浅影。
【声音设计】：低环境底噪持续，句末短暂停顿。

**分镜3（3秒）：**
【镜头设计】：70mm正面脸部近景，甲占画面左侧，镜头轻推后停住。
【可见动作】：甲先躲开视线，随后急促摇头，最后抿住嘴唇。
【可见背景】：暖象牙色向淡天蓝渐变铺满背景，深蓝灰放射线向外扩张。
【台词与语气】：甲：“違う！”（清晰女声，慌乱否认）。
【光影布光】：柔和侧光照亮发缘，脸颊保留浅影。
【声音设计】：低环境底噪持续，摇头时发丝轻响。
"""
        ledger = valid_ledger("えっ。")
        panel = ledger["panels"][0]
        panel["source_bubble_count"] = 3
        panel["coverage"] = "reverse"
        panel["bubbles"] = [
            {
                "id": "b1", "speaker": "甲", "speaker_evidence": "气泡尾指向甲",
                "kind": "dialogue", "source_text": "什么？", "status": "mapped",
                "script_text": "えっ。", "seconds": 1, "target": "片段1/分镜1",
            },
            {
                "id": "b2", "speaker": "乙", "speaker_evidence": "气泡尾指向乙",
                "kind": "dialogue", "source_text": "你在做什么？", "status": "mapped",
                "script_text": "何してるの。", "seconds": 2, "target": "片段1/分镜2",
            },
            {
                "id": "b3", "speaker": "甲", "speaker_evidence": "气泡尾指向甲",
                "kind": "dialogue", "source_text": "不是！", "status": "mapped",
                "script_text": "違う！", "seconds": 1, "target": "片段1/分镜3",
            },
        ]
        panel["dialogue_turns"] = [
            {"id": "t1", "bubble_ids": ["b1"], "function": "被撞见"},
            {"id": "t2", "bubble_ids": ["b2"], "function": "质问"},
            {"id": "t3", "bubble_ids": ["b3"], "function": "否认"},
        ]
        panel["coverage_groups"] = [
            {"id": "g1", "turn_ids": ["t1"], "targets": ["片段1/分镜1"]},
            {"id": "g2", "turn_ids": ["t2"], "targets": ["片段1/分镜2"]},
            {"id": "g3", "turn_ids": ["t3"], "targets": ["片段1/分镜3"]},
        ]
        for number, changes in [(2, ["subject_focus", "viewpoint_axis"]), (3, ["subject_focus", "scale"])]:
            ledger["shots"].append({
                "target": f"片段1/分镜{number}",
                "role": "uncited_coverage",
                "source_images": [],
                "derived_from": ["panel.jpg"],
                "coverage_changes": changes,
                "coverage_type": "speaker",
                "coverage_evidence": "当前面板明确显示两名说话人及相互视线方向",
                "evidence": "current_panel",
                "purpose": "多轮对白覆盖",
                "background_excerpt": BACKGROUND,
                "source_audit": "pass",
                "unsupported_additions": [],
                "fact_claims": {"entities": ["一只手"], "actions": [], "relations": ["手位于画面下方"]},
                "action_admissions": [],
                "risk_flags": ["D"],
                "risk_basis": "多轮对白；构图关系清楚，无脆弱几何",
            })
        ledger["shots"][0]["risk_flags"] = ["D"]
        ledger["shots"][0]["risk_basis"] = "多轮对白；构图关系清楚，无脆弱几何"
        result = self.run_validator(text, ledger, True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_short_question_and_denial_may_share_one_coverage_group(self) -> None:
        text = storyboard(line="えっ。") + """
**分镜2（6秒）：**
【镜头设计】：70mm平视双人近景，乙占右前景，甲在左中景；焦点由乙转到甲后停住。
【可见动作】：乙先抬眼发问；甲随即移开视线，随后摇头，最后抿住嘴唇。
【可见背景】：暖象牙色向淡天蓝渐变铺满背景，深蓝灰放射线向外扩张。
【台词与语气】：乙：“何してるの。”（清晰女声，短促质问）甲：“違う！”（清晰女声，慌乱否认）。
【光影布光】：柔和侧光先照亮乙的眼缘，再落到甲的脸颊和发缘。
【声音设计】：低环境底噪持续；质问后停半拍，否认句紧接着落下。
"""
        ledger = valid_ledger("えっ。")
        panel = ledger["panels"][0]
        panel["source_bubble_count"] = 3
        panel["coverage"] = "shared"
        panel["bubbles"] = [
            {"id": "b1", "speaker": "甲", "speaker_evidence": "气泡尾指向甲", "kind": "dialogue", "source_text": "什么？", "status": "mapped", "script_text": "えっ。", "seconds": 1, "target": "片段1/分镜1"},
            {"id": "b2", "speaker": "乙", "speaker_evidence": "气泡尾指向乙", "kind": "dialogue", "source_text": "你在做什么？", "status": "mapped", "script_text": "何してるの。", "seconds": 2, "target": "片段1/分镜2"},
            {"id": "b3", "speaker": "甲", "speaker_evidence": "气泡尾指向甲", "kind": "dialogue", "source_text": "不是！", "status": "mapped", "script_text": "違う！", "seconds": 1, "target": "片段1/分镜2"},
        ]
        panel["dialogue_turns"] = [
            {"id": "t1", "bubble_ids": ["b1"], "function": "被撞见"},
            {"id": "t2", "bubble_ids": ["b2"], "function": "短促质问"},
            {"id": "t3", "bubble_ids": ["b3"], "function": "立即否认"},
        ]
        panel["coverage_groups"] = [
            {"id": "g1", "turn_ids": ["t1"], "targets": ["片段1/分镜1"]},
            {"id": "g2", "turn_ids": ["t2", "t3"], "targets": ["片段1/分镜2"], "merge_basis": "两句合计短于四秒，双人近景以焦点转移承载问答"},
        ]
        ledger["shots"].append({
            "target": "片段1/分镜2", "role": "uncited_coverage", "source_images": [],
            "derived_from": ["panel.jpg"], "coverage_type": "relationship",
            "coverage_changes": ["subject_focus", "dramatic_function"],
            "coverage_evidence": "当前面板明确显示甲乙双方与相互视线，可在双人关系内转移焦点",
            "evidence": "current_panel", "purpose": "短促质问与立即否认",
            "background_excerpt": BACKGROUND, "source_audit": "pass", "unsupported_additions": [],
            "fact_claims": {"entities": ["一只手"], "actions": [], "relations": ["手位于画面下方"]},
            "action_admissions": [],
            "risk_flags": ["D"], "risk_basis": "三轮对白分为两个覆盖组，后两句短促且共享双人关系",
        })
        ledger["shots"][0]["risk_flags"] = ["D"]
        ledger["shots"][0]["risk_basis"] = "三轮对白；首轮单独建立被撞见反应"
        result = self.run_validator(text, ledger, True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_single_panel_manual_overflow_is_warning_not_error(self) -> None:
        text = storyboard().replace("分镜1（5秒）", "分镜1（16秒）")
        ledger = valid_ledger()
        ledger["panels"][0]["manual_overflow"] = {
            "segment": "片段1",
            "estimated_seconds": 16,
            "reason": "同一原格长对白按自然语速与必要表演拆分后仍超过硬上限",
            "manual_handling_required": True,
        }
        result = self.run_validator(text, ledger, True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("交由用户人工处理", result.stdout)

    def test_combined_sound_design_is_allowed(self) -> None:
        result = self.run_validator(storyboard(), valid_ledger(), require_ledger=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_removed_environment_audio_field_fails(self) -> None:
        text = storyboard().replace(
            "【镜头设计】：",
            "环境音：低环境底噪从画面后方持续传来。\n【镜头设计】：",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("已移除的环境音字段", result.stdout)

    def test_subject_composition_inside_environment_fails(self) -> None:
        text = storyboard().replace(
            f"【可见背景】：{BACKGROUND}，深蓝灰放射线向外扩张。",
            "【可见背景】：少女位于画面左侧，暖色墙面填满背景。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("混入主体、道具位置或构图关系", result.stdout)

    def test_long_dialogue_with_thin_acting_emits_warning(self) -> None:
        long_line = "あ" * 30
        result = self.run_validator(storyboard(line=long_line))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("类表演信号", result.stdout)

    def test_expressive_summary_fails_performance_fidelity_warnings(self) -> None:
        text = storyboard(line="いりません、いりません！").replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物手腕后撤、肩膀缩起，连续摇头时发梢向后拖；"
            "视线在石头和对方之间折返，最后手指停住。",
        ).replace(
            "50mm平视手部特写，手腕被下缘裁切，掌心占中央前景；固定镜头。",
            "35mm双人中近景，人物分居左右中景，交接的双手叠在中央前景；摄影机小幅横移，焦点跟随手部。",
        ).replace(
            "低环境底噪从画面后方持续传来，手指收紧时衣料轻响。",
            "晶石轻碰掌心，衣料轻响与动作落点同步。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("表演保真槽缺少", result.stdout)
        self.assertIn("没有镜头落幅", result.stdout)
        self.assertIn("重复话语但【台词与语气】没有区分", result.stdout)

    def test_staged_expressive_performance_passes_fidelity_warnings(self) -> None:
        text = storyboard(line="いりません、いりません！").replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物先把物件向前送出半掌，第一声拒绝时手腕迅速后撤，肩膀随后向内缩；"
            "第二声拒绝时眼睑压紧，嘴唇先合拢再张开，头部连续摇动，"
            "发梢晚半拍向反方向甩开后回弹，最后双手停在交接处。",
        ).replace(
            "50mm平视手部特写，手腕被下缘裁切，掌心占中央前景；固定镜头。",
            "35mm双人中近景，人物分居左右中景，交接的双手叠在中央前景；摄影机跟随物件往返移动，句末在双方交接处稳住。",
        ).replace(
            '人物：“いりません、いりません！”（清晰的中性音色，平静语气）。',
            '人物：“いりません、いりません！”（清晰的中性音色，第一次短促，第二次压力加重后收尾）。',
        ).replace(
            "低环境底噪从画面后方持续传来，手指收紧时衣料轻响。",
            "晶石轻碰掌心，衣料急响与动作落点同步，句末声场收静。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("表演保真槽缺少", result.stdout)
        self.assertNotIn("没有镜头落幅", result.stdout)
        self.assertNotIn("重复话语但【台词与语气】没有区分", result.stdout)

    def test_repeated_words_split_across_quotes_need_audio_contrast(self) -> None:
        text = storyboard(line="いや！").replace(
            '人物：“いや！”（清晰的中性音色，平静语气）。',
            '人物：“いや！”（清晰的中性音色，急促语气）。\n'
            '人物：“いや！”（清晰的中性音色，急促语气）。',
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("重复话语但【台词与语气】没有区分", result.stdout)

    def test_single_elongated_utterance_is_not_repetition(self) -> None:
        result = self.run_validator(storyboard(line="うううっ……せめて教えてください……"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("重复话语但【台词与语气】没有区分", result.stdout)

    def test_conflicting_depth_is_a_warning_not_error(self) -> None:
        text = storyboard().replace("固定镜头", "固定镜头，大光圈、全景深")
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("同时声明浅景深/大光圈与大景深", result.stdout)

    def test_repeated_atmosphere_effect_emits_warning(self) -> None:
        blocks = "\n".join(
            f"""**分镜{i}（2秒）：**
{"分镜参考 `[panel.jpg]`" if i == 1 else ""}
【镜头设计】：50mm平视手部特写，手腕被下缘裁切，手掌占中央前景；固定镜头。
【可见动作】：手掌稳定托住物件，手指先放松再轻微收紧。
【可见背景】：{BACKGROUND}，微尘漂浮。
【台词与语气】：无台词。
【光影布光】：柔和侧光照亮手指，微尘停在暗部。
【声音设计】：低环境底噪从画面后方持续传来，衣料发出轻响。
"""
            for i in range(1, 5)
        )
        text = f"## 场景色彩基准\n二维手绘质感。\n\n## 【片段1】测试\n\n{blocks}"
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("片段1的微尘出现在4/4个镜头", result.stdout)

    def test_three_second_micro_action_chain_has_no_capacity_warning(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "听见呼唤后先停住，眼睑微抬，嘴角放松，短吸气；"
            "指尖在衣料上收紧，衣摆随惯性晚半拍回落，视线最终留在说话者身上。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("主要动作", result.stdout)
        self.assertNotIn("类表演信号", result.stdout)

    def test_sentence_end_settle_counts_as_performance_endpoint(self) -> None:
        long_line = "あ" * 30
        text = storyboard(line=long_line).replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "听见问话后先停顿，视线转向对方；眉梢稍后松开，"
            "短促吸气，指尖捏住衣角，句末松手并让肩线回落。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("可能只有动作清单", result.stdout)

    def test_major_action_overload_is_soft_warning(self) -> None:
        text = storyboard().replace(
            "分镜1（5秒）", "分镜1（2秒）"
        ).replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物起身、转身、迈步跑向门口并推开门。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("主要动作", result.stdout)

    def test_contextual_pointing_is_not_generic_gesture_warning(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物抬手指向桌上的晶石，视线随指尖落定。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("主要依赖抬手", result.stdout)

    def test_audio_line_with_hidden_visual_action_warns(self) -> None:
        text = storyboard().replace(
            "【声音设计】：低环境底噪从画面后方持续传来，手指收紧时衣料轻响。",
            "【声音设计】：人物转身走向门并打开门，随后传来门轴声。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("重新断言了主体动作", result.stdout)
        self.assertIn("声音设计疑似包含新的视觉动作", result.stdout)

    def test_sound_rejects_dialogue_delivery_duplication(self) -> None:
        for phrase in (
            "青的喊声从右侧近距离冲入并盖过喘息。",
            "对白随奔跑轻微起伏。",
        ):
            text = storyboard().replace(
                "低环境底噪从画面后方持续传来，手指收紧时衣料轻响。",
                phrase,
            )
            result = self.run_validator(text)
            self.assertNotEqual(result.returncode, 0, phrase)
            self.assertIn("重复了对白表演", result.stdout)

    def test_sound_rejects_reasserted_subject_action(self) -> None:
        text = storyboard().replace(
            "低环境底噪从画面后方持续传来，手指收紧时衣料轻响。",
            "人物转身时衣料急响。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("重新断言了主体动作", result.stdout)

    def test_non_dialogue_sound_and_neutral_sync_pass(self) -> None:
        text = storyboard().replace(
            "低环境底噪从画面后方持续传来，手指收紧时衣料轻响。",
            "低环境底噪持续，衣料轻响与动作落点同步，句末声场收静。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_camera_rejects_temporal_subject_action(self) -> None:
        text = storyboard().replace(
            "50mm平视手部特写，手腕被下缘裁切，掌心占中央前景；固定镜头。",
            "50mm平视人物近景，人物占中央前景；镜头轻推，人物随后转身跑向出口。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("混入了时序性主体动作", result.stdout)

    def test_atmosphere_with_visible_source_does_not_warn(self) -> None:
        blocks = "\n".join(
            f"""**分镜{i}（2秒）：**
{"分镜参考 `[panel.jpg]`" if i == 1 else ""}
【镜头设计】：50mm平视近景，手腕被下缘裁切，手掌占中央前景；固定镜头。
【可见动作】：手掌稳定托住物件，手指先放松再轻微收紧。
【可见背景】：窗边蒸汽缓慢上升，{BACKGROUND}。
【台词与语气】：无台词。
【光影布光】：逆光穿过蒸汽形成微尘可见的光束。
【声音设计】：窗边风声从画面右侧传来，蒸汽发出轻响。
"""
            for i in range(1, 5)
        )
        text = f"## 场景色彩基准\n二维手绘质感。\n\n## 【片段1】测试\n\n{blocks}"
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("多数缺少可见依据", result.stdout)

    def test_re0_fields_are_required(self) -> None:
        text = storyboard().replace("【镜头设计】：", "【摄影设计】：")
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("缺少独立字段：镜头设计", result.stdout)

    def test_cross_shot_and_negative_meta_prose_fail(self) -> None:
        for phrase in ("保持原有构图", "上一格人物站在左侧", "不新增飞鸟", "不使用背景"):
            text = storyboard().replace(
                "人物手掌朝上托住物件，手指先放松再轻微收紧。",
                phrase + "。",
            )
            result = self.run_validator(text)
            self.assertNotEqual(result.returncode, 0, phrase)
            self.assertIn("不可执行元措辞", result.stdout)

    def test_negative_words_inside_dialogue_do_not_fail_meta_gate(self) -> None:
        text = storyboard(line="不要使用这个东西！")
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("不可执行元措辞", result.stdout)

    def test_six_second_static_dialogue_warns_on_visible_density(self) -> None:
        text = storyboard().replace("分镜1（5秒）", "分镜1（6秒）")
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("6秒对白镜头但可见动作只有", result.stdout)

    def test_six_second_staged_head_face_chain_passes_density(self) -> None:
        text = storyboard().replace("分镜1（5秒）", "分镜1（6秒）").replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物起幅为朝画面右侧的三分之二侧脸，听见问话后瞳孔先回到左侧；"
            "随后下巴轻收、脸转向正面，一侧眉梢松开，句末肩线回落，视线停在说话者身上。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("6秒对白镜头但可见动作只有", result.stdout)

    def test_pure_object_explanation_does_not_require_body_signals(self) -> None:
        text = storyboard().replace("分镜1（5秒）", "分镜1（6秒）").replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物未入画；晶石亮点沿棱线逐层显现，随后金属边缘泛起亮点，最后两件物体的反光同时稳定。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("6秒对白镜头但可见动作只有", result.stdout)
        self.assertNotIn("类表演信号", result.stdout)

    def test_chinese_dialogue_trigger_paraphrase_fails(self) -> None:
        line = "前は暗石区の入口だけだったのに、今は全部封鎖されてる。"
        text = storyboard(line=line).replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "提到暗石区入口时，人物视线收紧。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("用中文概括对白触发点", result.stdout)

    def test_verbatim_japanese_dialogue_trigger_passes(self) -> None:
        line = "前は暗石区の入口だけだったのに、今は全部封鎖されてる。"
        text = storyboard(line=line).replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "说到「暗石区の入口」时，人物视线收紧。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_chinese_quoted_utterance_exit_trigger_fails(self) -> None:
        line = "しっ。黙って。"
        text = storyboard(line=line).replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "“闭嘴”出口时，人物的嘴角压平。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("用中文概括对白触发点", result.stdout)

    def test_chinese_semantic_action_trigger_fails(self) -> None:
        line = "先に攻撃した方がよくない？"
        text = storyboard(line=line).replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "提出抢攻时，她的下巴朝目标送出。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("用中文概括对白触发点", result.stdout)

    def test_generic_emphasis_timing_remains_valid(self) -> None:
        line = "先に攻撃した方がよくない？"
        text = storyboard(line=line).replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "质问重音处，她的下巴朝目标送出。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unestablished_counted_gaze_target_fails(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物的视线落向对面的两名少女，手指随后放松。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("未在本镜建立的两名少女", result.stdout)

    def test_directional_gaze_target_is_self_contained(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物的视线转向画面右侧外，手指随后放松。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_terminal_uncited_coverage_before_source_shot_warns(self) -> None:
        base = storyboard().replace(
            f"【可见背景】：{BACKGROUND}，深蓝灰放射线向外扩张。",
            "【可见背景】：暖色墙面填满背景。",
        ).replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "浅发少女的手指先扣紧杯柄，随后放松并停住。",
        ).replace(
            "50mm平视手部特写，手腕被下缘裁切，掌心占中央前景；固定镜头。",
            "50mm平视人物近景，浅发少女位于画面左侧，木杯占据右前景；固定镜头。",
        )
        first = base.replace("分镜参考 `[panel.jpg]`\n", "")
        second = base.split("## 【片段1】", 1)[1]
        second = "## 【片段2】" + second.replace("测试", "下一格", 1)
        result = self.run_validator(first + "\n" + second)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("末镜为无参考补镜", result.stdout)

    def test_page_or_bubble_whitespace_is_not_visible_background(self) -> None:
        text = storyboard().replace(
            f"【可见背景】：{BACKGROUND}，深蓝灰放射线向外扩张。",
            "【可见背景】：浅色对话留白把背景切成上下两层。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("气泡/页面/格间空白", result.stdout)

    def test_ledger_cannot_underreport_japanese_speech_time(self) -> None:
        line = "これはとても長い説明なので最後までちゃんと聞いてください。"
        text = storyboard(line=line).replace("分镜1（5秒）", "分镜1（8秒）")
        ledger = valid_ledger(line)
        ledger["panels"][0]["bubbles"][0]["seconds"] = 1
        result = self.run_validator(text, ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("低于独立日文估时", result.stdout)

    def test_multi_reference_requires_source_bound_camera_rows(self) -> None:
        text = storyboard().replace(
            "分镜参考 `[panel.jpg]`",
            "分镜参考 `[panel.jpg]`、`[panel2.jpg]`",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("逐条绑定", result.stdout)

    def test_camera_requires_concrete_panel_composition(self) -> None:
        text = storyboard().replace(
            "50mm平视手部特写，手腕被下缘裁切，掌心占中央前景；固定镜头。",
            "平视固定镜头。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("缺少原格构图锁", result.stdout)

    def test_action_rejects_static_composition(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上托住物件，手指先放松再轻微收紧。",
            "人物占据画面中央前景，手掌朝上托住物件，手指先放松再轻微收紧。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("混入静态构图/摄影信息", result.stdout)

    def test_original_resolution_requires_escalation_reason(self) -> None:
        ledger = valid_ledger()
        ledger["panels"][0]["drafting_resolution"] = "original"
        result = self.run_validator(storyboard(), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("resolution_escalation_reason", result.stdout)

    def test_non_japanese_source_cannot_be_copied_from_final_script(self) -> None:
        ledger = valid_ledger()
        ledger["panels"][0]["bubbles"][0]["source_text"] = SHORT_LINE
        result = self.run_validator(storyboard(), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("禁止从成稿反向生成台账", result.stdout)

    def test_adjacent_shots_cannot_repeat_formal_reference(self) -> None:
        first = storyboard()
        second_block = first.split("**分镜1（5秒）：**", 1)[1]
        text = first + "\n**分镜2（5秒）：**" + second_block
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("重复同一参考图", result.stdout)

    def test_adjacent_segments_cannot_repeat_formal_reference(self) -> None:
        first = storyboard()
        second = storyboard().replace("## 【片段1】测试", "## 【片段2】测试")
        result = self.run_validator(first + "\n" + second)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("重复同一参考图", result.stdout)

    def test_risk_decision_requires_pre_draft_basis(self) -> None:
        ledger = valid_ledger()
        ledger["shots"][0].pop("risk_basis")
        result = self.run_validator(storyboard(), ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("缺少risk_basis", result.stdout)

    def test_uncited_coverage_requires_two_meaningful_changes(self) -> None:
        first = storyboard(line=None)
        second = """
**分镜2（3秒）：**
【镜头设计】：85mm平视手部极近景，指尖占画面右侧，固定镜头。
【可见动作】：手指先收紧，随后放松并停住。
【可见背景】：暖象牙色向淡天蓝渐变铺满背景，深蓝灰放射线向外扩张。
【台词与语气】：无台词。
【光影布光】：柔和侧光照亮指尖，指缝保留浅影。
【声音设计】：低环境底噪持续，指尖放松时衣料轻响。
"""
        ledger = valid_ledger()
        panel = ledger["panels"][0]
        panel["source_bubble_count"] = 0
        panel["coverage"] = "none"
        panel["bubbles"] = []
        ledger["shots"].append({
            "target": "片段1/分镜2",
            "role": "uncited_coverage",
            "source_images": [],
            "derived_from": ["panel.jpg"],
            "coverage_changes": ["scale"],
            "coverage_type": "detail_insert",
            "coverage_evidence": "当前面板明确显示手指与掌心，可裁取细节变化",
            "evidence": "current_panel",
            "purpose": "手指反应补镜",
            "background_excerpt": BACKGROUND,
            "source_audit": "pass",
            "unsupported_additions": [],
            "fact_claims": {"entities": ["一只手"], "actions": [], "relations": ["手位于画面下方"]},
            "action_admissions": [],
            "risk_flags": [],
            "risk_basis": "无对白；手部关系明确，无脆弱几何",
        })
        result = self.run_validator(first + second, ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("不足两项有效coverage_changes", result.stdout)

    def test_same_panel_coverage_cannot_cross_clip_boundary(self) -> None:
        first = storyboard(line=None)
        second = """
## 【片段2】补镜
**分镜1（3秒）：**
【镜头设计】：85mm侧向手部极近景，指尖占画面右侧，固定镜头。
【可见动作】：手指先收紧，随后放松并停住。
【可见背景】：暖象牙色向淡天蓝渐变铺满背景，深蓝灰放射线向外扩张。
【台词与语气】：无台词。
【光影布光】：柔和侧光照亮指尖，指缝保留浅影。
【声音设计】：低环境底噪持续，指尖放松时衣料轻响。
"""
        ledger = valid_ledger()
        panel = ledger["panels"][0]
        panel["source_bubble_count"] = 0
        panel["coverage"] = "none"
        panel["bubbles"] = []
        ledger["shots"].append({
            "target": "片段2/分镜1",
            "role": "uncited_coverage",
            "source_images": [],
            "derived_from": ["panel.jpg"],
            "coverage_changes": ["scale", "viewpoint_axis"],
            "coverage_type": "detail_insert",
            "coverage_evidence": "当前面板明确显示手指与掌心，可形成侧向细节",
            "evidence": "current_panel",
            "purpose": "手指反应补镜",
            "background_excerpt": BACKGROUND,
            "source_audit": "pass",
            "unsupported_additions": [],
            "fact_claims": {"entities": ["一只手"], "actions": [], "relations": ["手位于画面下方"]},
            "action_admissions": [],
            "risk_flags": [],
            "risk_basis": "无对白；手部关系明确，无脆弱几何",
        })
        result = self.run_validator(first + second, ledger, True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("同一原格的全部覆盖必须放在一个片段内", result.stdout)

    def test_genuinely_different_coverage_passes_inside_same_clip(self) -> None:
        first = storyboard(line=None)
        second = """
**分镜2（3秒）：**
【镜头设计】：85mm侧向手部极近景，指尖占画面右侧，固定镜头。
【可见动作】：手指先收紧，随后放松并停住。
【可见背景】：暖象牙色向淡天蓝渐变铺满背景，深蓝灰放射线向外扩张。
【台词与语气】：无台词。
【光影布光】：柔和侧光照亮指尖，指缝保留浅影。
【声音设计】：低环境底噪持续，指尖放松时衣料轻响。
"""
        ledger = valid_ledger()
        panel = ledger["panels"][0]
        panel["source_bubble_count"] = 0
        panel["coverage"] = "none"
        panel["bubbles"] = []
        ledger["shots"].append({
            "target": "片段1/分镜2",
            "role": "uncited_coverage",
            "source_images": [],
            "derived_from": ["panel.jpg"],
            "coverage_changes": ["scale", "viewpoint_axis"],
            "coverage_type": "detail_insert",
            "coverage_evidence": "当前面板明确显示手指与掌心，可形成侧向细节",
            "evidence": "current_panel",
            "purpose": "侧向手指反应插入",
            "background_excerpt": BACKGROUND,
            "source_audit": "pass",
            "unsupported_additions": [],
            "fact_claims": {"entities": ["一只手"], "actions": [], "relations": ["手位于画面下方"]},
            "action_admissions": [],
            "risk_flags": [],
            "risk_basis": "无对白；手部关系明确，无脆弱几何",
        })
        result = self.run_validator(first + second, ledger, True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
