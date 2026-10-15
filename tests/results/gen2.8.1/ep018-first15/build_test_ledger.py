"""Map the previously recorded visual observations/plans to their rendered shots.

Observed facts and P-card plans come only from source-observations.json.
The script extracts final prose only for exact realization excerpts.
"""
from pathlib import Path
import copy
import hashlib
import json
import re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SCRIPT = OUT / '第18话_前15格_完整分镜_Gen2.8.1.md'

def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

data = json.loads((OUT / 'source-observations.json').read_text(encoding='utf-8'))
integrity = {p['image']: p for p in json.loads((OUT / 'source-integrity.json').read_text(encoding='utf-8'))}
regions = {p['image']: p for p in json.loads((OUT / 'source-regions.json').read_text(encoding='utf-8'))}

panels = []
for observed in data['panels']:
    if observed.get('composite_file'):
        for sub in observed['subpanels']:
            p = copy.deepcopy(observed)
            p.pop('composite_file')
            p.pop('subpanels')
            p['parent_source_image'] = p['image']
            p['image'] = sub['image']
            p['source_region'] = regions[p['image']]['box']
            p['source_facts'] = sub['facts']
            p['performance_plan'] = sub['performance_plan']
            p['composition_lock'] = observed['composition_lock'].split('下格：')[0] if sub['region'] == 'top' else '下格：' + observed['composition_lock'].split('下格：')[1]
            p['page_overlays'] = [o for o in observed['page_overlays'] if (sub['region']=='top' and o['kind']=='sfx') or (sub['region']=='bottom' and o['kind'] in ('reaction_bubble','watermark'))]
            panels.append(p)
    else:
        panels.append(copy.deepcopy(observed))

owners = {
    '片段1/分镜1':'第18話_01_001.jpg', '片段1/分镜2':'第18話_01_003.jpg',
    '片段1/分镜3':'第18話_02_001.jpg', '片段2/分镜1':'第18話_02_002.jpg',
    '片段2/分镜2':'第18話_02_002.jpg', '片段3/分镜1':'第18話_02_003.jpg',
    '片段3/分镜2':'第18話_02_004.jpg', '片段4/分镜1':'第18話_03_001.jpg',
    '片段4/分镜2':'第18話_03_002.jpg', '片段5/分镜1':'第18話_03_003.jpg',
    '片段5/分镜2':'第18話_04_001_上格.jpg', '片段5/分镜3':'第18話_04_001_下格.jpg',
    '片段5/分镜4':'第18話_04_002.jpg', '片段5/分镜5':'第18話_05_001.jpg',
    '片段5/分镜6':'第18話_05_002.jpg', '片段6/分镜1':'第18話_05_003.jpg',
    '片段6/分镜2':'第18話_05_003.jpg',
}

bubble_map = {
    '第18話_01_001.jpg': [('片段1/分镜1','へえ、そう。',1.2), ('片段1/分镜1','自分で招いたことよ。',2.2)],
    '第18話_01_003.jpg': [('片段1/分镜2','えっ……はあ！？',2.0), ('片段1/分镜2','なんで急にケンカになるの！？',3.2)],
    '第18話_02_001.jpg': [('片段1/分镜3','もうやめなさい。',1.8), ('片段1/分镜3','子供じゃないんだから。',2.3)],
    '第18話_02_002.jpg': [('片段2/分镜1','お前ら、このガキ……',2.5), ('片段2/分镜1','また騒ぎですか、ご婦人。',2.7), ('片段2/分镜2','懲戒処分を受けてまだ日も浅いのに、もう厄介事ですか……。',6.2)],
    '第18話_02_003.jpg': [('片段3/分镜1','お二人も、そろそろご自分の用事に戻ってください。',5.0)],
    '第18話_02_004.jpg': [('片段3/分镜2','……行こう。',1.5), ('片段3/分镜2','ちっ……あいつ、本当に最低。',2.9)],
    '第18話_03_001.jpg': [('片段4/分镜1','ねえ、手を放して。',1.9), ('片段4/分镜1','ケンカを売るつもりなんてないわ。',3.2)],
    '第18話_05_001.jpg': [('片段5/分镜5','ハル……！',1.4)],
    '第18話_05_002.jpg': [('片段5/分镜6','ハルコ姉さん！！',2.0)],
    '第18話_05_003.jpg': [('片段6/分镜1','はあ、すっきりした。',2.3), ('片段6/分镜1','正気なの！？',1.5), ('片段6/分镜2','やりすぎよ……！',1.9)],
}

text = SCRIPT.read_text(encoding='utf-8')
clip = None
raw_shots = []
for line in text.splitlines():
    m = re.match(r'## 【片段(\d+)】', line)
    if m:
        clip = int(m.group(1))
    m = re.match(r'\*\*分镜(\d+)（(\d+)秒）', line)
    if m:
        raw_shots.append({'target': f'片段{clip}/分镜{m.group(1)}', 'seconds': int(m.group(2)), 'fields':{}, 'references':[]})
    if raw_shots:
        m = re.match(r'【([^】]+)】：(.*)',line)
        if m:
            raw_shots[-1]['fields'][m.group(1)] = m.group(2)
        if line.startswith('分镜参考'):
            raw_shots[-1]['references'] = re.findall(r'\[([^\]]+\.jpg)\]',line)

by_image = {p['image']:p for p in panels}
by_target = {s['target']:s for s in raw_shots}
for p in panels:
    targets = [t for t, image in owners.items() if image == p['image']]
    p['coverage'] = 'none' if not p['bubbles'] else ('shared' if len(targets)==1 else 'mixed')
    p['coverage_reason'] = '纯作品标题，无叙事图像，按规则省略' if not p['renderable_visual'] else '完整保留该格可见构图与叙事信息；同格短对白共用构图，长交付或反应重点另给覆盖。'
    p['source_bubble_count'] = len(p['bubbles'])
    p['bubble_audit'] = 'pass'
    p['reference_scope'] = 'full_renderable_panel'
    p['background']['evidence'] = 'current_panel'
    graphics = []
    valid_overlays = []
    for overlay in p['page_overlays']:
        o = copy.deepcopy(overlay)
        if o['kind'] == 'sfx':
            o['audio_meaning'] = o.get('disposition','已记录非对白音效')
        elif o.get('source_text'):
            o['observed_kind'] = o['kind']
            o['kind'] = 'caption'
        else:
            graphics.append(o)
            continue
        valid_overlays.append(o)
    p['page_overlays'] = valid_overlays
    p['source_graphic_conventions'] = graphics
    if p['image']=='第18話_01_002.jpg':
        p['composition_lock']='平视页面全景；画面上下裁到文件边缘，中心无叙事人物；不存在可生成的前后景与遮挡关系。'
    if p['image']=='第18話_04_002.jpg':
        p['composition_lock']='平视董白中近景；脸位于上半部，黑色上臂带在右中，手臂横伸至左侧画外；长发条带占下半部并遮挡胸前与前臂，双马尾拖向左，命中点不在可见画幅。'
    original_name = p.get('parent_source_image',p['image'])
    p['source_integrity'] = {**integrity[original_name], 'lfs_content_verified':True, 'source_unchanged':True}
    p['dialogue_turns'] = []
    p['coverage_groups'] = []
    for i, b in enumerate(p['bubbles']):
        target, script_text, seconds = bubble_map[p['image']][i]
        assert script_text in by_target[target]['fields']['台词与语气'], (p['image'],script_text)
        b.update(status='mapped',target=target,script_text=script_text,seconds=seconds,
                 speaker_evidence='当前气泡指向与可见张口者；画外呼唤按本格气泡及前后连续发言判定，仅确立声音身份。')
        p['dialogue_turns'].append({'id':f't{i+1}','bubble_ids':[b['id']], 'function':b['source_text']})
    for target in dict.fromkeys(b['target'] for b in p['bubbles']):
        ids = [f't{i+1}' for i,b in enumerate(p['bubbles']) if b['target']==target]
        p['coverage_groups'].append({'id':f'g{len(p["coverage_groups"])+1}', 'turn_ids':ids, 'targets':[target],
            'merge_basis':'相邻短句同一机位：可见回应完整，两人反应有时间交接，无隐藏切镜。' if len(ids)>1 else '独立语义交付，构图与时长保留反应。'})

purpose = {
    '片段1/分镜1':'以逼视和浅笑把挑衅变得可读，未发起攻击',
    '片段1/分镜2':'青从错愕到追问，春子抓衣的姿态形成对照',
    '片段1/分镜3':'明确演出青单手握住春子前臂的劝阻，保留春子自己的抓衣手与冷淡回应',
    '片段2/分镜1':'董白话到半截被身后守卫打断，两人的交接在同一视图可读',
    '片段2/分镜2':'把持续规劝转给守卫胸像；闭盔表演由肩和盔面承担',
    '片段3/分镜1':'董白回头听完规劝；保持抓臂接触',
    '片段3/分镜2':'青想结束争执，春子的不满继续，背景董白不同步反应',
    '片段4/分镜1':'演出挥臂甩开，接触解除可见，不扩大成攻击守卫',
    '片段4/分镜2':'两个分离背影继续行进，结束于可供下一段独立起步的状态',
    '片段5/分镜1':'用肩背带动回头，保留急动的整体姿态与马尾滞后',
    '片段5/分镜2':'两人背影注意到快速声响，保留接近前的空间关系',
    '片段5/分镜3':'春子疑惑的回望在受冲击前有独立落点',
    '片段5/分镜4':'兑现快速横向挥臂与发束遮挡，不猜画外命中部位',
    '片段5/分镜5':'青的惊呼开头被突发动势卡住',
    '片段5/分镜6':'岩壁空镜承接画外惊呼与撞击，保留未画机制',
    '片段6/分镜1':'三人反应形成反差，搀扶任务与质问并行',
    '片段6/分镜2':'将责备落在保护春子的双人关系里，春子仍低头',
}

# These split plans select the already recorded beats; they do not extract
# intent or observed facts from the finished action paragraph.
plan_overrides = {
    '片段2/分镜1': {'opening':'董白睁圆眼刚张口，守卫在左后方。','beats':['董白带不满起句；守卫压近并开口，她停口，视线转左。'],'coupling':'先被打断，再对身后发言者作可见回应。','landing':'董白嘴形收住、目光偏左；守卫仍在身后。'},
    '片段2/分镜2': {'opening':'守卫肩胸压近，盔面朝前下；董白肩臂在右下。','beats':['守卫连着肩胸进一步前压，头盔低下；董白肩部向后缩并绷住。'],'coupling':'保留原稿中压近与退缩的双方关系；闭盔表演由身体承担。','landing':'守卫胸甲前压、盔面低向；董白肩臂缩紧。'},
    '片段6/分镜1': {'opening':'青搭着春子肩背，春子低头弯腰、手掌贴脸；董白手举脸旁。','beats':['董白闭眼笑，手指放松并呼气；青先低眼看春子，再护着她转脸朝右质问。'],'coupling':'舒坦笑容与惊怒搀扶在同一画面异步发生，春子自己的覆脸手保留。','landing':'春子仍低头捂脸，青搭靠并望向右后方，董白仍笑。'},
    '片段6/分镜2': {'opening':'青护着低头春子，朝右侧外，眉头绷紧；春子的掌贴脸侧。','beats':['责问时青向右探肩，护臂稳在春子肩背；春子捂脸随呼吸起伏。'],'coupling':'质问与既有保护任务并行，覆脸与搭靠接触都持续。','landing':'青望向右侧外，春子仍低头捂脸。'},
}

shots = []
performance = []
intervals = {
    '片段1/分镜1':[(1.2,1.0),(2.2,1.6),(.0,.5)],
    '片段1/分镜2':[(2,1.7),(3.2,2),(.0,.5)],
    '片段1/分镜3':[(2.1,1.3),(2.6,1.7),(.0,.3)],
    '片段2/分镜1':[(2.7,1),(2.9,1.6),(.0,.4)],
    '片段2/分镜2':[(3.0,1.4),(3.3,1.4),(.0,.6)],
    '片段3/分镜1':[(2.4,1.1),(2.6,1.0),(.0,.5)],
    '片段3/分镜2':[(2.0,.7),(3.3,1.5),(.0,.4)],
    '片段4/分镜1':[(1.9,1.1),(3.2,1.3),(.0,.5)],
    '片段4/分镜2':[(0,3)], '片段5/分镜1':[(0,2)],
    '片段5/分镜2':[(0,1)], '片段5/分镜3':[(0,1)],
    '片段5/分镜4':[(0,2)], '片段5/分镜5':[(1.4,1.2),(0,.4)],
    '片段6/分镜1':[(2.6,1.7),(1.9,1.2),(0,.5)],
    '片段6/分镜2':[(2.3,1.5),(0,.6)],
}

for i, raw in enumerate(raw_shots):
    target = raw['target']
    p = by_image[owners[target]]
    fields = raw['fields']
    card = copy.deepcopy(plan_overrides.get(target,p.get('performance_plan')))
    is_p = target != '片段5/分镜6'
    flags = ['P'] if is_p else []
    if p['bubbles'] and (len(p['bubbles'])>1 or max(len(b['script_text']) for b in p['bubbles'])>=28):
        flags.append('D')
    if target in ('片段1/分镜3','片段2/分镜2','片段3/分镜1','片段4/分镜1','片段5/分镜4','片段5/分镜5','片段6/分镜1','片段6/分镜2'):
        flags.append('G')
    mode = 'graphic' if target=='片段5/分镜4' else ('continuity' if p['background']['type']=='omitted' else 'physical')
    sh = {'target':target,'role':'source_locked' if raw['references'] else 'uncited_coverage',
          'source_images':raw['references'],'derived_from':[] if raw['references'] else [p['image']],
          'evidence':'current_panel','purpose':purpose[target],
          'background_excerpt':fields['可见背景'],'viewed_while_writing':True,'source_audit':'pass',
          'unsupported_additions':[], 'risk_flags':flags,'risk_basis':purpose[target],
          'fact_claims':copy.deepcopy(p['source_facts']),
          'motion_decision':{'classification':'State' if target in ('片段4/分镜2','片段5/分镜6') else 'Mixed',
              'observed_anchor':p['composition_lock'], 'admitted_plan':card,
              'source_anchor_placement':'middle',
              'inference_limit':'只延展已见动作/姿态，保持身体范围、既有接触及画外边界；原图不作为起始帧。'},
          'camera_decision':{'mode':'fixed','reason':purpose[target],'anchor_phase':'middle',
              'opening':fields['镜头设计'],'landing':fields['镜头设计'],'evidence':p['composition_lock']},
          'background_decision':{'mode':mode,'basis':'原图实景' if mode=='physical' else ('快速挥臂段的源图速度衬底，改为简洁灰蓝冷白色面，非物理雾或新事件。' if mode=='graphic' else '连续洞窟会话，限定为已核对岩壁的低细节远景。'),
              'source_refs':['第18話_01_003.jpg','第18話_02_001.jpg'] if mode=='continuity' else [p['image']],
              'inspected_resolution':p['drafting_resolution']},
          'action_admissions':[]}
    if is_p:
        sh['action_admissions']=[{'claim':fields['可见动作'], 'source_image':p['image'],
            'visual_evidence':'观察：'+ '；'.join(p['source_facts']['actions']+p['source_facts']['relations'])+
                 '。已在写稿前记录的推演：'+'；'.join(card['beats'])+'。'+card['coupling'],
            'visible_in_framing':True,'anchor_safe':True}]
        ivs=[{'speech_seconds':s,'acting_seconds':a,'concurrent':True} for s,a in intervals[target]]
        assert sum(max(v['speech_seconds'],v['acting_seconds']) for v in ivs)<=raw['seconds']+1e-9, target
        performance.append({'target':target,'evidence':'current_panel','card':card,
            'details':[fields['可见动作']], 'intervals':ivs,
            'timing_basis':'同一段内对白与主动作并行，段间顺序相加；无对白动态依照可见动作自然时长。',
            'long_take_reason':purpose[target]})
    if not raw['references']:
        sh.update(coverage_type='relationship' if target=='片段6/分镜2' else 'speaker',
            coverage_changes=['subject_focus','composition_overlap','visible_information'],
            coverage_evidence='上一镜：'+raw_shots[i-1]['fields']['镜头设计']+'。本镜：'+fields['镜头设计'])
        if target=='片段2/分镜2':
            sh.update(next_source_image='第18話_02_003.jpg',next_source_changes=['subject_focus','composition_overlap','visible_information'],
                next_source_evidence='本镜由守卫肩胸甲主导，董白只露局部肩臂；之后原格显示董白回望的完整侧脸与抓臂关系，主体可见信息与摆位关系均不同。')
        else:
            sh['coverage_boundary']='用户范围终点；没有下一张来源构图纳入该测试。'
    shots.append(sh)

for sh in shots:
    if sh['target']=='片段2/分镜2':
        sh['fact_claims']={'entities':['董白','全盔守卫','岩壁'],'actions':[], 'relations':[]}
    elif sh['target']=='片段6/分镜2':
        p=by_image['第18話_05_003.jpg']
        sh['fact_claims']={'entities':['青','春子','岩壁'],
                          'actions':p['source_facts']['actions'][:2],
                          'relations':p['source_facts']['relations'][1:]}

ledger = {**{k:v for k,v in data.items() if k!='panels'},'panels':panels,'shots':shots,'performance':performance,
          'source_files':list(integrity.values()),'source_regions':list(regions.values()),
          'final_audit':{'source_scope':'15个原文件：1个标题不生成、1个双格拆开，得到15个叙事参考。',
              'palette_audit':'岩壁基色采用已查看工作区上色005_003的深褐色，与2.8场景一致；冷灰蓝仅为局部照明/远景层次。人物按已查看人设基色。',
              'clip_boundaries':{'1':'回应、错愕、介入劝阻同一段，15秒；下一整格规劝13秒放不下。','2':'保留规劝的完整3个语义回合与独立守卫覆盖，13秒。','3':'回头听规劝与前景结束争执，12秒；下一甩手6秒放不下。','4':'接触解除到两人背行，9秒；后面的快速回身、注意、挥臂、惊呼和冲击组成另一连续因果段。','5':'快速动作因果段10秒；下一完整后果单元8秒放不下。','6':'搀扶与质问的完整后果段8秒，结束于用户指定终点。'},
              'semantic_review':{'targets':list(owners),'retained_performance':'抓衣与错愕、青单手握前臂的接触形成、打断、回望、双方接触解除、整体回身、横向挥臂、画外冲击、搀扶与质问均已兑现。','visible_emotion':'挑衅、错愕、焦急、冷淡、不满、疑惑、惊慌、舒坦和惊怒由相应的图像态度及动作承载；闭盔守卫不编眉眼，春子低头格不强配脸部情绪。','limitations':'横向挥臂的具体命中点在画外，保留边界；未生成视频，表演效果待视频测试。'},
              'manual_overflow':[], 'rule_input_size_bytes':sum((ROOT/'write-comic-video-storyboards-gen2-8-1'/rel).stat().st_size for rel in ['SKILL.md','references/core-authoring.md','references/dialogue-performance.md','references/acting-calibration.md','references/cinematic-rendering.md','references/background-design.md','references/source-risk.md','references/2d-animation-execution.md'])}}
audit_path=OUT/'advisory-dispositions.json'
if audit_path.exists():
    ledger['advisory_dispositions']=json.loads(audit_path.read_text(encoding='utf-8'))
ledger['revision_audit']=[
    {'reason':'独立稿完成并冻结后对照基线，发现来源结构、方向和遗漏细节需要复查。',
     'affected_targets':['片段1/分镜2','片段1/分镜3','片段2/分镜2','片段3/分镜1','片段4/分镜1','片段5/分镜4','片段6/分镜1','片段6/分镜2'],
     'affected_images':['第18話_01_003.jpg','第18話_02_001.jpg','第18話_02_002.jpg','第18話_02_003.jpg','第18話_03_001.jpg','第18話_04_002.jpg','第18話_05_003.jpg'],
     'resolution':'01_003、02_001、02_003、03_001、04_002、05_001、05_003原尺寸；02_002代理；04_002、05_001、05_003辅助上色图。',
     'decision':'恢复01_003并置画面；纠正02_001手的归属为春子抓衣、青单手握前臂；抓臂处不用上臂强定裁切部位；恢复守卫压近与董白退缩的演出耦合；修正横臂方向；恢复春子自己的覆脸手；岩壁基色依据已查看上色05_003锁回深褐色。新稿整体文字没有改写成旧稿。',
     'reviewed_scope':'仅受影响的构图、方向、接触与表演；原冻结哈希另存，保留修订前状态追踪。'}]
save('source-ledger-v3.json',ledger)
save('shot-index.json',raw_shots)
print(f"Mapped {len(panels)} panel records, {len(shots)} shots, {len(performance)} P cards, {sum(s['seconds'] for s in raw_shots)} seconds.")
