from pathlib import Path
import json

out = Path(__file__).resolve().parent
facts_path = out / 'source-observations.json'
data = json.loads(facts_path.read_text(encoding='utf-8'))
panel = next(p for p in data['panels'] if p['image'] == '第18話_02_001.jpg')
panel['original_resolution_viewed'] = True
panel['original_resolution_reason'] = '原尺寸逐手辨认：春子自己的手在衣领旁抓衣，青的一只白袖手环住春子抬起的前臂；没有第二只青的手搭肩。'
panel['composition_lock'] = '平视紧凑双人胸像，春子居左前景、半垂眼嘴略张，自抬前臂，自己的手在衣领旁；青从右侧探头张口，用一只白袖手环住春子的前臂，接触位于下半部。'
panel['source_facts']['actions'] = ['青张口，用一只手握住春子抬起的前臂', '春子半垂眼，嘴略张，自己的手在衣领旁抓衣']
panel['source_facts']['relations'] = ['春子在左前景，青从右侧靠近', '青的一只白袖手环住春子的前臂，衣领旁的手属于春子自己']
panel['performance_plan'] = {'opening': '春子半垂眼，前臂抬在胸前，自己的手抓着衣领旁的衣料；青靠在右侧，一只手接近她的前臂。', 'beats': ['青用一只手握住春子抬起的前臂，探身劝阻。', '青紧皱眉头说完劝告，春子半垂眼把脸偏向左侧外，仍抓着衣料。'], 'coupling': '明确演出介入与单手接触形成；春子的冷淡回应和青的焦急并存。', 'landing': '青仍握着春子的前臂，春子自己的手仍在衣领旁，两人的态度不同。'}
for p in data['panels']:
    if p['image'] in ['第18話_02_003.jpg', '第18話_03_001.jpg']:
        changed = json.dumps(p, ensure_ascii=False).replace('近侧上臂', '近侧手臂').replace('董白上臂', '董白手臂').replace('上臂接触', '抓臂接触')
        p.update(json.loads(changed))
    if p['image'] == '第18話_02_003.jpg':
        p['original_resolution_viewed'] = True
        p['original_resolution_reason'] = '原尺寸确认下缘手甲与董白近侧手臂的接触；不用上臂一词强定被裁切的部位。'
facts_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

story_path = out / '第18话_前15格_完整分镜_Gen2.8.1.md'
story = story_path.read_text(encoding='utf-8')
story = story.replace('手腕、搭肩的手与交叠前臂位于下半部。', '春子自己的手留在衣领旁，青握住她前臂的手位于下半部。')
story = story.replace('春子半垂着眼，前臂抬在胸前。青焦急地靠上来，一手接住她的手腕，另一手搭上肩部，探身把劝告说完。春子没有迎上她的目光，只把脸偏向画面左侧外，嘴略张，神情依旧冷淡；青皱着眉看向她，两只手留在肩和手腕上，把想继续争执的姿态稳住。', '春子半垂着眼，前臂抬在胸前，自己的手抓着衣领旁的衣料。青焦急地靠上来，用一只手握住她抬起的前臂，探身把劝告说完。春子没有迎上她的目光，只把脸偏向画面左侧外，嘴略张，神情依旧冷淡；青皱着眉看向她，握臂的手没有放开，春子也仍抓着衣料。')
story = story.replace('手搭肩与接住手腕时两声轻微衣料摩擦', '青握住前臂时一声轻微衣料摩擦')
story = story.replace('近侧上臂', '近侧手臂').replace('与上臂的接触', '与手臂的接触').replace('手甲与上臂分界', '手甲与手臂分界')
story_path.write_text(story, encoding='utf-8')

audit_path = out / 'advisory-dispositions.json'
audit = json.loads(audit_path.read_text(encoding='utf-8'))
for item in audit:
    if item['target'] == '片段1/分镜3':
        item['basis'] = '原尺寸复核手的归属后，修正为青的一只手握住春子前臂，春子自己的手仍在衣领旁抓衣；介入接触形成、探身劝阻和偏脸冷淡回应均保留。没有新增第二只青的手搭肩。'
    else:
        item['basis'] = item['basis'].replace('抓住上臂', '抓住近侧手臂')
audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Corrected observed hand ownership first, then the plan, storyboard and manual review.')
