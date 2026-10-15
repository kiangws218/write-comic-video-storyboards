from pathlib import Path
import json
out=Path(__file__).resolve().parent
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path in (out/'observations').glob('06*.json'):
    data=load(path)
    for p in data:
        if p['image']=='第18話_06_001.jpg':
            p['composition_lock']='平视董白侧面头肩近景；脸位于右中、朝左，曲指手在左下胸前；后景岩壁沿侧脸左缘形成窄层，人物遮挡其余部分。'
            p['background_description']='董白侧脸后的窄区有真实凹凸岩壁。'
        elif p['image']=='第18話_06_002.jpg':
            p['background_description']='石地有裂纹并横铺下部，青和春子后方是凹凸岩壁。'
        elif p['image']=='第18話_06_003.jpg':
            p['composition_lock']='平视青正面偏左头胸近景；脸居上半部，交叠双手遮挡口前至胸前的部分衣领；长发沿左右肩侧垂下，后景省略实景。'
            p['original_resolution_viewed']=True
            p['original_resolution_reason']='确认下方手扣持另一侧手腕，上方手指交叠；未增加攻击接触。'
        elif p['image']=='第18話_06_004.jpg':
            p['composition_lock']='平视青正面偏左头胸近景；圆眼与张口居上半部，松叠双手居下半部并遮挡胸前领口；长发位于两侧，后景省略实景。'
    save(path,data)
for path in (out/'drafts').glob('06*.json'):
    data=load(path)
    for p in data:
        if p['image']=='第18話_06_003.jpg': p['bubble_seconds']=[1.6,2.8]
        if p['image']=='第18話_07_001.jpg':
            p.update(seconds=7, speech_seconds=6.5, bubble_seconds=[2.7,3.8])
        p['fields'][1]=p['fields'][1].replace('落入前景','落到近处').replace('左前景的春子','左侧的春子').replace('左前景','左侧')
    save(path,data)
