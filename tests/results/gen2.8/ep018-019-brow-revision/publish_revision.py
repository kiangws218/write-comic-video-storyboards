from pathlib import Path
import subprocess, os, json, sys, hashlib, shutil

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
SKILL='write-comic-video-storyboards-gen2-8'
SKILL_BRANCH='codex/gen2.8-performance-router'
WORKSPACE_BRANCH='codex/comic-workspace'
BASE='72a89198d6660479631d45be21f49dabad0316d0'
FILES=['references/core-authoring.md','references/dialogue-performance.md','references/regression-cases.md']
CHECKOUT=HERE/'skill-checkout'
ENV=os.environ.copy()
ENV['PATH']=str(REPO/'tests/results/gen2.8/ep018-full/git-lfs-runtime')+os.pathsep+ENV['PATH']
for key in ('HTTP_PROXY','HTTPS_PROXY','ALL_PROXY'):ENV[key]='http://127.0.0.1:7890'

def git(*args,cwd=REPO):
    result=subprocess.run(['git','-c','core.quotepath=false',*args],cwd=cwd,env=ENV,capture_output=True,text=True,encoding='utf-8',errors='strict')
    if result.returncode:raise RuntimeError(f'git {args}:\n{result.stdout}\n{result.stderr}')
    return result.stdout.strip()

def remote(branch):return git('ls-remote','origin','refs/heads/'+branch).split()[0]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def skill_prepare():
    assert remote(SKILL_BRANCH)==BASE,'Remote skill branch changed; integrate before publishing'
    assert not CHECKOUT.exists(),'Review the existing checkout rather than overwriting'
    assert not git('diff','--cached','--name-only'),'Existing staged work must be preserved'
    git('fetch','origin',SKILL_BRANCH)
    git('worktree','add','--detach',str(CHECKOUT),BASE)
    for rel in FILES:
        source=REPO/SKILL/rel
        installed=Path(r'C:\Users\86135\.codex\skills')/SKILL/rel
        assert digest(source)==digest(installed),(rel,'Local installed skill mismatch')
        shutil.copyfile(source,CHECKOUT/SKILL/rel)
    changed=git('diff','--name-only',cwd=CHECKOUT).splitlines()
    allowed=[f'{SKILL}/{rel}' for rel in FILES]
    assert set(changed)==set(allowed),(changed,allowed)
    git('diff','--check',cwd=CHECKOUT)
    git('add','--',*allowed,cwd=CHECKOUT)
    assert set(git('diff','--cached','--name-only',cwd=CHECKOUT).splitlines())==set(allowed)
    git('commit','-m','Refine Gen2.8 brow recognition and expressive continuity',cwd=CHECKOUT)
    commit=git('rev-parse','HEAD',cwd=CHECKOUT)
    manifest={'branch':SKILL_BRANCH,'baseline_commit':BASE,'commit':commit,'status':'committed',
        'files':[{'file':f'{SKILL}/{rel}','sha256':digest(CHECKOUT/SKILL/rel)} for rel in FILES],
        'validation':'quick_validate passed; existing 143 Python unit tests passed; image-based review recorded separately; no generated video'}
    (HERE/'skill-publish.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

def skill_push():
    record=json.loads((HERE/'skill-publish.json').read_text(encoding='utf-8'))
    assert git('rev-parse','HEAD',cwd=CHECKOUT)==record['commit']
    assert not git('status','--porcelain',cwd=CHECKOUT),'Skill checkout must be clean'
    assert remote(SKILL_BRANCH)==record['baseline_commit'],'Remote changed; integrate rather than force'
    print(git('push','origin',f'HEAD:refs/heads/{SKILL_BRANCH}',cwd=CHECKOUT))
    assert remote(SKILL_BRANCH)==record['commit']
    record['status']='pushed_and_remote_verified'
    (HERE/'skill-publish.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Skill remote verified:',record['commit'])

def workspace_prepare():
    assert git('branch','--show-current')==WORKSPACE_BRANCH
    pending=git('diff','--cached','--name-only').splitlines()
    base=git('rev-parse','HEAD')
    assert remote(WORKSPACE_BRANCH)==base,'Workspace remote changed; integrate before publishing'
    allowed=[]
    for ep in (18,19):
        root=REPO/f'comic-workspace/episodes/ep-{ep:03}'
        allowed.extend([root/'STATUS.md',root/f'storyboards/current/第{ep}话_制作分镜_Gen2.8.md'])
        dest=root/'storyboards/deliveries/2026-10-10_Gen2.8_眉形表演修订'
        allowed.extend(p for p in dest.rglob('*') if p.is_file())
    allowed.extend([HERE/'image-reviews.json',HERE/'revision-summary.json',HERE/'skill-publish.json',
        HERE/'apply_revision.py',HERE/'prepare_review.py',HERE/'finish_delivery.py',HERE/'publish_revision.py'])
    report=REPO/'tests/results/gen2.8/brow-performance-review/眉毛表演优化复查.md'
    allowed.append(report)
    rels=[p.relative_to(REPO).as_posix() for p in allowed]
    assert set(pending)<=set(rels),'Existing staged work outside this task must be preserved'
    assert all(p.exists() for p in allowed)
    assert not any(r.lower().endswith(('.jpg','.jpeg','.png')) for r in rels),'No source images in revision commit'
    git('diff','--check','--',*rels)
    git('add','--',*rels)
    staged=git('diff','--cached','--name-only').splitlines()
    assert set(staged)<=set(rels),staged
    git('commit','-m','Repair ep018 and ep019 brow performance with source review')
    commit=git('rev-parse','HEAD')
    record={'branch':WORKSPACE_BRANCH,'baseline_commit':base,'commit':commit,'staged_files':staged,'status':'committed'}
    (HERE/'workspace-publish.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Workspace committed:',commit,'files:',len(staged))

def workspace_push():
    record=json.loads((HERE/'workspace-publish.json').read_text(encoding='utf-8'))
    assert git('rev-parse','HEAD')==record['commit']
    assert remote(WORKSPACE_BRANCH)==record['baseline_commit'],'Remote changed; integrate rather than force'
    print(git('push','origin',f'HEAD:refs/heads/{WORKSPACE_BRANCH}'))
    assert remote(WORKSPACE_BRANCH)==record['commit']
    record['status']='pushed_and_remote_verified'
    (HERE/'workspace-publish.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Workspace remote verified:',record['commit'])

if __name__=='__main__':
    {'skill_prepare':skill_prepare,'skill_push':skill_push,'workspace_prepare':workspace_prepare,'workspace_push':workspace_push}[sys.argv[1]]()
