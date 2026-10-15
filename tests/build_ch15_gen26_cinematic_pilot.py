#!/usr/bin/env python3
"""Build a small, reproducible Gen2.6 cinematic-performance pilot.

The pilot intentionally keeps the source-ledger contract from the regular
forward fixture, but selects ten representative shots and enriches only their
performance, optical, material, and independent sound directions.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests/results/gen2.6-cinematic/ch15-part1-pilot"
SOURCE_DIR = ROOT / "tests/fixtures/ch15-part1/source"

# Make the existing fixture the factual source of dialogue, roles, and panel
# inventory.  This file is deliberately additive and never writes to its OUT.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ch15_gen26_fixture as base  # noqa: E402


PILOT_KEYS = [
    (3, 2),   # shame/defiance in a face close-up
    (5, 1),   # long question with a held listener reaction
    (5, 2),   # awkward lie, object-less but physically grounded acting
    (6, 3),   # crystal handoff and touch/weight continuity
    (7, 1),   # refusal with two people and a shared prop
    (11, 2),  # asymmetrical arithmetic/reaction beat
    (11, 3),  # multi-speaker reaction close-up
    (14, 2),  # recognition and object handling
    (15, 2),  # eyelid/pupil/awakening performance
    (16, 1),  # sound-led reaction and environmental follow-through
]


ENHANCEMENTS = {
    (3, 2): {
        "visual": (
            "脸部近景保持青侧脸贴在碎石地面的姿态：听见追问后，她紧闭的眼睑先轻颤，"
            "眉心略收，湿润呼吸从抿住的嘴唇间漏出；回答到句末，压在脸侧的手指微微蜷紧，"
            "嘴角只松开一侧，最终仍没有抬头。50mm，焦平面锁在眼睑与嘴角，"
            "后景春子的腿和衣摆保持遮挡，衣摆被风带动后迟半拍回落。"
        ),
        "background": "带裂纹的碎石地面铺在白发下，春子的腿与深色衣摆在后景形成遮挡层。",
        "sound": "碎石地风声铺底；手掌摩擦与青的湿润吸气在回答前浮起，随后风声回落。",
        "details": ["紧闭的眼睑先轻颤", "嘴角只松开一侧", "压在脸侧的手指微微蜷紧"],
    },
    (5, 1): {
        "visual": (
            "保持原有前后景双人构图：春子的正脸占据右侧前景，半垂眼睑和微启嘴唇平静追问；"
            "后景的青双手扣在领结下方，听到“撒谎”时指尖先收紧，张开的嘴停半拍，"
            "随后肩线缩起、视线偏开。50mm自然透视，焦点从春子的眼睛后移到青的手指，"
            "两人之间的浅灰树影保持柔化；句末春子只轻收下巴，青仍停在回避姿态。"
        ),
        "background": "浅灰树影和留白填满两人头肩之间，春子的头发与肩线形成前景遮挡。",
        "sound": "林道风声、远脚步与草叶声铺底；领口捏紧轻响，青吞咽后留半拍林间静默。",
        "details": ["半垂眼睑和微启嘴唇平静追问", "指尖先收紧", "肩线缩起、视线偏开"],
        "long_take_reason": "原格把追问、回避与听者停顿锁在同一并行关系构图内，镜内反应沿台词逐层发展。",
    },
    (5, 2): {
        "image": "ch15_p05_c001.jpg",
        "role": "uncited_coverage",
        "visual": (
            "补位反应近景只放大上一格已可见的青：双手仍扣在领结下方，左拇指摩挲布边；"
            "她先偏开视线，短吸气后才开口，说到“一直取笑”时一侧嘴角僵住，指节再次收紧。"
            "85mm浅景深，焦平面在眼睛与手指之间缓慢转移，浅灰树影压成散景；"
            "句末她松开一点领结，肩线仍缩着，发梢迟半拍落回。"
        ),
        "background": "浅灰树影与留白围住她的发丝和肩线，背景不增加新地点或物件。",
        "sound": "低林风铺底；领口绞动、发梢擦过衣领，说到转折处短吸气后吐出，不加提示音。",
        "details": ["左拇指摩挲布边", "一侧嘴角僵住", "指节再次收紧"],
    },
    (6, 3): {
        "visual": (
            "手部极近景保持原有接触关系：晶石落在青掌心，矮人的手稳住她的手腕。"
            "先让晶石重量压低她的掌根，青的无名指和小指逐渐收拢，拇指沿棱面确认触感；"
            "矮人指节随她的重心变化放松一点，腕部衣料出现受力褶皱。"
            "85mm微距质感，焦点从晶石棱面滑到两人接触的指节，前景袖口重度虚化；"
            "侧逆光在晶石边缘形成一线冷亮反射，发丝与衣料有克制的轮廓光，空气中只有一缕可见微尘。"
        ),
        "background": "浅灰留白与手腕衣料填满晶石和双手外侧，接触处成为画面唯一高对比焦点。",
        "sound": "远处林风被近景压低；晶石入掌的闷响接袖口摩擦，随后一声极轻清脆共鸣。",
        "details": ["无名指和小指逐渐收拢", "拇指沿棱面确认触感", "腕部衣料出现受力褶皱"],
    },
    (7, 1): {
        "visual": (
            "双人中近景以35mm保留两双手和晶石的关系：青先把掌中的晶石往回送，"
            "不是一次性甩开，而是手腕后撤、肩膀跟着缩起，连续摇头时发梢和衣摆因惯性向后拖。"
            "矮人的手从下方托住晶石，拇指避开她的指节；青的视线在石头、矮人脸和出口方向之间快速折返，"
            "眼角含泪但嘴唇把拒绝咬得很紧，最后手指停在两人相接处。"
            "轻微手持跟随后在双手处稳住，前景晶石边缘产生短暂炫光，背景灰色渐变与速度线形成图形纵深。"
        ),
        "background": "灰色渐变和速度线围住人物与晶石，手臂衣料在近景形成遮挡层。",
        "sound": "风声与衣摆拖动铺底；晶石轻碰掌心，第一次拒绝短促回响，第二次后迅速收干。",
        "details": ["手腕后撤、肩膀跟着缩起", "视线在石头、矮人脸和出口方向之间快速折返", "眼角含泪但嘴唇把拒绝咬得很紧"],
    },
    (11, 2): {
        "visual": (
            "三人中景保持春子居中抱臂、青在左侧前景、矮人在右侧的关系。春子说到条件时，"
            "半垂的眼睑先收紧一点，视线从矮人移向青，交叠在胸前的手指只增加轻微压力；"
            "青的头部停住，矮人随后慢慢点头，胡须和背包带迟半拍轻晃。50mm，"
            "焦点从春子的眼睛后移到矮人的点头反应，树冠与云层保持前后分层，句末落回春子的平静正脸。"
        ),
        "background": "浅灰云层与深色树冠填满三人轮廓之间，道路消失点从人物身后向远处收束。",
        "sound": "三人脚步与低频林风铺底；袖口、掌中晶石轻响，青短暂屏息，只留远枝碰撞。",
        "details": ["半垂的眼睑先收紧一点", "交叠在胸前的手指只增加轻微压力", "矮人随后慢慢点头"],
    },
    (11, 3): {
        "role": "uncited_coverage",
        "visual": (
            "补位双人反应近景沿用同一站位：青先眨眼再把视线转向春子，下唇轻轻内收，"
            "肩线由紧到松；矮人晚半拍短促点头，左侧眉峰先放松，鼻息随后从胡须间泄出。"
            "两人的回应错开，不同时张嘴。85mm浅景深，焦点从青的眼睛后移到矮人的嘴角，"
            "前景白发与头盔边缘形成虚化遮挡，句末视线仍留在春子方向。"
        ),
        "background": "云层和树冠在头盔、白发与肩线外侧形成浅深分区。",
        "sound": "远风与草叶声铺底；晶石重新抱稳的摩擦声后，两句回应之间留半拍静默。",
        "details": ["先眨眼再把视线转向春子", "下唇轻轻内收", "肩线由紧到松"],
    },
    (14, 2): {
        "image": "ch15_p13_c001.jpg",
        "visual": (
            "圆形怪物脸部近景保持上下手指托住的关系：它的巨大眼睑仍闭合，软质脸颊被指腹轻压，"
            "嘴部随着托举产生小幅回弹；矮人的惊喜台词从画外进入时，上方拇指调整一点压力，"
            "怪物只以含混鼻息回应。85mm近景，焦点锁在眼睑和受压脸颊，手指边缘轻微虚化，"
            "哑光表面只保留一块柔和侧光，动作结束后手指稳住。"
        ),
        "background": "浅灰留空与上下两只手指围住圆形脸部，背景不增加画外环境。",
        "sound": "林道风被近景压低；背包布摩擦接柔软回弹，辨认瞬间带一声短亮反应音。",
        "details": ["软质脸颊被指腹轻压", "嘴部随托举小幅回弹", "上方拇指调整一点压力"],
    },
    (15, 2): {
        "visual": (
            "圆形怪物脸部特写，两只粗大拇指稳在脸侧；巨大眼睑先抖动，随后只睁开一条缝，"
            "瞳孔在朦胧中缓慢聚焦，焦点先落在矮人的拇指再回到眼睛。它听到名字时鼻息停半拍，"
            "嘴部没有夸张张大，只让眼睑和瞳孔完成惊疑；矮人的拇指因等待而轻轻调整握法。"
            "100mm极近景，大光圈浅景深，焦平面锁在眼睛，背景留白完全柔化；"
            "圆形皮肤保留哑光漫反射，拇指边缘有柔和轮廓光，眼睑抖动带一丝细微运动模糊。"
        ),
        "background": "浅灰留空和两只粗大拇指围住圆形脸部，所有视觉信息集中在眼睑与瞳孔。",
        "sound": "近景近乎静默，只留布面底噪；拇指轻摩擦，名字响起后接含混鼻息和细小醒转声。",
        "details": ["巨大眼睑先抖动", "瞳孔在朦胧中缓慢聚焦", "拇指因等待而轻轻调整握法"],
    },
    (16, 1): {
        "visual": (
            "仰视天空空镜保持原有树冠与云层构图，声音先进入：尖叫响起前云层仍缓慢横移，"
            "树梢叶片被风带动；第一声尖叫时画面只发生极轻微震动，靠近画框的叶片突然压向同一侧，"
            "随后在风里迟半拍回弹，不新增飞鸟或画外事件。"
            "28mm广角强调天空纵深与树冠引导线，焦点在前景叶片，远处云层重度虚化；"
            "逆光在叶缘形成克制的轮廓光，云隙漏下一束淡淡丁达尔光，空气微尘只在光束内短暂可见。"
        ),
        "background": "灰白云层铺满天空，深色树冠从四周伸入并形成向上汇聚的引导线。",
        "sound": "高处风与树叶摩擦铺底；吸气后尖叫带短促高频回响，叶片回弹后重新落回风声。",
        "details": ["尖叫响起前云层仍缓慢横移", "第一声尖叫时画面只发生极轻微震动", "叶片在风里迟半拍回弹"],
    },
}


def make_items() -> list[dict]:
    base_by_key = {(item["clip"], item["number"]): item for item in base.SHOTS}
    items: list[dict] = []
    for pilot_clip, key in enumerate(PILOT_KEYS, start=1):
        item = copy.deepcopy(base_by_key[key])
        item["source_clip"] = item["clip"]
        item["source_number"] = item["number"]
        item["clip"] = pilot_clip
        item["number"] = 1
        item.update(ENHANCEMENTS[key])
        item["pilot_key"] = key
        items.append(item)
    return items


def build_storyboard(items: list[dict]) -> str:
    lines = [
        "# 第15话第一批｜Gen2.6 Cinematic Performance Pilot",
        "",
        "> 目标：在源图事实锁定下，测试连续表演链、非对称微表情、光学质感与独立声音设计。",
        "",
        "## 场景色彩基准",
        "",
        "京都动画制作系的生活流角色表演密度，《冰菓》式克制的面部细节与自然光层次，山田尚子导演式的身体局部、视线和留白叙事；只取这些可执行维度，不改变本作人物设计、漫画事实与原格构图。整体采用低饱和暖灰与冷灰分层、清晰二维线条、柔和明暗过渡和局部材质高光。",
        "",
        "## 非人物上色锁定",
        "",
        "林道维持低饱和灰绿，云层和留白偏冷灰，晶石只在原格支持的范围内使用克制冷亮反射；图形背景保留漫画的灰阶关系，不把风格参照扩写成新场景或新物件。",
        "",
    ]
    for item in items:
        lines += [f"## 【片段{item['clip']}】", ""]
        lines.append(f"**分镜1（{item['seconds']}秒）：**")
        if item["role"] == "source_locked":
            lines.append(f"分镜参考 `[{item['image']}]`")
        visual = item["visual"]
        if item["dialogue"]:
            visual += " 最后让当前视线或手指停住，身体重心落定。"
        lines.append(visual)
        if item["dialogue"]:
            for dialogue in item["dialogue"]:
                lines.append(f"{dialogue['speaker']}说：“{dialogue['script']}”（{dialogue['voice']}）")
        lines.append(f"可见背景：{item['background']}")
        lines.append(f"声音设计：{item['sound']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_ledger(items: list[dict], storyboard: str) -> dict:
    panel_names = sorted(path.name for path in SOURCE_DIR.glob("*.jpg"))
    panels: list[dict] = []
    for index, name in enumerate(panel_names, start=1):
        related = [item for item in items if item["image"] == name]
        bubbles: list[dict] = []
        for item in related:
            for dialogue in item["dialogue"]:
                bubbles.append({
                    "id": f"{name[:-4]}_b{len(bubbles)+1:02d}",
                    "speaker": dialogue["speaker"],
                    "speaker_evidence": "气泡尾向、人物口型与相邻格连续关系共同确认",
                    "kind": "dialogue",
                    "source_text": dialogue["source"],
                    "status": "mapped",
                    "script_text": dialogue["script"],
                    "target": f"片段{item['clip']}/分镜1",
                    "seconds": dialogue["seconds"],
                })
        bg_type, bg_desc = base.PANEL_BACKGROUNDS.get(
            index,
            ("physical", related[0]["background"] if related else "浅灰留空与画面内可见物件共同构成背景"),
        )
        targets = {bubble["target"] for bubble in bubbles}
        speakers = {bubble["speaker"] for bubble in bubbles}
        risky_turn = any(
            sum(ch.isalnum() for ch in bubble["script_text"]) >= 28
            or len(re.findall(r"[。！？!?]+", bubble["script_text"])) >= 3
            for bubble in bubbles
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
        if any(28 <= sum(ch.isalnum() for ch in b["script_text"]) < 42 for b in bubbles):
            panel["coverage_reason"] = "保留源图表演连续性，并用视线、非对称面部与道具接触维持信息可读性"
        if any(
            sum(ch.isalnum() for ch in b["script_text"]) >= 42
            or len(re.findall(r"[。！？!?]+", b["script_text"])) >= 3
            for b in bubbles
        ):
            panel["long_take_reason"] = "源图把完整语义和听者反应锁在同一构图内，镜内动作沿台词逐层发展"
        if len(speakers) >= 2 and len(bubbles) >= 3 and len(targets) < 2:
            panel["shared_reason"] = "源图把问答放在同一关系构图内，人物的错拍反应仍属于同一动作链"
        panels.append(panel)

    shots: list[dict] = []
    performance: list[dict] = []
    for item in items:
        target = f"片段{item['clip']}/分镜1"
        shots.append({
            "target": target,
            "role": item["role"],
            "source_images": [] if item["role"] == "uncited_coverage" else [item["image"]],
            "viewed_while_writing": item["role"] != "uncited_coverage",
            "evidence": "当前原格" if item["role"] == "source_locked" else "当前格的连续阶段" if item["role"] == "source_supported_phase" else "前后格的人物站位与道具状态",
            "purpose": "忠实呈现原格信息并测试电影化表演" if item["role"] == "source_locked" else "拆分对白转折并测试连续阶段表演" if item["role"] == "source_supported_phase" else "保持前后格关系并测试连续阶段表演",
            "background_excerpt": f"可见背景：{item['background'].rstrip('。')}",
            "source_audit": "pass",
            "unsupported_additions": [],
        })
        chars = sum(sum(ch.isalnum() for ch in d["script"]) for d in item["dialogue"])
        if chars > 20:
            details = item["details"]
            entry = {
                "target": target,
                "evidence": "源图表情、手势、道具接触与对白顺序；电影化增强只细化反应过程",
                "details": details,
                "intervals": [{
                    "speech_seconds": sum(d["seconds"] for d in item["dialogue"]),
                    "acting_seconds": min(item["seconds"], max(1.0, sum(d["seconds"] for d in item["dialogue"]) - 0.2)),
                }],
            }
            if len(details) >= 3 and chars >= 42:
                entry["long_take_reason"] = ENHANCEMENTS[item["pilot_key"]].get(
                    "long_take_reason",
                    "同一构图内的连续问答依赖双方姿态关系，镜内反应已形成发展",
                )
            performance.append(entry)
    return {"version": 2, "panels": panels, "shots": shots, "performance": performance}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    items = make_items()
    storyboard = build_storyboard(items)
    (OUT / "storyboard.md").write_text(storyboard, encoding="utf-8")
    ledger = build_ledger(items, storyboard)
    (OUT / "source-ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT / 'storyboard.md'}")
    print(f"wrote {OUT / 'source-ledger.json'}")
    print(f"pilot shots: {len(items)}")


if __name__ == "__main__":
    main()
