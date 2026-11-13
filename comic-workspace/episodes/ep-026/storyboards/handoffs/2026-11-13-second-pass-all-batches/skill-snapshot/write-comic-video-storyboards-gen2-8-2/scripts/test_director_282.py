"""Synthetic behavioral tests; fixtures are not real visual-inspection attestations."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import validate_storyboard as legacy
from validate_director import make_source_lock, review_digest
from render_storyboard import render

HERE = Path(__file__).parent


def fields(camera, action, speech="无台词。"):
    return {"镜头设计": camera, "可见动作": action,
            "可见背景": "深蓝墙面与灰褐地砖分成前后两层，墙边暗影稳定。",
            "台词与语气": speech, "光影布光": "左侧柔光照亮脸和金属刃口，墙角保持暗影。",
            "声音设计": "室内低环境声持续，衣料摩擦短促。"}


def fixture():
    """Four shots and two source nodes; all names/text are test-only invented data."""
    a = {"董白.阶段": "站立", "董白.持剑手": "右"}
    b = {"董白.阶段": "腾空", "董白.持剑手": "右"}
    panels = []
    for i, (image, state, target) in enumerate((("a.jpg", a, "片段1/分镜1"), ("b.jpg", b, "片段1/分镜4"))):
        bubbles = [] if i else [{"id": "b1", "speaker": "董白", "kind": "dialogue", "source_text": "走吧。",
            "script_text": "行くぞ。", "status": "mapped", "target": target, "start": 1, "seconds": 2}]
        panels.append({"image": image, "renderable_visual": True, "viewed_at_drafting": True,
            "drafting_resolution": "720p", "bubble_audit": "pass", "source_bubble_count": len(bubbles),
            "bubbles": bubbles, "composition_lock": "近景，主体位于左侧前景，脸部被原格侧缘裁切",
            "source_facts": {"entities": ["董白"], "actions": [], "relations": ["右手持剑"]},
            "background": {"type": "physical", "description": "墙面与地砖"},
            "node_state": dict(state), "anchor_target": target, "page_overlays": []})
    cameras = ["平视近景，董白位于左侧前景，肩部在画面下缘；固定镜头。",
               "平视眼部特写，眼睛位于中央，脸侧在后层；固定镜头。",
               "背后中景跟随，董白位于中央前景，地面向后掠过。",
               "正面近景，董白位于中央前景，墙面退向后层。"]
    shots = []
    for i, duration in enumerate((3, 3, 5, 4)):
        source = i in (0, 3)
        shot = {"target": f"片段1/分镜{i+1}", "duration": duration,
            "role": "source_locked" if source else "uncited_coverage", "source_images": ["a.jpg" if i == 0 else "b.jpg"] if source else [],
            "purpose": "synthetic behavioral fixture", "characters": ["董白"], "risk_flags": [], "risk_basis": "测试用简短行为，非实际图像审查",
            "state_in": dict(a if i < 3 else b), "state_out": dict(a if i < 2 else b),
            "fields": fields(cameras[i], "董白保持右手持剑，目光锁定前方。" if i != 2 else "董白压低重心，蹬地后向前跃出。")}
        if source:
            shot.update({"viewed_while_writing": True, "source_audit": "pass", "anchor_phase": "state" if i == 0 else "process",
                         "anchor_elements": "仅用于结构测试的持剑与阶段", "anchor_state": dict(a if i == 0 else b)})
        else:
            shot["derived_from"] = ["a.jpg", "b.jpg"]
            shot["neighbor_contrast"] = {}
            for direction, j in (("previous", i - 1), ("next", i + 1)):
                shot["neighbor_contrast"][direction] = {"target": f"片段1/分镜{j+1}",
                    "changes": [{"dimension": "viewpoint" if i == 2 or j == 2 else "scale",
                                 "description": "实际镜头观察方向或景别发生变化", "excerpt": cameras[i]}]}
        shots.append(shot)
    shots[0]["fields"]["台词与语气"] = "（沉默1秒）\n董白：“行くぞ。”（从容的中性声线，语气克制）。"
    shots[0]["silences"] = [{"start": 0, "seconds": 1}]
    ledger = {"version": 3, "skill_version": "2.8.2", "source_language": "zh", "look": "手绘二维动画，中等对比。",
              "panels": panels, "shots": shots, "performance": [],
              "character_registry": [{"canonical_name": "董白", "performance_profile": {"baseline": "高傲自负", "source": "用户明确确认"}}]}
    ledger["source_lock"] = make_source_lock(ledger)
    return ledger


def finish(ledger):
    text = render(ledger)
    ledger["director_review"] = {"characters": "合成人物基准记录，不宣称真实样段质量", "pacing": "三秒、三秒、五秒、四秒的合成顺序",
        "node_arrivals": "站立经跃出到腾空的合成状态连接", "contrast": "逐侧核对最终相邻的景别与方向"}
    ledger["director_review"]["sha256"] = review_digest(ledger, text)
    return text


def check(ledger, text=None):
    if text is None:
        text = finish(ledger)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "ledger.json"
        path.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
        warnings = []
        errors = legacy.validate_source_ledger(path, text, None, warnings)
        return errors, warnings


class DirectorPolicyTests(unittest.TestCase):
    def assert_bad(self, ledger, text=None):
        errors, _ = check(ledger, text)
        self.assertTrue(errors)
        return "\n".join(errors)

    def test_valid_one_difference_each_side_and_silent_shots(self):
        errors, warnings = check(fixture())
        self.assertEqual(errors, [])
        self.assertTrue(any("[来源]" in w for w in warnings))

    def test_text_mutation_fails_even_if_mapping_changed(self):
        l = fixture(); l["panels"][0]["bubbles"][0]["script_text"] = "行こう。"
        self.assertIn("来源／对白锁", self.assert_bad(l))

    def test_source_observations_cannot_be_rewritten_to_fit_directing(self):
        l = fixture(); l["panels"][0]["composition_lock"] = "另一个方向"
        self.assertIn("来源／对白锁", self.assert_bad(l))

    def test_removed_source_panel_is_detected_by_lock(self):
        l = fixture(); l["panels"].pop()
        self.assertIn("来源／对白锁", self.assert_bad(l))

    def test_source_shot_cannot_be_omitted(self):
        l = fixture(); l["shots"][3]["role"] = "uncited_coverage"; l["shots"][3]["source_images"] = []
        self.assertIn("原作镜头完整性", self.assert_bad(l))

    def test_merge_cannot_discard_per_panel_realization(self):
        l = fixture(); l["shots"][0]["source_images"] = ["a.jpg", "b.jpg"]
        self.assertIn("逐一登记anchors", self.assert_bad(l))

    def test_added_quote_fails(self):
        l = fixture(); l["shots"][1]["fields"]["台词与语气"] = "董白：“余計な台詞。”（平静）。"
        self.assertIn("正式对白", self.assert_bad(l))

    def test_unquoted_extra_speech_is_not_a_bypass(self):
        l = fixture(); l["shots"][0]["fields"]["台词与语气"] += "\n补充台词：快走吧"
        self.assertIn("未登记发声", self.assert_bad(l))

    def test_new_fact_cannot_be_mislabeled_as_observed(self):
        l = fixture(); l["shots"][1]["fact_claims"] = {"entities": ["另一把刀"]}
        self.assertIn("伪报", self.assert_bad(l))

    def test_malformed_role_reports_error_without_traceback(self):
        l = fixture(); text = finish(l); l["shots"][1]["role"] = []
        self.assertIn("分类无效", self.assert_bad(l, text))

    def test_source_overlays_are_frozen_but_audio_targets_can_move(self):
        l = fixture(); l["panels"][0]["page_overlays"] = [{"kind": "sfx", "source_text": "咔", "render": False,
            "audio_meaning": "短促接触声", "target": "片段1/分镜1", "audio_excerpt": "衣料摩擦"}]
        l["source_lock"] = make_source_lock(l)
        self.assertEqual(check(l)[0], [])
        l["panels"][0]["page_overlays"][0]["source_text"] = "另一声"
        self.assertIn("来源／对白锁", self.assert_bad(l))

    def test_wrong_owner_fails(self):
        l = fixture(); l["shots"][0]["fields"]["台词与语气"] = l["shots"][0]["fields"]["台词与语气"].replace("董白：", "春子：")
        self.assertIn("正式对白", self.assert_bad(l))

    def test_wrong_kind_fails(self):
        l = fixture(); l["shots"][0]["fields"]["台词与语气"] = l["shots"][0]["fields"]["台词与语气"].replace("董白：", "董白（内心）：")
        self.assertIn("正式对白", self.assert_bad(l))

    def test_split_line_across_return_does_not_repeat_or_change_text(self):
        l = fixture(); b = l["panels"][0]["bubbles"][0]
        b["segments"] = [{"target": "片段1/分镜1", "script_text": "行く", "start": 1, "seconds": 1},
                         {"target": "片段1/分镜3", "script_text": "ぞ。", "start": 0, "seconds": 1}]
        l["shots"][0]["fields"]["台词与语气"] = "（沉默1秒）\n董白：“行く”（平静）。"
        l["shots"][2]["fields"]["台词与语气"] = "董白（画外音）：“ぞ。”（平静）。"
        self.assertEqual(check(l)[0], [])
        b["segments"][1]["script_text"] = "行くぞ。"
        self.assertIn("拼接", self.assert_bad(l))

    def test_next_neighbor_cannot_be_old_next_source(self):
        l = fixture(); l["shots"][1]["neighbor_contrast"]["next"]["target"] = "片段1/分镜4"
        self.assertIn("最终next邻镜", self.assert_bad(l))

    def test_both_neighbors_needed(self):
        l = fixture(); l["shots"][1]["neighbor_contrast"]["next"]["changes"] = []
        self.assertIn("至少需要一项", self.assert_bad(l))

    def test_labels_without_rendered_difference_fail(self):
        l = fixture(); l["shots"][1]["neighbor_contrast"]["next"]["changes"][0]["excerpt"] = "没有出现在正式字段中的变化"
        self.assertIn("差异摘录", self.assert_bad(l))

    def test_timing_and_clip_boundaries_can_change(self):
        l = fixture(); l["shots"][1]["duration"] = 6
        self.assertEqual(check(l)[0], [])  # Per-clip ceiling checked by CLI separately.

    def test_character_registry_change_invalidates_review(self):
        l = fixture(); text = finish(l); l["character_registry"][0]["performance_profile"]["baseline"] = "惊慌"
        self.assertIn("已过期", self.assert_bad(l, text))

    def test_timing_change_invalidates_review(self):
        l = fixture(); text = finish(l); l["shots"][1]["duration"] = 4
        self.assertIn("已过期", self.assert_bad(l, text))

    def test_no_proof_does_not_block_new_choreography(self):
        l = fixture(); l["shots"][2]["unsupported_additions"] = ["完整起跳路线未画出"]
        errors, warnings = check(l)
        self.assertEqual(errors, [])
        self.assertTrue(any("添加内容" in w for w in warnings))

    def test_state_jump_fails(self):
        l = fixture(); l["shots"][2]["state_in"]["董白.持剑手"] = "左"
        self.assertIn("状态跳变", self.assert_bad(l))

    def test_next_node_state_must_match(self):
        l = fixture(); l["shots"][3]["anchor_state"]["董白.阶段"] = "站立"
        self.assertIn("未收束", self.assert_bad(l))

    def test_silence_is_timed_and_not_speech(self):
        l = fixture(); l["shots"][0]["silences"][0]["seconds"] = 2
        self.assertIn("沉默", self.assert_bad(l))

    def test_silence_cannot_overlap_speech(self):
        l = fixture(); l["shots"][0]["silences"][0]["start"] = 1
        self.assertIn("沉默与发声重叠", self.assert_bad(l))

    def test_silence_before_after_position_is_checked(self):
        l = fixture(); l["shots"][0]["fields"]["台词与语气"] = "董白：“行くぞ。”（平静）。\n（沉默1秒）"
        self.assertIn("句前／句后", self.assert_bad(l))

    def test_performance_must_be_rendered_and_fit(self):
        l = fixture(); l["shots"][1]["risk_flags"] = ["P"]
        self.assertIn("表演卡", self.assert_bad(l))
        l["performance"] = [{"target": "片段1/分镜2", "card": {"opening": "注视", "beats": ["观察"], "coupling": "锁定对方", "landing": "继续看"},
            "details": [l["shots"][1]["fields"]["可见动作"]], "intervals": [{"speech_seconds": 0, "acting_seconds": 3, "concurrent": True}]}]
        self.assertEqual(check(l)[0], [])
        l["performance"][0]["intervals"][0]["acting_seconds"] = 4
        self.assertIn("表演计时", self.assert_bad(l))

    def test_renderer_does_not_mutate_or_approve(self):
        l = fixture(); before = deepcopy(l); render(l)
        self.assertEqual(l, before)
        self.assertNotIn("director_review", l)

    def test_renderer_refuses_role_defaults(self):
        l = fixture(); l["shots"][1].pop("role")
        with self.assertRaises(ValueError): render(l)

    def test_unknown_version_is_not_legacy_escape(self):
        l = fixture(); text = finish(l); l["skill_version"] = "2.8.999"
        self.assertIn("不支持", self.assert_bad(l, text))

    def test_source_lock_preserves_order_and_voice(self):
        l = fixture(); frozen = deepcopy(l["source_lock"])
        l["panels"][0]["bubbles"][0]["speaker"] = "春子"
        self.assertNotEqual(make_source_lock(l), frozen)

    def test_freeze_cli_refuses_overwrite_and_never_fills_approvals(self):
        l = fixture(); l.pop("source_lock"); l["panels"][0]["viewed_at_drafting"] = False
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "l.json"; path.write_text(json.dumps(l, ensure_ascii=False), encoding="utf-8")
            cmd = [sys.executable, str(HERE / "freeze_storyboard.py"), str(path)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            frozen = json.loads(path.read_text(encoding="utf-8"))
            self.assertFalse(frozen["panels"][0]["viewed_at_drafting"])
            self.assertNotIn("director_review", frozen)
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)

    def test_cli_final_ceiling_and_new_policy_dispatch(self):
        l = fixture()
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); text = finish(l)
            (p / "s.md").write_text(text, encoding="utf-8"); (p / "l.json").write_text(json.dumps(l, ensure_ascii=False), encoding="utf-8")
            cmd = [sys.executable, "-X", "utf8", str(HERE / "validate_storyboard.py"), str(p / "s.md"), "--source-ledger", str(p / "l.json"), "--require-source-ledger"]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            l["shots"][1]["duration"] = 7; text = finish(l)
            (p / "s.md").write_text(text, encoding="utf-8"); (p / "l.json").write_text(json.dumps(l, ensure_ascii=False), encoding="utf-8")
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)

    def test_long_dialogue_is_not_a_hard_character_gate(self):
        l = fixture()
        names = {"片段1/分镜3": "片段2/分镜1", "片段1/分镜4": "片段2/分镜2"}
        for s in l["shots"]:
            s["target"] = names.get(s["target"], s["target"])
            for c in s.get("neighbor_contrast", {}).values():
                c["target"] = names.get(c["target"], c["target"])
        for p in l["panels"]:
            p["anchor_target"] = names.get(p["anchor_target"], p["anchor_target"])
        line = "状況を確かめながら進む必要があるので、まず周囲の様子をよく見てから次の行動を決めよう。"
        b = l["panels"][0]["bubbles"][0]
        b.update(source_text="需要确认情况，仔细观察周围，再决定下一步行动。", script_text=line, seconds=10)
        l["shots"][0]["duration"] = 12
        l["shots"][0]["fields"]["台词与语气"] = f"（沉默1秒）\n董白：“{line}”（平静）。"
        l["source_lock"] = make_source_lock(l)
        text = finish(l)
        self.assertEqual(check(l, text)[0], [])
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp); (p / "s.md").write_text(text, encoding="utf-8")
            (p / "l.json").write_text(json.dumps(l, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run([sys.executable, "-X", "utf8", str(HERE / "validate_storyboard.py"), str(p / "s.md"), "--source-ledger", str(p / "l.json")], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_root_array_is_a_diagnostic_not_a_traceback(self):
        l = fixture(); text = finish(l)
        self.assertIn("根必须是对象", self.assert_bad([], text))

    def test_pure_sfx_panel_cannot_lose_its_sound(self):
        l = fixture()
        p = {"image": "sfx.jpg", "renderable_visual": False, "viewed_at_drafting": True,
             "drafting_resolution": "720p", "bubble_audit": "pass", "source_bubble_count": 0,
             "bubbles": [], "page_overlays": [{"kind": "sfx", "source_text": "咔", "render": False,
             "audio_meaning": "短促接触声", "target": "片段1/分镜1", "audio_excerpt": "衣料摩擦"}]}
        l["panels"].insert(0, p); l["source_lock"] = make_source_lock(l)
        self.assertEqual(check(l)[0], [])
        p["page_overlays"][0]["audio_excerpt"] = "正文没有的声音"
        self.assertIn("拟声信息", self.assert_bad(l))


if __name__ == "__main__":
    unittest.main()
