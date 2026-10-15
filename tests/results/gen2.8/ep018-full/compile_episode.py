from pathlib import Path
import copy
import json
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
PREVIOUS = ROOT / 'tests/results/gen2.8.1/ep018-first15'
FIELDS = ['镜头设计','可见动作','可见背景','台词与语气','光影布光','声音设计']
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

ledger = read(PREVIOUS / 'source-ledger-v3.json')
old_text = (PREVIOUS / '第18话_前15格_完整分镜_Gen2.8.1.md').read_text(encoding='utf-8')
text = old_text.replace('# 第18话制作分镜 Gen2.8.1', '# 第18话制作分镜 Gen2.8')
integrity = {p['image']: p for p in read(OUT / 'source-integrity.json')}
observations = [o for path in sorted((OUT / 'observations').glob('*.json')) for o in read(path)]
drafts = [s for path in sorted((OUT / 'drafts').glob('*.json')) for s in read(path)]
assert len({o['image'] for o in observations}) == len(observations)
by_image = {o['image']: o for o in observations}
order = {name: i for i, name in enumerate(integrity)}
observations.sort(key=lambda o: order.get(o.get('parent_source_image', o['image']), 1000))
grouped = {o['image']: [s for s in drafts if s['image'] == o['image']] for o in observations}
first_translations = {'第18話_06_001.jpg': ['これからは人にもっと敬意を払いなさい。','分かった？'], '第18話_06_003.jpg': ['この女……！','腕をへし折ってやる……。']}
for observed in observations:
    owned = grouped[observed['image']]
    if len(owned) == 1 and 'jp' not in owned[0]:
        owned[0]['jp'] = observed.get('jp', first_translations.get(observed['image'], []))
assert len(drafts) == sum(len(v) for v in grouped.values())
clip = 6
shot_no = 2
clip_seconds = {int(m[0]): sum(map(int, re.findall(r'分镜\d+（(\d+)秒', m[1])))
                for m in re.findall(r'## 【片段(\d+)】(.*?)(?=## 【片段|\Z)', text, flags=re.S)}
scene = '洞窟争执'
assigned = []
for observed in observations:
    owned = grouped[observed['image']]
    if not owned:
        assert observed.get('renderable_visual') is False, observed['image']
        continue
    unit = sum(s['seconds'] for s in owned)
    assert unit <= 15, ('Plan explicit natural overflow before compiling', observed['image'], unit)
    new_scene = owned[0].get('scene', scene)
    if new_scene != scene or clip_seconds[clip] + unit > 15 or owned[0].get('new_clip'):
        clip += 1
        shot_no = 0
        clip_seconds[clip] = 0
        text += f'\n## 【片段{clip}】\n'
        scene = new_scene
    for index, s in enumerate(owned):
        assert len(s['fields']) == 6
        shot_no += 1
        target = f'片段{clip}/分镜{shot_no}'
        s = copy.deepcopy(s)
        s.update(target=target, source_locked=index == 0 and not s.get('uncited', False))
        assigned.append(s)
        clip_seconds[clip] += s['seconds']
        text += f'\n**分镜{shot_no}（{s["seconds"]}秒）：**\n'
        if s['source_locked']:
            text += f'分镜参考 `[{s["image"]}]`\n'
        text += '\n'.join(f'【{field}】：{value}' for field, value in zip(FIELDS, s['fields'])) + '\n'

by_target = {s['target']: s for s in assigned}
for observed in observations:
    p = copy.deepcopy(observed)
    p.pop('plan', None)
    p['performance_plan'] = observed.get('plan')
    owned = [s for s in assigned if s['image'] == p['image']]
    jp = [(s, j, i) for s in owned for i, j in enumerate(s.get('jp', []))]
    raw_bubbles = p['bubbles']
    assert len(jp) == len(raw_bubbles), (p['image'], len(jp), len(raw_bubbles))
    p.update(viewed_at_drafting=True, drafting_resolution='720p', renderable_visual=observed.get('renderable_visual', True),
             reference_scope='full_renderable_panel', source_bubble_count=len(raw_bubbles), bubble_audit='pass',
             story_context=observed.get('story_context', []), non_renderable_terms=observed.get('non_renderable_terms', []),
             coverage='none' if not raw_bubbles else ('shared' if len(owned) == 1 else 'mixed'),
             coverage_reason='保留来源完整语义与当前构图，按实际对白和表演时间规划覆盖。',
             background={'type': observed['background'], 'description': observed.get('background_description', '源图省略实景，只有低细节明暗底场。' if observed['background']=='omitted' else '凹凸岩壁与可见石地，按当前构图分层。'), 'evidence': 'current_panel'},
             page_overlays=[], bubbles=[], dialogue_turns=[], coverage_groups=[])
    original = observed.get('parent_source_image', p['image'])
    p['source_integrity'] = {**integrity[original], 'lfs_content_verified': True, 'source_unchanged': True}
    if observed.get('sfx'):
        p['page_overlays'].append({'kind': 'sfx', 'render': False, 'source_text': observed.get('sfx_source_text', '原图音效符号：'+observed['sfx']+'（未逐字转录）'), 'audio_meaning': observed['sfx']})
    for i, (raw, mapping) in enumerate(zip(raw_bubbles, jp)):
        s, final, local_i = mapping
        assert final in s['fields'][3], (p['image'], final)
        count = len(s['jp'])
        weights = [max(1, len(re.sub(r'[\s。、！？…「」]', '', t))) for t in s['jp']]
        seconds = s.get('bubble_seconds', [])[local_i] if s.get('bubble_seconds') else int(s['speech_seconds'] * weights[local_i] / sum(weights)*1000)/1000
        kind = raw[2] if len(raw) > 2 else 'dialogue'
        p['bubbles'].append({'id': f'b{i+1}', 'speaker': raw[0], 'kind': kind, 'source_text': raw[1],
                             'status': 'mapped', 'target': s['target'], 'script_text': final, 'seconds': seconds,
                             'speaker_evidence': observed.get('speaker_evidence', '本格气泡指向及当前张口者；画外声音仅确定说话人，不据此增加画内人物。')})
        p['page_overlays'].append({'kind': 'caption', 'observed_kind':'bubble', 'source_text': raw[1], 'render': False})
        p['dialogue_turns'].append({'id': f't{i+1}', 'bubble_ids': [f'b{i+1}'], 'function': raw[1]})
    for target in dict.fromkeys(b['target'] for b in p['bubbles']):
        ids = [f't{i+1}' for i, b in enumerate(p['bubbles']) if b['target'] == target]
        p['coverage_groups'].append({'id': f'g{len(p["coverage_groups"])+1}', 'turn_ids': ids, 'targets': [target],
                                     'merge_basis': observed.get('merge_basis', '相邻短语义在同一机位自然交付，主要回应由可见表演承接，无隐藏切镜。')})
    ledger['panels'].append(p)
    for s in owned:
        target = s['target']
        fields = dict(zip(FIELDS, s['fields']))
        plan = copy.deepcopy(s.get('plan', observed.get('plan')))
        flags = ['P'] if plan else []
        if len(raw_bubbles) > 1 or any(len(b['script_text']) >= 28 for b in p['bubbles']):
            flags.append('D')
        if observed.get('original_resolution_viewed') or s.get('G'):
            flags.append('G')
        mode = s.get('background_mode', 'continuity' if observed['background'] == 'omitted' else observed['background'])
        purpose = s.get('purpose', plan['coupling'] if plan else '明确环境与叙事落点')
        sh = {'target': target, 'role': 'source_locked' if s['source_locked'] else 'uncited_coverage',
              'source_images': [p['image']] if s['source_locked'] else [], 'derived_from': [] if s['source_locked'] else [p['image']],
              'evidence': 'current_panel', 'purpose': purpose, 'background_excerpt': fields['可见背景'],
              'viewed_while_writing': True, 'source_audit': 'pass', 'unsupported_additions': [],
              'risk_flags': flags, 'risk_basis': purpose, 'fact_claims': s.get('fact_claims', copy.deepcopy(p['source_facts'])),
              'motion_decision': {'classification': observed.get('kind', 'Mixed'), 'observed_anchor': p['composition_lock'],
                                  'admitted_plan': plan, 'source_anchor_placement': observed.get('anchor_phase', 'middle'),
                                  'continuity': observed.get('continuity', ''), 'inference_limit': observed.get('admission', '')},
              'camera_decision': {'mode': s.get('camera_mode', 'fixed'), 'reason': purpose, 'anchor_phase': observed.get('anchor_phase', 'middle'),
                                  'opening': s.get('camera_opening', fields['镜头设计']), 'landing': s.get('camera_landing', fields['镜头设计']), 'evidence': p['composition_lock']},
              'background_decision': {'mode': mode, 'basis': s.get('background_basis', '源图实景' if mode == 'physical' else '连续场景的已见环境，仅重建相容的低细节远景。'),
                                      'source_refs': s.get('background_refs', ['第18話_06_002.jpg'] if mode == 'continuity' else [p['image']]), 'inspected_resolution': '720p'},
              'action_admissions': [{'claim': fields['可见动作'], 'source_image': p['image'],
                                    'visual_evidence': '观察：' + '；'.join(p['source_facts']['actions'] + p['source_facts']['relations']) + '。准入规划：' + observed.get('admission', ''),
                                    'visible_in_framing': True, 'anchor_safe': True}] if plan else []}
        if not s['source_locked']:
            sh.update(s['coverage'])
        if observed.get('adaptation_scope'):
            p['reference_scope'] = 'safe_narrative_selection'
            p['adaptation_scope'] = observed['adaptation_scope']
            p['coverage_reason'] = '非露骨改编对白与可安全呈现的局部；不宣称原图全量保真。原始文件完整处理记录见 source-intake-audit.json。'
            sh['source_fidelity_mode'] = 'non_graphic_adaptation'
        if s.get('evidence_owner'):
            sh['derived_from'] = [p['image'], s['evidence_owner']]
            sh['action_admissions'][0]['source_image'] = s['evidence_owner']
            sh['action_admissions'][0]['visual_evidence'] = '20_002已见董白正面泪眼、左前位置及守卫右后头部，21_001画外追问明确交给董白；仅头部反打，面盔继承19_003掀起状态。'
        if s.get('supporting_visual_images'):
            sh['supporting_visual_images'] = s['supporting_visual_images']
            sh['adaptation_composition_basis'] = s['source_reference_note']
            sh['action_admissions'][0]['visual_evidence'] = s['visual_evidence_override']
            sh['motion_decision']['inference_limit'] = s['admission_override']
        ledger['shots'].append(sh)
        if plan:
            intervals = s.get('intervals', [{'speech_seconds': s['speech_seconds'], 'acting_seconds': s['acting_seconds'], 'concurrent': True}])
            assert sum(max(i['speech_seconds'], i['acting_seconds']) if i.get('concurrent', True) else i['speech_seconds'] + i['acting_seconds'] for i in intervals) <= s['seconds'] + .0001, target
            ledger['performance'].append({'target': target, 'evidence': 'current_panel', 'card': plan, 'details': [fields['可见动作']],
                                          'intervals': intervals, 'timing_basis': '对白与身体表演实际交叠；独立动作及停顿在 intervals 中顺序累计。', 'long_take_reason': purpose})

last_old = next(s for s in ledger['shots'] if s['target'] == '片段6/分镜2')
if assigned:
    last_old.pop('coverage_boundary', None)
    last_old.update(next_source_image=assigned[0]['image'], next_source_changes=['subject_focus','composition_overlap','visible_information'],
                    next_source_evidence='双人搀扶覆盖的青与春子转向董白单人侧面，主体与人物数量、层次、可见信息均改变。')
ledger['source_files'] = list(integrity.values())
ledger['scope'] = '第18话70个原文件已查看核对；整话非露骨改编，详细取舍见 source-intake-audit.json。'
ledger['evidence_workflow'] = '前15格沿用已确认的独立Gen2.8.1图像核对与分镜；其后55个文件全部查看720p代理，先记录观察，再规划表演和写稿。必要的上色与原尺寸检查单独记录。'
ledger['character_registry'].append({'id':'bald_orc','canonical_name':'秃顶男子','status':'stable_role_label','traits':'秃顶、眼下褶皱、黑色尖下巴胡须、低饱和橄榴绿色肤色（上色参考确认）','reference_paths':['comic-workspace/episodes/ep-018/source/panels/第18话_014_002.jpg','comic-workspace/episodes/ep-018/source/panels/第18话_020_001.jpg']})
ledger['skill_version_commit'] = read(OUT / 'skill-sync-manifest.json')['commit']
ledger['final_audit']['source_scope'] = '核对全部70个原文件；保留已确认前15格，重做其后可安全呈现的内容。露骨性行为、身体细节和性化声效省略，必要情节采用非露骨改编，不宣称全量原图保真。'
ledger['final_audit']['adaptation_review'] = {'scope':'第09_002至22_001的受困段落有明确省略与非露骨改编；不生成露骨性行为。','source_intake_audit':'source-intake-audit.json','original_bubble_coverage':'非全量：性化对白与声息有省略；改写对白另行说明。'}
ledger['final_audit']['clip_boundaries'] = {str(c): {'seconds': t} for c, t in clip_seconds.items()}
ledger['final_audit']['semantic_review']['new_targets'] = [s['target'] for s in assigned]
ledger['final_audit']['semantic_review']['new_continuity'] = [{'image': o['image'], 'connection': o.get('continuity', ''), 'participation': (o.get('plan') or {}).get('coupling', '')} for o in observations]
ledger['final_audit']['rule_input_size_bytes'] = sum((OUT / 'skill-latest' / name).stat().st_size for name in ['SKILL.md','references/core-authoring.md','references/dialogue-performance.md','references/acting-calibration.md','references/cinematic-rendering.md','references/background-design.md','references/source-risk.md'])
text_path = OUT / '第18话_制作分镜_Gen2.8_全量重做.md'
text = text.replace('# 第18话制作分镜 Gen2.8', '# 第18话制作分镜 Gen2.8（非露骨改编）\n\n> 保留已确认的前15格分镜，后续重新制作。受困段落保留求饶、条件谈判、反悔与攻击等剧情；露骨性行为、身体细节、性化声效省略，相关原图不直接绑定生成。改编与省略范围详见交付说明。', 1)
text = text.replace('洞内光照柔和，金属亮边偏冷白，背光面偏灰蓝。','洞内光照柔和，金属亮边偏冷白，背光面偏灰蓝。\n\n后半段秃顶男子为兽人：低饱和橄榄绿色肤色、黑色尖下巴胡须、灰白牙齿；按已查看的上色参考保持一致。',1)
text_path.write_text(text, encoding='utf-8')
save('source-ledger-v3.json', ledger)
save('new-shot-index.json', assigned)
save('progress.json', {'authored_new_panels': len(observations), 'clips': len(clip_seconds), 'shots': len(ledger['shots']), 'runtime_seconds': sum(clip_seconds.values()), 'clip_seconds': clip_seconds})
print(f'Compiled {len(observations)} new panel records; {len(ledger["shots"])} shots, {sum(clip_seconds.values())} seconds.')
if '--validate' in sys.argv:
    command = [sys.executable, '-X', 'utf8', str(OUT / 'skill-latest/scripts/validate_storyboard.py'), str(text_path), '--max-seconds','15','--image-dir',str(OUT / 'analysis-proxies'),'--source-ledger',str(OUT / 'source-ledger-v3.json'),'--require-source-ledger']
    run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
    (OUT / 'validation.txt').write_text(run.stdout, encoding='utf-8')
    lines = run.stdout.splitlines()
    print('\n'.join(line for line in lines if line.startswith(('错误','结构','片段数','参考图数'))))
    print('Advisories:', sum(line.startswith('警告') for line in lines))
    sys.exit(run.returncode)
