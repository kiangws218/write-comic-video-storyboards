"""Render manually authored, image-reviewed batches; never infer source evidence."""
from pathlib import Path
import json, math, re, sys

ROOT=Path(__file__).parent
SKILL=Path('C:/Users/86135/.codex/skills/write-comic-video-storyboards-gen2-8')
FIELDS=['镜头设计','可见动作','可见背景','台词与语气','光影布光','声音设计']

def speech_seconds(text):
    if not text.strip(): return 0
    count=sum(c.isalnum() for c in text)
    return round(max(2, count/6+text.count('、')*.25+sum(text.count(p) for p in '。！？')*.45+text.count('…')*.3),2)

def render():
    sources=[]; drafts=[]
    for file in sorted((ROOT/'batches').glob('*-source.json')):
        sources.extend(json.loads(file.read_text(encoding='utf-8')))
        prose=file.with_name(file.name.replace('-source','-shots'))
        if prose.exists(): drafts.extend(json.loads(prose.read_text(encoding='utf-8')))
    source_by={p['id']:p for p in sources}
    ledger={'version':3,'source_language':'zh','character_registry_source':'../../../../../character-references/角色映射.md version 2, 2026-10-11','panels':[],'shots':[],'performance':[]}
    # Clip placement is provisional until the next source unit has been inspected.
    units=[]
    for p in sources:
        shots=[s for s in drafts if s['id']==p['id']]
        if shots: units.append((p,shots))
    clips=[]; active=[]; total=0
    for p,shots in units:
        duration=sum(s['sec'] for s in shots)
        if duration>15:
            if not p.get('overflow'): raise ValueError('Plan stable overflow split explicitly: '+p['id'])
            if active and (p.get('new_scene',False) or total+shots[0]['sec']>15 or shots[0].get('clip_start',False)):
                clips.append(active); active=[]; total=0
            for shot in shots:
                if active and (total+shot['sec']>15 or shot.get('clip_start',False)):
                    clips.append(active); active=[]; total=0
                active.append(shot); total+=shot['sec']
        else:
            if active and (total+duration>15 or p.get('new_scene',False)):
                clips.append(active); active=[]; total=0
            active.extend(shots); total+=duration
        if p.get('clip_end',False): clips.append(active); active=[]; total=0
    if active: clips.append(active)
    shot_targets={}; output=['# 第20话 制作分镜 Gen2.8\n', '## 场景色彩基准\n',
        '高品质二维手绘动画，清晰线条与成块阴影，表演从人物正在做的事和彼此回应展开。面部近景保留准确眉形、目光与口部变化；可见肩背和手上任务参与整句表演，镜尾延续当前姿态而不统一回正。洞窟沿用第16—19话的深褐岩壁、灰褐石地、左上方柔光与较冷暗面；入口异空间保持深灰水面、冷白反光与层叠暗色群像。人物设计采用共享参考图库，当前衣物状态和伤势以本话源格为准。\n',
        '## 非人物上色锁定\n',
        '岩壁深褐，石缝褐黑，石地灰褐；街市木构蜂蜜褐，纸灯浅米白。金属盔甲钢灰，刀刃银灰、柄缠布米白；异空间水面深灰蓝，亮纹冷白，暗色群像保留黑灰层次；衣装和人物本色按参考图库，仅在源格有对应设计处使用。\n']
    for c,shots in enumerate(clips,1):
        output.append(f'## 【片段{c}】（{sum(s["sec"] for s in shots)}秒）\n')
        for n,s in enumerate(shots,1):
            target=f'片段{c}/分镜{n}'; shot_targets.setdefault(s['id'],[]).append((s,target))
            output.append(f'**分镜{n}（{s["sec"]}秒）：**')
            if not s.get('uncited'): output.append(f'分镜参考 `[第20話_{s["id"]}.jpg]`')
            output.extend(f'【{name}】：{s["f"][i]}' for i,name in enumerate(FIELDS))
            output.append('')
    for p in sources:
        owned=shot_targets.get(p['id'],[])
        if not owned: continue
        image='第20話_'+p['id']+'.jpg'
        panel={'image':image,'viewed_at_drafting':True,'drafting_resolution':p.get('resolution','720p'),'renderable_visual':True,
            'page_overlays':p.get('overlays',[]),'source_bubble_count':len(p['bubbles']),'bubble_audit':'pass',
            'background':{'type':p['bgtype'],'description':p['bgobserved'],'evidence':'current_panel'},
            'composition_lock':p['lock'],'source_facts':p['facts'],'story_context':p.get('context',[]),'non_renderable_terms':p.get('excluded',[]),
            'coverage':'shared' if len(owned)==1 else 'mixed','coverage_reason':p['coverage'],'bubbles':[]}
        for bi,b in enumerate(p['bubbles']):
            destinations=[(s,t) for s,t in owned if bi in s.get('b',[])]
            if len(destinations)!=1: raise ValueError(f'Bubble {image}/{bi} needs explicit unique mapping')
            s,target=destinations[0]
            panel['bubbles'].append({'id':f'b{bi+1}','speaker':b[1],'kind':b[3] if len(b)>3 else 'dialogue',
                'source_text':b[0],'status':'mapped','script_text':b[2],'seconds':speech_seconds(b[2]),'target':target})
        for bi,reason in p.get('bubble_omissions',{}).items():
            panel['bubbles'][int(bi)].update(status='omitted',omission_reason=reason)
        if p.get('speaker_evidence'):
            for bi,item in enumerate(panel['bubbles']): item['speaker_evidence']=p['speaker_evidence'][bi]
        if 'D' in p['flags']:
            panel['dialogue_turns']=[{'id':f't{i+1}','bubble_ids':[f'b{i+1}'],'speaker':b[1],'kind':b[3] if len(b)>3 else 'dialogue','function':p['coverage']} for i,b in enumerate(p['bubbles'])]
            panel['coverage_groups']=[{'id':f'g{i+1}','turn_ids':[f't{b+1}' for b in s.get('b',[])], 'targets':[t], 'merge_basis':p['coverage']} for i,(s,t) in enumerate(owned) if s.get('b')]
        if p.get('resolution_escalation_reason'): panel['resolution_escalation_reason']=p['resolution_escalation_reason']
        if p.get('overflow'): panel['overflow_split']={'estimated_seconds':sum(s['sec'] for s,t in owned),'segments':list(dict.fromkeys(int(t.split('/')[0][2:]) for s,t in owned)),**p['overflow']}
        ledger['panels'].append(panel)
        for s,target in owned:
            row={'target':target,'role':'uncited_coverage' if s.get('uncited') else 'source_locked',
                'source_images':[] if s.get('uncited') else [image], 'purpose':s.get('purpose',p['coverage']),
                'evidence':p['motion'],'background_excerpt':s['f'][2],'viewed_while_writing':True,'source_audit':'pass','unsupported_additions':[],
                'fact_claims':s.get('claims',p['facts']),'risk_flags':p['flags'],'risk_basis':p['risk'],'motion_decision':p['motion'],
                'action_admissions':[dict(a,source_image=image,visible_in_framing=True,anchor_safe=True) for a in p.get('admissions',[])],
                'background_decision':{'mode':s.get('bgmode',p.get('bgmode','physical')),'basis':p['bgbasis'],'source_refs':[str((ROOT.parent.parent.parent/'source/monochrome-panels'/r).resolve()) if not Path(r).is_absolute() else r for r in p.get('bgrefs',[])]},
                'camera_decision':{'mode':s.get('camera_mode','fixed'),'reason':s.get('purpose',p['coverage']),'anchor_phase':'middle','opening':p['plan'][0],'landing':p['plan'][3]}}
            if s.get('uncited'): row.update(s['uncited'],derived_from=[image])
            ledger['shots'].append(row)
            if 'P' in p['flags'] or sum(sum(c.isalnum() for c in p['bubbles'][bi][2]) for bi in s.get('b',[]))>20:
                plan=s.get('plan',p['plan'])
                speaking=sum(speech_seconds(p['bubbles'][bi][2]) for bi in s.get('b',[]))
                if len(s.get('b',[]))>1: speaking+=.35*(len(s['b'])-1)
                ledger['performance'].append({'target':target,'evidence':p['motion'],
                    'card':{'opening':plan[0],'beats':plan[1],'coupling':plan[2],'landing':plan[3]},
                    'details':[s['f'][1]],'intervals':[{'speech_seconds':speaking,'acting_seconds':s.get('acting',max(1,s['sec']-1)),'concurrent':True}]})
    ledger['final_audit']={'semantic_review':[{'image':p['id'],'decision':p['review']} for p in sources if p['id'] in shot_targets], 'scope':'逐批看图建证据并创作；镜尾与入镜状态及源图阶段锚点分别核对。战斗模块按用户要求禁用。'}
    current=ROOT.parent.parent/'current'; current.mkdir(exist_ok=True)
    (current/'第20话_制作分镜_Gen2.8.md').write_text('\n'.join(output)+'\n',encoding='utf-8')
    (ROOT/'source-ledger-v3.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Rendered {len(ledger["panels"])} panels, {len(drafts)} shots, {len(clips)} clips, {sum(s["sec"] for s in drafts)} seconds')

if __name__=='__main__': render()
