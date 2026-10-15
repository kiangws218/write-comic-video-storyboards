from pathlib import Path
import json
out=Path(__file__).resolve().parent
p=out/'drafts/07a.json'
d=json.loads(p.read_text(encoding='utf-8'))
for s in d:
    if s['image']=='第18話_08_001.jpg':
        s['bubble_seconds']=[2.7,2.0]
        s['fields'][0]='平视岩壁的横向近景空镜，近处凸石占下半部，后景石块由左上深暗区排到右下浅亮区，前后石面层叠清楚。镜头固定，纹理在焦内，给画外提议保留完整空间停留。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
