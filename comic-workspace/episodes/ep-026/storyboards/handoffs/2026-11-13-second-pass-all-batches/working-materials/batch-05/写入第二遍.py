from pathlib import Path
import json,math
R=Path(__file__).resolve().parent;P=R/'scene-ledger.json'
def load():return json.loads(P.read_text(encoding='utf-8'))
def save(d):P.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

def add(n,duration,camera,action,bg,light,sound,ja=(),tone='',kind='action',phase='process',node=None,meaning='',card=None,mode='continuity',motion='',ground='',characters=None):
 d=load();image=f'第28話_{n}.jpg';p=next(p for p in d['panels'] if p['image']==image)
 assert not any(image in s['source_images'] for s in d['shots']),image
 assert len(ja)==len(p['bubbles'])
 target=f'片段1/分镜{len(d["shots"])+1}';t=.3;lines=[]
 for b,txt in zip(p['bubbles'],ja):
  sec=round(max(.7,sum(c not in '、。？！… ,.!?「」' for c in txt)/4.8+.2),2)
  b.update(script_text=txt,status='mapped',target=target,start=round(t,2),seconds=sec);t+=sec+.25
  typ={'inner':'（内心）','narration':'（旁白）'}.get(b['kind'],'')
  lines.append(f'{b["speaker"]}{typ}：“{txt}”（{tone}）')
 if ja:duration=max(duration,math.ceil((t+.15)*2)/2)
 node=node or {'叙事阶段':meaning};meaning=meaning or p['first_pass']['initial_action_understanding']
 p.update(viewed_at_drafting=True,drafting_resolution='720p',bubble_audit='pass',bubble_audit_notes='第二遍实际重开逐图看清主体、接触与全部气泡，按最新用户路径纠正。',composition_lock=p['first_pass']['observation'],source_facts={'entities':[p['first_pass']['observation']],'actions':[],'relations':[]},background={'mode':mode,'basis':'当格实见云天／石面／烟尘与同场生产设计，色彩统一。'},node_state=node,anchor_target=target,narrative_kind=kind,story_context=[meaning])
 if kind in ['action','mixed']:p['action_reading']={'summary':meaning,'phase':phase,'world_motion':meaning,'screen_motion':motion or '按本镜主体朝向与镜内过程展开，摄影机换面不重新起动。','grounding':ground or '保留当格接触／悬空状态，依据前后关系与用户明确纠正。','basis':'本次实际重开二遍；关键空间关系按用户明确纠正。'}
 flags=(['P'] if card else [])+(['D'] if len(ja)>1 or sum(len(x) for x in ja)>42 else [])
 s={'target':target,'duration':duration,'role':'source_locked','source_images':[image],'purpose':meaning,'characters':characters if characters is not None else list(dict.fromkeys(b['speaker'] for b in p['bubbles'])),'risk_flags':flags,'risk_basis':'人物表演、动作连接与对白承载。' if flags else '动作或环境节点。','anchor_phase':phase,'anchor_elements':p['composition_lock'],'anchor_state':node,'state_changes':node,'viewed_while_writing':True,'source_audit':'pass','source_audit_notes':'实际第二遍核准原作主体、阶段、关键构图、表情与全文；晨光、失力、搀扶与扣头揭晓按用户确认执行。','frame_adaptation':'16:9等比二维画幅；竖长原格通过明确摇移或短促展开经过必要节点，漫画不是生成首帧。','fields':dict(zip(['镜头设计','可见动作','可见背景','台词与语气','光影布光','声音设计'],[camera,action,bg,'\n'.join(lines) if lines else '无台词。',light,sound]))}
 if kind in ['action','mixed']:s['meaning_excerpt']=action
 if card:s['performance']={'card':card,'details':[action[:85]],'intervals':[{'speech_seconds':round(sum(b['seconds'] for b in p['bubbles']),2),'acting_seconds':duration,'concurrent':True}]}
 d['shots'].append(s);save(d)
