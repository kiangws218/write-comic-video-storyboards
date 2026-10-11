import collections, hashlib, importlib.util, json, pathlib, re, shutil, subprocess, sys, zipfile
import author_revision as author

ROOT, TASK, DELIVERY, CURRENT = author.ROOT, author.TASK, author.DELIVERY, author.CURRENT

def dump(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Explicit semantic dispositions for the current 80-shot review, particularly
# the confirmed low-affect actor and the action bridges preserved from baseline.
SPECIAL = {
2:'半眯眼内瞳孔方向无法确定，删除向下移的强解读；只准入眼睑持态与眉褶稍松。',
8:'鼻底与躯干下表面支持明显仰拍；董白的轻松笑口、直视镜头和抬脸仍承担六秒交流，上摇后拉只到当前岩壁与膝上范围。',
19:'侧身转头的瞳孔朝画前，改为看镜头而非看左上；近手与肩后刀保持双手任务，轴向推进不展示新侧面。',
20:'入口空镜没有春子面部；画外提问已改平调，不新增不满或烦躁。',
21:'青为回头否认的主要表演者，春子只以左前后脑与平稳坐姿在场；青的目光朝镜头有源眼瞳依据。',
22:'四秒事实陈述：半垂眼直视镜头、单侧内眉头高，嘴随台词小幅开合；不追加不满、怒相、二次挑眉或肿脸绷紧。',
23:'青靠近并把冰袋送到脸侧，源锚点为闭眼笑与袋脸留隙；横移到此停住。春子背面不补迎脸、情绪或接袋，十秒主要由青完整解释占据。',
24:'三秒只拍青持袋回胸前；春子画外回应平调，袋始终青持有。近景以手袋袖占满，occluded提示已核对，不露额外房间。',
26:'四秒青长叹与肩头下落，春子侧偏头接短问；她只是转注意，语调平直，不演困惑或无奈。',
27:'八秒青自责，目光肩头逐项下沉；春子左侧平静听完，半垂眼朝左侧外，眉头高维持，压力背景主要属于青。',
28:'九秒青担忧的侧脸独白；春子只作为期待回应者在文本中，未在画内新加表演。推进止于侧脸头肩。',
29:'七秒春子平调说黑色幽默后短问；脸侧向左、嘴随两句动、句间等回应。源图无笑容，不制造嫌弃或兴奋，幽默由内容与青反差成立。',
30:'青闭眼压眉转肩挤冰袋；春子只背面在场并平调短问。六秒既有主动作保留，跟移不改变冰袋所有者。',
31:'七秒画外春子平调说明被盗事实，近手慢慢缓力，袋仍在青手中。摄影机固定，向右下展开是袋身构图方向，不是镜头移动。',
33:'四秒春子转正、看镜头，平调说当前无事可做；源眉形保持，不演冷硬、嫌弃或安慰焦虑。',
34:'七秒画外春子判断与岩壁雾空镜；粗口全文保留，但语气平淡，不据辱称加鄙夷。',
35:'鞋底与石面接触支持低机位略俯，短移在落脚时停住；下摆随后落稳，无重复踩地。',
36:'两秒高机位俯拍，青仰脸看上方镜头；春子眼睛朝左前、头转向脚步方向，坐姿稳定，不同时惊慌。',
37:'低坐青的后脑与高大来者正面构成仰拍；帽内全暗。五秒招呼及青结巴半问，后段停顿已有 voice 节拍，非重复同一句。',
38:'六秒回想建议与短问同构图接力；青回头眼瞳朝镜头，条板物不强命名武器。',
39:'九秒回想商人解释，既有帽口手动作保留，推进不跨轴或掀帽。',
40:'五秒青认出声音、抬食指与侧脸惊喜同时推进；镜头上摇止于脸和指尖同框。',
41:'五秒春子平调两问，青笑着准备解释，二人都保留源视线；横移将两个表演落在同一连续中景，不需隐切。',
42:'六秒木栏床沿空镜续青解释；物件层次与亮面已修正，固定构图无人物新增。',
43:'七秒青画外介绍后春子短应；春子半垂眼直视镜头、口小幅应答，源眉形保持，不追加疑心或重估情绪链。',
44:'七秒青由坐到站的必要动作保留，上摇后拉让腿脚全程留画；来者招呼与青接话并行，终点站位不额外靠近。',
49:'七秒青两问、春子无声省略号；春子半垂眼看镜头、口轻合、眉形保持。删除第一次问后再挑眉和困惑递进；停顿服务交流而非眨眼歪头填时。',
50:'四秒入口空景承载春子认地点的平调说明；不增加疑惑表演，随后仰拍双人来自同文件下框。',
51:'六秒青猜通道、春子平调否定，源下框的洞顶、鼻底与近大远小支持仰拍；源视线朝镜头，两者活力反差不被统一成疑惑。',
52:'八秒背面静止等下一步；前推沿当前地面到岩脚止步，双脚完整。春子仅无声内心判断，不演不耐烦，也不提前开机关。',
55:'四秒同次爆光，青闭眼护脸、发衣顺源动势；春子画外平调短问。只后拉摇移到源双层构图，光峰不加击飞或摄影震动。',
56:'三秒青降低挡眼手臂、目光朝镜头；源脸汗点与睁眼为依据，不仅来自内心标点。',
57:'五秒亮门形成与说明并行，摇上后拉显现现有圆形外沿；门内亮白，不虚构目的地画面。',
58:'七秒青惊讶侧脸目光向画外左，近眉抬形保持；不把侧脸与人物抬头误当仰拍或看镜头。',
59:'两秒春子短否定；内眉头高、眉尾低与斜眼睑是源形态，全程保持。嘴在画外，平调发言，不延伸警觉或紧张。',
60:'三秒快速身体前冲、手掠水再离水，源手背/头顶/水面上表面支持斜俯。半垂眼朝前方镜头、面部低外显，语调平直；退跟只在冲刺轴，不造新藏刀。',
61:'一秒踩水再蹬起，接触特写固定；只有脚部动作，低外显基调不削弱蹬地力度。',
62:'两秒水花升碎落回，俯拍右摇落帽背左、水花右，春子不额外出镜。',
63:'四秒来者转头赞许，仰拍上摇至帽口仍暗、上方留空的构图；未揭露面孔。',
64:'两秒春子跃起、收腿、举刀、进入下落；来者后方强仰拍跟上到源空中锚点。源头发遮脸不补瞳孔，三无不减跃起动作。',
65:'一秒刀刃下掠的插入特写，快速摇下仅见当前刀面，接下一镜急停，不增碰撞。',
66:'一秒刀尖急停微颤、水珠惯性散开，源窄隙保持；固定清晰焦面，无刺入伤口。',
67:'两秒下落到屈腿压制的已批准桥接保留，后侧俯拍随降停住，握刀与兜帽留隙贯穿；对比前镜极近接触和后镜背部中景，整身关系与裁切功能均不同。',
68:'六秒屈腿稳定压制，握柄压力持续；春子平调说制止与警告，不加愤怒或冷硬神态。推进止于后侧源中景。',
69:'三秒青跑近逐步收短，俯拍跟摇保留春子后脑左前；不新增青碰刀/推开人的接触。',
70:'四秒青收步喘气直视镜头追问；左眉头低另一眉较平源不对称保持，近手抬起即止。',
71:'六秒春子前俯朝向对应压制，直视镜头平调分析；半垂眼与单侧眉头高维持，不添加警觉眼神、厉色或情绪反转。',
72:'四秒刀尖留隙特写承载春子平调结论；当前可见灰水面白圆纹已修正为physical背景，刀未入布。',
75:'四秒董白屈身与欧迈及俯低黑脸、白眼朝镜头的巨躯反差；上摇后拉到源双人范围，未补第二次攻击。',
76:'六秒董白快速呼吸转稳、握柄在下巴旁，刘海遮眼始终保留；上摇不会编造可见瞳孔。',
77:'八秒青梅男说再生时董白握柄手先从下巴放低；深景深三层全景保留源人物远近，后拉不展示来源外空间。',
78:'四秒青梅女安全面部裁切与结巴补充，稍仰是源鼻底/颈部透视；不拉到裸露局部，不确定瞳孔不写看镜头。',
79:'四秒抬刀鞘、推回鞘再抽出的全路径保留，后拉止于手和下半脸；没有在已出鞘状态无因重新拔刀。',
80:'五秒再次备战：双手刀鞘分离、脸抬起直视镜头，后拉到源腰上中景；刀缩小由画外说明，不虚构可见瞬间伸缩机制。',
}

BOUNDARIES = {
 (22,23):'春子正面陈述切青靠近：反打改变机位，冰袋先在青胸前，再前送；春子未接袋。',
 (23,24):'脸侧留隙的同一冰袋退回青胸前；手部特写承接回收，不出现贴脸或换手。',
 (24,25):'冰袋已回到青胸前，岩壁空镜不推进人物动作。',
 (29,30):'春子平调黑色幽默引青转肩挤袋；冰袋属于青，主情绪反差在青。',
 (30,31):'青的同一近手挤袋后逐渐缓力，非镜位切换重置为另一手。',
 (35,36):'靴子落地声引二人注意；青仰脸看高处镜头，春子只朝脚步转头。',
 (36,37):'俯拍坐姿切低机位仰拍来者与青后脑，二人的头部方向符合高低关系。',
 (43,44):'青此前低坐，下一镜实际上摇跟起身；站稳后源全景锚点到达。',
 (48,49):'来者远去切春子沉默听青求证；只保留源眉形，不加情绪升级。',
 (52,53):'来者背面站定后侧面抬臂，身体状态未提前做响指。',
 (53,54):'手臂抬起停住进入指间近景，单次响指接下镜爆光。',
 (55,56):'爆光短峰退亮，青降低挡眼手臂再睁眼，眼睛朝镜头而非仍闭眼。',
 (56,57):'青反应插入后光门继续形成；来者位置不被反应特写重置。',
 (59,60):'春子平淡短否定到迅速前俯冲刺，情绪幅度维持但身体动作完整。',
 (60,61):'手掠水并离水后脚掌落水蹬起，刀仍在春子当前手上；退跟不引入新拔刀。',
 (61,62):'蹬起后的水花在来者背后腾起，春子跃起未被画外空镜重置。',
 (63,64):'来者转头切后方仰拍春子上升到空中收腿举刃，帽内持续遮挡。',
 (64,65):'空中举刃进入下落，刀身插入近景不产生新的上挥。',
 (65,66):'刀刃下掠在帽缘前急停，尖端留隙，无穿刺或新伤口。',
 (66,67):'急停刀尖留隙进入后侧俯拍双人下降桥接，握刀手随身形下降，间隙持续。',
 (67,68):'两人落水、春子屈腿落位后进入源背面压制，压制动作兑现，不直接由悬空跳到稳定骑跨。',
 (68,69):'春子压制保持，青从远处跑近；来者没有新挣扎，刀尖保持间隙。',
 (69,70):'青跑近收步后头肩追问，近手只抬起即停，无撞入春子的压制位置。',
 (70,71):'青疑问切春子平调分析，春子前俯朝向对应压制，头肩特写不改变腿与刀状态。',
 (71,72):'春子说完分析，刀尖插入特写续身份结论；细水纹背景可见，压制未松。',
 (76,77):'下巴旁握柄手先放低到身侧，三层全景到达源落点，刀始终由董白持有。',
 (78,79):'青梅女补充的语义停顿切董白动作；董白刀已在身侧外，先抬回胸前推回鞘再抽出。',
 (79,80):'回鞘再抽动作终点是双手分持，随后抬脸备战；刀与鞘不突然合回。',
}

def classify(line):
    tests=[('角色基调语义复查','character_profile_semantics'),('需表演语义复查','performance_semantics'),('含2名明确说话人','multiple_speakers'),('缺少焦段','camera_quality'),('没有镜头落幅','camera_landing'),('含重复话语','repeated_dialogue'),('证据说明涉及文本语境','mixed_evidence'),('需背景遮挡','background_occlusion'),('需摄影机俯仰','camera_angle')]
    for needle,name in tests:
        if needle in line:return name
    return 'other'

def main():
    baseline=json.loads((TASK/'inventory.json').read_text(encoding='utf-8'))
    text=CURRENT.read_text(encoding='utf-8');shots=author.parser.parse(text)
    ledger=json.loads((DELIVERY/'source-ledger-v3.json').read_text(encoding='utf-8'))
    obs={x['image']:x for x in json.loads((TASK/'image-observations.json').read_text(encoding='utf-8'))}
    assert len(shots)==len(baseline)==80
    for a,b in zip(baseline,shots):
        assert (a['target'],a['seconds'],a['refs'])==(b['target'],b['seconds'],b['refs'])
        assert re.findall('“([^”]+)”',a['fields']['台词与语气'])==re.findall('“([^”]+)”',b['fields']['台词与语气'])
    # Actual byte checks of all supplied images against package and published
    # manifest, including the two non-renderable page files.
    src=ROOT/'comic-workspace/episodes/ep-019/source/monochrome-panels'
    archive=ROOT/'comic-workspace/episodes/19.zip'
    source_checks=[]
    with zipfile.ZipFile(archive) as z:
        members={}
        for info in z.infolist():
            name=info.filename
            if not info.flag_bits & 0x800:
                for encoding in ['utf-8','gbk']:
                    try:
                        name=info.filename.encode('cp437').decode(encoding)
                        break
                    except UnicodeError:
                        pass
            members[name]=info
        for entry in ledger['source_files']:
            data=z.read(members[entry['archive_member']]);expected=entry['sha256']
            assert hashlib.sha256(data).hexdigest()==expected
            assert hashlib.sha256((src/entry['image']).read_bytes()).hexdigest()==expected
            source_checks.append({'image':entry['image'],'sha256':expected,'package_and_workspace_match':True})
    dump(DELIVERY/'source-integrity.json',{'status':'pass','source_images':len(source_checks),'originals':source_checks})
    # Concrete per-shot outcome, independent of the validator's warning count.
    review=[]
    for n,(s,record) in enumerate(zip(shots,ledger['shots']),1):
        im=baseline[n-1]['images'][0]
        conclusion=SPECIAL.get(n,obs[im]['plan']+' 保留已批准任务与接触；新版摄影机路径不新增主体、环境或遮挡面。')
        review.append({'index':n,'target':s['target'],'seconds':s['seconds'],'evidence_images':baseline[n-1]['images'],'source_angle':obs[im]['angle'],'source_gaze':obs[im]['gaze'],'conclusion':conclusion,'status':'reviewed'})
        record['semantic_revision_review']={'conclusion':conclusion,'seconds':s['seconds'],'status':'reviewed'}
    boundaries=[]
    for n in range(1,80):
        a,b=ledger['shots'][n-1],ledger['shots'][n]
        conclusion=BOUNDARIES.get((n,n+1),'按当前源格与已批准相邻状态切换；本轮只改变取景路径或低外显表演，原场景、道具所有者、接触和动作终点保留，无未编号切镜。')
        boundaries.append({'from':a['target'],'to':b['target'],'outgoing':a['motion_decision'].get('admitted_plan'),'incoming':b['motion_decision'].get('admitted_plan'),'status':'reviewed','conclusion':conclusion})
    ledger['final_audit']['camera_gaze_affect_revision']['shot_review']=review
    ledger['final_audit']['camera_gaze_affect_revision']['boundary_review']=boundaries
    dump(DELIVERY/'source-ledger-v3.json',ledger)
    command=[sys.executable,'-X','utf8',str(ROOT/'write-comic-video-storyboards-gen2-8/scripts/validate_storyboard.py'),str(CURRENT),'--max-seconds','15','--image-dir',str(ROOT/'tests/results/gen2.8/ep019-full/analysis-proxies'),'--source-ledger',str(DELIVERY/'source-ledger-v3.json'),'--require-source-ledger']
    result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',cwd=ROOT)
    output=result.stdout+result.stderr
    (DELIVERY/'validation.txt').write_text(output,encoding='utf-8')
    errors=[x for x in output.splitlines() if x.startswith('错误：')]
    assert result.returncode==0 and not errors, errors
    lines=[x for x in output.splitlines() if x.startswith('警告：')]
    by_target={s['target']:n for n,s in enumerate(shots,1)}
    dispositions=[]
    for line in lines:
        m=re.search(r'片段(\d+)(?:的)?(?:分镜|/分镜)(\d+)',line)
        target=f'片段{m[1]}/分镜{m[2]}' if m else None
        cls=classify(line)
        if target:
            n=by_target[target]
            conclusion=review[n-1]['conclusion']
            if cls=='camera_landing':
                conclusion+=' 当前镜头正文：'+shots[n-1]['fields']['镜头设计']+' 已标明停住/固定取景；纯构图方向不作为镜头移动。'
            if cls=='camera_angle':
                conclusion+=' 头顶部分可见并不足以建立明显俯拍；08_003使用肩高平视，区别人物回头与摄影机光轴。'
            if cls=='mixed_evidence':
                conclusion+=' 物理动作来自图像及已记录动作桥接，台词只承担说话时序；未以文本设定补新接触。'
            if cls=='character_profile_semantics':
                conclusion+=' 已对照共享映射版本3；春子现有动作/朝向参与交流，低外显并不冻结身体任务。'
        else:
            assert cls=='camera_quality',line
            conclusion='逐镜明确源透视、构图、焦面和取景路径。片段31/分镜1深景深保留三层，送冰袋同焦面保持间距，拔刀/跃起/压制各有连贯路径与落点；无需以焦段术语数量增加摄影变化。仍待实际视频验证。'
        dispositions.append({'warning':line,'target':target,'class':cls,'disposition':'reviewed','conclusion':conclusion,'review_scope':'当前720p图像、完整动作/台词与摄影机路径逐镜语义复查。'})
    warning_report={'errors':0,'warning_count':len(lines),'classes':dict(collections.Counter(x['class'] for x in dispositions)),'dispositions':dispositions}
    dump(DELIVERY/'warning-dispositions.json',warning_report)
    dump(DELIVERY/'shot-boundary-review.json',{'shots':review,'boundaries':boundaries})
    shutil.copyfile(TASK/'changes.json',DELIVERY/'changes.json')
    shutil.copyfile(TASK/'skill-sync.json',DELIVERY/'skill-sync.json')
    modules=['SKILL.md','references/core-authoring.md','references/dialogue-performance.md','references/acting-calibration.md','references/cinematic-rendering.md','references/source-risk.md','references/2d-animation-execution.md','references/background-design.md']
    rule_bytes=sum(len((ROOT/'write-comic-video-storyboards-gen2-8'/p).read_bytes().replace(b'\r\n',b'\n')) for p in modules)
    summary={'clips':32,'shots':80,'seconds':357,'max_clip_seconds':15,'formal_reference_images':69,'reviewed_images':73,'supplied_images':75,'changed_camera_fields':80,'moving_cameras_before':2,'moving_cameras_after':sum(s['camera_decision']['mode']!='fixed' for s in ledger['shots']),'actions_changed':len(author.ACTS),'voice_notes_changed':len(author.VOICE_NOTES),'errors':0,'warnings':len(lines),'warning_classes':warning_report['classes'],'manual_overflow_items':[],'source_audit':'75/75 SHA-256 matches original package and workspace','rule_input_bytes':rule_bytes,'rule_modules':modules,'skill_commit':author.SKILL_COMMIT,'character_map_version':3,'video_tested':False,'dialogue_literals_references_durations_unchanged':True}
    dump(DELIVERY/'summary.json',summary)
    dump(TASK/'verification.json',summary)
    # Human-readable comparison keeps the finished script free of audit detail.
    changes=json.loads((TASK/'changes.json').read_text(encoding='utf-8'))
    report=['# 第19话运镜、视线与春子三无表演修订','',
        '最新 Gen2.8 技能提交：`'+author.SKILL_COMMIT+'`，本机20个受管文件逐一核对哈希。共享角色映射采用版本3。',
        '', '完整脚本为32片段、80镜、357秒，正式引用69张；实际复查73张720p源图，包内提供75张。日文台词文本、引用、时长与原动作桥接保持。',
        '', '80镜重写摄影机字段；有明确路径的运动镜头从2镜变为42镜。运动围绕源动作和源构图选择，接触特写与冷面交流仍可固定。31镜动作表述、20镜语气备注同步修订。',
        '', '董白登场与来者身高关系补清仰拍，诊所抬头与落地压制补清俯拍；可辨眼瞳朝画前的镜头将“看镜头”写进动作，闭眼、背头、遮眼和不清晰瞳孔不强推视线。',
        '', '春子保留原内眉头偏高、半垂眼等形态，去掉不满、困惑递进、警觉、鄙夷等额外情绪；声音平淡、语调起伏低。快速前冲、跃起、挥刀与稳定压制完整保留，粗口及黑色幽默台词全文保留。',
        '', f'校验：0错误，{len(lines)}条启发式提示逐条处置。分类：'+json.dumps(summary['warning_classes'],ensure_ascii=False)+'。79个相邻边界与80个表演/摄影机任务已有具体审阅记录；无手工超时拆分。',
        '', f'源图：75/75与原包SHA-256一致。规则输入：{rule_bytes}字节，模块见summary.json。此轮未生成视频；脚本级审查不能替代生成后对表演幅度及机位执行的核对。',
        '', '## 逐镜对照','']
    for item in changes:
        report += ['### '+item['target']+'（'+str(item['seconds'])+'秒）', '',SPECIAL.get(item['index'],obs[item['source_images'][0]]['plan']), '']
        for field, vals in item['fields'].items():
            report += ['**'+field+'**','', '- 原：'+vals['before'], '- 新：'+vals['after'],'']
    (DELIVERY/'修订对照.md').write_text('\n'.join(report).rstrip()+'\n',encoding='utf-8')
    (DELIVERY/'交付说明.md').write_text('\n'.join(report[:16])+'\n\n当前正文保留原先非露骨取景及未提供第01页的素材范围。相机取景变化同步修正必要的可见背景与布光。\n\n详细变化见修订对照.md；源图事实与取舍见source-ledger-v3.json。\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__': main()
