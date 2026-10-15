"""Validate the completed episode and persist concrete cut/advisory reviews."""
from pathlib import Path
import collections, json, os, re, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
CURRENT=ROOT.parent.parent/'current/第20话_制作分镜_Gen2.8.md'
BASE=ROOT.parent.parent/'archive/2026-10-11_Gen2.8_最终动作复查前'
SKILL=Path('C:/Users/86135/.codex/skills/write-comic-video-storyboards-gen2-8')
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def save(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
ledger=read(ROOT/'source-ledger-v3.json'); baseline=read(BASE/'source-ledger-v3.json')
env=dict(os.environ,PYTHONIOENCODING='utf-8')
args=[sys.executable,str(SKILL/'scripts/validate_storyboard.py'),str(CURRENT),'--max-seconds','15',
 '--image-dir',str(ROOT/'proxies'),'--source-ledger',str(ROOT/'source-ledger-v3.json'),'--require-source-ledger']
result=subprocess.run(args,env=env,capture_output=True,text=True,encoding='utf-8')
(ROOT/'validation-report.txt').write_text(result.stdout+result.stderr,encoding='utf-8')
assert result.returncode==0,result.stdout+result.stderr
text=CURRENT.read_text(encoding='utf-8'); old= (BASE/CURRENT.name).read_text(encoding='utf-8')
refs=re.findall(r'分镜参考 `\[([^\]]+)\]`',text)
assert refs==re.findall(r'分镜参考 `\[([^\]]+)\]`',old),'Reference order changed'
assert len(refs)==len(set(refs))==66
assert '战斗段' not in text
def bubble_signature(data):
    return [(p['image'],[(b['source_text'],b['script_text'],b['speaker'],b['kind'],b['status']) for b in p['bubbles']]) for p in data['panels']]
assert bubble_signature(ledger)==bubble_signature(baseline),'Dialogue ownership/content changed'
shots=ledger['shots']; reviews=ledger['final_audit']['semantic_review']; review_by={r['target']:r for r in reviews}
durations=collections.Counter()
for r in reviews: durations[r['target'].split('/')[0]]+=r['seconds']
assert max(durations.values())<=15
assert sum(durations.values())==356 and len(durations)==34 and len(shots)==76

# These are manual semantic decisions, keyed by the actual incoming owner.
connections={
 '03_001':('local_connection','前镜帽口/竖刃压制持续，本镜只将该刀向上提起，升高到春子握刀肩侧；不是刺入帽内。'),
 '03_002':('direct_cut','刀已上提至高位，春子握持与侧脸逼问接续；头部前压不改变握柄和刀的所有权。'),
 '03_004':('direct_cut','经过兜帽局部反应，春子的持刀高位仍延续；侧脸沉默不重演举刀。'),
 '04_001':('local_connection','春子高位握刀接一次下挥；“ゼロ。”不再补数数或第二刀。'),
 '04_002':('local_connection','下挥仍在行程中，另一只手从右下入画抓腕，接触后截住下行；动作只完成一次。'),
 '04_003':('direct_cut','抓腕已经成立，青急切说明与春子下压力缓弱并行；后续手部覆盖抓腕持续。'),
 '05_001':('direct_cut','解释后的手部覆盖仍抓腕，春子呼气让步不松掉刀柄，也不重置青的接触。'),
 '05_002':('local_connection','持刀下压已停止；可见抓帽手从左上入画、抓紧帽边，不能写成持刀手换手或收刀。'),
 '05_003':('intentional_source_ellipsis','局部掀帽切到源图已给的开阔双人背影和水纹；帽下脸与来者消失机制均无可用图像，保留显露结果，未假称过渡已演出。'),
 '06_001':('direct_cut','开阔水面后青惊觉，源图斜线作两秒图形强化；下一格回到水面亮团。'),
 '06_002':('direct_cut','惊觉切至明确水域亮团，图形线势不进入实景，不据此新增受击者。'),
 '06_003':('direct_cut','亮团后只保留源浪过局部布边；肢体匿名，不能据切点反推冲刺/跳跃。'),
 '07_001':('action_bridge','托肩手与承膝手合近、春子膝腿抬起进入横抱；桥末双支撑到位。后面的源镜仅压稳承重并回应，抱起不重复。'),
 '07_002':('direct_cut','青继续承重横抱，低角度腿部框出远方四站一蹲；裁去春子不代表将她放下。'),
 '08_001':('direct_cut','同五人群组从远景切近景，中央下肢被裁去，不能把前后层次变化当成起立。'),
 '08_002':('graphic_transition','一秒源图黑带是对峙与董白介绍间的独立顿点，不承担人物位移。'),
 '09_001':('direct_cut','握刀局部作为董白准备的引入，双手所有权不变，刀尚未挥出。'),
 '09_002':('local_connection','双手握刀接向上举至头顶，闭眼锚点与原图一致；不借能力旁白再造凝刃路线或挥砍。'),
 '09_003':('expository_insert','无面黑剪影为源介绍插景；不把旁白姓名转换成该人身份，不要求董白动作在插景里重置。'),
 '10_001':('expository_insert','高俯视董白全身/裂纹石地是源新的介绍视角，承重呼吸继续；并非未画路线的迁移。'),
 '10_002':('local_connection','新的巨大手掌局部短压入石面；原图拇指/长指拓扑纠正脚掌误读，只有一次按地。'),
 '11_001':('direct_cut','同一按地手掌保持，环纹绕掌指，手不重压、无新施法者。'),
 '11_002':('direct_cut','环纹消退后手掌仍按地，两秒读取完整掌指结果。'),
 '11_003':('local_connection','完整掌指接局部断口分开、断块离位及黑色飞溅；不增未见攻击者/刀路。'),
 '12_001':('direct_cut','源刀刃向上掠过、黑滴飞散为已有动作过程，未扩成额外身体攻击。'),
 '12_002':('local_connection','刀的已有行程后董白肩背与前臂收势，身体先止、马尾后回；镜尾双手仍在右后握柄。'),
 '13_001':('graphic_transition','原图黑带/斜白线与碰鸣作两秒转折，不补实体刀的隐藏路径。'),
 '13_002':('local_connection','前段源图形接刀刃断裂结果，董白前臂仍有余势；不能追加第二次断裂或反击。'),
 '14_001':('direct_cut','断刃后圆眼/咬牙/短呼气反应，近距离与手臂余势持续，未安排退步。'),
 '14_002':('local_connection','巨指在身侧已有开口向内合拢到接触，主要抓握明确可见；不补远处伸手或空中路线。'),
 '14_003':('direct_cut','抓握持续，董白头后仰反应，巨指不第二次圈紧。'),
 '15_001':('listener_cut','青梅男独立反应只露盔/下颌；董白的巨手包围通过听者镜持续，不放开后重抓。'),
 '15_002':('scene_insert','王座台阶/云层是独立来源插景，不能将其当连续洞内路线；前后短片均因场景断点保留。'),
 '15_003':('return_from_insert','王座插景后回欧迈及现有脸部，咧笑与露齿继续，未调用巨形变身桥。'),
 '16_001':('semantic_overflow','五段稳定语义拆分保留现有非露骨改编；15_003确认支配与本格首命令合15秒，随后各局部反应/暗场在稳定思想边界继续，不重演接触。'),
 '17_001':('direct_cut','威胁插段继续到欧迈及眼尾/女子眼部，现有受制状态不变；裁切不承担新行为。'),
 '18_001':('graphic_transition','原有黑灰面承接威胁插景结束，保留有目的暗场；回18_002明确巨形双白点眼及手。'),
 '18_002':('return_from_insert','回巨形上身与现有大手，牙列/口侧雾随呼气；条件话语不证明释放或怀孕发生。'),
 '18_003':('listener_cut','双人头部反应，女子泪目与男子盔下惊语不同步；身体受制不改写为新的动作。'),
 '19_001':('direct_cut','董白现有巨指包围持续，质骂与询问不触发新攻击；后续局部上臂镜维持同一接触。'),
 '19_002':('speaker_cut','欧迈及眼鼻特写仅在可见眼鼻内回答；董白受制通过反打延续。'),
 '19_003':('listener_cut','董白听任务消息，再内部疑问，现有灰暗弧面/受制位置不变；反应覆盖不重新抓握。'),
 '20_001':('speaker_cut','对目标的三个短语是同一描述，口部/暗面连续，未新增被描述人物。'),
 '20_002':('intentional_time_ellipsis','长段介绍与插景之后重返青，以原图交臂站姿冷启动；实际放下时刻没有相邻源端点，明确省略，不写虚构放下桥。'),
 '21_001':('direct_cut','交臂青切同水面双人并立全景，青右春子左的世界站位成立；镜头从前到背不是演员重转身。'),
 '21_002':('direct_cut','全景并立接青向右侧问话；无新走近路线或握手目标。'),
 '21_003':('listener_cut','兜帽沉默三秒承接两问；青的站位和问后注意不因反打重置。'),
 '22_001':('local_connection','侧脸问后转回正面略低头，右手抬起拨发；镜尾手仍在脸旁，眼闭。'),
 '22_002':('local_connection','青从略低正面转向右侧称呼；春子抬眼应答后青托付。右手在此裁切外继续高位，不凭裁切默认落手。'),
 '22_003':('local_connection','原图辨认右手拨发/左臂横展是两臂：右手落至左袖边并捋高，左臂横胸、开放掌光；同一条手臂的错误衔接撤回。'),
 '23_001':('listener_cut','兜帽局部反应是源图线势内的小偏头；青左臂/右手捋袖的镜尾通过反应镜延续。'),
 '23_002':('local_connection','青开放左手从横臂抬近眼侧，源软焦/灰细点保留；不把手伸进眼内。'),
 '23_003':('local_connection','同一开放手从眼侧移到口前，拇指仍与唇留窄隙；没有新增咬伤。'),
 '23_004':('local_connection','来者从袖内抬腕至肩侧，贴拇指/中指准备，未提前响指；青口前手通过覆盖仍在。'),
 '24_001':('source_phase_and_reaction','贴指准备接一次弹开响指，再切青眼部反应，青的口前手因极近裁切不可见，不增放手动作。'),
 '24_002':('memory_insert','响指/青反应切源餐桌回忆，纸页、餐具与站后来者都是该格实体，不假称现场瞬移。'),
 '25_001':('local_connection','从餐桌回忆转肩侧局部：同一深色手从左上落指形成接触，0.4秒后按图内下段抬离和细闪；没有脱衣机制。'),
 '25_002':('direct_cut','手抬离后的源心冠卷纹结果，三秒读清已有图形；不补复杂绘制路径或身体后果。'),
 '26_001':('graphic_result','已有肩侧纹样接对应白纹/黑晕闪现，最后只呈原图图形高点及衰减，不新增人物、文字或伤害。')}
boundaries=[]
for previous,incoming in zip(shots,shots[1:]):
    a=review_by[previous['target']]; b=review_by[incoming['target']]
    pid=re.search(r'第20話_(.+)\.jpg', (incoming['source_images'] or incoming['derived_from'])[0]).group(1)
    mode,decision=connections.get(pid,('direct_cut','已审机位覆盖维持当前人物姿势、接触和任务；无新事件。'))
    if a['image']==b['image'] and pid!='16_001':
        mode='same_panel_coverage'; decision='同一源格的覆盖承接；'+decision
    boundaries.append({'outgoing':previous['target'],'incoming':incoming['target'],
      'clip_boundary':previous['target'].split('/')[0]!=incoming['target'].split('/')[0],
      'outgoing_current_state':a['landing'],'incoming_opening':b['opening'],
      'connection':mode,'decision':decision})
assert len(boundaries)==75
ledger['final_audit']['cut_continuity_review']=boundaries
ledger['final_audit']['reviewed_images']=['第20話_'+i+'.jpg' for i in
 '01_001 02_001 03_002 04_001 04_002 04_003 05_001 05_002 05_003 06_001 06_002 06_003 07_001 07_002 08_001 08_002 09_001 09_002 09_003 10_001 10_002 11_001 11_002 11_003 12_001 12_002 13_001 13_002 14_001 14_002 20_002 21_001 21_002 22_001 22_002 22_003 23_001 23_002 23_003 23_004 24_001 24_002 25_001 25_002 26_001'.split()]
ledger['final_audit']['original_resolution_reinspection']=['第20話_'+i+'.jpg' for i in '10_002 11_002 20_002 22_001 22_003'.split()]
warnings=[l for l in result.stdout.splitlines() if l.startswith('警告：')]
dispositions=[]; counts=collections.Counter()
for warning in warnings:
    target=re.search(r'片段\d+/分镜\d+',warning)
    if '需表演语义复查' in warning:
        category='performance'; r=review_by[target.group(0)]
        decision='时序：'+ '→'.join(r['time_course'])+'；互动：'+r['interaction']+'；'+r['decision']
    elif '需背景字段语义复查' in warning:
        category='background_field'; decision='复看12_002原图：此字段“脸部后方”只是限定斜线底场的亮区，未把脸/衣服写成背景；主体肩背收势只在可见动作，图形不投出实体气流。保留。'
    elif '明确说话人' in warning:
        category='dialogue_coverage'; decision='22_002同框可见青的口部、春子眼口，称呼→短应答→托付共9秒；听者头/眼回应在句间可读。三轮短话由同一机位承接，无需重复反打。'
    elif '合并复查' in warning:
        category='clip_grouping'
        decision=('15_001青梅男反应与15_002王座台阶之间为明确空间插景，8秒也不跨场强合；王座退出回欧迈及已有6+9秒威胁命令合为15秒。' if '片段14与片段15' in warning else
          '20_001描述后返回20_002青交臂有明确时间省略，分开10秒/3秒冷启动。20_002的3秒反应与下一完整21_001—21_003的15秒单元合计18秒；保留该短片。')
    else:
        category='action_admission'; decision='按当前源原子与相邻端点检查三项准入；本稿的必要前导/身体表演未由对白单独授权。'
    counts[category]+=1
    dispositions.append({'target':target.group(0) if target else warning.split('，')[0].replace('警告：',''),
      'class':category,'warning':warning,'decision':decision,'blocking':False})
ledger['advisory_dispositions']=dispositions
rule_files=[SKILL/'SKILL.md']+[SKILL/'references'/name for name in
 ['core-authoring.md','dialogue-performance.md','acting-calibration.md','cinematic-rendering.md','background-design.md','background-visual-library.md','source-risk.md']]
rule_bytes=sum(p.stat().st_size for p in rule_files)
ledger['final_audit']['rule_input_size']={'utf8_bytes':rule_bytes,'files':[str(p) for p in rule_files],'combat_module_loaded':False}
metrics={'clips':len(durations),'shots':len(shots),'runtime_seconds':sum(durations.values()),
 'references':len(refs),'max_clip_seconds':max(durations.values()),'blocking_errors':0,
 'advisories_by_class':dict(counts),'manual_overflow_count':0,
 'documented_natural_overflow_panels':[p['image'] for p in ledger['panels'] if p.get('overflow_split')],
 'source_images_reopened':len(ledger['final_audit']['reviewed_images']),
 'original_resolution_reinspections':len(ledger['final_audit']['original_resolution_reinspection']),
 'cut_boundaries_reviewed':len(boundaries),'rule_input_utf8_bytes':rule_bytes,
 'cross_episode_scene_review':'deferred_by_user','storyboard_path':str(CURRENT),'ledger_path':str(ROOT/'source-ledger-v3.json')}
ledger['final_audit']['validation_summary']=metrics
save(ROOT/'source-ledger-v3.json',ledger); save(ROOT/'final-review-metrics.json',metrics)
# Revalidate the actual delivery ledger including dispositions, not an earlier copy.
final=subprocess.run(args,env=env,capture_output=True,text=True,encoding='utf-8')
(ROOT/'validation-report.txt').write_text(final.stdout+final.stderr,encoding='utf-8')
assert final.returncode==0,final.stdout+final.stderr
report='''# 第20话 Gen2.8 最终动作复查

已基于已保存制作稿和V3来源台账完成动作/表演、实际切点、源图阶段、字段、台词、增镜、背景和时长复查。按用户最新指示，本轮暂停十六至十九话场景对照；保持战斗模块关闭。

## 制作结果

- 34片段，76镜，356秒（5分56秒），66张正式来源参考；每片不超过15秒。
- 新增片段8/分镜3，2秒，托肩/承膝形成横抱；片段8/分镜4只压稳承重和回应，抱起不重复。
- 抓帽、抬右手拨发、右手捋左袖/左臂横展、抬腕贴指准备响指、手肩接触均补最短可见前导；指端断口由完整接触衔接到分开。
- 纠正10_002—11_003手掌/指端误作脚掌/趾端，09_002恢复闭眼；08_001裁切不再被误解为起立。
- 06_001、12_002、23_001采用本话源格已有的斜线图形与统一冷色配色，分别在06_002、13_002、23_002返回可见空间；不新增图形施法或气流。
- 15_003冷笑6秒与16_001第一命令9秒合为15秒；王座空间插景保留独立边界。

## 时间省略与证据边界

横抱后有长段介绍及插叙，20_002原图清楚交臂，21_001明确两人并立。放下动作的具体时点与相邻端点没有源图；撤回不合准入的放下桥，将返回青明确作为时间省略，冷启动采用已经交臂站立的实态。05_002局部抓帽与05_003开阔结果之间保留源省略，不虚构帽下脸或消失机制。

漫画图作为中段/接触/结果参考，未绑定首帧，未调用视频生成工具。文字审校与结构通过不代表生成视频已获表演验证。

## 校验与审阅

'''
report+=f'- 阻塞校验：0错误；启发式提示{len(warnings)}项，按类记录如下：'+ '、'.join(f'{k} {v}' for k,v in counts.items())+'。每项均在V3台账的advisory_dispositions中逐条处理。\n'
report+='- 75个实际切点全部留有出镜状态→入镜开场及具体连接决定；反应覆盖后回接、接触持续和同一动作不重复分别检查。\n'
report+=f'- 本轮复看45张受影响/相邻图，其中5张升级原图；其他已审批次复用，无全量源图二次审阅声明。\n- 16_001自然单格42秒，五个稳定语义段按源台账溢出拆分；人工超时项0。\n- 规则输入：8文件，共{rule_bytes} UTF-8字节；未加载战斗模块。\n'
report+='- 原日文、来源文字、对白归属/类型/顺序与66张参考顺序同基线一致；所有原证据及前一版审阅记录保留。\n'
report+='\n## 文件\n\n'+f'- 当前稿：`{CURRENT}`\n- 来源及审阅台账：`{ROOT / "source-ledger-v3.json"}`\n- 校验报告：`{ROOT / "validation-report.txt"}`\n- 修订记录：`{ROOT / "action-review-changes.json"}`\n- 原稿归档：`{BASE}`\n'
(ROOT/'第20话_最终动作复查报告.md').write_text(report,encoding='utf-8')
status=ROOT.parent.parent.parent/'STATUS.md'
status.write_text('''# 第20话

- 单色单格：66张（已去除66份完全重复文件）。
- 当前分镜：storyboards/current/第20话_制作分镜_Gen2.8.md。
- 2026-10-11本地复查结果：34片段、76镜、356秒、66张参考；结构/来源台账校验0错误，最终动作及75个切点审阅完成。
- 必要增镜：横抱形成动作桥2秒；抓帽、拨发、右手捋左袖、抬腕准备响指、肩侧接触的最短前导已补。
- 战斗模块：关闭，按普通六字段保留原图事件。
- 时间省略：介绍/插叙之后回青时已交臂站立，未虚构未被相邻源图支持的放下过程。
- 暂缓事项：按用户指示暂停十六至十九话场景一致性复核，保留既有场景基准。
- 台账/报告：storyboards/deliveries/gen2.8/；复查前原稿位于storyboards/archive/2026-10-11_Gen2.8_最终动作复查前/。
- 整页漫画：未上传。
''',encoding='utf-8')
print(json.dumps(metrics,ensure_ascii=False,indent=2))
