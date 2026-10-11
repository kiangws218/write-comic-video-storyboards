from pathlib import Path
import json,zipfile,hashlib,shutil
O=Path(__file__).parent;R=O.parents[3];m=json.loads((O/'delivery-manifest.json').read_text(encoding='utf-8'));D=Path(m['delivery']);C=D/'reference-crops';C.mkdir(exist_ok=True)
with zipfile.ZipFile(D/'reference-crops.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
    for n in ['第18話_04_001_上格.jpg','第18話_04_001_下格.jpg']:
        p=O/'source-originals'/n;shutil.copy2(p,C/n);z.write(p,arcname='reference-crops/'+n)
for p in [O/'source-ledger-v3.json',D/'source-ledger-v3.json']:
    d=json.loads(p.read_text(encoding='utf-8'))
    d['character_registry'][-1]['traits']=d['character_registry'][-1]['traits'].replace('橄榴绿','橄榄绿')
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in [O/'交付说明.md',D/'交付说明.md']:
    t=p.read_text(encoding='utf-8');t+='\n前段04_001上下分区参考图随交付打包为 `reference-crops.zip`，本机另有解压后的 `reference-crops/`，用于分镜引用。漫画原文件仍保持不变。\n'
    p.write_text(t,encoding='utf-8')
installed=Path('C:/Users/86135/.codex/skills/write-comic-video-storyboards-gen2-8');sync=json.loads((O/'skill-sync-manifest.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((installed/n).read_bytes()).hexdigest()==h for n,h in sync['hashes'].items())
print('Latest installed 20 skill files still match; two approved reference crops packaged.')
