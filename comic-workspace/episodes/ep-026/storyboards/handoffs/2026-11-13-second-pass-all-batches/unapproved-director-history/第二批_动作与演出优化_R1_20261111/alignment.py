import copy
from authoring import proposal_digest
from validate_director import make_source_lock
from director_plan import CLIPS
REVIEWED=[s['source'].replace('第27話_','').replace('.jpg','') for c in CLIPS for s in c['shots'] if s['source']]
QUOTE='4是两手同时抓握。5摔倒地上之后要有烟尘爆炸效果，遮盖武士身躯和画面。其他无误，请优化第二批脚本。'
def apply_alignment(d,old):
 before=copy.deepcopy(d['source_lock']);route=d['action_routes'][0]
 route['path']='''第27话17_001—26_003，25原文件、26视觉节点，含20_001a/b。
1. 保留原作转场与此前交手的时间省略，不补一个未经明确展示的开头招式。青在同一石铺地面喘息，观察烟尘、怀疑陷阱、开口试探。
2. 武士从烟尘跃到青近上方，粗臂擦胸而过未击中。青后仰险避，双手迎向同一来臂。
3. 青两手同时抓握来臂末端；从闭合到承重、转体、带过头顶、身体前折、向下抡摔，双手持续抓牢，不先一手抓再补另一手。起抡站姿、接地前巨体轮廓与原作裂地节点保留。
4. 武士砸实石地、石板放射状裂开；接地后才有烟尘爆炸，从撞击点扩张，迅速吞没武士身躯并遮满画面。碰实前不以烟抹去抡摔和接地，厚尘持续到下一段。
5. 青摔后才松开双手、后撤，嫌恶对方湿软黏触感；回骂后心里觉得比持刀时好对付，内心不被听见。武士随后在这次抡摔新撞点的烟尘中撑起。
6. 武士头肩颤动蓄势，青觉得眼熟，身体前端喷出同一股白色液流。青扭身让开，身体和衣物完全没有接触喷流；喷流越过原站位落到石地，未增新伤或新裂地。
7. 青愤怒回骂后被落点动静吸引；白团鼓动、爆散后，白色有尾小体群完整显出并搜寻，最后青双手抱头惊叫。本批止于反应。
导演细化仅围绕已确认事件的接触、脚步、取景、余势、烟尘与液体接续；不新增独立交锋。身体受力、石体破坏、烟尘由快到慢错层，夜晚与青尚未强化状态保持。'''
 route['user_confirmation']={'quote':'先前确认：19003擦着青的胸部过去，没有击中青，24004没有碰到青，被躲过去了，其他没问题。\n本轮确认：'+QUOTE,'scope':'用户确认九段动作理解并明确修正双手同时抓握和摔后烟尘遮体满画。'}
 route['user_confirmation']['sha256']=proposal_digest(route,'path');route['proposal_sha256']=route['user_confirmation']['sha256'];route['confirmation_status']='user_explained_corrected_path';route['performance_mode']='action'
 for p in d['panels']:
  if p['image']=='第27話_20_001a.jpg':
   p['node_state']={'青.接触':'两手同时扣住同一来臂末端','武士.阶段':'来臂掠过后被抓握'}
   p['action_reading'].update(summary='用户明确两手同时抓握；近侧手清楚、另一手在对侧，同拍完成闭合。',world_motion='两手同时扣紧同一腕臂，持续抓握直至抡摔撞实。',basis='2026-11-11用户明确纠正，原格近手与接触位置复看。')
  if p['image']=='第27話_20_001b.jpg':
   p['node_state'].update({'青.接触':'双手持续抓住同一腕臂','青.阶段':'将武士带过头顶'})
   p['action_reading'].update(summary='保留双手举臂、前屈后直站位和巨体横过头顶；起抡前双手已经同时扣牢，后续保持同一抓握，脚步承重为导演连续补全。',world_motion='双手持续抓住同一腕臂，将巨大武士带过头顶，脚步与髋肩向下抡方向连续转移。',basis='2026-11-11用户明确双手同时抓握；本轮原格复看，删除先后补手的旧解释。')
  if p['image']=='第27話_22_001.jpg':
   p['action_reading'].update(summary='先读清武士接地和原作放射裂石；用户要求接地后烟尘爆起吞没武士并遮满画面，后续尘幕为新增演出。',world_motion='抡摔撞实、石体裂开，再由同一接地点爆起厚尘。')
 d['source_lock']=make_source_lock(d)
 d['source_revision']={'date':'2026-11-11','old_lock':before,'new_lock':d['source_lock'],'reason':'用户修正两手同时抓握，并明确授权接地后烟尘吞体遮画，更新动作解释重新冻结。','reviewed_this_turn':REVIEWED,'user_quote':QUOTE,'immutable_dialogue':'22条ID/来源原文/日文/归属/类型及26节点顺序不变。'}
 d['initial_state'].update({'场景':'同一石铺地面C、残墙与厚尘区','武士.位置':'青左后厚尘中、尚未现身','青.位置':'尘区右近石地','青.强化光':'未启动'})
 return d
