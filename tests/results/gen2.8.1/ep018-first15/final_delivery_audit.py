from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

out = Path(__file__).resolve().parent
root = out.parents[3]
def read(name):
    return json.loads((out / name).read_text(encoding='utf-8'))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = read('skill-baseline-manifest.json')
installation = read('installation.json')
for rel, digest in manifest['baseline_hashes'].items():
    assert sha(Path(manifest['baseline']) / rel) == digest, rel
    assert sha(Path(installation['workspace_skill']) / rel) == sha(Path(installation['installed_skill']) / rel), rel
original = root / 'comic-workspace/episodes/ep-018/storyboards/current/第18话_制作分镜_Gen2.8.md'
assert sha(original) == '9c5d05bf3cfb4b2ec21188e5abcaad5b4baf3f6d3721eccedae630188f4836e8'
names = ['第18话_前15格_完整分镜_Gen2.8.1.md', '第18话_前15格_工作区基线_Gen2.8.md',
         '逐镜表演对照_Gen2.8_vs_Gen2.8.1.md', 'Gen2.8.1_迭代与第18话对比评估.md',
         'source-ledger-v3.json', 'comparison-data.json', 'validation-gen2.8.1.txt',
         'Gen2.8.1_skill_changes.diff', 'advisory-dispositions.json']
audit = {'verified_at': datetime.now(timezone.utc).isoformat(),
         'installed_new_files_match_workspace': len(manifest['baseline_hashes']),
         'installed_gen2_8_unchanged': True, 'original_storyboard_unchanged': True,
         'final_artifact_hashes': {name: sha(out / name) for name in names}}
(out / 'final-delivery-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Final artifacts recorded; new installation matches workspace; old skill and original storyboard unchanged.')
