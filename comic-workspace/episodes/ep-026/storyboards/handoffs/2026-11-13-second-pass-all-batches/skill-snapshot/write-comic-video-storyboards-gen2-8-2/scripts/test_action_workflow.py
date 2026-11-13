"""Synthetic approval/scope regressions; no real user approval or visual claim."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from authoring import addition_digest, check_confirmations, route_digest
from render_storyboard import render
from test_director_282 import fixture, check
from validate_director import make_source_lock, review_digest

HERE = Path(__file__).parent


def action_ledger(addition_confirmed=True):
    ledger = fixture()
    route = {"id": "route-a", "source_images": ["a.jpg", "b.jpg"],
             "path": "软件测试：站立后跃出，到达腾空原作节点。", "performance_mode": "action"}
    route["user_confirmation"] = {
        "quote": "软件测试合成确认，不代表人类实际批准", "sha256": route_digest(route)}
    ledger["requires_route_confirmation"] = True
    ledger["action_routes"] = [route]
    addition = {"id": "addition-a", "route_id": "route-a", "source_images": ["a.jpg", "b.jpg"],
                "proposal": "软件测试：在两节点之间增加一次避让，不改变腾空落点。"}
    if addition_confirmed:
        approve(addition)
    ledger["action_additions"] = [addition]
    ledger["shots"][1]["action_addition_ids"] = ["addition-a"]
    ledger["source_lock"] = make_source_lock(ledger)
    return ledger


def approve(addition):
    addition["user_confirmation"] = {
        "quote": "软件测试合成确认，不代表人类实际批准", "sha256": addition_digest(addition)}


class ActionWorkflowTests(unittest.TestCase):
    def test_legacy_ledger_and_render_do_not_need_new_fields(self):
        ledger = fixture()
        before = deepcopy(ledger)
        check_confirmations(ledger)
        self.assertEqual(ledger, before)
        self.assertEqual(check(ledger)[0], [])

    def test_valid_addition_reuses_existing_renderer_and_validator(self):
        ledger = action_ledger()
        check_confirmations(ledger)
        self.assertEqual(check(ledger)[0], [])
        self.assertEqual(render(ledger), render(fixture()))

    def test_mode_only_is_valid_after_route_confirmation(self):
        ledger = action_ledger()
        ledger.pop("action_additions")
        ledger["shots"][1].pop("action_addition_ids")
        check_confirmations(ledger)
        ledger["action_routes"][0].pop("user_confirmation")
        with self.assertRaisesRegex(ValueError, "尚未获用户"):
            check_confirmations(ledger)

    def test_mode_does_not_rewrite_or_reapprove_original_route(self):
        ledger = action_ledger()
        route = ledger["action_routes"][0]
        original = route_digest(route)
        route.pop("performance_mode")
        self.assertEqual(route_digest(route), original)
        self.assertEqual(route["user_confirmation"]["sha256"], original)

    def test_invalid_mode_is_rejected_instead_of_silent_fallback(self):
        ledger = action_ledger()
        ledger["action_routes"][0]["performance_mode"] = "auto-approved"
        with self.assertRaisesRegex(ValueError, "performance_mode"):
            check_confirmations(ledger)

    def test_pending_addition_blocks_render_and_final_validation(self):
        text = render(fixture())
        ledger = action_ledger(False)
        with self.assertRaisesRegex(ValueError, "新增动作提案尚未获用户"):
            render(ledger)
        self.assertTrue(any("新增动作提案尚未获用户" in e for e in check(ledger, text)[0]))

    def test_changed_proposal_scope_or_route_invalidates_grant(self):
        for key, value in (("proposal", "改为另一招式"), ("source_images", ["b.jpg"]),
                           ("route_id", "another-route")):
            with self.subTest(key=key):
                ledger = action_ledger()
                ledger["action_additions"][0][key] = value
                with self.assertRaisesRegex(ValueError, "重新请用户确认"):
                    check_confirmations(ledger)

    def test_empty_quote_is_not_approval(self):
        ledger = action_ledger()
        ledger["action_additions"][0]["user_confirmation"]["quote"] = " "
        with self.assertRaisesRegex(ValueError, "尚未获用户"):
            check_confirmations(ledger)

    def test_addition_requires_marked_action_route(self):
        for route_id in ("missing-route", None, {"bad": "id"}):
            ledger = action_ledger()
            addition = ledger["action_additions"][0]
            addition["route_id"] = route_id
            approve(addition)
            with self.assertRaisesRegex(ValueError, "performance_mode"):
                check_confirmations(ledger)
        ledger = action_ledger()
        ledger["action_routes"][0].pop("performance_mode")
        with self.assertRaisesRegex(ValueError, "performance_mode"):
            check_confirmations(ledger)

    def test_addition_cannot_claim_panels_outside_its_route(self):
        ledger = action_ledger()
        extra = deepcopy(ledger["panels"][0]); extra["image"] = "c.jpg"
        ledger["panels"].append(extra)
        addition = ledger["action_additions"][0]
        addition["source_images"] = ["a.jpg", "c.jpg"]
        approve(addition)
        with self.assertRaisesRegex(ValueError, "超出所属动作路径"):
            check_confirmations(ledger)

    def test_unknown_duplicate_or_empty_shot_grant_is_rejected(self):
        for ids in (["unknown"], ["addition-a", "addition-a"], [], "addition-a"):
            with self.subTest(ids=ids):
                ledger = action_ledger()
                ledger["shots"][1]["action_addition_ids"] = ids
                with self.assertRaisesRegex(ValueError, "action_addition_ids"):
                    check_confirmations(ledger)

    def test_shot_cannot_borrow_an_unrelated_route_grant(self):
        ledger = action_ledger()
        addition = ledger["action_additions"][0]
        addition["source_images"] = ["a.jpg"]; approve(addition)
        ledger["shots"][1]["derived_from"] = ["b.jpg"]
        with self.assertRaisesRegex(ValueError, "无交集"):
            check_confirmations(ledger)

    def test_each_grant_must_have_actual_panel_overlap(self):
        ledger = action_ledger()
        first = ledger["action_additions"][0]
        first["source_images"] = ["a.jpg"]; approve(first)
        second = deepcopy(first); second.update(id="addition-b", source_images=["b.jpg"]); approve(second)
        ledger["action_additions"].append(second)
        ledger["shots"][1].update(derived_from=["a.jpg"], action_addition_ids=["addition-a", "addition-b"])
        with self.assertRaisesRegex(ValueError, "无交集"):
            check_confirmations(ledger)

    def test_continuous_source_shot_may_include_later_original_nodes(self):
        ledger = action_ledger()
        addition = ledger["action_additions"][0]
        addition["source_images"] = ["a.jpg"]; approve(addition)
        ledger["shots"][1].pop("action_addition_ids")
        shot = ledger["shots"][0]
        shot["source_images"] = ["a.jpg", "b.jpg"]
        shot["action_addition_ids"] = ["addition-a"]
        # Scope association only; existing anchor/merge validation still applies.
        check_confirmations(ledger)

    def test_effect_refinement_does_not_automatically_require_a_new_grant(self):
        ledger = fixture()
        ledger["shots"][1]["creative_additions"] = "合成测试：短促几何拖影后恢复清楚轮廓。"
        check_confirmations(ledger)
        self.assertNotIn("action_additions", ledger)

    def test_unresolved_shot_grant_cannot_hide_behind_missing_collection(self):
        ledger = action_ledger()
        ledger.pop("action_additions")
        with self.assertRaisesRegex(ValueError, "action_addition_ids"):
            check_confirmations(ledger)

    def test_source_lock_excludes_mode_and_added_action_permission(self):
        ledger = action_ledger()
        before = make_source_lock(ledger)
        ledger["action_routes"][0].pop("performance_mode")
        ledger["action_additions"][0]["proposal"] += "另一个拟增方案"
        approve(ledger["action_additions"][0])
        self.assertEqual(make_source_lock(ledger), before)

    def test_review_digest_changes_when_mode_or_permission_changes(self):
        for change in ("mode", "proposal", "quote"):
            with self.subTest(change=change):
                ledger = action_ledger(); text = render(ledger)
                before = review_digest(ledger, text)
                if change == "mode": ledger["action_routes"][0].pop("performance_mode")
                elif change == "proposal":
                    ledger["action_additions"][0]["proposal"] += "新拟增内容"
                    approve(ledger["action_additions"][0])
                else: ledger["action_additions"][0]["user_confirmation"]["quote"] += "合成更正"
                self.assertNotEqual(review_digest(ledger, text), before)

    def test_digest_cli_is_read_only_and_does_not_need_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            ledger = action_ledger(False)
            path.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
            before = path.read_bytes()
            run = subprocess.run([sys.executable, "-X", "utf8", str(HERE / "authoring.py"), str(path),
                                  "--addition-digest", "addition-a"], capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(run.stdout.decode().strip(), addition_digest(ledger["action_additions"][0]))
            self.assertEqual(path.read_bytes(), before)

    def test_freezer_refuses_pending_addition_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            ledger = action_ledger(False); ledger.pop("source_lock")
            path.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
            before = path.read_bytes()
            run = subprocess.run([sys.executable, "-X", "utf8", str(HERE / "freeze_storyboard.py"), str(path)],
                                 capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("新增动作提案", run.stderr.decode("utf-8"))
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
