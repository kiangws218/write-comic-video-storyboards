from pathlib import Path
import json,math,re
O=Path(__file__).parent
def write(folder,page,rows):
    (O/folder/f'{page:02}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def obs(page,n,comp,entities,actions,relations,bubbles,jp,bg,plan,continuity,limit,kind='Mixed',background='physical',adapt=None):
    comp=comp.replace('居中','位于画面中央').replace('特写','近景特写')
    d=dict(image=f'第19話_{page:02}_{n:03}.jpg',composition_lock=comp,source_facts=dict(entities=entities,actions=actions,relations=relations),bubbles=bubbles,jp=jp,background=background,background_description=bg,kind=kind,anchor_phase='middle' if kind in ['State','Reaction','Mixed'] else 'result',plan=plan,continuity=continuity,admission=limit)
    if adapt:d['adaptation_scope']=adapt
    return d
def P(opening,beats,coupling,landing):return dict(opening=opening,beats=beats,coupling=coupling,landing=landing)
def shot(p,seconds,camera,action,bg,voice,light,sound,speech=0,acting=None,**kw):
    camera=camera.replace('居中','位于画面中央').replace('特写','近景特写')
    jp=kw.get('jp',p['jp']); budgets=[max(2 if len(re.sub(r'[\s。！？、…「」]', '',v))>=4 else 1.1,len(re.sub(r'[\s。！？、…「」]', '',v))/6+v.count('、')*.25+sum(v.count(c) for c in '。！？')*.45+len(re.findall(r'…+',v))*.6+.25) for v in jp]
    natural=sum(budgets)+max(0,len(jp)-1)*.35
    speech=max(speech,natural); seconds=max(seconds,math.ceil(speech))
    kw['bubble_seconds']=budgets
    return dict(image=p['image'],seconds=seconds,scene=kw.pop('scene','洞窟救援'),speech_seconds=speech,acting_seconds=acting if acting is not None else max(0,seconds-.6),fields=[camera,action,bg,voice,light,sound],**kw)
ROCK='深褐洞窟岩壁，凸石上缘稍亮，纵向石缝深暗，后层纹理低对比。'
LIGHT='左上方柔光落在人物与凸石上缘，人物以清晰线条和块面阴影表现，岩缝留深暗，环境色稳定。'
AIR='洞窟空气底声持续，岩壁间保留短促自然回响。'
def F(p,seconds,action,notes,bg=None,camera=None,sound=AIR,light=LIGHT,scene='临时诊所外',**kw):
    parts=[]
    for j,n in zip(kw.get('jp',p['jp']),notes):
        b=p['bubbles'][p['jp'].index(j)]
        label='内心' if len(b)>2 and b[2]=='inner' else '说'
        parts.append(f'{b[0]}{label}：“{j}”（{n}）')
    voice=''.join(parts) if parts else '无台词。'
    return shot(p,seconds,camera or '固定'+p['composition_lock']+'焦点落在主要人物或物件，前后层次保持清楚。',action,bg or p['background_description'],voice,light,sound,scene=scene,**kw)
