from pathlib import Path
import json
O=Path(__file__).parent
P=O/'drafts/remaining.json'; ss=json.loads(P.read_text(encoding='utf-8'))
for s in ss:
    n=s['image'];f=s['fields']
    if n=='第18話_13_003.jpg':
        s.update(seconds=7,speech_seconds=6.5,bubble_seconds=[4.15,2.0],intervals=[{'speech_seconds':4.5,'acting_seconds':4.5,'concurrent':True},{'speech_seconds':2.0,'acting_seconds':2.0,'concurrent':True}])
    if n=='第18話_19_003.jpg':s.update(speech_seconds=3.5,intervals=[{'speech_seconds':2.35,'acting_seconds':0,'concurrent':True},{'speech_seconds':1.15,'acting_seconds':1.5,'concurrent':True}])
    if n=='第18話_15_004.jpg' and '极近景' in f[0]:f[2]='背景被满幅头盔遮挡，实景不可见。'
    if n=='第18話_20_002.jpg':
        if '空镜' in f[0]:f[2]='深褐岩壁横向层叠，右下凸石偏浅，中央石缝很暗，整体低细节。'
        else:f[5]='低洞窟空气声持续，董白急促的受惊呼吸在恳求后仍断续，近处发束轻擦。'
    if n=='第18話_21_001.jpg' and s.get('supporting_visual_images'):
        s['source_reference_note']='董白与守卫头部关系来自20_002，面盔来自19_003；本格21_001只提供画外对白与男子听者反应。非露骨反打不使用裸露身体。'
        s['admission_override']='20_002已见董白泪眼正面与守卫右后位置；19_003面盔掀起；21_001的董白追问触发最短回望，只表现头部注意方向。'
        s['visual_evidence_override']='20_002董白左前、守卫右后，19_003掀起面盔；21_001董白画外追问。'
P.write_text(json.dumps(ss,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
