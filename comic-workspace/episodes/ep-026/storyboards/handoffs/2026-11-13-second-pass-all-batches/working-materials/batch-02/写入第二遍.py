from pathlib import Path
from copy import deepcopy
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parent;P=R/'scene-ledger.json'
def load():return json.loads(P.read_text(encoding='utf-8'))
def save(d):P.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def init():
 d=load()
 if d['shots']:return
 rt=d['action_routes'][0]
 d['route_proposal_history']=[{'path':rt['path'],'sha256':rt['proposal_sha256'],'status':'用户纠正两处未接触，旧解释作废。'}]
 rt['path']=rt['path'].replace('25原文件；20_001实际有上下两格，冻结前拆分','25原文件；20_001已按真实上下两格拆成a/b，共26视觉节点')
 rt['path']=rt['path'].replace('粗壮手臂攻到她上身；青在极近接触中受压惊叫','粗壮手臂擦着青的胸部通过，没有击中；青后仰闪开后惊叫，并抓住从身旁掠过的腕臂').replace('喷流紧贴背侧擦过，再愤怒回骂。24_004保留背侧衣边附近的尖白擦掠形；拟按擦背侧／衣边的险避处理，不扩写正中躯干、重伤或额外能力。','喷流从青身旁通过，完全被她躲开，没有碰到身体或衣物；随后青愤怒回骂。24_004的尖白形只作高速掠过的图形与风压，不作为接触、沾染或新伤。').replace('青承受近身压力后抓腕的闭合过程','青闪开擦胸攻击后抓住掠过腕臂的闭合过程').replace('仍有接触细节需确认：19_003按上身被攻到／极近接触后抓腕处理；24_004按贴背侧／衣边擦掠的险避处理。','用户已明确：19_003擦着青的胸部过去，没有击中青；24_004没有碰到青，被完全躲开；其他路径没有问题。')
 rt['user_confirmation']={'quote':'19003擦着青的胸部过去，没有击中青，24004没有碰到青，被躲过去了，其他没问题。','sha256':None}
 rt['confirmation_status']='user_explained_corrected_path'
 rt['proposal_sha256']=None
 original=next(p for p in d['panels'] if p['image']=='第27話_20_001.jpg');i=d['panels'].index(original)
 im=Image.open(original['source_path']);(R/'sources').mkdir(exist_ok=True)
 obs=['青一只手的指端从上方扣住武士粗壮腕部的收束处，掌根贴实，腕臂斜穿画幅。','青双臂抬起抓住武士腕臂，武士身体横越她头上；青一腿屈起、另一腿下伸至斜向石铺面，长发甩成弧线。']
 parts=[]
 for tag,box,o in zip(['a','b'],[(0,0,1080,560),(0,690,1080,1409)],obs):
  f=f'第27話_20_001{tag}.jpg';out=R/'sources'/f;im.crop(box).save(out,quality=96)
  proxy=Image.open(out);proxy.thumbnail((1280,720));proxy.save(R.parent/'proxies'/'ep27'/f,quality=95)
  p=deepcopy(original);p.update(image=f,source_path=str(out),source_provenance={'original_image':original['image'],'original_path':original['source_path'],'crop_box':list(box),'note':'两个真实独立画格，中间白隙不作为新画格。'})
  p['first_pass']['observation']=o;parts.append(p)
 d['panels'][i:i+1]=parts
 j=rt['source_images'].index(original['image']);rt['source_images'][j:j+1]=[p['image'] for p in parts]
 for n,summary in [('19_003','依据用户解释：攻击擦过胸前，没有击中；青惊叫后抓住掠过的腕臂。'),('24_004','依据用户解释：喷流完全被青侧身躲开，没有碰到身体或衣物。')]:
  p=next(p for p in d['panels'] if p['image']==f'第27話_{n}.jpg');p['first_pass']['initial_action_understanding']=summary
  p['first_pass']['observation']=p['first_pass']['observation'].replace('紧贴／压到她胸前衣物附近，接触处','掠过她胸前衣物附近，近处').replace('尖白接触／擦掠形','尖白掠过形')
 d['stage']='second_pass_in_progress'
 d['initial_state']={'场景':'相接石铺平台与残墙、尘雾','青.武器':'空手','武士.形态':'巨大半实力形态','青.新伤':'无新增击中或沾染'}
 d['revision_audit'].append({'date':'2026-10-25','scope':'记录用户纠正并据此进入第二遍；20_001诚实拆为上下a/b。','quote':rt['user_confirmation']['quote']})
 save(d)

def add(n,duration,camera,action,background,light,sound,ja=(),tone='',kind='action',phase='process',node=None,meaning='',card=None,mode='continuity'):
 d=load();name=f'第27話_{n}.jpg';p=next(p for p in d['panels'] if p['image']==name)
 if any(name in s['source_images'] for s in d['shots']):raise ValueError('禁止重复写入'+name)
 assert len(ja)==len(p['bubbles']),(name,len(ja),len(p['bubbles']))
 target=f'片段1/分镜{len(d["shots"])+1}';t=.4;lines=[]
 for b,txt in zip(p['bubbles'],ja):
  sec=round(max(.6,sum(c not in '、。？！… ,.!?' for c in txt)/5.8+.2),2)
  b.update(script_text=txt,status='mapped',target=target,start=round(t,2),seconds=sec);t+=sec+.3
  typ={'inner':'（内心）','narration':'（旁白）'}.get(b['kind'],'')
  lines.append(f'{b["speaker"]}{typ}：“{txt}”（{tone}）')
 if ja:duration=max(duration,int((t+.5)*2)/2)
 p.update(viewed_at_drafting=True,drafting_resolution='720p',bubble_audit='pass',bubble_audit_notes='本次第二遍实际重新打开此格，逐泡核对原文、声音归属、类型与顺序，写日文等值译文。',composition_lock=p['first_pass']['observation'],source_facts={'entities':[p['first_pass']['observation']],'actions':[],'relations':[]},background={'mode':mode,'basis':'原格实际可见环境及当前统一配色；未画部分为导演补全。'},node_state=node or {},anchor_target=target,narrative_kind=kind,story_context=[meaning or p['first_pass']['initial_action_understanding']])
 if kind in ['mixed','action']:p['action_reading']={'summary':meaning or p['first_pass']['initial_action_understanding'],'phase':phase,'world_motion':meaning or p['first_pass']['initial_action_understanding'],'screen_motion':'实际向镜头逼近、横越或远离以本格构图及动作中明确路线为准；相机俯仰不变为身体运动。','grounding':'实际手脚接触／腾空按本格及相邻节点核对。','basis':'本次第二遍重看原图；19_003与24_004未击中／未碰到依据用户明确解释。'}
 flags=(['P'] if card else [])+(['D'] if len(ja)>1 else [])
 s={'target':target,'duration':duration,'role':'source_locked','source_images':[name],'purpose':meaning or p['first_pass']['initial_action_understanding'],'characters':['青','鬼头武士'] if n not in ['17_001','19_001','25_003','26_001','26_002'] else (['白色有尾小体群'] if n=='26_002' else []),'risk_flags':flags,'risk_basis':'人物意图、表情与动作持续关系需要规划。' if flags else '实景或图形节点。','anchor_phase':phase,'anchor_elements':p['composition_lock'],'anchor_state':node or {},'state_changes':node or {},'viewed_while_writing':True,'source_audit':'pass','source_audit_notes':'已实际二遍回图，保留主体、观察关系、动作阶段、关键表情与全部气泡。','frame_adaptation':'16:9等比动画画幅；竖格按所写摇镜展开，不把漫画作为首帧。','fields':dict(zip(['镜头设计','可见动作','可见背景','台词与语气','光影布光','声音设计'],[camera,action,background,'\n'.join(lines) if lines else '无台词。',light,sound]))}
 if kind in ['mixed','action']:s['meaning_excerpt']=action
 if card:s['performance']={'card':card,'details':[action[:85]],'intervals':[{'speech_seconds':round(sum(b['seconds'] for b in p['bubbles']),2),'acting_seconds':duration,'concurrent':True}]}
 d['shots'].append(s);save(d)

if __name__=='__main__':init()
