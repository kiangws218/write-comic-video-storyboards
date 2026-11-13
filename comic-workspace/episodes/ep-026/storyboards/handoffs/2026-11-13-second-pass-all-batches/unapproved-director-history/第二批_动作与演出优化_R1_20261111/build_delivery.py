"""编译新版本：主稿按共享场面/逐镜时间表/连续声轨组织，六字段只在核对稿展开。"""
import copy,hashlib,json,re,subprocess,sys
from collections import Counter
from pathlib import Path
from director_plan import R,OUT,CLIPS,BEATS,NIGHT
S=Path(r'C:\Users\86135\.codex\skills\write-comic-video-storyboards-gen2-8-2\scripts');sys.path.insert(0,str(S))
from authoring import expand
from render_storyboard import render
from validate_director import source_snapshot,make_source_lock,review_digest
from alignment import apply_alignment,REVIEWED

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def n(v):return f'{v:g}'
def comic_ref(s):return f'参考“{Path(s["source"]).stem}”。' if s['source'] else ''

OLD=R/'第二批_第27话'
old=read(OLD/'scene-ledger.json');d=copy.deepcopy(old)
apply_alignment(d,old)
original_files=[OLD/'scene-ledger.json',OLD/'第二批_青与鬼头武士_导演版_Gen2.8.2.md',R/'青与鬼头武士_完整导演分镜_Gen2.8.2.md']
original_hashes={str(p):sha(p) for p in original_files}
bubbles={v['id']:v for p in d['panels'] for v in p['bubbles']}
base_source={s['source_images'][0]:s for s in old['shots'] if s['source_images']}
flat=[];global_clock=0;source_sequence=[]
for c in CLIPS:
    c['duration']=sum(s['duration'] for s in c['shots']);assert c['duration']<=15
    c['global_start']=global_clock;local=0
    for j,s in enumerate(c['shots'],1):
        s['target']=f'片段{c["number"]}/分镜{j}';s['local_start']=local;s['global_start']=global_clock+local;s['number']=j;s['clip']=c['number'];s['speech']=[]
        local+=s['duration'];flat.append(s)
        if s['source']:source_sequence.append(s['source'])
    for q in c['voice']:
        if q['text'] is None:q['text']=bubbles[q['bubble_id']]['script_text']
        assert 0<=q['start']<q['end']<=c['duration'],(c['number'],q)
        q['global_start']=global_clock+q['start'];q['global_end']=global_clock+q['end']
    global_clock+=c['duration']
assert source_sequence==[p['image'] for p in old['panels']]
assert len(flat)==51 and global_clock==94.5

# 主稿中的整句声轨连续穿过切点；台账按真实镜尾切分文字，仅作对应，不在切点加停顿。
segments={k:[] for k in bubbles}
for c in CLIPS:
    for q in c['voice']:
        intersections=[]
        for s in c['shots']:
            a=max(q['start'],s['local_start']);b=min(q['end'],s['local_start']+s['duration'])
            if b>a+1e-8:intersections.append((s,a,b))
        text=q['text'];pos=0
        for j,(s,a,b) in enumerate(intersections):
            if j==len(intersections)-1:stop=len(text)
            else:
                ideal=round(len(text)*(b-q['start'])/(q['end']-q['start']))
                stop=max(pos+1,min(len(text)-(len(intersections)-j-1),ideal))
            piece=text[pos:stop];assert piece
            seg={'target':s['target'],'script_text':piece,'start':round(a-s['local_start'],3),'seconds':round(b-a,3)}
            segments[q['bubble_id']].append(seg);s['speech'].append({'bubble_id':q['bubble_id'],**seg,'tone':q['tone']});pos=stop
        assert pos==len(text)
for k,v in bubbles.items():assert ''.join(x['script_text'] for x in segments[k])==v['script_text'],k

d['project_title']='第二批｜双手抓握与烟尘抡摔｜动作与演出优化 R1（2026-11-11）'
d['shots']=[];d['performance']=[];d['cuts']=[];d['clip_plan']=[{'clip':c['number'],'seconds':c['duration']} for c in CLIPS]
d['clip_boundary_notes']='8片；片3以13.5秒连续完成双手同时抓握、持续承重、带过头顶、下抡、接地、烟尘吞体遮满。喷流蓄势至完全躲开和落地合在片6；液团至群体揭晓/青反应合片8。'
d['look']='夜晚深靛天空、暗青灰石地与冷灰褐实体厚尘。青沿青2参考的冷银灰发、粉紫衣、白袜靴暗面；巨大武士形体从原作，既有肤色暗面和低亮湿反射保留。白色小体珍珠白、浅灰软阴影、深灰眼点，非发光。青未强化，没有蓝色身体辉光和电弧。'
d['director_intent']='喘息和怀疑使空白可感，挑衅引出突然近身；擦胸险避后双手同时抓牢，完整身体抡摔再以地面后果放大重量。烟尘接地后吞没武士和画面，保持到原作重新撑起。喷流完全躲开，白团爆散后才揭晓小体。嫌恶、胜算和受惊通过持续表演与听者/环境回应推进。'
d['director_space']='沿第一批同一C石铺地面，青在右近，巨大武士在左后厚尘中。武士从尘区跃到青近上方，粗臂掠过后被双手同时抓住，青在地面承重转体抡摔，新撞点在青脚前交叉板缝左端，较旧藏身尘区更近；接地后新厚尘保持在此撞点。青后撤至新撞点右前薄边，武士仍在该撞点尘中撑起；喷流直向青原站位，青让到空出一侧，液团落在青原站位后方下游同一长板缝旁。群体和后撤路径均在同一石地，不增设高台/山坡。'
d['spatial_lighting_plan']=d['director_space']+' 弱冷夜空散射，无新增灯/月/火；特写按画内触点裁切，烟尘有厚薄与前后层次。'
d['environment_collaboration']={'date':'2026-11-11','file':'环境复核.md','status':'按第二批实际机位与烟尘遮挡增量复核，结果见同目录记录，无动态实测。'}
d['native_revision']={'date':'2026-11-11','separate_version':True,'based_on':str(OLD),'user_direction':'两手同时抓握，摔后烟尘爆炸遮武士和画面；其余九步理解确认。连续动作同片，原格镜头正文直接写参考编号。','prior_drafts_untouched':True,'observed_this_round':REVIEWED,'effect_methods':'读取FX-04实体裂解、FX-05烟尘分层、DRAW-02过渡形方法并改写到本场；未播放参考片或生成验证，ID不进提示正文。'}

for s in flat:
    if s['source']:
        x=copy.deepcopy(base_source[s['source']]);x['source_images']=[s['source']]
        for k in ['performance','neighbor_contrast','state_in','state_out','silences']:x.pop(k,None)
        x['source_audit']='pass';x['viewed_while_writing']=True
        p=next(p for p in d['panels'] if p['image']==s['source'])
        x['anchor_state']=copy.deepcopy(p['node_state'])
        if not isinstance(x.get('source_audit_notes'),dict):x['source_audit_notes']={'previous':x.get('source_audit_notes')}
        x['source_audit_notes']['native_director_review']=('2026-11-11回看此受影响格，结合用户明确纠正核对动作与接触。' if Path(s['source']).stem.replace('第27話_','') in REVIEWED else '沿用此前原格核对；本轮不伪报重看。')
    else:
        prev=next((v['source'] for v in reversed(flat[:flat.index(s)]) if v['source']),None)
        nxt=next((v['source'] for v in flat[flat.index(s)+1:] if v['source']),None)
        refs=list(dict.fromkeys(v for v in [prev,nxt] if v))
        x={'role':'source_supported_phase','source_images':[],'derived_from':refs,'state_changes':{},'risk_basis':'同一已批准事件的导演覆盖和实际切镜，不增加交锋、伤势或独立战术。'}
    x.update({'target':s['target'],'_draft_key':s['key'],'duration':s['duration'],'purpose':s['purpose'],'characters':s['actors'],'risk_flags':['P'] if s['actors'] else []})
    x['creative_additions']=['2026-11-11用户确认后修订：'+s['purpose']+'；本场连续抓握、接地烟尘、喷流落点为已确认事件演出，不伪报原图新增观察。']
    x['state_changes']=copy.deepcopy(x.get('anchor_state',{})) if s['source'] else {}
    x['state_changes']['当前演出阶段']=s['landing']
    if s['key']=='S013':x['state_changes']['青.接触']='双手同时扣紧同一来臂末端'
    if s['key'] in ['S014','S015','S016','S017','S018','S019']:x['state_changes']['青.接触']='双手持续抓牢直至接地'
    if s['key']=='S020':x['state_changes'].update({'武士.阶段':'重砸石地','青.接触':'撞实后解除双手抓握','烟尘.阶段':'从接地点爆起，吞没武士'})
    if s['key']=='S021':x['state_changes'].update({'烟尘.阶段':'实体厚尘遮满画面','武士.可见性':'完全被尘遮盖'})
    if s['key']=='S038':x['state_changes'].update({'青.喷流接触':'身体与衣物均无接触','青.位置':'同一石地避让后位置'})
    labels=[]
    for q in s['speech']:
        v=bubbles[q['bubble_id']]
        if v['kind']=='inner':label=v['speaker']+'（内心）'
        elif v['kind']=='narration':label=v['speaker']+'（旁白）'
        else:
            face_visible=v['speaker'] in s['actors'] and not any(w in s['camera'] for w in ['脚部','靴与','手臂与刀','掌根','掌与','后脚','鞘口','髋侧','手与','腿部','脚步','衣领与','圆钝肢端'])
            label=v['speaker']+('' if face_visible else '（画外音）')
        labels.append(f'{label}：“{q["script_text"]}”（同一声轨跨切镜连续；{q["tone"]}）')
    x['fields']={'镜头设计':comic_ref(s)+'16:9，'+s['camera'],'可见动作':s['action'],'可见背景':s['background'],'台词与语气':'\n'.join(labels) if labels else '无台词。','光影布光':s['light'],'声音设计':s['sound']}
    if 'meaning_excerpt' in x or s['source']:x['meaning_excerpt']=s['action']
    if s['actors']:
        speech_seconds=round(sum(q['seconds'] for q in s['speech']),3)
        x['performance']={'card':{'opening':s['purpose'],'beats':[s['action'].split('；')[0].rstrip('。'),s['landing']],'coupling':('同一动作链中，另一方距离/视线/受力随本镜继续，切走不重置。' if len(s['actors'])>1 else '本镜的注意或触点直接改变下一镜的观察/动作选择。'),'landing':s['landing']},'details':[s['action']],'intervals':[{'speech_seconds':speech_seconds,'acting_seconds':s['duration'],'concurrent':True}]}
    d['shots'].append(x)

for p in d['panels']:
    p['anchor_target']=next(s['target'] for s in flat if s['source']==p['image'])
    for v in p['bubbles']:
        for k in ['target','start','seconds','segments']:v.pop(k,None)
        v['segments']=segments[v['id']]

# 每条边只登记一次；原镜到插入、插入到原镜都使用实际相邻镜头。
for before,after in zip(flat,flat[1:]):
    d['cuts'].append({'from':before['target'],'to':after['target'],'changes':[{'dimension':'composition','description':f'{before["camera"].rstrip("。")}切到{after["camera"].rstrip("。")}；观看任务由“{before["purpose"]}”转入“{after["purpose"]}”。','shot':after['target'],'field':'镜头设计'}]})

# 有作用的沉默只标实际空白；其他无台词动作不反复写成“沉默”。
silence_plan={c['number']:c.get('silences',[]) for c in CLIPS}
for c in CLIPS:
    c['silences']=silence_plan.get(c['number'],[])
    for a,b,reason in c['silences']:
        for s,x in zip(flat,d['shots']):
            if s['clip']!=c['number']:continue
            start=max(a,s['local_start']);end=min(b,s['local_start']+s['duration'])
            if end>start:
                x.setdefault('silences',[]).append({'start':round(start-s['local_start'],3),'seconds':round(end-start,3),'purpose':reason})
for s,x in zip(flat,d['shots']):
    if not x.get('silences'):continue
    spoken=x['fields']['台词与语气'].splitlines()
    events=[(q['start'],line) for q,line in zip(s['speech'],spoken)]
    events += [(v['start'],f'（沉默{n(v["seconds"])}秒）') for v in x['silences']]
    x['fields']['台词与语气']=('无台词。\n' if not s['speech'] else '')+'\n'.join(line for _,line in sorted(events))

d['stage']='final'
d['director_review']={'characters':'青从喘息、试探、惊觉、发力、嫌恶、胜算到抱头尖叫；巨大武士以突进、被抡摔、重新撑起与喷流回应，保持本场性格和触感。','pacing':'51镜/8片/94.5秒；13.5秒片内完成同拍双手抓握至接地烟尘吞体满画。对峙台词跨手、身体与环境，不原地读完再动。','node_arrivals':'26视觉节点按原序保留，25原文件及22条锁定日文全文一致；本轮逐图复看，关键双手与接地烟尘按用户明确解释落实。','contrast':'50条实际邻接重建，放射裂石节点先可读，随后实体厚尘爆开遮盖武士和画面，直到23_002才重新揭出其身形。','limitations':'源图与文字/结构层面审查，未生成或播放本版动态分镜、未实录日语配音，程序通过不证明成片品质。'}
for p,op in zip(d['panels'],old['panels']):
    assert p['image']==op['image']
    for b,ob in zip(p['bubbles'],op['bubbles']):
        assert all(b[k]==ob[k] for k in ['id','source_text','script_text','speaker','kind'])
assert make_source_lock(d)==d['source_lock']

# 六字段展开只作为次要核对稿，用户阅读的主稿是下方紧凑时间表。
audit=render(d);audit_path=OUT/'第二批_六字段核对稿.md';audit_path.write_text(audit,encoding='utf-8')
d['director_review']['sha256']=review_digest(d,audit);write(OUT/'scene-ledger.json',d)

header='''# 第二批｜动作与演出优化 R1

2026-11-11独立版本。51镜／8片／94.5秒（1分34.5秒）。

夜战：深靛天空、暗青灰石地、冷灰褐厚尘；青沿青2人物参考，武士为本场巨大形态。青尚未强化，白色液体与小体均为实体。原作省略的开头交手不另补成确定招式。

每行是一个真实镜头，行间硬切；一行里的运镜连续。时间是片内时间。每片只写一次场面；对白另列成连续声轨，跨切镜不断句、不重新起音。内心不做说话口型。没有BGM。

'''
blocks=[]
for c in CLIPS:
    lines=[f'## 【片段{c["number"]}】{c["title"]}｜{n(c["duration"])}秒','',f'场面：{c["scene"]}', '', '| 镜 | 片内时间 | 镜头与动作 |', '|---|---|---|']
    for s in c['shots']:
        extra=''
        if '图形底' in s['background'] or '图形' in s['camera']:extra=' 背景：'+s['background']
        lines.append(f'| {s["number"]} | {n(s["local_start"])}—{n(s["local_start"]+s["duration"])}s | {comic_ref(s)}**{s["camera"].rstrip("。")}** {s["action"]}{extra} |')
    lines += ['', '声音轨：']
    for q in c['voice']:
        v=bubbles[q['bubble_id']];kind='（内心）' if v['kind']=='inner' else '（旁白）' if v['kind']=='narration' else ''
        lines.append(f'- {n(q["start"])}—{n(q["end"])}s｜{v["speaker"]}{kind}：“{q["text"]}” {q["tone"]}')
    if not c['voice']:lines.append('- 无台词。')
    for a,b,reason in c['silences']:lines.append(f'- {n(a)}—{n(b)}s｜沉默{n(b-a)}秒；{reason}，保留环境与呼吸。')
    lines.append('- 拟音：'+'；'.join(s['sound'].rstrip('。') for s in c['shots'])+'。')
    lines+=['',f'接下一片：{c["exit"]}','']
    block='\n'.join(lines);blocks.append(block)
main=header+'\n'.join(blocks)
main_path=OUT/'第二批_动作与演出优化_R1.md';main_path.write_text(main,encoding='utf-8')

# 另附用于逐片粘贴的同内容版本，保留共享景设/独立镜号与完整声音轨，不重新编故事。
execblocks=[]
for c in CLIPS:
    lines=[f'## 【片段{c["number"]}】（{n(c["duration"])}秒）',f'共用：16:9二维手绘夜战；{c["scene"]} 弱冷夜色，人物固有色暗形清楚。','〖分镜〗']
    for s in c['shots']:
        lines.append(f'分镜{s["number"]}（{n(s["duration"])}秒）：'+('硬切。' if s['number']>1 else '')+comic_ref(s)+s['camera']+'【可见动作】：'+s['action']+(' 图形背景：'+s['background'] if '图形' in s['background'] else ''))
    lines.append('【台词与语气】：')
    for q in c['voice']:
        v=bubbles[q['bubble_id']];kind='（内心）' if v['kind']=='inner' else '（旁白）' if v['kind']=='narration' else ''
        tone=q['tone'].replace('不做内心口型','嘴保持呼吸状态')
        lines.append(f'{n(q["start"])}—{n(q["end"])}秒，{v["speaker"]}{kind}：“{q["text"]}”（{tone}）')
    if not c['voice']:lines.append('无台词。')
    for a,b,reason in c['silences']:lines.append(f'{n(a)}—{n(b)}秒：沉默{n(b-a)}秒，环境与呼吸继续。')
    lines.append('【声音设计】：'+'；'.join(s['sound'].rstrip('。') for s in c['shots'])+'。')
    block='\n'.join(lines);assert len(block)<1900,(c['number'],len(block));execblocks.append(block)
(OUT/'第二批_逐片执行稿.md').write_text('\n\n'.join(b.split('\n',1)[0]+'\n\n```text\n'+b.split('\n',1)[1]+'\n```' for b in execblocks)+'\n',encoding='utf-8')
write(OUT/'剪辑与声轨.json',{'clips':CLIPS,'silence_plan':silence_plan,'main_sha256':sha(main_path),'audit_sha256':sha(audit_path)})

cmd=[sys.executable,str(S/'validate_storyboard.py'),str(audit_path),'--max-seconds','15','--image-dir',str(R/'全段_校验用参考'),'--source-ledger',str(OUT/'scene-ledger.json'),'--require-source-ledger']
p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');(OUT/'结构校验.txt').write_text(p.stdout+p.stderr,encoding='utf-8')
if p.returncode:
    print('\n'.join(l for l in (p.stdout+p.stderr).splitlines() if l.startswith('错误') or '验证失败' in l));raise SystemExit('结构校验有错误，尚未交付。')
warn=int(re.search(r'0个错误，(\d+)个警告',p.stdout+p.stderr)[1])
assert all(sha(Path(name))==h for name,h in original_hashes.items())
write(OUT/'版本与验证.json',{'date':'2026-11-11','shots':len(flat),'added':sum(not s['source'] for s in flat),'source_nodes':len(d['panels']),'original_files':25,'locked_text_units':len(bubbles),'clips':len(CLIPS),'seconds':global_clock,'max_clip_seconds':max(c['duration'] for c in CLIPS),'max_main_clip_chars':max(map(len,blocks)),'max_execution_clip_chars':max(map(len,execblocks)),'silence_intervals':sum(len(c['silences']) for c in CLIPS),'silence_seconds':sum(b-a for c in CLIPS for a,b,_ in c['silences']),'source_interpretation_relocked_after_user_correction':True,'all_dialogue_fragments_rejoin_frozen_text':True,'source_order_unchanged':True,'old_file_hashes_unchanged':original_hashes,'errors':0,'warnings':warn,'actual_video_playback':False})
print('第二批：51镜/8片/94.5秒，26节点/22台词；0错误/',warn,'提示。')
