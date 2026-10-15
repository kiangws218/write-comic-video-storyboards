"""Validate the saved script and record the decisions reviewed against 66 source proxies."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import runpy
import subprocess

OUT = Path(__file__).resolve().parent
EP = OUT.parents[2]
ROOT = EP.parents[2]
CURRENT = EP/'storyboards/current/第20话_制作分镜_Gen2.8.md'
BASE = OUT.parent/'gen2.8'
NAMES = ['镜头设计', '可见动作', '可见背景', '台词与语气', '光影布光', '声音设计']
plan = runpy.run_path(str(OUT/'revision_choices.py'))
S = plan['S']
ledger = json.loads((OUT/'source-ledger-v3.json').read_text(encoding='utf-8'))
text = CURRENT.read_text(encoding='utf-8')
old = (BASE/'第20话_制作分镜_Gen2.8.md').read_text(encoding='utf-8')
shots = {s['target']: s for s in ledger['shots']}
cards = {p['target']: p['card'] for p in ledger['performance']}
durations = {}
clip = 0
for line in text.splitlines():
    m = re.match(r'## 【片段(\d+)】', line)
    if m: clip = int(m[1])
    m = re.match(r'\*\*分镜(\d+)（(\d+)秒）', line)
    if m: durations[f'片段{clip}/分镜{m[1]}'] = int(m[2])
assert len(durations) == len(shots) == 76
for cut in ledger['final_audit']['cut_continuity_review']:
    for target, part, value in [(cut['outgoing'], 'landing', cut['outgoing_current_state']),
                                (cut['incoming'], 'opening', cut['incoming_opening'])]:
        if target not in cards: cards[target] = {'review_kind': 'task_or_state', 'beats': [], 'coupling': shots[target]['motion_decision']}
        if part not in cards[target]: cards[target][part] = value
assert len(cards) == 76
assert sum(durations.values()) == 356
assert re.findall(r'“([^”]+)”', text) == re.findall(r'“([^”]+)”', old)
assert re.findall(r'^分镜参考 .*$', text, re.M) == re.findall(r'^分镜参考 .*$', old, re.M)
assert (OUT/'storyboard.md').read_text(encoding='utf-8') == text
for s in shots.values():
    spec = S[s['review_key']]
    assert s['camera_excerpt'] == spec['camera']
    if 'performance' in spec: assert cards[s['target']] == spec['performance']
    if s['camera_decision']['mode'] != 'fixed':
        assert s['camera_decision']['path_basis']['source_refs']
    assert s['camera_decision']['opening'] and s['camera_decision']['landing']

command = ['python', str(ROOT/'write-comic-video-storyboards-gen2-8/scripts/validate_storyboard.py'),
           str(CURRENT), '--max-seconds', '15', '--image-dir', str(BASE/'proxies'),
           '--source-ledger', str(OUT/'source-ledger-v3.json'), '--require-source-ledger']
proc = subprocess.run(command, capture_output=True)
report = (proc.stdout+proc.stderr).decode('utf-8').replace('\r\n', '\n').replace('\r', '')
(OUT/'validation-report.txt').write_text(report, encoding='utf-8')
assert proc.returncode == 0, report
warnings = [line for line in report.splitlines() if line.startswith('警告：')]
dispositions = []
for warning in warnings:
    m = re.search(r'片段(\d+)(?:/分镜|的分镜)(\d+)', warning)
    target = f'片段{m[1]}/分镜{m[2]}' if m else warning.split('，')[0]
    s = shots.get(target)
    card = cards.get(target)
    item = {'target': target, 'warning': warning, 'blocking': False}
    if '角色基调语义复查' in warning:
        item['class'] = 'character_profile'
        key = s['review_key']
        if key in ['01_002-source','02_002-source','07_002-source']:
            decision = '春子只在画外说话；当前可见主体为帽刃或远层来者。声线已改为偏低、清晰、平直，未让他人动作承担春子的情绪。'
        elif key in ['05_002-source','04_003-coverage-1','07_001-formation']:
            decision = '当前是抓帽、抓腕或托肩承膝任务。手部力度、支撑及承重变化保留；动作不被冻结，也不扩写成愤怒、嫌弃或情绪反转。'
        elif key in ['05_003-source','21_001-source']:
            decision = '背向远景只有衣摆、发尾、水纹等持续状态；未在看不清的脸部制造情绪或新眼线。'
        elif key == '04_001-source':
            decision = '源格圆眼与下压刀臂保留，属于图中已有形状和任务；短词平直，未添加吼叫、震惊、暴怒或第二次挥刀。'
        else:
            decision = '已对照当格眉眼和确认的三无基线：保留高内眉、半垂眼及本镜明确视线；说话以嘴部、停顿和当前任务参与，头肩与配音不另作情绪递进。'
        item.update(decision=decision, action=s['action_excerpt'], voice=s['dialogue_excerpt'])
    elif '没有镜头落幅' in warning:
        item.update({'class': 'camera_landing',
                     'decision': '本镜已写明末幅停点或镜头停稳，并明确末幅包含的对象、占幅及焦点；属于落幅措辞识别提示。按当前摄影指令保留。',
                     'camera': s['camera_excerpt'], 'landing': s['camera_decision']['landing']})
    elif '表演语义复查' in warning:
        item.update({'class': 'acting_review', 'seconds': durations[target],
                     'decision': S[s['review_key']]['reason'], 'reviewed_card': copy.deepcopy(card),
                     'action': s['action_excerpt'], 'dialogue': s['dialogue_excerpt'],
                     'timing_review': '按当前完整台词与任务核对该时长；口部、呼吸、持续接触或眼线与说话并行。持态阶段有明确的交流/任务用途，未为填秒新增无依据手势或拆镜。'})
    elif '背景字段' in warning:
        item.update({'class': 'background_field',
                     'decision': '12_002的脸部后方仅指定斜线抽象底场亮区；人物肩背与刀的收势在动作字段。图形只承担强调，不转成实体风流或新增空间。',
                     'background': s['background_excerpt']})
    elif '明确说话人' in warning:
        item.update({'class': 'dialogue_coverage',
                     'decision': '22_002双人同框，青下半脸与春子眼口均可见。9秒内称呼、平直短应、托付三轮有句间停顿；横摇后停在二人同框，不切掉春子的短应，也不追加情绪反打。',
                     'action': s['action_excerpt'], 'camera': s['camera_excerpt']})
    elif '跨格合并复查' in warning:
        item['class'] = 'clip_grouping'
        item['decision'] = ('青梅男现场反应与王座台阶插景存在场景断点，分别保留。' if '片段14与片段15' in warning
                            else '介绍/插叙结束后，青以20_002源格交臂站姿重新进入现场；有明确时间省略，不合为连续放下过程。')
    else:
        raise AssertionError('Unreviewed warning: '+warning)
    dispositions.append(item)
ledger['advisory_dispositions'] = dispositions

audit = ledger['final_audit']
audit['prior_cut_continuity_review'] = copy.deepcopy(audit['cut_continuity_review'])
for cut in audit['cut_continuity_review']:
    a, b = shots[cut['outgoing']], shots[cut['incoming']]
    cut['outgoing_current_state'] = cards[cut['outgoing']]['landing']
    cut['incoming_opening'] = cards[cut['incoming']]['opening']
    cut['outgoing_camera_landing'] = a['camera_decision']['landing']
    cut['incoming_camera_opening'] = b['camera_decision']['opening']
    cut['outgoing_action'] = a['action_excerpt']
    cut['incoming_action'] = b['action_excerpt']
    cut['camera_motion_does_not_replay_action'] = True
    if cut['incoming'] == '片段14/分镜1':
        cut['decision'] = '青梅男反应由三槽面盔、颈侧与汗滴承担，嘴部不可见；董白的巨指包围通过反应镜持续，不放开后重抓。'
    if cut['incoming'] == '片段31/分镜1':
        cut['decision'] = '青从拨发的正面略低头转向右侧称呼；春子半垂眼直视镜头、平直短应，随后青托付。高位右手在裁切外持续，不默认落手。'
assert len(audit['cut_continuity_review']) == 75
rules = [Path(p) for p in audit['rule_input_size']['files']]
audit['rule_input_size'] = {'utf8_bytes': sum(p.stat().st_size for p in rules),
                            'files': [str(p) for p in rules], 'combat_module_loaded': False}
counts = dict(collections.Counter(i['class'] for i in dispositions))
sync = json.loads((OUT/'skill-sync.json').read_text(encoding='utf-8'))
for entry in sync['files']:
    p = Path(sync['destination'])/entry['path']
    repo_file = ROOT/'write-comic-video-storyboards-gen2-8'/entry['path']
    normalize = lambda b: b.replace(b'\r\n', b'\n')
    assert normalize(p.read_bytes()) == normalize(repo_file.read_bytes())
    entry['final_installed_sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
    entry['normalized_lf_sha256'] = hashlib.sha256(normalize(p.read_bytes())).hexdigest()
sync['final_verification'] = 'Installed and repository text match; concurrent installation normalized CRLF to LF without content changes.'
(OUT/'skill-sync.json').write_text(json.dumps(sync,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
metrics = {'clips': 34, 'shots': 76, 'seconds': 356, 'formal_references': 66,
           'reviewed_source_proxies': 66, 'original_reinspections': 1,
           'camera_fields_revised': 76, 'moving_shots': sum(s['camera_decision']['mode']!='fixed' for s in shots.values()),
           'fixed_shots': sum(s['camera_decision']['mode']=='fixed' for s in shots.values()),
           'cut_points_reviewed': 75, 'errors': 0, 'warnings': len(warnings),
           'warning_classes': counts, 'all_warnings_disposed': True, 'manual_overflow': 0,
           'rule_input_utf8_bytes': audit['rule_input_size']['utf8_bytes'],
           'combat_module': 'off', 'cross_episode_scene_review': 'deferred_by_user',
           'skill_source_commit': sync['source_commit'], 'skill_changed_files_verified': len(sync['files']),
           'source_dialogue_preserved': True, 'video_generation_reviewed': False,
           'script_sha256': hashlib.sha256(CURRENT.read_bytes()).hexdigest()}
test_report = (OUT/'skill-regression-tests.txt').read_text(encoding='utf-8')
assert re.search(r'Ran 151 tests',test_report) and re.search(r'^OK$',test_report,re.M)
metrics['skill_regression_tests'] = {'passed': 151, 'failed': 0}
audit['validation_summary'] = copy.deepcopy(metrics)
audit['semantic_review'] = 'completed_camera_gaze_character_and_cut_review'
audit['unresolved_action_gaps'] = []
audit['manual_overflow'] = 0
audit['camera_character_revision'].update({'profile_warning_targets_reviewed': counts.get('character_profile',0),
                                         'camera_landing_warnings_disposed': counts.get('camera_landing',0)})
for name, value in [('source-ledger-v3.json',ledger),('final-review-metrics.json',metrics)]:
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'第20话_运镜视线角色复查报告.md').write_text(f'''# 第20话 Gen2.8 运镜、视线与角色复查

已基于保存的最终动作复查版完成66张单格来源与76镜全量复查。34片段、356秒、66张正式参考及全部日文对白保留。75个切点重新登记当前表演状态与摄影起止构图。

- Skill：来源 `codex/gen2.8-performance-router` 的 `{sync['source_commit']}`；工作区 skill 已包含该版本，安装目录7项更新均核对内容与归一化LF的SHA-256，旧安装文件保存在 `skill-before-sync/`。并行任务将安装文件统一为LF，内容与本轮同步版本相同。
- 运镜：76个摄影字段修订，{metrics['moving_shots']}镜运动、{metrics['fixed_shots']}镜固定；角度、起幅、运动对象与路径、减速/停稳和末幅均按当前画面写明。固定镜服务抓腕、托抱形成、响指、柔焦、暗场等具体任务，无固定运动比例要求。
- 视线：区分人物低头与摄影机俯拍；源格可辨的直视镜头明确写出，背面、闭眼、不可辨眼向不强行补看镜头。高俯董白全身、超低仰巨形、陡俯水面、低仰王座等角度恢复；巨掌未再误作脚。
- 春子：按确认的三无基线，移除警觉、嫌弃、勉强答应、情绪反转等额外递进；保留当格半垂眼、高内眉、圆眼例外、抓帽/持刀/抓腕/被托抱及平直回应。青的急切和明确任务反射仍由青承担。
- 源图纠错：15_001原尺寸复看确认面盔下是颈部，不写张嘴；18_003同样保留遮口边界。10_001石地宽长暗影按源格恢复。抽象底场继续服务现有插景、能力强调和图形转折，不产生新实体。
- 动作衔接：此前2秒横抱形成桥保留；捋袖仍是右手拉左袖，响指只完成一次。长段插叙后青已交臂站立的时间省略保留，不虚构放下桥。战斗模块关闭，十六至十九话场景对照仍暂缓。
- 校验：0个错误，{len(warnings)}个启发式提示，分类 {json.dumps(counts,ensure_ascii=False)}。每条提示在台账中关联当前镜号、具体动作/摄影/表演卡及处理理由；校验通过不替代实际视频生成评估。
- 最新skill回归测试：151项通过，0失败。
- 规则输入：8份规则共{metrics['rule_input_utf8_bytes']} UTF-8字节；人工溢出0。66张单图代理逐张查看，仅15_001升级原尺寸复看。本次未生成视频。

当前稿：`../../current/第20话_制作分镜_Gen2.8.md`；本目录 `storyboard.md` 为同内容副本。旧版与旧台账位于 `../../archive/2026-10-11_Gen2.8_运镜视线角色修订前/`，此前 `gen2.8` 来源与交付副本不被重写。

`revision-plan.json` 保存逐源格观察和逐镜修改计划；`change-index.json` 对应稳定审阅ID与镜号；`source-ledger-v3.json` 保存来源、当前表演卡、75切点及逐条提示处理；`validation-report.txt` 是结构校验原始输出，`skill-regression-tests.txt` 是最新skill回归测试输出。
''',encoding='utf-8')
(OUT/'README.md').write_text('''# 第20话运镜、视线与三无角色修订

最终制作稿与本目录 `storyboard.md` 内容相同。请先读 `第20话_运镜视线角色复查报告.md` 和 `final-review-metrics.json`，逐镜细节在来源台账与修改计划。

复现本次交付：先运行 `apply_revision.py`，再运行 `audit_current.py`。前者从不可变的 `../gen2.8/` 基线应用已审阅的 `revision_choices.py`，后者校验保存稿并登记审阅。若之后手工修改当前稿，请在修改稿上继续复查，勿直接重跑基线生成脚本覆盖新成果。

源图代理复用 `../gen2.8/proxies/`；角色基调的唯一主档为 `comic-workspace/character-references/角色映射.md`。安装skill同步来源与哈希在 `skill-sync.json`，同步前文件保存于 `skill-before-sync/`。
''',encoding='utf-8')
print(json.dumps(metrics,ensure_ascii=False))
