import json,re,zipfile
from revise_identity import REPO,HERE,PRIOR,DELIVERY,MAPPING,parse,sha,jwrite

def protected(value,path=''):
    found={}
    if isinstance(value,dict):
        for key,item in value.items():
            at=path+'/'+key
            if key in ('source_text','script_text','jp','source_integrity'):found[at]=item
            else:found.update(protected(item,at))
    elif isinstance(value,list):
        for index,item in enumerate(value):found.update(protected(item,path+'/'+str(index)))
    return found

results=[]
for ep in (18,19):
    root=REPO/f'comic-workspace/episodes/ep-{ep:03}/storyboards'
    prior=root/'deliveries'/PRIOR
    dest=root/'deliveries'/DELIVERY
    filename=f'第{ep}话_制作分镜_Gen2.8.md'
    old=parse((prior/filename).read_text(encoding='utf-8'))
    new=parse((root/'current'/filename).read_text(encoding='utf-8'))
    assert len(old)==len(new)
    for a,b in zip(old,new):
        assert (a['target'],a['seconds'],a['refs'])==(b['target'],b['seconds'],b['refs'])
        for key in a['fields']:
            assert re.findall(r'“[^”]*”|「[^」]*」',a['fields'][key])==re.findall(r'“[^”]*”|「[^」]*」',b['fields'][key])
        if ep==18 and int(re.search(r'片段(\d+)',b['target'])[1])<11:assert a==b
        late=ep==19 or int(re.search(r'片段(\d+)',b['target'])[1])>=11
        forbidden=r'全盔守卫|受困少女|求助者|秃顶男子|巨型兽人' if ep==19 else r'董白|双马尾|守卫|男子'
        if late:assert not re.search(forbidden,json.dumps(b['fields'],ensure_ascii=False)),b['target']
    old_ledger=json.loads((prior/'source-ledger-v3.json').read_text(encoding='utf-8'))
    ledger=json.loads((dest/'source-ledger-v3.json').read_text(encoding='utf-8'))
    for group in ('panels','shots','performance','source_files'):
        assert protected(old_ledger[group])==protected(ledger[group]),group
    assert ledger['character_registry_source']['sha256']==sha(MAPPING)
    assert (root/'current'/filename).read_bytes()==(dest/filename).read_bytes()
    pack=dest/f'第{ep}话_完整分镜与身份审校_Gen2.8.zip'
    with zipfile.ZipFile(pack) as z:
        assert z.testzip() is None
        for f in dest.iterdir():
            if f.is_file() and f!=pack:assert z.read(f.name)==f.read_bytes(),f.name
    result={'episode':ep,'status':'pass','shots':len(new),'seconds':sum(s['seconds'] for s in new),
        'all_quoted_text_unchanged':True,'bubble_text_and_raw_integrity_unchanged':True,
        'times_and_references_unchanged':True,'ep18_early_identity_unchanged':True if ep==18 else None,
        'canonical_labels_checked':True,'current_delivery_zip_identical':True}
    results.append(result)
jwrite(HERE/'verification.json',results)
print(json.dumps(results,ensure_ascii=False))
