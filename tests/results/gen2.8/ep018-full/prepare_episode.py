from pathlib import Path
import concurrent.futures
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
REF = 'origin/codex/gen2.8-performance-router'
INSTALLED = Path('C:/Users/86135/.codex/skills/write-comic-video-storyboards-gen2-8')
PREFIX = 'write-comic-video-storyboards-gen2-8/'
def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])
def digest(data):
    return hashlib.sha256(data).hexdigest()
def order(path):
    match = re.search(r'(\d{2})_(\d{3})\.jpg$', path.name)
    return tuple(map(int, match.groups()))

def export():
    files = git('ls-tree', '-r', '--name-only', REF, '--', PREFIX).decode('utf-8').splitlines()
    assert files
    records = {}
    for name in files:
        rel = name[len(PREFIX):]
        data = git('show', REF + ':' + name)
        dest = OUT / 'skill-latest' / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        records[rel] = digest(data)
    save('skill-sync-manifest.json', {'ref': REF, 'commit': git('rev-parse', REF).decode().strip(), 'hashes': records})
    print('Exported latest Gen2.8:', len(records), 'files.')

def install():
    manifest = json.loads((OUT / 'skill-sync-manifest.json').read_text(encoding='utf-8'))
    for rel, expected in manifest['hashes'].items():
        data = (OUT / 'skill-latest' / rel).read_bytes()
        assert digest(data) == expected
        prior = INSTALLED / rel
        if prior.exists():
            backup = OUT / 'skill-before-sync' / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_bytes(prior.read_bytes())
        for folder in [INSTALLED, ROOT / PREFIX]:
            dest = folder / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
    assert all(digest((INSTALLED / rel).read_bytes()) == h for rel, h in manifest['hashes'].items())
    save('skill-sync-verification.json', {'commit': manifest['commit'], 'files_verified': len(manifest['hashes']), 'installed': str(INSTALLED)})
    print('Installed latest Gen2.8 and synchronized local package; all files hash verified.')

def fetch():
    source = ROOT / 'comic-workspace/episodes/ep-018/source/monochrome-panels'
    originals = OUT / 'source-originals'
    originals.mkdir(parents=True, exist_ok=True)
    old = ROOT / 'tests/results/gen2.8.1/ep018-first15/source-originals'
    def one(pointer):
        raw = pointer.read_bytes()
        if not raw.startswith(b'version https://git-lfs'):
            data, origin = raw, 'workspace_original'
            oid, size = digest(data), len(data)
        else:
            lines = raw.decode().splitlines()
            oid = next(s.split(':', 1)[1] for s in lines if s.startswith('oid sha256:'))
            size = int(next(s.split()[1] for s in lines if s.startswith('size ')))
            choices = [originals / pointer.name, old / pointer.name, ROOT / '.git/lfs/objects' / oid[:2] / oid[2:4] / oid]
            cached = next((p for p in choices if p.exists() and digest(p.read_bytes()) == oid), None)
            if cached:
                data, origin = cached.read_bytes(), 'verified_cache'
            else:
                url = 'https://media.githubusercontent.com/media/kiangws218/write-comic-video-storyboards/codex/comic-workspace/comic-workspace/episodes/ep-018/source/monochrome-panels/' + urllib.parse.quote(pointer.name)
                for attempt in range(3):
                    try:
                        with urllib.request.urlopen(url, timeout=20) as response:
                            data = response.read()
                        break
                    except Exception:
                        if attempt == 2:
                            raise
                origin = url
        assert len(data) == size and digest(data) == oid, pointer.name
        (originals / pointer.name).write_bytes(data)
        return {'image': pointer.name, 'order': list(order(pointer)), 'size': size, 'sha256': oid, 'origin': origin}
    paths = sorted(source.glob('*.jpg'), key=order)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(one, paths))
    save('source-integrity.json', records)
    print('Verified episode18 original images:', len(records), 'remaining:', sum(r['order'][0] >= 6 for r in records))

def proxies():
    from PIL import Image
    dest = OUT / 'analysis-proxies'
    dest.mkdir(exist_ok=True)
    for path in (OUT / 'source-originals').glob('*.jpg'):
        with Image.open(path) as im:
            im.thumbnail((720, 720))
            im.convert('RGB').save(dest / path.name, quality=92)
    old = ROOT / 'tests/results/gen2.8.1/ep018-first15'
    for region in ['第18話_04_001_上格.jpg', '第18話_04_001_下格.jpg']:
        shutil.copy2(old / 'source-originals' / region, OUT / 'source-originals' / region)
        shutil.copy2(old / 'analysis-proxies' / region, dest / region)
    print('Cached 720p image proxies; preserved approved source-region crops.')

{'export': export, 'install': install, 'fetch': fetch, 'proxies': proxies}[sys.argv[1]]()
