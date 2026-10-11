from pathlib import Path
import urllib.request,hashlib,zipfile,os,subprocess,json
O=Path(__file__).parent;R=O.parents[3];T=O/'git-lfs-runtime';T.mkdir(exist_ok=True)
url='https://github.com/git-lfs/git-lfs/releases/download/v3.8.0/git-lfs-windows-amd64-v3.8.0.zip'
expected='b62e7b8ceddee635f691233d77de8eaa4b213e9209e0173811d8cfa77f7882c1'
p=T/'official-git-lfs.zip'
if not p.exists():
    with urllib.request.urlopen(url,timeout=45) as src, p.open('wb') as dst:
        while chunk:=src.read(1024*1024):dst.write(chunk)
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,'Official asset SHA-256 mismatch; do not execute.'
with zipfile.ZipFile(p) as z:
    members=[n for n in z.namelist() if n.endswith('/git-lfs.exe') or n=='git-lfs.exe']
    assert len(members)==1
    exe=T/'git-lfs.exe';exe.write_bytes(z.read(members[0]))
env=os.environ.copy();env['PATH']=str(T)+os.pathsep+env['PATH']
print(subprocess.run([str(exe),'version'],env=env,cwd=R,check=True,stdout=subprocess.PIPE,text=True).stdout.strip())
# 正常执行现有post-commit检查。运行时只加入当前任务子进程PATH，不改系统PATH或钩子。
subprocess.run(['git','lfs','post-commit'],env=env,cwd=R,check=True)
(O/'git-lfs-runtime-verification.json').write_text(json.dumps({'official_url':url,'official_asset_sha256':expected,'verified':True,'version':'v3.8.0','scope':'task-local process PATH','existing_hooks_preserved':True},indent=2)+'\n',encoding='utf-8')
