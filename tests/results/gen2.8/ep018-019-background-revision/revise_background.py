"""Apply reviewed backing choices; preserve action, dialogue, timing, and prior audits."""
import json, re, sys, hashlib, shutil, subprocess, zipfile
from pathlib import Path
from copy import deepcopy
from collections import Counter
from decisions import CHANGES, VIEWED, REFERENCES, RETAINED

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
SKILL=Path(r'C:\Users\86135\.codex\skills\write-comic-video-storyboards-gen2-8')
sys.path.insert(0,str(REPO/'tests/results/gen2.8/ep018-019-brow-revision'))
from prepare_review import parse
PRIOR='2026-10-11_Gen2.8_动作衔接修订'
DELIVERY='2026-10-11_Gen2.8_抽象背景修订'

def jwrite(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def warning_target(w):
    m=re.search(r'片段(\d+)(?:的|/)?分镜(\d+)',w)
    return f'片段{m[1]}/分镜{m[2]}' if m else None
def category(w):
    for text,label in [('需表演卡语义复查','performance_card'),('需表演语义复查','performance_semantics'),
        ('含重复话语','repeated_dialogue'),('需背景字段语义复查','background_field'),
        ('需背景遮挡语义复查','background_occlusion'),('证据说明涉及文本语境','mixed_evidence'),
        ('名明确说话人','multiple_speakers'),('没有镜头落幅','camera_landing'),('缺少焦段','camera_quality')]:
        if text in w:return label
    return 'other'

def render(text,ep):
    target=None;clip=0;out=[]
    for line in text.splitlines():
        m=re.match(r'## 【片段(\d+)】',line)
        if m:clip=int(m[1])
        m=re.match(r'\*\*分镜(\d+)（(\d+)秒）',line)
        if m:target=f'片段{clip}/分镜{m[1]}'
        c=CHANGES[ep].get(target,{})
        if c and line.startswith('【可见背景】'):line='【可见背景】：'+c['background']
        if c.get('light') and line.startswith('【光影布光】'):line='【光影布光】：'+c['light']
        out.append(line)
    return '\n'.join(out)+'\n'

def main():
    summaries=[]
    refs=deepcopy(REFERENCES)
    for r in refs:r['sha256']=sha(HERE/'references'/r['local'])
    for ep in (18,19):
        root=REPO/f'comic-workspace/episodes/ep-{ep:03}'
        prior=root/'storyboards/deliveries'/PRIOR
        dest=root/'storyboards/deliveries'/DELIVERY;dest.mkdir(parents=True,exist_ok=True)
        current=root/f'storyboards/current/第{ep}话_制作分镜_Gen2.8.md'
        before=(prior/current.name).read_text(encoding='utf-8');after=render(before,ep)
        if current.read_text(encoding='utf-8') not in (before,after):
            # Resume only our exact already-written candidate after a validation repair.
            assert (dest/current.name).exists() and current.read_bytes()==(dest/current.name).read_bytes()
            recorded=json.loads((dest/'background-changes.json').read_text(encoding='utf-8'))
            expected={c['target']:c for c in recorded}
            for baseline,candidate in zip(parse(before),parse(current.read_text(encoding='utf-8'))):
                assert baseline['target']==candidate['target'] and baseline['seconds']==candidate['seconds'] and baseline['refs']==candidate['refs']
                for field,value in baseline['fields'].items():
                    c=expected.get(baseline['target'])
                    allowed=c['background_after'] if c and field=='可见背景' else c['light_after'] if c and field=='光影布光' else value
                    assert candidate['fields'][field]==allowed,'Current changed outside recorded candidate'
        old=parse(before);new=parse(after);by={s['target']:s for s in new}
        old_ledger=json.loads((prior/'source-ledger-v3.json').read_text(encoding='utf-8'))
        ledger=deepcopy(old_ledger);rows={s['target']:s for s in ledger['shots']}
        changes=[]
        for s in old:
            n=by[s['target']];c=CHANGES[ep].get(s['target'])
            assert s['seconds']==n['seconds'] and s['refs']==n['refs']
            for field in s['fields']:
                if c and (field=='可见背景' or field=='光影布光' and 'light' in c):continue
                assert s['fields'][field]==n['fields'][field],(ep,s['target'],field)
            if not c:continue
            row=rows[s['target']]
            prior_decision=deepcopy(row['background_decision'])
            ref=next((r for r in refs if r['id']==c['family']),None)
            basis=c['basis']+' 当前观察：'+c['observed']+' 退出：'+c['return']
            if ref:basis+=' 静帧形式参考：'+ref['work']+' '+ref['url']+'；'+ref['adaptation']+'。未声称原动画具有本轮动态。'
            row['background_decision']={'mode':c['mode'],'basis':basis,'source_refs':[c['image']],
                'inspected_resolution':'720p','treatment':'decorative_overlay' if c['mode']=='physical' else 'replacement_graphic',
                'motion':'静态图形层；无新增转场动画、时长、声音或图形发光。'}
            row['background_excerpt']=c['background']
            row['background_revision_review']={'status':'reviewed','source_image':c['image'],
                'observation':c['observed'],'decision':c['basis'],'sequence_return':c['return'],
                'field_purity':'只写背景层；人物动作与接触、眉形和说话全文保持。',
                'lighting':'沿用人物左上柔光与人设基色；抽象底场不是新光源。'+(' 删除通用凸石/岩缝布光，改写为当前可见人物的明暗。' if 'light' in c else '')}
            changes.append({'target':s['target'],'image':c['image'],'mode_before':prior_decision['mode'],
                'mode_after':c['mode'],'family':c['family'],'observation':c['observed'],'basis':c['basis'],
                'sequence_return':c['return'],'background_before':s['fields']['可见背景'],
                'background_after':n['fields']['可见背景'],'light_before':s['fields']['光影布光'],
                'light_after':n['fields']['光影布光'],'prior_background_decision':prior_decision})
        # The original observational ledger and all character/action plans are untouched.
        for k in ('panels','source_files','character_registry','character_registry_source','performance','source_regions'):
            if k in old_ledger:assert ledger[k]==old_ledger[k],k
        for a,b in zip(old_ledger['shots'],ledger['shots']):
            assert {k:v for k,v in a.items() if k not in ('background_decision','background_excerpt','background_revision_review')}=={
                k:v for k,v in b.items() if k not in ('background_decision','background_excerpt','background_revision_review')}
        boundaries=[]
        for a,b in zip(new,new[1:]):
            if a['target'] not in CHANGES[ep] and b['target'] not in CHANGES[ep]:continue
            ra=rows[a['target']];rb=rows[b['target']]
            pa=ra['motion_decision'].get('admitted_plan') or {};pb=rb['motion_decision'].get('admitted_plan') or {}
            context=[CHANGES[ep][t]['return'] for t in (a['target'],b['target']) if t in CHANGES[ep]]
            boundaries.append({'outgoing':a['target'],'incoming':b['target'],
                'outgoing_background':a['fields']['可见背景'],'incoming_background':b['fields']['可见背景'],
                'outgoing_state':pa.get('landing',a['fields']['可见动作']),
                'incoming_state':pb.get('opening',b['fields']['可见动作']),
                'connection':' / '.join(context),'status':'reviewed',
                'action_connection':'原动作链字节相同；现有编号切镜承担抽象底的开始/结束，无暗藏切镜、重复动作或增时。'})
        audit={'date':'2026-10-11','scope':'全话扫描137镜背景模式与连续段落；只重开候选镜头和实际采用的相邻环境证据。',
            'affected_targets':list(CHANGES[ep]),'image_inspection':[{'image':f'第{ep}話_{f}.jpg','resolution':'720p缓存代理'} for f in VIEWED[ep]],
            'original_escalation':[],'changes':changes,'boundaries':boundaries,'retained':RETAINED[ep],
            'references':'background-references.json','palette':'实景岩壁深褐、诊所木墙灰棕和人物基色保持；冷灰/蓝灰用于心理与静默，浅金平面亮纹用于自我展示，浅青蓝圆斑用于认出旧识。不是固定情绪色表。',
            'light_effect_review':'图形在独立背衬上，静态且不投光；没有实体粉尘、泡泡、魔法、天气、雨雾或新声效。',
            'limitations':['未生成视频，语义审校不等于视频执行验证。','源事实、动作相位、角色映射、眉形、台词、镜头取景/数量/时长、非露骨改编边界保持。']}
        ledger['revision_audit'].append(audit)
        sem=ledger['final_audit']['semantic_review']
        sem['background_revision']={'review_file':'background-review.json','affected_targets':list(CHANGES[ep]),
            'inspected_source_images':len(VIEWED[ep]),'affected_boundaries':len(boundaries),'status':'reviewed',
            'actor_action_dialogue_timing_unchanged':True,'graphic_motion':'静态','video_generated':False}
        for a in ledger.get('advisory_dispositions',[]):
            if a.get('target') in CHANGES[ep]:
                a['previous_background_revision_basis']=a.get('basis','')
                a['basis']=a.get('basis','')+' 当前背景复核：'+CHANGES[ep][a['target']]['basis']
        for p in prior.iterdir():
            if p.is_file() and p.suffix.lower()!='.zip' and p.name not in (current.name,'source-ledger-v3.json','revision-summary.json','validation.txt','warning-dispositions.json','交付说明.md'):
                shutil.copyfile(p,dest/p.name)
        current.write_text(after,encoding='utf-8');(dest/current.name).write_text(after,encoding='utf-8')
        jwrite(dest/'source-ledger-v3.json',ledger);jwrite(dest/'background-review.json',audit);jwrite(dest/'background-changes.json',changes)
        jwrite(dest/'background-references.json',refs)
        proc=subprocess.run([sys.executable,'-X','utf8',str(SKILL/'scripts/validate_storyboard.py'),str(current),
            '--max-seconds','15','--image-dir',str(REPO/f'tests/results/gen2.8/ep{ep:03}-full/analysis-proxies'),
            '--source-ledger',str(dest/'source-ledger-v3.json'),'--require-source-ledger'],capture_output=True,encoding='utf-8')
        (dest/'validation.txt').write_text(proc.stdout+proc.stderr,encoding='utf-8')
        assert proc.returncode==0 and '0个错误' in proc.stdout,proc.stdout+proc.stderr
        warnings=[l for l in proc.stdout.splitlines() if l.startswith('警告：')]
        previous=json.loads((prior/'warning-dispositions.json').read_text(encoding='utf-8'))['dispositions']
        dispositions=[]
        for w in warnings:
            t=warning_target(w);kind=category(w)
            p=next((r for r in previous if r['target']==t and r['class']==kind),None)
            assert p,(ep,'New advisory needs manual review',w)
            d={'warning':w,'target':t,'class':kind,'disposition':'reviewed','conclusion':p['conclusion']}
            if t in CHANGES[ep]:
                d['prior_conclusion']=p['conclusion']
                d['conclusion']+=' 当前背景：'+CHANGES[ep][t]['basis']+' '+CHANGES[ep][t]['return']
                d['review_scope']='背景和必要布光复查；原表演、引用和时长精确一致，复用有效原表演结论。'
            else:d['review_scope']='本轮该镜正文和规划全未改，沿用逐镜有效审校。'
            dispositions.append(d)
        warning_result={'errors':0,'warning_count':len(warnings),'classes':dict(Counter(d['class'] for d in dispositions)),'dispositions':dispositions}
        jwrite(dest/'warning-dispositions.json',warning_result)
        sem['warnings']=dispositions;sem['warning_dispositions']='warning-dispositions.json'
        jwrite(dest/'source-ledger-v3.json',ledger)
        counts=Counter(s['target'].split('/')[0] for s in new)
        times=Counter()
        for s in new:times[s['target'].split('/')[0]]+=s['seconds']
        assert max(times.values())<=15
        summary={'episode':ep,'current':str(current),'delivery':str(dest),'clips':len(counts),'shots':len(new),
            'seconds':sum(s['seconds'] for s in new),'formal_reference_count':len(set(r for s in new for r in s['refs'])),
            'changed_background_shots':len(CHANGES[ep]),'new_graphic_replacements':sum(rows[t]['background_decision']['mode']=='graphic' and next(s for s in old_ledger['shots'] if s['target']==t)['background_decision']['mode']!='graphic' for t in CHANGES[ep]),
            'graphic_overlays':sum(c['mode']=='physical' for c in CHANGES[ep].values()),
            'inspected_source_images':len(VIEWED[ep]),'inspected_animation_stills':len(refs),'affected_boundary_reviews':len(boundaries),
            'errors':0,'warning_count':len(warnings),'warning_classes':warning_result['classes'],'manual_overflow_items':0,
            'rule_input_bytes':sum((SKILL/name).stat().st_size for name in ['SKILL.md']+['references/'+n+'.md' for n in ['core-authoring','dialogue-performance','acting-calibration','cinematic-rendering','background-design','background-visual-library']]),
            'action_dialogue_brows_camera_sound_timing_unchanged':True,'source_panels_registry_and_fact_claims_unchanged':True,
            'source_audit':'扫描全话，重开背景候选及相邻环境；漫画原件和气泡观察不改。','current_sha256':sha(current),'video_generated':False}
        jwrite(dest/'revision-summary.json',summary);summaries.append(summary)
        lines=[f'# 第{ep}话抽象背景修订对照','',f'本轮调整{len(CHANGES[ep])}镜。镜头数量、时长、动作、台词、角色姓名和眉形全文保持；仅背景与受影响的通用布光更新。','',
            '图形层均采用静态设计，开始和结束由现有编号切镜承担；没有新增粒子声、天气、魔法或人物着色。','']
        for c in changes:
            lines.extend([f'## {c["target"]}','',f'用途：{c["basis"]}','',f'修订前：{c["background_before"]}','',f'修订后：{c["background_after"]}','',f'衔接：{c["sequence_return"]}',''])
            if c['light_before']!=c['light_after']:lines.extend(['布光同步：'+c['light_after'],''])
        lines.extend(['## 保留与验证','',*['- '+s for s in RETAINED[ep]],'',f'当前{summary["clips"]}片段、{summary["shots"]}镜、{summary["seconds"]}秒、{summary["formal_reference_count"]}张正式引用；0错误，{len(warnings)}条提示逐镜处置。','',
            '本轮源格观察、形式参考和相邻边界结论见background-review.json及background-references.json。此前动作衔接审校仍有效，原文保存在continuity-review.json；其summary与旧ZIP以此前交付目录为准。',''])
        (dest/'抽象背景修订对照.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
        (dest/'交付说明.md').write_text('\n'.join([f'# 第{ep}话完整分镜｜抽象背景修订','',
            f'{current.name}：{summary["clips"]}片段、{summary["shots"]}镜、{summary["seconds"]}秒、{summary["formal_reference_count"]}张正式引用。',
            '',f'调整{len(CHANGES[ep])}镜背景；只在有依据的情绪/喜剧拍点使用平底、压力纹理或柔亮纹样。带必要地面、扶肩、冰袋操作和水面战斗的镜头保留原处理。',
            '', 'Gen2.8技能及漫画原件不改。动作、角色映射、眉形、台词、声音、取景、引用和时长与动作衔接修订版精确相同；受影响的通用凸石/岩缝布光同步为人物明暗。',
            '',f'结构/台账0错误，{len(warnings)}条提示逐镜处置。本轮对照、背景准入/回景、静帧参考和验证随包；既有身份、眉形、动作衔接审校保留。',
            '', '本轮只核实静帧形式，未观察参考动画运动；图形层静止，不发光、不形成实体、不增加声效。未生成视频。原有非露骨改编边界保持。',
            '', 'current制作稿、本目录制作稿与ZIP逐字节一致；更早交付不覆盖，保留在原目录。','']).rstrip()+'\n',encoding='utf-8')
        status=root/'STATUS.md';st=status.read_text(encoding='utf-8').replace(PRIOR,DELIVERY)
        st=re.sub(r'\d+条启发式提示',f'{len(warnings)}条启发式提示',st)
        st=re.sub(r'^- 2026-10-11抽象背景修订：.*\n?','',st,flags=re.M)
        st=st.rstrip()+f'\n\n- 2026-10-11抽象背景修订：调整{len(CHANGES[ep])}镜背景，静态图形服务具体反应拍点，动作依赖的实景保留；原动作/台词/眉形/取景/时长保持。0错误，{len(warnings)}条提示已逐镜处置。\n'
        status.write_text(st,encoding='utf-8')
        pack=dest/f'第{ep}话_完整分镜与抽象背景审校_Gen2.8.zip'
        with zipfile.ZipFile(pack,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for p in sorted(dest.iterdir()):
                if p.is_file() and p.suffix.lower()!='.zip':z.write(p,p.name)
        with zipfile.ZipFile(pack) as z:
            assert z.testzip() is None
            for p in dest.iterdir():
                if p.is_file() and p.suffix.lower()!='.zip':assert z.read(p.name)==p.read_bytes()
        assert current.read_bytes()==(dest/current.name).read_bytes()
        print(json.dumps({k:summary[k] for k in ('episode','changed_background_shots','clips','shots','seconds','errors','warning_count')},ensure_ascii=False))
    jwrite(HERE/'revision-summary.json',summaries)

if __name__=='__main__':main()
