from pathlib import Path
import json
O=Path(__file__).parent
e={'viewed_before_palette_revision':True,'images':['comic-workspace/episodes/ep-018/source/panels/第18话_014_002.jpg','comic-workspace/episodes/ep-018/source/panels/第18话_020_001.jpg'],'observed_traits':['秃顶兽人为低饱和橄榄绿色肤色','黑色尖下巴胡须','牙齿灰白','洞窟岩石暖褐色'],'scope':'只确认上色及身份类别；保留稳定称呼秃顶男子，不强配角色人名。'}
(O/'color-observations.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=O/'drafts/remaining.json';ss=json.loads(p.read_text(encoding='utf-8'))
for s in ss:
    f=s['fields']
    if s['image']=='第18話_15_004.jpg' and '极近景' in f[0]:f[2]='背景被满幅主体遮挡，实景不可见。'
    if s['image'] in ['第18話_14_002.jpg','第18話_15_003.jpg','第18話_17_003.jpg','第18話_20_001.jpg','第18話_21_002.jpg'] or (s['image']=='第18話_21_001.jpg' and not s.get('supporting_visual_images')):
        f[4]=f[4].replace('面部自然肤色','面部橄榄绿色肤色').replace('面部肤色','面部橄榄绿色肤色').replace('手部肤色','手部橄榄绿色肤色')
        if '橄榄绿' not in f[4]:f[4]+='肤色保持低饱和橄榄绿，暗面偏深绿，亮面带暖黄反光。'
    if s['image']=='第18話_09_003.jpg' and s['seconds']==5:
        f[3]=f[3].replace('开头结巴，后句带急迫的制止','开头结巴并急于制止，后句更痛苦、压力加重')
    if s['image']=='第18話_17_001.jpg':f[3]=f[3].replace('开头惊怒结巴','开头惊怒结巴、第二次起音更急')
p.write_text(json.dumps(ss,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
