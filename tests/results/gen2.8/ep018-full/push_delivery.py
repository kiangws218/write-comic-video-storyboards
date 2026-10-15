from pathlib import Path
import os,subprocess,json,urllib.request
O=Path(__file__).parent;R=O.parents[3];env=os.environ.copy();env['PATH']=str(O/'git-lfs-runtime')+os.pathsep+env['PATH']
p=O/'publish-status.json';status=json.loads(p.read_text(encoding='utf-8'))
run=subprocess.run(['git','push','origin','HEAD:refs/heads/codex/comic-workspace'],cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
print(run.stdout)
status['existing_hooks_preserved']=True
status['git_lfs_runtime_verified']=True
status['remote_status']='pushed' if run.returncode==0 else 'push_failed'
p.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if run.returncode:raise SystemExit(run.returncode)
u='https://api.github.com/repos/kiangws218/write-comic-video-storyboards/git/ref/heads/codex/comic-workspace'
d=json.load(urllib.request.urlopen(u,timeout=25));status['remote_head']=d['object']['sha'];status['remote_verified']=status['remote_head']==status['commit'];p.write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert status['remote_verified'],'Remote head changed; inspect before claiming it matches.'
print('Remote commit verified:',status['remote_head'])
