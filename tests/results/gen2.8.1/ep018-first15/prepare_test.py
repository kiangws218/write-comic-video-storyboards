from pathlib import Path
import hashlib
import json
import shutil
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
INSTALLED = Path(r'C:\Users\86135\.codex\skills\write-comic-video-storyboards-gen2-8')
NEW = ROOT / 'write-comic-video-storyboards-gen2-8-1'
SOURCE = ROOT / 'comic-workspace/episodes/ep-018/source/monochrome-panels'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stage():
    if NEW.exists():
        raise RuntimeError('Version directory already exists; refusing to replace it.')
    shutil.copytree(INSTALLED, NEW, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for rel in ['SKILL.md', 'agents/openai.yaml']:
        p = NEW / rel
        s = p.read_text(encoding='utf-8')
        s = s.replace('write-comic-video-storyboards-gen2-8', 'write-comic-video-storyboards-gen2-8-1')
        s = s.replace('Gen2.8', 'Gen2.8.1')
        p.write_text(s, encoding='utf-8', newline='\n')
    manifest = {'baseline': str(INSTALLED), 'new_version': str(NEW),
                'baseline_hashes': {str(p.relative_to(INSTALLED)).replace('\\', '/'): sha(p)
                                    for p in INSTALLED.rglob('*') if p.is_file()
                                    and '__pycache__' not in p.parts and p.suffix != '.pyc'}}
    (OUT / 'skill-baseline-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Staged', NEW)

def fetch():
    originals = OUT / 'source-originals'
    originals.mkdir(exist_ok=True)
    files = sorted(p for p in SOURCE.glob('第18話_*.jpg') if p.name <= '第18話_05_003.jpg')
    assert len(files) == 15, len(files)
    def one(pointer):
        data = pointer.read_text(encoding='utf-8').splitlines()
        oid = next(s.split(':', 1)[1] for s in data if s.startswith('oid sha256:'))
        size = int(next(s.split()[1] for s in data if s.startswith('size ')))
        target = originals / pointer.name
        if target.exists() and sha(target) == oid:
            return {'image': pointer.name, 'sha256': oid, 'size': size, 'cache': True}
        local = ROOT / '.git/lfs/objects' / oid[:2] / oid[2:4] / oid
        if local.exists():
            payload = local.read_bytes()
            origin = 'local_lfs_cache'
        else:
            url = 'https://media.githubusercontent.com/media/kiangws218/write-comic-video-storyboards/codex/comic-workspace/comic-workspace/episodes/ep-018/source/monochrome-panels/' + urllib.parse.quote(pointer.name)
            with urllib.request.urlopen(url, timeout=20) as response:
                payload = response.read()
            origin = url
        assert len(payload) == size, (pointer.name, len(payload), size)
        assert hashlib.sha256(payload).hexdigest() == oid, pointer.name
        target.write_bytes(payload)
        return {'image': pointer.name, 'sha256': oid, 'size': size, 'origin': origin}
    with ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(one, files))
    (OUT / 'source-integrity.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Verified original JPEGs:', len(records))

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    {'stage': stage, 'fetch': fetch}[sys.argv[1]]()
