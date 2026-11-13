"""Semantic records do not prove image understanding; test preservation and realization."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_director_282 import fixture, check, finish, HERE
from validate_director import make_source_lock
from render_storyboard import render


def continuous_take():
    ledger = fixture()
    first, last = ledger['shots'][0], ledger['shots'][-1]
    first['duration'] = 8
    first['source_images'] = ['a.jpg', 'b.jpg']
    first['merge_basis'] = '合成测试：同一固定观察关系内，连续拍到站立、蹬地与腾空，不含切镜。'
    first['fields']['镜头设计'] = ('平视中景，董白在中央前景，墙面处于后景；固定机位。\n'
        '- 参考 [a.jpg]（起势）：董白在中央前景站立，墙面位于后层。\n'
        '- 参考 [b.jpg]（过程）：董白在中央前景腾空，剑位于身体右侧。')
    first['fields']['可见动作'] = '董白右手持剑站立，压低重心，蹬地跃起后腾空前行。'
    first['state_out'] = deepcopy(last['state_out'])
    first['anchors'] = []
    for i, old in enumerate((first, last)):
        first['anchors'].append({'image': ('a.jpg', 'b.jpg')[i], 'start': (0, 5)[i],
            'anchor_phase': old['anchor_phase'], 'anchor_elements': old['anchor_elements'],
            'anchor_state': deepcopy(old['anchor_state']),
            'action_excerpt': ('右手持剑站立', '蹬地跃起后腾空前行')[i]})
    ledger['shots'] = [first]
    ledger['panels'][1]['anchor_target'] = first['target']
    return ledger


def moving_node():
    ledger = fixture()
    panel = ledger['panels'][1]
    panel['narrative_kind'] = 'action'
    panel['action_reading'] = {
        'summary': '合成测试：人物在空中迎面冲来', 'phase': '冲刺过程',
        'world_motion': '由后方向前方目标趋近', 'screen_motion': '朝摄影机趋近',
        'grounding': '腾空', 'basis': '合成测试预设，不冒充实际看图', 'uncertainty': ''}
    ledger['shots'][-1]['fields']['可见动作'] = '董白保持右手持剑，在空中迎面冲向镜头，发束拖向身后。'
    ledger['shots'][-1]['meaning_excerpt'] = '在空中迎面冲向镜头'
    ledger['source_lock'] = make_source_lock(ledger)
    return ledger


def unknown_cast():
    ledger = fixture()
    ledger['character_registry'].append({'id': 'U001', 'canonical_name': '短发访客',
        'aliases': ['陌生女孩'], 'identity_status': 'unidentified',
        'performance_profile': {'baseline': '长期性格未确认；本场策略谨慎观察', 'source': '合成测试情境'},
        'color_prompt': '短发访客：深棕短发，暖米肤色，棕眼，靛蓝上衣，黄铜纽扣；保持原有版型。',
        'color_basis': '合成测试生产配色，非官方颜色'})
    ledger['shots'][1]['characters'].append('短发访客')
    return ledger


class MeaningAndRegistryTests(unittest.TestCase):
    def test_continuous_panels_are_one_shot_without_losing_nodes(self):
        ledger = continuous_take()
        self.assertEqual(check(ledger)[0], [])
        self.assertEqual(render(ledger).count('**分镜'), 1)
        self.assertEqual(len(ledger['shots'][0]['anchors']), 2)

    def test_merged_take_passes_complete_cli_including_phase_bullets(self):
        ledger = continuous_take(); text = finish(ledger)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p/'s.md').write_text(text, encoding='utf-8')
            (p/'l.json').write_text(json.dumps(ledger, ensure_ascii=False), encoding='utf-8')
            r = subprocess.run([sys.executable, '-X', 'utf8', str(HERE/'validate_storyboard.py'),
                str(p/'s.md'), '--source-ledger', str(p/'l.json'), '--require-source-ledger'],
                capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stdout+r.stderr)

    def test_merged_take_wrong_order_fails(self):
        l = continuous_take(); l['shots'][0]['source_images'].reverse()
        self.assertTrue(check(l)[0])

    def test_merged_take_missing_node_state_fails(self):
        l = continuous_take(); l['shots'][0]['anchors'][1]['anchor_state']['董白.阶段'] = '站立'
        self.assertIn('未收束', '\n'.join(check(l)[0]))

    def test_merged_take_missing_action_realization_fails(self):
        l = continuous_take(); l['shots'][0]['anchors'][1]['action_excerpt'] = '并未出现的动作'
        self.assertIn('未落实', '\n'.join(check(l)[0]))

    def test_merged_take_node_times_must_advance(self):
        l = continuous_take(); l['shots'][0]['anchors'][1]['start'] = 0
        self.assertIn('严格递增', '\n'.join(check(l)[0]))

    def test_action_meaning_is_realized_and_frozen(self):
        l = moving_node(); self.assertEqual(check(l)[0], [])
        l['panels'][1]['action_reading']['screen_motion'] = '远离摄影机'
        self.assertIn('来源／对白锁', '\n'.join(check(l)[0]))

    def test_dynamic_meaning_cannot_be_only_a_ledger_label(self):
        l = moving_node(); l['shots'][-1]['fields']['可见动作'] = '董白站立，瞪眼。'
        self.assertIn('动作含义须落实', '\n'.join(check(l)[0]))

    def test_declared_action_requires_actual_reading(self):
        l = fixture(); l['panels'][1]['narrative_kind'] = 'action'; l['source_lock'] = make_source_lock(l)
        self.assertIn('动作含义复核', '\n'.join(check(l)[0]))

    def test_action_ambiguity_is_warning_not_creative_proof_gate(self):
        l = moving_node(); l['panels'][1]['action_reading']['uncertainty'] = '合成例中的完整离地过程未画'
        l['source_lock'] = make_source_lock(l)
        errors, warnings = check(l)
        self.assertEqual(errors, []); self.assertTrue(any('[动作理解]' in v for v in warnings))

    def test_unknown_character_colors_at_opening_and_renderer_pure(self):
        l = unknown_cast(); before = deepcopy(l); text = render(l)
        self.assertEqual(l, before)
        self.assertLess(text.index('U001｜短发访客'), text.index('## 【片段1】'))
        self.assertEqual(check(l)[0], [])

    def test_unknown_character_missing_colors_not_silently_omitted(self):
        l = unknown_cast(); del l['character_registry'][1]['color_prompt']
        with self.assertRaises(ValueError): render(l)

    def test_color_header_cannot_be_removed(self):
        l = unknown_cast(); text = finish(l)
        text = text.replace('- U001｜短发访客：'+l['character_registry'][1]['color_prompt'], '')
        self.assertIn('脚本开头', '\n'.join(check(l, text)[0]))

    def test_alias_in_cast_is_not_a_second_character(self):
        l = unknown_cast(); l['shots'][1]['characters'][-1] = '陌生女孩'
        self.assertIn('称呼须统一', '\n'.join(check(l)[0]))

    def test_duplicate_character_id_fails(self):
        l = unknown_cast(); l['character_registry'][0]['id'] = 'U001'
        self.assertIn('稳定ID', '\n'.join(check(l)[0]))

    def test_alias_cannot_be_another_characters_canonical_name(self):
        l = unknown_cast(); l['character_registry'][1]['aliases'].append('董白')
        self.assertIn('另一统一称呼', '\n'.join(check(l)[0]))

    def test_master_snapshot_version_change_invalidates_review(self):
        l = fixture(); l['character_registry_source'] = {'path': '角色映射.md', 'version': 4}
        text = finish(l); l['character_registry_source']['version'] = 5
        self.assertIn('已过期', '\n'.join(check(l, text)[0]))


if __name__ == '__main__':
    unittest.main()
