"""Reproduce the image-reviewed revision without rewriting source images or history."""
from pathlib import Path
import copy
import hashlib
import json
import re
import runpy

OUT = Path(__file__).resolve().parent
EP = OUT.parents[2]
ROOT = EP.parents[2]
BASE = OUT.parent / 'gen2.8'
CURRENT = EP / 'storyboards/current/第20话_制作分镜_Gen2.8.md'
ARCHIVE = EP / 'storyboards/archive/2026-10-11_Gen2.8_运镜视线角色修订前'
NAMES = ['镜头设计', '可见动作', '可见背景', '台词与语气', '光影布光', '声音设计']
choices = runpy.run_path(str(OUT / 'revision_choices.py'))
P, S = choices['P'], choices['S']
baseline = (BASE / '第20话_制作分镜_Gen2.8.md').read_text(encoding='utf-8')
ledger = json.loads((BASE / 'source-ledger-v3.json').read_text(encoding='utf-8'))
assert len(P) == len(ledger['panels']) == 66
assert set(S) == {s['review_key'] for s in ledger['shots']}

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def parse(text):
    clips = list(re.finditer(r'^## 【片段(\d+)】（(\d+)秒）$', text, re.M))
    result = []
    for i, clip in enumerate(clips):
        end = clips[i+1].start() if i+1 < len(clips) else len(text)
        block = text[clip.end():end]
        shots = list(re.finditer(r'^\*\*分镜(\d+)（(\d+)秒）：\*\*$', block, re.M))
        for j, shot in enumerate(shots):
            stop = shots[j+1].start() if j+1 < len(shots) else len(block)
            piece = block[shot.end():stop]
            fields = [re.search(r'^【'+name+r'】：(.*)$', piece, re.M).group(1) for name in NAMES]
            ref = re.search(r'^分镜参考 .*$', piece, re.M)
            result.append({'target': f'片段{clip[1]}/分镜{shot[1]}', 'clip': int(clip[1]),
                           'number': int(shot[1]), 'seconds': int(shot[2]),
                           'reference': ref.group(0) if ref else '', 'fields': fields})
    return text[:clips[0].start()].rstrip(), result

preamble, records = parse(baseline)
assert len(records) == len(ledger['shots']) == 76
old_records = copy.deepcopy(records)
by_target = {r['target']: r for r in records}
shot_by_target = {s['target']: s for s in ledger['shots']}

# Keep the approved input and earlier delivery immutable.
ARCHIVE.mkdir(parents=True, exist_ok=True)
for name, source in [('第20话_制作分镜_Gen2.8.md', BASE/'第20话_制作分镜_Gen2.8.md'),
                     ('source-ledger-v3.json', BASE/'source-ledger-v3.json')]:
    dest = ARCHIVE/name
    if not dest.exists():
        dest.write_bytes(source.read_bytes())
    assert dest.read_bytes() == source.read_bytes()

registry = ROOT/'comic-workspace/character-references/角色映射.md'
profile = {
    'id': 'C002', 'canonical_name': '春子',
    'reference_paths': ['comic-workspace/character-references/turnarounds/春子.png'],
    'aliases': ['棕发女子', '黑衣女子'], 'status': 'confirmed',
    'discriminating_traits': '长棕发、半垂眼、齐刘海、黑色交领衣裙；身份沿用既有发生处核查。',
    'performance_profile': {
        'baseline': '三无角色，低情绪外显、表情变化幅度小、声线平直。以任务、视线、头肩朝向与回应节奏参与交流；保留当格明确眉眼和身体反射，不把直白语言扩成愤怒、嫌弃、警觉或情绪反转。',
        'source': '用户本轮明确指示“春子是三无角色但是写了太多情绪”；共享角色映射.md 的 C002 性能设定为唯一项目主档。',
        'registry_reference': registry.relative_to(ROOT).as_posix(),
        'registry_sha256': hashlib.sha256(registry.read_bytes()).hexdigest(),
    },
}
ledger['character_registry'] = [profile]
ledger['character_registry_source'] = registry.relative_to(ROOT).as_posix()
ledger['prior_advisory_dispositions'] = copy.deepcopy(ledger.get('advisory_dispositions', []))
ledger['advisory_dispositions'] = []

panel_by_id = {p['image'].replace('第20話_', '').replace('.jpg', ''): p for p in ledger['panels']}
removed_facts = {}
for pid, obs in P.items():
    panel = panel_by_id[pid]
    panel['prior_composition_lock'] = panel['composition_lock']
    panel['prior_source_facts'] = copy.deepcopy(panel['source_facts'])
    old_layout = re.sub(r'高俯视|略俯视|略仰视|偏俯|低角度|平视|俯视|仰视', '', panel['composition_lock'])
    panel['composition_lock'] = obs['angle'] + ' 布局：' + old_layout
    panel['camera_gaze_review'] = copy.deepcopy(obs)
    panel['camera_gaze_review'].update({'resolution': 'original' if 'escalation' in obs else '720p',
                                      'viewed_during_revision': True})
    terms = obs.get('remove_fact_terms', [])
    removed = []
    for kind in ['entities', 'actions', 'relations']:
        keep = []
        for fact in panel['source_facts'].get(kind, []):
            if any(term in fact for term in terms):
                removed.append((kind, fact))
            else:
                keep.append(fact)
        panel['source_facts'][kind] = keep
    removed_facts[panel['image']] = removed
    new_relations = list(obs.get('relations', []))
    for actor, gaze in obs['gaze'].items():
        if actor in panel['source_facts']['entities']:
            new_relations.append(actor + '：' + gaze)
    if obs.get('brow'):
        new_relations.append(obs['brow'])
    for fact in new_relations:
        if fact not in panel['source_facts']['relations']:
            panel['source_facts']['relations'].append(fact)

revised = []
for shot in ledger['shots']:
    spec = S[shot['review_key']]
    record = by_target[shot['target']]
    old = copy.deepcopy(record['fields'])
    f = record['fields']
    f[0] = spec['camera']
    for key, index in [('action', 1), ('background', 2), ('dialogue', 3), ('light', 4), ('sound', 5)]:
        if key in spec:
            f[index] = spec[key]
    if 'voice' in spec:
        assert len(re.findall(r'（[^（）]*）', f[3])) == 1
        f[3] = re.sub(r'（[^（）]*）', lambda _: '（'+spec['voice']+'）', f[3])
    shot['prior_camera_decision'] = copy.deepcopy(shot.get('camera_decision'))
    shot['camera_decision'] = {
        'mode': 'fixed' if spec['mode'].startswith('fixed') else spec['mode'], 'reason': spec['reason'],
        'anchor_phase': shot.get('camera_decision', {}).get('anchor_phase', 'middle'),
        'opening': spec['opening'], 'landing': spec['landing'],
    }
    if 'path_basis' in spec:
        shot['camera_decision']['path_basis'] = {
            'type': 'inspected_source_reframe',
            'source_refs': [panel_by_id[p]['image'] for p in spec['path_basis']],
            'scope': '沿已见图像内容的二维重构、摇移或收放；本轮没有无证据绕拍或新增隐面。',
        }
    shot['camera_excerpt'] = f[0]
    shot['action_excerpt'] = f[1]
    shot['reviewed_action_excerpt'] = f[1]
    shot['background_excerpt'] = f[2]
    shot['dialogue_excerpt'] = f[3]
    shot['revision_fields'] = [NAMES[i] for i in range(6) if f[i] != old[i]]
    owner_images = shot.get('source_images') or shot.get('derived_from', [])
    claims = shot['fact_claims']
    for kind in ['entities', 'actions', 'relations']:
        claims[kind] = [fact for fact in claims.get(kind, [])
                        if not any((kind, fact) in removed_facts.get(image, []) for image in owner_images)]
    if 'action' in spec:
        shot['prior_motion_decision'] = copy.deepcopy(shot.get('motion_decision'))
        shot['prior_action_admissions'] = copy.deepcopy(shot.get('action_admissions', []))
        if '春子' in f[1]:
            shot['purpose'] = spec['reason']
            shot['risk_basis'] = '低情绪角色任务与回应节奏复查；当前眉眼、视线和持续接触按源图及用户设定。'
            shot['evidence'] = '当前源格的任务、头肩朝向和眉眼锚点；春子按用户明确的三无基线演出。'
            shot['motion_decision'] = {'basis': shot['evidence'],
                                       'selected_performance': spec.get('performance', {}).get('beats', []),
                                       'endpoint': spec.get('performance', {}).get('landing', ''),
                                       'character_baseline': 'C002.performance_profile'}
            # Removed head-tilt/forward emotional arcs cannot remain future acting authority.
            shot['action_admissions'] = []
            primary_claims = {
                '03_002-source': ['手指收紧握柄'],
                '04_001-source': ['握刀前臂向下压落'],
                '04_003-source': ['青持续抓住春子手腕', '青身体前倾', '持刀前臂下压力减弱'],
                '07_001-source': ['青躯干后仰稳住承重'],
            }.get(shot['review_key'], [])
            for claim in primary_claims:
                shot['action_admissions'].append({
                    'claim': claim,
                    'visual_evidence': '源图已建立当前握柄、抓腕或横抱任务；该局部发展在已见躯干和手臂范围内发生，持续原有支撑与所有权，回到图中接触锚点。表演幅度受三无人物基线约束。',
                    'source_image': owner_images[0], 'visible_in_framing': True, 'anchor_safe': True,
                })
        elif shot['review_key'] in ['15_001-source', '18_003-source']:
            shot['evidence'] = '已看图确认三槽面盔遮住青梅男嘴部；颈侧、汗滴与头颈姿态可见。'
            shot['purpose'] = spec['reason']
            shot['motion_decision'] = {'basis': shot['evidence'], 'development': spec['performance']['beats'],
                                       'endpoint': spec['performance']['landing']}
    revised.append({'target': shot['target'], 'review_key': shot['review_key'],
                    'source_images': owner_images, 'fields': shot['revision_fields'],
                    'camera': copy.deepcopy(shot['camera_decision'])})

for shot in ledger['shots']:
    if shot['review_key'] == '11_001-source':
        shot['motion_decision'] = 'Action，巨大手掌持续按地，白亮环纹从已见掌指局部起流并收束；不补施法者或攻击方向。'
    if shot['review_key'] == '23_003-source':
        shot['motion_decision'] = 'Action，开放手从眼侧短移到唇前窄隙；后续切来者响指，未声称青发生手唇接触。'

existing_performance = {p['target'] for p in ledger['performance']}
for shot in ledger['shots']:
    spec = S[shot['review_key']]
    if 'performance' in spec and shot['target'] not in existing_performance:
        ledger['performance'].append({'target': shot['target'], 'evidence': shot['evidence'],
                                     'card': copy.deepcopy(spec['performance']),
                                     'details': [by_target[shot['target']]['fields'][1]]})

for perf in ledger['performance']:
    shot = shot_by_target[perf['target']]
    spec = S[shot['review_key']]
    record = by_target[perf['target']]
    if 'performance' in spec:
        perf['prior_card'] = copy.deepcopy(perf['card'])
        perf['card'] = copy.deepcopy(spec['performance'])
    if 'action' in spec:
        perf['details'] = [record['fields'][1]]
        perf['evidence'] = shot['evidence']
    perf['camera_review'] = {'mode': spec['mode'], 'landing': spec['landing'],
                             'performer_endpoint_separate': True}

# One authoritative profile in the project master, with self-contained shot execution.
preamble = preamble.replace('人物设计采用共享参考图库，当前衣物状态和伤势以本话源格为准。',
    '人物设计采用共享参考图库，当前衣物状态和伤势以本话源格为准。春子为三无角色：低情绪外显、头肩自然、目光明确，声音偏低清晰而平直；她以持续任务和回应节奏参与交流，眉眼保持本镜写明的幅度。')
parts = [preamble, '']
for clip in sorted({r['clip'] for r in records}):
    selected = [r for r in records if r['clip'] == clip]
    seconds = sum(r['seconds'] for r in selected)
    assert seconds <= 15
    parts += [f'## 【片段{clip}】（{seconds}秒）', '']
    for r in selected:
        parts.append(f'**分镜{r["number"]}（{r["seconds"]}秒）：**')
        if r['reference']:
            parts.append(r['reference'])
        parts += [f'【{name}】：{value}' for name, value in zip(NAMES, r['fields'])]
        parts.append('')
output = '\n'.join(parts).rstrip() + '\n'
_, verify = parse(output)
assert [(r['target'], r['seconds'], r['reference']) for r in verify] == [
    (r['target'], r['seconds'], r['reference']) for r in old_records]
quoted = lambda field: re.findall(r'“([^”]+)”', field)
assert [quoted(r['fields'][3]) for r in verify] == [quoted(r['fields'][3]) for r in old_records]
assert [p['bubbles'] for p in ledger['panels']] == [
    p['bubbles'] for p in json.loads((BASE/'source-ledger-v3.json').read_text(encoding='utf-8'))['panels']]

ledger['revision_audit'].append({
    'revision': '2026-10-11-camera-gaze-character-review',
    'reason': '用户要求全量修复保守运镜、俯仰角度、镜头方向视线，以及春子情绪和配音OOC。',
    'reviewed_images': [p['image'] for p in ledger['panels']],
    'original_reinspection': ['第20話_15_001.jpg'],
    'unchanged': ['全部日文引号内对白、归属、顺序', '34片段/76镜/356秒/66正式参考',
                  '横抱形成桥及所有权、腕部接触、左右手捋袖', '战斗模块关闭', '跨话场景对照暂缓'],
    'resolution': revised,
})
ledger['final_audit']['prior_camera_character_audit'] = copy.deepcopy(ledger['final_audit'])
ledger['final_audit']['scope'] = '本话66张来源、76镜全量运镜/角度/视线复查；既有非露骨改编裁切持续。'
ledger['final_audit']['camera_character_revision'] = {
    'camera_reviewed': 76, 'source_images_viewed': 66,
    'new_unsupported_camera_orbits': 0, 'timing_preserved': True,
    'source_dialogue_preserved': True, 'character_profile': profile,
    'manual_video_generation_checked': False,
}
ledger['final_audit']['reviewed_images'] = [p['image'] for p in ledger['panels']]
ledger['final_audit']['original_resolution_reinspection'] = [
    {'image': '第20話_15_001.jpg', 'reason': P['15_001']['escalation']}]
ledger['final_audit']['validation_summary'] = {'status': 'pending_current_validator'}

CURRENT.write_text(output, encoding='utf-8')
(OUT/'storyboard.md').write_text(output, encoding='utf-8')
write_json(OUT/'source-ledger-v3.json', ledger)
write_json(OUT/'revision-plan.json', {'panels': P, 'shots': S})
write_json(OUT/'change-index.json', revised)
print('Revised 76 camera fields and image-reviewed acting/gaze; 34 clips, 356 seconds, 66 references retained.')
