"""Reconcile prior per-shot reviews, check invariants, and build complete deliverables."""
from pathlib import Path
from collections import Counter
import json,re,subprocess,sys,hashlib,zipfile,shutil
from prepare_review import HERE,REPO,DATES,parse
from apply_revision import DELIVERY

SKILL=Path(r'C:\Users\86135\.codex\skills\write-comic-video-storyboards-gen2-8')

def write_json(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def target(warning):
    m=re.search(r'片段(\d+)(?:的|/)?分镜(\d+)',warning)
    return f'片段{m[1]}/分镜{m[2]}' if m else None

def category(w):
    for text,label in [('需表演卡语义复查','performance_card'),('需表演语义复查','performance_semantics'),
        ('含重复话语','repeated_dialogue'),('需背景字段语义复查','background_field'),
        ('需背景遮挡语义复查','background_occlusion'),('证据说明涉及文本语境','mixed_evidence'),
        ('名明确说话人','multiple_speakers'),('没有镜头落幅','camera_landing'),
        ('缺少焦段','camera_quality')]:
        if text in w:return label
    return 'other'

def validate(script,ledger,ep):
    proc=subprocess.run([sys.executable,'-X','utf8',str(SKILL/'scripts/validate_storyboard.py'),str(script),
        '--max-seconds','15','--image-dir',str(REPO/f'tests/results/gen2.8/ep{ep:03}-full/analysis-proxies'),
        '--source-ledger',str(ledger),'--require-source-ledger'],capture_output=True,encoding='utf-8')
    assert proc.returncode==0,proc.stdout+proc.stderr
    assert '0个错误' in proc.stdout
    return proc.stdout, [w for w in proc.stdout.splitlines() if w.startswith('警告：')]

def main():
    published=json.loads((HERE/'skill-publish.json').read_text(encoding='utf-8'))
    assert published['status']=='pushed_and_remote_verified'
    summary=json.loads((HERE/'revision-summary.json').read_text(encoding='utf-8'))
    for result in summary:
        ep=result['episode'];dest=Path(result['delivery']);root=dest.parents[2]
        current=Path(result['current']);base=HERE/f'baseline/ep-{ep:03}'
        prior=root/f'storyboards/deliveries/{DATES[ep]}'
        ledger_path=dest/'source-ledger-v3.json'
        ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
        ledger['skill_version_commit']=published['commit']
        if 'skill_version' in ledger:ledger['skill_version']='Gen2.8 '+published['commit'][:7]+' 眉形表演优化'
        ledger['final_audit']['semantic_review']['brow_revision']['skill_commit']=published['commit']
        write_json(ledger_path,ledger)
        text,warnings=validate(current,ledger_path,ep)
        (dest/'validation.txt').write_text(text,encoding='utf-8')
        base_text,base_warnings=validate(base/current.name,base/'source-ledger-v3.json',ep)
        (HERE/f'baseline/ep-{ep:03}/validation-current-validator.txt').write_text(base_text,encoding='utf-8')
        if ep==18: old_review=json.loads((prior/'warning-dispositions.json').read_text(encoding='utf-8'))['dispositions']
        else:old_review=json.loads((prior/'warning-review.json').read_text(encoding='utf-8'))
        reviews=json.loads((dest/'image-reviews.json').read_text(encoding='utf-8'))
        changed={t:review for review in reviews for t in dict.fromkeys(p['target'] for p in review['patches'])}
        cards={p['target']:p for p in ledger['performance']}
        shot_rows={s['target']:s for s in ledger['shots']}
        all_shots={s['target']:s for s in parse(current.read_text(encoding='utf-8'))}
        decisions=[]
        for w in warnings:
            t=target(w);c=category(w)
            exact=next((r for r in old_review if r['warning']==w),None)
            previous=exact or next((r for r in old_review if target(r['warning'])==t and category(r['warning'])==c),None)
            assert previous or t in changed,(ep,'Unreviewed warning',w)
            item={'warning':w,'target':t,'class':c,'disposition':'reviewed'}
            if previous:
                item['prior_conclusion']=previous.get('conclusion',previous.get('reason',''))
                item['conclusion']=item['prior_conclusion']
            if t in changed:
                r=changed[t];card=cards[t]['card'];seconds=all_shots[t]['seconds']
                item['image_reinspection']=r['image']
                item['conclusion']=r['decision']+f' 本镜{seconds}秒：'+card['coupling']+' 镜尾：'+card['landing']
                if c=='background_field' or c=='background_occlusion':
                    item['conclusion']+=' 背景正文未改，仍采用既有脸部极近裁切的遮挡说明。'
                if c=='mixed_evidence':
                    item['conclusion']+=' 眉形以当前图像为锚点；台词只决定回应时机，不作为隐藏动作证据。'
            else:item['review_scope']='沿用对应原审校结论；本轮该镜正文与表演卡未修改。'
            decisions.append(item)
        assert len(decisions)==len(warnings)
        report={'errors':0,'warning_count':len(warnings),'classes':dict(Counter(category(w) for w in warnings)),
            'baseline_warning_count_with_current_validator':len(base_warnings),
            'new_warning_keys':sorted({(target(w) or '全稿')+' '+category(w) for w in warnings}-
                {(target(w) or '全稿')+' '+category(w) for w in base_warnings}),
            'removed_warning_keys':sorted({(target(w) or '全稿')+' '+category(w) for w in base_warnings}-
                {(target(w) or '全稿')+' '+category(w) for w in warnings}),
            'dispositions':decisions}
        write_json(dest/'warning-dispositions.json',report)
        ledger['final_audit']['semantic_review']['brow_revision']['warning_review_file']='warning-dispositions.json'
        if ep==18:
            shutil.copyfile(prior/'semantic-review.json',dest/'prior-semantic-review.json')
            ledger['final_audit']['semantic_review']['review_file']='prior-semantic-review.json'
            ledger['final_audit']['semantic_review']['review_file_scope']='前轮历史审校；当前眉形以本轮brow_revision及image-reviews.json为准。'
        else:
            ledger['final_audit']['semantic_review']['warnings']=decisions
        write_json(ledger_path,ledger)
        # Verify all present dialogue fields, source bubbles, identity and references separately from the validator.
        before=parse((base/current.name).read_text(encoding='utf-8'));after=list(all_shots.values())
        assert [(s['target'],s['seconds'],s['refs'],s['fields']['台词与语气']) for s in before]==[
            (s['target'],s['seconds'],s['refs'],s['fields']['台词与语气']) for s in after]
        old_ledger=json.loads((base/'source-ledger-v3.json').read_text(encoding='utf-8'))
        for p,q in zip(old_ledger['panels'],ledger['panels']):
            assert p['image']==q['image']
            for k in ('bubbles','jp','dialogue_turns','coverage_groups','source_integrity'):
                assert p.get(k)==q.get(k),(ep,p['image'],k)
        for t in changed:
            assert cards[t]['details']==[all_shots[t]['fields']['可见动作']]
            assert shot_rows[t]['motion_decision']['admitted_plan']==cards[t]['card']
            assert any(x['claim']==all_shots[t]['fields']['可见动作'] for x in shot_rows[t]['action_admissions'])
        result.update({'structural_errors':0,'warning_count':len(warnings),'warning_classes':report['classes'],
            'formal_reference_count':len(set(r for s in after for r in s['refs'])),
            'source_dialogue_mapping_equal':True,'skill_commit':published['commit'],'video_generated':False})
        write_json(dest/'revision-summary.json',result)
        write_json(dest/'skill-sync.json',published)
        installed_files=[]
        for row in published['files']:
            rel=Path(row['file']).relative_to('write-comic-video-storyboards-gen2-8')
            source=SKILL/rel
            assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256']
            target_path=dest/'Gen2.8_更新文件'/rel;target_path.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,target_path);installed_files.append(rel.as_posix())
        write_json(dest/'Gen2.8_更新文件/manifest.json',{'scope':'相对Gen2.8基线72a8919更新的三个文件；完整技能见仓库2.8分支。',**published})
        changes=json.loads((dest/'brow-changes.json').read_text(encoding='utf-8'))
        lines=[f'# 第{ep}话眉形表演修订对照','',f'复查{result["reviewed_images"]}张来源图，修改{result["changed_shots"]}镜；Gen2.8技能提交 `{published["commit"][:7]}`。',
            '',f'完整稿仍为{result["clips"]}片段、{result["shots"]}分镜、{result["seconds"]}秒。现有日文台词、归属与顺序、每镜时长及引用保持一致。',
            '',f'结构与台账0错误，{len(warnings)}条启发式提示已对应保留原结论或补充本轮逐镜复查；未生成视频。',
            '', '静态眉形与遮挡来自实际图像复查。局部变化是基于源边界的表演设计，不冒充原图提供的逐帧运动。',
            '', '原有探身、握臂、扶肩、转头、捏布与对白交接继续保留；修订主要区分眉头/眉尾、单侧/双侧、抬高/压低/平直，以及变化后的持续状态。',
            '', '本轮已确认的不对称个案是19话29/1：一侧眉头压低，另一侧眉线较平。没有把头部倾斜造成的屏幕高差误标成一侧整体上抬。',
            '', '完整逐图记录见 image-reviews.json；逐字段机器对照见 brow-changes.json；提示处置见 warning-dispositions.json。','']
        for change in changes:
            t=change['target'];r=changed[t]
            lines.extend([f'## {t}（{change["seconds"]}秒）','',f'来源：{r["image"]}。{r["decision"]}',''])
            for field in change['fields']:
                lines.extend([f'**{field}**','',f'- 修订前：{change["before"][field]}','',f'- 修订后：{change["after"][field]}',''])
        (dest/'眉形修订对照.md').write_text('\n'.join(lines),encoding='utf-8')
        (dest/'交付说明.md').write_text('\n'.join([
            f'# 第{ep}话 Gen2.8 眉形表演修订交付','',
            f'完整制作稿：第{ep}话_制作分镜_Gen2.8.md。{result["clips"]}片段、{result["shots"]}分镜、{result["seconds"]}秒；修正{result["changed_shots"]}个镜头。',
            '', '眉形识别、变化和持态经过源图核对，修改对照与审校台账随包交付。先前非露骨取景与剧情改编边界保留。',
            '', '本轮两份制作稿的现有日文台词、说话人归属、语义顺序、镜头时长和参考图保持一致；与原漫画对白的覆盖范围仍以先前改编说明为准。',
            '', f'结构/台账0错误；{len(warnings)}条启发式提示已有逐项处置。表演完成图像与文字审校，未生成视频。',
            '', f'技能2.8分支：codex/gen2.8-performance-router；提交{published["commit"]}。更新仅涉及三个现有参考模块；其增量文件和SHA-256在Gen2.8_更新文件/。',
            '', '原交付目录作为历史保留；current/制作稿与本包制作稿一致。',
            '', '包内不重复漫画原图与缓存代理；原图仍在本话source/。','']),encoding='utf-8')
        status=root/'STATUS.md'
        value=status.read_text(encoding='utf-8')
        value=value.replace(DATES[ep],DELIVERY).replace('72a8919',published['commit'][:7])
        value+='\n- 2026-10-10眉形表演修订：复查'+str(result['reviewed_images'])+'格，修改'+str(result['changed_shots'])+'镜；现有日文台词、时长及引用保持一致，逐镜对照与技能增量随包。\n'
        if ep==19:value=value.replace('52条启发式提示已有逐条处置',str(len(warnings))+'条启发式提示已有逐条处置')
        status.write_text(value,encoding='utf-8')
        zip_path=dest/f'第{ep}话_完整分镜与眉形审校_Gen2.8.zip'
        with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(dest.rglob('*')):
                if file.is_file() and file!=zip_path:archive.write(file,file.relative_to(dest).as_posix())
        with zipfile.ZipFile(zip_path) as archive:
            assert archive.testzip() is None
            assert archive.read(current.name)==current.read_bytes()
        print(ep,': errors 0, warnings',len(warnings),', shots',result['shots'],', changed',result['changed_shots'],', complete zip',zip_path.name)
    write_json(HERE/'revision-summary.json',summary)

if __name__=='__main__':main()
