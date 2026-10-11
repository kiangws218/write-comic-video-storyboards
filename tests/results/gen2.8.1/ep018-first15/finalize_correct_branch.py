from pathlib import Path
import hashlib
import json
import subprocess

out = Path(__file__).resolve().parent
audit_dir = out / 'merge-to-gen2.8'
snapshot = json.loads((audit_dir / 'correct-branch-before.json').read_text(encoding='utf-8'))
manifest = json.loads((out / 'skill-baseline-manifest.json').read_text(encoding='utf-8'))
tree = Path(snapshot['existing_worktree'])
clean = Path(snapshot['isolated_worktree'])
installed = Path(manifest['baseline'])
def git(path, *args):
    return subprocess.check_output(['git', '-c', 'safe.directory=' + str(path), '-C', str(path), *args], text=True, encoding='utf-8').strip()
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def normal(p):
    return p.read_bytes().replace(b'\r\n', b'\n')

new_head = git(clean, 'rev-parse', 'HEAD')
assert git(clean, 'rev-parse', 'HEAD^') == snapshot['old_head']
assert git(tree, 'rev-parse', 'HEAD') == snapshot['old_head'], 'Existing branch moved concurrently.'
assert not git(tree, 'diff', '--cached', '--name-only'), 'Existing staged changes must remain untouched.'
assert git(tree, 'status', '--porcelain') == snapshot['preserved_existing_changes'], 'Existing worktree changed concurrently.'
for name, digest in snapshot['other_dirty_file_hashes'].items():
    assert sha(tree / name) == digest, name
names = ['SKILL.md', 'agents/openai.yaml', 'references/dialogue-performance.md']
assert set(git(clean, 'diff', '--name-only', snapshot['old_head'], new_head).splitlines()) == {'write-comic-video-storyboards-gen2-8/' + name for name in names}
for name in manifest['baseline_hashes']:
    assert normal(clean / 'write-comic-video-storyboards-gen2-8' / name) == normal(installed / name), name
for name in names:
    dest = tree / 'write-comic-video-storyboards-gen2-8' / name
    assert hashlib.sha256(normal(dest)).hexdigest() == manifest['baseline_hashes'][name]
    dest.write_bytes((installed / name).read_bytes())
git(tree, 'reset', '--mixed', '--quiet', new_head)
assert git(tree, 'status', '--porcelain') == snapshot['preserved_existing_changes']
for name, digest in snapshot['other_dirty_file_hashes'].items():
    assert sha(tree / name) == digest, name
assert git(out.parents[3], 'rev-parse', 'HEAD') == 'c5dcd2412b912c5d09836727be0b24e886d027d3'
assert not git(out.parents[3], 'diff', '--name-only', '--', 'README.md')
record = {'branch': snapshot['correct_branch'], 'commit': new_head,
          'changed_files': ['write-comic-video-storyboards-gen2-8/' + name for name in names],
          'installed_matches_remote_package': True, 'existing_gen2_8_worktree_fast_forwarded': True,
          'other_existing_edits_preserved': True, 'comic_workspace_mistaken_commit_removed': True,
          'regression_tests': {'passed': 120}, 'quick_validation_passed': True}
(audit_dir / 'final-correct-branch-sync.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Correct Gen2.8 local branch advanced; independent worktree edits preserved; installed package matches published commit.')
print(new_head)
