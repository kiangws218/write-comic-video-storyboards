from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,re,hashlib,shutil,sys,subprocess,zipfile

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
sys.path.insert(0,str(REPO/'tests/results/gen2.8/ep018-019-brow-revision'))
from prepare_review import parse,FIELDS
from finish_delivery import category,target as warning_target

PRIOR='2026-10-10_Gen2.8_眉形表演修订'
DELIVERY='2026-10-11_Gen2.8_角色身份修订'
MAPPING=REPO/'comic-workspace/character-references/角色映射.md'
SKILL=Path(r'C:\Users\86135\.codex\skills\write-comic-video-storyboards-gen2-8')
BASE='b56148232717979e8b04a36b8191cf56df5c74a8'

# Actual current-view observations, written after viewing the panels and four reference originals.
OBSERVATIONS={18:{
'02_002':'董白双马尾、近脸浅色束发与无袖高领；左后守卫面甲为Y形面缝，不是三槽面甲。',
'02_003':'董白高领与双马尾侧背轮廓；守卫仍为Y形面缝、分节板甲，不匹配青梅男参考。',
'03_002':'董白两侧长马尾与无袖背面；左方守卫分节背甲，保留未确认姓名的稳定代称。',
'09_003':'已批准头部取景可见齐刘海、长脸侧束发与惊恐侧脸；与后续单马尾女子头部锚点相容，未见董白的近脸浅色挑染。',
'13_003':'面盔正面三道横槽与侧部连接结构吻合青梅男；衣物状态仍按本格，不强加参考袍服。',
'14_001':'青梅男侧盔三道横槽和圆形铰点；后层光头宽躯轮廓与欧迈及相邻正面头部锚点相接。',
'14_002':'光头、厚重眉眼、宽鼻大下颌、窄眼与露齿轮廓对应欧迈及；保留当前尖下巴须。',
'15_002':'近侧面甲三道横槽与圆形连接点对应青梅男。',
'15_003':'欧迈及宽额、窄眼、宽下颌与尖下巴须，当前角度与14_002同一头部设计。',
'15_004':'三槽面甲正面、两侧圆形铰点对应青梅男。',
'16_001':'左侧为三槽面甲；右后头部有单束高马尾、齐刘海与脸侧长束发，对应青梅女，非董白双马尾。',
'16_002':'青梅女侧脸：耳前长发束、齐刘海、头后单束发轮廓；没有董白的浅色近脸发束。',
'16_003':'眼部极近裁切延续青梅女的刘海与耳前长发束，眼形与16_002相符；不补不可见马尾。',
'17_001':'青梅男三道横槽面甲正面，铰点与侧部轮廓相符。',
'17_003':'欧迈及窄眼、厚重眼下褶皱、鼻根与宽面部裁切相符。',
'18_002':'青梅女完整侧脸、齐刘海、耳前长束发及后方单马尾轮廓清楚。',
'18_003':'青梅女侧面嘴鼻局部与垂下的耳前长束发相接；不借近景新增双马尾。',
'19_002':'青梅男三槽面甲正面与圆形侧部铰点；当前汗点与暴露肩部状态保留。',
'19_003':'同一三槽面甲沿侧部铰接点掀起，露出嘴与下颌；这是青梅男当前盔面状态。',
'20_001':'欧迈及光头、窄眼褶纹、宽鼻、尖下巴须与前述头部一致。',
'20_002':'前层齐刘海女子无浅色挑染；右后是三槽面甲，核为青梅女与青梅男；保持头部安全取景。',
'21_001':'欧迈及的眼部与鼻根褶纹极近裁切；两位青梅角色的声音在画外，不能画入本镜。',
'21_002':'近拳厚大，与同格后层欧迈及宽躯及青梅男三槽面甲的已有握持场面对应；不新增攻击结果。',
'21_003':'青梅男同一三槽面甲与侧部铰点，当前面盔掀起和头部反应保留。',
'22_001':'女子头后单个高束马尾、齐刘海、两侧耳前束发明确对应青梅女；撤回双马尾描述。',
},19:{
'02_002':'欧迈及宽面部、窄眼与深褶纹的局部头部，与18话21_001设计连续。',
'02_003':'欧迈及光头、宽面部、窄眼、宽躯；保留源格断端，不因命名更改伤势。',
'03_001':'仅原图跌落/局部边缘与两声惊叫，现稿为空镜；两声原归属分别沿用三槽面甲人物与单马尾女子，统一青梅男/女，不声称两人出现在空镜。',
'03_002':'局部缠柄、手与无袖黑色短装腰腿对应已确认董白的持刀视图；不混入青梅女的宽袖交领袍。',
'03_003':'左前无袖高领黑短装腰腿与董白同一视图链；右后欧迈及光头宽躯，与02_003/04_001对应。',
'04_001':'欧迈及光头侧面、厚重眉眼、宽鼻与颊线，当前原图不改。',
'04_002':'董白双长马尾、近脸浅色束发、无袖高领短装与缠柄明确匹配参考。',
'04_003':'近层三槽面甲与圆形侧部结构对应青梅男；右后齐刘海女子头部与26_001单马尾女子相符，求助声归青梅女。',
'05_001':'粗大手掌局部属于原稿已锁定欧迈及的当前动作，不从手部裁切补出脸或新事件。',
'05_002':'欧迈及光头宽躯背侧与厚大近手，头/颈/躯干轮廓与03_003一致。',
'05_003':'欧迈及窄眼、宽面颊与露齿嘴形对应已确认头部。',
'06_001':'董白无袖高领短装与当前露指手套局部；保留既有道具操作，不把手套设为其他角色装备。',
'06_002':'董白双马尾、近脸浅色发束与高领衣，近手握缠柄明确。',
'07_001':'董白双马尾、无袖高领、两手刀与鞘；原动作不改。',
'07_002':'董白双马尾与近脸浅色发束、高领黑短装，并有原漫画董白介绍标签，明确保留董白。',
'25_001':'宽大的光头兽人、宽肩厚躯与粗大手，当前黑脸白眼为压暗表现，沿用欧迈及身份；左前双马尾、高领黑短装为董白。只命名当前已显示的大体型，不补变形过程。',
'25_002':'董白耳前浅色发束与高领黑衣、握柄近手清楚；不能因同为黑发女子改成青梅女。',
'25_003':'右前为青梅男三槽面甲/侧部铰点，左中董白双马尾/高领无袖，后层光头宽躯为欧迈及。三人分别登记。',
'26_001':'齐刘海与单个高束马尾明确、耳前黑发束，无董白的浅色挑染，匹配青梅女。仅核对已批准头脸取景。',
'26_002':'董白的高领无袖装与近脸浅色束发、当前握刀/鞘两手，保持董白。',
'26_003':'董白双马尾、近脸浅色挑染、高领黑短装与刀/鞘，画外补充说话人来自26_001青梅女。',
}}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def jwrite(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def late18(image):
    m=re.search(r'第18話_(\d+)_',image);return m and int(m[1])>=9
def transform_text(text,ep,late=True):
    pairs=[]
    if ep==18 and late:
        pairs=[('全盔守卫','青梅男'),('守卫','青梅男'),('董白','青梅女'),('秃顶男子','欧迈及'),('男子','欧迈及'),
            ('双马尾在两侧后方','高束马尾与脸侧发束留在后方'),('双马尾分列侧后','高束马尾与脸侧发束留在侧后'),('双马尾','高束马尾')]
    elif ep==19:
        pairs=[('全盔守卫','青梅男'),('全盔者','青梅男'),('守卫','青梅男'),('受困少女','青梅女'),('求助少女','青梅女'),('求助者','青梅女'),
            ('秃顶男子','欧迈及'),('男子','欧迈及'),('巨型兽人','欧迈及'),
            ('青梅女另列，身份未确认。','青梅女另列，已按单马尾与头部锚点确认，见本轮identity-review.json。')]
    def replace(part):
        for old,new in pairs:part=part.replace(old,new)
        return part
    # Preserve dialogue itself, including named speech timing quotations.
    return ''.join(p if i%2 else replace(p) for i,p in enumerate(re.split(r'(“[^”]*”|「[^」]*」)',text)))

def walk(value,ep,late=True):
    if isinstance(value,str):return transform_text(value,ep,late)
    if isinstance(value,list):return [walk(v,ep,late) for v in value]
    if isinstance(value,dict):return {k:(v if k in ('source_text','script_text','jp','source_integrity') else walk(v,ep,late)) for k,v in value.items()}
    return value

def update_master():
    text=MAPPING.read_text(encoding='utf-8')
    if '2026-10-11｜18、19话发生处复查' in text:return
    text=text.replace('更新日期：2026-10-11。版本：1。','更新日期：2026-10-11。版本：2。',1)
    additions={
        'C004':'18话前半的双马尾、高领无袖人物和19话持刀人物仍为董白（18话02_002/003、03_002；19话04_002、06_002、07_002、25_002、26_002/003）。18话后半受困女子不是董白，已在最新制作稿更正为C005。',
        'C005':'18话16_001/002、18_002、20_002、22_001及19话26_001复查显示高束单马尾、齐刘海与耳前黑发束，匹配青梅女；18话旧“董白”、19话旧“受困少女/求助者”在本次18、19话制作稿及当前台账已纠正。嘴/眼局部按当前裁切与同一头部锚点核对，不补画完整发型或参考衣物。',
        'C006':'18话13_003、15_002/004、17_001、19_002/003、21_003及19话04_003、25_003的三槽面甲、侧部圆形铰点与青梅男匹配。本次18、19话发生处已改名；18话02_002/003的Y形面缝全甲守卫不同于此设计，保留独立稳定代称“全盔守卫”，不认作青梅男或豪斯。',
        'C012':'18话14_002、15_003、17_003、20_001、21_001及19话02_002/003、04_001、05_002/003的光头、窄眼厚褶、宽面下颌与宽躯对应欧迈及。19话25_001/003的同线宽大兽人沿用C012；黑脸白眼及显著体型按当前源格保留，不依据名字补造变形/再生镜头。旧“秃顶男子/巨型兽人”在当前稿件归并为欧迈及；不与角盔欧铂合并。'
    }
    for cid,note in additions.items():
        m=re.search(r'^### '+cid+r'｜[^\n]+\n',text,re.M);assert m
        start=m.end();next_heading=text.find('\n### ',start)
        assert next_heading!=-1
        text=text[:next_heading]+'\n- 2026-10-11｜18、19话发生处复查：'+note+'\n'+text[next_heading:]
    text+='\n2026-10-11追加维护：版本2仅补充本次18、19话身份发生处的图像核对与误认撤回。前述“本轮未修改既有脚本”指版本1建档阶段；本次18、19话修订完成，16话仍不在本次改稿范围。\n'
    MAPPING.write_text(text,encoding='utf-8')

def registry(ep,old):
    refs='comic-workspace/character-references/turnarounds/'
    rows=[{'id':'C001','canonical_name':'青','reference_paths':[refs+'青.png'],'traits':'尖耳、浅色长发及卷束、齐刘海','status':'visually_confirmed'},
        {'id':'C002','canonical_name':'春子','reference_paths':[refs+'春子.png'],'traits':'长直发、平刘海、宽松深色衣','status':'visually_confirmed'},
        {'id':'C004','canonical_name':'董白','reference_paths':[refs+'董白.png'],'traits':'双侧高长马尾、近脸浅色挑染、无袖高领短装','status':'visually_confirmed'},
        {'id':'C005','canonical_name':'青梅女','reference_paths':[refs+'青梅女.png'],'traits':'单个高束马尾、齐刘海、耳前长黑发束；参考为浅边交领宽袖袍，当前服装状态按源格','status':'visually_confirmed'},
        {'id':'C006','canonical_name':'青梅男','reference_paths':[refs+'青梅男.png'],'traits':'三道横槽面甲、侧部圆形铰点；参考围巾、肩甲、宽袖袍，当前衣物/掀盔状态按源格','status':'visually_confirmed'},
        {'id':'C012','canonical_name':'欧迈及','reference_paths':[refs+'欧迈及.jpg'],'traits':'光头、窄眼厚褶、宽面大下颌、厚实宽躯；当前尖须、压暗脸部及体型按源格','status':'visually_confirmed'}]
    if ep==18:
        rows.append({'id':'closed_helmet_guard_ep18','canonical_name':'全盔守卫','reference_paths':[],
            'traits':'18话前半Y形面缝、分节全身板甲；与三槽面甲的青梅男不同','status':'stable_role_label',
            'identity_audit':'02_002/003、03_002已复查；未由无名盔甲角色强配项目姓名。'})
    else:rows.extend(deepcopy(r) for r in old if r['id']=='hooded_visitor')
    return rows

def create():
    update_master();summaries=[]
    for ep in (18,19):
        root=REPO/f'comic-workspace/episodes/ep-{ep:03}'
        current=root/f'storyboards/current/第{ep}话_制作分镜_Gen2.8.md'
        base=HERE/f'baseline/ep-{ep:03}'
        if not base.exists():base=root/f'storyboards/deliveries/{PRIOR}'
        before_text=(base/current.name).read_text(encoding='utf-8')
        before=parse(before_text);old_shots={s['target']:s for s in before}
        clip=0;shot_target=None;lines=[]
        for line in before_text.splitlines():
            m=re.match(r'## 【片段(\d+)】',line)
            if m:clip=int(m[1])
            m=re.match(r'\*\*分镜(\d+)（',line)
            if m:shot_target=f'片段{clip}/分镜{m[1]}'
            if line.startswith('【'):
                line=transform_text(line,ep,clip>=11)
                if ep==19 and shot_target in ('片段3/分镜1','片段6/分镜2') and line.startswith('【镜头设计】'):line=line.replace('少女','董白')
                if ep==19 and shot_target=='片段30/分镜2':line=line.replace('怪物把','欧迈及把').replace('怪物躯体','欧迈及的巨大躯体')
            lines.append(line)
        revised='\n'.join(lines)+'\n';after=parse(revised);new_shots={s['target']:s for s in after}
        changes=[]
        for a,b in zip(before,after):
            assert (a['target'],a['seconds'],a['refs'])==(b['target'],b['seconds'],b['refs'])
            assert re.findall(r'[“「](.*?)[”」]',a['fields']['台词与语气'])==re.findall(r'[“「](.*?)[”」]',b['fields']['台词与语气'])
            changed=[f for f in FIELDS if a['fields'][f]!=b['fields'][f]]
            if changed:changes.append({'target':a['target'],'seconds':a['seconds'],'fields':changed,
                'before':{f:a['fields'][f] for f in changed},'after':{f:b['fields'][f] for f in changed}})
        assert len(before)==len(after)
        ledger=json.loads((base/'source-ledger-v3.json').read_text(encoding='utf-8'))
        old_registry=deepcopy(ledger['character_registry'])
        for panel in ledger['panels']:
            applicable=ep==19 or late18(panel['image'])
            if applicable:panel.update(walk(panel,ep))
            if ep==19 and int(re.search(r'第19話_(\d+)_',panel['image'])[1])>=25:
                panel.update(walk_specific(panel,{'怪物':'欧迈及','受困者补充，身份保持待确认角色名':'青梅女补充，姓名已按共享映射与单马尾头部核对'}))
        for row in ledger['shots']:
            applicable=ep==19 or int(re.search(r'片段(\d+)',row['target'])[1])>=11
            if applicable:row.update(walk(row,ep))
            if ep==19 and int(re.search(r'片段(\d+)',row['target'])[1])>=30:
                row.update(walk_specific(row,{'怪物':'欧迈及','受困者补充，身份保持待确认角色名':'青梅女补充，姓名已按共享映射与单马尾头部核对'}))
            target=row['target'];new=new_shots[target]['fields'];old=old_shots[target]['fields']
            if new!=old:
                row['camera_decision']['opening']=new['镜头设计'];row['camera_decision']['landing']=new['镜头设计']
                for admission in row.get('action_admissions',[]):
                    if admission['claim']==transform_text(old['可见动作'],ep,applicable):admission['claim']=new['可见动作']
                if 'background_excerpt' in row:row['background_excerpt']=new['可见背景']
        for row in ledger['performance']:
            applicable=ep==19 or int(re.search(r'片段(\d+)',row['target'])[1])>=11
            if applicable:row.update(walk(row,ep))
            if ep==19 and int(re.search(r'片段(\d+)',row['target'])[1])>=30:
                row.update(walk_specific(row,{'怪物':'欧迈及'}))
            row['details']=[new_shots[row['target']]['fields']['可见动作']]
        # Body/camera excerpt normalization for the few canonical labels outside the alias replacement.
        for row in ledger['shots']:
            if ep==19 and row['target']=='片段30/分镜2':
                row.update(walk_specific(row,{'怪物把':'欧迈及把','怪物躯体':'欧迈及的巨大躯体'}))
        ledger['character_registry']=registry(ep,old_registry)
        ledger['character_registry_source']={'path':'comic-workspace/character-references/角色映射.md','version':2,
            'date':'2026-10-11','baseline_commit':BASE,'sha256':sha(MAPPING),
            'scope':'仅摘录本话出场角色，身份设计以共享映射主档为唯一维护入口；当前 pose/contact 仍以源格为准。'}
        inspections=[]
        for short,observation in OBSERVATIONS[ep].items():
            image=f'第{ep}話_{short}.jpg'
            inspections.append({'image':image,'observed':observation,'resolution':'cached 720p',
                'scope':'已批准非露骨头脸取景' if (HERE/f'inspection-head-crops/ep-{ep:03}'/image).exists() else '当前源格身份/道具归属',
                'targets':[s['target'] for s in ledger['shots'] if image in s.get('source_images',[])+s.get('derived_from',[])]})
        audit={'date':'2026-10-11','reason':'用户指出18、19话青梅男、青梅女、欧迈及与董白身份混用；使用最新共享映射复查。',
            'mapping_source':deepcopy(ledger['character_registry_source']),'previous_character_registry':old_registry,
            'previous_semantic_review':deepcopy(ledger['final_audit']['semantic_review']),
            'previous_advisory_dispositions':deepcopy(ledger.get('advisory_dispositions',[])),
            'affected_targets':[c['target'] for c in changes],'affected_images':[r['image'] for r in inspections],
            'visual_review':inspections,'reference_originals_viewed':['董白.png','青梅女.png','青梅男.png','欧迈及.jpg'],
            'decisions':['18话前半董白及Y形面缝守卫保留；后半受困者分别为青梅女/青梅男。',
                '19话受困女子归青梅女、三槽面甲人物归青梅男；持刀双马尾角色继续为董白。',
                '欧迈及的近脸、身体局部和19话后段宽大兽人归C012，保留当前压暗/体型/伤势，不新增转变机制。',
                '姓名同步至六字段、说话人、源事实、动作准入、表演卡和当前审校说明；原气泡文本与先前审阅证据保留。'],
            'design_correction':'18话后半双马尾错误随身份撤回，改为源格已见单个高束马尾；不照参考图恢复衣物。',
            'invariants':'镜数、时长、引用、实际日文语句和顺序，以及已有动作时序/眉形修订保持；仅更正人物姓名、speaker身份和身份误认带出的发型。'}
        ledger.setdefault('revision_audit',[]).append(audit)
        # Historical reviews are retained verbatim in revision_audit; current review copies use scoped names.
        sem=ledger['final_audit']['semantic_review']
        if ep==19:
            sem.update(walk(sem,ep))
            for item in sem.get('continuity',[]):
                if int(re.search(r'第19話_(\d+)_',item['image'])[1])>=25:
                    item.update(walk_specific(item,{'怪物':'欧迈及','受困者补充，身份保持待确认角色名':'青梅女补充，姓名已按共享映射与单马尾头部核对'}))
        else:
            for item in sem.get('new_continuity',[]):
                if late18(item['image']):item.update(walk(item,ep))
            for item in ledger.get('advisory_dispositions',[]):
                target=item.get('target','')
                match=re.search(r'片段(\d+)',target)
                if (match and int(match[1])>=11) or (not match and any(late18(i) for i in item.get('images',[]))):
                    item.update(walk(item,ep))
        if 'review_file' in sem:
            sem['review_file']='identity-review.json'
            sem['review_file_scope']='本轮身份复查；此前语义结论保留于revision_audit.previous_semantic_review，眉形图像记录为prior-image-reviews.json。'
        sem['identity_revision']={'status':'image_reviewed','targets':audit['affected_targets'],
            'inspection_file':'identity-review.json','mapping_version':2,'limitations':'未生成视频；未确认的前半守卫不强配姓名。'}
        dest=root/f'storyboards/deliveries/{DELIVERY}';dest.mkdir(parents=True,exist_ok=True)
        current.write_text(revised,encoding='utf-8');(dest/current.name).write_text(revised,encoding='utf-8')
        jwrite(dest/'source-ledger-v3.json',ledger);jwrite(dest/'identity-review.json',audit);jwrite(dest/'identity-changes.json',changes)
        prior=root/f'storyboards/deliveries/{PRIOR}'
        if (prior/'dialogue-mapping.json').exists():
            mapping=json.loads((prior/'dialogue-mapping.json').read_text(encoding='utf-8'));jwrite(dest/'dialogue-mapping.json',walk(mapping,ep))
        for file in ('source-integrity.json','source-package.json','source-copy-check.json','skill-sync.json'):
            if (prior/file).exists():shutil.copyfile(prior/file,dest/file)
        jwrite(dest/'dialogue-mapping-current.json',[{'image':p['image'],'bubbles':p.get('bubbles',[]),
            'dialogue_turns':p.get('dialogue_turns',[]),'coverage_groups':p.get('coverage_groups',[])} for p in ledger['panels']])
        for file in ('brow-changes.json','image-reviews.json'):
            shutil.copyfile(prior/file,dest/('prior-'+file))
        summaries.append({'episode':ep,'clips':len(set(s['target'].split('/')[0] for s in after)),
            'shots':len(after),'seconds':sum(s['seconds'] for s in after),'formal_reference_count':len(set(r for s in after for r in s['refs'])),
            'changed_shots':len(changes),'inspected_images':len(inspections),'baseline_sha256':sha(base/current.name),
            'revised_sha256':sha(current),'current':str(current),'delivery':str(dest),
            'timings_and_refs_equal':True,'japanese_quotes_equal':True,'mapping':deepcopy(ledger['character_registry_source'])})
    jwrite(HERE/'revision-summary.json',summaries)
    print(json.dumps([{k:r[k] for k in ('episode','shots','changed_shots','inspected_images')} for r in summaries],ensure_ascii=False))

def walk_specific(value,pairs):
    if isinstance(value,str):
        def replace(part):
            for old,new in pairs.items():part=part.replace(old,new)
            return part
        return ''.join(p if i%2 else replace(p) for i,p in enumerate(re.split(r'(“[^”]*”|「[^」]*」)',value)))
    if isinstance(value,list):return [walk_specific(v,pairs) for v in value]
    if isinstance(value,dict):return {k:(v if k in ('source_text','script_text','jp','source_integrity') else walk_specific(v,pairs)) for k,v in value.items()}
    return value

def finish():
    summaries=json.loads((HERE/'revision-summary.json').read_text(encoding='utf-8'))
    for result in summaries:
        ep=result['episode'];dest=Path(result['delivery']);root=dest.parents[2]
        ledger_path=dest/'source-ledger-v3.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
        proc=subprocess.run([sys.executable,'-X','utf8',str(SKILL/'scripts/validate_storyboard.py'),result['current'],
            '--max-seconds','15','--image-dir',str(REPO/f'tests/results/gen2.8/ep{ep:03}-full/analysis-proxies'),
            '--source-ledger',str(ledger_path),'--require-source-ledger'],capture_output=True,encoding='utf-8')
        (dest/'validation.txt').write_text(proc.stdout+proc.stderr,encoding='utf-8')
        assert proc.returncode==0,proc.stdout[-7000:]+proc.stderr
        assert '0个错误' in proc.stdout
        warnings=[w for w in proc.stdout.splitlines() if w.startswith('警告：')]
        old_reviews=json.loads((root/f'storyboards/deliveries/{PRIOR}/warning-dispositions.json').read_text(encoding='utf-8'))['dispositions']
        changes=json.loads((dest/'identity-changes.json').read_text(encoding='utf-8'));changed={x['target'] for x in changes}
        rows={s['target']:s for s in ledger['shots']};decisions=[]
        for w in warnings:
            t=warning_target(w);c=category(w)
            prior=next((r for r in old_reviews if r['class']==c and r['target']==t),None)
            assert prior,(ep,'Unreviewed new warning',w)
            item={'warning':w,'target':t,'class':c,'disposition':'reviewed','prior_conclusion':prior['conclusion']}
            applicable=ep==19 or (t and int(re.search(r'片段(\d+)',t)[1])>=11)
            item['conclusion']=transform_text(prior['conclusion'],ep,applicable)
            if t in changed:
                item['identity_revision']='对照当前源格与共享映射确认姓名；语句、表演时序和取景保持，非露骨头部场面只核对已批准范围。'
            decisions.append(item)
        jwrite(dest/'warning-dispositions.json',{'errors':0,'warning_count':len(warnings),
            'classes':dict(Counter(category(w) for w in warnings)),'dispositions':decisions})
        result.update({'structural_errors':0,'warning_count':len(warnings),'warning_classes':dict(Counter(category(w) for w in warnings)),
            'video_generated':False,'source_audit':'affected identity occurrences visually reviewed; raw bubbles/integrity retained'})
        jwrite(dest/'revision-summary.json',result)
        lines=[f'# 第{ep}话角色身份修订对照','',f'使用共享角色映射版本2（2026-10-11），复查{result["inspected_images"]}张源格/头部取景，修订{result["changed_shots"]}镜。',
            '',f'完整稿仍为{result["clips"]}片段、{result["shots"]}分镜、{result["seconds"]}秒。镜数、时长、引用与日文语句逐项比对保持一致；台词说话人标签随身份修正。',
            '', '18话前半Y形面缝全盔守卫保留独立代称；后半三槽面甲人物为青梅男。青梅女的单马尾不再写成董白的双马尾。',
            '', '19话持刀双马尾人物仍为董白；三槽面甲人物为青梅男，受困单马尾女子为青梅女。欧迈及在两话的局部及大体型场面统一命名，保留当前源格造型，不补转变机制。',
            '',f'结构与台账0错误，{len(warnings)}条提示逐镜沿用/更新已有处置。没有生成视频。','']
        for change in changes:
            lines.extend([f'## {change["target"]}（{change["seconds"]}秒）',''])
            for field in change['fields']:
                lines.extend([f'**{field}**','',f'- 修订前：{change["before"][field]}','',f'- 修订后：{change["after"][field]}',''])
        (dest/'角色身份修订对照.md').write_text('\n'.join(lines),encoding='utf-8')
        (dest/'交付说明.md').write_text('\n'.join([f'# 第{ep}话完整分镜｜角色身份修订','',
            f'完整制作稿：第{ep}话_制作分镜_Gen2.8.md；{result["clips"]}片段、{result["shots"]}镜、{result["seconds"]}秒。',
            '', '姓名/人物定义复用共享角色映射版本2；本话台账仅摘录出场者及实际匹配记录。修订后的制作稿、说话人映射、源事实、表演卡与准入摘录保持对应。',
            '', '镜头安排、时长、日文台词内容与眉形表演保留；只修复姓名和身份误认导致的发型。既有非露骨改编边界保持。',
            '',f'结构与台账0错误，{len(warnings)}条启发式提示逐项处置；未生成视频。',
            '', 'identity-review.json记录原图/参考对照；identity-changes.json及角色身份修订对照.md记录前后差异。dialogue-mapping-current.json为本轮完整气泡归属。',
            '', 'prior-*及revision_audit中的旧记录为修订历史，保留原姓名以便追踪，不作为当前人物命名。前轮交付目录整体保留；current/已更新为本轮完整稿。',
            '', '漫画原图、人设原件及Gen2.8技能规则没有修改。','']),encoding='utf-8')
        status=root/'STATUS.md';text=status.read_text(encoding='utf-8').replace(PRIOR,DELIVERY)
        note=f'- 2026-10-11角色身份修订：使用共享映射版本2；复查{result["inspected_images"]}张，更新{result["changed_shots"]}镜，台词语句/时长/引用保持，人物与说话人标签已同步。'
        if note not in text:text+='\n'+note+'\n'
        status.write_text(text,encoding='utf-8')
        pack=dest/f'第{ep}话_完整分镜与身份审校_Gen2.8.zip'
        with zipfile.ZipFile(pack,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(dest.rglob('*')):
                if file.is_file() and file!=pack:archive.write(file,file.relative_to(dest).as_posix())
        with zipfile.ZipFile(pack) as archive:
            assert archive.testzip() is None
            assert archive.read(Path(result['current']).name)==Path(result['current']).read_bytes()
        print(ep,'0 errors;',len(warnings),'reviewed advisories;',result['changed_shots'],'shots revised')
    jwrite(HERE/'revision-summary.json',summaries)

if __name__=='__main__':{'create':create,'finish':finish}[sys.argv[1]]()
