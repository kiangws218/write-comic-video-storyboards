from pathlib import Path
import json
R=Path(__file__).parent
DATA=[];SHOTS=[]
def add(id,lock,entities,actions,relations,bg,bubbles,motion,plan,review,sec,f,flags=None,bgmode='continuity',bgrefs=None,overlays=None,new_scene=False):
    p={'id':id,'lock':lock,'facts':{'entities':entities,'actions':actions,'relations':relations},'bgtype':('occluded' if bgmode=='occluded' else 'physical' if bgmode=='physical' else 'omitted'),'bgobserved':bg,'bgmode':bgmode,'bgbasis':('当前源格可见实景' if bgmode=='physical' else '主体遮住全部独立环境' if bgmode=='occluded' else '同场景有界重建，仅在留白中延续已核查的环境'),'bgrefs':bgrefs or ['第20話_01_003.jpg'],'bubbles':bubbles,'flags':flags or ([] if not bubbles else ['P','D'] if len(bubbles)>1 else ['P']),'risk':review,'motion':motion,'plan':plan,'coverage':review,'review':review,'new_scene':new_scene,'overlays':overlays or []}
    DATA.append(p);SHOTS.append({'id':id,'sec':sec,'b':list(range(len(bubbles))),'f':f})
def save(name):
    (R/'batches'/f'{name}-source.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2),encoding='utf8')
    (R/'batches'/f'{name}-shots.json').write_text(json.dumps(SHOTS,ensure_ascii=False,indent=2),encoding='utf8')
