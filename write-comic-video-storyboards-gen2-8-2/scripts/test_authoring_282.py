"""Mechanical authoring regressions; synthetic fixtures do not attest real read-throughs."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from authoring import check_routes, expand, route_digest
from test_director_282 import fixture, finish, check
from render_storyboard import render
from validate_director import make_source_lock, review_digest

HERE = Path(__file__).parent


def compact():
    ledger = fixture()
    ledger["authoring_format"] = "compact-2.8.2"
    ledger["initial_state"] = dict(ledger["shots"][0]["state_in"])
    ledger.pop("performance")
    for shot in ledger["shots"]:
        before, after = shot.pop("state_in"), shot.pop("state_out")
        shot["state_changes"] = {k: v for k, v in after.items() if before.get(k) != v}
        shot.pop("neighbor_contrast", None)
    ledger["cuts"] = []
    for left, right in zip(ledger["shots"], ledger["shots"][1:]):
        ledger["cuts"].append({"from": left["target"], "to": right["target"], "changes": [{
            "dimension": "viewpoint" if "分镜3" in (left["target"] + right["target"]) else "scale",
            "description": "合成测试中的实际方向或景别改变", "shot": right["target"], "field": "镜头设计"}]})
    return ledger


def routes(ledger, confirmed=False):
    ledger["requires_route_confirmation"] = True
    route = {"id": "test-route", "source_images": ["a.jpg", "b.jpg"],
             "path": "合成示例：持剑站立，蹬地向前跃出，节点b为腾空过程。"}
    if confirmed:
        route["user_confirmation"] = {"quote": "合成确认语，仅用于软件测试", "sha256": route_digest(route)}
    ledger["action_routes"] = [route]
    ledger["source_lock"] = make_source_lock(ledger)
    return ledger


class AuthoringTests(unittest.TestCase):
    def test_compact_passes_existing_full_checks_and_renders_identically(self):
        ledger = compact()
        self.assertEqual(render(ledger), render(fixture()))
        self.assertEqual(check(ledger)[0], [])

    def test_state_changes_inherit_without_repeating_records(self):
        ledger = expand(compact())
        self.assertEqual(ledger["shots"][2]["state_in"]["董白.阶段"], "站立")
        self.assertEqual(ledger["shots"][2]["state_out"]["董白.阶段"], "腾空")
        self.assertEqual(ledger["shots"][3]["state_in"], ledger["shots"][2]["state_out"])

    def test_shared_cut_checks_both_adjacent_new_shots(self):
        expanded = expand(compact())
        self.assertEqual(expanded["shots"][1]["neighbor_contrast"]["next"]["changes"],
                         expanded["shots"][2]["neighbor_contrast"]["previous"]["changes"])

    def test_no_input_mutation(self):
        ledger = compact(); before = deepcopy(ledger)
        expand(ledger); render(ledger)
        self.assertEqual(ledger, before)

    def test_inline_performance_keeps_actual_plan_and_timing(self):
        ledger = compact(); shot = ledger["shots"][1]; shot["risk_flags"] = ["P"]
        shot["performance"] = {"card": {"opening": "锁定目标", "beats": ["稳住目光"], "coupling": "持续压迫对手", "landing": "仍持剑"},
            "details": ["目光锁定前方"], "intervals": [{"speech_seconds": 0, "acting_seconds": 3, "concurrent": True}]}
        self.assertEqual(check(ledger)[0], [])
        shot["performance"]["intervals"][0]["acting_seconds"] = 9
        self.assertTrue(any("表演计时" in e for e in check(ledger)[0]))

    def test_missing_cut_still_blocks_each_side(self):
        ledger = compact(); ledger["cuts"].pop(1)
        errors, _ = check(ledger)
        self.assertTrue(any("previous" in e for e in errors))
        self.assertTrue(any("next" in e for e in errors))

    def test_empty_changes_do_not_satisfy_significance_gate(self):
        ledger = compact(); ledger["cuts"][0]["changes"] = []
        with self.assertRaises(ValueError): expand(ledger)

    def test_cut_must_be_actual_adjacency(self):
        ledger = compact(); ledger["cuts"][0]["to"] = "片段1/分镜4"
        with self.assertRaises(ValueError): expand(ledger)

    def test_cut_cannot_point_to_unrelated_fields(self):
        ledger = compact(); ledger["cuts"][0]["changes"][0]["shot"] = "片段1/分镜4"
        with self.assertRaises(ValueError): expand(ledger)

    def test_duplicate_edges_are_rejected(self):
        ledger = compact(); ledger["cuts"].append(deepcopy(ledger["cuts"][0]))
        with self.assertRaises(ValueError): expand(ledger)

    def test_mixed_state_sources_are_rejected(self):
        ledger = compact(); ledger["shots"][0]["state_in"] = {"a": 1}
        with self.assertRaises(ValueError): expand(ledger)

    def test_changed_cut_or_state_invalidates_review(self):
        for field in ("cut", "state", "card"):
            ledger = compact(); text = finish(ledger); before = review_digest(ledger, text)
            if field == "cut": ledger["cuts"][0]["changes"][0]["description"] += "changed"
            elif field == "state": ledger["shots"][1]["state_changes"]["董白.阶段"] = "蓄力"
            else: ledger["shots"][1]["performance"] = {"card": {"opening": "changed"}}
            self.assertNotEqual(review_digest(ledger, text), before)

    def test_expansion_never_creates_inspection_or_approval(self):
        ledger = compact(); ledger["shots"][0].pop("viewed_while_writing"); ledger["shots"][0].pop("source_audit")
        expanded = expand(ledger)
        self.assertNotIn("viewed_while_writing", expanded["shots"][0])
        self.assertNotIn("source_audit", expanded["shots"][0])
        self.assertNotIn("director_review", expanded)
        self.assertTrue(any("真实看图" in e for e in check(ledger)[0]))

    def test_dialogue_and_source_omissions_still_fail(self):
        ledger = compact(); ledger["panels"][0]["bubbles"][0]["script_text"] = "別の言葉。"
        self.assertTrue(any("来源／对白锁" in e for e in check(ledger)[0]))
        ledger = compact(); text = finish(ledger); ledger["shots"][3]["source_images"] = []
        self.assertTrue(check(ledger, text)[0])

    def test_pending_route_blocks_render_and_final_validation(self):
        text = render(compact()); ledger = routes(compact())
        with self.assertRaisesRegex(ValueError, "尚未获用户"): render(ledger)
        self.assertTrue(any("尚未获用户" in e for e in check(ledger, text)[0]))

    def test_confirmed_route_uses_existing_validation(self):
        self.assertEqual(check(routes(compact(), confirmed=True))[0], [])

    def test_changed_route_invalidates_user_confirmation(self):
        ledger = routes(compact(), confirmed=True)
        ledger["action_routes"][0]["path"] += "改为落地"
        with self.assertRaisesRegex(ValueError, "重新请用户确认"): check_routes(ledger)

    def test_missing_route_or_quote_is_not_confirmation(self):
        ledger = fixture(); ledger["requires_route_confirmation"] = True
        with self.assertRaises(ValueError): check_routes(ledger)
        ledger = routes(fixture(), True); ledger["action_routes"][0]["user_confirmation"]["quote"] = ""
        with self.assertRaises(ValueError): check_routes(ledger)

    def test_false_flag_cannot_bypass_an_existing_unconfirmed_route(self):
        ledger = routes(fixture()); ledger["requires_route_confirmation"] = False
        with self.assertRaises(ValueError): check_routes(ledger)

    def test_route_is_bound_into_source_lock(self):
        ledger = routes(fixture(), True); before = make_source_lock(ledger)
        ledger["action_routes"][0]["path"] += "新的解释"
        self.assertNotEqual(before, make_source_lock(ledger))

    def test_route_digest_cli_does_not_write_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"; ledger = routes(fixture())
            path.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
            before = path.read_bytes()
            run = subprocess.run([sys.executable, "-X", "utf8", str(HERE / "authoring.py"), str(path),
                                  "--route-digest", "test-route"], capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(run.stdout.decode().strip(), route_digest(ledger["action_routes"][0]))
            self.assertEqual(path.read_bytes(), before)

    def test_freezer_refuses_pending_route_without_modification(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"; ledger = routes(fixture()); ledger.pop("source_lock")
            path.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
            before = path.read_bytes()
            run = subprocess.run([sys.executable, "-X", "utf8", str(HERE / "freeze_storyboard.py"), str(path)], capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
