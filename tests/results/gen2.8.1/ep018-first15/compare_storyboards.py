from pathlib import Path
from collections import Counter
import difflib
import hashlib
import json
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
BASE = ROOT / 'comic-workspace/episodes/ep-018/storyboards/current/第18话_制作分镜_Gen2.8.md'
NEW = OUT / '第18话_前15格_完整分镜_Gen2.8.1.md'
SKILL = ROOT / 'write-comic-video-storyboards-gen2-8-1'
OLD_SKILL = Path(r'C:\Users\86135\.codex\skills\write-comic-video-storyboards-gen2-8')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def parse(path):
    text = path.read_text(encoding='utf-8')
    current_clip = 0
    current_owner = None
    shots = []
    titles = {}
    for line in text.splitlines():
        m = re.match(r'## 【片段(\d+)】(.*)',line)
        if m:
            current_clip=int(m.group(1)); titles[current_clip]=line
        m = re.match(r'\*\*分镜(\d+)（(\d+)秒）',line)
        if m:
            shots.append({'target':f'片段{current_clip}/分镜{m.group(1)}','clip':current_clip,
                          'seconds':int(m.group(2)),'references':[], 'owner':current_owner,
                          'fields':{},'lines':[line]})
            continue
        if shots:
            if line.startswith('分镜参考'):
                refs=re.findall(r'\[([^\]]+\.jpg)\]',line)
                shots[-1]['references']=refs
                if refs:
                    current_owner=refs[0]
                    shots[-1]['owner']=current_owner
            m=re.match(r'【([^】]+)】：(.*)',line)
            if m:
                shots[-1]['fields'][m.group(1)]=m.group(2)
                shots[-1]['lines'].append(line)
            elif line.startswith('分镜参考'):
                shots[-1]['lines'].append(line)
    return text,shots,titles

full_old,old_all,titles=parse(BASE)
_,new_shots,_=parse(NEW)
old_shots=[]
for s in old_all:
    if s['owner'] and s['owner']>'第18話_05_003.jpg':
        break
    old_shots.append(s)
assert len(old_shots)==len(new_shots)==17
for old,new in zip(old_shots,new_shots):
    norm = lambda s: s.replace('_上格','').replace('_下格','')
    assert norm(old['owner'])==norm(new['owner']), (old['owner'],new['owner'])

extracted=['# 第18话前15源文件对应范围 — Gen2.8工作区基线摘取','']
previous=None
for s in old_shots:
    if s['clip']!=previous:
        previous=s['clip']
        seconds=sum(x['seconds'] for x in old_shots if x['clip']==previous)
        original=titles[previous]
        extracted += [re.sub(r'（\d+秒）',f'（{seconds}秒）',original),'']
    extracted+=s['lines']+['']
baseline_copy=OUT/'第18话_前15格_工作区基线_Gen2.8.md'
baseline_copy.write_text('\n'.join(extracted),encoding='utf-8')

def metrics(shots):
    actions=[s['fields']['可见动作'] for s in shots]
    clips=Counter()
    for s in shots:
        clips[s['clip']]+=s['seconds']
    keywords=['颈','下颌','停','稳','落','收','冷淡','不耐烦','焦急','疑惑','惊慌','惊怒','舒坦']
    return {'clips':len(clips),'shots':len(shots),'runtime_seconds':sum(clips.values()),
            'clip_seconds':dict(clips),'references':sum(len(s['references']) for s in shots),
            'action_characters':sum(map(len,actions)), 'mean_action_characters':round(sum(map(len,actions))/len(actions),1),
            'six_field_characters':sum(sum(len(t) for t in s['fields'].values()) for s in shots),
            'literal_keyword_occurrences':{k:sum(t.count(k) for t in actions) for k in keywords}}

rows=[]
for i,(old,new) in enumerate(zip(old_shots,new_shots),1):
    rows.append({'pair':i,'source_file':old['owner'],'gen2_8_target':old['target'],
                 'gen2_8_1_target':new['target'],'old_seconds':old['seconds'],'new_seconds':new['seconds'],
                 'old_action':old['fields']['可见动作'],'new_action':new['fields']['可见动作']})
report={'scope':'第18話_01_001.jpg—第18話_05_003.jpg，15原文件；两版均覆盖19对白气泡',
        'baseline_path':str(BASE),'baseline_sha256':digest(BASE),'new_path':str(NEW),'new_sha256':digest(NEW),
        'baseline':metrics(old_shots),'new':metrics(new_shots),'rows':rows,
        'method_limitations':['独立重生成不是只改一个变量的模型A/B。','画面、上色和分段有正常再创作差异，不能把它们全部归因于措辞规则。','没有视频生成或盲评，不能证明视频模型整体表演不退化。']}
(OUT/'comparison-data.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

comparison=['# 第18话逐镜表演对照：Gen2.8 / Gen2.8.1','',
            '按源图与演出位置配对，镜头编号因片段分组不同而变化。以下是两版实际完整动作字段，不是压缩节选。末格后的06_001不在基线摘取范围内。','']
for row in rows:
    comparison += [f"## {row['pair']}. {row['source_file']}",'',
                   f"**2.8 · {row['gen2_8_target']} · {row['old_seconds']}秒**",'',row['old_action'],'',
                   f"**2.8.1 · {row['gen2_8_1_target']} · {row['new_seconds']}秒**",'',row['new_action'],'']
(OUT/'逐镜表演对照_Gen2.8_vs_Gen2.8.1.md').write_text('\n'.join(comparison),encoding='utf-8')

diff=[]
for rel in ['SKILL.md','agents/openai.yaml','references/dialogue-performance.md']:
    diff.extend(difflib.unified_diff((OLD_SKILL/rel).read_text(encoding='utf-8').splitlines(True),
                (SKILL/rel).read_text(encoding='utf-8').splitlines(True),fromfile='gen2.8/'+rel,tofile='gen2.8.1/'+rel))
(OUT/'Gen2.8.1_skill_changes.diff').write_text(''.join(diff),encoding='utf-8')
validation=subprocess.run([sys.executable,'-X','utf8',str(SKILL/'scripts/validate_storyboard.py'),
                str(baseline_copy),'--max-seconds','15','--image-dir',str(OUT/'analysis-proxies')],
                cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
(OUT/'validation-gen2.8-baseline.txt').write_text(validation.stdout+validation.stderr,encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k in ('baseline','new','scope')},ensure_ascii=False,indent=2))
print('Baseline structural validation exit:',validation.returncode)
print(validation.stdout)
freeze=json.loads((OUT/'independent-draft-freeze.json').read_text(encoding='utf-8'))
assert digest(BASE)==freeze['baseline_sha256'], 'Workspace baseline was changed.'
