from pathlib import Path
import json,re,hashlib

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
DATES={18:'2026-10-09_Gen2.8_整话非露骨改编',19:'2026-10-10_Gen2.8_整话'}
FIELDS=['镜头设计','可见动作','可见背景','台词与语气','光影布光','声音设计']
def parse(text):
    clip=0;out=[];shot=None
    for line in text.splitlines():
        m=re.match(r'## 【片段(\d+)】',line)
        if m:clip=int(m[1])
        m=re.match(r'\*\*分镜(\d+)（(\d+)秒）：\*\*',line)
        if m:
            shot={'target':f'片段{clip}/分镜{m[1]}','seconds':int(m[2]),'refs':[],'fields':{}};out.append(shot)
        elif shot and line.startswith('分镜参考'):shot['refs']+=re.findall(r'\[([^\]]+\.jpg)\]',line)
        elif shot:
            m=re.match(r'【([^】]+)】：(.*)',line)
            if m:shot['fields'][m[1]]=m[2]
    return out

if __name__=='__main__':
    inventory={}
    for ep,date in DATES.items():
        root=REPO/f'comic-workspace/episodes/ep-{ep:03}'
        current=root/f'storyboards/current/第{ep}话_制作分镜_Gen2.8.md'
        backup=HERE/f'baseline/ep-{ep:03}';backup.mkdir(parents=True,exist_ok=True)
        old=current.read_bytes();b=backup/current.name
        if b.exists():assert b.read_bytes()==old,'Baseline already differs'
        else:b.write_bytes(old)
        ledger=json.loads((root/f'storyboards/deliveries/{date}/source-ledger-v3.json').read_text(encoding='utf-8'))
        lp=backup/'source-ledger-v3.json'
        if not lp.exists():lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        shots=parse(old.decode('utf-8'));lookup={x['target']:x for x in ledger['shots']}
        for shot in shots:
            row=lookup[shot['target']];shot['evidence_images']=row.get('source_images',[])+row.get('derived_from',[])+row.get('evidence_images',[])
            shot['evidence_images']=list(dict.fromkeys(shot['evidence_images']))
        inventory[str(ep)]={'baseline_sha256':hashlib.sha256(old).hexdigest(),'shots':shots}
    (HERE/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Baseline saved:',[(ep,len(data['shots'])) for ep,data in inventory.items()])
