"""Apply the image-reviewed final pass to the saved draft, retaining its baseline."""
from pathlib import Path
import copy, importlib.util, json, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent / 'archive/2026-10-11_Gen2.8_最终动作复查前'
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def write(path, data): path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
files = {f.name: read(f) for f in (BASE/'batches').glob('*.json')}
panels = {p['id']: p for name, rows in files.items() if name.endswith('-source.json') for p in rows}
drafts = [s for name, rows in sorted(files.items()) if name.endswith('-shots.json') for s in rows]
revisions = []
def shot(pid, n=0): return [s for s in drafts if s['id']==pid][n]
def amend(pid, reason, **kwargs):
    p=panels[pid]; p.update(kwargs); p['review']=reason
    revisions.append({'image': '第20話_'+pid+'.jpg', 'decision':reason})
def action(pid, prose, opening, beats, coupling, landing, reason, n=0, admissions=None):
    s=shot(pid,n); s['f'][1]=prose; s['plan']=[opening,beats,coupling,landing]
    s['motion_override']=reason
    if admissions is not None: s['admissions_override']=admissions
    revisions.append({'image':'第20話_'+pid+'.jpg','shot_index':n,'decision':reason})
def admit(claim,evidence): return {'claim':claim,'visual_evidence':evidence}

# Newly initiated cloth contact: the knife hand remains the knife hand.
action('05_002',
 '春子伸向帽顶的手从左上进入，张开的指尖先贴上兜帽布边，再向掌心合拢。抓点收出短褶，她把布边向上提起一小段，帽缘随力道抬高；手仍攥住这处布边，黑袍较宽的下部留在画面下方。',
 '手从左上接近帽顶，指端张开', ['指端接触帽边并抓紧','抓点形成褶线后向上提起'],
 '承接握刀腕已停止下压，以另一可见手完成本格抓帽任务', '手仍抓着帽边并上提',
 'Action：源格抓帽为contact/middle锚点；补同一只手从左上入画的最短接近→抓紧→已有上提，不换手、不收刀。',
 admissions=[admit('手进入画面抓住帽边并向上提起','05_002当前手臂由左上连到抓点，布边被指端包住并有受力褶；入手为本次接触最短前导，抓点与源锚点相同。')])

# A low-angle group crop does not prove that the central figure stood up.
amend('08_001','07_002中央蹲姿之后，08_001仅露上身，不能据近景高低认定起立。保持中央前、两侧后和五人帽口，不新增起立桥。',
 motion='State：上身近景显露五人前后层次；中央下肢和支撑被裁去，姿态不作起立解释。',
 risk='五人数量与前格一致；中央下肢不可见，近景不证明由蹲到站。')

# Actual blade preparation: closed eyes at the source anchor.
p=panels['09_002']; p['facts']['relations'].append('双眼闭合，嘴部闭合')
action('09_002',
 '董白双手握住刀柄，从肩侧把刀抬到头顶，肘部随抬升展开，长冰刃斜向右下。她闭着眼睛，嘴角收住，肩部沉下承住刀的重量；双马尾在举臂之后向两侧扬过，再缓缓回落。冰面上的冷纹渐渐清楚，双臂仍举着刀，闭眼的专注持续。',
 '双手握刀，刀在肩侧，眼睛闭合', ['举臂把刀抬到头顶','闭眼承重，马尾随举臂回摆'],
 '握刃准备配合能力介绍，动作不借旁白扩成攻击', '刀举在头顶斜向右下，双眼闭合',
 'Action：09_001握持→09_002举刃contact/middle锚点；当前图双眼为完整闭眼线，修正原稿前下凝视。')

# Reinspect anatomy rather than inherit an adjacent panel's earlier misreading.
for pid in ['10_002','11_001','11_002','11_003']:
    p=panels[pid]
    trans=[('巨大的脚掌局部','巨大的手掌局部'),('巨大的脚掌','巨大的手掌'),('小腿','前臂'),('脚掌','手掌'),('脚趾','手指'),('趾端','指端'),('踝部','腕部'),('趾侧','指侧'),('踝侧','腕侧'),('落脚','压掌'),('脚缘','掌缘'),('脚面','手背'),('脚下','掌下'),('踩压','按压'),('重踩','重复压掌')]
    def convert(v):
        if isinstance(v,str):
            for a,b in trans: v=v.replace(a,b)
            return v
        if isinstance(v,list): return [convert(x) for x in v]
        if isinstance(v,dict): return {k:convert(x) for k,x in v.items()}
        return v
    p.update(convert(p))
    for s in [s for s in drafts if s['id']==pid]: s.update(convert(s))
    p['review']='复看720p并以10_002、11_002原图核对：11_002下前外展为拇指，向左并列长指连接手背，右缘为腕部；原脚掌误读撤回。维持实际掌指按石、环纹及后续碎裂，不添走路或踩踏。'
    p['resolution']='original' if pid in ['10_002','11_002'] else '720p'
    if p['resolution']=='original': p['resolution_escalation_reason']='巨大手/足误读会改变主要动作；原图核对拇指外展、并列长指与腕部连接。'
    revisions.append({'image':'第20話_'+pid+'.jpg','decision':p['review']})
shot('10_002')['f'][0]='70mm贴近石面的低角度手掌特写，巨大手指占下中前景，前臂从上中央延下，碎石围住按压区；固定机位，指端与石块的前后关系清楚。'
action('10_002',
 '巨大的手掌从碎石上方短短压下，张开的手指随掌面落到石块之间，接触处的小石向两侧弹起。手背在承压时绷紧，指端压住碎石；弹起的石块逐块落回，手掌仍撑在石地上。',
 '巨掌贴近石面，手指张开', ['巨掌压下接触石块','石块从接触处弹起后落回'],
 '主动作是手掌按地，进入同一手掌的环纹局部', '巨掌撑住石面，指端接触持续',
 'Action：原图竖向前臂连到张开的掌指，石块腾起；最短压掌前导恢复接触锚点。',
 admissions=[admit('巨大手掌向下按压碎石','10_002原图掌指连接前臂；11_002原图明确拇指、并列长指及腕部。接触与腾起碎石支持最短压下，不能写成落脚。'),admit('碎石向两侧弹起','10_002当前接触周围可见离开石面的碎石，随后只落回同一区域。')])
shot('10_002')['f'][5]='一声重而短的掌面撞石闷响，碎石接连碰撞落下，尾部有细碎砂砾声。'
shot('11_001')['f'][0]='75mm平视巨大手掌近景，手背横占中央，长指伸向左侧，拇指分在下前，腕部出右缘；白亮弧纹分布在掌指周围，尖角碎石退在后层。固定机位。'
shot('11_001')['f'][1]='巨大手掌持续撑在碎石上，几道冷白环纹从掌指周围绕过，在指侧与腕侧交错收束。手背随承压绷紧，指端仍压在石块之间；白亮逐渐变淡，手掌的按地位置清楚。'
shot('11_002')['f'][0]='75mm平视巨大手掌近景，手背横占中央，长指朝左、拇指分在下前，腕部延出右缘；灰褐碎石托住掌指，固定机位，焦点覆盖手背和接触边界。'
shot('11_002')['f'][1]='巨大手掌撑在碎石之间，掌缘细砂逐渐落低，绷紧的手背纹理稍稍放松。长指和拇指仍压在石块上，腕部停在右侧；两秒内细砂落定，按地的结果保留清楚。'
shot('11_003')['f'][0]='85mm平视掌指局部特写，灰暗断块在中央前景，大手局部从右缘伸入，黑色飞溅斜越上右，下方石块退在后景；固定机位。'
action('11_003',
 '巨大的指端仍压在石块之间，断口突然分开，灰暗断块从原接触处短短离开，黑色飞溅沿右上方向散开。较重的断块转而落向下方石面，细小黑滴继续向上散过，手的较大部分仍从右侧延入。',
 '巨大指端仍在石块间', ['指端断口分开，断块离开接触处','黑色飞溅向右上散开，断块转落'],
 '接11_002完整掌指状态，直接兑现源断裂结果，不新增未画出的攻击路线', '断块下降，黑滴仍在飞散，手从右侧延入',
 'Action：11_002完整掌指→11_003明确断块离位，最短局部分开恢复本格middle锚点；不以已裂后细动替代主要断裂，不扩写新刀路或其他伤处。',
 admissions=[admit('巨大指端分裂、断块和黑色飞溅散开','11_003当前指端有分离断块、右上飞溅；11_002完整掌指在石块间。最短局部断口分开至当前离位锚点，不添加攻击者或刀路。')])

# Keep aftermath in place, and carry the contact through the later reaction.
action('12_002',
 '董白的肩背随既有挥刀余势向右后拧转，双手在右后把刀柄拉住，横在下缘的前臂逐渐止住行程。她圆睁着眼睛，露出的眉头向中间压低，牙关咬紧，目光扣向左前；马尾在身体收势之后继续外扬，再向后落回，急促呼吸让胸肩有起伏，双手仍握住刀柄。',
 '挥刀已在执行尾段，双手刀柄位于右后', ['肩背与前臂收住已有余势','眉眼咬牙回应，马尾晚于身体回摆'],
 '前一刀的身体收势与旁白评价并行，不另起攻击', '刀柄在右后握稳，董白仍看左前',
 'Action：当前前臂横在下前、双手右后、马尾外扬及咬牙为收势中段；补可读的前臂止动和身体先、头发后。')

# Actual action can use graphics without turning them into room geometry.
shot('06_001')['f'][2]='图形底场由青灰渐暗至蓝黑，稀疏斜向细线从上左和下右向画缘展开，脸后的中区保持清楚。'
shot('06_001')['bgmode']='graphic'
panels['06_001']['bgbasis']='源格本身有斜向强调线，突然睁圆瞳仁收小的惊觉可作短心理强调；将既有线势和灰底配成青灰至蓝黑。下一格06_002回到可见水域，不把线势当实物气流。'
panels['06_001']['bgtype']='graphic'; panels['06_001']['bgobserved']='灰色底面及画缘斜向强调细线，脸部占中间。'
shot('12_002')['f'][2]='图形底场从左下蓝灰暗面过渡到右上冷白亮面，细斜线沿左下至右上的方向铺开，脸部后方留出较宽亮区。'
shot('12_002')['bgmode']='graphic'
panels['12_002']['bgbasis']='12_002源图斜向密线与亮暗对比明确，保留其收势强调功能并选冷白/蓝灰生产配色；不是给空白随意加底。下一13_001转原有断裂图形，13_002恢复两主体关系。'
panels['12_002']['bgtype']='graphic'; panels['12_002']['bgobserved']='从左下至右上的斜向密线，左下较暗、右上较亮。'
shot('23_001')['f'][2]='图形底场由左侧冷白向右侧青灰过渡，黑灰细线从左缘斜向中右收束，帽缘后的区域对比稍低。'
shot('23_001')['bgmode']='graphic'
panels['23_001']['bgbasis']='23_001当前明确带斜向细线和偏头反应；保留原有反应图形并配成冷白/青灰。23_002回到青脸前的柔焦水域，不使线势证明后退或逃跑。'
panels['23_001']['bgtype']='graphic'; panels['23_001']['bgobserved']='灰白底场及画面左缘向中右收束的细斜线。'

# The folded-arm state is visible in the full-resolution source.
p=panels['20_002']; p['lock']='青正面胸像，尖耳长白发、内低外高的眉；两前臂交叉在胸下，两侧手指搭在对侧袖口/臂侧，下缘裁切。'
p['facts']['relations'] += ['两前臂交叉在胸下','两侧手指搭在对侧衣袖附近']
p['resolution']='original'; p['resolution_escalation_reason']='胸像下缘的交叉前臂决定横抱是否仍持续；原图确认双臂抱在胸下，春子不在怀中。'
shot('20_002')['f'][0]='65mm平视青正面胸像近景，脸居中央，长白发和尖耳分在两侧，蓝衣领及白领带在下中，交叉前臂与两侧手指保留在下缘；固定机位，焦点覆盖脸部和交臂姿态。'
action('20_002',
 '青把收回身前的两条前臂交叉在胸下，两侧手指搭住对侧袖口附近。她眉头向内收低，红眼正对镜头前方，嘴唇逐渐压紧；吸入一口短气之后，肩部在交臂姿态里稳住，紧绷的判断停在脸上，双臂仍抱在胸下。',
 '双臂已收回身前，手在胸下', ['前臂交叉至源抱臂锚点','内眉压低、唇压紧并继续观察'],
 '放下动作已完成，交臂反应明确进入独立站姿', '交叉双臂，正面注视',
 'Reaction：原图胸下清楚交叉两前臂；不再按承重怀抱解释。前置动作桥完成春子落地，两前臂的最短交叠至源middle锚点。',
 admissions=[admit('两前臂交叉在胸下','20_002原图两前臂交叉、两侧手搭在对侧袖口附近；最短局部交臂恢复该源姿，不引入新的对象。')])

# Hair hand stays raised through partner coverage, then moves once.
action('22_001',
 '青的脸从向右略转回正面，缓缓吐出一口长气，双眼合上，头低下一点。她的手从画面左下抬到脸侧，张开的指尖拨住一束白发并把它送向左外，发梢顺势扬过；后半句里指尖离开发束，手仍张着停在脸旁，肩部随呼气落低，闭眼的无奈持续。',
 '脸略向右，手从左下接近发束', ['转回正面、闭眼长呼气','抬手拨发、指尖离开发束但手留脸旁'],
 '对沉默的回答作无奈回应，拨发只作一次', '正面略低头、眼闭，张手在脸旁',
 'Mixed：22_001可见张手、外扬发束和闭眼；补最短抬手至已见拨发contact锚点，侧脸转正由21_002/当前前后朝向支持。',
 admissions=[admit('抬手拨开白发并转回正面','当前22_001手在脸侧、发束向左扬，21_002头向右；同一脸侧最短抬手拨发，有限转正恢复源锚点。')])
action('22_002',
 '青的脸由正面略低转向右侧，闭着的眼睛在上缘外逐渐睁开；她叫出称呼，嘴唇合住，脸旁张开的手仍留在裁切外同一高度。春子的眼皮稍抬，头向左偏过一点，露出的内眉仍高，目光落向画面左前。青等待这一声回应后把托付说完，下颌微收；春子继续看向左前，嘴唇合住，两人的注意仍接在这次托付上。',
 '青略低头正面，拨发后的手仍在脸旁；春子在右后', ['青转向右侧称呼，春子抬眼回应','青在回应后说完托付，春子保留注意'],
 '呼名、应答、托付在同框里依次发生', '青头向右，手仍在脸旁；春子望左前',
 'Mixed：头部方向改接22_001正面略低的镜尾，局部转向恢复22_002关系middle锚点。青的抬手在当前裁切外，只在内部状态中继承，不生成不可见手或眼。')
# Do not put invisible eye/hand performance into a generatable field.
shot('22_002')['f'][1]='青的脸由正面略低转向右侧，嘴唇短短叫出称呼，随后合住等回应。春子眼皮稍抬，头向左偏过一点，露出的内眉仍高，目光落向画面左前。青在回应后把托付说完，下颌微收；春子继续看向左前，嘴唇合住，两人的注意仍接在这次托付上。'
action('22_003',
 '青把脸旁的右手落向左臂袖口，左前臂同时横过胸前，朝画面左侧展开。右手抓住袖边向左肘捋高，衣袖在画面右侧的肘部堆起，左前臂显露，张开的掌面朝向前方。掌侧几处冷白亮点依次清楚，她眉头低收，红眼扣住前方，把判断和打算说完；右手仍扣着肘旁袖边，横展的左臂稳住，掌上的白亮继续闪动。',
 '拨发右手仍在脸旁，左臂在身前较低处', ['右手落向左袖边，左前臂同时横展','右手将袖边捋至左肘，左掌开放后显出白光'],
 '拨发的是右手，展开的是左臂；右手转为捋袖任务，回应镜不重置手位，也不把两臂混成一臂', '左裸前臂横向画面左，袖堆在右侧左肘；右手扣袖边，左掌有白光',
 'Action：复看22_001/22_003原图，前格脸旁手连接画面左侧右肩，本格裸前臂从画面右侧左肘横过胸前，右手扣在其袖边。修正同一条手臂的错误衔接：右手从高位落到已见袖边，左臂横展，最短捋袖至当前堆袖middle锚点；袖子本身不是新增道具。',
 admissions=[admit('右手抓住袖边捋高、左前臂横展','22_003原图裸前臂从右侧肘部横展向左，袖布堆在肘部，另一只手扣在袖边下方；22_001是右手拨发。最短右手落到袖边并捋高恢复当前接触和裸前臂锚点，不把两只手混同。'),admit('掌侧白光亮起','22_003当前开放左掌有明确白光，横展到位后仅让已见亮点显出。')])
p=panels['22_003']; p['facts']['entities'] += ['扣袖边的右手','左臂衣袖']
p['facts']['relations'] += ['裸前臂从画面右侧左肘横展向左','右手扣在左臂袖边下方']
p['resolution']='original'; p['resolution_escalation_reason']='必须区分拨发右手与横展左臂，并核对肘旁捋袖接触；原图核对两臂连接和右手袖边位置。'
if 'G' not in p['flags']: p['flags'].append('G')

action('23_004',
 '兜帽来者的手从右下随袍袖抬到肩侧偏高处，腕部在这里停稳。中指向拇指靠拢，指腹相贴，其余手指自然弯着；袖口在抬腕之后垂下，帽口仍朝前，准备好的指端接触保持到镜尾。',
 '手在右下较低处，帽口朝前', ['抬腕到肩侧','中指与拇指贴合准备响指'],
 '抬手形成下一镜唯一一次响指的准备接触', '腕在肩侧偏高，中指拇指相贴',
 'Action：23_004首次手势为抬腕/贴指middle锚点，补同一袖口内短抬手，不提前弹开；24_001才响一次。',
 admissions=[admit('抬手并使中指靠拢拇指','23_004当前手抬在肩側、袍袖向下且指腹靠拢；同一右下可见区域短抬腕恢复准备锚点。')])

action('25_001',
 '深色手从左上进入，张开的指端朝青肩面落近，先贴住肩侧，再让其余指腹落稳。接触保持短短一拍，指端随即抬离肩面，肩侧几个冷白亮点闪起；白发在手侧颤过，手停在肩面上方，亮点逐渐变弱。',
 '深色手从左上接近肩面', ['指端落下形成接触并停0.4秒','指端抬离，肩侧细闪亮起'],
 '回忆的新接触形成一次，再接源图下段抬离结果', '手在肩面上方，细闪收弱',
 'Action：25_001上段是新接触B，不当作全镜起始；以同手同肩从左上最短落指A，0.4秒接触锚点后连接图内明确抬离及细闪C。两段为图内明确连续阶段，未补脱衣机制。',
 admissions=[admit('深色手落向肩面形成接触后抬离','25_001图内上段手肩接触、下段同轴抬离及细闪；最短落指进入上段contact锚点，再按明确下段抬离。'),admit('肩侧细闪亮起','25_001下段指端抬离之后的肩侧细闪可见。')])
shot('25_001')['f'][5]='指端贴住与离开肩面各一声细擦，细亮点一声短清响，餐馆低缓人声持续在远处。'

action('14_002',
 '巨大的手指从董白身侧已有的开口向内圈拢，指腹逐渐贴住她的衣侧，黑白头发在上方指间颤过。指间开口合小，手背绷出清楚褶线，腕侧亮点一闪后变弱；圈拢的手稳住，董白头部仍露在指间上方。',
 '巨指在董白身侧，指间尚有开口', ['指腹圈拢到衣侧','指间开口合小至源抓握接触'],
 '断刃后抓握形成一次，下一镜接持续抓握的反应', '董白被包在指间，头部露在上方',
 'Action：14_002接触为contact/result锚点；保留最短合指并使前导可见，不只以手背纹理充当抓住。',
 admissions=[admit('巨手手指圈拢抓住董白','14_002当前黑白头发露在合拢巨指上方，手背向镜头，指腹与身体接触；只从现有开口圈拢到源接触，不添远处伸手路径。')])

def bridge(pid,key,sec,fields,plan,evidence,previous,next_image,changes,other=None,claims=None):
    row={'id':pid,'review_key':key,'sec':sec,'b':[],'f':fields,'plan':plan,'acting':sec,
      'purpose':evidence,'motion_override':evidence,'bgmode':'continuity',
      'uncited':{'coverage_type':'action_phase','visual_function':evidence,
       'coverage_changes':['subject_focus','visible_information'],
       'coverage_evidence':'；'.join(changes[0]), 'next_source_image':next_image,
       'next_source_changes':['subject_focus','visible_information'],
       'next_source_evidence':'；'.join(changes[1])},
      'previous_review_key':previous}
    if other: row['evidence_images_override']=['第20話_'+other+'.jpg','第20話_'+pid+'.jpg']
    if claims: row['claims']=claims
    owned=[s for s in drafts if s['id']==pid]
    owner_file=next(rows for name,rows in files.items() if name.endswith('-shots.json') and any(s is owned[0] for s in rows))
    owner_file.insert(owner_file.index(owned[0]),row); drafts.insert(drafts.index(owned[0]),row)
    revisions.append({'image':'第20話_'+pid+'.jpg','review_key':key,'decision':evidence})
    return row

formation=bridge('07_001','07_001-formation',2,[
 '55mm平视动作近景，机位略低于胸口，裁切从双人肩部至膝下；青躯干在右后，两条承托前臂位于中间，春子的黑裙与双腿在左前遮住部分青的衣身，刀占右下。固定机位，焦点覆盖托肩与承膝的接触位置。',
 '青的一条前臂从春子肩后合近，另一条前臂从膝弯下托入。春子的膝部随承托收起，两条腿离开下缘低处，身体横向落进青的臂弯；青双臂收向胸前承住重量，托肩与承膝两处支撑同时到位，春子握着的刀低垂向右下。',
 '下方深灰蓝水面带着断续冷白亮纹，两人下方黑色倒影碎成小片，后层水雾低淡。',
 '无台词。',
 '冷白水光由前下照亮前臂与刀面，春子的黑裙保留折面阴影，青的蓝袖明暗分开，支撑处的薄影清楚。',
 '衣料在承托处短短绷擦，一口短吸气，低柔水声持续。'],
 ['青在春子身后侧，两前臂接近肩后和膝弯', ['两前臂合近托肩承膝','膝部抬起，身体进入臂弯'], '把源图横抱真正形成后再交给双人回应镜', '托肩承膝同时到位，春子横抱且刀朝右下'],
 'Action bridge：07_001当前直接建立青托肩承膝、春子双腿离地的横抱。补同一对人物、同一侧最短合臂承托→双腿抬起；不是从06_003匿名肢体反推跳跃，也不加奔跑、飞跃或转场。动作在本镜末抵达横抱，下一源镜只承重与回应。',
 '06_003','第20話_07_002.jpg',
 [['主体由匿名肢体/布浪变为两条承托前臂和膝弯','可见信息由浪过布边变为抱持接触的形成'],
  ['下一漫画07_002以两腿为前景开口、远处五人群组为主；本镜主视觉为托肩承膝的接触','下一漫画给出远群组数量与空间；本镜只读抱持形成，信息及前后层次不同']])
formation['uncited']['owner_anchor_comparison']='紧接的本格源镜07_001为双人面部与完整怀抱；动作桥以肩下承托接触为主，较低正侧向动作近景；主体焦点和可读信息不同。'
formation['admissions_override']=[admit('青合臂承托并抱起春子','07_001可见青一手肩后、一手承膝，春子腿离地且刀下垂。最短合臂承托形成同一抱持；本镜只补这个动作的必要前导。')]
shot('07_001',1)['f'][1]='青的双臂已经在肩后和膝下承住春子，躯干在承重时略向后压稳，怀里的双腿和黑裙余摆逐渐收下。春子把目光转向前下，短短开口，眼皮又低下来；刀低垂向右下，青继续托着她，双臂的支撑位置稳定。'
shot('07_001',1)['plan']=['青已完成托肩承膝，春子横抱且刀向右下',['躯干承重压稳、腿裙余摆收下','春子勉强承认而仍警觉'],'回应承接已经完成的抱起','抱姿持续，刀低垂右下']
shot('07_001',1)['motion_override']='Mixed：横抱前导在前置动作桥完成；本源镜middle锚点承接已成立的托肩承膝，不再次抱起或重复升高。'

# The proposed release cannot borrow a remote endpoint under the V3 adjacency
# gate. Preserve the supported return state as an explicit temporal ellipsis.
amend('20_002','横抱与交臂之间隔着长段介绍、独立插叙和受制现场。07_001与20_002不是相邻可生成端点，撤回放下动作桥，按有目的时间省略处理；返回青时以原图已有交臂正面站态冷启动，21_001明确两人并立。不声称实际放下时刻、路线或手部过程已拍出。',
    new_scene=True)
shot('20_002')['f'][1]='青的两条前臂交叉在胸下，两侧手指搭住对侧袖口附近。她的眉头向内收低，红眼在镜头前方集中，嘴唇逐渐压紧；吸入一口短气之后，肩部在交臂姿态里稳住，紧绷的判断停在脸上，双臂仍抱在胸下。'
shot('20_002')['plan']=['青已经交臂站着，正面看前方',['内眉收低，嘴唇压紧','短吸气后肩部稳住'],'从长段插景返回，青对描述保持警惕','交臂站着、正面注视']
shot('20_002')['motion_override']=panels['20_002']['review']
shot('20_002')['admissions_override']=[]

# 15_003 and the first overflow thought are one uninterrupted threat.
panels['16_001']['new_scene']=False
revisions.append({'image':'第20話_16_001.jpg','decision':'15_003冷笑确认支配6秒接16_001第一完整命令9秒，合为15秒片段；16_001本身42秒自然超限，保留其五个稳定语义段，头段可与前一完整单元同片，未加速或减戏。'})
plans16=[
 ['黑灰底场已铺满，上缘柔亮',['命令在灰带缓缓收窄中完成','两句间保留明确短顿'],'继承欧迈及冷笑后的支配话语，图形只承载命令，不呈现其所要求的行为','上灰下黑底场稳定'],
 ['青梅女闭眼受制，董白半垂眼，两头相近',['青梅女随第一内心声收紧眼角','董白在后一内心声压低眼皮，头位保持'],'两人的反感各有时点，现有包围关系持续','青梅女眼闭，董白眼低，头位相近'],
 ['黑面及窄灰带已铺满',['第一规则下灰带缓缓减亮','致死威胁后保留0.4秒暗度落点'],'规则用暗场完成，紧接受制局部，未添加实际伤害','厚黑面与低亮窄灰带'],
 ['巨指维持圈拢，三段指节横列',['内心声下维持指间紧窄关系','随既有呼吸皮褶轻起伏，指间不再收窄'],'11秒局部承载受困者断续辨认；持续接触是该段压力，不另加挤压','指节圈拢、现有接触持续'],
 ['董白额角紧张、眼皮半垂',['前一画外内心声下保持注意','董白内心反抗时额角绷紧、头局部偏侧'],'先受困再反抗，用现有眼额局部承接而不发起挣脱','半垂眼、额角发紧、受制未解除']]
for i,plan in enumerate(plans16):
    s=shot('16_001',i); s['plan']=plan
    s['motion_override']='非露骨局部/图形改编的表演复查：'+plan[2]+'；'+('图形动势只在背景层，原图实体关系未扩写。' if i in [0,2] else '限定已有眼额或指节裁切，保留原有接触，时长随自然内心声安排。')


# Formal fields contain executable content, not negative evidence controls.
cleanup={'，不补额外器物':'','，不补岩壁或器物':'','，帽后没有新增实体构件':'',
 '，没有实体环境构件':'，下层为均匀暗面','，不抢前层轮廓':'',
 '反感的紧张继续':'受困的紧张继续'}
for s in drafts:
    for i,f in enumerate(s['f']):
        for a,b in cleanup.items(): f=f.replace(a,b)
        s['f'][i]=f

# Assign stable review identifiers before the clip packing/renumbering pass.
for pid in panels:
    for n,s in enumerate(s for s in drafts if s['id']==pid):
        s.setdefault('review_key',pid+('-source' if not s.get('uncited') else '-coverage-'+str(n)))
for name,rows in files.items(): write(ROOT/'batches'/name,rows)
spec=importlib.util.spec_from_file_location('saved_authoring',ROOT/'authoring-tools.py')
author=importlib.util.module_from_spec(spec); spec.loader.exec_module(author); author.render()
current=ROOT.parent.parent/'current/第20话_制作分镜_Gen2.8.md'
ledger=read(ROOT/'source-ledger-v3.json')
baseline=read(BASE/'source-ledger-v3.json')
by_image={p['image']:p for p in ledger['panels']}

# Generated clip order follows complete contiguous panel units; reconcile metadata.
ordered=[]
for pid in panels: ordered += [s for s in drafts if s['id']==pid]
assert len(ordered)==len(ledger['shots'])
performance={r['target']:r for r in ledger['performance']}
key_to_target={}
for s,row in zip(ordered,ledger['shots']):
    pid=s['id']; image='第20話_'+pid+'.jpg'; p=panels[pid]
    assert row.get('source_images')==([] if s.get('uncited') else [image])
    key_to_target[s['review_key']]=row['target']; row['review_key']=s['review_key']
    row['motion_decision']=s.get('motion_override',p['motion'])
    if s.get('uncited') and 'G' not in row['risk_flags']: row['risk_flags']=row['risk_flags']+['G']
    if s.get('evidence_images_override'): row['evidence_images']=s['evidence_images_override']
    if s.get('admissions_override') is not None:
        row['action_admissions']=[dict(a,source_image=a.get('source_image',image),visible_in_framing=True,anchor_safe=True) for a in s['admissions_override']]
    if s.get('background_override'): row['background_decision']=s['background_override']
    plan=s.get('plan',p['plan']); row['camera_decision']['opening']=plan[0]; row['camera_decision']['landing']=plan[3]
    row['camera_decision']['anchor_phase']='contact' if s['review_key']=='07_001-formation' else 'middle'
    row['source_audit']='pass'; row['reviewed_action_excerpt']=s['f'][1]
    if row['target'] in performance:
        entry=performance[row['target']]; entry['card']={'opening':plan[0],'beats':plan[1],'coupling':plan[2],'landing':plan[3]}
        entry['details']=[s['f'][1]]; entry['evidence']=row['motion_decision']
    if s['review_key']=='07_001-formation':
        row['risk_basis']=row['motion_decision']
        # Silent bridges have the same staged review as speaking shots.
        if row['target'] not in performance:
            entry={'target':row['target'],'evidence':row['motion_decision'],
              'card':{'opening':plan[0],'beats':plan[1],'coupling':plan[2],'landing':plan[3]},
              'details':[s['f'][1]],'intervals':[{'speech_seconds':0,'acting_seconds':s['sec'],'concurrent':True}]}
            ledger['performance'].append(entry); performance[row['target']]=entry
        if 'P' not in row['risk_flags']: row['risk_flags'].append('P')

ledger['revision_audit']=baseline.get('revision_audit',[])+[{
 'date':'2026-10-11','scope':'第二十话最终动作/实际切点复查；按用户最新指示暂停第16—19话场景对照；战斗模块关闭。',
 'baseline':str(BASE.resolve()),'decisions':revisions,
 'anatomy_correction':'10_002/11_001/11_002/11_003巨大脚掌误读撤回，按手掌/指端/前臂修正，原证据保留于归档。',
 'deferred':'跨话场景色彩/光向复核暂缓，保留已保存场景基准，不声称本轮已重查。'}]
ledger['final_audit']['prior_audit']=baseline['final_audit']
ledger['final_audit']['semantic_review']=[{
 'target':row['target'],'review_key':s['review_key'],'image':'第20話_'+s['id']+'.jpg',
 'decision':s.get('motion_override',panels[s['id']]['review']),
 'time_course':s.get('plan',panels[s['id']]['plan'])[1],
 'interaction':s.get('plan',panels[s['id']]['plan'])[2],
 'opening':s.get('plan',panels[s['id']]['plan'])[0],
 'landing':s.get('plan',panels[s['id']]['plan'])[3],
 'seconds':s['sec'],'action_excerpt':s['f'][1],
 'review_scope':'changed_image' if any(r.get('image')=='第20話_'+s['id']+'.jpg' for r in revisions) else 'retained_image_approved_batch_and_final_text_review'
 } for s,row in zip(ordered,ledger['shots'])]
ledger['final_audit']['scope']='全稿动作时序、每个实际切点、冷启动与覆盖回接复查；改变动作/裁切/背景的源图专项复看，未改变的已审源批次复用。'
ledger['final_audit']['unresolved_action_gaps']=[]
ledger['final_audit']['combat_module']='disabled'
ledger['final_audit']['deferred_cross_episode_scene_review']=True
ledger['final_audit']['execution_reference_role']='漫画图仅作中段/接触/结果锚点，不绑定首帧；本轮未调用视频生成工具。'
ledger['final_audit']['manual_overflow']=[]
ledger['final_audit']['bridge_targets']=[key_to_target['07_001-formation']]
ledger['final_audit']['intentional_ellipses']=[{'incoming':key_to_target['20_002-source'],'decision':panels['20_002']['review']}]
write(ROOT/'source-ledger-v3.json',ledger)
write(ROOT/'action-review-changes.json',{'baseline':str(BASE.resolve()),'revisions':revisions,'bridge_targets':ledger['final_audit']['bridge_targets'],'key_to_target':key_to_target})
print('Final pass: '+str(len(ledger['shots']))+' shots; '+str(len(revisions))+' revision decisions; bridges '+', '.join(ledger['final_audit']['bridge_targets']))
