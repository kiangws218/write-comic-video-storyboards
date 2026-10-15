from authoring import *
def replace_tree(v,mapping):
    if isinstance(v,str):
        for a,b in mapping.items():v=v.replace(a,b)
        return v
    if isinstance(v,list):return [replace_tree(x,mapping) for x in v]
    if isinstance(v,dict):return {k:replace_tree(x,mapping) for k,x in v.items()}
    return v
names={'持刀少女':'董白','持刀者':'董白','巨型怪物':'巨型兽人'}
for folder in ['observations','drafts']:
    for f in sorted((O/folder).glob('*.json')):
        rows=json.loads(f.read_text(encoding='utf-8'))
        for i,r in enumerate(rows):
            if r['image']=='第19話_03_001.jpg':r=replace_tree(r,{'董白':'受困少女'})
            r=replace_tree(r,names);rows[i]=r
            if folder=='drafts':
                r['fields'][3]=r['fields'][3].replace('，均为非性化惊叫','')
        f.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def edit(folder,page,fn):
    p=O/folder/f'{page:02}.json';rows=json.loads(p.read_text(encoding='utf-8'));fn(rows);p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
edit('drafts',17,lambda rows:rows[0].update(new_clip=True))
edit('drafts',21,lambda rows:rows[-1].update(new_clip=True))
def camera(rows):
    s=rows[-1];s['fields'][0]='全景缓慢前推，黑袍来者在画面中央远处，宽地面在前层，巨大岩壁在后方；人物比例逐渐增大，最后在人物与岩脚薄雾均清楚的全景中稳定，双脚始终可见。'
    s.update(camera_opening='黑袍背影处于岩壁前远层，地面前景宽。',camera_landing='前推后稳定在背影与岩脚薄雾均清楚的全景，双脚完整。')
edit('drafts',16,camera)
def tracking(rows):
    rows[0]['fields'][0]+='最后在手部位于左下前层时停住跟拍，头部与近臂保持清楚。'
    rows[0].update(camera_opening='低位头部中央，伸出的近臂指向左下前层。',camera_landing='手部位于左下前层，头与近臂均清楚，跟拍收稳。')
edit('drafts',20,tracking)
def geometry(rows):
    p=rows[1]
    p['composition_lock']='刀尖与兜帽边缘极近景，灰色兜帽曲面占画面左侧，黑色尖刃从右侧抵近帽缘，中央窄隙与少量小圆粒清楚。'
    p['source_facts']=dict(entities=['灰色兜帽曲面','黑色尖刃','细白短线','小圆粒'],actions=['尖刃停在兜帽边缘近处'],relations=['帽缘左侧，尖刃右侧，中间窄隙'])
    p['plan']=P('刀刃快速劈落。',['刀尖在帽缘近处急停，细白短线与小圆粒沿惯性散开，刃尖微颤后稳定。'],'同次攻击转为近距威胁，未出现刺入。','刀尖停在帽缘近处，窄隙保持。')
    p['continuity']='21_002举刃、22_001下落、此格急停，22_004压制结果；23_004进一步看清帽缘与刀尖间隙。'
    p['admission']='原尺寸及23_004邻近构图确认目标为兜帽边缘，刀尖停在近处；不将细白短线或清硬音效当作身体刺入、硬质皮肤或伤口证据。'
    p['original_resolution_reason']='核对刀尖、灰色帽缘与窄隙；结合23_004修订早期硬质曲面与碰撞解释为抵近急停。'
edit('observations',22,geometry)
def geometry_text(rows):
    s=rows[1];s['fields'][0]='固定刀尖与兜帽边缘极近景，灰色兜帽曲面占画面左侧，黑色尖刃从右侧抵近帽缘，中央窄隙与少量小圆粒清楚。'
    s['fields'][1]='黑色刀尖在兜帽边缘近处急停，细白短线短促闪过，少量小圆粒沿原来下落的惯性散开。刃尖微颤后稳定，窄隙始终保持，刀没有刺入。'
    s['fields'][4]='刀尖细白亮边短促闪过，帽缘灰色块面保持稳定，亮点随急停迅速收暗。'
    s['fields'][5]='一声短促清硬刃响，刀面微鸣随后收短。'
edit('drafts',22,geometry_text)
phases={'06_001':'middle','06_004':'middle','18_001':'middle','20_001':'middle','20_002':'contact','20_003':'middle','21_002':'middle','22_001':'middle','22_002':'endpoint','23_001':'middle','26_002':'middle','26_003':'result'}
for f in sorted((O/'observations').glob('*.json')):
    rows=json.loads(f.read_text(encoding='utf-8'))
    for p in rows:
        k=p['image'][5:11]
        if k in phases:p['anchor_phase']=phases[k]
    f.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
