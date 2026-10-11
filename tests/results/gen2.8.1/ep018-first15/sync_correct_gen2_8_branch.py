from pathlib import Path
import hashlib
import json
import subprocess

out = Path(__file__).resolve().parent
manifest = json.loads((out / 'skill-baseline-manifest.json').read_text(encoding='utf-8'))
audit = json.loads((out / 'merge-to-gen2.8/merge-manifest.json').read_text(encoding='utf-8'))
clean_tree = Path('C:/Users/86135/OneDrive/文档/ChatGPT/New project/gen28-performance-sync')
base_tree = Path('C:/Users/86135/OneDrive/文档/ChatGPT/New project/write-comic-video-storyboards-gen27')
installed = Path(manifest['baseline'])
def normalized(p):
    return p.read_bytes().replace(b'\r\n', b'\n')
def git(path, *args):
    return subprocess.check_output(['git', '-c', 'safe.directory=' + str(path), '-C', str(path), *args], text=True, encoding='utf-8').strip()

assert git(clean_tree, 'rev-parse', 'HEAD') == '0a0bd1c2a7f3bf2393b3b1074675cf0c168f049a'
assert not git(clean_tree, 'status', '--porcelain'), 'Isolated worktree must be clean.'
differences = [name for name, digest in manifest['baseline_hashes'].items()
               if hashlib.sha256(normalized(clean_tree / 'write-comic-video-storyboards-gen2-8' / name)).hexdigest() != digest]
assert not differences, f'Remote branch baseline differs: {differences}'
for name in audit['changed_from_local_baseline']:
    path = base_tree / 'write-comic-video-storyboards-gen2-8' / name
    assert hashlib.sha256(normalized(path)).hexdigest() == manifest['baseline_hashes'][name], f'Existing worktree has independent edits: {name}'
before_dirty = git(base_tree, 'status', '--porcelain')
snapshot = {'correct_branch': 'codex/gen2.8-performance-router', 'old_head': git(base_tree, 'rev-parse', 'HEAD'),
            'existing_worktree': str(base_tree), 'isolated_worktree': str(clean_tree),
            'preserved_existing_changes': before_dirty,
            'other_dirty_file_hashes': {name: hashlib.sha256((base_tree / name).read_bytes()).hexdigest()
                                      for name in ['GEN2.8-V3-REFACTOR.md', 'README.md', 'write-comic-video-storyboards-gen2-8/scripts/audit_seedance_prompt.py', 'GEN2.8-OPTIMIZATION-PLAN.md', 'write-comic-video-storyboards-gen2-8/scripts/test_audit_seedance_prompt.py']}}
(out / 'merge-to-gen2.8/correct-branch-before.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for name in audit['changed_from_local_baseline']:
    (clean_tree / 'write-comic-video-storyboards-gen2-8' / name).write_bytes((installed / name).read_bytes())
print('Confirmed remote branch matches prior Gen2.8; applied exactly the three approved changes in isolation.')
print('Original Gen2.8 worktree independent edits recorded and untouched.')
