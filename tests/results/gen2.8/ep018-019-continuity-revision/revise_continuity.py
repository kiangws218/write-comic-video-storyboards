from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,re,hashlib,shutil,sys,subprocess,zipfile
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
sys.path.insert(0,str(REPO/'tests/results/gen2.8/ep018-019-brow-revision'))
from prepare_review import parse,FIELDS
from finish_delivery import category,target as warning_target
from decisions import CHANGES,BRIDGE,VIEWED,SEQUENCES
PRIOR='2026-10-11_Gen2.8_角色身份修订'
DELIVERY='2026-10-11_Gen2.8_动作衔接修订'
SKILL=Path(r'C:\Users\86135\.codex\skills\write-comic-video-storyboards-gen2-8')

def jwrite(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def target_map(t,ep):
    return {'片段28/分镜4':'片段28/分镜5','片段28/分镜5':'片段28/分镜6'}.get(t,t) if ep==19 else t
def map_targets(v,ep):
    if isinstance(v,str):return re.sub(r'片段28/分镜[45]',lambda m:target_map(m[0],ep),v)
    if isinstance(v,list):return [map_targets(i,ep) for i in v]
    if isinstance(v,dict):return {k:map_targets(i,ep) for k,i in v.items()}
    return v
def card(c):return {k:deepcopy(c[k]) for k in ('opening','beats','coupling','landing')}
def observed_prop(v,pairs):
    if isinstance(v,str):
        for a,b in pairs.items():v=v.replace(a,b)
        return v
    if isinstance(v,list):return [observed_prop(x,pairs) for x in v]
    if isinstance(v,dict):return {k:(x if k in ('source_text','script_text','jp','source_integrity') else observed_prop(x,pairs)) for k,x in v.items()}
    return v

def render(before,ep):
    clip=0;target=None;out=[]
    for line in before.splitlines():
        m=re.match(r'## 【片段(\d+)】',line)
        if m:clip=int(m[1])
        m=re.match(r'\*\*分镜(\d+)（(\d+)秒）',line)
        if m:
            target=f'片段{clip}/分镜{m[1]}'
            if ep==19 and target=='片段28/分镜4':
                out.extend(['**分镜4（2秒）：**',*['【'+f+'】：'+BRIDGE['fields'][f] for f in FIELDS],''])
            mapped=target_map(target,ep);newnum=mapped.split('分镜')[1]
            seconds=CHANGES[ep].get(target,{}).get('seconds',int(m[2]))
            line=f'**分镜{newnum}（{seconds}秒）：**'
        changes=CHANGES[ep].get(target,{})
        for key,field in [('action','可见动作'),('camera','镜头设计'),('sound','声音设计'),('background','可见背景')]:
            if line.startswith('【'+field+'】') and key in changes:line='【'+field+'】：'+changes[key]
        out.append(line)
    return '\n'.join(out)+'\n'

def create():
    summaries=[]
    for ep in (18,19):
        root=REPO/f'comic-workspace/episodes/ep-{ep:03}'
        prior=root/'storyboards/deliveries'/PRIOR;dest=root/'storyboards/deliveries'/DELIVERY;dest.mkdir(parents=True,exist_ok=True)
        current=root/f'storyboards/current/第{ep}话_制作分镜_Gen2.8.md'
        before=(prior/current.name).read_text(encoding='utf-8');after=render(before,ep)
        old=parse(before);new=parse(after);new_by={s['target']:s for s in new}
        # All speech and formal references retain sequence despite the one silent bridge.
        assert [s['fields']['台词与语气'] for s in old if s['fields']['台词与语气']!='无台词。']==[s['fields']['台词与语气'] for s in new if s['fields']['台词与语气']!='无台词。']
        assert [r for s in old for r in s['refs']]==[r for s in new for r in s['refs']]
        ledger=json.loads((prior/'source-ledger-v3.json').read_text(encoding='utf-8'))
        previous_audit=deepcopy(ledger['final_audit'])
        previous_advisories=deepcopy(ledger.get('advisory_dispositions',[]))
        for key in ('panels','shots','performance','final_audit','advisory_dispositions'):
            if key in ledger:ledger[key]=map_targets(ledger[key],ep)
        rows={s['target']:s for s in ledger['shots']};performance={s['target']:s for s in ledger['performance']}
        changed=[]
        for target,c in CHANGES[ep].items():
            mapped=target_map(target,ep);s=rows[mapped];newshot=new_by[mapped]
            oldshot=next(x for x in old if x['target']==target)
            s['motion_decision']['admitted_plan']=card(c)
            s['purpose']=c['coupling']
            s['motion_decision']['continuity']=c['evidence']
            s['motion_decision']['inference_limit']=c['evidence']
            s['camera_decision']['opening']=newshot['fields']['镜头设计'];s['camera_decision']['landing']=newshot['fields']['镜头设计']
            s['background_excerpt']=newshot['fields']['可见背景']
            if 'background' in c:
                s['background_decision']['mode']='occluded' if '完全被' in c['background'] else 'continuity'
                s['background_decision']['basis']='动作取景同步检查：紧裁双手/袋身/衣袖遮满独立背衬，或仅保留10_003已见石地。'
            s['action_admissions']=[{'claim':c['action'],'source_image':(s['source_images'] or s['derived_from'])[0],
                'visual_evidence':'本轮对照已复查原格及相邻状态：'+c['evidence'], 'visible_in_framing':True,'anchor_safe':True}]
            s['continuity_revision_review']={'status':'reviewed','opening':c['opening'],'landing':c['landing'],
                'connection':c['evidence'],'timing':'与既有说话并行；静默回鞘独立延长至4秒。' if c.get('seconds') else '主动作与台词/对方回应并行，不削弱原表演。'}
            if 'brow_revision_review' in s:
                s['brow_revision_review']['planned_state']=card(c)
                s['brow_revision_review']['continuity_note']+=' 本轮补动作相位，已批准的眉形和遮挡不重置。'
            p=performance.get(mapped)
            if p:
                p['card']=card(c);p['details']=[c['action']];p['long_take_reason']=c['coupling']
                if c.get('seconds'):p['intervals']=[{'speech_seconds':0,'acting_seconds':3.6,'concurrent':True}]
                elif target=='片段7/分镜1' and ep==18:p['intervals']=[{'speech_seconds':0,'acting_seconds':2.7,'concurrent':True}]
            changed.append({'previous_target':target,'target':mapped,'seconds_before':oldshot['seconds'],'seconds_after':newshot['seconds'],
                'before':oldshot['fields'],'after':newshot['fields'],'plan':card(c),'admission':c['evidence']})
            if s['source_images']:
                panel=next(p for p in ledger['panels'] if p['image']==s['source_images'][0])
                panel['performance_plan']=card(c)
                panel['continuity']=c['evidence'];panel['admission']=c['evidence']
                panel['continuity_revision_note']={'planned_transition':c['evidence'],'static_facts_unchanged':True}
        if ep==19:
            # Reobserved prop atoms: pale bag opening in 08_003; actual ice cubes in 09_001.
            prop_targets={'片段8/分镜2','片段9/分镜1','片段9/分镜2','片段13/分镜1','片段13/分镜2'}
            for target in prop_targets:
                s=rows[target];s.update(observed_prop(s,{'浅色布':'冰袋','浅布':'冰袋','握布':'持冰袋','捏布':'握冰袋','抓布':'握冰袋'}))
            for image in ('第19話_08_003.jpg','第19話_09_001.jpg','第19話_10_003.jpg'):
                panel=next(p for p in ledger['panels'] if p['image']==image)
                panel.update(observed_prop(panel,{'浅色布':'浅色袋装物' if '08_003' in image else '冰袋',
                    '浅布':'浅色袋装物' if '08_003' in image else '冰袋','握布':'持袋','捏布':'握袋','抓布':'握袋'}))
                if '09_001' in image:
                    panel['source_facts']['entities'].append('袋内可见冰块')
                    panel['source_facts']['relations'].append('青持袋在两人之间，袋子与春子脸侧未见确定贴合')
                panel['continuity_revision_note']['static_facts_unchanged']=False
                panel['continuity_revision_note']['observed_prop_correction']='重新看原格：袋口/袋装物或可见袋内冰块，非空布团；发生运动写入计划而非源事实。'
            # Single-panel close-up must not pretend two hands are visible in 10_003.
            s=rows['片段13/分镜2'];panel=next(p for p in ledger['panels'] if p['image']=='第19話_10_003.jpg')
            s['fact_claims']=deepcopy(panel['source_facts'])
            for box in (s['fact_claims'],panel['source_facts']):
                for key in ('entities','actions','relations'):
                    box[key]=[text.replace('双手','近手').replace('两手','近手') for text in box[key]]
            for target in prop_targets:
                s=rows[target];source=(s['source_images'] or s['derived_from'])[0]
                panel=next(p for p in ledger['panels'] if p['image']==source)
                s['fact_claims']=deepcopy(panel['source_facts'])
            # The bridge draws on adjacent renderable endpoints; 22_003 has text only.
            endpoints=['第19話_22_002.jpg','第19話_22_004.jpg'];panels=[next(p for p in ledger['panels'] if p['image']==i) for i in endpoints]
            facts={k:list(dict.fromkeys(atom for p in panels for atom in p['source_facts'][k])) for k in ('entities','actions','relations')}
            bridge={'target':BRIDGE['target'],'role':'uncited_coverage','source_images':[],'derived_from':[endpoints[1]],
                'evidence':'current_panel','evidence_images':endpoints,'purpose':'补下落到压制的必要身体状态变化，保留刀尖急停和骑压源锚。',
                'background_excerpt':BRIDGE['fields']['可见背景'],'viewed_while_writing':True,'source_audit':'pass','unsupported_additions':[],
                'risk_flags':['P','G'],'risk_basis':'跨格下落及腿部落位；刀尖与兜帽关系必须延续。', 'fact_claims':facts,
                'motion_decision':{'classification':'Action','observed_anchor':'22_002刀尖与帽缘近处；22_004春子屈腿压住黑袍身体。',
                    'admitted_plan':card(BRIDGE),'source_anchor_placement':'result','continuity':BRIDGE['evidence'],'inference_limit':BRIDGE['evidence']},
                'camera_decision':{'mode':'fixed','reason':'比刀尖局部和稳定背面压制分别扩大到身体关系与动态下降。',
                    'anchor_phase':'result','opening':BRIDGE['fields']['镜头设计'],'landing':BRIDGE['fields']['镜头设计'],'evidence':BRIDGE['evidence']},
                'background_decision':{'mode':'continuity','basis':'只使用22_004已见水面，不增加空间。','source_refs':[endpoints[1]],'inspected_resolution':'720p'},
                'action_admissions':[{'claim':BRIDGE['fields']['可见动作'],'source_image':endpoints[1],
                    'visual_evidence':BRIDGE['evidence'],'visible_in_framing':True,'anchor_safe':True}],
                'coverage_type':'action_phase','coverage_changes':['viewpoint_axis','scale','visible_information'],
                'coverage_evidence':'前镜只见刀尖和帽缘；本桥侧面低机位全景见两人下降、腿部收落与水面；后镜背面侧向中景看压制和竖向握刀。主体范围、轴向、摆位与运动信息不同。',
                'next_source_image':endpoints[1],'next_source_changes':['viewpoint_axis','scale','visible_information'],
                'next_source_evidence':'侧面全景动态关系转为背面侧向中景稳定压制，主体范围、轴向、摆位与可见信息不同。','source_fidelity_mode':'source_grounded_bridge'}
            pos=next(i for i,s in enumerate(ledger['shots']) if s['target']=='片段28/分镜5');ledger['shots'].insert(pos,bridge)
            p={'target':BRIDGE['target'],'evidence':'current_panel','card':card(BRIDGE),'details':[BRIDGE['fields']['可见动作']],
                'intervals':[{'speech_seconds':0,'acting_seconds':1.8,'concurrent':True}],'timing_basis':'无对白；共同下降与腿部收落并行，末尾0.2秒落稳。','long_take_reason':BRIDGE['coupling']}
            pos=next(i for i,p in enumerate(ledger['performance']) if p['target']=='片段28/分镜5');ledger['performance'].insert(pos,p)
            changed.append({'previous_target':None,'target':BRIDGE['target'],'seconds_before':0,'seconds_after':2,'before':None,'after':BRIDGE['fields'],'plan':card(BRIDGE),'admission':BRIDGE['evidence']})
            # Original source result is now reached by the bridge, so its next opening is an actual match.
            rows['片段28/分镜5']['motion_decision']['continuity']='由新增片段28/分镜4共同下落、落腿形成压制；本镜只保持该压制和刀尖间隙，不重复落地。'
        for s in ledger['shots']:
            if s.get('next_source_image'):
                nextpanel=next(p for p in ledger['panels'] if p['image']==s['next_source_image'])
                if s['target'] in {target_map(t,ep) for t in CHANGES[ep]}:
                    s['next_source_evidence']='本轮状态终点：'+s['motion_decision']['admitted_plan']['landing']+'；下一源格构图：'+nextpanel['composition_lock']
        audit={'date':'2026-10-11','scope':'逐镜扫描两话全部镜头及相邻边界；仅重开影响动作/接触/道具判断的图片，未改批准的身份和眉形设计。',
            'previous_semantic_audit':previous_audit,'previous_advisory_dispositions':previous_advisories,'affected_targets':[c['target'] for c in changed],
            'image_inspection':[{'image':f'第{ep}話_{p}.jpg','resolution':'720p缓存代理'} for p in VIEWED[ep]],
            'original_escalation': [{'image':f'第19話_{p}.jpg','reason':'卷身/压制或握袋的细小接触与手数改变动作决策'} for p in ('21_002','22_004','10_003')] if ep==19 else [],
            'sequence_review':[{'clips':[a,b],'conclusion':text} for a,b,text in SEQUENCES[ep]],
            'changes':[{k:v for k,v in c.items() if k not in ('before','after')} for c in changed],
            'shot_target_map':{'片段28/分镜4':'片段28/分镜5','片段28/分镜5':'片段28/分镜6'} if ep==19 else {},
            'limits':['没有生成视频；逐镜语义复查不等于视频执行验证。','18话非露骨改编与事件省略、19话诊所治疗及转场的省略保留；不编画外命中、未给出路线、冰袋存放或治疗新操作。']}
        # Every actual boundary retains concrete rendered states plus the manual sequence conclusion.
        rows={s['target']:s for s in ledger['shots']}
        boundaries=[]
        for a,b in zip(new,new[1:]):
            clipa=int(re.search(r'片段(\d+)',a['target'])[1]);clipb=int(re.search(r'片段(\d+)',b['target'])[1])
            seq=next(text for lo,hi,text in SEQUENCES[ep] if lo<=clipb<=hi)
            endpoints=[]
            for s,phase in ((a,'landing'),(b,'opening')):
                row=rows[s['target']];plan=row['motion_decision'].get('admitted_plan') or {}
                endpoints.append(plan.get(phase,s['fields']['可见动作']))
            boundaries.append({'outgoing':a['target'],'incoming':b['target'],'clip_boundary':clipa!=clipb,
                'outgoing_state':endpoints[0],'incoming_state':endpoints[1],
                'rendered_outgoing_action':a['fields']['可见动作'],'rendered_incoming_action':b['fields']['可见动作'],
                'manual_sequence_conclusion':seq,'status':'reviewed'})
        audit['boundaries']=boundaries
        ledger.setdefault('revision_audit',[]).append(audit)
        clip_seconds=Counter()
        for s in new:clip_seconds[re.search(r'片段(\d+)',s['target'])[1]]+=s['seconds']
        ledger['final_audit']['clip_boundaries']={k:{'seconds':v} for k,v in clip_seconds.items()}
        if ep==19:
            ledger['final_audit']['limitations']='未生成视频。只补已供状态之间的下落落腿压制和同一刀/鞘的轴向回鞘；不增加额外踢击、甩投、反击、完整行进路线、体型转变或全身再生机制。裸露局部仍为非露骨取景。'
        elif 'bald_orc_palette_audit' in ledger['final_audit']:
            ledger['final_audit']['bald_orc_palette_audit']['scope']='此前上色观察保留；当前欧迈及身份采用共享角色映射版本2和前轮identity-review，不再用旧代称作为当前姓名。'
        sem=ledger['final_audit']['semantic_review'];sem['continuity_revision']={'review_file':'continuity-review.json','targets':audit['affected_targets'],
            'boundary_count':len(boundaries),'status':'reviewed','limitation':'保留明确转场/非露骨省略，具体列于sequence_review；未生成视频。'}
        if 'review_file' in sem:
            sem['review_file']='continuity-review.json';sem['review_file_scope']='当前动作衔接复查；身份审校为prior-identity-review.json及上一交付目录。'
        if 'identity_revision' in sem:sem['identity_revision']['inspection_file']='prior-identity-review.json'
        for item in ledger.get('advisory_dispositions',[]):
            c=next((v for t,v in CHANGES[ep].items() if target_map(t,ep)==item.get('target')),None)
            if c:
                item['previous_basis']=item.get('basis','')
                item['basis']='本轮实际时程：'+c['opening']+' → '+'；'.join(c['beats'])+' → '+c['landing']+'。互动：'+c['coupling']
        # Current continuity notes must not keep the superseded "not animating" decisions.
        for collection in ('new_continuity','continuity'):
            for item in sem.get(collection,[]):
                image=item.get('image','')
                affected=[c for t,c in CHANGES[ep].items() if image in (rows[target_map(t,ep)]['source_images']+rows[target_map(t,ep)]['derived_from'])]
                if affected:
                    item['connection']=affected[0]['evidence'];item['participation']=affected[0]['coupling']
        current.write_text(after,encoding='utf-8');(dest/current.name).write_text(after,encoding='utf-8')
        for name in ('source-integrity.json','source-package.json','source-copy-check.json','skill-sync.json'):
            if (prior/name).exists():shutil.copyfile(prior/name,dest/name)
        if ep==18:
            intake=root/'storyboards/deliveries/2026-10-09_Gen2.8_整话非露骨改编/source-intake-audit.json'
            if intake.exists():shutil.copyfile(intake,dest/intake.name)
        shutil.copyfile(prior/'identity-review.json',dest/'prior-identity-review.json')
        shutil.copyfile(prior/'prior-image-reviews.json',dest/'prior-image-reviews.json')
        jwrite(dest/'source-ledger-v3.json',ledger);jwrite(dest/'continuity-review.json',audit);jwrite(dest/'continuity-changes.json',changed)
        jwrite(dest/'dialogue-mapping-current.json',[{'image':p['image'],'bubbles':p.get('bubbles',[]),'dialogue_turns':p.get('dialogue_turns',[]),'coverage_groups':p.get('coverage_groups',[])} for p in ledger['panels']])
        summary={'episode':ep,'current':str(current),'delivery':str(dest),'clips':len(set(s['target'].split('/')[0] for s in new)),
            'shots':len(new),'seconds':sum(s['seconds'] for s in new),'formal_reference_count':len(set(r for s in new for r in s['refs'])),
            'changed_existing_shots':len(CHANGES[ep]),'added_bridges':1 if ep==19 else 0,'inspected_images':len(VIEWED[ep]),
            'reviewed_boundaries':len(boundaries),'dialogue_unchanged':True,'reference_order_unchanged':True,'manual_overflow_items':0,
            'rule_input_bytes':sum((SKILL/name).stat().st_size for name in ['SKILL.md']+['references/'+n+'.md' for n in ['core-authoring','dialogue-performance','acting-calibration','source-risk','cinematic-rendering','2d-animation-execution']]),
            'current_sha256':sha(current),'video_generated':False}
        summaries.append(summary)
    jwrite(HERE/'revision-summary.json',summaries)
    print(json.dumps([{k:s[k] for k in ('episode','shots','seconds','changed_existing_shots','added_bridges')} for s in summaries],ensure_ascii=False))

if __name__=='__main__':create()
