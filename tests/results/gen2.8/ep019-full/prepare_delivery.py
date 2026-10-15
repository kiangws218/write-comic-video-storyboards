from authoring import *
import subprocess,sys,re,shutil,hashlib,zipfile
R=O.parents[3]; S=Path('C:/Users/86135/.codex/skills/write-comic-video-storyboards-gen2-8')
E=R/'comic-workspace/episodes/ep-019'; D=E/'storyboards/deliveries/2026-10-10_Gen2.8_整话'; C=E/'storyboards/current'
for n,k,u in [(6,'第19話_06_003.jpg',dict(new_clip=True)),(26,'第19話_26_002.jpg',dict(new_clip=True)),(24,'第19話_24_001.jpg',dict(scene='洞窟入口'))]:
    p=O/'drafts'/f'{n:02}.json';rows=json.loads(p.read_text(encoding='utf-8'))
    for row in rows:
        if row['image']==k:row.update(u)
    p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=O/'drafts/22.json';rows=json.loads(p.read_text(encoding='utf-8'));rows[-1]['fields'][3]='春子说：“動くな。喉を切るのに、一秒もかからない。”（第一句短促制止，第二句低、坚定，把威胁说清。）';p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=O/'drafts/03.json';rows=json.loads(p.read_text(encoding='utf-8'));rows[0]['fields'][5]='洞窟底声；两次下落的短气流擦声，接两声低闷落地声，余响短促。';p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
subprocess.run([sys.executable,'-X','utf8',str(O/'compile_episode.py'),'--validate'],check=True)
ledger=json.loads((O/'source-ledger-v3.json').read_text(encoding='utf-8')); shots=json.loads((O/'new-shot-index.json').read_text(encoding='utf-8')); progress=json.loads((O/'progress.json').read_text(encoding='utf-8'))
for p in ledger['panels']:
    if p['image']=='第19話_07_002.jpg':p['page_overlays'] += [dict(kind='caption',source_text='魔族斩铁团37期',render=False),dict(kind='caption',source_text='董白（20）',render=False)]
assert len(ledger['panels'])==75 and progress['inspected_panels']==75
by_target={s['target']:s for s in shots}
V={
'02_003':'5秒内飞溅结果先出现，男子随后低头困惑发问；没有重演斩击或补认断端为手臂。',
'03_003':'7秒解释期间，左前董白站姿从容，右后男子转向声音；裁切不允许董白脸入画，衣摆随动承担局部参与。',
'04_002':'轻松笑容与两句走运/日期疑问共同支持好奇；微抬脸和腰侧持态可见，不补隐藏动机或救人手势。',
'04_003':'盔面6秒从急喘到抬头确认获救，另6秒岩壁承接画外求助；省略裸体后仍保留先松气后催促的情绪次序。',
'05_002':'背面头部偏向前方、手从失稳到松开，跟随冒犯的两句打量；不切女性身体特写，不补伸手接触。',
'06_002':'警告到讥讽的转折由嘴角与握柄握实承接；9秒是两句日文和行动并行，没有每词强配手势。',
'07_002':'抬眼侧身继承出鞘后的双手状态，刀在肩后、鞘在近手；轻松威胁有笑容、站姿与对白支撑。',
'08_003':'青回头吃惊后否认，笑来不及收且手捏布；春子背影仍参与听，未编造她未见的脸部表情。',
'09_001':'10秒憋笑解释中肩与握布任务持续，夸赞时笑意再次浮出；随后独立握布近景接春子冷答，指松收束同一任务。',
'09_004':'双人同框承接青的两项自责，视线与肩头逐渐降低，春子安静听完；敷料为当前源图状态，不补医疗过程。',
'10_001':'9秒从自责到担忧，侧脸抬眼后说不下去，停在条件句等待回应；不靠无关摆手填满对白。',
'10_002':'春子冷淡讲黑色玩笑并追问能否哭，脸上不笑而等回答；没有把台词中的死亡变成实际葬礼。',
'10_003':'青转肩气急、攥布，春子背面短问；后续握布视角让偷窃解释独立落点，保持青未能立即回应的焦虑。',
'11_001':'结巴首句、强调生命、末句委屈已在语气栏分开；可见肩头绷起与头降低承接争辩，不要求额外重复手势。',
'11_002':'春子先截争论，另岩壁空镜说出对董白能力的判断；短停用于结束争论。辱称强度保留，未编造董白战斗画面。',
'12_001':'来者从容招呼和青半句迟疑是同一构图内的短交接；她仰头辨认而帽内不露脸，结巴与后段停顿已明确。',
'12_002':'短回想用已给商人问题与青的短反问辨认声音，左侧条板物不强称武器；双声短交接无需隐藏反打。',
'13_001':'9秒商人旧日说明由帽旁手指与肩部呼吸参与；面罩仅此回想可见，不反填当前暗帽内的五官。',
'13_002':'认出熟人先惊叫再确认，眼与右下手抬起支持惊喜；未新增握手或拥抱。',
'13_003':'春子提问调侃留双人关系镜头，青的完整澄清转为空物件视角，避免多完整句压进同镜或重复制图。',
'14_001':'画外青说明入行缘由，画内春子眼稍偏后哼一声；一段说明与简短回应可在反应近景完成，不把青画入。',
'14_002':'重新建立来者背面与青正面站位，意外问候接热情猜测；双人全景读出态度差，未补站起或靠近路线。',
'15_003':'两项画外疑问夹春子无声省略号，半垂眼皱起支撑疑惑；“骑士？”保留问句，不作为身份结论。',
'16_001':'复合原文件的上格空景和下格双人各作一镜；认地点、猜密道、短否定按顺序，全单元10秒不碎成独立片段。',
'16_002':'8秒有意保持背影等待，袍料呼吸与缓推聚焦未进行的下一步；镜头末明确稳定在背影和岩脚薄雾全景，未填新机关事件。',
'18_001':'一次爆光触发青护脸和画外春子短问，4秒内同一突发事件可承载；弧光、亮粒、发衣推移与短峰衰减同向。',
'18_002':'闭眼护脸到睁眼降臂只需3秒，嘴张汗点与前格爆光支持震惊；标点是无声反应，不伪造说话。',
'19_001':'5秒通道由峰值收成圆形、旋纹变稳、亮粒流动与来者短说明并行；内部保持白光，不新增北方风景。',
'19_002':'青侧脸从结巴感叹到求证，眼仍圆且注意未移；7秒为两项自然日文，未以机械微动作凑时。',
'19_003':'眉眼源图收紧及后格前冲支持警觉，嘴裁出故台词画外；不凭否定词新增手或刀动作。',
'20_001':'3秒前冲跟随手到左下，末明确跟拍收稳；手掠水、发刃随动由原尺寸核对，后侧握法不补，未增加命中。',
'22_004':'压制是漫画提供的结果，不补击倒手法；同一春子的制止和割喉威胁合为一段6秒，握刀与屈腿稳持读出控制，不产生刀伤。',
'23_002':'跑近后停步与喘气继承水花，近手抬而未接触；结巴追问反映冲突不明，不加扯刀或拉人。',
'23_003':'6秒推断由稳定眼眉与头肩支撑，压制在画外延续；不因战争论述生成新的战场。',
'25_002':'低头汗点及喘息支撑吃力评估，握柄在下巴旁持续准备；刘海盖眼不补眼神，背景只留岩壁。',
'25_003':'8秒盔面偏左与呼吸承接急问和再生说明，深景深保留守卫、董白、巨型兽人的三层关系；再生不直接转成未给动作。',
'26_001':'头脸中迟疑补充、汗点与张口支持不安，结巴与末停已注明；胸部从派生镜头退出，未强化裸体或性化声音。',
'26_003':'一次抽刀后的细刃、呼气与发束落稳支持继续备战；受困者画外说明武器规则，不补多次抽刀或独立缩刀效果。'
}
warnings=[l for l in (O/'validation.txt').read_text(encoding='utf-8').splitlines() if l.startswith('警告')]
review=[]
for w in warnings:
    targets=[a+'/'+b for a,b in re.findall(r'(片段\d+)(?:/|的)(分镜\d+)',w)]
    if targets:
        scope=[by_target[t]['image'] for t in targets]; decisions=[]
        for im in scope:
            key=im[5:11];assert key in V,(w,key);decisions.append(V[key])
        review.append(dict(warning=w,targets=targets,images=scope,decision='文字与对应源图核对后保留或已修订',reason='；'.join(dict.fromkeys(decisions))))
    elif '跨格合并' in w:
        review.append(dict(warning=w,decision='按实际场景边界判断',reason='黑灰过场已并入入口对峙末片；之后切回董白洞窟线，存在真实叙事/场景断点，不以时长候选把两线合成同一场面。'))
    elif '缺少焦段、景深、焦点或空间透视' in w:
        review.append(dict(warning=w,images=['第19話_16_002.jpg','第19話_20_001.jpg','第19話_25_003.jpg'],decision='按实际二维空间安排复查，保留提示',reason='16_002由宽前景缓推到背影与岩脚全景；20_001跟拍让手在左下前层清楚；25_003明确深景深保留守卫近、董白中、巨兽后三层。常规对话靠静态构图与低细节后景保持眼口清楚，没有为术语数量强加摄影机动作。此文本判断未获得视频验证。'))
    else:
        raise AssertionError(('Unreviewed global warning',w))
ledger['scope']='完整覆盖用户19.zip提供的75个原文件（第02—26页），未提供第01页。'
ledger['skill_version']='Gen2.8 / 72a89198d6660479631d45be21f49dabad0316d0'
for r in ledger['character_registry']:
    if r['id']=='dongbai':r['identity_audit']='04_002核对长双马尾、浅色内发束及高领黑短装，07_002介绍框明确董白（20）；03_002/003按连续手柄与黑短装构图归入持刀董白。受困少女另列。'
    if r['id']=='closed_helmet_guard':r.update(traits='覆面全盔，正面多道水平狭缝、宽肩甲；第19话当前外观按04_003、25_003核对。',identity_audit='使用稳定角色名，未强配有姓名的人设；不沿用前话Y形面缝作为本话造型。')
ledger['character_registry'] += [
 dict(id='captive_girl_ep19',canonical_name='受困少女',status='stable_role_label',traits='黑色刘海、后方束起长发，26_001头脸可见；无已确认姓名。',reference_paths=['comic-workspace/episodes/ep-019/source/monochrome-panels/第19話_26_001.jpg'],identity_audit='与持刀董白同场，不沿用第18话脚本对受困者的董白映射；未据相似黑发确定人名。'),
 dict(id='hooded_visitor',canonical_name='黑袍来者',status='stable_role_label',traits='深灰长袍、全暗兜帽、圆形肩扣；回想13_001单独出现面罩轮廓。',reference_paths=['comic-workspace/episodes/ep-019/source/monochrome-panels/第19話_12_001.jpg'],identity_audit='青确认是此前大叔；春子判断魔族为剧情信息，不补帽内脸或已知姓名。'),
 dict(id='giant_orc_ep19',canonical_name='巨型兽人',status='stable_role_label',traits='巨大宽躯、黑色圆脸白眼、粗大手指，25_003台词称兽人。',reference_paths=['comic-workspace/episodes/ep-019/source/monochrome-panels/第19話_25_001.jpg'],identity_audit='本话洞窟线承接开头对手；采用当前明确兽人称呼，不补变形与再生机制。')]
ledger['revision_audit']=[
 dict(images=['第19話_03_002.jpg','第19話_03_003.jpg','第19話_04_002.jpg','第19話_07_002.jpg'],reason='持刀者身份确认',resolution='参考董白的人设及07_002人物介绍框确认，统一持刀者为董白；受困者保持独立角色名。'),
 dict(images=['第19話_06_001.jpg','第19話_06_002.jpg','第19話_06_003.jpg','第19話_06_004.jpg'],reason='手部任务',resolution='原尺寸核对06_001的黑色料面为露指手套，修订拉衣描述；黑手与裸露手按当前源图，不强行补两侧同色。'),
 dict(images=['第19話_22_002.jpg','第19話_23_004.jpg'],reason='刀尖几何',resolution='原尺寸与后续相同物件视角确认兜帽近缘及间隙，改写早期硬质曲面撞击为刀尖抵近急停；没有刺入或新增伤口。'),
 dict(images=['第19話_17_001.jpg','第19話_18_001.jpg','第19話_19_001.jpg','第19話_21_002.jpg','第19話_26_002.jpg','第19話_24_001.jpg'],reason='片段连续性',resolution='聚合抬手至通道15秒、空中挥刀至压制及青跑近13秒、末次抽刀至准备7秒；暗场并入入口线结尾，场景切回独立。')
]
ledger['final_audit']['source_scope']=ledger['scope']
ledger['final_audit']['semantic_review']=dict(status='completed_source_and_text_review',method='本次作者逐格图像核对并按已读学园表演校准比较成稿；不是独立盲评或视频验证。',warnings=review,continuity=[dict(image=p['image'],connection=p['continuity'],anchor_phase=p['anchor_phase']) for p in ledger['panels']],quality_basis='任务与情绪按整段发展；同框人物持续参与，裁切反应与有意持态不强填手势；声线只在台词栏。')
ledger['final_audit']['limitations']='未生成视频；源图未提供的脚步全路线、击倒手法、回鞘过程、变形和再生机制均未补画。自然日文保留语义，裸露局部及性化口腔强调以非露骨取景处理。'
(O/'source-ledger-v3.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(O/'warning-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in [D,C,E/'source/monochrome-panels']:p.mkdir(parents=True,exist_ok=True)
manifest=json.loads((O/'source-integrity.json').read_text(encoding='utf-8'));checks=[]
for m in manifest:
    src=O/'source-originals'/m['image'];dst=E/'source/monochrome-panels'/m['image']
    shutil.copy2(src,dst)
    assert hashlib.sha256(dst.read_bytes()).hexdigest()==m['sha256']
    checks.append(dict(image=m['image'],source_unchanged=True,sha256=m['sha256']))
assert len(checks)==75
(O/'source-copy-check.json').write_text(json.dumps(dict(status='pass',count=75,files=checks),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
name='第19话_制作分镜_Gen2.8.md'
for dest in [C/name,D/name]:shutil.copy2(O/name,dest)
for name in ['source-ledger-v3.json','new-shot-index.json','source-integrity.json','source-package.json','source-copy-check.json','warning-review.json','progress.json']:
    shutil.copy2(O/name,D/name)
run=subprocess.run([sys.executable,'-X','utf8',str(S/'scripts/validate_storyboard.py'),str(C/'第19话_制作分镜_Gen2.8.md'),'--max-seconds','15','--image-dir',str(E/'source/monochrome-panels'),'--source-ledger',str(D/'source-ledger-v3.json'),'--require-source-ledger'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
(D/'validation.txt').write_text(run.stdout,encoding='utf-8');assert run.returncode==0,run.stdout
assert [l for l in run.stdout.splitlines() if l.startswith('警告')]==warnings
bubbles=[dict(image=p['image'],speaker=b['speaker'],kind=b['kind'],source_text=b['source_text'],japanese=b['script_text'],target=b['target']) for p in ledger['panels'] for b in p['bubbles']]
(D/'dialogue-mapping.json').write_text(json.dumps(bubbles,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
adap=[dict(image=p['image'],scope=p['adaptation_scope']) for p in ledger['panels'] if p.get('adaptation_scope')]
report=f'''# 第19话交付说明

2026-10-10，Gen2.8，技能基线72a8919。

- 覆盖：19.zip的75个原文件，页码02—26，包中没有01页；逐格核对完成。
- 输出：{progress['clips']}片段、{progress['shots']}分镜、{progress['runtime_seconds']}秒（5分53秒），每片段不超过15秒，六字段完整。
- 对白：{len(bubbles)}项气泡内容/内心/无声标点均有映射。中文原文与自然日文及目标镜头见dialogue-mapping.json。省略号/问号中的无声反应有明确处理；Splash等拟声不当作角色台词。
- 原图：解包到source/monochrome-panels，75张逐文件SHA-256与包内原图一致，没有压缩、改名或覆盖改绘。
- 特殊页：08_001纯作品标题不生成镜头；22_003“别动”接到22_004压制镜头；16_001上下两格分为两个连续镜头。
- 检查：结构和台账0错误；保留{len(warnings)}条语义启发式提示，逐条处置见warning-review.json。本次是图像和文本检查，未生成视频。

## 表演与连续性

青从憋笑否认转入内疚，再到认人惊喜、通道震惊及冲突困惑。春子的冷淡回应、警觉判断和出手保持连续，头肩/背面裁切不强配未见表情。董白从从容威胁转为吃力估量，握刀与备战贯穿。长句按自然日文计时，拆分视角与前后图至少有两项有意义的差异。

抬手、指间轻响、爆光护脸及完整通道合为15秒；卷身、刀路、急停、压制及青跑近合为13秒；末次抽刀与正面备战合为7秒。近距刀尖与帽缘保持间隙，没有新增刺入或割喉伤口。

## 身份与改编范围

07_002人物框明确持刀者为董白（20），并与人设外形核对。受困少女另列角色名，没有沿用前话稿的董白映射；黑袍来者未露出当前五官。后段按对白采用“巨型兽人”，没有补其变化机制。

'''
report+=''.join('- '+a['image']+'：'+a['scope']+'\n' for a in adap)
report+='\n上述裸露细节以非露骨镜头处理；本话普通剧情与对白语义保留。未经供给的路线、收刀、击倒和再生过程留在镜间，没有为串戏补新事件。静态构图参考用于过程/结果锚点，不作为视频首帧输入。\n'
(D/'交付说明.md').write_text(report,encoding='utf-8')
status=f'''# 第19话

- 原始上传包：../19.zip（用户提交71f1784）。
- 单色原图：source/monochrome-panels/，75张，第02—26页；包中无第01页，已逐格核对。
- 当前分镜：storyboards/current/第19话_制作分镜_Gen2.8.md
- 版本：Gen2.8（72a8919），{progress['clips']}片段、79分镜、{progress['runtime_seconds']}秒，单片段≤15秒。
- 覆盖：完整覆盖提供素材。纯标题省略、纯指令并入动作镜头；裸露局部为非露骨取景，详见交付说明。
- 审计：storyboards/deliveries/2026-10-10_Gen2.8_整话/。结构/台账0错误，{len(warnings)}条启发式提示已有逐条处置。
- 原图字节与包内SHA-256一致。未生成视频，表演质量仍需视频制作阶段验证。
'''
(E/'STATUS.md').write_text(status,encoding='utf-8')
readme=R/'comic-workspace/README.md';t=readme.read_text(encoding='utf-8');t=t.replace('第1—18话均已建立统一目录。','第1—19话均已建立统一目录。').replace('ep-001/ ... ep-018/','ep-001/ ... ep-019/')
readme.write_text(t,encoding='utf-8')
with zipfile.ZipFile(D/'第19话_分镜交付包_Gen2.8.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(D.iterdir()):
        if f.is_file() and f.suffix!='.zip':z.write(f,f.name)
print(json.dumps(dict(delivery=str(D),current=str(C/'第19话_制作分镜_Gen2.8.md'),source_count=75,shots=79,clips=progress['clips'],seconds=progress['runtime_seconds'],bubble_items=len(bubbles),warnings=len(warnings),source_checks='75/75 byte-identical',validation='0 errors'),ensure_ascii=False))
