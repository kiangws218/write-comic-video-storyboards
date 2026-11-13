from pathlib import Path
from copy import deepcopy
import json, hashlib

ROOT=Path(__file__).resolve().parent
PATH=ROOT/'scene-ledger.json'
def load(): return json.loads(PATH.read_text(encoding='utf-8'))
def save(d): PATH.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

def initialise():
    d=load()
    if d['shots']: return
    route=d['action_routes'][0]
    d['route_proposal_history']=[{'id':route['id'],'path':route['path'],'sha256':route['proposal_sha256'],'result':'用户指出3、4、6需改，旧稿不得沿用。'}]
    route['path']=route['path'].replace('武士的刀切开后方砖石建筑','武士的刀切断青身后的烟囱').replace('青以单手在粗糙表面撑一下借力，继而脚触表面蹬离，回身抓住飞起的砖石大块并投向武士。世界动作是撑触→蹬转→抓石→掷石；倾斜画格不作为墙面绝对倾角依据。','青手掌贴住被切断的烟囱，调整身体与脚步发力，将断烟囱向前推砸向武士。世界动作是掌贴断烟囱→身体发力→前推砸出；不是抓石投掷，倾斜机位不变为世界坡度。').replace('武士以为投石容易破解','武士以为推来的断烟囱容易破解').replace('出刀斩裂石块','出刀斩裂断烟囱').replace('拟将弧线理解为武士被击退翻飞，青随后独立落地；弧线终端本身无法认人。','15_002的弧线是青的身影向后退去，随后承接滑退落地；这是用户对原作动作的明确解释，不作为图中已可独立认人的观察。').replace('投石由青近侧飞向远处武士','断烟囱由青近侧推砸向远处武士').replace('抓投石的受力','掌贴断烟囱的前推受力').replace('待确认的实际歧义：15_002远景轨迹拟归给被青击退的武士；粗糙借力面的具体材质不强认树干，按城内可衔接的屋面／碎建筑表面设计。','用户明确纠正：被斩断的是青身后的烟囱；青以手掌贴住断烟囱向前推砸；15_002为青的身影后退并衔接滑退落地。用户称15003的滑退落地在本目录对应紧接15_002之后的第26話_16_001.jpg，按画面及相邻次序定位。')
    route['confirmation_status']='user_explained_corrected_path'
    route['user_confirmation']={'quote':'3.青空中后翻后仰躲过斩击，然后斩击切断了身后的烟囱，4.青是手掌贴住被切断的烟囱，发力前推砸向武士。6. 15002是青的身影后退，接15003后滑落地','sha256':None,'scope':'用户针对整批提案指出三处修正；以用户直接解释覆盖修正动作路径，未改处保持原提案。'}
    d['stage']='second_pass_in_progress'
    d['initial_state']={'场景':'城内屋顶及相接石铺空地','青.武器':'空手','武士.形态':'人形','武士.刀':'肩后鞘内'}
    d['look']={'environment':'清晨／日间阴云下的石砌城镇；灰米砖墙、蓝灰瓦屋面与灰绿不规则石铺地；烟囱断面米灰、内腔深褐；烟尘偏米灰；远景树冠灰绿。环境颜色为统一生产设计。','light':'破烟囱后侧的开阔天空为主要柔光，浅冷白；背离烟囱的空地敞口提供较弱中性补光。机位变化按稳定参照换算画面来光侧。','style':'高品质二维手绘、赛璐璐人物与有笔触的建筑；关键爆发用清楚强姿态、短促残影与紧凑接触，不持续乱震。'}
    d['revision_audit'].append({'date':'2026-10-25','scope':'按用户解释纠正烟囱、掌推与青后退的动作理解；当前源文尚未冻结。','user_quote':route['user_confirmation']['quote']})
    save(d)

def add(suffix, seconds, camera, action, background, light, sound, japanese=(), tone='自然发声，按句意停连。', phase='process', kind='action', node=None, meaning=None, pcard=None, background_mode='continuity', update=None, audit='第二遍重新打开本格核对构图、主体、动作阶段及气泡。'):
    d=load(); filename=f'第26話_{suffix}.jpg'
    panel=next(p for p in d['panels'] if p['image']==filename)
    if any(filename in s['source_images'] for s in d['shots']): raise ValueError('已写镜头，不得重复初始化：'+filename)
    if update:
        for key,value in update.items(): panel[key]=value
    if len(japanese)!=len(panel['bubbles']): raise ValueError((filename,len(japanese),len(panel['bubbles'])))
    target=f'片段1/分镜{len(d["shots"])+1}'
    utter=[]; t=.4
    for b,ja in zip(panel['bubbles'],japanese):
        b.update(script_text=ja,status='mapped',target=target,start=round(t,2))
        speech=round(max(.5,sum(1 for c in ja if c not in '、。！？…「」 ,.!?')/5.8),2)
        b['seconds']=speech; t+=speech+.25
        label={'inner':'（内心）','narration':'（旁白）'}.get(b['kind'],'')
        if b['speaker'] not in ['青','鬼头武士','青梅女'] or (suffix=='16_002'): label=label or '（画外音）'
        utter.append(f'{b["speaker"]}{label}：“{ja}”（{tone}）')
    # 基本串行／并行计时在第二遍保留，精确切分与最终片段在第三轮处理。
    if t>seconds-.3 and japanese: seconds=((t+.5)*2//1)/2
    panel.update(viewed_at_drafting=True,drafting_resolution='720p',bubble_audit=audit,composition_lock=panel['first_pass']['observation'],narrative_kind=kind,
        source_facts={'entities':[panel['first_pass']['observation']],'actions':[],'relations':[]},
        background={'mode':background_mode,'basis':'当前原格可见内容与本场统一配色；未画部分为动画场景补全。'},
        node_state=node or {},anchor_target=target,
        story_context=[meaning or panel['first_pass']['initial_action_understanding']])
    if kind in ['action','mixed']:
        panel['action_reading']={'summary':meaning or panel['first_pass']['initial_action_understanding'],'phase':phase,'world_motion':meaning or panel['first_pass']['initial_action_understanding'],'screen_motion':'见本格构图与镜头中明确的相对运动；机位变化不代表世界位移。','grounding':'接触／离地按本格可见脚手及邻格因果记录','basis':'本次第二遍原图重看；烟囱掌推与15_002青后退依据用户明确解释。'}
    shot={'target':target,'duration':seconds,'role':'source_locked','source_images':[filename],'purpose':meaning or panel['first_pass']['initial_action_understanding'],'characters':list(dict.fromkeys([b['speaker'] for b in panel['bubbles']]+(['青','鬼头武士'] if suffix not in ['08_003','09_001','09_002','09_003','13_003'] else []))),
        'risk_flags':['P'] if pcard else [],'risk_basis':'人物的表情、主姿态及任务变化需实际演出。' if pcard else '环境或动作图形节点。',
        'anchor_phase':phase,'anchor_elements':[panel['composition_lock']],'anchor_state':node or {},'state_changes':node or {},
        'viewed_while_writing':True,'source_audit':{'status':'pass','notes':audit},
        'frame_adaptation':'16:9动画画幅；保留原格的观察关系与视觉重点，按所写连续运镜展开竖向内容。原格仅作过程节点参考。',
        'fields':{'镜头设计':camera,'可见动作':action,'可见背景':background,'台词与语气':'\n'.join(utter) if utter else '无台词。','光影布光':light,'声音设计':sound}}
    if kind in ['action','mixed']: shot['meaning_excerpt']=action
    if pcard:
        shot['performance']={'card':pcard,'details':[action], 'intervals':[{'speech_seconds':round(sum(b['seconds'] for b in panel['bubbles']),2),'acting_seconds':seconds,'concurrent':True}]}
    d['shots'].append(shot); save(d)

if __name__=='__main__': initialise()
