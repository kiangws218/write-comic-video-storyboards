"""Publish only the reviewed episode deliverables and this task's authoring records."""
import os, subprocess, hashlib
from revise_background import REPO, HERE, DELIVERY, jwrite

env=os.environ.copy()
env['PATH']=str(REPO/'tests/results/gen2.8/ep018-full/git-lfs-runtime')+os.pathsep+env['PATH']
for k in ('HTTP_PROXY','HTTPS_PROXY','ALL_PROXY'):env[k]='http://127.0.0.1:7890'
def git(*args):
    p=subprocess.run(['git','-c','core.quotepath=false',*args],cwd=REPO,env=env,capture_output=True,encoding='utf-8')
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    return p.stdout.strip()

assert git('branch','--show-current')=='codex/comic-workspace'
remote=git('ls-remote','origin','refs/heads/codex/comic-workspace').split()[0]
assert remote==git('rev-parse','HEAD'),'Remote advanced; inspect and integrate before publishing'
paths=[]
for ep in (18,19):
    root=f'comic-workspace/episodes/ep-{ep:03}'
    paths.extend([root+'/STATUS.md',root+f'/storyboards/current/第{ep}话_制作分镜_Gen2.8.md'])
    dest=REPO/root/'storyboards/deliveries'/DELIVERY
    paths.extend(p.relative_to(REPO).as_posix() for p in dest.iterdir() if p.is_file())
paths.extend((HERE/n).relative_to(REPO).as_posix() for n in ('decisions.py','revise_background.py','publish_workspace.py','revision-summary.json'))
initial=git('diff','--cached','--name-only').splitlines()
assert not initial or set(initial)==set(paths),'Preserve unrelated staged work'
source=[p for ep in (16,17,18,19) for p in (REPO/f'comic-workspace/episodes/ep-{ep:03}/source').rglob('*') if p.is_file()]
hashes={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in source}
git('add','--',*paths)
staged=git('diff','--cached','--name-only').splitlines()
assert set(staged)==set(paths),(set(staged)-set(paths),set(paths)-set(staged))
assert not any('/source/' in p for p in staged)
git('diff','--cached','--check')
print('Staged',len(paths),'reviewed files;',len(hashes),'source files protected',flush=True)
git('commit','-m','Add supported abstract backgrounds to episodes 18 and 19')
commit=git('rev-parse','HEAD');print('Created',commit,flush=True)
git('push','origin','HEAD:refs/heads/codex/comic-workspace')
assert git('ls-remote','origin','refs/heads/codex/comic-workspace').split()[0]==commit
assert all(hashlib.sha256(p.read_bytes()).hexdigest()==v for p,v in hashes.items())
jwrite(HERE/'workspace-publish.json',{'branch':'codex/comic-workspace','commit':commit,'remote_verified':True,
    'files':staged,'source_files_byte_preserved':len(hashes)})
print('Remote verified',commit,flush=True)
