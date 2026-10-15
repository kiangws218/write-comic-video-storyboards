from pathlib import Path
import hashlib
import json
import sys

out = Path(__file__).resolve().parent
root = out.parents[3]
manifest = json.loads((out / 'skill-baseline-manifest.json').read_text(encoding='utf-8'))
baseline = Path(manifest['baseline'])
source = root / 'write-comic-video-storyboards-gen2-8-1'
target = root / 'write-comic-video-storyboards-gen2-8'
audit_dir = out / 'merge-to-gen2.8'
changed = {'SKILL.md', 'agents/openai.yaml', 'references/dialogue-performance.md'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def expected():
    files = {name: (source / name).read_bytes() for name in manifest['baseline_hashes']}
    for name in ['SKILL.md', 'agents/openai.yaml']:
        files[name] = files[name].decode('utf-8').replace('write-comic-video-storyboards-gen2-8-1', 'write-comic-video-storyboards-gen2-8').replace('Gen2.8.1', 'Gen2.8').encode('utf-8')
    assert {name for name, data in files.items() if sha(data) != manifest['baseline_hashes'][name]} == changed
    return files

files = expected()
mode = sys.argv[1]
if mode == 'stage':
    assert not target.exists(), 'Repository target already exists; inspect before replacing.'
    assert all(sha((baseline / name).read_bytes()) == digest for name, digest in manifest['baseline_hashes'].items()), 'Installed baseline changed since approved comparison.'
    for name, data in files.items():
        dest = target / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    audit_dir.mkdir(parents=True, exist_ok=True)
    for name in changed:
        dest = audit_dir / 'prior-local-gen2-8' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((baseline / name).read_bytes())
    record = {'repository_skill': str(target), 'installed_skill': str(baseline), 'changed_from_local_baseline': sorted(changed), 'file_hashes': {name: sha(data) for name, data in files.items()}}
    (audit_dir / 'merge-manifest.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared repository Gen2.8: 19 files; exactly three approved changes; Gen2.8 identity retained.')
elif mode == 'install':
    assert all((target / name).read_bytes() == data for name, data in files.items()), 'Repository package differs from reviewed merge.'
    assert all(sha((baseline / name).read_bytes()) == digest for name, digest in manifest['baseline_hashes'].items()), 'Installed baseline changed; refusing overwrite.'
    for name in changed:
        (baseline / name).write_bytes(files[name])
    assert all((baseline / name).read_bytes() == data for name, data in files.items())
    (audit_dir / 'sync-verification.json').write_text(json.dumps({'local_repository_files_identical': len(files), 'invoke': '$write-comic-video-storyboards-gen2-8', 'gen2_8_1_retained': True}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Merged into installed Gen2.8; all 19 local/repository files match; Gen2.8.1 retained.')
elif mode == 'verify':
    assert all((target / name).read_bytes() == (baseline / name).read_bytes() == data for name, data in files.items())
    print('Verified all 19 files: approved Gen2.8 merge, repository and installed version identical.')
else:
    raise ValueError(mode)
