from pathlib import Path
import json, math, importlib.util
O=Path(__file__).parent
def read(n):return json.loads((O/n).read_text(encoding='utf-8'))
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
spec=importlib.util.spec_from_file_location('validate',O/'skill-latest/scripts/validate_storyboard.py'); v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
obs=read('observations/remaining.json'); ss=read('drafts/remaining.json')
for p in obs:
    p['composition_lock']=p['composition_lock'].replace('居中','位于中央').replace('在左，','在左侧，').replace('在右，','在右侧，').replace('左，','左侧，').replace('右，','右侧，')
    if sum(bool(q.search(p['composition_lock'])) for q in v.COMPOSITION_SIGNAL_GROUPS)<2:
        p['composition_lock'] += '取景沿画面边缘裁切，局部保持清楚。'
    for b in p['bubbles']:
        if len(b)>2:b[2]='inner' if b[2]=='thought' else 'dialogue'
    if p['image']=='第18話_17_003.jpg':p['jp']=['まったく、','ない。']
by={p['image']:p for p in obs}
for s in ss:
    f=s['fields']
    f[0]=f[0].replace('居中','位于中央').replace('在左，','在左侧，').replace('在右，','在右侧，').replace('画面不出现人物','画面保持无人空镜')
    f[0]=f[0].replace('固定守卫側面','固定守卫侧面').replace('固定董白頭部','固定董白头部')
    if sum(bool(q.search(f[0])) for q in v.COMPOSITION_SIGNAL_GROUPS)<2:
        if s['image']=='第18話_09_003.jpg':f[0]+='远处石缝留在后景，上方凸石压住较深的岩面。'
        elif s['image']=='第18話_22_001.jpg':f[0]+='头部位于画面中央，黑发边缘在左右侧清楚分开。'
        else:f[0]+='取景边缘裁切清楚，局部占据画面中央。'
    if '黑发遮住大半后景' in f[2]:f[2]='背景被黑发大幅遮挡，右侧露出窄而低细节的灰褐图形底场，明暗稳定。'
    elif '黑发与脸部暗面占满' in f[2]:f[2]='背景被满幅头部遮挡，后方仅留窄而低细节的灰暗图形底场。'
    elif '面部暗面占满' in f[2]:f[2]='背景被满幅面部遮挡，取景中只有脸部由上浅下深的暗面。'
    elif '极近处钢灰金属' in f[2]:f[2]='背景被满幅头盔遮挡，画面只见钢灰金属暗面与深黑盔缝。'
    elif '冷灰底' in f[2] or '灰暗底场' in f[2] or '白底与黑色' in f[2]:f[2]=f[2].replace('冷灰底','冷灰图形底场').replace('灰暗底场','灰暗图形底场').replace('白底与黑色','白色图形底场与黑色')
    replacements={'说到自己时':'说到「俺」时','说到次数时':'说到「五回」时','说到因为是对方时':'说到「あなただから」时','提到未婚夫时':'提到「婚約者」时'}
    for old,new in replacements.items():f[1]=f[1].replace(old,new)
    # 气泡表演留在台词字段，声音仅保留环境、呼吸和拟音。
    if any(w in f[5] for w in ['对白','尾音','拒绝声','话音']):
        env='低洞窟空气声持续，近处呼吸一口气后渐缓，空旷回响很短。'
        if '守卫' in f[0]:env='低洞窟空气声持续，盔部随头动轻微金属摩擦，头盔内呼吸短而清楚。'
        if s['image']=='第18話_21_002.jpg':env='低洞窟空气声压低，手指收紧时短而轻的衣料摩擦，随后留短停。'
        f[5]=env
    if s['image']=='第18話_17_003.jpg':s['jp']=['まったく、','ない。'];f[3]=f[3].replace('まったく、違う。','まったく、ない。')
    jp=s.get('jp',by[s['image']]['jp'])
    # 以独立自然语速复核人工估时；不缩短日文来挤入既定秒数。
    s['bubble_seconds']=[round(max(a,b),2) for a,b in zip(s.get('bubble_seconds',[0]*len(jp)),map(v.estimated_japanese_speech_seconds,jp))]
    s['speech_seconds']=round(max(s['speech_seconds'],sum(s['bubble_seconds'])),2)
    # 无气泡且有声画任务的镜头保留原秒数；有对白镜头给够完整发声时间。
    s['seconds']=max(s['seconds'],math.ceil(s['speech_seconds']))
    s['acting_seconds']=min(s['acting_seconds'],s['seconds'])
    if s['image']=='第18話_21_001.jpg' and s.get('evidence_owner'):
        # 原图20_002只承担人物排列证据，不作为本格的第二个所有者。
        s.pop('evidence_owner')
        s['supporting_visual_images']=['第18話_20_002.jpg','第18話_19_003.jpg']
        s['fact_claims']={'entities':[],'actions':[],'relations':[]}
    if s.get('plan','x') is None:s['fact_claims']={'entities':[],'actions':[],'relations':[]}
    if s.get('uncited'):
        s['coverage']['coverage_evidence']=s['coverage']['coverage_evidence'].replace('具体身体接触不入画','原图中露骨内容省略')
save('observations/remaining.json',obs);save('drafts/remaining.json',ss)
print('Refined field ownership and independently rechecked Japanese speech durations.')
