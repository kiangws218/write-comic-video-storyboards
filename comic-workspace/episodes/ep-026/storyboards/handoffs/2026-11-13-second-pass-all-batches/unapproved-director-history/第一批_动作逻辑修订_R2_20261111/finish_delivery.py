"""核对明确纠正项，整理R2交付；不改旧版本。"""
import hashlib,json,re
from pathlib import Path
P=Path(__file__).parent;R=P.parent
def read(name):return json.loads((P/name).read_text(encoding='utf-8'))
def save(name,text):(P/name).write_text(text,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=read('scene-ledger.json');t=read('剪辑与声轨.json');v=read('版本与验证.json')
execution=(P/'第一批_逐片执行稿.md').read_text(encoding='utf-8')
assert '审计通过：0个错误，0个警告。' in (P/'执行稿校验.txt').read_text(encoding='utf-8')
assert '结构验证通过：0个错误' in (P/'结构校验.txt').read_text(encoding='utf-8')
shots=[s for c in t['clips'] for s in c['shots']];by={s['key']:s for s in shots}
assert execution.count('参考“')==36
assert all(('参考“' in s['fields']['镜头设计'])==bool(s['source_images']) for s in d['shots'])
assert [s['key'] for s in t['clips'][5]['shots']]==['R031','R033','R034','R035','R036','R037','R038','R039','R040']
assert t['clips'][5]['duration']==11
assert all('青' not in by[f'R{i:03d}']['actors'] for i in range(41,51))
assert not re.search('银灰发缘|贴青后肩|青已经穿到|武士POV', ''.join(by[f'R{i:03d}'][k] for i in range(41,51) for k in ['camera','action']))
assert '脱刃刀光' in by['R028']['action']
assert '一脚先触石' in by['R049']['action'] and '双方脚底' in by['R052']['camera']
assert all('颈' in by[f'R{i:03d}']['action'] for i in range(59,64))
assert '安回肩背' in by['R059']['action']
assert sha(P/'第一批_动作逻辑修订_R2.md')==t['main_sha256']
previous=R/'第一批_原生动画导演重制_20261110'
old_manifest=json.loads((previous/'交付指纹.json').read_text(encoding='utf-8'))
assert all(sha(previous/name)==expected for name,expected in old_manifest.items())

save('README.md','''# 第一批动作逻辑修订 R2 · 2026-11-11

用于视频生成的最终正文是 [第一批逐片执行稿](第一批_逐片执行稿.md)，每片一个可复制代码块。

[时间表主稿](第一批_动作逻辑修订_R2.md)方便通读与剪辑核对。89镜、15片、164.5秒；范围仍为第26话01_001及08_003—19_002。

本次落实：

- 斩击刀光脱离武士实体刀，越过青后切断烟囱。
- 第6片为连续11秒：青坠到B屋顶→撑手→双脚落稳→站起→掌贴断囱→前推出去。武士仍在空中。
- 第7片与第8片前半主要拍武士，隐藏青推后起跳、尾随与接近；第8片分镜4才首次揭晓青已近身。
- 武士在第8片分镜2落C地面，近身出拳、青后撤滑停及双方对峙均衔接同一地面。
- 第9片中武士一手安回带鞘刀、另一手扶颈，边走出烟尘边活动头部，随后回正看青。

36个原格对应镜头直接标注“参考‘第26話_格编号’”（执行正文用中文双引号），35条锁定日文台词全文保留。

原R1、根台账及原全段主稿均保留。本目录为修订后的完整第一批，未将R2混入其余批次。检验范围见 [修改与核对记录](修改与核对记录.md)，环境结果见 [环境复核](环境复核.md)。尚无本版动态视频或日语实录验证。
''')

warning_text=(P/'结构校验.txt').read_text(encoding='utf-8')
groups=[]
for line in warning_text.splitlines():
    if not line.startswith('警告：'):continue
    n=re.search(r'同类(\d+)条',line)
    groups.append({'count':int(n[1]) if n else 1,'message':line.split('（同类')[0]})
source_warnings=sum(g['count'] for g in groups if '[来源]' in g['message'])
save('修改与核对记录.md',f'''# R2修改与核对记录

本版89镜（53新增镜）、15片、164.5秒，最大单片{v['max_clip_seconds']:g}秒。原36个视觉节点及顺序保留，35条信息的来源原文、锁定日文、归属、类型、ID逐项不变；跨镜重接全文一致。

动作与悬念：根据2026-11-11用户明确解释，把钢刃切砖改为脱刃刀光切烟囱；青在B屋顶接同一次坠落完成撑手、落脚、站稳、掌推，整段归入第6片11秒。推送后至14_002首次揭晓前，R041—R050无青入画，也没有发缘、影子、后肩、对面POV或提前发声提示。以武士R049落脚交代空中转C地面，R051第一次揭青，R052同框见双方脚底在C。

扶颈：R059武士一手安回带鞘刀，另一手放颈侧；R060局部活动头部，R061脚步继续，R062全身走出时仍扶颈转头，R063回正后才松手。没有用扶颈动作增加新伤或改变战果。

连续动作与片界：第3片屋顶追逐/观察/起跳为完整12秒；第6片落地到掌推为完整11秒；第9片后撤滑停接扶颈走出为同一13秒片；第14片膨胀、反应、局部落地、全貌、青的反应合在13.5秒。其他片界沿用实际姿态与余势，没有重演落地或出招。拔刀至躲避及斩碎至地面揭晓两组因完整台词与演出总长超过15秒而分片，片界仍连续。

场面设计与时间：A为起跳屋顶，B为落脚/掌推屋顶，C为后续石铺地面。断囱长节底角落B屋面并靠残基承重，是本轮明确记录的制作衔接设计，未伪报源图观察。空中段按同一主观时距约1/6实速连续推进，武士始终沿弧下降，檐线上移；声轨自然发声，刀光与发力有快峰值，触C后恢复常速。未增设悬浮能力。

回源：本轮实际重开20个受影响原格及邻格（清单在scene-ledger.json的source_revision）；11_001a长裁图由工具缩放显示。其余沿用先前核对，未声称全批重新看图。12_002“脚蹬后离开”及16_003“手臂自然垂/摆”等旧理解，按本轮用户解释和回图修正。source_revision保存旧来源锁、新锁、原因和确认原话；重新冻结针对解释纠错，完整台词与原镜序列不变。

校验：结构0错误、{v['warnings']}条提示，其中来源类{source_warnings}条主要注明创作补充与新增镜身份；执行稿0错误、0警告。每片正文低于1900字符。已核对35全文、36参考标记、89目标唯一性、第6片完整连续动作、揭晓前无青入画、双方地面接触、扶颈跨镜及刀具回肩背。R1交付指纹逐文件比对全部一致，根台账/旧第一批/旧全段主稿未改。

提示处置：环境词表和裁切提示按真实镜内范围核对，掌、砖、脚特写不列镜外屋檐/远楼；摄影落幅按正文跟随对象与终点核对；持续表演按落地、站稳、发力、判断、听者变化及颈部/脚步协同核对；新增镜头保留创作身份。发声估时是规划提示，不能据单镜文字切分强迫配音加速，实际日语实录尚未做。完整程序输出保留在结构校验.txt。

边界：未生成/播放R2动态分镜或视频，未读取用户测试视频，未实录配音。文字演出与空间检查通过不等于视频生成质量已验证。
''')
save('提示分类.json',json.dumps({'total':v['warnings'],'source_warnings':source_warnings,'groups':groups},ensure_ascii=False,indent=2)+'\n')
v['execution_audit']={'errors':0,'warnings':0}
v['explicit_comic_references']=36
v['continuity_check']={'roof_landing_to_push_in_one_clip':6,'continuous_clip_seconds':11,'qing_hidden_keys':'R041—R050','ground_first_reveal_key':'R051','neck_action_keys':'R059—R063','r1_manifest_all_unchanged':True}
save('版本与验证.json',json.dumps(v,ensure_ascii=False,indent=2)+'\n')
manifest={f.name:sha(f) for f in sorted(P.iterdir()) if f.is_file() and f.name not in ['交付指纹.json','编译日志.txt']}
save('交付指纹.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('R2关键修订核对通过：落地至掌推同片11秒，R041—050不露青，地面接触明确，扶颈连续。')
