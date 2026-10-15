#!/usr/bin/env python3
"""Build the Gen2.7 compressed-rule/full-output comparison fixture."""

from __future__ import annotations

import copy
import json
import re

import build_ch15_gen26_first8_cinematic as base

OUT = base.ROOT / "tests/results/gen2.7/ch15-first8"
WORKSPACE_OUT = base.ROOT / "comic-workspace/episodes/ep-015/storyboards/gen2.7/part1-p001-p008"
line, shot = base.line, base.shot
YOUNG, COOL, DWARF = base.YOUNG, base.COOL, base.DWARF


opening = shot(1, 1, 3, "ch15_p01_c001.jpg",
    "层叠灰白云团占据中央天空，深色树冠从左侧、左下与右下边缘围出仰视开口。",
    "高处风声宽阔铺开，树冠叶声从画面下缘稀疏上浮。",
    "28mm垂直仰视全景，树冠构成不对称框景；固定机位把视线压向云隙亮区与标题中心。",
    "云团在高空缓慢改形，中央亮区从薄云后透出；边缘树叶错拍轻摆，最后云隙与标题共同稳定在画面中轴。",
    "云后日光形成大面积柔亮天光，云层具有冷灰体积和暖白透亮边；树冠压成深色剪影，云隙只保留克制柔光晕。",
    "声音设计：风声先行，树叶晚半拍响应；标题落幅处收窄高频并留半拍静默。")

raised_hand = shot(2, 1, 3, "ch15_p02_c001.jpg",
    "摊开的右手从画面右侧占据主体，灰云天空铺在掌后，深色树冠沿左下边缘围住手腕。",
    "林上风声由右后方进入，袖口与手腕移动产生近距离布料轻擦。",
    "85mm手掌近景，低机位沿掌心方向仰拍；焦平面锁住掌纹与五指，手腕斜线把视线引向画面上方。",
    "右手已经高举、五指张开；食指与中指先向掌心收拢半程，其余手指随后蓄力，腕部轻内扣，袖口滞后摆回，落点停在下压前的绷紧掌形。",
    "阴天漫射光均匀铺过掌心，指缝与腕根形成柔暗层次；云隙反光在手指外缘勾出细窄轮廓。",
    "声音设计：指节收拢伴随极轻皮肤摩擦，袖口回摆后环境声短暂抽空，为下落动作蓄势。")

confrontation = shot(3, 1, 6, "ch15_p03_c001.jpg",
    "青趴在带裂纹的碎石路上占据右前景，春子从左后方俯身压入画面；两人之间露出灰云、深色树冠与狭窄路面。",
    "近处碎石摩擦和衣料窸窣贴地展开，远处林风从两人之间穿过。",
    "35mm贴地双人中近景，青的大头部前景与春子的侧脸后景形成强纵深；镜头极缓向右横移并保留上下压迫关系，句末在两人对视轴线上稳住。",
    "春子以三分之二侧脸俯视青，眼睑先压低、下巴随后前探；青双肘撑地，先从地面抬起眼睛，再把脸转向画面左后方，嘴巴由错愕张开转为反问，肩线因疼痛向内缩。句末两人的目光都停在对方脸上。",
    "阴云提供冷柔顶光，碎石反射暖灰低位补光；春子背侧发丝有一线云隙轮廓，青泛红面颊和泪光保持局部高光。",
    "声音设计：春子的短句之间留冷静停顿；青抬脸时肘部擦过碎石，反问前急吸气，尾字伴随肩膀回缩。",
    [line("春子", "你居然敢对我说谎。", "よくも私に嘘をつきましたね。", 2.4, COOL), line("青", "什么啊？！为什么要打我？！", "何ですか?! どうして叩くんですか?!", 2.5, YOUNG)], details=["眼睑先压低", "先从地面抬起眼睛", "肩线因疼痛向内缩"])

ground_face = shot(3, 2, 6, "ch15_p03_c002.jpg",
    "青的脸颊和白发铺在带细裂纹的碎石地面上，紧闭双眼与泪滴占据前景；春子的膝部、衣摆和一缕头发从右上后景压入。",
    "贴地风声掠过发丝，衣摆与碎石分别位于右后方和画面下方。",
    "100mm贴地脸部特写，焦平面锁在青的眼睑、泪滴和抿住的嘴唇；后景春子压成柔化遮挡，镜头只作极慢前推，句末在眼睑与贴地嘴角处稳住。",
    "青以右脸贴地、双眼紧闭，春子的问句落下时右侧眼睑先颤、眉心随后收紧；她吸气，嘴唇从抿紧到微开，泪滴沿眼角滑到面颊，回答后下巴失去力气重新压实地面，发梢迟半拍摊回碎石。",
    "暖灰地面反光托亮白发和下颌，春子后景衣料形成深色遮挡；眼角泪滴、唇缘与贴地发丝获得细小冷白高光。",
    "声音设计：春子画外问句近而平直；青吸气带轻微哽咽，脸颊重新贴地时出现柔闷摩擦，句末只剩贴地风声。",
    [line("春子", "知道错了吗？", "反省しましたか？", 1.3, COOL), line("青", "呜呜……至少告诉我为什么要打我屁股……", "うううっ……せめて、どうしてお尻を叩いたのか教えてください……", 3.8, YOUNG)], details=["右侧眼睑先颤", "泪滴沿眼角滑到面颊", "下巴失去力气重新压实地面"])

dizzy = shot(4, 3, 4, "ch15_p04_c003.jpg",
    "青的正面胸像填满画面，背景为上深下浅的灰色渐变，螺旋瞳孔、脸颊斜线与汗滴构成抽象眩晕画面。",
    "现实脚步和林风被压成遥远低声，近处只保留浅呼吸与轻微耳鸣。",
    "85mm正面中近景固定机位，完全对称构图锁住双眼；景深压平，灰色渐变只提供图形层次。",
    "青的脸保持正对镜头，螺旋瞳孔缓慢转动；左眼先迟钝眨一下，嘴角勉强上扬后立刻僵住，两侧汗滴沿面颊下移，肩膀随浅吐气再沉一点，最后视线仍失焦停在镜头前。",
    "均匀柔光保持脸部高可读度，发丝外缘有薄冷灰轮廓；背景由深灰压向浅灰，眼睛和汗滴保留锐利高光。",
    "声音设计：低频耳鸣随螺旋瞳孔进入，浅呼吸贴近中央；嘴角僵住时环境声短暂恢复又退远。")

crystal_explanation = shot(6, 1, 9, "ch15_p05_c002.jpg",
    "青蓝透明晶石连着深蓝灰粗糙底座，悬在由深灰过渡到冷白的星屑图形背景中央；人物与手均未入画。",
    "林道风声被抽象空间压远，晶体附近保留细小清脆共鸣和稀疏高频闪点。",
    "100mm物件特写，晶石略向右倾；固定构图中先锁内部星屑，再沿棱面缓慢拉焦到粗糙底座，后半句极轻推近并在晶石与底座连接处落幅。",
    "晶石保持同一朝向，内部冷白亮点从暗面向中央逐层显现；青的画外疑问结束后停顿半拍。矮人说到「処女」时一条亮棱突然增强，改口「特定の資質」后亮度转为均匀，最后细碎光点沿棱线缓慢衰减，落点停在晶石与底座连接处。",
    "冷白背光穿过半透明晶体形成蓝灰折射；底座吸光而粗粝，星屑只照亮附近小范围，画面边缘保持深灰颗粒与清晰暗角。",
    "声音设计：青的画外疑问保持近景位置；矮人在「処女」后短暂停顿并清嗓改口，晶体共鸣随最亮棱线升起，句末缓慢消失。",
    [line("青", "话说回来，怎么可能存在这种东西？", "話を戻しますけど、どうしてこんなものが存在するんですか？", 3.0, YOUNG), line("矮人", "一块只有处……我是说只有具备特定特质的人才能触摸的石头。", "処女だけが……いや、特定の資質を持つ者だけが触れられる石だ。", 4.3, DWARF)], details=["内部冷白亮点从暗面向中央逐层显现", "改口「特定の資質」后亮度转为均匀", "细碎光点沿棱线缓慢衰减"])

dwarf_offer = shot(7, 1, 4, "ch15_p05_c003.jpg",
    "矮人的头盔、半垂眼睛与浓密黑胡须占满中近景，灰云与浅亮天空只从轮廓外侧露出；画面没有晶石和手。",
    "林风从后方低声经过，胡须与衣领产生细小近距摩擦；青的回答位于画面右侧外。",
    "85mm矮人脸部近景，平视固定机位，焦平面锁住头盔下的双眼和胡须上缘；右侧留出画外回答空间。",
    "矮人的脸以三分之二角度朝画面右侧，眼睛先向右偏移，左侧眉峰略抬，胡须随短问句轻动；听到青立刻拒绝后，瞳孔停住半拍，下巴向内收一点，胡须迟缓回落，结束时仍看向右侧画外。",
    "云层漫射光从右前方照亮鼻梁和头盔铆钉，眼窝与胡须保持深暗；头盔边缘有冷白轮廓，脸颊得到微弱暖灰补光。",
    "声音设计：矮人问句低沉而直接，尾音保留半拍；青的「いりません」从右侧画外突然切入，矮人鼻息在回答后轻短落下。",
    [line("矮人", "你想要？", "欲しいか？", 1.0, DWARF), line("青", "才不要！", "いりません!!!", 1.0, YOUNG)], details=["眼睛向右偏移", "下巴向内收", "胡须迟缓回落"])

crystal_in_palm = shot(10, 1, 6, "ch15_p06_c003.jpg",
    "一只戴袖口的手掌从左侧托住青蓝晶石，晶体与粗糙底座占据中央，白色留白背景和黑色冲击线填满四周；画面只显示这一只手。",
    "远处林风被极近景压低，晶体落在掌心的轻响居中，袖口摩擦位于左下。",
    "100mm斜俯视手部极近景，焦平面锁住掌纹、晶石底座和透明棱面；镜头在承重瞬间短推，落幅停在掌根与底座接触线。",
    "晶石已经压入掌心；小指与无名指先收拢，中指随后贴近底座侧面，拇指停在棱面外侧确认重量。腕部因承重下沉少许，袖口褶皱向掌根集中，最后整只手稳定托住晶石。",
    "高键留白提供正面柔光，晶体内部星屑集中发亮，粗糙底座保持深蓝灰吸光面；侧逆光沿棱角形成冷亮边，掌心得到局部蓝色反射。",
    "声音设计：晶石触掌轻响后接袖口受力声；矮人画外解释平稳推进，手指收拢与「持つのが一番いい」同步，句末晶体共鸣变轻。",
    [line("矮人", "由一个能触摸它的人来持有它是再好不过了。", "触れられる者が持つのが一番いい。お前が持っていけ。", 3.8, DWARF)], details=["小指与无名指先收拢", "腕部因承重下沉少许", "最后整只手稳定托住晶石"])

dwarf_long = shot(12, 1, 8, "ch15_p07_c002.jpg",
    "矮人的头盔、半垂眼睛、鼻梁与浓密胡须占满竖幅，浅灰背景色块和白色留白围住轮廓；画面没有手和晶石。",
    "林风位于后方，胡须与衣领有近距细响，青的呼吸从画面右侧外隐约传来。",
    "100mm正面脸部特写，机位略低于眼线，焦平面锁在双眼和鼻梁；固定镜头以极轻前推承载长解释，胡须下缘作为稳定落幅。",
    "矮人正脸略朝画面右侧，开口前瞳孔先向右侧青的位置停住；「そう考えるな」时一侧眉峰抬高、眼睑放松，转入「使い手に条件」时下巴轻收，眼睛短暂落向画面右下；说到「強力な鉱物」时目光重新抬起、鼻翼轻张，胡须随重音振动，句末肩颈放松而视线仍留在右侧外。",
    "右上方云隙天光擦亮头盔铆钉、鼻梁和胡须外缘，左侧脸落入柔暗；浅色背景提供低位反射，眼瞳有克制高光，胡须内部保留丰富暗部。",
    "声音设计：低沉解释保持均匀气息，「そう考えるな」后停半拍；中段鼻息与下巴轻收同步，句末重音落下后胡须摩擦声延迟消失。",
    [line("矮人", "别这么想。即使它对使用者有要求，但它仍然是一种强大到令人难以置信的矿物。虽然这么小一块很难制作大型武器……", "そう考えるな。使い手に条件はあるが、それでも信じられないほど強力な鉱物だ。小さすぎて大きな武器にはできないが……", 6.7, DWARF)], details=["瞳孔先向右侧青的位置停住", "下巴轻收", "目光重新抬起"])

weapon_concept = shot(13, 1, 10, "ch15_p08_c001.jpg",
    "青蓝透明晶石悬在左侧，银蓝金属四孔指虎位于右侧；深灰颗粒渐变、冷白星点与两团柔亮光晕填满物件周围，人物和手均未入画。",
    "抽象低频空气声铺底，晶体清脆泛音位于左侧，金属短鸣位于右侧，远处林风保持极低音量。",
    "70mm说明性物件镜头，略高视角保持晶石与指虎完整并置；焦点从晶体内部沿冷白亮线横移到指虎四孔，后半段极缓推近并在两件物体的中心关系处落幅。",
    "两件物体保持既定位置。说到「戦い方」时晶体内部星点由下向上点亮；说到「ナックルダスター」时亮线横跨两者，指虎轮廓从暗部完整显现，四个指孔依次获得窄亮边。转入「鍛えられれば」后两团光晕轻微靠近，听到「強敵」时金属高光增强一次，最后所有亮点稳定在并置构图。",
    "晶石由冷白背光形成蓝灰折射和内部透亮层，底座吸光；指虎由右上硬边光勾出厚度，孔壁保留深暗。星点只在物件附近密集，光晕向深灰边缘快速衰减。",
    "声音设计：左侧晶体泛音先起，亮线横移时声像移向右侧并接金属短鸣；第二句重音使尾音加亮，结尾两种泛音同时衰减并留一拍静默。",
    [line("矮人", "对于你的战斗风格来说，像指虎这样的东西已经足够了。", "お前の戦い方なら、ナックルダスター程度で十分だ。", 3.8, DWARF), line("矮人", "如果你能打造出它，在你遇到强敌时它会很有作用。", "鍛えられれば、強敵と出会った時にきっと役に立つ。", 3.2, DWARF)], details=["晶体内部星点由下向上点亮", "四个指孔依次获得窄亮边", "所有亮点稳定在并置构图"])

offer = shot(9, 1, 2, "ch15_p06_c002.jpg",
    "白色留白承载对白，林间石路、低矮草丛与灰白天空组成两人交接的关系背景。",
    "林道风声居中，草叶窸窣从左右两侧传来。",
    "50mm平视双人中近景，焦点落在青与矮人之间的晶石位置，固定机位保留手部交接空间。",
    "矮人把晶石送到两人中间；青双手收在胸前，脸朝画面左侧，视线先落向晶石再抬向矮人，动作停在接触前。",
    "灰白天空作柔和背光，石路和草丛提供低位冷暖反射，晶石保持冷蓝亮点。",
    "声音设计：短句落下时衣袖轻响；青吸气后留半拍林风。",
    [line("矮人", "拿着吧。", "持っていけ。", 1.0, DWARF)], role="uncited_coverage", details=["视线先落向晶石再抬向矮人", "动作停在接触前"])

refusal = shot(11, 1, 5, "ch15_p07_c001.jpg",
    "青闭眼哭喊的正面上身占据右侧，矮人的汗湿侧脸压在左缘；双方前臂、张开的手掌与晶石围住下方交接区，浅灰渐变和弧形速度线填满人物之间。",
    "风声与衣摆拖动声居中，矮人的急促鼻息贴在左侧，林道声场退到远处。",
    "35mm双人中近景，轻微手持跟随青上身的后撤；焦点先锁住她紧闭的泪眼与张口，再落向双方手掌和晶石，句末在人物面部与交接区形成的三角关系处稳住。",
    "青双眼紧闭，泪珠挂在眼角，双手竖在胸前隔开晶石；第一声「いりません」时她的手腕向外推半掌，肩线随后向内缩。第二声拒绝前嘴唇短暂合拢换气，再张口喊出时头部连续摇动，长发和袖口晚半拍向反方向甩开后回弹；矮人侧脸绷紧、汗滴下移，手掌仍在下方承托晶石。最后青的双掌停在胸前与晶石之间，肩线绷紧，嘴唇回到半开急喘状态。",
    "浅灰高键图形光保持青的面部、双手与晶石可读；泪珠和晶石棱面各留一处冷白高光，袖口内侧与矮人眼窝压入受力暗部，弧形速度线沿后撤方向增强。",
    "声音设计：第一声拒绝带短促空间回响，手腕推出时衣袖绷紧；第二声与肩线后缩同步并迅速收干，摇头结束后只留下发丝回弹、晶石轻碰掌心和青的急促换气。",
    [line("青", "不要！不要！请拿回去！", "いやあああっ！ いりません、いりません！ 持って帰ってください！", 3.7, YOUNG)],
    details=["第一声「いりません」时她的手腕向外推半掌", "第二声拒绝前嘴唇短暂合拢换气", "长发和袖口晚半拍向反方向甩开后回弹"])

refusal_followup = shot(11, 2, 5, "ch15_p07_c001.jpg",
    "青的胸前衣料、竖起的双掌、矮人从下方伸入的承托手与青蓝晶石填满近景，浅灰弧形速度线在手臂外侧收束。",
    "风声从手臂间穿过，衣袖拉扯位于右侧，晶石底座与掌心摩擦贴近中央。",
    "85mm交叠手部与下半脸近景，焦点从晶石底座移到青的嘴唇和矮人的承托手；镜头随晶石下滑短推半步，矮人稳住重量后在腕部、晶石与她紧绷下唇构成的关系处落幅。",
    "晶石从青张开的指间下滑半掌，矮人的手掌立即从下方托住底座，掌根同时抵住她向外推的腕部；矮人的「気をつけろ」落下时青的手指本能收拢，却仍把掌心朝外。她的眼睑继续压紧，嘴唇先抿住吸气，说到「一度もデートしたことがない」时下唇向内收、右肩再缩一点，句末双手仍挡在胸前，晶石稳定在矮人的承托手上。",
    "低对比柔光集中在手指、腕部和晶体底座，晶石冷蓝反射只染亮邻近指缘；袖口褶皱和下唇保留细窄受力阴影，外围速度线降为浅灰。",
    "声音设计：晶石下滑先带出一声短促擦响，矮人的警告与托底动作同时落下；青吸气后把抱怨一口气推出，重音「一度もデートしたことがない」压紧衣袖摩擦，句末底座轻碰掌心后留半拍喘息。",
    [line("矮人", "小心！", "おい、気をつけろ！", 1.2, DWARF), line("青", "带着它不就等于被盖上从没约会过的烙印吗！", "これを持っていたら、一度もデートしたことがないって烙印を押されるじゃないですか！", 2.4, YOUNG)],
    role="uncited_coverage", details=["晶石从青张开的指间下滑半掌", "矮人的警告与托底动作同时落下", "下唇向内收、右肩再缩一点"])

final_question = dict(base.SHOTS[22])
final_question["environment"] = "白色留白背景和浅灰网点包围青的正面胸像，掌中晶石位于左下前景。"

question = dict(base.SHOTS[8])
question["camera"] = "50mm双人中景侧向跟拍，焦点从春子侧脸转到青的领口和眼神，句末在青的手指与回避侧脸之间稳住。"

# Keep already source-correct Gen2.6 shots, replace the panels whose earlier fixture
# had wrong backgrounds, dialogue ownership, hidden hands, or invented gestures.
SHOTS = [
    opening, raised_hand, base.SHOTS[2], confrontation, ground_face,
    base.SHOTS[5], base.SHOTS[6], dizzy,
    question, base.SHOTS[9], crystal_explanation, dwarf_offer,
    base.SHOTS[14], offer, crystal_in_palm,
    refusal, refusal_followup, dwarf_long, weapon_concept, final_question,
]


def merge_continuous_clips(shots: list[dict]) -> list[dict]:
    """Group adjacent beats into complete generated clips of at most 15 seconds."""
    clip_groups = (
        (1, 2),          # title sky -> raised hand -> impact (9s)
        (3,),            # confrontation -> grounded reply (12s)
        (4,),            # sky pause -> walk -> dizzy reaction (11s)
        (5,),            # question -> embarrassed answer (11s)
        (6,),            # crystal explanation (9s)
        (7, 8, 9, 10),  # offer/refusal -> retrieve -> present -> handoff (15s)
        (11,),           # emphatic refusal -> catch (10s)
        (12,),           # dwarf explanation (8s)
        (13, 14),        # weapon concept -> Qing follow-up question (14s)
    )
    source_by_clip: dict[int, list[dict]] = {}
    for item in shots:
        source_by_clip.setdefault(item["clip"], []).append(item)

    merged: list[dict] = []
    for new_clip, source_clips in enumerate(clip_groups, start=1):
        new_shot = 1
        for source_clip in source_clips:
            for item in source_by_clip[source_clip]:
                current = copy.deepcopy(item)
                current["clip"] = new_clip
                current["number"] = new_shot
                merged.append(current)
                new_shot += 1
    return merged


SHOTS = merge_continuous_clips(SHOTS)


def workspace_panel_name(name: str) -> str:
    match = re.fullmatch(r"ch15_p(\d+)_c(\d+)\.jpg", name)
    if not match:
        return name
    return f"第15话_{int(match.group(1)):03d}_{int(match.group(2)):03d}.jpg"


def workspace_source_id(source_id: str) -> str:
    """Convert stable panel/bubble ids to the comic-workspace naming scheme."""
    match = re.fullmatch(r"ch15_p(\d+)_c(\d+)(.*)", source_id)
    if not match:
        return source_id
    return (
        f"第15话_{int(match.group(1)):03d}_{int(match.group(2)):03d}"
        f"{match.group(3)}"
    )


def export_workspace_copy() -> None:
    """Export the test script with filenames matching comic-workspace source assets."""
    WORKSPACE_OUT.mkdir(parents=True, exist_ok=True)
    storyboard = (OUT / "storyboard.md").read_text(encoding="utf-8")
    storyboard = re.sub(
        r"ch15_p\d+_c\d+\.jpg",
        lambda match: workspace_panel_name(match.group(0)),
        storyboard,
    )
    (WORKSPACE_OUT / "storyboard.md").write_text(storyboard, encoding="utf-8")

    ledger = json.loads((OUT / "source-ledger.json").read_text(encoding="utf-8"))
    for panel in ledger["panels"]:
        panel["image"] = workspace_panel_name(panel["image"])
        if "id" in panel:
            panel["id"] = workspace_source_id(panel["id"])
        for bubble in panel.get("bubbles", []):
            if "id" in bubble:
                bubble["id"] = workspace_source_id(bubble["id"])
    for item in ledger["shots"]:
        item["source_images"] = [workspace_panel_name(name) for name in item["source_images"]]
        item["source_bubbles"] = [
            workspace_source_id(source_id) for source_id in item.get("source_bubbles", [])
        ]
    (WORKSPACE_OUT / "source-ledger.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    base.OUT = OUT
    base.SHOTS = SHOTS
    base.main()
    path = OUT / "storyboard.md"
    text = path.read_text(encoding="utf-8").replace(
        "# 第15话前八图｜Gen2.6电影化表演测试",
        "# 第15话前八图｜Gen2.7精简规则完整质量测试", 1)
    path.write_text(text, encoding="utf-8")
    export_workspace_copy()


if __name__ == "__main__":
    main()
