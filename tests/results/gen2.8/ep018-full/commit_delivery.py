from pathlib import Path
import subprocess,json
O=Path(__file__).parent;R=O.parents[3];D=R/'comic-workspace/episodes/ep-018/storyboards/deliveries/2026-10-09_Gen2.8_整话非露骨改编'
def git(*args):return subprocess.run(['git',*args],cwd=R,check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8').stdout.strip()
assert git('branch','--show-current')=='codex/comic-workspace'
assert not git('diff','--cached','--name-only'),'Preserve external staging; do not include unrelated files.'
files=[R/'comic-workspace/episodes/ep-018/STATUS.md',R/'comic-workspace/episodes/ep-018/storyboards/current/第18话_制作分镜_Gen2.8.md']
files.extend(sorted(p for p in D.iterdir() if p.is_file()))
names=[p.relative_to(R).as_posix() for p in files]
git('add','--',*names)
before=git('rev-parse','HEAD')
run=subprocess.run(['git','commit','-m','Redo ep018 with latest Gen2.8 and document non-graphic adaptation'],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
result=run.stdout
if run.returncode and git('rev-parse','HEAD')==before:
    print(result)
    raise SystemExit(run.returncode)
commit=git('rev-parse','HEAD');manifest={'commit':commit,'branch':'codex/comic-workspace','paths':names,'remote_status':'not_pushed_yet','source_images_in_commit':False}
(O/'publish-status.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(result);print('Commit:',commit)
