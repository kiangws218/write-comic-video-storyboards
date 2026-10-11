from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE = REPO / 'write-comic-video-storyboards-gen2-8'
TARGET = Path(r'C:\Users\86135\.codex\skills\write-comic-video-storyboards-gen2-8')
BASE = '72a89198d6660479631d45be21f49dabad0316d0'
FILES = ['references/core-authoring.md', 'references/dialogue-performance.md', 'references/regression-cases.md']
MANIFEST = HERE / 'sync-manifest.json'

def digest(data):
    return hashlib.sha256(data).hexdigest()

mode = sys.argv[1]
if mode == 'prepare':
    assert not MANIFEST.exists(), 'Existing preparation must be reviewed instead of overwritten'
    rows = []
    for rel in FILES:
        old = (TARGET / rel).read_bytes()
        base = subprocess.check_output(['git', 'show', f'{BASE}:write-comic-video-storyboards-gen2-8/{rel}'], cwd=REPO)
        assert old.decode('utf-8').replace('\r\n', '\n') == base.decode('utf-8').replace('\r\n', '\n'), f'Unexpected installed baseline: {rel}'
        new = (SOURCE / rel).read_bytes()
        backup = HERE / 'prior-installed' / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(old)
        rows.append({'file': rel, 'before_sha256': digest(old), 'after_sha256': digest(new)})
    MANIFEST.write_text(json.dumps({'baseline_commit': BASE, 'installed_path': str(TARGET), 'source_path': str(SOURCE), 'status': 'prepared', 'files': rows}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared three-file update with byte-identical backups.')
elif mode == 'install':
    record = json.loads(MANIFEST.read_text(encoding='utf-8'))
    assert record['status'] == 'prepared'
    for row in record['files']:
        assert digest((TARGET / row['file']).read_bytes()) == row['before_sha256'], 'Installed skill changed after preparation'
        assert digest((SOURCE / row['file']).read_bytes()) == row['after_sha256'], 'Source changed after preparation'
    for row in record['files']:
        (TARGET / row['file']).write_bytes((SOURCE / row['file']).read_bytes())
    for row in record['files']:
        assert digest((TARGET / row['file']).read_bytes()) == row['after_sha256']
    record['status'] = 'installed_and_hash_verified'
    MANIFEST.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Installed and SHA-256 verified all three files.')
else:
    raise ValueError(mode)
