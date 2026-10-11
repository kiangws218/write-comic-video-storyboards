import os,subprocess,json,hashlib
from revise_identity import REPO,HERE,DELIVERY,BASE,jwrite

env=os.environ.copy()
env['PATH']=str(REPO/'tests/results/gen2.8/ep018-full/git-lfs-runtime')+os.pathsep+env['PATH']
for name in ('HTTP_PROXY','HTTPS_PROXY','ALL_PROXY'):env[name]='http://127.0.0.1:7890'
def git(*args):
    p=subprocess.run(['git','-c','core.quotepath=false',*args],cwd=REPO,env=env,capture_output=True,encoding='utf-8')
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
    return p.stdout.strip()
assert git('branch','--show-current')=='codex/comic-workspace'
assert not git('diff','--cached','--name-only'),'Existing staged work must be preserved'
remote=git('ls-remote','origin','refs/heads/codex/comic-workspace').split()[0]
assert remote==git('rev-parse','HEAD')==BASE,'Remote moved; inspect before proceeding'
dirty_sources=[p for p in git('diff','--name-only').splitlines() if '/source/' in p]
source_hashes={p:hashlib.sha256((REPO/p).read_bytes()).hexdigest() for p in dirty_sources}
paths=['comic-workspace/character-references/角色映射.md']
for ep in (18,19):
    root=f'comic-workspace/episodes/ep-{ep:03}'
    paths.extend([root+'/STATUS.md',root+f'/storyboards/current/第{ep}话_制作分镜_Gen2.8.md'])
    dest=REPO/root/'storyboards/deliveries'/DELIVERY
    paths.extend(p.relative_to(REPO).as_posix() for p in dest.rglob('*') if p.is_file())
paths.extend((HERE/file).relative_to(REPO).as_posix() for file in
    ('revise_identity.py','verify_delivery.py','publish_workspace.py','revision-summary.json','verification.json'))
git('add','--',*paths)
staged=git('diff','--cached','--name-only').splitlines()
assert set(staged)==set(paths),(set(staged)-set(paths),set(paths)-set(staged))
git('diff','--cached','--check')
print('Staged',len(staged),'approved files; preserved',len(source_hashes),'existing source modifications',flush=True)
git('commit','-m','Fix ep18 and ep19 identities using shared character references')
commit=git('rev-parse','HEAD')
print('Created',commit,flush=True)
git('push','origin','HEAD:refs/heads/codex/comic-workspace')
assert git('ls-remote','origin','refs/heads/codex/comic-workspace').split()[0]==commit
assert all(hashlib.sha256((REPO/p).read_bytes()).hexdigest()==v for p,v in source_hashes.items())
jwrite(HERE/'workspace-publish.json',{'branch':'codex/comic-workspace','commit':commit,'remote_verified':True,
    'files':staged,'preserved_existing_source_modifications':len(source_hashes)})
print('Remote verified:',commit,flush=True)
