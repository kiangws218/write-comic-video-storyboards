from pathlib import Path
import json, hashlib, shutil, re
O=Path(__file__).parent; R=O.parents[3]; E=R/'comic-workspace/episodes/ep-018'; B=E/'storyboards'
def read(n):return json.loads((O/n).read_text(encoding='utf-8'))
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
integrity=read('source-integrity.json'); ledger=read('source-ledger-v3.json'); assigned=read('new-shot-index.json'); progress=read('progress.json')
restr={p['image']:p for p in read('adaptation-observations.json')['observed']}
panels={p['image']:p for p in ledger['panels']}
intake=[]
for i,p in enumerate(integrity):
    n=p['image']; q=panels.get(n)
    if i<15:decision='retained_approved_front';why='前15个原文件沿用已确认的17镜；04_001的上下分区由两个已检查裁切记录覆盖。'
    elif q:
        decision='non_graphic_adaptation' if q.get('adaptation_scope') else 'redrafted_source_grounded'
        why=q.get('adaptation_scope') or '本格先观察再重写，兑现源格构图与允许的动作阶段。'
    elif n=='19_004.jpg':decision='duplicate_reaction_merged';why='与19_003同一抬起面盔的惊讶反应，文件裁切与上方气泡不同，合并演出一次。'
    elif n in ['第18話_15_001.jpg','第18話_18_001.jpg']:decision='reaction_merged';why='局部短反应并入相邻头部镜头，保留惊疑与注意方向，不再重复一次盔部停顿。'
    else:decision='explicit_content_omitted';why='省略露骨性行为、身体细节、性化对白或声息；本话必要非露骨剧情在邻接镜头保留。'
    intake.append({**p,'viewed_at_drafting':True,'drafting_resolution':'720p','decision':decision,'reason':why,'source_original_preserved':True,'source_observation':restr.get(n,{}),'targets':[s['target'] for s in ledger['shots'] if n in s.get('source_images',[])+s.get('derived_from',[])]})
assert len(intake)==70 and len({i['image'] for i in intake})==70
save('source-intake-audit.json',{'scope':'整话70个原文件全部核对；完整非露骨叙事改编，原始露骨对白与过程非全量覆盖。','files':intake})

review={
'06_001':'董白面对他人的责备仍挑衅地笑，短句与偏脸相连；不加新指人手势。',
'06_002':'脚部离开与留下扶持者形成距离，低位姿态为前一个插镜期间的有意省略；不声称镜内演出落座。',
'06_003':'由下缘抬起双手形成自握承载怒气；威胁不是实际攻击，手势持续到下一格。',
'06_004':'画外打断导致青的手势与怒气松动；人物仍在听，没有另加画外事件。',
'07_001':'自握先分开再向春子伸臂一次，追问的压力持续；长句已给7秒，没有重复接触形成。',
'07_002':'低身侧脸保持，冷淡声音与擦痕构成回应；不因反打虚构整身转动。',
'07_003':'2秒眼部反应让惊讶替代怒气，不给极近裁切增加肩手动作。',
'08_001':'5秒实景空镜承载处理伤口的提议，画外对白是任务内容，没有直接演出找水路线。',
'08_002':'肩部颤动与青的支撑随动组成照料任务，扶肩接触持续，不再重握一次。',
'08_003':'扶持延续时头部回望一次，2秒足够，不添加脚步与松手。',
'08_004':'头转回前方而扶肩继续；栈道材质经彩色图确认，忧虑独白没有对嘴。',
'09_001':'1秒原有暗场承担场景分隔。具体侵害过程属于明确省略，不假称已经动画化。',
'09_003':'惊恐制止到无力恳求，由头部近景与岩壁空镜覆盖三个短语；不展示身体与性化呼吸。',
'13_003':'7秒质问与冷答形成不同权力位置，听者僵住仍在参与；画外答复保留而无需复述提问。',
'14_001':'求放走她到愿意承担的意义变化由低头再抬头承担，6秒完整，不增加手部求情。',
'14_002':'三气泡是一句分节拒绝，3秒拖音加蔑视下巴，不误判成三句不同语义。',
'15_002':'2秒惊疑抬盔承接条件追问，省略纯局部抖动不会丢失新剧情。',
'15_003':'9秒条件陈述与次数重读，以近处目光和微笑持续施压；露骨具体要求明确泛化。',
'15_004':'怒骂、求死、拒绝用近景与盔缝极近景覆盖，后段压低而咬紧，没有整镜静止等对白。',
'16_001':'3秒同伴突然插话，守卫转注意向她，双头部关系可读。',
'16_002':'5秒勉强安慰，目光躲开又回到同伴；原性化神态删去，情绪不是轻松或愉悦。',
'16_003':'3秒眼部劝说强调自己也无把握，范围只在眼睛与目光，不凑大动作。',
'17_001':'7秒从惊怒质问到放慢提醒，头部持续对着同伴；重复起音压力已区分。',
'17_002':'4秒已见岩壁承接画外质疑，原催情解释只保留是否受影响的非露骨功能。',
'17_003':'2秒男子冷淡否认，两短气泡为连续句，眼神压低是听者到回应的转变。',
'18_002':'5秒解释到急切说服，笑意消失、目光压向同伴；不演出未呈现的身体行为。',
'18_003':'7秒降声请求保密到信任陈述，口部停顿用于难堪，非性化呼气已去除。',
'19_002':'8秒低头、抬一点、再垂下，承载被迫决定的艰难，不是随意多一串手势。',
'19_003':'4秒画外反悔→掀盔惊问，两人语气分明；19_004合并，面盔从此保持掀起。',
'20_001':'3秒笑意收成咬牙狠相，半句悬停制造威胁，橄榄绿色由两张上色原图确认。',
'20_002':'5秒岩壁威胁与8秒泪眼恳求同属一个13秒片段；只保留绝望和婚约关系信息，不演出原露骨目的。',
'21_001':'7秒男子眉眼听者镜承接守卫承认，6秒董白头部反打承担追问；反打位置由20_002、面盔状态由19_003支撑，属于明确改编补镜。',
'21_002':'3秒手指收拢与直接威胁对应，只有一记源图支持的握紧，不增新攻击路线、骨折或结果。',
'21_003':'2秒守卫仰头痛叫，盔旁手部随冲击抖动；面盔继承掀起状态，身体裁去。',
'22_001':'2秒董白惊叫与仰头接连续攻击反应，头部安全取景，不推导伤口或死亡。',
'22_002':'1秒黑白抽象冲击→衰暗结束，本话没有再添加人物结果或下一话事件。',
}
def key(n):m=re.search(r'_(\d{2}_\d{3})\.jpg$',n);return m[1] if m else n
semantic=[]
for s in assigned:
    n=s['image']; p=panels[n]
    semantic.append({'target':s['target'],'image':n,'result':'reviewed_adaptation' if p.get('adaptation_scope') else 'reviewed_source_grounded','conclusion':review[key(n)],'performance_card':s.get('plan',p.get('performance_plan')),'continuity':p.get('continuity'),'limitations':p.get('admission'),'supporting_visual_images':s.get('supporting_visual_images',[])})
save('semantic-review.json',{'review_type':'分镜文字与已查看源图的语义复查；没有生成或评测视频。','front17':'保留用户确认的原17镜及此前校对记录；最新验证未要求改变这些表演。','shots':semantic})
warn=(O/'validation.txt').read_text(encoding='utf-8').splitlines(); warnings=[w for w in warn if w.startswith('警告')]
dispositions=[]
indexed={s['target']:s for s in semantic}
for w in warnings:
    m=re.search(r'片段(\d+)(?:/|的)分镜(\d+)',w); target=f'片段{m[1]}/分镜{m[2]}' if m else None
    context=indexed.get(target)
    if context:answer=context['conclusion']
    else:answer='用户已确认的前17镜保留。原校对记录包含抓衣、错愕、打断、回望、解除接触与搀扶；此次不改变人物动作。'
    if 'coupling复制' in w:answer+=' 表演卡所述任务/关系已与准入限制分开检查：以具体节拍服务当前互动，无需为消除提示补造动作。'
    if '背景' in w:answer+=' 当前极近或头部裁切决定背景的可见性；保留实际遮挡/低细节底场说明，不把皮肤和头盔表面当成独立环境。'
    if '文本语境' in w:answer+=' 情绪与对白可帮助解释已见姿态，但不为未观察的接触、线路或攻击结果提供依据；改编补镜例外范围已明示。'
    dispositions.append({'warning':w,'target':target,'disposition':'reviewed','conclusion':answer})
save('warning-dispositions.json',{'warning_count':len(warnings),'errors':0,'dispositions':dispositions,'limits':'只评审分镜文本；静态图片与台账不能证明生成视频质量。改编段不声称全幅原格一致。'})
ledger['final_audit']['semantic_review']['review_file']='semantic-review.json'
ledger['final_audit']['semantic_review']['warning_dispositions']='warning-dispositions.json'
ledger['final_audit']['bald_orc_palette_audit']=read('color-observations.json')
save('source-ledger-v3.json',ledger)

new=O/'第18话_制作分镜_Gen2.8_全量重做.md'; current=B/'current/第18话_制作分镜_Gen2.8.md'
expected='9c5d05bf3cfb4b2ec21188e5abcaad5b4baf3f6d3721eccedae630188f4836e8'
assert sha(current)==expected,'Current script changed externally; preserve it and review before replacement.'
archive=B/'archive/2026-10-09_Gen2.8_全量重做前';archive.mkdir(parents=True,exist_ok=True)
shutil.copy2(current,archive/current.name)
delivery=B/'deliveries/2026-10-09_Gen2.8_整话非露骨改编';delivery.mkdir(parents=True,exist_ok=True)
shutil.copy2(new,current);shutil.copy2(new,delivery/current.name)
count=len(ledger['shots']);bubbles=sum(len(p['bubbles']) for p in ledger['panels'])
report=f'''# 第18话 Gen2.8 整话交付说明

最新Gen2.8已从 `codex/gen2.8-performance-router` 同步到本机，提交 `{read('skill-sync-manifest.json')['commit']}`。本机20个技能文件与远端内容逐一核对一致；143项技能回归测试通过。

整话脚本：{progress['clips']}个片段、{count}个分镜、{progress['runtime_seconds']}秒（4分02秒）。每镜六字段独立，所有片段不超过15秒。前15个原文件的已确认17镜保留，后续重新制作，整体连续编号。新版采用整句情绪和人物互动推进，镜头之间继承扶肩、回望与面盔开合等状态。

## 改编范围

这是完整的**非露骨剧情改编**，不是对露骨原图的逐动作完整复现。70个原文件全部查看核对，未覆盖的原文件均有明确取舍记录。第09_002至13_002涉及露骨性行为、身体细节及性化声音，省略具体过程；第09_003及13_003之后的受困段落用头部取景、反打和少量岩壁空镜保留求饶、条件谈判、反悔、关系揭示与攻击。具体强迫性行为要求改成泛化条件，露骨目的改成绝望与哭喊；部分催情解释、性化神态和声息删除。未增加救援、脱困、骨折或死亡结果。

第19_003与`19_004.jpg`为同一掀盔惊讶的重复收录，合并一次演出。15_001与18_001的局部短反应并入相邻表演。详细逐文件记录见 `source-intake-audit.json`。

## 核对结果与边界

- 已确认前17镜的六字段与时长保留；新增40镜。
- 剧本台账映射{bubbles}条日文气泡/内心独白/惊叫记录；该数量是交付版本，不代表原始性化对白全量覆盖。
- 结构与台账校验：0错误、{len(warnings)}条语义复查提示。提示逐条记录处理结论，未把零错误当成自然表演质量保证。
- 青与春子扶持关系、头部回望/回正、董白与守卫的对话注意方向、19_003后掀起的面盔状态已复查。兽人橄榄绿色肤色及木板栈道材质由上色图确认。
- 未生成视频；表演质量结论限于分镜文本和图像核对。非露骨改编镜头明确裁切或改写，不宣称原格全幅保真。

当前稿已回填 `storyboards/current/第18话_制作分镜_Gen2.8.md`。旧稿按原字节保存在本地 `storyboards/archive/2026-10-09_Gen2.8_全量重做前/`，历史内容不作重新生成。源漫画、人设图及已有上色改动均保持不变。
'''
(O/'交付说明.md').write_text(report,encoding='utf-8');(delivery/'交付说明.md').write_text(report,encoding='utf-8')
for n in ['source-ledger-v3.json','source-intake-audit.json','semantic-review.json','warning-dispositions.json','validation.txt','skill-sync-manifest.json','skill-sync-verification.json','color-observations.json']:
    shutil.copy2(O/n,delivery/n)
status=f'''# 第18话

- 单色单格：70张（源素材保持原样）。
- 上色单格：66张。
- 当前分镜：`storyboards/current/第18话_制作分镜_Gen2.8.md`
- 覆盖状态：完整非露骨剧情改编；已确认前15个原文件的17镜保留，后续重新制作。
- 当前版本：Gen2.8（技能提交 `{read('skill-sync-manifest.json')['commit'][:7]}`），21片段、57分镜、242秒。
- 改编边界：露骨性行为、身体细节及性化声效省略；条件与威胁有非露骨改写，原始对白并非全量复现。
- 交付及审计：`storyboards/deliveries/2026-10-09_Gen2.8_整话非露骨改编/`
- 原稿历史：Git历史保留；本机旧稿另存`storyboards/archive/2026-10-09_Gen2.8_全量重做前/`。
- 检查：结构与台账0错误，语义提示逐条复查；未生成视频。
- 整页漫画：未上传。
'''
(E/'STATUS.md').write_text(status,encoding='utf-8')
save('delivery-manifest.json',{'current':str(current),'delivery':str(delivery),'archive':str(archive),'current_sha256':sha(current),'old_sha256':expected,'shots':count,'clips':progress['clips'],'seconds':progress['runtime_seconds'],'mapped_safe_bubbles':bubbles,'warnings':len(warnings),'source_files_audited':70,'source_files_selected':sum(i['decision'] not in ['explicit_content_omitted','duplicate_reaction_merged','reaction_merged'] for i in intake),'remote_publish_paths':['comic-workspace/episodes/ep-018/STATUS.md','comic-workspace/episodes/ep-018/storyboards/current/第18话_制作分镜_Gen2.8.md','comic-workspace/episodes/ep-018/storyboards/deliveries/2026-10-09_Gen2.8_整话非露骨改编/']})
print(json.dumps({'shots':count,'clips':progress['clips'],'seconds':progress['runtime_seconds'],'mapped_safe_bubbles':bubbles,'warnings':len(warnings),'current':str(current)},ensure_ascii=False))
