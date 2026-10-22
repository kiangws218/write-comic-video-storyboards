"""Gen2.8.2 V3 policy. Consistency checks do not certify visual/acting truth."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import re
from pathlib import Path

POLICY = "2.8.2"
FIELDS = ("镜头设计", "可见动作", "可见背景", "台词与语气", "光影布光", "声音设计")
DIMENSIONS = {"subject", "scale", "viewpoint", "composition", "information",
              "action_phase", "emotion", "rhythm", "dramatic_function"}
QUOTE = re.compile(r'“([^”]*)”|「([^」]*)」|"([^"\n]*)"')
SPEECH = re.compile(
    r'(?m)^\s*([^\n：:“”「」"]+?)\s*[：:]\s*(?:“([^”]*)”|「([^」]*)」|"([^"\n]*)")'
)
SILENCE = re.compile(r'[（(]沉默\s*(\d+(?:\.\d+)?)\s*秒[）)]')


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def seconds(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def authoring_tools():
    # Also works when legacy callers load this file with importlib from another cwd.
    spec = importlib.util.spec_from_file_location("storyboard_authoring", Path(__file__).with_name("authoring.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_snapshot(ledger):
    """Only source observations and locked text, never final shot mappings or approvals."""
    if not isinstance(ledger, dict) or not isinstance(ledger.get("panels"), list) or not ledger["panels"]:
        raise ValueError("panels必须是非空数组")
    panels = []
    for p in ledger["panels"]:
        if not isinstance(p, dict) or not nonempty(p.get("image")):
            raise ValueError("原格缺少image")
        bubbles = p.get("bubbles")
        count = p.get("source_bubble_count")
        if not isinstance(bubbles, list) or isinstance(count, bool) or not isinstance(count, int) or count != len(bubbles):
            raise ValueError(f"{p['image']}气泡数或数组无效")
        overlays = p.get("page_overlays", [])
        if not isinstance(overlays, list) or any(not isinstance(v, dict) for v in overlays):
            raise ValueError(f"{p['image']}page_overlays须为对象数组")
        locked = []
        for b in bubbles:
            if not isinstance(b, dict) or any(not nonempty(b.get(k)) for k in
                    ("id", "speaker", "kind", "source_text", "script_text")):
                raise ValueError(f"{p['image']}气泡缺少原文、锁定译文、身份或类型")
            locked.append({k: b[k] for k in ("id", "speaker", "kind", "source_text", "script_text")}
                          | {"overlap": b.get("overlap", False)})
        panels.append({k: p.get(k) for k in ("image", "renderable_visual", "composition_lock",
                       "source_facts", "background", "node_state", "source_bubble_count")}
                      | {"bubbles": locked, "page_overlays": [
                          {k: v.get(k) for k in ("kind", "source_text", "render", "audio_meaning")}
                          for v in overlays]})
        # New observations are frozen when present; existing 2.8.2 locks remain readable.
        for key in ("narrative_kind", "action_reading"):
            if key in p:
                panels[-1][key] = p[key]
    result = {"source_language": ledger.get("source_language"), "panels": panels}
    for key in ("requires_route_confirmation", "action_routes"):
        if key in ledger:
            result[key] = ledger[key]
    return result


def make_source_lock(ledger):
    snapshot = source_snapshot(ledger)
    return {"version": 1, "sha256": digest(snapshot),
            "manifest": [{"image": p["image"], "renderable_visual": p["renderable_visual"]}
                         for p in snapshot["panels"]]}


def review_digest(ledger, text):
    """Bind actual reviewed text, states, casts and performance; never grant an approval."""
    ledger = authoring_tools().expand(ledger)
    payload = {"text": text, **{k: ledger.get(k) for k in
               ("skill_version", "source_lock", "shots", "performance", "character_registry")}}
    if "character_registry_source" in ledger:
        payload["character_registry_source"] = ledger["character_registry_source"]
    return digest(payload)


def speaker_kind(label):
    kind = "inner" if re.search(r"内心|独白", label) else "narration" if "旁白" in label else "dialogue"
    name = re.sub(r"[（(][^）)]*[）)]", "", label).strip()
    name = re.sub(r"(?:说道|问道|回答道|回答|说|问)$", "", name).strip()
    return name, kind


def spoken_entries(field):
    return [(speaker_kind(m.group(1)), next(g for g in m.groups()[1:] if g is not None), m.start())
            for m in SPEECH.finditer(field)]


def merged(entries):
    result = []
    for who, text in entries:
        if result and result[-1][0] == who:
            result[-1] = (who, result[-1][1] + text)
        else:
            result.append((who, text))
    return result


def validate_director_ledger(ledger, text, image_dir, warnings, h):
    """Return errors; source insufficiency emits warnings without approval requirements."""
    errors = []
    warn = warnings.append if warnings is not None else lambda _: None
    if not isinstance(ledger, dict):
        return ["2.8.2台账根必须是对象。"]
    try:
        tools = authoring_tools()
        tools.check_routes(ledger)
        ledger = tools.expand(ledger)
    except (ValueError, TypeError, KeyError) as exc:
        return [f"创作台账无效：{exc}"]
    if ledger.get("version") != 3:
        errors.append("2.8.2沿用version:3。")
    language = ledger.get("source_language")
    if not nonempty(language):
        errors.append("缺少source_language。")
        language = ""
    if ledger.get("migration_review_required"):
        errors.append("旧台账迁移尚未实际复核，不能自动升级为2.8.2。")
    try:
        lock = make_source_lock(ledger)
    except (ValueError, TypeError) as exc:
        return errors + [f"2.8.2来源记录无效：{exc}"]
    if ledger.get("source_lock") != lock:
        errors.append("来源／对白锁不一致或缺失：原格、原文、译文、归属、类型与顺序不能在导演轮改写；先核对第二轮真实记录。")

    shot_map = h["build_shot_map"](text)
    order = list(shot_map)
    rank = {t: i for i, t in enumerate(order)}
    records = ledger.get("shots")
    if not isinstance(records, list) or any(not isinstance(s, dict) for s in records):
        return errors + ["shots必须是对象数组。"]
    targets = [s.get("target") for s in records]
    if targets != order:
        errors.append("shots必须逐一按最终镜头顺序登记，不能漏镜、重镜、藏切镜或混用旧目标。")
    by_target = {s["target"]: s for s in records if isinstance(s.get("target"), str)}
    panels = ledger["panels"]
    images = [p["image"] for p in panels]
    if len(set(images)) != len(images):
        errors.append("原格image重复；多格文件须有诚实独立标识。")
    by_image = {p["image"]: p for p in panels}
    original_order = [p["image"] for p in panels if p.get("renderable_visual") is True]
    actual_originals = []
    fields_by_target = {t: h["shot_field_values"](block) for t, (_, block) in shot_map.items()}
    speech_by_target = {t: [] for t in order}
    last_event = (-1, -1.0)
    previous_end = {}
    durations = {t: float(next(iter(h["SHOT_RE"].finditer(block))).group(2))
                 for t, (_, block) in shot_map.items() if h["SHOT_RE"].search(block)}
    if set(order) != set(durations):
        errors.append("2.8.2最终序列使用逐镜编号；自动分镜不能隐藏原作镜头与邻接比较。")
    for p in panels:
        image = p["image"]
        if image_dir is not None and not (image_dir / image).is_file():
            errors.append(f"原格文件不存在：{image}")
        if p.get("viewed_at_drafting") is not True or p.get("bubble_audit") != "pass":
            errors.append(f"{image}缺少真实看图／气泡复核记录；工具不能自动填通过。")
        if p.get("drafting_resolution") not in {"720p", "1080p", "original"}:
            errors.append(f"{image}的drafting_resolution无效。")
        if p.get("drafting_resolution") in {"1080p", "original"} and not nonempty(p.get("resolution_escalation_reason")):
            errors.append(f"{image}缺少放大原因。")
        if not isinstance(p.get("renderable_visual"), bool):
            errors.append(f"{image}须明确renderable_visual。")
        if p.get("renderable_visual"):
            reading = p.get("action_reading")
            if p.get("narrative_kind") in ("action", "mixed") or reading is not None:
                if not isinstance(reading, dict) or any(not nonempty(reading.get(k)) for k in
                        ("summary", "phase", "world_motion", "screen_motion", "grounding", "basis")):
                    errors.append(f"{image}缺少动作含义复核：主动作、阶段、世界／画面方向、接地状态与理解依据。")
                elif nonempty(reading.get("uncertainty")):
                    warn(f"[动作理解] {image}保留歧义：{reading['uncertainty']}；不可默认为静止或伪报确认。")
            elif p.get("narrative_kind") is None:
                warn(f"[动作理解] {image}旧记录未分类；关键动作须回图复核，来源锁不能证明读懂。")
            if not nonempty(p.get("composition_lock")) or not isinstance(p.get("node_state"), dict) or not p["node_state"]:
                errors.append(f"{image}缺少真实构图或已知node_state。")
            if not isinstance(p.get("source_facts"), dict) or any(
                not isinstance(p["source_facts"].get(k), list) or
                any(not nonempty(v) for v in p["source_facts"][k]) for k in ("entities", "actions", "relations")):
                errors.append(f"{image}的source_facts须分开entities/actions/relations原子事实。")
        overlays = p.get("page_overlays", [])
        if p.get("renderable_visual") is False and not overlays:
            errors.append(f"{image}纯排字格缺少原作信息映射。")
        for overlay in overlays:
            if overlay.get("render") is not False or not nonempty(overlay.get("source_text")):
                errors.append(f"{image}页面文字须诚实记录且不得作为生成画面。")
            elif overlay.get("kind") == "sfx":
                target, excerpt = overlay.get("target"), overlay.get("audio_excerpt")
                if not isinstance(target, str) or target not in fields_by_target or not nonempty(excerpt) or excerpt not in fields_by_target.get(target, {}).get("声音设计", ""):
                    errors.append(f"{image}拟声信息未实际映射到声音设计。")
        ids = []
        for b in p["bubbles"]:
            ids.append(b["id"])
            label = f"{image}/{b['id']}"
            if b.get("kind") not in {"dialogue", "inner", "narration"} or b.get("status") != "mapped":
                errors.append(f"{label}必须完整mapped并保留正确类型，不能omitted。")
            mappings = b.get("segments", [b])
            if not isinstance(mappings, list) or not mappings or any(not isinstance(m, dict) for m in mappings):
                errors.append(f"{label}的segments必须是非空对象数组。")
                continue
            if b["script_text"] != "".join(m.get("script_text", "") for m in mappings if isinstance(m.get("script_text"), str)):
                errors.append(f"{label}台词片段拼接不等于锁定全文。")
            if language.lower() in {"ja", "jp", "japanese"} and b["source_text"] != b["script_text"]:
                errors.append(f"{label}日文原句不得改写。")
            for m in mappings:
                target, value = m.get("target"), m.get("script_text")
                start, length = m.get("start"), m.get("seconds")
                if not isinstance(target, str) or target not in rank or not nonempty(value):
                    errors.append(f"{label}发声映射目标或正文无效。")
                    continue
                if not seconds(start) or not seconds(length) or length <= 0:
                    errors.append(f"{label}须记录实际非负start与正seconds。")
                    continue
                key = (rank[target], float(start))
                if key < last_event:
                    errors.append(f"{label}改变了原作对白／跨镜片段顺序。")
                last_event = key
                if start + length > durations.get(target, 0) + .001:
                    errors.append(f"{label}发声超出{target}实际镜头时长。")
                if start < previous_end.get(target, 0) - .001 and b.get("overlap") is not True:
                    errors.append(f"{label}与前句发声重叠，原作未登记overlap。")
                previous_end[target] = max(previous_end.get(target, 0), start + length)
                speech_by_target[target].append(((b["speaker"], b["kind"]), value, start, length))
                if length + .35 < h["estimated_japanese_speech_seconds"](value):
                    warn(f"[演出计时] {label}短于文字预估，按真实发声复查；估算不是硬语速。")
        if len(ids) != len(set(ids)):
            errors.append(f"{image}气泡ID重复。")

    for idx, target in enumerate(order):
        s = by_target.get(target, {})
        f = fields_by_target[target]
        try:
            if not isinstance(s.get("duration"), (int, float)):
                raise ValueError("时长须为数值")
            tools.duration_seconds(s.get("duration"))
        except ValueError:
            errors.append(f"{target}台账duration须为大于0的0.5秒整数倍。")
        errors.extend(tools.action_timeline_errors(f.get("可见动作", ""), durations.get(target), target))
        if s.get("duration") != durations.get(target):
            errors.append(f"{target}台账duration与最终正文时长不一致。")
        planned_fields = s.get("fields")
        if not isinstance(planned_fields, dict) or any(not isinstance(planned_fields.get(k), str) or planned_fields[k].strip() != f.get(k, "").strip() for k in FIELDS):
            errors.append(f"{target}实际六字段与规划记录不一致，不能沿用旧稿。")
        role = s.get("role")
        if not nonempty(s.get("purpose")):
            errors.append(f"{target}缺少具体演出作用purpose。")
        if not isinstance(role, str) or role not in {"source_locked", "source_supported_phase", "uncited_coverage"}:
            errors.append(f"{target}角色分类无效，不能默认全是原镜。")
        refs = s.get("source_images")
        if not isinstance(refs, list) or any(not isinstance(v, str) for v in refs):
            errors.append(f"{target}source_images必须是字符串数组。")
            refs = []
        if role == "source_locked":
            if not refs or any(image not in original_order for image in refs):
                errors.append(f"{target}须绑定真实可视原格，不能替换或引用纯排字格。")
            actual_originals.extend(refs)
            # Camera phase bullets repeat filenames; only the formal header owns references.
            header = shot_map[target][1].split("【镜头设计】", 1)[0]
            if h["REFERENCE_RE"].findall(header) != refs:
                errors.append(f"{target}正式原图引用与绑定不一致。")
            anchors = s.get("anchors") if len(refs) > 1 else [s]
            if len(refs) > 1:
                positions = [original_order.index(v) for v in refs if v in original_order]
                if not positions or positions != list(range(positions[0], positions[0] + len(refs))):
                    errors.append(f"{target}只可合并连续原格，不能跨越其他节点。")
                if not nonempty(s.get("merge_basis")):
                    errors.append(f"{target}缺少真实连续镜头的合并理由，不能仅因相似删格。")
                if not isinstance(anchors, list) or any(not isinstance(a, dict) for a in anchors) or [a.get("image") for a in anchors] != refs:
                    errors.append(f"{target}合并原格须按顺序逐一登记anchors，不能只剩引用。")
                    anchors = []
                phases = list(h["MULTI_REF_BULLET_RE"].finditer(f.get("镜头设计", "")))
                if [m.group(1) for m in phases] != refs:
                    errors.append(f"{target}镜头设计须按源顺序列出连续原格阶段参考。")
            last_start = -1.0
            for image, anchor in zip(refs, anchors if isinstance(anchors, list) else []):
                if image not in by_image:
                    continue
                p = by_image[image]
                if p.get("anchor_target") != target:
                    errors.append(f"{image}的anchor_target未指向实际原作镜头。")
                known, state = p.get("node_state"), anchor.get("anchor_state")
                if not isinstance(known, dict) or not isinstance(state, dict) or any(state.get(k) != v for k, v in known.items()):
                    errors.append(f"{target}/{image}未收束到漫画节点的已知anchor_state。")
                if anchor.get("anchor_phase") not in ("preparation", "process", "middle", "contact", "reaction", "result", "state", "endpoint") or not nonempty(anchor.get("anchor_elements")):
                    errors.append(f"{target}/{image}缺少原作时间阶段或保留要素。")
                if len(refs) > 1:
                    start, excerpt = anchor.get("start"), anchor.get("action_excerpt")
                    if not seconds(start) or start <= last_start or start >= durations.get(target, 0):
                        errors.append(f"{target}/{image}节点start须在镜内严格递增，不要求停住。")
                    else:
                        last_start = start
                    if not nonempty(excerpt) or excerpt not in f.get("可见动作", ""):
                        errors.append(f"{target}/{image}原格阶段未落实到实际可见动作。")
                if isinstance(p.get("action_reading"), dict):
                    excerpt = anchor.get("meaning_excerpt")
                    if not nonempty(excerpt) or excerpt not in f.get("可见动作", ""):
                        errors.append(f"{target}/{image}动作含义须落实到正文meaning_excerpt；标签不证明读懂。")
            if s.get("viewed_while_writing") is not True or s.get("source_audit") != "pass":
                errors.append(f"{target}原作镜头缺少真实看图比较。")
        else:
            if refs or h["REFERENCE_RE"].findall(shot_map[target][1]):
                errors.append(f"{target}是导演镜头，不可伪装正式原镜引用。")
            related = s.get("derived_from")
            if not isinstance(related, list) or not related or any(not isinstance(v, str) or v not in by_image for v in related):
                errors.append(f"{target}缺少相关原作节点derived_from；这是来源关联，不要求逐动作证据。")
            contrast = s.get("neighbor_contrast")
            if not isinstance(contrast, dict):
                contrast = {}
            for direction, other_idx in (("previous", idx - 1), ("next", idx + 1)):
                if not 0 <= other_idx < len(order):
                    continue
                entry = contrast.get(direction)
                expected = order[other_idx]
                if not isinstance(entry, dict) or entry.get("target") != expected:
                    errors.append(f"{target}缺少对最终{direction}邻镜{expected}的差异记录。")
                    continue
                changes = entry.get("changes")
                if not isinstance(changes, list) or not changes:
                    errors.append(f"{target}对{expected}至少需要一项显著差异。")
                    continue
                for c in changes:
                    if not isinstance(c, dict) or not isinstance(c.get("dimension"), str) or c["dimension"] not in DIMENSIONS or not nonempty(c.get("description")):
                        errors.append(f"{target}显著差异须有有效维度与具体说明。")
                        continue
                    excerpt = c.get("excerpt")
                    pair_text = "\n".join(f.values()) + "\n" + "\n".join(fields_by_target[expected].values())
                    if not nonempty(excerpt) or excerpt not in pair_text:
                        errors.append(f"{target}差异摘录未落实到实际前后镜头；标签不能证明显著。")
            warn(f"[来源] {target}为导演新增：缺少直接漫画画面不是准入错误；统一场景假设并保留原作结果。")
        if s.get("reference_mode") == "first_frame":
            errors.append(f"{target}不能把漫画绑定为视频首帧。")
        if s.get("unsupported_additions"):
            warn(f"[来源] {target}存在导演添加内容，按节点与内部连续性检查，不要求消除证据空白。")
        if s.get("creative_additions"):
            warn(f"[来源] {target}的创作补充沿用统一设计，不回填为原图观察。")
        claims = s.get("fact_claims")
        if claims is not None:
            related = refs if role == "source_locked" else s.get("derived_from", [])
            if not isinstance(claims, dict):
                errors.append(f"{target}fact_claims须为观察事实对象；创作不必填此字段。")
            else:
                for kind in ("entities", "actions", "relations"):
                    values = claims.get(kind, [])
                    allowed = set()
                    for image in related if isinstance(related, list) else []:
                        if not isinstance(image, str) or image not in by_image:
                            continue
                        facts = by_image[image].get("source_facts", {})
                        observed = facts.get(kind, []) if isinstance(facts, dict) else []
                        if isinstance(observed, list):
                            allowed.update(v for v in observed if isinstance(v, str))
                    if not isinstance(values, list) or any(not isinstance(v, str) or v not in allowed for v in values):
                        errors.append(f"{target}把未观察内容伪报为fact_claims.{kind}；原创放creative_additions。")
        for key in ("state_in", "state_out"):
            state = s.get(key)
            if not isinstance(state, dict) or not state or any(not isinstance(k, str) or not isinstance(v, (str, int, float, bool)) or isinstance(v, float) and not math.isfinite(v) for k, v in state.items()):
                errors.append(f"{target}缺少明确的世界状态{key}。")
        if idx:
            prev = by_target.get(order[idx - 1], {}).get("state_out", {})
            cur = s.get("state_in", {})
            boundary = s.get("boundary", {})
            if isinstance(prev, dict) and isinstance(cur, dict):
                changed = [k for k in prev.keys() & cur.keys() if prev[k] != cur[k]]
                if changed and not (isinstance(boundary, dict) and boundary.get("kind") == "ellipsis"
                                    and boundary.get("from") == order[idx - 1] and nonempty(boundary.get("reason"))):
                    errors.append(f"{target}镜头连接状态跳变：{changed}；在动作内演出变化，或诚实说明原作时间省略。")
                elif changed:
                    warn(f"[连续性] {target}有明确省略，请人工核对不掩盖到达失败：{changed}")
        flags = s.get("risk_flags", [])
        if not isinstance(flags, list) or any(not isinstance(v, str) or v not in {"D", "P", "G"} for v in flags):
            errors.append(f"{target}risk_flags应为D/P/G字符串数组。")
        elif not nonempty(s.get("risk_basis")):
            errors.append(f"{target}缺少实际路由risk_basis。")

        # Exact rendered speech, owner and kind; count no action-field quotations.
        field = f.get("台词与语气", "")
        actual = spoken_entries(field)
        expected = speech_by_target[target]
        if merged([(who, value) for who, value, _ in actual]) != merged([(who, value) for who, value, _, _ in expected]):
            errors.append(f"{target}正式对白与锁定映射不一致（增删改／归属／类型）。")
        if len(QUOTE.findall(field)) != len(actual):
            errors.append(f"{target}存在未按说话人登记的引号内容。")
        remaining = SPEECH.sub("", field)
        remaining = SILENCE.sub("", remaining)
        remaining = re.sub(r"[（(][^）)\n]*[）)]|无台词", "", remaining)
        if re.sub(r"[\s，,；;。.!！?？]+", "", remaining):
            errors.append(f"{target}台词字段含未登记发声或不支持的排版；每条准确台词独立一行，语气放括号。")
        if not expected and "无台词" not in field:
            errors.append(f"{target}纯表演镜头应明确无台词，不补发声。")
        silences = s.get("silences", [])
        if not isinstance(silences, list) or any(not isinstance(v, dict) for v in silences):
            errors.append(f"{target}silences必须是实际时间对象数组。")
            silences = []
        declared = []
        for silence in silences:
            a, n = silence.get("start"), silence.get("seconds")
            if not seconds(a) or not seconds(n) or n <= 0 or a + n > durations.get(target, 0) + .001:
                errors.append(f"{target}沉默超时或数值无效。")
                continue
            declared.append((a, n))
            if any(a < b + length - .001 and b < a + n - .001 for _, _, b, length in expected):
                errors.append(f"{target}沉默与发声重叠。")
        declared.sort()
        if any(b < a + n - .001 for (a, n), (b, _) in zip(declared, declared[1:])):
            errors.append(f"{target}沉默区间重复或重叠。")
        marks = [(m.start(), float(m.group(1))) for m in SILENCE.finditer(field)]
        if [n for _, n in marks] != [n for _, n in declared]:
            errors.append(f"{target}明确沉默标记未按实际时间登记。")
        # Aggregate adjacent speech entries before comparing silence placement.
        text_types = [kind for _, kind in sorted([(p, "speech") for _, _, p in actual] + [(p, "silence") for p, _ in marks])]
        time_types = [kind for _, kind in sorted([(a, "speech") for _, _, a, _ in expected] + [(a, "silence") for a, _ in declared])]
        squeeze = lambda seq: [v for i, v in enumerate(seq) if i == 0 or v != seq[i - 1]]
        if squeeze(text_types) != squeeze(time_types):
            errors.append(f"{target}句前／句后沉默位置与时间线不一致。")
        if sum(len(v) for _, v, _, _ in expected) >= 28:
            warn(f"[演出] {target}长台词：审查角色参与、听者、停顿或覆盖，不按字数强制切镜。")

    if actual_originals != original_order:
        errors.append("原作镜头完整性／顺序错误：每个可视原格节点须按顺序保留一次；连续格可合镜，不能漏掉或重复。")

    performance = ledger.get("performance", [])
    if not isinstance(performance, list) or any(not isinstance(v, dict) for v in performance):
        errors.append("performance必须是对象数组。")
        performance = []
    planned = {}
    for item in performance:
        target = item.get("target")
        if not isinstance(target, str) or target not in rank or target in planned:
            errors.append("performance存在未知或重复target。")
            continue
        planned[target] = item
        card = item.get("card")
        flags = by_target.get(target, {}).get("risk_flags", [])
        if isinstance(flags, list) and "P" in flags:
            if not isinstance(card, dict) or any(not nonempty(card.get(k)) for k in ("opening", "coupling", "landing")) or not isinstance(card.get("beats"), list) or not card["beats"] or any(not nonempty(v) for v in card["beats"]):
                errors.append(f"{target}缺少真实表演计划card。")
        details = item.get("details")
        if not isinstance(details, list) or not details or any(not nonempty(v) or v not in fields_by_target[target].get("可见动作", "") for v in details):
            errors.append(f"{target}表演计划没有落实到动作正文。")
        intervals = item.get("intervals")
        total = 0
        if not isinstance(intervals, list) or not intervals:
            errors.append(f"{target}缺少实际串并行计时。")
            continue
        speech_total = 0
        for interval in intervals:
            if not isinstance(interval, dict) or any(not seconds(interval.get(k)) for k in ("speech_seconds", "acting_seconds")) or not isinstance(interval.get("concurrent", True), bool):
                errors.append(f"{target}计时间隔无效。")
                continue
            a, b = interval["speech_seconds"], interval["acting_seconds"]
            speech_total += a
            total += max(a, b) if interval.get("concurrent", True) else a + b
        if total > durations.get(target, 0) + .001 or speech_total + .001 < sum(v[3] for v in speech_by_target[target]):
            errors.append(f"{target}表演计时超过镜长或遗漏发声。")
    for target, s in by_target.items():
        flags = s.get("risk_flags", [])
        if isinstance(flags, list) and "P" in flags and target not in planned:
            errors.append(f"{target}标记P却没有实际表演卡。")

    registry = ledger.get("character_registry", [])
    profiles = {}
    ids, names, aliases = set(), set(), {}
    if not isinstance(registry, list):
        errors.append("character_registry必须是数组。")
        registry = []
    for person in registry:
        if not isinstance(person, dict) or not nonempty(person.get("canonical_name")):
            errors.append("角色记录须有canonical_name。")
            continue
        profile = person.get("performance_profile")
        name, char_id = person["canonical_name"], person.get("id")
        if name in names or char_id is not None and (not nonempty(char_id) or char_id in ids):
            errors.append("角色稳定ID或统一称呼重复／无效。")
        names.add(name)
        if char_id is not None:
            ids.add(char_id)
        for alias in person.get("aliases", []) if isinstance(person.get("aliases", []), list) else []:
            if nonempty(alias) and alias != name:
                if alias in aliases and aliases[alias] != name:
                    errors.append(f"角色别称冲突：{alias}。")
                aliases[alias] = name
        if person.get("identity_status") == "unidentified":
            if not nonempty(char_id) or not nonempty(person.get("color_prompt")) or not nonempty(person.get("color_basis")):
                errors.append(f"{name}未识别角色须有稳定ID、上色提示词与颜色来源／生产设计说明。")
            elif f"{char_id}｜{name}：{person['color_prompt']}" not in text.split("## 【片段", 1)[0]:
                errors.append(f"{name}上色提示词未放在脚本开头。")
        if not isinstance(profile, dict) or not nonempty(profile.get("baseline")) or not nonempty(profile.get("source")):
            errors.append(f"{person['canonical_name']}缺少已确认表演基准及来源。")
        else:
            profiles[person["canonical_name"]] = profile
    for alias, owner in aliases.items():
        if alias in names and alias != owner:
            errors.append(f"角色别称与另一统一称呼冲突：{alias}。")
    for s in records:
        cast = s.get("characters", [])
        if not isinstance(cast, list) or any(not isinstance(v, str) for v in cast):
            errors.append(f"{s.get('target')}characters必须是字符串数组。")
            continue
        for name in cast:
            if name in aliases:
                errors.append(f"{s.get('target')}角色称呼须统一：{name}→{aliases[name]}。")
            if name not in profiles:
                warn(f"[角色] {name}缺少已确认性格；不凭外观补造隐藏性格，人工核对演出。")
    for target, entries in speech_by_target.items():
        for (name, _), *_ in entries:
            if name in aliases:
                errors.append(f"{target}发声标签须统一：{name}→{aliases[name]}；不改变原句内部称呼。")
    audit = ledger.get("director_review")
    if not isinstance(audit, dict) or audit.get("sha256") != review_digest(ledger, text):
        errors.append("最终导演审查缺失或已过期：绑定实际文本、时长、人物和连接，不能沿用改动前通过结果。")
    if not isinstance(audit, dict) or any(not nonempty(audit.get(k)) for k in ("characters", "pacing", "node_arrivals", "contrast")):
        errors.append("导演审查须写明人物表演、节奏、节点到达和差异的具体结论，不能自动填pass。")
    for issue in ledger.get("continuity_errors", []) if isinstance(ledger.get("continuity_errors", []), list) else ["连续性错误记录类型无效"]:
        errors.append(f"已报告实际连续性问题：{issue}")
    return errors
