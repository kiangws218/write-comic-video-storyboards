from pathlib import Path
import json,math
R=Path(__file__).resolve().parent;P=R/'scene-ledger.json'
def load():return json.loads(P.read_text(encoding='utf-8'))
def save(d):P.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def init():
 d=load();assert not d['shots']
 rt=d['action_routes'][0]
 d['route_proposal_history']=[{'path':rt['path'],'sha256':rt['proposal_sha256'],'status':'用户纠正：武士原地只回头，青残影瞬间到背后；空中旁观；伏地与雾中走来的青合为前推转焦。'}]
 quote='1.武士就站在原地维持站姿，只有回头，因为青速度很快，这里青要直接残影瞬移过来。4.就按漫画来处理就行，有一种旁观者视角。5.20001和20002合并为同一个镜头，烟雾散开，镜头前推，先展示武士趴在地上一动不动，随后前景趴在地上的武士虚化，聚焦后面雾中走出来的青。青从远处缓缓走来'
 rt['path']='''本批第28話_11_003—20_003，22原文件；21_001、21_002只作后续邻格。
1. 青咬指后蹬裂石面，以高速残影瞬间出现在武士背后说“在你后面”；武士保持原地站姿，双臂与脚不改位，只有头转向青。残影是高速到位的画面表达，不补绕身路线或武士挥臂攻击。
2. 青拉拳，命中武士头／颈侧交叠处，武士被打得横向离地，青贴身跟进连续拳击；12_004的EUT...!!按武士受击闷哼。用户针对其他步骤给出明确纠正，未改此项，沿用确认。
3. 青支撑脚踩实，短喝蓄力，上踢把武士送往高空；青竖直踢腿、屈收另一腿与高处武士小身影保留。16_001保留悬空城镇平台、斜索与竖直轨迹的高度关系。
4. 武士在林海上空吃痛质问，青追到其头旁反问。随后严格以漫画旁观者远景呈现两小身影闪点、扩散冲击环、城内远看竖向坠落烟尘；不补近处空中招式或具体向下重击姿势。
5. 20_001和20_002是同一个连续镜头：先看武士伏在石坑里一动不动，烟尘散开，镜头缓慢前推；武士留在前景逐渐虚化，焦点交给远处雾中缓缓走来的青。青在平台上从远处走来，不站到武士背上。20_003再看她按住太阳穴、喘息微颤着嘲讽，本批结束。
原作未证明死亡；高空白迹与冲击环沿漫画作为运动与受力表现，不新设能力或突然变成夜晚。16_003中英词义注、20_003页外评论不作人物台词。第三轮用插入与返回组织蹬地、拉拳、拳击接触／横飞、连打节奏、脚下转力与上踢；空中保持旁观距离，落地只发生一次。'''
 rt.update(proposal_sha256=None,confirmation_status='user_explained_corrected_path',user_confirmation={'quote':quote,'sha256':None,'interpretation_note':'依用户最新纠正直接进入二遍，不另求重复确认；1、4、5替换旧提案，2、3保留。'})
 d['stage']='second_pass_in_progress'
 d['initial_state']={'场景':'阴云下的城镇石铺平台','青.武器':'空手','青.状态':'已咬指，力量速度激增，尚能行动','武士.形态':'巨大形态','武士.位置':'原地站立','叙事阶段':'青高速到背后之前'}
 d['character_registry']=[c for c in d['character_registry'] if c['id'] in ['C001','C008']]
 d['look']='日间阴云下的悬空城镇平台，灰绿石铺地面、灰米砖墙、蓝灰屋顶、米灰烟尘；远处森林灰绿，岩体断面深灰褐，跨平台斜索深褐。正上方云天冷白漫射，烟囱残基侧稍亮，平台敞口中性弱补光。高空云天深蓝灰，细白粒与亮迹为速度和冲击的二维画面表现。高品质二维手绘，手脚接触、残影和单次落地节奏清楚。'
 for p in d['panels']:
  if p['image'] in ['第28話_11_003.jpg','第28話_12_002.jpg','第28話_17_001.jpg','第28話_18_001.jpg','第28話_18_002.jpg','第28話_20_001.jpg','第28話_20_002.jpg']:
   p['user_action_override']='最新用户纠正见QG-B04-28B：原地只回头／高速残影／空中旁观／伏地前推转焦后景走来，优先于未确认首遍解释。'
 d['revision_audit'].append({'date':'2026-10-25','scope':'依用户纠正修订动作路径并开始二遍。完整保留原提案与本次原话。','user_quote':quote})
 save(d)

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
 s={'target':target,'duration':duration,'role':'source_locked','source_images':[image],'purpose':meaning,'characters':characters if characters is not None else list(dict.fromkeys(b['speaker'] for b in p['bubbles'])),'risk_flags':flags,'risk_basis':'人物表演、动作连接与对白承载。' if flags else '动作或环境节点。','anchor_phase':phase,'anchor_elements':p['composition_lock'],'anchor_state':node,'state_changes':node,'viewed_while_writing':True,'source_audit':'pass','source_audit_notes':'实际第二遍核准原作主体、阶段、关键构图、表情与全文；用户指定的连续前推转焦按其意图执行。','frame_adaptation':'16:9等比二维画幅；竖长原格通过明确摇移或短促展开经过必要节点，漫画不是生成首帧。','fields':dict(zip(['镜头设计','可见动作','可见背景','台词与语气','光影布光','声音设计'],[camera,action,bg,'\n'.join(lines) if lines else '无台词。',light,sound]))}
 if kind in ['action','mixed']:s['meaning_excerpt']=action
 if card:s['performance']={'card':card,'details':[action[:85]],'intervals':[{'speech_seconds':round(sum(b['seconds'] for b in p['bubbles']),2),'acting_seconds':duration,'concurrent':True}]}
 d['shots'].append(s);save(d)
if __name__=='__main__':init()
