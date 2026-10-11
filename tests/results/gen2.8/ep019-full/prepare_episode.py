from pathlib import Path
import urllib.request,json,hashlib,zipfile,re
O=Path(__file__).parent;R=O.parents[3]
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
proxy=urllib.request.build_opener(urllib.request.ProxyHandler({'https':'http://127.0.0.1:7890'}))
direct=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def open_url(url,timeout=25):
    last=None
    for op in [proxy,direct,proxy]:
        try:return op.open(urllib.request.Request(url,headers={'User-Agent':'ComicStoryboardWorkspace'}),timeout=timeout)
        except Exception as e:last=e;print('Retrying connection:',type(e).__name__,flush=True)
    raise last
api='https://api.github.com/repos/kiangws218/write-comic-video-storyboards'
branch=json.load(open_url(api+'/git/ref/heads/codex/comic-workspace'))['object']['sha']
package=O/'19.zip'
if not package.exists():
    u=f'https://raw.githubusercontent.com/kiangws218/write-comic-video-storyboards/{branch}/comic-workspace/episodes/19.zip'
    with open_url(u,timeout=25) as src,package.open('wb') as dst:
        while chunk:=src.read(1024*1024):dst.write(chunk)
data=package.read_bytes();git_sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
assert git_sha=='09b65673ab08ab755e8fc7e04a36e8c09e435689','User package changed; inspect current repository before processing.'
P=O/'source-originals';P.mkdir(exist_ok=True);manifest=[];ignored=[]
with zipfile.ZipFile(package) as z:
    for m in z.infolist():
        if m.is_dir():continue
        name=m.filename
        if not m.flag_bits&0x800:
            for enc in ['utf-8','gbk']:
                try:name=name.encode('cp437').decode(enc);break
                except (UnicodeError,LookupError):pass
        if Path(name).suffix.lower() not in ['.jpg','.jpeg','.png','.webp']:
            ignored.append(name);continue
        if '__MACOSX' in name or Path(name).name.startswith('._'):
            ignored.append(name);continue
        target=P/Path(name).name
        assert target.resolve().is_relative_to(P.resolve())
        content=z.read(m);h=hashlib.sha256(content).hexdigest()
        if target.exists():assert hashlib.sha256(target.read_bytes()).hexdigest()==h,'Duplicate filename has different image data.'
        else:target.write_bytes(content)
        manifest.append({'image':target.name,'archive_member':name,'sha256':h,'size':len(content)})
def order(p):return [int(n) for n in re.findall(r'\d+',Path(p['image']).stem)]
manifest.sort(key=order)
save('source-integrity.json',manifest)
save('source-package.json',{'branch':'codex/comic-workspace','commit':branch,'path':'comic-workspace/episodes/19.zip','git_blob_sha':git_sha,'sha256':hashlib.sha256(data).hexdigest(),'size':len(data),'image_count':len(manifest),'ignored':ignored})
print(json.dumps({'commit':branch,'image_count':len(manifest),'first_names':[p['image'] for p in manifest[:8]],'last_names':[p['image'] for p in manifest[-6:]],'ignored':ignored},ensure_ascii=False,indent=2))
