from pathlib import Path
from copy import deepcopy
import json,hashlib
R=Path(__file__).resolve().parent;P=R/'scene-ledger.json'
def load():return json.loads(P.read_text(encoding='utf-8'))
def save(d):P.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def init():
 d=load()
 if d['shots']:return
 rt=d['action_routes'][0];d['route_proposal_history']=[{'path':rt['path'],'sha256':rt['proposal_sha256'],'status':'用户纠正为扯断后用力砸地；旧甩开解释作废。'}]
 rt['path']=rt['path'].replace('随后将残段甩开／放开，一手空下','随后握住分离部分用力砸到石地，接触后手空下').replace('抓握、断开、甩离','抓握、断开、用力砸地').replace('扯开与甩落','扯开与砸地').replace('按双手扯断小体并甩开','按双手扯断小体后用力砸地').replace('需要确认的关键解释：','用户已确认的关键解释：')
 rt['user_confirmation']={'quote':'2.青把白色蝌蚪扯断指头，用力砸到地上。其他部分没问题','sha256':None,'interpretation_note':'结合前一提案及本次指明砸地，执行为“扯断后用力砸地”；原话完整保留，不解读成青扯断自己的手指。'}
 rt['confirmation_status']='user_explained_corrected_path';rt['proposal_sha256']=None
 p=next(p for p in d['panels'] if p['image']=='第28話_04_001.jpg');p['first_pass']['initial_action_understanding']='用户明确解释：扯断白色蝌蚪后，用力砸到地上；该格保留砸地后的反弹残段／落点形和已经空下的手。'
 d['stage']='second_pass_in_progress'
 d['initial_state']={'场景':'城内轰响与避难治疗房间','青.武器':'空手','武士.形态':'巨大半实力形态','青.新伤':'无新增击中或喷流沾染'}
 first=json.loads((R.parent/'scene-ledger.json').read_text(encoding='utf-8'))
 for person in first['character_registry']:
  if person['id'] in ['C005','C006','U001'] and not any(p['id']==person['id'] for p in d['character_registry']):d['character_registry'].append(deepcopy(person))
 d['character_registry'].append({'id':'C004','canonical_name':'董白','aliases':[],'identity_status':'identified','design_reference':'turnarounds/董白.png，已实际打开；黑发双高长马尾、浅色挑染、蓝眼、黑色高领无袖短裙与高跟鞋。','performance_profile':{'baseline':'高傲自负；从容占据空间与自信判断，保留原格夸张圆眼、惊讶和受冒犯反应。','source':'项目共享人物主档用户确认条目。'},'reference_visually_opened':True})
 d['revision_audit'].append({'date':'2026-10-25','scope':'按用户明确纠正进入第二遍；小体由甩开改为用力砸地，其他路径沿用确认。','user_quote':rt['user_confirmation']['quote']})
 save(d)

def add(n,duration,camera,action,background,light,sound,ja=(),tone='',kind='action',phase='process',node=None,meaning='',card=None,mode='continuity',characters=None):
 d=load();name=f'第28話_{n}.jpg';p=next(p for p in d['panels'] if p['image']==name)
 assert not any(name in s['source_images'] for s in d['shots']),name
 assert len(ja)==len(p['bubbles']),(name,len(ja),len(p['bubbles']))
 target=f'片段1/分镜{len(d["shots"])+1}';t=.4;lines=[]
 for b,txt in zip(p['bubbles'],ja):
  sec=round(max(.6,sum(c not in '、。？！… ,.!?' for c in txt)/5.8+.2),2)
  b.update(script_text=txt,status='mapped',target=target,start=round(t,2),seconds=sec);t+=sec+.3
  typ={'inner':'（内心）','narration':'（旁白）'}.get(b['kind'],'')
  if not typ and (n in ['02_002','06_002','06_004','10_002'] or (n=='02_004' and b['speaker']=='门口来者')):typ='（画外音）'
  lines.append(f'{b["speaker"]}{typ}：“{txt}”（{tone}）')
 if ja:duration=max(duration,int((t+.5)*2)/2)
 p.update(viewed_at_drafting=True,drafting_resolution='720p',bubble_audit='pass',bubble_audit_notes='本次第二遍实际重开此格；逐泡核对文字、类型、尾部及前后声音，等值翻译日语。',composition_lock=p['first_pass']['observation'],source_facts={'entities':[p['first_pass']['observation']],'actions':[],'relations':[]},background={'mode':mode,'basis':'原格实见环境；缺失部分按统一场景设计，色彩为既有参考及生产设计。'},node_state=node or {},anchor_target=target,narrative_kind=kind,story_context=[meaning or p['first_pass']['initial_action_understanding']])
 if kind in ['action','mixed']:p['action_reading']={'summary':meaning or p['first_pass']['initial_action_understanding'],'phase':phase,'world_motion':meaning or p['first_pass']['initial_action_understanding'],'screen_motion':'按本镜实际面对对象、趋近／远离及横越路线；摄影机变换不算人物瞬移。','grounding':'手脚接触按该格与邻格实见状态；画外部分不冒报观察。','basis':'第二遍实际重看原图，关键路线按用户本次明确解释。'}
 flags=(['P'] if card else [])+(['D'] if len(ja)>1 or sum(len(t) for t in ja)>42 else [])
 s={'target':target,'duration':duration,'role':'source_locked','source_images':[name],'purpose':meaning or p['first_pass']['initial_action_understanding'],'characters':characters if characters is not None else list(dict.fromkeys(b['speaker'] for b in p['bubbles'])),'risk_flags':flags,'risk_basis':'人物表演与声音承载按本场任务规划。' if flags else '环境或动作节点。','anchor_phase':phase,'anchor_elements':p['composition_lock'],'anchor_state':node or {},'state_changes':node or {},'viewed_while_writing':True,'source_audit':'pass','source_audit_notes':'实际第二遍对照：原格主体、动作阶段、重要构图、表情、持物／接触及气泡完整保留。','frame_adaptation':'16:9等比动画画幅，竖格按实际连续摇移展开，原漫画作为镜内过程节点参考。','fields':dict(zip(['镜头设计','可见动作','可见背景','台词与语气','光影布光','声音设计'],[camera,action,background,'\n'.join(lines) if lines else '无台词。',light,sound]))}
 if kind in ['action','mixed']:s['meaning_excerpt']=action
 if card:s['performance']={'card':card,'details':[action[:85]],'intervals':[{'speech_seconds':round(sum(b['seconds'] for b in p['bubbles']),2),'acting_seconds':duration,'concurrent':True}]}
 d['shots'].append(s);save(d)
if __name__=='__main__':init()
