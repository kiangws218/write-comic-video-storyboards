from pathlib import Path
import os,subprocess,sys,json
O=Path(__file__).parent;R=O.parents[3]
env=os.environ.copy();env['PATH']=str(O.parent/'ep018-full/git-lfs-runtime')+os.pathsep+env['PATH'];env.update(HTTP_PROXY='http://127.0.0.1:7890',HTTPS_PROXY='http://127.0.0.1:7890',ALL_PROXY='http://127.0.0.1:7890')
def git(*args,capture=False):
    return subprocess.run(['git',*args],cwd=R,env=env,check=True,stdout=subprocess.PIPE if capture else None,text=True,encoding='utf-8').stdout
mode=sys.argv[1]
assert git('branch','--show-current',capture=True).strip()=='codex/comic-workspace'
if mode=='fetch':
    git('-c','http.proxy=http://127.0.0.1:7890','fetch','origin','codex/comic-workspace')
    print(git('rev-list','--left-right','--count','HEAD...origin/codex/comic-workspace',capture=True).strip())
elif mode=='ff':
    git('merge','--ff-only','origin/codex/comic-workspace')
elif mode=='stage':
    assert not git('diff','--cached','--name-only',capture=True).strip(),'Existing staged changes'
    git('add','--','comic-workspace/episodes/ep-019','comic-workspace/README.md')
    paths=git('diff','--cached','--name-only','-z',capture=True).split('\0');paths=[p for p in paths if p]
    assert all(p.startswith('comic-workspace/episodes/ep-019/') or p=='comic-workspace/README.md' for p in paths)
    print('Staged',len(paths),'episode19-only files and workspace index.')
    git('diff','--cached','--check')
elif mode=='commit':
    paths=[p for p in git('diff','--cached','--name-only','-z',capture=True).split('\0') if p]
    assert len(paths)==90 and all(p.startswith('comic-workspace/episodes/ep-019/') or p=='comic-workspace/README.md' for p in paths),'Unexpected staged scope'
    git('commit','-m','Complete ep019 storyboards with Gen2.8 and source audit')
    print('COMMIT',git('rev-parse','HEAD',capture=True).strip())
elif mode=='push':
    git('-c','http.proxy=http://127.0.0.1:7890','push','origin','codex/comic-workspace')
    print('LOCAL',git('rev-parse','HEAD',capture=True).strip())
    print('REMOTE',git('-c','http.proxy=http://127.0.0.1:7890','ls-remote','origin','refs/heads/codex/comic-workspace',capture=True).strip())
else:raise ValueError(mode)
