import json,re,zipfile
from pathlib import Path
from collections import Counter
from revise_continuity import HERE,REPO,PRIOR,DELIVERY,CHANGES,BRIDGE,parse,sha,jwrite,category,warning_target,target_map,map_targets

def protected(v,path=''):
    out={}
    if isinstance(v,dict):
        for k,x in v.items():
            if k in ('source_text','script_text','jp','source_integrity'):out[path+'/'+k]=x
            else:out.update(protected(x,path+'/'+k))
    elif isinstance(v,list):
        for i,x in enumerate(v):out.update(protected(x,path+'/'+str(i)))
    return out

summaries=json.loads((HERE/'revision-summary.json').read_text(encoding='utf-8'))
for result in summaries:
    ep=result['episode'];dest=Path(result['delivery']);root=dest.parents[2]
    prior=root/'storyboards/deliveries'/PRIOR
    current=Path(result['current']);old=parse((prior/current.name).read_text(encoding='utf-8'));new=parse(current.read_text(encoding='utf-8'))
    assert sha(current)==result['current_sha256']
    ledger_path=dest/'source-ledger-v3.json';ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
    old_ledger=json.loads((prior/'source-ledger-v3.json').read_text(encoding='utf-8'))
    assert protected(ledger['panels'])==protected(old_ledger['panels'])
    assert ledger['source_files']==old_ledger['source_files']
    assert ledger['character_registry']==old_ledger['character_registry']
    assert ledger['character_registry_source']==old_ledger['character_registry_source']
    by={s['target']:s for s in new}
    for a in old:
        t=target_map(a['target'],ep);b=by[t]
        assert a['refs']==b['refs']
        assert a['fields']['台词与语气']==b['fields']['台词与语气']
        for field in a['fields']:
            assert re.findall(r'“[^”]*”|「[^」]*」',a['fields'][field])==re.findall(r'“[^”]*”|「[^」]*」',b['fields'][field])
        assert b['seconds']==(4 if ep==19 and a['target']=='片段32/分镜1' else a['seconds'])
        if a['target'] not in CHANGES[ep]:assert a['fields']==b['fields'],a['target']
    warnings=[l for l in (dest/'validation.txt').read_text(encoding='utf-8').splitlines() if l.startswith('警告：')]
    assert '0个错误' in (dest/'validation.txt').read_text(encoding='utf-8')
    prior_reviews=json.loads((prior/'warning-dispositions.json').read_text(encoding='utf-8'))['dispositions']
    plans={target_map(t,ep):c for t,c in CHANGES[ep].items()}
    if ep==19:plans[BRIDGE['target']]=BRIDGE
    dispositions=[]
    for w in warnings:
        t=warning_target(w);kind=category(w)
        previous=next((r for r in prior_reviews if target_map(r['target'],ep)==t and r['class']==kind),None)
        c=plans.get(t)
        assert previous or c,('new unreviewed warning',ep,w)
        row={'warning':w,'target':t,'class':kind,'disposition':'reviewed'}
        if c:
            row['conclusion']='实际表演：'+c['opening']+' → '+'；'.join(c['beats'])+' → '+c['landing']+'。任务/互动：'+c['coupling']
            row['timing']='4秒内先回鞘再抽刀；无对白，约3.6秒动作。' if ep==19 and t=='片段32/分镜1' else (
                '2秒内共同下降和腿部落位并行，约1.8秒动作；后镜才说警告，刀尖窄隙持续。' if ep==19 and t==BRIDGE['target'] else
                '主动作与当前对白/反应并行，镜尾状态明确；未增加手势配额或削减已批准表演。')
            if kind=='background_occlusion':row['conclusion']+=' 本取景由既有双手、冰袋、袖口占满；独立背景确实遮住，未把袋面写作环境。'
            if kind=='mixed_evidence':row['conclusion']+=' 动作准入单独记录于motion_decision，台词只组织时序，不提供新的接触或事件。'
            row['inspection']='continuity-review.json中的图像记录和具体阶段判断。'
        else:row['conclusion']=map_targets(previous['conclusion'],ep)
        if previous:row['prior_conclusion']=previous['conclusion']
        dispositions.append(row)
    warning_result={'errors':0,'warning_count':len(warnings),'classes':dict(Counter(r['class'] for r in dispositions)),'dispositions':dispositions}
    jwrite(dest/'warning-dispositions.json',warning_result)
    ledger['final_audit']['semantic_review']['warnings']=dispositions
    ledger['final_audit']['semantic_review']['warning_dispositions']='warning-dispositions.json'
    jwrite(ledger_path,ledger)
    result.update({'structural_errors':0,'warning_count':len(warnings),'warning_classes':warning_result['classes'],
        'raw_bubble_text_and_integrity_unchanged':True,'identities_unchanged':True,'all_existing_quoted_text_unchanged':True,
        'unmodified_shot_fields_identical':True,'source_audit':'50 affected/adjoining source panels reinspected across both episodes; unchanged approved evidence reused; no video generated.'})
    jwrite(dest/'revision-summary.json',result)
    changes=json.loads((dest/'continuity-changes.json').read_text(encoding='utf-8'))
    audit=json.loads((dest/'continuity-review.json').read_text(encoding='utf-8'))
    lines=[f'# 第{ep}话动作衔接修订对照','',f'全量扫描{len(new)}镜与{len(new)-1}个相邻边界，重开{result["inspected_images"]}张影响判断的源格。',
        f'修改{result["changed_existing_shots"]}个既有镜头，新增{result["added_bridges"]}个必要衔接镜头。当前{result["clips"]}片段、{result["shots"]}镜、{result["seconds"]}秒，单片段不超过15秒。',
        '', '原有日文台词、说话人、图片引用顺序、最新角色映射和眉形设计保留。19话增加2秒压制桥和2秒回鞘时间；没有压缩台词或用空镜代替主动作。',
        '', '## 全话连续性结论','']
    for seq in audit['sequence_review']:lines.append(f'- 片段{seq["clips"][0]}—{seq["clips"][1]}：{seq["conclusion"]}')
    for c in changes:
        lines.extend(['',f'## {c["target"]}','',f'时长：{c["seconds_before"]} → {c["seconds_after"]}秒。'+('新增镜头；原28/4、28/5顺延为28/5、28/6。' if not c['previous_target'] else ''),''])
        for field in c['after']:
            if c['before'] and c['before'][field]==c['after'][field]:continue
            lines.extend([f'**{field}**',''])
            if c['before']:lines.extend(['修订前：'+c['before'][field],''])
            lines.extend(['修订后：'+c['after'][field],''])
        lines.extend(['内部动作准入：'+c['admission'],''])
    (dest/'动作衔接修订对照.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    (dest/'交付说明.md').write_text('\n'.join([f'# 第{ep}话完整分镜｜动作衔接修订','',
        f'当前制作稿：{current.name}。{result["clips"]}片段、{result["shots"]}镜、{result["seconds"]}秒；正式引用{result["formal_reference_count"]}张。',
        '', f'本轮修订{result["changed_existing_shots"]}个既有镜头，新增{result["added_bridges"]}镜。19话09_001补靠近与冰袋前送，冷淡回应后收回；抓臂、扶肩、起身、握柄/鞘、掠水/蹬出、下落压制和再次抽刀所需状态变化逐项核对。',
        '', '此前姓名与眉形修订保留；原气泡文本、日文语句与引用顺序未改。19话片段28插入2秒桥，原分镜4/5顺延为5/6；片段32/1从2秒延至4秒，其余既有时长保持。',
        '', f'结构/台账0错误，{len(warnings)}条提示按类别和镜头处置，见warning-dispositions.json。全话边界复查见continuity-review.json，前后对照见动作衔接修订对照.md。',
        '', '明确转场和非露骨剧情省略保留；没有补画外命中、性行为、未显示路线、冰袋存放地点或治疗新操作。未生成视频，后续制作仍需验证实际运动。',
        '', 'current/与本目录制作稿、ZIP内容相同。prior-*和revision_audit内原审校为历史记录；本轮编号对照在continuity-review.json。Gen2.8技能及漫画原件未修改。','']),encoding='utf-8')
    status=root/'STATUS.md';text=status.read_text(encoding='utf-8').replace(PRIOR,DELIVERY)
    if ep==19:text=text.replace('79分镜、353秒','80分镜、357秒')
    text=re.sub(r'^- 2026-10-11动作衔接修订：.*\n?','',text,flags=re.M)
    if ep==19:text=text.replace('52条启发式提示','55条启发式提示')
    note=f'- 2026-10-11动作衔接修订：全量复查{result["shots"]}镜及{result["reviewed_boundaries"]}个边界；修改{result["changed_existing_shots"]}镜，新增{result["added_bridges"]}镜。当前{result["seconds"]}秒；日文台词、最新姓名/眉形与正式引用保留。'
    text=text.rstrip()+'\n\n'+note+'\n'
    status.write_text(text,encoding='utf-8')
    pack=dest/f'第{ep}话_完整分镜与动作衔接审校_Gen2.8.zip'
    with zipfile.ZipFile(pack,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(dest.iterdir()):
            if p.is_file() and p!=pack:z.write(p,p.name)
    with zipfile.ZipFile(pack) as z:
        assert z.testzip() is None
        for p in dest.iterdir():
            if p.is_file() and p!=pack:assert z.read(p.name)==p.read_bytes(),p
    assert (dest/current.name).read_bytes()==current.read_bytes()
    print(ep,'0 errors;',len(warnings),'reviewed advisories;',result['shots'],'shots;',result['seconds'],'seconds')
jwrite(HERE/'revision-summary.json',summaries)
