import copy, hashlib, importlib.util, json, pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[4]
TASK = pathlib.Path(__file__).resolve().parent
CURRENT = ROOT / 'comic-workspace/episodes/ep-019/storyboards/current/第19话_制作分镜_Gen2.8.md'
DELIVERY = ROOT / 'comic-workspace/episodes/ep-019/storyboards/deliveries/2026-10-11_Gen2.8_运镜视线三无修订'
SKILL_COMMIT = 'a77fe4c0045ce03f58ce0b1feb022e940868fbff'
parser_path = ROOT / 'tests/results/gen2.8/ep018-019-brow-revision/prepare_review.py'
spec = importlib.util.spec_from_file_location('review_parser', parser_path)
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)

# Plans authored after inspecting all current 720p evidence. One uninterrupted
# primary camera intention per shot; source anchoring occurs inside its path.
CAMERAS = {
1: '固定正投影全景，白色图形底场铺满画面，黑色尖锐笔触集中在左右下缘，中央保留宽留白。',
2: '固定正面略仰极特写，欧迈及的眉眼与鼻梁填满画面，左眼在左上，右眼裁在右缘，鼻梁位于中央偏右。',
3: '正面低机位仰拍，从欧迈及胸前两处圆形断端的近景向上摇约半个头高，前两秒纳入脸部，停在头部上方中央、两处断端位于左右胸前的上身近景；岩壁位于两侧后层。',
4: '固定正对岩壁的近景空镜，中央为密集凸石，上部深缝退入后层，下部雾气占窄边。',
5: '固定腰部高度的正向近景，董白握柄的手位于左上，缠布刀柄贴在腰侧，黑色短装与腿部从下缘裁切。',
6: '低机位仰拍双人局部，董白的腰腿占左前，欧迈及上身在右后。沿镜轴缓慢后拉约五分之一画宽，落在两层中景；董白头部位于上缘之外，两处圆端留在右后。',
7: '固定平视左向侧脸近景，欧迈及占右侧，眼口处于清晰焦面，鼻尖前的左侧留出窄幅岩壁。',
8: '正面低机位仰拍，起点为董白腰间握柄手的近景，向上摇并后拉至膝上中景；前半镜头完成，后半固定。脸落上中，双马尾分列两侧，刀柄留左下，岩壁为后层。',
9: '固定高机位俯拍青梅男盔面近景，盔顶和肩部上缘可见，三道横槽位于中央偏左，后层为岩壁。',
10: '固定正对洞窟岩壁的近景空镜，中央凸石占主要画面，上部暗缝深入后层，下部雾气留窄边。',
11: '手部近景，镜头随欧迈及前臂由左下向右上抬入而上摇约半个手掌高，手形收清时停在中央偏右；指尖全留画内，岩壁在后层。',
12: '肩部高度略俯拍欧迈及背面近景，从左下张手向右横移约四分之一画宽，停在张手占左下、后脑占上中的两层构图；背部横过下方。',
13: '正面低机位仰拍欧迈及脸部近景，沿轴短推约五分之一画宽，停在双眼、鼻底与张口同框的极近景；脸颊从两侧裁切，焦面覆盖眼口。',
14: '固定略俯手部近景，董白的手腕从右上斜向左下，露指手套位于左中，另一手扣住套口，碎石地面从右下露出。',
15: '正面略仰上身近景，董白位于中央，握柄手在左下前景。沿轴缓推至胸上近景，前半完成，后半停住；脸在上中，握柄手仍留左下，双马尾斜向两侧。',
16: '固定刀柄与鞘口接触特写，柄手在左上，握鞘手在右下，刀柄刀鞘沿左上至右下斜线相接，焦面覆盖双手与鞘口。',
17: '固定黑拳正向特写，拳头占中央偏左，白色锯齿能量包围右侧拳缘，图形底场铺满后层。',
18: '正面略俯拍董白拔刀，从鞘口近景沿刀身朝左上摇移并后拉，随抽刀一次完成，停在膝上中景。刀柄左上、鞘右侧，刀身斜贯胸前，脸与双手同框。',
19: '董白侧前方低机位仰拍中景，左下近手与鞘占前层，脸在上中，刀位于左上肩后。沿轴推进约六分之一画宽，停在胸上近景，脸、握鞘手与肩后刀保留三层。',
20: '平视诊所入口近景，从左侧牌匾向右横移约三分之一画宽，停在牌匾左边、木柱中央、垂直门帘右边的构图，木纹保持清晰。',
21: '肩部高度平视双人中近景，春子后脑占左前、青在右侧。随青回头向右短移约一个脸宽，落在春子左前遮挡与青右侧头肩同框的位置，冰袋和托袋双手留右下。',
22: '固定正面平视头肩近景，春子居中，半垂双眼与露出的单侧眉毛在清晰焦面，肿起的脸颊和深色罩衫上缘同框。',
23: '平视双人中近景，青在左、春子后脑在右前，青胸前的冰袋位于下中。随青靠近向右横移约半个肩宽，袋子送到脸侧时停住；两张脸的局部、托袋双手和袋脸之间的空隙留在同一焦面。',
24: '固定青持冰袋的手部近景，双手与透明袋身占中央，蓝色袖口沿两侧下缘裁切，右侧近层至胸前的回收路径留在画内。',
25: '固定正对岩壁的近景空镜，中央凸石与上部暗缝分层，下部薄雾占窄幅。',
26: '背面高机位略俯拍，从青和春子的肩背中景缓慢后拉约四分之一画宽，停在青左侧较高、春子右侧较低的坐姿中全景；木凳在下层，床面中后，岩壁最远。',
27: '正面高机位略俯拍双人头肩近景，春子在左、青在右。向右缓移约半个脸宽，青占右侧主位，春子的脸留在左边完整可见；两人面部处于同一焦面，抽象底场低细节。',
28: '平视青的左向侧脸，从胸上近景沿轴推进约五分之一画宽，停在头肩近景；脸占右侧，鼻尖前的左侧保留宽留白，尖耳留在右缘内。',
29: '固定平视春子的左向侧脸头肩近景，半垂眼与贴带位于清晰焦面，青的白发和肩部局部在右前形成窄遮挡。',
30: '肩部高度略俯拍双人侧背中近景，青左前、春子右前背面。随青转肩向左横移约半个脸宽后停住，冰袋与近手落下中，两人之间露出石地。',
31: '固定略俯单手持袋近景，青的近侧袖口从左下裁入，捏袋口的手在中央，透明袋身和冰块向右下展开；石地为低细节后层。',
32: '正面偏侧略仰拍青，镜头随她抬头向上摇约四分之一头高后停在头肩近景，脸位于中央偏右，长白发与肩部留在下方，岩壁在左后。',
33: '固定正面平视春子头肩近景，脸在中央偏左，贴带和半垂双眼清晰，岩壁从左后窄边露出。',
34: '固定正对诊所外岩壁的近景空镜，凸石在左中，上部深缝退入后层，浅雾横过下缘。',
35: '地面附近低机位略俯脚部近景，随黑靴落脚向右短移约半个鞋长，鞋底接地时停住；鞋尖向右，黑袍下摆从上缘裁切，石地铺满下方。',
36: '高机位明显俯拍诊所双人，从领旁手和凳面向上摇约半个头高，停在青右前仰脸、春子左后坐着的中近景；凳面和石地在下方，两人面部清晰。',
37: '从青坐姿后肩附近的低机位仰拍黑袍来者，沿轴推进约六分之一画宽，落在来者中全景与青左下后脑同框的两层构图；圆扣清晰，帽口全暗。',
38: '固定正面略仰双人局部中近景，青在右侧回头，左侧条板状物与黑色横带占近层，另一人物只见局部头发；回忆灰白底场低细节。',
39: '平视回忆中黑袍商人的左向侧面，沿轴由头肩近景缓推至兜帽与领扣近景，近手仍在帽口左边；帽内面罩轮廓留在阴影中，背景降低细节。',
40: '平视青的右向侧面，从右下举起的手指向上摇约半个头高，停在脸占左侧、食指留右下的头肩近景；鼻尖朝右，右侧留宽抽象底场。',
41: '高机位略俯拍诊所双人，从左后春子头肩向右横移约半个肩宽，停在春子坐于左后、青上身位于右前的中景；青双手留在两边画缘，面部处于同一焦面。',
42: '固定平视诊所旁物件近景，木栏横在右前，床沿和垂下的床单占左下，岩壁退入后层。',
43: '固定正面平视春子面部近景，双眼与露出的眉毛处于清晰焦面，嘴和脸侧贴带留在下方；头部填满中央，后层低细节。',
44: '诊所双人全景，黑袍来者背面在左、青在右。随青起身上摇并后拉，站稳时落在略俯双人全景；腿脚完整，左侧帘床、右側木栏和远处岩壁同框。',
45: '固定平视黑袍来者的左向兜帽头肩近景，兜帽占右侧，帽口全暗，左侧留出岩壁与浅雾。',
46: '平视青的右向侧脸，沿轴短推约六分之一画宽至头肩近景后停住；脸占左侧，鼻前右方保留岩壁，尖耳留在左缘内。',
47: '肩高平视黑袍来者的背侧头肩近景，随他转头向左小幅摇约四分之一帽宽，停在帽口朝左、肩袍占下方的背侧构图；岩壁在上后窄边。',
48: '胸部高度略仰拍双人中近景，青侧脸在左前、黑袍背面在右后。随来者起步向右横移约半个肩宽，停在青留左边、来者位于右后边的两层构图，岩壁为后层。',
49: '固定正面平视春子眉眼与下半脸近景，露出的单侧眉毛和双眼清晰，青的白发局部占右前窄边，灰紫底场保持低细节。',
50: '固定正对洞窟入口的全景空镜，岩壁占后方，地面从前层向岩脚收拢，上部暗缝深入，地面细节略简化。',
51: '低机位仰拍双人，从胸上近景沿轴后拉约五分之一画宽，停在春子左前较大、青右后较小的半身中景；洞顶岩面在上方，两人的脸处于清晰焦面。',
52: '背面略俯全景，黑袍来者站在中央远处岩壁前，前层留宽地面。沿镜轴持续缓推约四分之一画宽，最后一秒停在来者双脚完整、岩脚薄雾与宽地面仍可见的全景。',
53: '平视黑袍来者的侧面上身近景，从袖口随抬臂向左上摇约半个手长，停在兜帽右上、伸出的手在左中的构图；岩壁位于手后。',
54: '固定侧向手指极近景，黑手从右向左伸，拇指与中指位于中央，上方两指分开；岩壁在左边，指尖前留灰亮窄隙，焦点落指间。',
55: '侧后方略俯拍爆光场，左后为黑袍小剪影、右前为青。白光展开时短后拉并向青前臂摇约半个脸宽，停在倾斜双层中景；白光占左中，青的头肩和挡脸前臂留右前，石地斜贯下缘。',
56: '固定正面偏侧略俯拍青的头肩近景，头顶位于上缘内，挡脸前臂与手横过下方近层，眼口处于清晰焦面；岩壁在左后，白光余亮在右后。',
57: '从黑袍来者后肩附近略仰拍，起点为背侧上身与圆门中心，向上摇并后拉约三分之一画宽，停在整座圆形光门和下中来者背侧同框的中全景；岩壁分列两侧，圆门外沿全留画内。',
58: '固定平视青的左向侧脸头肩近景，脸在画面右侧，鼻前左方留岩壁和通道余光，脸侧汗点清晰。',
59: '固定平视春子右向侧面眉眼极近景，耳在左，完整的近侧眉毛在上部，半垂眼占中央偏右，鼻尖裁在右缘，嘴位于下缘之外。',
60: '镜头压至春子前俯头部稍上方，斜俯拍前冲中近景；沿冲刺轴线快速后退约半个身位，先跟上速度再等速，停在手指掠水时的构图。脸在上中、近手在左下，细刃斜贯左缘，水面下方、岩壁后层。',
61: '固定水面附近低机位、略俯脚部接触近景，春子的露趾凉鞋居中、鞋尖向左，脚踝从上缘裁切；鞋底与涟漪同在清晰焦面。',
62: '高机位俯拍黑袍来者肩背近景与水面，向右短摇约四分之一画宽，水花腾起时停在来者后脑左前、水花右后的构图；水面层次保持清晰。',
63: '正面偏侧低机位仰拍黑袍来者头肩近景，随头部朝右转向上摇约四分之一帽高后停住；来者在下方中央偏左，上方留宽灰白底场，帽口全暗。',
64: '从黑袍来者后方低机位强仰拍，沿春子跃起的方向向上摇，峰值处停在来者兜帽下前、春子卷身举刃上后的纵向双人中全景；刀尖留上缘内，水花占两侧。',
65: '刀身竖向极近景，沿刀刃向下快速摇约半个画高，停在前端窄刃占中央的构图；亮灰刃边在左、窄黑面在右，速度底场沿两侧铺开。',
66: '固定侧向刀尖与兜帽布边极近景，灰色兜帽占左，刀尖自右前抵近，中央窄隙和水珠处于同一清晰焦面。',
67: '后侧高机位俯拍双人全景，春子在上层、黑袍躯干斜贯下层，水面铺在右后方。随两人下降向下跟移约半个身高，腿部落位时停住；两人的下降、屈腿两侧、握刀手与兜帽边缘同框。',
68: '后侧高机位略俯拍压制，从双人中全景沿轴缓推约六分之一画宽，停在春子背面屈腿压制的中景；黑袍在下方，刀柄竖在右侧，水纹在右后。',
69: '高机位俯拍水面，从右后跑来的青向左短摇跟随约四分之一画宽，步伐收短时停在青右中、春子后脑左前的两层中景；青全身与脚下水花留在画内。',
70: '固定正面略俯拍青头肩近景，脸位于中央、稍向右倾，两侧白发与左下近手构成边框；双眼和两侧不对称眉线处于清晰焦面。',
71: '固定正面略俯拍春子头肩近景，露出的单侧眉头和半垂双眼清晰，口在下中，肩部从下缘裁切；灰色后层降低细节。',
72: '固定侧向刀尖与兜帽边缘极近景，帽布曲面占左，刀尖自右斜指左下，中央窄隙留在清晰焦面，后层为灰色水面与细白波纹。',
73: '固定正投影暗色图形全景，宽黑色中央铺满主要画面，上下边缘过渡到灰色。',
74: '固定正对岩壁的竖向近景空镜，岩壁占右侧，深缝退入后层，左侧雾气留出亮区，白雾沿下部石面铺开。',
75: '从董白背后低机位仰拍欧迈及，起点为董白右下握刀手与巨躯下部，向上摇并短后拉，前两秒落在董白左下全身、欧迈及巨躯中后同框的双人全景；黑脸白眼位于上中，岩壁白雾在后。',
76: '平视董白右向侧脸，从下巴旁握柄手向上摇约四分之一头高，停在脸居画面左侧、握柄手位于下中、刘海盖眼的头肩近景；柄向右伸，脸侧汗点清晰。',
77: '从青梅男右前肩后平视略俯拍，沿轴缓慢后拉约六分之一画宽，停在三层全景：青梅男盔肩右前、董白左中全身、欧迈及中央后层巨躯；深景深保留三层，石地铺前、白雾在下。',
78: '固定青梅女正面偏侧略仰头脸近景，脸位于中央偏右，黑发束沿后侧垂下，下缘止于颈肩上缘，汗点与眼口处于清晰焦面。',
79: '正面略俯拍董白的双手与下半脸，从刀柄鞘口近景短后拉约六分之一画宽，停在左手握柄、右手握鞘与紧嘴同框的上身近景；眼部裁在上缘之外，两端回鞘再分开的全程留在画内。',
80: '正面略俯拍董白，从刀鞘与双手近景后拉约四分之一画宽，前半完成，停在腰上中景；脸位于上中、刀斜贯胸前、刀柄左上、刀鞘右下，双马尾分列两侧，岩壁与白雾为后层。',
}

# Decisive gaze is an observed pose. Temporal acts below are admitted designs,
# not observations; quiet face does not reduce whole-body action.
ACTS = {
2: '欧迈及半眯着眼，眉间褶纹绷着。冲击余响落下，他的眼睑短短停在原位，眉间褶纹随后稍松，脸上的反应迟于冲击。',
8: '董白的手停在腰侧刀柄旁，稍抬起脸，目光直视镜头，露出轻松的笑容。她带着好奇把两句问话说完，发尾随抬脸轻晃后落稳，握柄的手仍从容留在腰侧。',
13: '欧迈及的嘴角又扬起来，半眯的眼睛看向镜头，露舌的笑口带着冒犯感。他先叫住对方，再直接问出男友的事，问完仍等回答，口边细涎随下巴的微动向下拖长。',
15: '董白把整理手套的近手放回左下的缠布刀柄，手指扣住后，脸上的玩笑笑容也收起来。她目光直视镜头，先警告对方不该闯来，说到「それとも」时嘴角露出一点讥讽，握柄的手随之握实；两句说完，目光仍朝镜头。',
19: '董白侧过身把刀留在肩后，转头看向镜头，近手握鞘垂在左下。她轻轻打发刚才的问题，接着从容说出威胁，目光仍朝镜头；双马尾随侧身摆过后逐渐收住，刀和鞘分在两只手中。',
20: '入口保持安静，春子在画外问出一句。门帘下缘随空气轻轻一动，随后落稳。',
21: '青双手托着胸前冰袋，听到问话扭头，目光转向镜头方向，嘴角的笑还留着。她先吃惊地反问，接着急忙否认，袋口被捏紧一点，袋身仍在手心；春子的后脑留在左前，坐姿平稳。',
22: '春子正对镜头，半垂的双眼直视镜头，露出的单侧内眉头略高、眉尾较低。她平淡地把青还在笑的事实指出来，嘴唇随台词小幅开合；肿起的脸颊形状稳定，句末合口，目光和眉形留在原位。',
24: '青的双手托着冰袋，听到回应后，把袋子从右侧近处收回自己胸前。袋身回到中央，捏袋口的指节稍松，冰块轻碰在一起，袋子仍由双手拿着。',
26: '青坐在左侧，长长叹气，背部与肩头随呼气慢慢落下，长发下缘移过凳沿。右侧春子听到叹气，头部略偏向左侧，平淡地问了一句；她问完保持坐姿，青的肩头停在低处。',
27: '青的目光沉下来，先犹豫地承认弄丢通行证，说到「私のせい」时目光更低，肩头也跟着垂下。春子坐在左侧，半垂眼看向画面左侧外，露出的单侧眉头略高；她平静听着，头肩维持坐姿，青把自责说完整。',
29: '春子侧脸朝左，半垂眼看向画面左侧外，脸侧贴带留在原处。她面容平淡地说完黑色玩笑，随后问青能否哭出来；嘴唇随两句小幅开合，句间停顿只留给等回应，头肩和眉眼形态稳定。',
30: '青急得转过肩，近侧眉头压低，闭眼叫春子别说不吉利的话。托着冰袋的近手猛地收紧，袋面挤出皱褶，冰块向一侧挤动，袋身短促鼓起；春子的后脑朝向前方，坐姿平稳。青嘴张着，近侧眉头仍压低，冰袋攥在胸前。',
33: '春子把脸稍转正，半垂的双眼直视镜头，露出的单侧内眉头略高。她平淡地说清现在做不了什么，嘴唇小幅开合后合住；头肩留在原位，眉形与目光维持到句末。',
34: '岩壁保持安静，春子在画外把判断说完，薄雾缓缓移过下方，话后留一瞬平静。',
36: '青坐在右前，听到脚步抬起脸，睁圆眼看向上方的镜头，领旁的手停着，短短问了一声。春子坐在左后，半垂眼看向画面左前方，头部略转向脚步方向，上身维持坐姿。',
38: '回想中的青在右侧回头，熟悉的话让她睁圆眼，目光转向镜头方向。她短短反问，头肩停在回望的位置，像在把声音与以前见过的人对上；左侧条板物稳在近层。',
41: '春子坐在左后，脸转向前方，半垂眼看向镜头方向，露出的眉头略高。她平淡问这是谁，再直接问青是否喜欢这种人，句间停顿短。青在右前看向左上方的镜头，仍带着认出旧人的笑，举着的手停在脸旁，准备解释。',
43: '春子正面听着画外青的介绍，半垂的双眼直视镜头，露出的单侧内眉头略高、眉身弯曲。青说完，她平淡地应一声，嘴唇小幅开合后合住，头肩与目光留在原位。',
49: '春子正面半垂眼直视镜头，露出的单侧内眉头略高、眉尾较低，嘴唇轻合。画外青先问状况，句间停一拍后又问是不是骑士；春子始终平静听着，目光留在镜头，眉眼形态保持。',
51: '青在右后抬脸看向镜头方向，带着好奇问是不是藏着通道。春子在左前，半垂眼朝低处镜头，露出的单侧眉头略高，平淡地否定；她嘴唇小幅开合后合住，头肩仍保持站姿。',
52: '黑袍来者背向镜头站在岩壁前，双脚分开，袍料随呼吸轻轻起落。他停在原地，春子的内心判断与这段等待并行，背影一直留在中央。',
56: '白光减弱后，青慢慢睁开眼，挡脸的前臂降到身前，张开的手仍绷着。她睁圆眼看向镜头方向，震惊地张口，脸侧留一点汗，一时没有真的说出话。',
59: '春子侧脸朝右，露出的内眉头高、眉尾低，近侧眼睑斜压，目光朝画面右侧外。她简短说出否定，头部停在侧向位置，眉眼形态保持；嘴位于下缘之外。',
60: '春子身体前俯迅速冲出，压低头部，半垂的双眼看向前方镜头方向。近臂朝左下伸出，手指掠到水面，细波纹随触水扩开；长发向后扬，黑刃随身体带进左缘。她平直说清判断，手指随前冲离水，尾流稍晚收短，身体继续前送，脸部外显幅度低。',
68: '春子屈腿压在黑袍身体两侧，上身前俯，近手握刀柄竖下，刀尖停在兜帽边缘前。她面容平淡地让对方停住，再说清警告，握柄手的压力维持；长发落在背上，袍布和水纹逐渐平稳，压制姿势持续。',
70: '青跑近后收住步伐，喘着气问清状况，目光直视镜头。她的眼睛仍睁圆，画面左侧露出的眉头压低，另一侧眉线较平；左下近手刚抬起便停住，问题问完仍看镜头，不对称眉形留住。',
71: '春子上身前俯，半垂的双眼直视镜头，露出的单侧内眉头略高、眉尾较低。她平淡地把战争的现实与眼前魔法联系起来，嘴唇随解释小幅开合，句末反问自然落下；头肩维持压制时的朝向，目光与眉形保持。',
72: '刀尖的余颤渐渐减小，始终停在兜帽边缘前，窄隙保持。细白水纹逐渐减弱，春子在画外平淡说出结论，压制仍稳定。',
75: '欧迈及把黑色面孔慢慢俯低，白色双眼朝镜头方向看着，嘴部笑意拉出轻蔑。董白在左下屈身面对它，握刀的手始终稳着，双马尾随气流轻摆；欧迈及把蝼蚁的比喻说完，双方仍在原来的远近位置。',
80: '董白抬起脸，目光直视镜头，刀与鞘完全分开，细长刀身斜向右下。她短促呼气，双马尾的扬动慢慢收住，握刀手保持稳，眉头压低、嘴角绷紧；画外说明说完，她仍维持备战姿势。',
}
VOICE_NOTES = {
20: ['平淡、音量平稳，直接提问，句尾轻落。'],
22: ['平淡陈述，语调平直，按自然语速说完。'],
24: ['平淡、简短，音量和语调平稳。'],
26: ['青发愁，叹气拖长；春子平淡短问，音量与句尾平稳。'],
29: ['语调平直，黑色幽默由内容与青的反应形成；末句简短，句间稍停。'],
30: [None, '春子平淡短问，音量平稳。'],
31: ['平淡说明，后句自然反问，语调起伏小。'],
33: ['平淡、直接，自然语速，句尾平稳。'],
34: ['平淡地说明判断，辱称按整句自然语速带过。'],
41: ['平淡连续两问，句间短停，音量和语调平稳。'],
43: [None, '春子平淡应一声，音量平稳。'],
50: ['平淡地确认地点，自然语速，句尾平稳。'],
51: [None, '春子平淡、简短，直接否定。'],
52: ['无声的内心停顿。', '无声的内心判断，节奏平稳，疑问由内容呈现。'],
55: [None, '春子在画外平淡短问，语调起伏小，音量足以听清。'],
59: ['简短、平淡，音量平稳，嘴在画外。'],
60: ['行动中平淡说明判断，语调平直，语速清楚。'],
68: ['平淡、低外显；首句简短，后句匀速把警告说清，音量平稳。'],
71: ['平淡分析，语调平直，按自然语速说清反问。'],
72: ['平淡说出结论，语速清楚，句尾平稳。'],
}

PURPOSES = {
20:'诊所外场景先建立，春子的平淡提问引出青的否认。',
22:'春子低外显的事实陈述与青的笑形成反差，眉形仅保持源形。',
24:'平淡回应使青收回冰袋；同一袋子仍由青持有。',
26:'青的叹气引出春子任务性的询问，春子不继承青的烦恼。',
27:'青展开自责，春子平静倾听，以源眉形与朝向参与。',
29:'平直的黑色幽默与青的担忧形成反差，笑点由台词内容承担。',
30:'青转肩挤袋的争辩对照春子的平淡短问。',
31:'画外春子平淡陈述被盗事实，青的手随倾听缓力。',
33:'春子平淡说明当前无事可做，截停争论而不演成冷硬安慰。',
34:'春子平调完成判断，粗口保留语义而不表演鄙夷。',
36:'脚步让青仰脸辨认，春子仅转注意方向；高机位承接来者身高关系。',
41:'春子平淡两问与青认人后的活力形成反差。',
43:'春子平静听介绍并短应，镜頭持态承载完整交接。',
49:'青两次求证，春子沉默倾听；源眉形维持，身份不提前确认。',
50:'春子平静认出地点，以空景建立后续通道位置。',
51:'青猜通道，春子平淡否定；低机位保留两人近远关系。',
52:'来者站定的等待承载春子的内心判断，外显表演仍平淡。',
55:'同一次爆光使青护脸，春子画外平调短问，二人的反差保留。',
59:'春子平淡给出短否定，内眉头高是形态锚点，不解释成警觉情绪。',
60:'春子快速掠水前冲的身体任务与平淡面部、语气同时成立。',
68:'稳定压制与清晰警告形成行动力，春子语气平淡而不加怒相。',
71:'春子维持压制朝向，平静分析战争与魔法的关系。',
72:'刀尖留隙的稳定状态承载春子的平淡结论。',
}

LENS_FACTS = {
'04_002':'董白目光朝镜头方向', '05_003':'欧迈及眯眼内的瞳孔朝镜头方向',
'06_002':'董白目光朝镜头方向', '07_002':'董白侧身回头，目光朝镜头方向',
'08_003':'青回头，目光朝镜头方向', '08_004':'春子半垂眼，目光直视镜头',
'11_002':'春子半垂眼，目光直视镜头', '11_004':'青仰脸，目光朝上方镜头',
'12_002':'青回头，目光朝镜头方向', '13_003':'春子半垂眼朝镜头方向，青看向左上方镜头',
'14_001':'春子半垂眼，目光直视镜头', '15_003':'春子半垂眼，目光直视镜头',
'16_001':'下框春子半垂眼朝低处镜头，青目光朝镜头方向',
'18_002':'青睁大眼，目光朝镜头方向', '20_001':'春子压低头部，半垂眼朝前方镜头方向',
'23_002':'青目光朝镜头方向', '23_003':'春子半垂眼，目光直视镜头',
'25_001':'欧迈及黑脸中的白眼朝镜头方向', '26_003':'董白目光朝镜头方向',
}

OPENINGS = {
8:'董白腰侧握柄，正面略仰，准备抬脸，嘴角带笑。',
13:'欧迈及脸朝镜头方向，半眯眼，嘴角准备再扬起。',
15:'董白刚整理手套，近手在刀柄旁，目光朝镜头方向。',
19:'董白拔刀完成，两手分持刀与鞘，侧身准备转头看镜头。',
21:'青双手托着胸前冰袋，嘴角带笑，准备回头。',
22:'春子正面半垂眼直视镜头，单侧内眉头略高，肿脸形状稳定。',
26:'青左、春子右背面坐着，青准备叹气，春子头肩平稳。',
27:'青正面低垂眉眼，春子左侧半垂眼朝画外左，眉头保持略高。',
29:'春子左向侧脸，半垂眼看左，青白发在右前。',
33:'春子脸朝前方、半垂眼，头部从稍侧向转正。',
36:'青右前坐着，手在领旁；春子左后坐着，头肩平稳。',
38:'回忆中青位于右侧，准备回头，条板物位于左前。',
41:'春子左后坐着，青右前双手举在脸旁，笑容留着。',
43:'春子正面半垂眼直视镜头，单侧内眉头略高，听画外介绍。',
49:'春子正面半垂眼直视镜头，单侧内眉头略高、口轻合，青白发右前。',
51:'春子左前站着，青右后，二人面朝低处镜头。',
59:'春子右侧脸，露出的内眉头高、眉尾低，眼睑斜压，目光朝右侧外。',
60:'春子前俯准备冲出，手臂向前下方，细刃位于身体后侧。',
68:'春子屈腿压制已落稳，刀尖与兜帽边缘留隙。',
71:'春子保持压制时的前俯上身，半垂眼直视镜头，单侧内眉头略高。',
75:'董白左下屈身持刀，欧迈及中后巨躯，黑脸白眼朝前方镜头方向。',
80:'董白刀鞘已经分开，脸稍低，两只手分别握刀与鞘。',
}
LANDINGS = {
8:'董白略抬脸看镜头，笑容留着，腰侧握柄手稳定。',
13:'欧迈及眯眼看镜头，笑口露舌，口边细涎向下。',
15:'董白握实刀柄，目光朝镜头，嘴角的讥讽收住。',
19:'董白侧身转头看镜头，刀留肩后，近手鞘垂左下。',
21:'青回头看镜头方向，双手仍托胸前冰袋，嘴角残笑。',
22:'春子合口，半垂眼直视镜头，单侧内眉头略高。',
26:'青叹气后的肩头较低，春子稍朝左偏头，二人仍坐着。',
27:'青低垂目光，春子平静听完，半垂眼朝左侧外。',
29:'春子侧脸朝左、眉眼平稳，嘴合上等回应。',
33:'春子转正合口，半垂眼直视镜头，眉形维持。',
36:'青仰脸直視上方镜头，春子半垂眼朝左前方，坐姿稳定。',
38:'青回头看镜头方向，条板物留左前，短反问结束。',
41:'春子平静问完，青仍举着手带笑准备解释。',
43:'春子短应后合口，眼睛仍朝镜头，眉形维持。',
49:'两问结束，春子口轻合、半垂眼朝镜头，眉形保持。',
51:'春子平调否定后合口，二人保持站位和朝镜头的方向。',
59:'春子目光仍朝右侧外，眉眼保留原形，身体准备接前冲。',
60:'手指掠离水面，身体继续前送，脸部外显幅度低。',
68:'刀尖留隙、握柄稳，屈腿压制保持，袍布水纹趋稳。',
71:'春子说完理由合口，前俯朝向、半垂眼朝镜头与源眉形保持。',
75:'欧迈及黑脸稍俯，白眼仍朝镜头，董白握刀屈身不变。',
80:'董白直视镜头，刀斜贯胸前、鞘在另一手，眉头压低、嘴角绷紧。',
}

def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def camera_mode(text):
    if text.startswith('固定'): return 'fixed'
    if '跟移' in text or '跟拍' in text: return 'track'
    if '上摇' in text or '下摇' in text or '短摇' in text or '向上摇' in text or '向下' in text and '摇' in text: return 'tilt'
    if '横移' in text or '短移' in text: return 'track'
    if '后拉' in text: return 'pull'
    if '推' in text: return 'push'
    return 'fixed'

def main():
    original = (TASK/'baseline/第19话_制作分镜_Gen2.8.md').read_text(encoding='utf-8')
    inventory = json.loads((TASK/'inventory.json').read_text(encoding='utf-8'))
    ledger = json.loads((TASK/'baseline/source-ledger-v3.json').read_text(encoding='utf-8'))
    observations = json.loads((TASK/'image-observations.json').read_text(encoding='utf-8'))
    observed = {x['image']:x for x in observations}
    panels = {p['image']:p for p in ledger['panels']}
    all_images = {im for s in inventory for im in s['images']}
    assert all_images == set(observed), (all_images-set(observed), set(observed)-all_images)
    for image, ob in observed.items():
        p = panels[image]
        p['camera_gaze_reinspection'] = copy.deepcopy(ob)
        # Keep the validated, image-grounded size/layout signature. Current
        # inspection refines pitch and gaze, not typography or page furniture.
        if image == '第19話_20_001.jpg':
            p['composition_lock'] = p['composition_lock'].replace('低机位','斜俯机位')
        if image == '第19話_22_004.jpg':
            p['composition_lock'] = p['composition_lock'].replace('侧面','后侧俯视')
        observed_angle=ob['angle'].replace('，非头顶俯视','')
        p['composition_lock'] += ' 当前透视观察：'+observed_angle+'。眼部观察：'+ob['gaze']+'。'
        p['source_facts']['relations'].append('取景透视：'+ob['angle'])
        short = image.removeprefix('第19話_').removesuffix('.jpg')
        if short in LENS_FACTS: p['source_facts']['actions'].append(LENS_FACTS[short])
        if image == '第19話_11_002.jpg':
            p['admission']='不把提到双马尾者的能力画成未见战斗；粗口保留语义，发言依春子平淡基调。'
        if image == '第19話_19_003.jpg':
            p['continuity']='青求证后切春子的短否定，下一格行动。'
            p['admission']='源格明确内眉头高、眉尾低、眼睑斜压，2秒短否定保留此形态及朝右的目光；嘴在画外。'
        if image == '第19話_23_004.jpg':
            p['background']={'type':'physical','description':'兜帽和刀尖之间可见灰色水面及细白圆形波纹。','evidence':'current_panel'}
            p['background_description']=p['background']['description']
    # Narrow eye gaps did not establish a downward pupil direction.
    p = panels['第19話_02_002.jpg']
    p['source_facts']['actions'] = ['欧迈及半眯眼，眼缝内瞳孔朝向不清晰', '欧迈及眉间有紧皱的褶纹']
    ledger['shots'][1]['fact_claims']['actions'] = copy.deepcopy(p['source_facts']['actions'])
    # Design cards are saved before the prose is rendered. Existing task/action
    # bridges are retained; facts are only augmented from current inspection.
    plans = {}
    for n, s in enumerate(ledger['shots'], 1):
        inv = inventory[n-1]
        ob = observed[inv['images'][0]]
        old = s.get('motion_decision', {}).get('admitted_plan')
        if n in ACTS and old:
            plan = {
                'opening': OPENINGS.get(n, old['opening']),
                'beats': [ACTS[n]],
                'coupling': PURPOSES.get(n, s['purpose']),
                'landing': LANDINGS.get(n, ACTS[n].split('。')[-2]+'。'),
            }
            plans[s['target']] = plan
        if n in PURPOSES: s['purpose'] = PURPOSES[n]
        source_images = s.get('source_images', [])
        for image in source_images:
            short = image.removeprefix('第19話_').removesuffix('.jpg')
            if short in LENS_FACTS and not (n==50):
                s['fact_claims']['actions'].append(LENS_FACTS[short])
        camera = CAMERAS[n]
        mode = camera_mode(camera)
        cam = {
            'mode':mode,
            'reason':ob['plan'] + ' 当前任务：'+s['purpose'],
            'anchor_phase':s['motion_decision']['source_anchor_placement'],
            'opening':camera.split('，')[0]+'；'+ob['facts'],
            'landing':camera,
            'evidence':ob['angle']+'；'+ob['facts'],
        }
        if mode != 'fixed':
            cam['path_basis'] = {
                'source_refs':inv['images'],
                'observed_path_support':ob['facts'],
                'approved_motion':ob['plan'],
                'extent_limit':'路径在当前源格已见区域及已准入动作范围内；轴向拉开止于源格构图，不展示额外房间/人物/接触。',
            }
        s['camera_decision'] = cam
        s['motion_decision']['observed_anchor'] = panels[inv['images'][0]]['composition_lock']
        s['camera_gaze_revision_review'] = {
            'resolution':'720p','source_images':inv['images'],
            'source_angle':ob['angle'], 'eye_reading':ob['gaze'],
            'camera_plan':ob['plan'], 'reviewed':True,
        }
        if s['target'] in plans:
            s['motion_decision']['admitted_plan'] = copy.deepcopy(plans[s['target']])
            if source_images:
                panels[source_images[0]]['performance_plan'] = copy.deepcopy(plans[s['target']])
        if n in PURPOSES:
            s['motion_decision']['inference_limit']=s['motion_decision']['inference_limit'].replace('辱称译为带鄙夷的女呼。','粗口保留语义、语气平淡。').replace('维持警觉形状','维持可见眉眼形状')
            s['motion_decision']['continuity']=s['motion_decision']['continuity'].replace('春子的警觉','春子的短否定').replace('两人疑惑','青的追问与春子沉默')
            s['motion_decision']['inference_limit'] += ' 本轮角色表演按共享映射版本3：春子低情绪外显，源眉形不解释成情绪递进；保持原主任务、动作桥接与接触。'
            if 'brow_revision_review' in s:
                s['brow_revision_review']['decision'] = '保留复查可见眉形；以本轮三无表演规划取代情绪解释和额外挑眉递进。'
                s['brow_revision_review']['planned_state'] = copy.deepcopy(s['motion_decision'].get('admitted_plan'))
            if n in [22,49]:
                b = s['background_decision']
                b['basis'] = ('静止空底用于春子平淡反应与青的活力形成对比；半垂眼和内眉头高是源形态，'+
                              '不放大成嫌弃或困惑情绪。采用已批准的简洁灰紫至灰米白家族，仍在原位置回到实景。')
                s['background_revision_review']['decision'] = b['basis']
    dump(TASK/'authored-plans.json', {'camera':CAMERAS, 'performance':plans, 'voice_notes':VOICE_NOTES})
    revised = original
    changes = []
    for n, inv in enumerate(inventory, 1):
        fields = copy.deepcopy(inv['fields'])
        fields['镜头设计'] = CAMERAS[n]
        if n in ACTS: fields['可见动作'] = ACTS[n]
        if n in VOICE_NOTES:
            notes = VOICE_NOTES[n]
            matches = list(re.finditer(r'（[^）]*）', fields['台词与语气']))
            assert len(matches)==len(notes), (n,len(matches),len(notes))
            for match, note in reversed(list(zip(matches,notes))):
                if note is not None:
                    fields['台词与语气'] = fields['台词与语气'][:match.start()]+'（'+note+'）'+fields['台词与语气'][match.end():]
        # Camera/backing agreement: inherited room light must not refer to rock
        # planes absent from an occluded face/hand or the water-backed sequence.
        if n==42:
            fields['光影布光']='左上柔光照亮木栏上缘与床单褶面，栏杆暗面偏灰褐，后层岩缝较暗，环境色稳定。'
        if n==43:
            fields['光影布光']='左上柔光落在春子的额头、鼻梁与贴带上缘，棕发暗面压成灰褐块面，半垂双眼留小高光；后层保持低对比。'
        if n==59:
            fields['光影布光']='左上柔光落在春子的耳廓、额侧与鼻梁，棕发暗面保持灰褐块面，眼窝浅暗，半垂眼内留小高光。'
        if n in [61,62,67,68,69,72]:
            fields['光影布光']={
                61:'通道余光柔和照亮鞋背与水面，鞋底接水处压暗，水纹亮边细窄，反光低于主体亮部。',
                62:'通道余光照亮兜帽肩缘与右后水花，深灰袍面保留块面暗部，水面亮纹细窄。',
                67:'通道余光落在春子头肩和握刀手上，黑袍暗面形成清楚块面，身下水面留柔和浅亮反光。',
                68:'通道余光照亮春子背发与露出的手臂，黑袍在下方保持深灰块面，右后水纹浅亮。',
                69:'通道余光照亮青的白发与蓝衣上缘，春子近处棕发暗面压成块面，水面浅亮但低于人物亮部。',
                72:'通道余光沿刀刃形成窄亮边，灰色兜帽布面分出浅暗块面，间隙处水纹低对比。',
            }[n]
        if n==71:
            fields['光影布光']='左上柔光落在春子的额头、鼻梁和肩上，棕发保持灰褐暗面，半垂双眼留小高光；灰色后层低对比。'
        if n==72:
            fields['可见背景']='灰暗水面从兜帽与刀尖之间露出，细白波纹弯过空隙，层次低对比。'
            s=ledger['shots'][n-1]
            s['background_decision']={'mode':'physical','basis':'当前23_004可见兜帽与刀尖之间的灰色水面及白圆纹；不再将可见水面误记为完全遮挡。','source_refs':inv['images'],'inspected_resolution':'720p'}
        # Exact section-local replacement; never globally replace actor words.
        clip, shot = map(int,re.findall(r'\d+',inv['target']))
        clip_pattern = re.compile(r'(## 【片段'+str(clip)+r'】.*?)(?=\n## 【片段|\Z)', re.S)
        cm = clip_pattern.search(revised); assert cm, inv['target']
        chunk = cm.group(1)
        shot_pattern = re.compile(r'(\*\*分镜'+str(shot)+r'（[^\n]+\n)(.*?)(?=\n\*\*分镜|\Z)',re.S)
        sm = shot_pattern.search(chunk); assert sm, (inv['target'],chunk[:100])
        body = sm.group(2)
        for field, value in fields.items():
            pattern = re.compile(r'(【'+field+r'】：)[^\n]*')
            assert len(pattern.findall(body))==1, (inv['target'],field)
            body = pattern.sub(lambda m:m.group(1)+value,body)
        chunk = chunk[:sm.start(2)]+body+chunk[sm.end(2):]
        revised = revised[:cm.start()]+chunk+revised[cm.end():]
        s = ledger['shots'][n-1]
        if n in ACTS:
            if s.get('action_admissions'):
                for admission in s['action_admissions']:
                    admission['claim'] = ACTS[n]
                    admission['visual_evidence'] = ('当前720p观察：'+observed[inv['images'][0]]['facts']+
                         ' 视线：'+observed[inv['images'][0]]['gaze']+
                         '。表演准入：'+s['motion_decision']['inference_limit'])
                    admission['visible_in_framing'] = True
                    admission['anchor_safe'] = True
        s['background_excerpt'] = fields['可见背景']
        changed = {k:{'before':inv['fields'][k],'after':fields[k]} for k in fields if fields[k]!=inv['fields'][k]}
        changes.append({'index':n,'target':inv['target'],'seconds':inv['seconds'], 'source_images':inv['images'],'fields':changed})
        for perf in ledger['performance']:
            if perf['target'] == s['target']:
                if s['target'] in plans:
                    perf['card'] = copy.deepcopy(plans[s['target']])
                    perf['details'] = [fields['可见动作']]
                    perf['long_take_reason'] = plans[s['target']]['coupling']+' 时长'+str(inv['seconds'])+'秒，原台词与动作并行；持态不追加情绪或填时动作。'
                perf['camera_gaze_review'] = copy.deepcopy(s['camera_gaze_revision_review'])
                if n in PURPOSES: perf['confirmed_profile_source']='comic-workspace/character-references/角色映射.md#c002春子'
    revised=revised.replace('人物以整句情绪和任务互动展开表演。','人物通过当下任务与交流展开表演。春子以平淡面容、低情绪外显和自然动作节奏为常态。')
    after = parser.parse(revised)
    assert len(after)==80
    for a,b in zip(inventory, after):
        assert a['target']==b['target'] and a['seconds']==b['seconds'] and a['refs']==b['refs']
        assert re.findall(r'“([^”]+)”',a['fields']['台词与语气']) == re.findall(r'“([^”]+)”',b['fields']['台词与语气'])
    map_path = ROOT/'comic-workspace/character-references/角色映射.md'
    mtext = map_path.read_text(encoding='utf-8')
    profile = re.search(r'- 表演基调（用户于2026-10-11明确确认）：([^\n]+)',mtext).group(1)
    for entry in ledger['character_registry']:
        if entry['id']=='C002':
            entry['performance_profile'] = {'source':'用户明确确认；comic-workspace/character-references/角色映射.md，版本3，2026-10-11','baseline':profile}
    ledger['character_registry_source'].update({'version':3,'date':'2026-10-11','baseline_commit':'cd3c5d9a87f5a2045f342866131834194a8e61d4','sha256':hashlib.sha256(map_path.read_bytes()).hexdigest()})
    ledger['skill_version']='Gen2.8 最新运镜规则与用户确认三无角色基调'
    ledger['skill_version_commit']=SKILL_COMMIT
    ledger['revision_audit'].append({'date':'2026-10-11','reason':'用户视频实践反馈运镜、俯仰视线遗漏与春子情绪OOC','inspected_images':73,'inspected_resolution':'720p','affected_targets':[x['target'] for x in changes],'result':'重新设计80镜镜头字段；源图明确视线落动作字段；春子保留源眉形与身体任务，去掉额外情绪递进；共享角色映射版本3。','supersedes':'此前眉形/背景审阅中对春子不满、警觉、鄙夷与困惑递进的解释由本轮低外显规划取代；历史审计仅留作版本记录。'})
    ledger['final_audit']['camera_gaze_affect_revision']={'inspected_images':73,'reviewed_shots':80,'dialogue_literals_unchanged':True,'references_unchanged':True,'durations_unchanged':True,'source_anchor_policy':'in_process_not_first_frame','character_map_version':3,'video_generated':False}
    DELIVERY.mkdir(parents=True,exist_ok=True)
    CURRENT.write_text(revised,encoding='utf-8')
    (DELIVERY/CURRENT.name).write_text(revised,encoding='utf-8')
    dump(DELIVERY/'source-ledger-v3.json',ledger)
    dump(DELIVERY/'image-observations.json',observations)
    dump(TASK/'changes.json',changes)
    (TASK/'delivery-path.txt').write_text(str(DELIVERY),encoding='utf-8')
    print(json.dumps({'delivery':str(DELIVERY),'shots':80,'images':73,'changed_actions':len(ACTS),'voice_revisions':len(VOICE_NOTES),'camera_modes':{m:sum(s['camera_decision']['mode']==m for s in ledger['shots']) for m in sorted({s['camera_decision']['mode'] for s in ledger['shots']})}},ensure_ascii=False))

if __name__=='__main__': main()
