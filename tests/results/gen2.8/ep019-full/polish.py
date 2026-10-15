from authoring import *
replacements={
'02_003':{'，第二句问得比第一声更清楚；':'；'},
'03_003':{'说话很平静':'腰侧站姿从容'},
'04_001':{'第二句更低，':''},
'04_002':{'第一句说得随意，第二句带着好奇，脸稍抬起':'带着好奇稍抬起脸'},
'04_003':{'短促催促之后，第二句更急，岩壁仍静':'两句求助之后，岩壁仍静'},
'05_002':{'他低声吐出两句':'他在两句打量中仍偏着头'},
'06_002':{'时语气转成轻微讥讽':'时嘴角露出一点讥讽'},
'07_002':{'眼神比语气更冷':'眼神始终冷着'},
'08_004':{'语气说得平，':''},
'09_004':{'时声音更低':'时目光更低'},
'10_001':{'低声说自己什么也没做好':'说出自己什么也没做好'},
'11_001':{'第一句气势高，':'她的肩头绷着，','末句声音弱一些':'句末嘴唇慢慢合起'},
'13_001':{'后句干脆落在能战斗这一点':'后句落在能战斗这一点'},
'15_001':{'话尾落得干脆':'肩部转向随之稳定'},
'16_001':{'句中略停，声音有些疑惑':'场面留给她认出地点的一瞬'},
'19_002':{'话越问越清楚，':''},
'22_001':{'动作直接进入接触':'动作直接进入刀尖抵近的急停'},
'22_004':{'后一句低而坚定':'握刀的手一直压稳'},
'25_003':{'担心一直在声音里':'盔面仍朝左后看着'}
}
for f in sorted((O/'drafts').glob('*.json')):
    rows=json.loads(f.read_text(encoding='utf-8'))
    for s in rows:
        for a,b in replacements.get(s['image'][5:11],{}).items():s['fields'][1]=s['fields'][1].replace(a,b)
        if s['image']=='第19話_05_003.jpg':s['fields'][2]='独立背景完全被主体遮住。'
        if s['image']=='第19話_08_003.jpg':s['fields'][2]='灰棕木门竖纹在后景，右侧一小段深褐岩壁，木面暗缝低对比。'
        if s['image']=='第19話_25_002.jpg':s['fields'][2]='深褐岩壁退在后景，凸石暗面低对比，细缝纹理稳定。'
        if s['image']=='第19話_25_003.jpg':s['fields'][0]=s['fields'][0].replace('固定','固定深景深',1)
        if s['image']=='第19話_11_001.jpg':s['fields'][3]='青说：“そ、それでも！命は大事にしてよ！この道は危険だって、自分で言ったでしょ……。”（首句急促结巴，随后强烈强调生命，最后的提醒放轻，带着委屈与担心。）'
        if s['image']=='第19話_12_001.jpg':s['fields'][3]='黑袍来者说：“久しぶり。”（熟悉、从容。）青说：“あ、あなたは……？”（开头迟疑结巴，停一下才把疑问接出，后段更轻。）'
        if s['image']=='第19話_26_001.jpg':s['fields'][3]='受困少女说：“い、いえ、それだけじゃ……。”（开头惊慌结巴，随后急着补充，末尾略停，话还没有说完。）'
        if s['image']=='第19話_11_002.jpg':
            old='何かあっても、あのツインテール女が何とかするよ。';new='何かあっても、あのツインテールのクソ女が何とかするよ。'
            s['fields'][3]=s['fields'][3].replace(old,new)
            s['jp']=[j.replace(old,new) for j in s['jp']]
            if old in ''.join(s.get('jp',[])):raise AssertionError()
            if new in s.get('jp',[]):s.update(seconds=7,speech_seconds=6.8,bubble_seconds=[6.65])
    f.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for f in sorted((O/'observations').glob('*.json')):
    rows=json.loads(f.read_text(encoding='utf-8'))
    for p in rows:
        p['jp']=[j.replace('何かあっても、あのツインテール女が何とかするよ。','何かあっても、あのツインテールのクソ女が何とかするよ。') for j in p['jp']]
        if p['image']=='第19話_22_001.jpg':
            p['continuity']='承接空中举刃与直线下落，下一格刀尖抵近急停。'
            p['plan']['landing']='刀刃快速下落，准备停在目标近处。'
    f.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
