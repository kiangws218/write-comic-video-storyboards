from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
NEW = ROOT / 'write-comic-video-storyboards-gen2-8-1'
SCRIPT = OUT / '第18话_前15格_完整分镜_Gen2.8.1.md'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(args, name):
    result = subprocess.run([sys.executable, '-X', 'utf8', *args], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8')
    (OUT / name).write_text(result.stdout + result.stderr, encoding='utf-8')
    print(name, 'exit', result.returncode, flush=True)
    return result

if sys.argv[1] == 'draft':
    result = run([str(NEW/'scripts/validate_storyboard.py'), str(SCRIPT), '--max-seconds','15',
                  '--image-dir',str(OUT/'analysis-proxies'), '--source-ledger',str(OUT/'source-ledger-v3.json'),
                  '--require-source-ledger'], 'validation-gen2.8.1.txt')
    print(result.stdout)
    if result.returncode:
        raise SystemExit(result.returncode)
    # The timestamped draft hash is fixed before reading the baseline body.
    frozen = OUT / 'independent-draft-freeze.json'
    if not frozen.exists():
        baseline = ROOT / 'comic-workspace/episodes/ep-018/storyboards/current/第18话_制作分镜_Gen2.8.md'
        record = {'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'new_draft_sha256':sha(SCRIPT), 'baseline_sha256':sha(baseline),
                  'baseline_read_at_freeze':False, 'scope':'01_001—05_003',
                  'qualification':'独立新稿，不是读取旧稿后逐句改写；不是模型或随机种子的受控A/B实验。'}
        frozen.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
elif sys.argv[1] == 'skill':
    quick = run([r'C:\Users\86135\.codex\skills\.system\skill-creator\scripts\quick_validate.py',str(NEW)],'skill-validation.txt')
    tests = run(['-m','unittest','discover','-s',str(NEW/'scripts'),'-p','test_*.py'],'regression-tests.txt')
    manifest = json.loads((OUT/'skill-baseline-manifest.json').read_text(encoding='utf-8'))
    changes=[]
    for rel, digest in manifest['baseline_hashes'].items():
        if sha(NEW/rel)!=digest:
            changes.append(rel)
    assert set(changes)=={'SKILL.md','agents/openai.yaml','references/dialogue-performance.md'}, changes
    assert all(sha(Path(manifest['baseline'])/rel)==digest for rel,digest in manifest['baseline_hashes'].items())
    report={'changed_files':changes, 'scripts_and_other_references_unchanged':True,
            'installed_gen2_8_unchanged':True, 'quick_validation_exit':quick.returncode,
            'regression_exit':tests.returncode, 'new_skill_path':str(NEW)}
    (OUT/'skill-change-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(tests.stdout+tests.stderr)
    if quick.returncode or tests.returncode:
        raise SystemExit(1)
