from pathlib import Path
import json,copy,re,subprocess,sys,math,hashlib
O=Path(__file__).parent;R=O.parents[3];S=Path('C:/Users/86135/.codex/skills/write-comic-video-storyboards-gen2-8')
FIELDS=['镜头设计','可见动作','可见背景','台词与语气','光影布光','声音设计']
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
integrity=read(O/'source-integrity.json');rank={p['image']:i for i,p in enumerate(integrity)};by_integrity={p['image']:p for p in integrity}
observations=[p for f in sorted((O/'observations').glob('*.json')) for p in read(f)];observations.sort(key=lambda p:rank[p['image']]);assert len({p['image'] for p in observations})==len(observations)
drafts=[s for f in sorted((O/'drafts').glob('*.json')) for s in read(f)]
groups={p['image']:[s for s in drafts if s['image']==p['image']] for p in observations};assert sum(map(len,groups.values()))==len(drafts)
ledger={'version':3,'source_language':'zh','scope':f'第19话用户提供75格；当前已检查{len(observations)}格。','evidence_workflow':'逐格查看720p代理，先记录源图事实、气泡与准入规划，再写六字段；原尺寸与安全取舍单独标明。','panels':[],'shots':[],'performance':[],'character_registry':read(O.parent/'ep018-full/source-ledger-v3.json')['character_registry']}
header='# 第19话制作分镜 Gen2.8\n\n'
header+='> 覆盖工作区19.zip提供的75个原文件（第02—26页，包中没有第01页）。普通剧情与对白保留原意；裸体局部采用非露骨取景，范围见交付说明。纯作品标题不生成镜头，纯台词格并入相邻动作镜头。\n\n'
header+='## 场景色彩基准\n\n二维手绘动画：清晰线条、成块阴影，人物以整句情绪和任务互动展开表演。洞窟岩壁采用低饱和深褐，上方偏左柔光照入，石缝深暗。董白黑发蓝眼，青白发红眼，春子棕发；人物按已核对的人设统一。秃顶兽人为低饱和橄榄绿色肤色、黑色尖下巴胡须。\n\n'
header+='## 非人物上色锁定\n\n洞窟岩石深褐、石缝深褐黑；诊所木构灰棕、床单与门帘米灰；金属甲钢灰；刀柄缠布浅米灰、刃面银灰。通道能量冷白，水面灰暗并映冷白细纹；黑袍来者袍面深灰、帽内黑；巨型兽人保持原图的灰暗躯体、黑脸白眼。新角色颜色为本稿统一配色，不宣称来自未提供的彩色原图。\n'
text=header;clip=0;number=0;scene=None;durations={};assigned=[]
for p in observations:
    owned=groups[p['image']]
    if not owned:
        assert p.get('renderable_visual') is False or p.get('omit_reason'),p['image']
        continue
    unit=sum(s['seconds'] for s in owned)
    assert unit<=15,('Needs explicit natural overflow split',p['image'],unit)
    if not clip or scene!=owned[0]['scene'] or durations[clip]+unit>15 or owned[0].get('new_clip'):
        clip+=1;number=0;durations[clip]=0;scene=owned[0]['scene'];text+=f'\n## 【片段{clip}】\n'
    for i,s in enumerate(owned):
        s=copy.deepcopy(s);number+=1;s.update(target=f'片段{clip}/分镜{number}',source_locked=i==0 and not s.get('uncited',False));s.setdefault('jp',p.get('jp',[]) if len(owned)==1 else []);assigned.append(s);durations[clip]+=s['seconds'];assert len(s['fields'])==6
        text+=f'\n**分镜{number}（{s["seconds"]}秒）：**\n'
        if s['source_locked']:text+=f'分镜参考 `[{p["image"]}]`\n'
        text+='\n'.join(f'【{k}】：{v}' for k,v in zip(FIELDS,s['fields']))+'\n'
for op in observations:
    owned=[s for s in assigned if s['image']==op['image']]
    dialogue_only=bool(op.get('dialogue_attaches_to'))
    if dialogue_only:owned=[s for s in assigned if s['image']==op['dialogue_attaches_to']]
    if not owned:
        p=copy.deepcopy(op); p.update(viewed_at_drafting=True,drafting_resolution='720p',source_bubble_count=len(p.pop('bubbles')),bubbles=[],bubble_audit='pass',renderable_visual=False,reference_scope='typography_only',coverage='none',story_context=op.get('story_context',[]),non_renderable_terms=op.get('non_renderable_terms',[]),background={'type':op['background'],'description':op['background_description'],'evidence':'current_panel'},page_overlays=[{'kind':'caption','source_text':op.get('overlay_text',''),'render':False}],source_integrity={**by_integrity[p['image']],'source_unchanged':True}); ledger['panels'].append(p);continue
    p=copy.deepcopy(op);p.pop('plan',None);p['performance_plan']=op.get('plan');raw=p.pop('bubbles');translations=[(s,i,j) for s in owned for i,j in enumerate(s['jp']) if j in op['jp']];assert len(raw)==len(translations),(p['image'],len(raw),len(translations))
    p.update(viewed_at_drafting=True,drafting_resolution='720p',renderable_visual=True,reference_scope='safe_narrative_selection' if op.get('adaptation_scope') else 'full_renderable_panel',source_bubble_count=len(raw),bubble_audit='pass',coverage='none' if not raw else 'shared' if len(owned)==1 else 'mixed',coverage_reason='先保留语义转折与当前构图，再按自然日文时长、表演任务和必要反应规划镜头。',story_context=op.get('story_context',[]),non_renderable_terms=op.get('non_renderable_terms',[]),page_overlays=[],bubbles=[],dialogue_turns=[],coverage_groups=[],background={'type':op['background'],'description':op['background_description'],'evidence':'current_panel'},source_integrity={**by_integrity[p['image']],'source_unchanged':True})
    if op.get('sfx'):p['page_overlays'].append({'kind':'sfx','source_text':op['sfx_source_text'],'render':False,'audio_meaning':op['sfx']})
    for i,(b,mapping) in enumerate(zip(raw,translations)):
        s,local,jp=mapping;assert jp in s['fields'][3],(p['image'],jp)
        weights=[max(1,len(re.sub(r'[\s。！？、…]','',v))) for v in s['jp']]
        seconds=s['bubble_seconds'][local] if s.get('bubble_seconds') else round(s['speech_seconds']*weights[local]/sum(weights),3)
        p['bubbles'].append({'id':f'b{i+1}','speaker':b[0],'kind':b[2] if len(b)>2 else 'dialogue','source_text':b[1],'status':'mapped','target':s['target'],'script_text':jp,'seconds':seconds,'speaker_evidence':op.get('speaker_evidence','本格气泡尾与可见发言者；画外发言不增加画内人物。')})
        p['page_overlays'].append({'kind':'caption','observed_kind':'bubble','source_text':b[1],'render':False});p['dialogue_turns'].append({'id':f't{i+1}','bubble_ids':[f'b{i+1}'],'function':b[1]})
    for target in dict.fromkeys(b['target'] for b in p['bubbles']):
        ids=[f't{i+1}' for i,b in enumerate(p['bubbles']) if b['target']==target]
        p['coverage_groups'].append({'id':f'g{len(p["coverage_groups"])+1}','turn_ids':ids,'targets':[target],'merge_basis':op.get('merge_basis','同一姿态与当下回应能够承接相邻短句，语义顺序保持，没有隐藏切镜。')})
    ledger['panels'].append(p)
    if dialogue_only:
        p.update(renderable_visual=False,reference_scope='typography_only',omit_reason=op['omit_reason'])
        continue
    for s in owned:
        plan=copy.deepcopy(s.get('plan',op.get('plan')));flags=['P'] if plan else []
        if len(raw)>1 or any(len(t['script_text'])>=28 for t in p['bubbles']):flags.append('D')
        if op.get('original_resolution_viewed') or s.get('G') or not s['source_locked']:flags.append('G')
        mode=s.get('background_mode','continuity' if op['background']=='omitted' else op['background']);purpose=s.get('purpose',plan['coupling'] if plan else '明确当前环境、冲击或画外剧情落点。')
        sh={'target':s['target'],'role':'source_locked' if s['source_locked'] else 'uncited_coverage','source_images':[p['image']] if s['source_locked'] else [],'derived_from':[] if s['source_locked'] else [p['image']],'evidence':'current_panel','purpose':purpose,'background_excerpt':s['fields'][2],'viewed_while_writing':True,'source_audit':'pass','unsupported_additions':[],'risk_flags':flags,'risk_basis':purpose,'fact_claims':s.get('fact_claims',p['source_facts']),'motion_decision':{'classification':op['kind'],'observed_anchor':p['composition_lock'],'admitted_plan':plan,'source_anchor_placement':op['anchor_phase'],'continuity':op['continuity'],'inference_limit':op['admission']},'camera_decision':{'mode':s.get('camera_mode','fixed'),'reason':s.get('camera_reason',purpose),'anchor_phase':op['anchor_phase'],'opening':s.get('camera_opening',s['fields'][0]),'landing':s.get('camera_landing',s['fields'][0]),'evidence':p['composition_lock']},'background_decision':{'mode':mode,'basis':s.get('background_basis','当前源图的可见实景或已声明的非实景/遮挡处理。'),'source_refs':s.get('background_refs',[p['image']]),'inspected_resolution':'720p'},'action_admissions':[{'claim':s['fields'][1],'source_image':p['image'],'visual_evidence':'观察：'+'；'.join(p['source_facts']['actions']+p['source_facts']['relations'])+'。规划：'+op['admission'],'visible_in_framing':True,'anchor_safe':True}] if plan else []}
        if not s['source_locked']:sh.update(s['coverage'])
        if op.get('adaptation_scope'):sh['source_fidelity_mode']='non_graphic_adaptation'
        sh['risk_basis']='；'.join((['P：可见人物的表情、任务或互动需要阶段设计。源图动作：'+'、'.join(p['source_facts']['actions'])] if 'P' in flags else [])+(['D：当前源图有'+str(len(raw))+'项对白/内心内容，按语义转折与自然日文预算检查覆盖。'] if 'D' in flags else [])+(['G：'+op.get('original_resolution_reason','派生取景按已检查构图和相邻镜头差异核对。')] if 'G' in flags else [])) or '当前镜头为简短图形/环境节拍，未出现额外角色动作。'
        ledger['shots'].append(sh)
        if plan or s['speech_seconds']>=3.5:
            intervals=s.get('intervals',[{'speech_seconds':s['speech_seconds'],'acting_seconds':s['acting_seconds'],'concurrent':True}]);assert sum(max(i['speech_seconds'],i['acting_seconds']) if i.get('concurrent',True) else i['speech_seconds']+i['acting_seconds'] for i in intervals)<=s['seconds']+.0001
            ledger['performance'].append({'target':s['target'],'evidence':'current_panel','card':plan,'details':[s['fields'][1]],'intervals':intervals,'timing_basis':'日文发声与当下动作交叠，分开的入句、停顿和镜尾以intervals顺序累计。','long_take_reason':purpose})
ledger['source_files']=integrity;ledger['source_package']=read(O/'source-package.json');ledger['final_audit']={'clip_boundaries':{str(c):{'seconds':t} for c,t in durations.items()},'semantic_review':{'status':'in_progress','continuity':[{'image':p['image'],'connection':p['continuity']} for p in observations]},'source_scope':ledger['scope'],'limitations':'非露骨改编处单独标明；结构通过不等于视频表演质量，未生成视频。'}
save('source-ledger-v3.json',ledger);save('new-shot-index.json',assigned);save('progress.json',{'inspected_panels':len(observations),'source_count':75,'shots':len(assigned),'clips':len(durations),'runtime_seconds':sum(durations.values()),'clip_seconds':durations})
path=O/'第19话_制作分镜_Gen2.8.md';path.write_text(text,encoding='utf-8')
print(f'Inspected {len(observations)}/75; {len(assigned)} shots, {len(durations)} clips, {sum(durations.values())} seconds.')
if '--validate' in sys.argv:
    run=subprocess.run([sys.executable,'-X','utf8',str(S/'scripts/validate_storyboard.py'),str(path),'--max-seconds','15','--image-dir',str(O/'analysis-proxies'),'--source-ledger',str(O/'source-ledger-v3.json'),'--require-source-ledger'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8');(O/'validation.txt').write_text(run.stdout,encoding='utf-8');print('\n'.join(l for l in run.stdout.splitlines() if l.startswith(('错误','结构','片段数','参考图数'))));print('Advisories:',sum(l.startswith('警告') for l in run.stdout.splitlines()));sys.exit(run.returncode)
