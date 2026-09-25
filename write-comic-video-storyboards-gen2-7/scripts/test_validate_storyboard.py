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
    action = "人物手指轻微收紧。" if line is None else "人物手掌朝上，手指稳定托住画外物件。"
    speech = "无台词。" if line is None else f"人物：“{line}”（清晰的中性音色，平静语气）。"
    return f"""## 场景色彩基准
二维手绘质感，中等对比。

## 【片段1】测试

**分镜1（5秒）：**
分镜参考 `[panel.jpg]`
场景环境：{background}，深蓝灰放射线向外扩张。
环境音：低环境底噪从画面后方持续传来。
镜头设计：平视手部特写，固定镜头。
可见动作：{action}
台词与语气：{speech}
光影布光：柔和侧光照亮手指轮廓，掌心保留浅影。
声音设计：低环境底噪铺底，手指收紧时衣料轻响。
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

    def test_sound_design_is_allowed(self) -> None:
        text = storyboard().replace(
            BACKGROUND,
            BACKGROUND + "。\n声音设计：远处人声铺底，手指收紧时衣料轻响。",
        )
        result = self.run_validator(text, valid_ledger(), require_ledger=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("含音效或音乐字段", result.stdout)
        audio_alias = text.replace("声音设计：", "音频：")
        alias_result = self.run_validator(audio_alias, valid_ledger(), require_ledger=True)
        self.assertEqual(alias_result.returncode, 0, alias_result.stdout + alias_result.stderr)

    def test_long_dialogue_with_thin_acting_emits_warning(self) -> None:
        long_line = "あ" * 30
        result = self.run_validator(storyboard(line=long_line))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("类表演信号", result.stdout)

    def test_three_second_standalone_clip_requires_merge_review(self) -> None:
        text = storyboard().replace("分镜1（5秒）", "分镜1（3秒）")
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("总时长仅3秒", result.stdout)
        self.assertIn("连续性审计", result.stdout)

    def test_expressive_summary_fails_performance_fidelity_warnings(self) -> None:
        text = storyboard(line="いりません、いりません！").replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "人物手腕后撤、肩膀缩起，连续摇头时发梢向后拖；"
            "视线在石头和对方之间折返，最后手指停住。",
        ).replace(
            "平视手部特写，固定镜头。",
            "35mm双人中近景，摄影机小幅横移，焦点跟随手部。",
        ).replace(
            "低环境底噪铺底，手指收紧时衣料轻响。",
            "晶石轻碰掌心，拒绝声与手腕后撤同步。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("表演保真槽缺少", result.stdout)
        self.assertIn("没有镜头落幅", result.stdout)
        self.assertIn("重复话语但声音设计没有区分", result.stdout)

    def test_staged_expressive_performance_passes_fidelity_warnings(self) -> None:
        text = storyboard(line="いりません、いりません！").replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "人物先把物件向前送出半掌，第一声拒绝时手腕迅速后撤，肩膀随后向内缩；"
            "第二声拒绝时眼睑压紧，嘴唇先合拢再张开，头部连续摇动，"
            "发梢晚半拍向反方向甩开后回弹，最后双手停在交接处。",
        ).replace(
            "平视手部特写，固定镜头。",
            "35mm双人中近景，摄影机跟随物件往返移动，句末在双方交接处稳住。",
        ).replace(
            "低环境底噪铺底，手指收紧时衣料轻响。",
            "第一声拒绝带短促回响，第二声与手腕后撤同步并迅速收干。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("表演保真槽缺少", result.stdout)
        self.assertNotIn("没有镜头落幅", result.stdout)
        self.assertNotIn("重复话语但声音设计没有区分", result.stdout)

    def test_repeated_words_split_across_quotes_need_audio_contrast(self) -> None:
        text = storyboard(line="いや！").replace(
            '人物：“いや！”（清晰的中性音色，平静语气）。',
            '人物：“いや！”（清晰的中性音色，急促语气）。\n'
            '人物：“いや！”（清晰的中性音色，急促语气）。',
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("重复话语但声音设计没有区分", result.stdout)

    def test_single_elongated_utterance_is_not_repetition(self) -> None:
        result = self.run_validator(storyboard(line="うううっ……せめて教えてください……"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("重复话语但声音设计没有区分", result.stdout)

    def test_conflicting_depth_is_a_warning_not_error(self) -> None:
        text = storyboard().replace("固定镜头", "固定镜头，大光圈、全景深")
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("同时声明浅景深/大光圈与大景深", result.stdout)

    def test_repeated_atmosphere_effect_emits_warning(self) -> None:
        blocks = "\n".join(
            f"""**分镜{i}（2秒）：**
分镜参考 `[panel.jpg]`
场景环境：{BACKGROUND}，微尘漂浮。
环境音：低环境底噪从画面后方持续传来。
镜头设计：50mm平视手部特写，固定镜头。
可见动作：手掌朝上，手指稳定托住物件。
台词与语气：无台词。
光影布光：柔和侧光照亮手指，微尘停在暗部。
声音设计：低环境底噪铺底，衣料发出轻响。
"""
            for i in range(1, 5)
        )
        text = f"## 场景色彩基准\n二维手绘质感。\n\n## 【片段1】测试\n\n{blocks}"
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("片段1的微尘出现在4/4个镜头", result.stdout)

    def test_three_second_micro_action_chain_has_no_capacity_warning(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "平视近景，固定镜头。听见呼唤后先停住，眼睑微抬，嘴角放松，短吸气；"
            "指尖在衣料上收紧，衣摆随惯性晚半拍回落，视线最终留在说话者身上。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("主要动作", result.stdout)
        self.assertNotIn("类表演信号", result.stdout)

    def test_sentence_end_settle_counts_as_performance_endpoint(self) -> None:
        long_line = "あ" * 30
        text = storyboard(line=long_line).replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "平视近景，听见问话后先停顿，视线转向对方；眉梢稍后松开，"
            "短促吸气，指尖捏住衣角，句末松手并让肩线回落。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("可能只有动作清单", result.stdout)

    def test_major_action_overload_is_soft_warning(self) -> None:
        text = storyboard().replace(
            "分镜1（5秒）", "分镜1（2秒）"
        ).replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "平视中景，人物起身转身迈步跑向门口推开门。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("主要动作", result.stdout)

    def test_contextual_pointing_is_not_generic_gesture_warning(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "平视中景，人物抬手指向桌上的晶石，视线随指尖落定。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("主要依赖抬手", result.stdout)

    def test_audio_line_with_hidden_visual_action_warns(self) -> None:
        text = storyboard().replace(
            BACKGROUND,
            BACKGROUND + "。\n声音设计：人物转身走向门并打开门，随后传来门轴声。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("声音设计疑似包含新的视觉动作", result.stdout)

    def test_atmosphere_with_visible_source_does_not_warn(self) -> None:
        blocks = "\n".join(
            f"""**分镜{i}（2秒）：**
分镜参考 `[panel.jpg]`
场景环境：窗边蒸汽缓慢上升，{BACKGROUND}。
环境音：窗边风声和蒸汽轻响从画面右侧传来。
镜头设计：50mm平视近景，固定镜头。
可见动作：手掌朝上，手指稳定托住物件。
台词与语气：无台词。
光影布光：逆光穿过蒸汽形成微尘可见的光束。
声音设计：低环境底噪铺底，蒸汽发出轻响。
"""
            for i in range(1, 5)
        )
        text = f"## 场景色彩基准\n二维手绘质感。\n\n## 【片段1】测试\n\n{blocks}"
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("多数缺少可见依据", result.stdout)

    def test_re0_fields_are_required(self) -> None:
        text = storyboard().replace("镜头设计：", "摄影设计：")
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("缺少独立字段：镜头设计", result.stdout)

    def test_cross_shot_and_negative_meta_prose_fail(self) -> None:
        for phrase in ("保持原有构图", "上一格人物站在左侧", "不新增飞鸟", "不使用背景"):
            text = storyboard().replace(
                "人物手掌朝上，手指稳定托住画外物件。",
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
            "人物手掌朝上，手指稳定托住画外物件。",
            "人物起幅为朝画面右侧的三分之二侧脸，听见问话后瞳孔先回到左侧；"
            "随后下巴轻收、脸转向正面，一侧眉梢松开，句末肩线回落，视线停在说话者身上。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("6秒对白镜头但可见动作只有", result.stdout)

    def test_pure_object_explanation_does_not_require_body_signals(self) -> None:
        text = storyboard().replace("分镜1（5秒）", "分镜1（6秒）").replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "说明性物件镜头，人物未入画；晶石亮点沿棱线逐层显现，"
            "随后焦点移向金属边缘，最后两件物体稳定在并置构图。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("6秒对白镜头但可见动作只有", result.stdout)
        self.assertNotIn("类表演信号", result.stdout)

    def test_chinese_dialogue_trigger_paraphrase_fails(self) -> None:
        line = "前は暗石区の入口だけだったのに、今は全部封鎖されてる。"
        text = storyboard(line=line).replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "提到暗石区入口时，人物视线收紧。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("用中文概括对白触发点", result.stdout)

    def test_verbatim_japanese_dialogue_trigger_passes(self) -> None:
        line = "前は暗石区の入口だけだったのに、今は全部封鎖されてる。"
        text = storyboard(line=line).replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "说到「暗石区の入口」时，人物视线收紧。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unestablished_counted_gaze_target_fails(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "人物的视线落向对面的两名少女，手指随后放松。",
        )
        result = self.run_validator(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("未在本镜建立的两名少女", result.stdout)

    def test_directional_gaze_target_is_self_contained(self) -> None:
        text = storyboard().replace(
            "人物手掌朝上，手指稳定托住画外物件。",
            "人物的视线转向画面右侧外，手指随后放松。",
        )
        result = self.run_validator(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_terminal_uncited_coverage_before_source_shot_warns(self) -> None:
        base = storyboard().replace(
            f"场景环境：{BACKGROUND}，深蓝灰放射线向外扩张。",
            "场景环境：浅发少女位于画面左侧，木杯占据右前景，暖色墙面填满背景。",
        ).replace("平视手部特写", "平视人物近景")
        first = base.replace("分镜参考 `[panel.jpg]`\n", "")
        second = base.split("## 【片段1】", 1)[1]
        second = "## 【片段2】" + second.replace("测试", "下一格", 1)
        result = self.run_validator(first + "\n" + second)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("末镜为无参考补镜", result.stdout)


if __name__ == "__main__":
    unittest.main()
