import hashlib, json, os, pathlib, subprocess, sys
import author_revision as author

ROOT,TASK,DELIVERY,CURRENT=author.ROOT,author.TASK,author.DELIVERY,author.CURRENT
ENV=os.environ.copy()
ENV['PATH']=str(ROOT/'tests/results/gen2.8/ep018-full/git-lfs-runtime')+os.pathsep+ENV['PATH']
ENV.update({k:'http://127.0.0.1:7890' for k in ['HTTP_PROXY','HTTPS_PROXY','ALL_PROXY']})
BASELINE='cd3c5d9a87f5a2045f342866131834194a8e61d4'
BRANCH='codex/comic-workspace'

def git(*args):
    p=subprocess.run(['git',*args],cwd=ROOT,env=ENV,capture_output=True)
    if p.returncode:raise RuntimeError((p.stderr or p.stdout).decode('utf-8',errors='replace'))
    return p.stdout.decode('utf-8',errors='replace').strip()

def paths():
    files=[CURRENT,ROOT/'comic-workspace/episodes/ep-019/STATUS.md']
    files.extend(sorted(p for p in DELIVERY.iterdir() if p.is_file()))
    files.extend(TASK/p for p in ['author_revision.py','verify_delivery.py','publish_workspace.py','inventory.json','image-observations.json','authored-plans.json','changes.json','skill-sync.json','skill-sync-plan.json','verification.json','protected-sources.json'])
    files.extend(TASK/'baseline'/p for p in ['第19话_制作分镜_Gen2.8.md','source-ledger-v3.json','warning-dispositions.json','validation-latest-skill.txt'])
    assert all(p.is_file() for p in files)
    return sorted(p.relative_to(ROOT).as_posix() for p in files)

def source_hashes():
    files=[p for p in (ROOT/'comic-workspace/episodes').rglob('*') if p.is_file() and 'source' in p.parts]
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

def check_skill():
    m=json.loads((TASK/'skill-sync.json').read_text(encoding='utf-8'))
    for item in m['files']:
        expected=item['sha256'];relative='write-comic-video-storyboards-gen2-8/'+item['file']
        data=subprocess.run(['git','show',author.SKILL_COMMIT+':'+relative],cwd=ROOT,env=ENV,capture_output=True,check=True).stdout
        assert hashlib.sha256(data).hexdigest()==expected
        assert hashlib.sha256((pathlib.Path(m['installed_path'])/item['file']).read_bytes()).hexdigest()==expected
        assert (ROOT/relative).read_bytes().replace(b'\r\n',b'\n')==data

def main():
    mode=sys.argv[1]
    assert git('branch','--show-current')==BRANCH
    if mode=='prepare':
        assert git('rev-parse','HEAD')==BASELINE
        assert git('ls-remote','origin','refs/heads/'+BRANCH).split()[0]==BASELINE
        assert not git('diff','--cached','--name-only')
        check_skill()
        hashes=source_hashes()
        (TASK/'protected-sources.json').write_text(json.dumps({'baseline':BASELINE,'files':hashes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        expected=paths()
        (TASK/'publish-plan.json').write_text(json.dumps({'branch':BRANCH,'baseline':BASELINE,'files':expected},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'files_to_publish':len(expected),'protected_source_files':len(hashes),'skill_install':'20 files match latest branch blobs','branch':BRANCH},ensure_ascii=False))
    elif mode=='commit':
        assert git('rev-parse','HEAD')==BASELINE
        assert git('ls-remote','origin','refs/heads/'+BRANCH).split()[0]==BASELINE
        expected=paths()
        already_staged=git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines()
        assert set(already_staged).issubset(set(expected)),already_staged
        assert expected==json.loads((TASK/'publish-plan.json').read_text(encoding='utf-8'))['files']
        assert source_hashes()==json.loads((TASK/'protected-sources.json').read_text(encoding='utf-8'))['files']
        git('add','--',*expected)
        staged=git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines()
        assert sorted(staged)==expected,(staged,expected)
        assert all('/source/' not in p for p in staged)
        git('diff','--cached','--check')
        print(git('commit','-m','Repair episode 19 camera, lens gaze and low-affect acting with latest Gen2.8'))
        print('COMMIT',git('rev-parse','HEAD'))
    elif mode=='push':
        head=git('rev-parse','HEAD')
        assert git('rev-parse','HEAD^')==BASELINE
        assert git('ls-remote','origin','refs/heads/'+BRANCH).split()[0]==BASELINE
        git('push','origin','HEAD:refs/heads/'+BRANCH)
        remote=git('ls-remote','origin','refs/heads/'+BRANCH).split()[0]
        assert remote==head
        before=json.loads((TASK/'protected-sources.json').read_text(encoding='utf-8'))['files']
        assert before==source_hashes()
        check_skill()
        result={'status':'pushed_and_remote_verified','commit':head,'remote_commit':remote,'branch':BRANCH,'source_files_preserved':len(before),'skill_commit':author.SKILL_COMMIT,'published_files':paths()}
        (TASK/'workspace-publish.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='published_files'},ensure_ascii=False))
    else:raise ValueError(mode)

if __name__=='__main__':main()
