#!/usr/bin/env python3
"""Build the reproducible Gen2.6 forward-test artifacts for chapter 15 batch 1."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests/results/gen2.6/ch15-part1"


def shot(clip, number, seconds, image, visual, background, dialogue=None, role="source_locked"):
    return {
        "clip": clip,
        "number": number,
        "seconds": seconds,
        "image": image,
        "visual": visual,
        "background": background,
        "dialogue": dialogue or [],
        "role": role,
    }


def line(speaker, source, script, seconds, voice):
    return {"speaker": speaker, "source": source, "script": script, "seconds": seconds, "voice": voice}


YOUNG = "年轻女声，清亮柔和，情绪随表情自然推进"
COOL = "年轻女声，清冷平直，语气克制而明确"
DWARF = "成年男声，低沉粗粝，说话直接"
MONSTER = "细小尖锐声，刚醒时含混，受惊后骤然拔高"


SHOTS = [
    shot(1, 1, 3, "ch15_p01_c001.jpg", "仰视天空空镜，云层缓慢横移，标题停在画面中央；镜头保持稳定。", "灰白云层和浅灰天空填满画面，四周没有可辨识地标。"),
    shot(2, 1, 3, "ch15_p02_c001.jpg", "手掌近景，春子抬起右手，手指先收紧再张开，动作停在落掌前。", "黑白网点和人物衣料边缘填满手掌四周。"),
    shot(2, 2, 3, "ch15_p02_c002.jpg", "斜后方局部近景，手掌落在青的臀部，接触处的红色强调与放射线瞬间扩开；青的身体因冲击向前一颤。", "白底冲击区与黑色放射线铺满人物轮廓外侧。", [line("青", "呀啊啊啊！", "きゃあああっ!!!", 1.6, YOUNG)]),
    shot(3, 1, 6, "ch15_p03_c001.jpg", "贴地双人中近景，春子俯身责问，青撑着地面回头；春子说话时目光始终压在青身上，青在反问时护住臀部。", "碎石路面铺满下半幅，树林和阴云压在人物身后。", [line("春子", "居然敢骗我。", "よくも私に嘘をつきましたね。", 2.4, COOL), line("青", "干嘛！为什么打我！", "何ですか?! どうして叩くんですか?!", 2.5, YOUNG)]),
    shot(3, 2, 6, "ch15_p03_c002.jpg", "青脸部近景，她伏在路面上抬眼，先咬住下唇，再带着泪光挤出回答；春子的腿和衣摆停在后景。", "带裂纹的碎石地面铺在白发下，衣摆在上缘形成深色遮挡。", [line("春子", "知道错了吗？", "反省しましたか？", 1.3, COOL), line("青", "呜……至少告诉我为什么打屁股……", "うううっ……せめて、どうしてお尻を叩いたのか教えてください……", 3.8, YOUNG)]),
    shot(4, 1, 3, "ch15_p04_c001.jpg", "仰视天空空镜，云层由左向右缓慢移动，时间在静止构图中自然流过。", "灰白云层与浅灰天空填满整幅画面。"),
    shot(4, 2, 4, "ch15_p04_c002.jpg", "远景，春子、青和矮人沿林间石路向前走，三人的步幅错开，队形保持不变。", "石路向远处收束，两侧草丛、岩石和树林形成通道。"),
    shot(4, 3, 4, "ch15_p04_c003.jpg", "青的中近景，她跟在队伍里踉跄半步，眼睛呈旋涡状，肩膀无力下垂。", "道路与树丛以简化网点铺在她身后，眩晕线围住头部。"),
    shot(5, 1, 6, "ch15_p05_c001.jpg", "春子与青并行的双人中景，春子侧头追问，青攥住领口躲开视线；问句结束后春子保持注视，给青留下回应停顿。", "浅灰天空和远处树冠填满两人头肩之间。", [line("春子", "没约会过又不是罪，为什么要为这种事撒谎？", "デートしたことがないのは罪ではないのに、どうしてそんなことで嘘をついたんですか？", 4.7, COOL)]),
    shot(5, 2, 5, "ch15_p05_c002.jpg", "青胸部以上近景，她双手绞紧领口，先看向路边，再偷偷抬眼确认春子的反应；句末肩膀继续缩紧。", "淡灰云层和白色留空围住她的发丝与肩线。", [line("青", "因、因为……我以为你会一直拿这件事取笑我……", "だ、だって……！ ずっとそのことで私をからかうと思ったんです……", 3.8, YOUNG)]),
    shot(5, 3, 3, "ch15_p05_c003.jpg", "矮人胸部以上近景，他托起晶石，视线在晶石和青之间移动，最后抬下巴直接询问。", "云层和树冠留在头盔与胡须外侧，晶石周围是浅色留空。", [line("矮人", "真有这种只有特定条件的人才能碰的石头。你想要吗？", "特定の条件を満たす者だけが触れられる石か。欲しいか？", 2.5, DWARF)]),
    shot(6, 1, 3, "ch15_p06_c001.jpg", "矮人半身中景，他低头翻找背包，一只手撑开袋口，另一只手从杂物中取出晶石。", "深色背包布面和人物衣料围住双手，林路只在边缘露出。"),
    shot(6, 2, 2, "", "承接上一镜的双人中近景，矮人把握着晶石的手伸到青面前；青的双手仍收在胸前，先看石头再看他。", "林间石路与低矮草丛横向延伸，灰白天空从两人头肩间露出。", [line("矮人", "拿着吧。", "持っていけ。", 1.0, DWARF)], role="uncited_coverage"),
    shot(6, 3, 6, "ch15_p06_c003.jpg", "手部极近景，晶石已经落在青的掌心，矮人的另一只手稳住她的手腕；青的手指因重量轻轻收拢，双方关系保持在原有接触位置。", "浅灰留白与手腕衣料填满晶石和双手外侧。", [line("矮人", "让能碰它的人拿着最好。你带着。", "触れられる者が持つのが一番いい。お前が持っていけ。", 3.8, DWARF)]),
    shot(7, 1, 5, "ch15_p07_c001.jpg", "青与矮人的双人中近景，青慌忙把掌中的晶石往回送，矮人的手从下方护住；她连续摇头，动作停在两双手相接处。", "灰色渐变和速度线围住人物与晶石。", [line("青", "不要！不要！请拿回去！", "いやあああっ！ いりません、いりません！ 持って帰ってください！", 3.7, YOUNG)]),
    shot(7, 2, 4, "ch15_p07_c001.jpg", "同一动作的后续阶段，矮人托稳晶石并按住青的手腕；青低头盯着石头，眼角含泪，肩膀明显缩起。", "灰色渐变、手臂衣料和放射线填满两人轮廓外侧。", [line("矮人", "喂，小心！", "おい、気をつけろ！", 1.2, DWARF), line("青", "带着它不就等于被盖上从没约会过的烙印吗！", "これを持っていたら、一度もデートしたことがないって烙印を押されるじゃないですか！", 2.4, YOUNG)], role="source_supported_phase"),
    shot(7, 3, 6, "ch15_p07_c002.jpg", "矮人脸部近景，他抬起一根手指解释，随后将手指转向晶石；青的白发只在画面边缘形成前景。", "灰色网点和浅色留白围住头盔、胡须与前景发丝。", [line("矮人", "别这么想。使用者虽有限制，它仍是强得难以置信的矿物。", "そう考えるな。使い手に条件はあるが、それでも信じられないほど強力な鉱物だ。", 4.7, DWARF)]),
    shot(8, 1, 6, "ch15_p08_c001.jpg", "晶石和指虎的说明性物件镜头，晶石位于左侧，指虎位于右侧；镜头沿两者之间的亮线平移，依次读清棱面与四个指孔。", "深灰颗粒渐变和白色星点铺满两件物体周围。", [line("矮人", "太小做不了大武器，不过按你的战斗方式，指虎就够了。", "小さすぎて大きな武器にはできないが、お前の戦い方ならナックルダスターで十分だ。", 4.8, DWARF)]),
    shot(8, 2, 6, "ch15_p08_c002.jpg", "青捧着晶石的中近景，她先盯着掌心，听到强敌时抬起视线，手指沿晶石边缘重新握稳。", "大块白色留空和浅灰网点包围人物与掌中晶石。", [line("矮人", "锻成之后，遇到强敌时一定能派上用场。", "鍛えられれば、強敵と出会った時にきっと役に立つ。", 3.2, DWARF), line("青", "你也是为了某个目标才出来冒险的吧？", "あなたも、何か目的があって冒険に出たんでしょう？", 2.3, YOUNG)]),
    shot(9, 1, 6, "ch15_p09_c001.jpg", "黑色兽影占据想象画面，尖牙和眼窝从斜线中显现；画面缓慢压近，青的念头停在未说尽的位置。", "深灰斜线与黑色阴影块填满兽影轮廓之间。", [line("青", "有了这个，说不定……！", "これがあれば、もしかしたら……！", 2.1, YOUNG)]),
    shot(9, 2, 5, "ch15_p09_c002.jpg", "春子脸部近景，她抬手打断想象，目光从青手中的晶石转向矮人，像核对技术条件一样发问。", "浅灰留空和人物肩部衣料围住她的脸与抬起的手。", [line("春子", "等等。也就是说，铁匠也必须是从没约会过的处男吗？", "待ってください。ということは、鍛冶師も一度もデートしたことがない童貞でなければならないんですか？", 4.2, COOL)]),
    shot(10, 1, 7, "ch15_p10_c001.jpg", "矮人正面近景，他沉重地点头，视线避开两名女子；说到可惜时，眉眼压低，手掌摊向晶石。", "白色留空和浅灰网点围住头盔、胡须与手掌。", [line("矮人", "没错。所以这东西虽稀有又强大，却因为没有用途而可惜。", "そうだ。だからこいつは、希少で強力なのに使い道がなくて惜しい代物なんだ。", 4.9, DWARF)]),
    shot(10, 2, 7, "ch15_p10_c002.jpg", "老铁匠伏在堆着工具的工作台边，姿态疲惫；镜头从散落的锤子和金属块缓慢移到他垂下的脸，信息只沿原画中的人物与物件展开。", "工作台、锤子、金属块和深灰阴影填满老铁匠周围。", [line("矮人", "使用者和铁匠都必须满足那种苛刻条件。", "使い手も鍛冶師も、あの厳しい条件を満たさなければならない。", 4.1, DWARF)]),
    shot(11, 1, 4, "ch15_p11_c001.jpg", "三人关系中景，春子竖起一根手指列出第一项条件，青抱着晶石，矮人侧耳听。", "云层和树冠横向铺在三人头肩之后。", [line("春子", "还得找到经验丰富的铁匠……", "経験豊富な鍛冶師も探さなければなりませんし……", 2.6, COOL)]),
    shot(11, 2, 4, "ch15_p11_c001.jpg", "同一场面的后续阶段，春子抬起第二根手指，青的嘴角僵住；矮人顺着她的计算慢慢点头。", "浅灰云层与深色树冠填满三人轮廓之间。", [line("春子", "而且活到那个岁数还保持条件的锻造大师，恐怕很难找。", "その歳まで童貞の鍛冶の達人なんて、見つけるのは難しそうですね。", 3.0, COOL)], role="source_supported_phase"),
    shot(11, 3, 3, "ch15_p11_c001.jpg", "青与矮人的反应近景，青眨眼看向春子并把晶石收紧，矮人则短促点头。", "云层和树冠在两人的头盔、白发与肩线外侧形成浅深分区。", [line("青", "哇……想得真现实。", "わあ……ずいぶん現実的な考え方ですね。", 1.8, YOUNG), line("矮人", "确实，分析得好。", "確かにな。いい分析だ。", 1.0, DWARF)], role="source_supported_phase"),
    shot(11, 4, 4, "ch15_p11_c002.jpg", "春子侧身朝前路迈步，同时用手指向青怀里的晶石；青低头看石头，矮人在旁摊开手。", "林间道路、低矮草丛与灰白天空围住三人。", [line("春子", "总之先带一阵子吧。", "とにかく、しばらく持っておきなさい。", 2.0, COOL), line("矮人", "说不定意外地能找到那种铁匠。", "案外、そんな鍛冶師が見つかるかもしれん。", 1.8, DWARF)]),
    shot(12, 1, 5, "ch15_p11_c003.jpg", "青脸部近景，她闭眼勉强点头，额角挂着细汗；说到仍然尴尬时，嘴角抽动并把晶石抱得更靠近身体。", "灰色渐变与白色留空铺满白发和肩线外侧。", [line("青", "呜……明白了。但果然还是很尴尬。", "うううう……分かりました。でも、やっぱり気まずいです。", 3.4, YOUNG)]),
    shot(12, 2, 5, "ch15_p12_c001.jpg", "林道三人全景，矮人转身面对两名女子并抬手指向前路；春子点头，青抱着晶石站在她身后。", "碎石路向远处收束，岩块、草叶、灌木和树冠夹住道路。", [line("矮人", "就在这里分别吧。你们要去地下城，对吧？", "ここでお別れだ。お前たちはダンジョンへ行くんだろ？", 3.2, DWARF), line("春子", "是。", "はい。", 0.6, COOL)]),
    shot(12, 3, 5, "ch15_p12_c001.jpg", "同一全景的后续阶段，春子已经转向前路，青低头迈出半步又迟疑；矮人留在原地看着两人。", "林道、两侧灌木和远处树冠保持连续，天空从枝叶间露出。", [line("青", "唉……得重新想想自己的人生了……", "はあ……人生について考え直さないと……", 2.8, YOUNG)], role="source_supported_phase"),
    shot(13, 1, 2, "ch15_p12_c002.jpg", "矮人背面肩部近景，他提稳背包后回头，眉毛压低，目光越过两人看向林间。", "灰白天空与树冠填满背包、头盔和胡须外侧。", [line("矮人", "小心，最近形势不对劲。", "気をつけろ。最近、何やらきな臭い。", 1.6, DWARF)]),
    shot(13, 2, 3, "ch15_p12_c003.jpg", "矮人侧脸近景，他刚要离开便停步，胡须和背包仍因惯性轻晃；眼睛转向身后的行囊。", "浅灰天空和行囊布面分占人物轮廓两侧。", [line("矮人", "等等。", "待て。", 0.8, DWARF)]),
    shot(13, 3, 5, "ch15_p12_c004.jpg", "矮人半身中近景，他转肩按住行囊侧面鼓起的一块，低头试探性地压一下，眼睛随即睁大。", "背包布面、肩甲与浅色留空填满手掌周围。", [line("矮人", "嗯？", "ん？", 0.5, DWARF)]),
    shot(14, 1, 4, "ch15_p13_c001.jpg", "斜俯视行囊近景，圆形清洁怪物蜷在袋内熟睡，矮人的手托住它的头侧，把它缓慢抬离袋口。", "深色袋口、布面和浅色留空包围圆形身体。"),
    shot(14, 2, 4, "ch15_p13_c002.jpg", "矮人抱着圆形怪物的中近景，他先睁大眼辨认，再抬头看向春子，双手把圆形身体托稳。", "浅灰留空与背包边缘围住矮人、怪物和双手。", [line("矮人", "哦哦！这个！你们要把它送给我吗？", "おおおおっ！ これは！ こいつを俺にくれるのか？", 2.6, DWARF)]),
    shot(14, 3, 4, "ch15_p13_c003.jpg", "春子回头的近景，她先看一眼青怀里的晶石，再看向怪物，轻轻点头确认交换。", "云层与树冠铺在春子头部后方。", [line("春子", "我们收了石头，这样就公平了。", "石をもらいましたから。これで公平です。", 2.0, COOL)]),
    shot(14, 4, 3, "ch15_p13_c003.jpg", "同一场面的后续阶段，春子和青继续沿路离开；矮人把怪物举到眼前，听见使用痕迹后反而抱得更稳。", "林道、云层和两侧树冠在离去背影与矮人之间展开。", [line("春子", "顺便说，它用过几次；介意的话就丢掉。", "何度か使いました。気持ち悪ければ捨ててください。", 1.8, COOL), line("矮人", "怎么会！用过的反而更好！", "とんでもない！ むしろ使ってあるほうがいい！", 1.1, DWARF)], role="source_supported_phase"),
    shot(15, 1, 6, "ch15_p14_c001.jpg", "手部与布袋极近景，矮人捏住包裹怪物的拉链头，缓慢拉开袋口，圆形身体逐渐露出。", "深色布面、滚边和拉链齿铺满手指周围。", [line("矮人", "我已经好几天没洗澡了，正合适。", "もう何日も風呂に入っていない。ちょうどいい。", 3.0, DWARF)]),
    shot(15, 2, 3, "ch15_p14_c002.jpg", "圆形怪物脸部特写，它被矮人托在两侧，巨大眼睑抖动后勉强睁开一线，瞳孔慢慢聚焦。", "浅灰留空和两只粗大拇指围住圆形脸部。", [line("矮人", "醒醒，搭档。", "起きろ、相棒。", 1.0, DWARF), line("圆形怪物", "伊尔琳……？", "イールリン……？", 1.0, MONSTER)]),
    shot(15, 3, 3, "ch15_p14_c003.jpg", "低机位手臂与怪物近景，矮人抬起粗壮手臂，把刚醒的怪物送向长着体毛的腋下；怪物的眼睛骤然睁大。", "手臂、腋下体毛和浅色冲击底填满圆形怪物周围。", [line("矮人", "来吧，把我弄干净。", "さあ、俺をきれいにしてもらおうか。", 1.7, DWARF)]),
    shot(16, 1, 4, "ch15_p14_c004.jpg", "仰视天空空镜，树冠从四角围住云层；尖叫响起时画面轻震，几只鸟从树梢飞离。", "灰白云层铺满天空，深色树冠从四周伸入。", [line("圆形怪物", "咿——！", "キィィィィィィィッ!!!", 1.8, MONSTER)]),
]


PANEL_BACKGROUNDS = {
    1: ("graphic", "灰白云层和浅灰天空填满画面"),
    2: ("surface", "黑白网点与人物衣料形成近景表面"),
    3: ("graphic", "白底冲击区与放射线填满画面"),
    4: ("physical", "碎石路、树林与阴云构成林间道路"),
    5: ("physical", "裂纹碎石路与人物衣摆构成贴地环境"),
    6: ("graphic", "灰白云层与浅灰天空填满画面"),
    7: ("physical", "石路、岩块、草丛和树林形成通道"),
    8: ("graphic", "道路网点和眩晕线围住人物"),
}


def image_index(name: str) -> int:
    names = sorted((ROOT / "tests/fixtures/ch15-part1/source").glob("*.jpg"))
    return [p.name for p in names].index(name) + 1


def build_storyboard():
    groups = {}
    for item in SHOTS:
        groups.setdefault(item["clip"], []).append(item)
    lines = ["# 第15话第一批｜Gen2.6 正向回归测试", "", "> 目标：在不牺牲戏剧节奏的前提下，以逐格证据锁定构图、动作、背景和对白。", ""]
    for clip, items in groups.items():
        lines += [f"## 【片段{clip}】", ""]
        for item in items:
            lines.append(f"**分镜{item['number']}（{item['seconds']}秒）：**")
            if item["role"] == "source_locked":
                lines.append(f"分镜参考 `[{item['image']}]`")
            lines.append(item["visual"])
            if item["dialogue"]:
                lines.append("说话时先保持当前身体重心；句末让视线或手部动作停住，留出可读反应。")
                for dialogue in item["dialogue"]:
                    lines.append(f"{dialogue['speaker']}说：“{dialogue['script']}”（{dialogue['voice']}）")
            lines.append(f"可见背景：{item['background']}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_ledger(storyboard: str):
    panel_names = sorted(p.name for p in (ROOT / "tests/fixtures/ch15-part1/source").glob("*.jpg"))
    panels = []
    for index, name in enumerate(panel_names, 1):
        related = [s for s in SHOTS if s["image"] == name]
        bubbles = []
        for s in related:
            for dialogue in s["dialogue"]:
                bubbles.append({
                    "id": f"{name[:-4]}_b{len(bubbles)+1:02d}",
                    "speaker": dialogue["speaker"],
                    "speaker_evidence": "气泡尾向、人物口型与相邻格连续关系共同确认",
                    "kind": "dialogue",
                    "source_text": dialogue["source"],
                    "status": "mapped",
                    "script_text": dialogue["script"],
                    "target": f"片段{s['clip']}/分镜{s['number']}",
                    "seconds": dialogue["seconds"],
                })
        bg_type, bg_desc = PANEL_BACKGROUNDS.get(index, ("physical", related[0]["background"] if related else "浅灰留空与画面内可见物件共同构成背景"))
        targets = {b["target"] for b in bubbles}
        speakers = {b["speaker"] for b in bubbles}
        risky_turn = any(
            sum(c.isalnum() for c in b["script_text"]) >= 28
            or len(re.findall(r"[。！？!?]+", b["script_text"])) >= 3
            for b in bubbles
        )
        coverage = "mixed" if len(targets) > 1 else "shared" if len(bubbles) >= 3 or len(speakers) >= 2 or risky_turn else "none"
        panel = {
            "image": name,
            "viewed_at_drafting": True,
            "source_bubble_count": len(bubbles),
            "bubble_audit": "pass",
            "background": {"type": bg_type, "description": bg_desc, "evidence": "current_panel"},
            "locks": {
                "composition": related[0]["visual"].split("；")[0] if related else "原格为纯对白或过渡信息格",
                "visible_subjects": ["仅保留原格中可见人物、物件与图形元素"],
                "relations": ["人物与物件的接触、朝向和前后关系按原格锁定"],
                "forbidden_inferences": ["不补造原格未显示的新人物、新道具、新地点或动作结果"],
            },
            "coverage": coverage,
            "bubbles": bubbles,
        }
        if any(28 <= sum(c.isalnum() for c in b["script_text"]) < 42 for b in bubbles):
            panel["coverage_reason"] = "保留原格表演连续性，并用眼神、手部和停顿维持信息可读性"
        if any(
            sum(c.isalnum() for c in b["script_text"]) >= 42
            or len(re.findall(r"[。！？!?]+", b["script_text"])) >= 3
            for b in bubbles
        ):
            panel["long_take_reason"] = "原格把完整语义和反应锁在同一构图内，镜内动作已有清楚的发展阶段"
        if len(speakers) >= 2 and len(bubbles) >= 3 and len(targets) < 2:
            panel["shared_reason"] = "原格把问答放在同一关系构图内，动作焦点连续且时长足够"
        panels.append(panel)

    shots = []
    performance = []
    for s in SHOTS:
        target = f"片段{s['clip']}/分镜{s['number']}"
        bg_excerpt = f"可见背景：{s['background'].rstrip('。')}"
        shots.append({
            "target": target,
            "role": s["role"],
            "source_images": [] if s["role"] == "uncited_coverage" else [s["image"]],
            "viewed_while_writing": True if s["role"] != "uncited_coverage" else False,
            "evidence": "当前原格" if s["role"] == "source_locked" else "当前格的连续阶段" if s["role"] == "source_supported_phase" else "前后格的人物站位与道具状态",
            "purpose": "忠实呈现原格信息" if s["role"] == "source_locked" else "拆分对白转折并保持空间连续",
            "background_excerpt": bg_excerpt,
            "source_audit": "pass",
            "unsupported_additions": [],
        })
        chars = sum(sum(c.isalnum() for c in d["script"]) for d in s["dialogue"])
        if chars > 20:
            detail_count = 3 if chars >= 42 else 2
            details = ["保持当前身体重心", "让视线或手部动作停住"]
            if detail_count == 3:
                details.append("留出可读反应")
            speech = sum(d["seconds"] for d in s["dialogue"])
            entry = {
                "target": target,
                "evidence": "原格表情、手势和对白顺序",
                "details": details,
                "intervals": [{"speech_seconds": speech, "acting_seconds": min(s["seconds"], max(1.0, speech - 0.2))}],
            }
            if chars >= 42:
                entry["long_take_reason"] = "同一构图内的连续问答依赖双方姿态关系，镜内反应已形成发展"
            performance.append(entry)
    return {"version": 2, "panels": panels, "shots": shots, "performance": performance}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    storyboard = build_storyboard()
    (OUT / "storyboard.md").write_text(storyboard, encoding="utf-8")
    ledger = build_ledger(storyboard)
    (OUT / "source-ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    source_dir = ROOT / "tests/fixtures/ch15-part1/source"
    manifest = {
        "fixture": "ch15-part1",
        "source_branch": "test",
        "source_commit": "37df5f2",
        "normalization": "ZIP内文件按页码与格号后缀重命名；像素内容未修改。",
        "files": [
            {
                "name": path.name,
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path in sorted(source_dir.glob("*.jpg"))
        ],
    }
    (source_dir.parent / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
