from pathlib import Path
import hashlib
import json
import shutil

out=Path(__file__).resolve().parent
root=out.parents[3]
source=root/'write-comic-video-storyboards-gen2-8-1'
target=Path(r'C:\Users\86135\.codex\skills\write-comic-video-storyboards-gen2-8-1')
assert source.is_dir()
files={p.relative_to(source):hashlib.sha256(p.read_bytes()).hexdigest()
       for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
if target.exists():
    assert all((target/r).is_file() and hashlib.sha256((target/r).read_bytes()).hexdigest()==h for r,h in files.items()), 'Existing version differs; refusing overwrite.'
else:
    shutil.copytree(source,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
assert all(hashlib.sha256((target/r).read_bytes()).hexdigest()==h for r,h in files.items())
record={'installed_skill':str(target),'workspace_skill':str(source),'files_verified':len(files),
        'gen2_8_preserved':True,'invoke':'$write-comic-video-storyboards-gen2-8-1'}
(out/'installation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print('Installed and hash-verified',target)
