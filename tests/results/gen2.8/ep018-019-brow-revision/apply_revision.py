"""Apply the pre-authored, image-reviewed eyebrow revision; preserve approved history."""
from pathlib import Path
from copy import deepcopy
import json, hashlib, re, shutil
from prepare_review import HERE, REPO, DATES, FIELDS, parse

DELIVERY = '2026-10-10_Gen2.8_眉形表演修订'

# Static observations from the open images. These are not animation transitions.
SHAPES = {
18: {
'第18話_01_001.jpg': ('relations', '董白的眉毛大部被刘海遮挡'),
'第18話_01_003.jpg': ('actions', '青露出的双眉内端朝眉间压低'),
'第18話_02_001.jpg': ('actions', '春子露出的单侧眉头上挑，青可见眉头向内侧压低'),
'第18話_02_004.jpg': ('actions', '青露出的眉头上挑，春子露出的眉头略翘'),
'第18話_04_001_下格.jpg': ('relations', '春子的眉部大多被刘海遮住'),
'第18話_05_003.jpg': ('actions', '青的眉头压低并向中间靠拢'),
'第18話_06_003.jpg': ('actions', '青可见的眉头向内侧压低'),
'第18話_06_004.jpg': ('actions', '青露出的近侧眉头向内侧压低'),
'第18話_07_001.jpg': ('actions', '青的眉头向内侧压低'),
'第18話_07_002.jpg': ('actions', '春子露出的近侧眉头翘起，眉身弯曲'),
'第18話_07_003.jpg': ('actions', '青的刘海间露出一小段抬高的眉线'),
'第18話_20_001.jpg': ('actions', '男子眉间褶皱挤紧'),
'第18話_21_001.jpg': ('actions', '男子眉间与鼻根褶纹密集'),
},
19: {
'第19話_02_002.jpg': ('actions', '男子眉间有紧皱的褶纹'),
'第19話_08_004.jpg': ('actions', '春子露出的单侧眉头略上挑'),
'第19話_09_004.jpg': ('actions', '春子露出的单侧眉头略上挑'),
'第19話_10_003.jpg': ('actions', '青露出的近侧眉头压低'),
'第19話_11_001.jpg': ('actions', '青露出的眉头压低'),
'第19話_11_002.jpg': ('actions', '春子露出的单侧眉头轻翘'),
'第19話_14_001.jpg': ('actions', '春子露出的眉头略翘，眉身弯曲'),
'第19話_15_003.jpg': ('actions', '春子露出的单侧眉头上挑'),
'第19話_19_002.jpg': ('actions', '青露出的近侧眉毛抬高'),
'第19話_19_003.jpg': ('actions', '春子露出的眉头上挑，眉身弯曲，近侧眼睑压低'),
'第19話_23_002.jpg': ('actions', '青画面左侧露出的眉头压低，另一侧眉线较平'),
'第19話_23_003.jpg': ('actions', '春子露出的眉头上挑，眉身弯曲'),
}}

# Replace only erroneous source atoms; retain unrelated pose/contact facts.
FACT_REPLACEMENTS = {
18: {
'第18話_06_004.jpg': {
'青睁大眼睛张口，眉间松开': '青睁大眼睛张口，露出的近侧眉头向内侧压低',
'青双手在胸前交叠，指端较松': '青双手在胸前交叠',
}},
19: {
'第19話_15_003.jpg': {'春子半垂眼皱眉': '春子半垂眼，露出的单侧眉头上挑'},
'第19話_19_003.jpg': {'春子皱眉看向右': '春子看向右，露出的眉头上挑、眉身弯曲，近侧眼睑压低'},
'第19話_23_003.jpg': {'春子半垂眼皱眉': '春子半垂眼，露出的眉头上挑、眉身弯曲'},
}}

# Small edits to existing cards preserve the approved task/body performance.
CARD_EDITS = {
18: {
'片段1/分镜1': {'应答时略抬眉，头向前倾': '应答时头向前倾'},
'片段1/分镜2': {'追问时她又向前探出肩膀，曲起的手指': '追问时她又向前探出肩膀，眉头压低并向中间靠拢，曲起的手指', '青仍紧张地张口': '青仍压低眉头，紧张地张口'},
'片段1/分镜3': {'春子半垂眼，前臂': '春子半垂眼，露出的眉头上挑，前臂', '青紧皱眉头说完劝告': '青的眉头随着劝阻压低，说完劝告', '春子半垂眼把脸偏向左侧外': '春子维持露出的眉头上挑，半垂眼把脸偏向左侧外'},
'片段3/分镜2': {'眉梢抬起': '露出的眉头上挑', '春子不耐烦地歪头': '春子露出的眉头仍略翘着，不耐烦地歪头'},
'片段5/分镜3': {'，眉梢抬起': ''},
'片段6/分镜1': {'再护着她转脸朝右质问': '再护着她转脸朝右质问，眉头压低并向中间靠拢', '青搭靠并望向右后方': '青搭靠并望向右后方，眉头仍压低'},
'片段6/分镜2': {'眉头绷紧': '眉头压低', '青望向右侧外': '青仍压着眉头望向右侧外'},
'片段7/分镜2': {'接着皱紧眉向左侧外威胁': '接着压着眉头向左侧外威胁', '眉眼绷紧': '眉头向内侧压低'},
'片段8/分镜1': {'眉眼重新压紧发问': '眉头仍向内侧压低，急切发问', '眉眼急切': '眉头仍压低，神情急切'},
'片段8/分镜2': {'眼睛半垂。': '眼睛半垂，露出的近侧眉头翘起、眉身弯着。', '呼吸渐缓': '呼吸渐缓，上挑的弯眉形持续', '半垂眼和绷着的嘴角延续': '半垂眼、上挑的近侧弯眉与绷着的嘴角延续'},
'片段8/分镜3': {'眉梢扬起': '刘海间露出的短眉段抬高', '眉梢扬着': '露出的短眉段抬高'},
'片段18/分镜2': {'皱紧眉头': '挤紧眉间的褶皱'},
'片段20/分镜1': {'眉头越压越低': '眉间褶纹越挤越紧', '眉间绷紧': '眉间褶纹挤紧'},
},
19: {
'片段1/分镜2': {'眉间开始松动成困惑': '眉间紧皱的褶纹略松开，迟来的困惑从眼神里显出来', '眉间疑惑尚未展开': '眉间褶纹略松开，疑惑留在眼神里'},
'片段8/分镜3': {'春子盯着刚否认的青。': '春子半垂着眼，露出的眉头略挑着，看向前方。', '视线没有移开': '视线没有移开，略挑的眉头持续', '半垂的眼仍盯着前方。': '半垂的眼仍盯着前方，露出的眉头仍略挑着。'},
'片段10/分镜2': {'春子留在左侧听完': '春子在左侧维持单侧露出的眉头略上挑，听完', '春子留在左侧。': '春子留在左侧，半垂眼与微挑的眉头持续。'},
'片段13/分镜1': {'闭眼气急地叫她别说坏话': '压低近侧眉头，闭眼气急地叫她别说坏话', '握布未松': '近侧眉头仍压低，握布未松'},
'片段14/分镜1': {'她闭眼用力争辩': '她延续压低的眉头，闭眼用力争辩', '嘴慢慢合起': '眉头仍压低，嘴慢慢合起'},
'片段15/分镜1': {'她把头小幅转正': '她维持单侧露出的眉头轻翘，把头小幅转正', '春子面向前，目光平稳': '春子面向前，目光平稳，露出的眉头仍轻翘'},
'片段20/分镜1': {'春子正听青解释': '春子露出的眉头略翘、眉身弯着，正听画外解释', '仍不热络': '仍不热络，略翘的弯眉形持续'},
'片段26/分镜1': {'她眼睛仍圆着': '她眼睛仍圆着，露出的近侧眉毛保持抬高', '青侧脸朝左，等待解释': '青侧脸朝左，露出的近侧眉毛仍抬高，等待解释'},
'片段29/分镜1': {'眼睛圆着': '眼睛圆着，画面左侧露出的眉头压低，另一侧眉线较平', '手仍抬在下缘': '手仍抬在下缘，不对称眉形持续'},
'片段29/分镜2': {'眉间一直绷着': '露出的眉头一直翘起、眉身弯着', '警惕未松': '警惕未松，露出的眉头仍上挑'},
}}

NEW_CARDS = {
(18,'片段7/分镜3'): {
'opening': '青的交叠双手仍扣在口前，眉头压低，威胁尚未完成。',
'beats': ['画外制止截住威胁，交叠双手落到胸前，同时眼睛睁圆、嘴停在小张的位置；近侧眉头仍向内侧压着，惊讶没有抹掉怒意。'],
'coupling': '回应制止的是手位与眼口，保持原有交叠关系；不把错愕误演成眉间放松或指端松开。',
'landing': '青略朝左侧外，双手在胸前保持交叠，近侧眉头仍压低，圆眼小张口。'},
(19,'片段22/分镜1'): {
'opening': '春子半垂着眼听画外追问，露出的眉头原本略翘，嘴唇闭着。',
'beats': ['第一问后，露出的眉头再挑高一点，抵达本格明确的单侧上挑眉形。', '两问之间沉默一拍；第二问继续时，上挑眉头、半垂眼与闭口一起持续，困惑留在脸上。'],
'coupling': '青连续求证，春子沉默回应；眉头局部变化承接提问，持续状态承接等待，未知身份继续保留。',
'landing': '春子露出的单侧眉头保持上挑，半垂眼望向前方，嘴唇闭着。'},
(19,'片段26/分镜2'): {
'opening': '春子露出的眉头已经朝上挑着、眉身弯曲，近侧眼睑压低，警觉地看向右侧外。',
'beats': ['说出否定时目光不移开，上挑眉形与压低的近侧眼睑持续至镜尾。'],
'coupling': '2秒用于对青的惊讶作出警觉的短否定，并把这份警觉留给下一格动作；不重复挑眉或强行回落。',
'landing': '目光仍朝画面右侧外，上挑的眉头和紧张眼神持续，嘴在画外。'},
}

SPECIAL = {
18: {
'第18話_06_004.jpg': {
'松叠双手': '交叠双手',
'刚要发作的准备被打断，手势松下来但不回到中性站姿。': '威胁被制止，交叠双手从口前落到胸前，圆眼中仍有压低眉头留下的怒意。',
'交握手从紧到松的变化由06_003和本格手形对照支持；局部脸部反应以本格圆眼张口为结果。': '06_003交叠双手在口前，本格交叠双手位于胸前；以有界的短下降连接两格手位，手仍交叠。眼睛睁圆、嘴小张以本格为结果，近侧眉头始终压低，不推断指端松开。',
'06_003同一手势延续，不重做抬手；06_004只松指并接到07_001的转问。': '06_003口前交叠手势延续；06_004在2秒内把双手落到胸前，与圆眼张口同时发生；接到07_001分开双手、转问春子，眉头仍压低。',
},
'第18話_07_001.jpg': {'06_004松叠双手后': '06_004胸前双手仍交叠，本镜'},
'第18話_07_003.jpg': {'已见眼睛、眉梢与汗珠': '已见眼睛、刘海间露出的短眉段与汗珠'},
'第18話_20_001.jpg': {'眉头紧皱': '眉间褶皱挤紧', '源图皱眉咬牙': '源图眉间褶皱挤紧、咬牙'},
'第18話_21_001.jpg': {'眉头压低': '眉间与鼻根褶纹密集'},
},
19: {
'第19話_15_003.jpg': {'半垂眼与微皱眉清楚': '半垂眼与露出的单侧上挑眉头清楚'},
'第19話_19_003.jpg': {'眉抬起': '露出的眉头上挑、眉身弯曲，近侧眼睑压低'},
'第19話_23_002.jpg': {'浅发两側。': '浅发两側；头略向画面右侧倾斜，画面左侧露出的眉头压低，另一侧眉线较平。'},
'第19話_23_003.jpg': {'眉间紧起': '露出的眉头上挑、眉身弯曲'},
}}

def walk_replace(value, replacements):
    if isinstance(value,str):
        for old,new in replacements.items(): value=value.replace(old,new)
        return value
    if isinstance(value,list): return [walk_replace(x,replacements) for x in value]
    if isinstance(value,dict): return {k:walk_replace(v,replacements) for k,v in value.items()}
    return value

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def run():
    reviews=json.loads((HERE/'image-reviews.json').read_text(encoding='utf-8'))
    results=[]
    for ep in (18,19):
        base=HERE/f'baseline/ep-{ep:03}'
        root=REPO/f'comic-workspace/episodes/ep-{ep:03}'
        current=root/f'storyboards/current/第{ep}话_制作分镜_Gen2.8.md'
        old_text=(base/current.name).read_text(encoding='utf-8')
        before=parse(old_text); old_by={s['target']:s for s in before}
        selected=[r for r in reviews if r['ep']==ep]
        patches=[p for r in selected for p in r['patches']]
        grouped={t:[p for p in patches if p['target']==t] for t in dict.fromkeys(p['target'] for p in patches)}
        new_lines=[]; target=None;clip=0
        for line in old_text.splitlines():
            m=re.match(r'## 【片段(\d+)】',line)
            if m:clip=int(m[1])
            m=re.match(r'\*\*分镜(\d+)（',line)
            if m:target=f'片段{clip}/分镜{m[1]}'
            m=re.match(r'【([^】]+)】：(.*)',line)
            if m:
                field=m[1]; value=m[2]
                for patch in grouped.get(target,[]):
                    if patch['field']==field:
                        assert value.count(patch['old'])==1,(ep,target,field,patch['old'])
                        value=value.replace(patch['old'],patch['new'])
                line=f'【{field}】：{value}'
            new_lines.append(line)
        new_text='\n'.join(new_lines)+'\n'; after=parse(new_text); new_by={s['target']:s for s in after}
        changes=[]
        for a,b in zip(before,after):
            assert (a['target'],a['seconds'],a['refs'])==(b['target'],b['seconds'],b['refs'])
            assert a['fields']['台词与语气']==b['fields']['台词与语气']
            changed=[f for f in FIELDS if a['fields'][f]!=b['fields'][f]]
            assert set(changed)=={p['field'] for p in grouped.get(a['target'],[])},(ep,a['target'],changed)
            if changed: changes.append({'target':a['target'],'seconds':a['seconds'],'fields':changed,
                'before':{f:a['fields'][f] for f in changed},'after':{f:b['fields'][f] for f in changed}})
        assert len(after)==len(before)
        ledger=json.loads((base/'source-ledger-v3.json').read_text(encoding='utf-8'))
        panels={p['image']:p for p in ledger['panels']}
        shots={s['target']:s for s in ledger['shots']}
        perf={p['target']:p for p in ledger['performance']}
        for image,replacements in FACT_REPLACEMENTS.get(ep,{}).items():
            panels[image]['source_facts']=walk_replace(panels[image]['source_facts'],replacements)
            for row in ledger['shots']:
                if image in row.get('source_images',[])+row.get('derived_from',[]):
                    row['fact_claims']=walk_replace(row['fact_claims'],replacements)
                    if 'risk_basis' in row: row['risk_basis']=walk_replace(row['risk_basis'],replacements)
        # Source observations and occlusion, separate from the subsequent plan.
        for image,(kind,atom) in SHAPES[ep].items():
            if atom not in panels[image]['source_facts'][kind]:panels[image]['source_facts'][kind].append(atom)
        for image,replacements in SPECIAL.get(ep,{}).items():
            panels[image].update(walk_replace(panels[image],replacements))
            for row in ledger['shots']:
                if image in row.get('source_images',[])+row.get('derived_from',[]):row.update(walk_replace(row,replacements))
        # Also repair stale forward/backward continuity summaries, scoped to the exact claims.
        if ep==18:
            repl={**SPECIAL[18]['第18話_06_004.jpg'],**SPECIAL[18]['第18話_07_001.jpg']}
            ledger['final_audit']=walk_replace(ledger['final_audit'],repl)
        for target in grouped:
            old,new=old_by[target],new_by[target]
            row=shots[target]
            review=next(r for r in selected if any(p['target']==target for p in r['patches']))
            image=review['image']; panel=panels[image]
            card=deepcopy(perf[target]['card'])
            card=walk_replace(card,CARD_EDITS[ep].get(target,{}))
            if (ep,target) in NEW_CARDS:card=deepcopy(NEW_CARDS[ep,target])
            perf[target]['card']=deepcopy(card)
            perf[target]['details']=[new['fields']['可见动作']]
            row['motion_decision']['admitted_plan']=deepcopy(card)
            # One source panel can have multiple cards; keep its principal source-locked owner.
            if row['role']=='source_locked':panel['performance_plan']=deepcopy(card)
            kind,atom=SHAPES[ep][image]
            if atom not in row['fact_claims'][kind]:row['fact_claims'][kind].append(atom)
            row['camera_decision']['opening']=new['fields']['镜头设计']
            row['camera_decision']['landing']=new['fields']['镜头设计']
            row['motion_decision']['observed_anchor']=panel['composition_lock']+' 可辨眉形/遮挡：'+atom+'。'
            row['camera_decision']['evidence']=row['motion_decision']['observed_anchor']
            if ep==18 and target=='片段7/分镜3':
                row['purpose']=card['coupling'];row['risk_basis']=card['coupling']
                row['camera_decision']['reason']=card['coupling']
                perf[target]['long_take_reason']=card['coupling']
                row['motion_decision']['continuity']=panel['continuity']
                row['motion_decision']['inference_limit']=panel['admission']
            if ep==19 and target=='片段22/分镜1':
                panel['admission']='本格静态锚点是单侧眉头上挑；以14_001略翘的眉形作为起态，在第一问后作有界的局部上挑，抵达本格锚点并持续。无声省略号保留沉默，不生成发声。'
                row['motion_decision']['inference_limit']=panel['admission']
            if ep==19 and target=='片段26/分镜2':
                panel['admission']='源格明确单侧眉头上挑、眉身弯曲且近侧眼睑压低；2秒短否定全程维持警觉形状，目光继续向右。嘴不在镜内，台词画外发声。'
                row['motion_decision']['inference_limit']=panel['admission']
                row['purpose']=card['coupling'];row['camera_decision']['reason']=card['coupling']
                perf[target]['long_take_reason']=card['coupling']
            # Retain original body/contact admissions and add the exact reinspection outcome.
            for admission in row.get('action_admissions',[]):
                if admission['claim']==old['fields']['可见动作']:admission['claim']=new['fields']['可见动作']
                admission['visual_evidence']='观察：'+'；'.join(panel['source_facts']['actions']+panel['source_facts']['relations'])+'。准入规划：'+row['motion_decision']['inference_limit']+' 眉形复查：'+review['decision']
            row['brow_revision_review']={'image':image,'resolution':review.get('inspection','720p缓存代理'),
                'observed_facts':review['facts'],'decision':review['decision'],'seconds':new['seconds'],
                'planned_state':card,'continuity_note':'保留已批准身体任务与当前取景，眉形保持或局部变化与台词/注意节点并行；静态源形状与规划时序分别记录。'}
            # Existing warnings have per-shot dispositions; extend affected ones with actual review.
            containers=[ledger.get('advisory_dispositions',[]),ledger['final_audit']['semantic_review'].get('warning_dispositions',[])]
            for container in containers:
                if isinstance(container,dict):container=container.values()
                for item in container:
                    if not isinstance(item,dict):continue
                    if item.get('target')==target or target in item.get('targets',[]):
                        item['brow_revision']=review['decision']+f' 本镜{new["seconds"]}秒；'+card['coupling']
        ledger['revision_audit'].append({'date':'2026-10-10','reason':'用户反馈眉形识别与变化不准确；按更新后的Gen2.8进行局部表演修订。',
            'affected_targets':list(grouped),'affected_images':[r['image'] for r in selected if r['patches']],
            'inspected_images':len(selected),'resolution':'缓存720p，已批准非露骨头部取景的风险图用局部复查；详见image-reviews.json。',
            'decisions':[{'image':r['image'],'targets':list(dict.fromkeys(p['target'] for p in r['patches'])),'decision':r['decision']} for r in selected if r['patches']],
            'invariants':'镜数、时长、引用、全部现有日文台词及其归属顺序保持一致；先前非露骨改编边界保持。',
            'limitations':'未生成视频；不可辨/被遮挡眉毛不补全，不以头部倾斜产生的屏幕高差推断一眉上抬。'})
        ledger['final_audit']['semantic_review']['brow_revision']={'targets':list(grouped),'image_review_count':len(selected),
            'boundary_review':[
                '18话6/1→6/2保持青的压低眉头、扶肩和春子覆脸；7/2→7/3→8/1从口前交叠手到胸前，再分手伸臂，眉头没有错误松开/重新压低。',
                '18话8/2→8/3春子冷淡的单侧弯眉持续，切青局部错愕；仅露出的短眉段抬高，不补刘海后的眉梢。',
                '19话春子的单侧微挑眉跨听者反打延续；22/1第一问后的局部挑高抵达源形，后续沉默与第二问保持。',
                '19话26/2的2秒警觉持续至下一动作格；29/1不对称低眉/平眉与犹豫的近手同时存在，29/2春子单侧上挑持续。'
            ][0:2] if ep==18 else [
                '19话春子的单侧微挑眉跨听者反打延续；22/1第一问后的局部挑高抵达源形，后续沉默与第二问保持。',
                '19话26/2的2秒警觉持续至下一动作格；29/1不对称低眉/平眉与犹豫的近手同时存在，29/2春子单侧上挑持续。'],
            'review_limit':'仅眉形和必要的手位连续性，不回填静态图中未画出的时间过程；未生成视频。'}
        dest=root/f'storyboards/deliveries/{DELIVERY}';dest.mkdir(parents=True,exist_ok=True)
        current.write_text(new_text,encoding='utf-8');(dest/current.name).write_text(new_text,encoding='utf-8')
        (dest/'source-ledger-v3.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (dest/'image-reviews.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (dest/'brow-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        prior=root/f'storyboards/deliveries/{DATES[ep]}'
        for name in ('dialogue-mapping.json','source-integrity.json','source-package.json','source-copy-check.json','source-intake-audit.json'):
            if (prior/name).exists():shutil.copyfile(prior/name,dest/name)
        results.append({'episode':ep,'clips':len(set(re.match(r'片段(\d+)',s['target'])[1] for s in after)),
            'shots':len(after),'seconds':sum(s['seconds'] for s in after),'reviewed_images':len(selected),'changed_shots':len(changes),
            'changed_fields':sum(len(c['fields']) for c in changes),'baseline_sha256':sha(base/current.name),
            'revised_sha256':sha(current),'dialogue_field_byte_equal':True,'timings_and_references_equal':True,
            'delivery':str(dest),'current':str(current)})
    (HERE/'revision-summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))

if __name__=='__main__':run()
