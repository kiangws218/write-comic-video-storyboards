import hashlib,json,re
from pathlib import Path
P=Path(__file__).parent
def read(name):return json.loads((P/name).read_text(encoding='utf-8'))
def save(name,text):(P/name).write_text(text,encoding='utf-8')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
d=read('scene-ledger.json');t=read('剪辑与声轨.json');v=read('版本与验证.json')
assert '结构验证通过：0个错误' in (P/'结构校验.txt').read_text(encoding='utf-8')
assert '审计通过：0个错误，0个警告。' in (P/'执行稿校验.txt').read_text(encoding='utf-8')
exe=(P/'第二批_逐片执行稿.md').read_text(encoding='utf-8');shots=[s for c in t['clips'] for s in c['shots']];by={s['key']:s for s in shots}
assert exe.count('参考“')==26
assert all(('参考“' in s['fields']['镜头设计'])==bool(s['source_images']) for s in d['shots'])
assert len(shots)==51 and len(t['clips'])==8 and sum(c['duration'] for c in t['clips'])==94.5
assert t['clips'][2]['duration']==13.5
assert '同一时刻' in by['S013']['action'] and '两掌' in by['S013']['action']
assert all('双手' in by[k]['action'] or '两手' in by[k]['action'] for k in ['S014','S015','S016','S017','S018'])
assert '撞实后才松开两手' in by['S020']['action']
assert '吞住武士全身' in by['S020']['action'] and '吞没整幅' in by['S021']['action']
assert '完全没有接触' in by['S038']['action'] or '身体和衣物均与白流分开' in by['S038']['action']
assert sha(P/'第二批_动作与演出优化_R1.md')==t['main_sha256']
assert all(sha(Path(path))==h for path,h in v['old_file_hashes_unchanged'].items())
old=json.loads((P.parent/'第二批_第27话'/'scene-ledger.json').read_text(encoding='utf-8'))
assert [p['image'] for p in d['panels']]==[p['image'] for p in old['panels']]
for p,op in zip(d['panels'],old['panels']):
 for b,ob in zip(p['bubbles'],op['bubbles']):
  assert all(b[k]==ob[k] for k in ['id','source_text','script_text','speaker','kind'])
  assert ''.join(s['script_text'] for s in b['segments'])==b['script_text']

save('README.md','''# 第二批动作与演出优化 R1 · 2026-11-11

直接用于视频生成：[第二批逐片执行稿](第二批_逐片执行稿.md)，每片一个可复制代码块。

通读与剪辑：[完整时间表主稿](第二批_动作与演出优化_R1.md)。全批51镜、8片、94.5秒；对应第27话17_001—26_003。26个原格对应分镜已直接标注参考编号，22条锁定日文台词完整保留。

重点在第3片，13.5秒：青两手同拍抓住来臂→双手持续承重转体→带过头顶→向下抡摔→砸实裂石→烟尘从接地点爆起，吞没武士并遮满画面。此段连续动作在同一片内，既没有先后补手，也没有提前松手。

第6片为同一股喷流的蓄势、逼近、完全躲开与落地；第8片为液团鼓动、爆散、小体完整揭晓与青抱头反应。全段夜晚，青尚未强化。开头保留原作时间省略，没有补写一个确定的新招式。

原第二批台账、原导演稿和原全段主稿保留。本目录为独立优化版。详见[修改与核对记录](修改与核对记录.md)及[环境复核](环境复核.md)。本版尚未生成/播放动态视频或实录日语对白。
''')

warnings=[]
for line in (P/'结构校验.txt').read_text(encoding='utf-8').splitlines():
 if line.startswith('警告：'):
  m=re.search(r'同类(\d+)条',line);warnings.append({'count':int(m[1]) if m else 1,'message':line.split('（同类')[0]})
source_count=sum(w['count'] for w in warnings if '[来源]' in w['message'])
save('修改与核对记录.md',f'''# 第二批修改与核对记录

版本：2026-11-11独立优化稿。51镜（25新增），8片，94.5秒；最长{v['max_clip_seconds']:g}秒，执行正文最长{v['max_execution_clip_chars']}字符。

用户明确纠正已落实：两手同时闭合抓握同一来臂末端，起抡前就完成同拍抓牢，双手持续承重直到武士砸实才松开。第3片连续13.5秒包含抓握、站姿承重、转体过顶、折身下抡、接地裂石、厚尘吞体满画。删除了20_001b解释中旧“补手过程”，更正动作路径与节点后重新冻结来源解释；旧锁与新锁、原话与范围保存在source_revision。

烟尘的顺序：S020先让接地姿态和原作放射裂石短暂可读，碎屑喷出、厚尘从真实撞点爆起吞没武士；S021分瓣烟团铺满整幅，保留到下一片。青在撞实后解除抓握并后撤至薄尘边，武士继续被厚尘遮住，直到S031原作23_002才重新显出撑起轮廓。没有用满画烟雾跳过原作接地节点，也没有把烟尘爆发变成火焰或新能力。

空间：开场旧藏身尘区与本次抡摔的新撞点分开。新点在青脚前交叉板缝左端，比旧尘区更近；S017沿板缝转机位，S018按正对下抡弧观察，S020俯视重立青与落点。后段厚尘和武士起身均在这个新撞点。反打时尘只贴武士近侧及裂坑，不复制到青身后。

喷流：从武士上游到青原站位，再到其后方下游同一长板缝旁。S038从青左后下游回看上游，白流远右上→近右侧出镜；S039顺流承接同一落点。青身体和衣物完全避开，无击中/沾染。液团落地不增新裂地，小体在液团爆散后才完整出现。

演出：喘息、等待与试探持续有重心、眼神、手部和环境回应；抡过头顶阶段短慢镜、下砸末段快峰值，面部与脚步插入期间抓握和下抡一直推进。嫌恶回骂和内心胜算有完整身体表演；内心声音不被武士听见。喷流错身时身体短慢、主流仍快。4段明确对白空白共2秒，另有无对白动作与环境停留。

作画与特效：将FX-04实体裂解、FX-05碎屑/烟尘分层、DRAW-02短促尖形过渡方法改写到真实受力、落点、轻重速度与结束状态。接触黑白替换仅两帧后回夜景；重块慢翻、细屑快喷、厚尘后卷并持续。读取了方法文本，未在本轮播放参考片，不把文本方法称为本轮动态观察或生成验证。

来源检查：本轮重新打开26个视觉节点的720p代理，20_001a/b按已验证的真实上下格裁图分别核对；人物主档复查青与鬼头武士条目。25原文件、26节点及顺序保留，22条ID/来源原文/日文/归属/类型不变，跨镜文字重接与全文逐项一致。26处漫画引用已进入执行正文，新增25镜保留导演创作身份。

程序：结构0错误、{v['warnings']}条提示，其中来源类{source_count}条主要说明创作补充和导演新增身份；执行格式0错误、0提示，均低于15秒/1900字符。其余词表、裁切、运镜、持续表演和估时提示已按实际正文前向核对；估时仍需日语实录验证，不能用文字片段强迫发声加速。完整输出保留在结构校验.txt。

旧版第二批台账、导演稿及原全段主稿哈希逐项未变。最终环境文字结论见环境复核.md；本版未生成/播放动态视频，未实录配音，文本和程序通过不等于成片效果已验证。
''')
lines=['# 原格与台词对照','','| 原格节点 | 新版分镜 |','|---|---|']
for p in d['panels']:lines.append(f'| {p["image"]} | {p["anchor_target"]} |')
lines+=['','| 信息ID | 来源原文 | 锁定日文全文 | 覆盖镜号 |','|---|---|---|---|']
clean=lambda s:s.replace('|','／').replace('\n',' ')
for p in d['panels']:
 for b in p['bubbles']:lines.append('| '+' | '.join([b['id'],clean(b['source_text']),clean(b['script_text']),'、'.join(s['target'] for s in b['segments'])])+' |')
save('原格与台词对照.md','\n'.join(lines)+'\n')
save('提示分类.json',json.dumps({'total':v['warnings'],'source_warnings':source_count,'groups':warnings},ensure_ascii=False,indent=2)+'\n')
v['execution_audit']={'errors':0,'warnings':0};v['explicit_comic_references']=26
v['confirmed_checks']={'simultaneous_two_hand_grip':'S013','continuous_grip_through_throw':'S014—S019','ground_impact_before_release':'S020','full_frame_dust_cover':'S021','all_in_one_clip_seconds':13.5,'spray_fully_avoided':'S037—S038','old_files_hashes_unchanged':True}
save('版本与验证.json',json.dumps(v,ensure_ascii=False,indent=2)+'\n')
manifest={f.name:sha(f) for f in sorted(P.iterdir()) if f.is_file() and f.name not in ['交付指纹.json','编译日志.txt']}
save('交付指纹.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('第二批关键核对完成：双手同拍抓握、接地才松手、烟尘吞体满画；26节点/22全文/51镜/8片。')
