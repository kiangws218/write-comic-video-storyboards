#!/usr/bin/env python3
"""Expand compact 2.8.2 data, or fingerprint a human-facing proposal (never approve)."""
from copy import deepcopy
from decimal import Decimal, InvalidOperation
import argparse
import hashlib
import json
import re
from pathlib import Path

FORMAT = "compact-2.8.2"
FIELDS = ("镜头设计", "可见动作", "可见背景", "台词与语气", "光影布光", "声音设计")


def duration_seconds(value):
    """Seconds on the half-second grid; no rounding, truncation or new ledger fields."""
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError("时长须为大于0的0.5秒整数倍")
    try:
        number = Decimal(str(value))
    except InvalidOperation:
        raise ValueError("时长须为大于0的0.5秒整数倍") from None
    if not number.is_finite() or number <= 0 or number * 2 != (number * 2).to_integral_value():
        raise ValueError("时长须为大于0的0.5秒整数倍")
    return float(number)


def format_seconds(value):
    return f"{duration_seconds(value):g}"


# Only line-leading ranges in the existing action field are structured timing.
# Ordinary prose (including a one-frame smear) remains free text.
ACTION_RANGE = re.compile(
    r'^\s*(\d+(?:\.\d+)?)\s*(?:s\s*)?-\s*(\d+(?:\.\d+)?)\s*s\s*[：:]\s*(\S.*)$', re.I)
RANGE_START = re.compile(r'^\s*[+-]?\d+(?:\.\d+)?\s*(?:s\s*)?[-–—~～]', re.I)


def action_timeline_errors(text, duration, label="可见动作"):
    """Validate optional local ranges, without interpreting acting or storing a copy."""
    if not isinstance(text, str):
        return []
    errors, intervals = [], []
    for line in text.splitlines():
        if not RANGE_START.match(line):
            continue
        match = ACTION_RANGE.fullmatch(line)
        if not match:
            errors.append(f"{label}时间段格式须为0-0.5s：具体画面，且描述不能为空。")
            continue
        start, end = map(float, match.groups()[:2])
        if not all(Decimal(str(v)).is_finite() for v in (start, end)):
            errors.append(f"{label}时间段须为有限数值。")
            continue
        if start % .5 or end % .5 or end <= start:
            errors.append(f"{label}时间段须递增且以0.5秒为步长。")
            continue
        intervals.append((start, end))
    if not intervals:
        return errors
    try:
        length = duration_seconds(duration)
    except ValueError:
        return errors + [f"{label}所属镜头时长无效。"]
    previous = 0
    for start, end in intervals:
        if start != previous:
            errors.append(f"{label}时间段须从0开始连续排列，不能留空、重叠或倒序。")
        if end > length:
            errors.append(f"{label}时间段越过镜头时长{length:g}秒。")
        previous = end
    if previous != length:
        errors.append(f"{label}最后时间段须结束于镜头时长{length:g}秒。")
    return errors


def route_digest(route):
    return proposal_digest(route, "path")


def scene_digest(scene):
    return proposal_digest(scene, "baseline")


def addition_digest(addition):
    return proposal_digest(addition, "proposal", extra_keys=("route_id",))


def proposal_digest(proposal, text_key, extra_keys=()):
    value = {key: proposal.get(key) for key in ("id", "source_images", text_key) + extra_keys}
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def check_routes(ledger):
    """Check recorded human confirmation, never create one or infer it from time."""
    check_proposals(ledger, "action_routes", "requires_route_confirmation", "path", "动作路径")
    for route in ledger.get("action_routes", []):
        if "performance_mode" in route and route["performance_mode"] != "action":
            raise ValueError(f"{route['id']}的performance_mode仅支持action；日常不登记该标记")


def check_proposals(ledger, collection, required_key, text_key, label, *, extra_keys=(),
                    pending_stage="不能进入第二遍写作"):
    """Shared confirmation mechanics; the caller still supplies real human evidence."""
    required = ledger.get(required_key, False) if required_key else False
    if not isinstance(required, bool):
        raise ValueError(f"{required_key}须为布尔值")
    proposals = ledger.get(collection, [])
    if not isinstance(proposals, list) or (required and not proposals):
        raise ValueError(f"{label}尚未提交用户确认：{collection}不能为空")
    images = [p.get("image") for p in ledger.get("panels", []) if isinstance(p, dict)]
    ids = set()
    for proposal in proposals:
        if not isinstance(proposal, dict):
            raise ValueError(f"{collection}须为对象数组")
        identity, refs, text = proposal.get("id"), proposal.get("source_images"), proposal.get(text_key)
        if not isinstance(identity, str) or not identity.strip() or identity in ids:
            raise ValueError(f"{label}id缺失或重复")
        ids.add(identity)
        if (not isinstance(refs, list) or not refs or any(not isinstance(v, str) or v not in images for v in refs)
                or len(set(refs)) != len(refs) or refs != sorted(refs, key=images.index)):
            raise ValueError(f"{identity}{label}须按顺序关联真实原格")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"{identity}缺少可读的{label}")
        confirmation = proposal.get("user_confirmation")
        if (not isinstance(confirmation, dict) or not isinstance(confirmation.get("quote"), str)
                or not confirmation["quote"].strip()):
            raise ValueError(f"{identity}{label}尚未获用户明确确认，{pending_stage}")
        if confirmation.get("sha256") != proposal_digest(proposal, text_key, extra_keys):
            raise ValueError(f"{identity}{label}已改变或确认指纹缺失，须重新请用户确认")


def check_action_additions(ledger):
    """Validate explicit additional-action grants; do not classify creative prose."""
    shots = ledger.get("shots", [])
    if "action_additions" not in ledger and not any(
            isinstance(shot, dict) and "action_addition_ids" in shot
            for shot in (shots if isinstance(shots, list) else [])):
        return  # Preserve the validation behavior of ledgers without this extension.
    check_proposals(ledger, "action_additions", None, "proposal", "新增动作提案",
                    extra_keys=("route_id",), pending_stage="不能进入新增动作正式写作")
    routes = {route["id"]: route for route in ledger.get("action_routes", [])}
    additions = {item["id"]: item for item in ledger.get("action_additions", [])}
    for identity, addition in additions.items():
        route_id = addition.get("route_id")
        route = routes.get(route_id) if isinstance(route_id, str) else None
        if route is None or route.get("performance_mode") != "action":
            raise ValueError(f"{identity}须关联已确认且performance_mode为action的动作路径")
        if not set(addition["source_images"]).issubset(route["source_images"]):
            raise ValueError(f"{identity}新增动作范围超出所属动作路径")
    if not isinstance(shots, list) or any(not isinstance(shot, dict) for shot in shots):
        raise ValueError("shots须为对象数组")
    for shot in shots:
        if "action_addition_ids" not in shot:
            continue
        ids = shot["action_addition_ids"]
        target = shot.get("target", "未知镜头")
        if (not isinstance(ids, list) or not ids or
                any(not isinstance(identity, str) or identity not in additions for identity in ids)
                or len(set(ids)) != len(ids)):
            raise ValueError(f"{target}的action_addition_ids须唯一引用已确认的新增动作提案")
        refs = shot.get("source_images") if shot.get("role") == "source_locked" else shot.get("derived_from")
        images = {panel.get("image") for panel in ledger.get("panels", [])
                  if isinstance(panel, dict) and isinstance(panel.get("image"), str)}
        if (not isinstance(refs, list) or not refs or
                any(not isinstance(ref, str) or ref not in images for ref in refs)):
            raise ValueError(f"{target}引用新增动作提案时须关联真实原格范围")
        for identity in ids:
            allowed = set(additions[identity]["source_images"])
            if not allowed.intersection(refs):
                raise ValueError(f"{target}与新增动作提案{identity}的原格范围无交集")
        # A continuous shot may also realize original nodes outside the added
        # action's scope. Intersection binds the grant; semantics remain human review.


def check_scene_baselines(ledger):
    check_proposals(ledger, "scene_baselines", "requires_scene_confirmation", "baseline", "场景基准")
    if not ledger.get("scene_baselines"):
        return  # Old ledgers stay readable; this does not attest historical approval.
    ids = {scene["id"] for scene in ledger["scene_baselines"]}
    compact = ledger.get("authoring_format") == FORMAT
    initial = ledger.get("initial_state", {}) if compact else {}
    shots = ledger.get("shots", [])
    if not isinstance(initial, dict) or not isinstance(shots, list) or any(not isinstance(s, dict) for s in shots):
        raise ValueError("场景基准关联须有对象状态和镜头数组")
    active = initial.get("场景基准")
    for shot in shots:
        keys = ("state_changes",) if compact else ("state_in", "state_out")
        if any(not isinstance(shot.get(key, {}), dict) for key in keys):
            raise ValueError("场景基准须关联对象状态")
        if compact:
            active = shot.get("state_changes", {}).get("场景基准", active)
            values = [active]
        else:
            values = [shot.get(key, {}).get("场景基准") for key in ("state_in", "state_out")]
        if any(not isinstance(value, str) or value not in ids for value in values):
            raise ValueError(f"{shot.get('target', '未知镜头')}须通过现有状态关联已确认场景基准")


def check_confirmations(ledger):
    check_routes(ledger)
    check_scene_baselines(ledger)
    check_action_additions(ledger)


def expand(ledger):
    """Pure conversion. No invented actions, observations, cards, or approvals."""
    if not isinstance(ledger, dict):
        raise ValueError("台账根须为对象")
    if "authoring_format" not in ledger:
        return ledger
    if ledger["authoring_format"] != FORMAT:
        raise ValueError("未知authoring_format")
    if ledger.get("version") != 3 or ledger.get("skill_version") != "2.8.2":
        raise ValueError("compact仅适用于V3、2.8.2")
    result = deepcopy(ledger)
    result.pop("authoring_format")
    state = result.pop("initial_state", None)
    if not isinstance(state, dict) or not state or any(isinstance(v, (dict, list)) for v in state.values()):
        raise ValueError("compact须有非空扁平initial_state")
    shots = result.get("shots")
    if not isinstance(shots, list) or any(not isinstance(s, dict) for s in shots):
        raise ValueError("shots须为对象数组")
    targets = [s.get("target") for s in shots]
    if any(not isinstance(t, str) or not t for t in targets) or len(set(targets)) != len(targets):
        raise ValueError("target缺失或重复")
    if result.get("performance"):
        raise ValueError("compact表演卡只写镜头performance，不混用根performance")
    result["performance"] = []
    for shot in shots:
        if "state_in" in shot or "state_out" in shot or "neighbor_contrast" in shot:
            raise ValueError("compact不混用完整状态／neighbor_contrast；保留单一事实源")
        changes = shot.pop("state_changes", {})
        if not isinstance(changes, dict) or any(isinstance(v, (dict, list)) for v in changes.values()):
            raise ValueError("state_changes须为扁平对象，空对象表示状态未改变")
        shot["state_in"] = dict(state)
        state = {**state, **changes}
        shot["state_out"] = dict(state)
        performance = shot.pop("performance", None)
        if performance is not None:
            if not isinstance(performance, dict) or "target" in performance:
                raise ValueError("镜头performance须为无重复target的对象")
            result["performance"].append({"target": shot["target"], **performance})
    cuts = result.pop("cuts", [])
    if not isinstance(cuts, list):
        raise ValueError("cuts须为数组")
    pairs = set()
    for cut in cuts:
        if not isinstance(cut, dict):
            raise ValueError("cut须为对象")
        before, after = cut.get("from"), cut.get("to")
        if before not in targets or after not in targets or targets.index(after) != targets.index(before) + 1:
            raise ValueError("cuts只能登记最终实际相邻镜头，重新剪辑后须更新")
        if (before, after) in pairs:
            raise ValueError("同一切点只写一份差异")
        pairs.add((before, after))
        details = cut.get("changes")
        if not isinstance(details, list) or not details:
            raise ValueError("每个登记切点至少有一项显著差异")
        resolved = []
        for change in details:
            if not isinstance(change, dict):
                raise ValueError("切点差异须为对象")
            target, field = change.get("shot"), change.get("field")
            if target not in (before, after) or field not in FIELDS:
                raise ValueError("差异须引用本切点一侧的实际六字段")
            value = shots[targets.index(target)].get("fields", {}).get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError("差异引用字段为空")
            resolved.append({"dimension": change.get("dimension"), "description": change.get("description"),
                             "excerpt": value})
        for target, direction, other in ((before, "next", after), (after, "previous", before)):
            shot = shots[targets.index(target)]
            if shot.get("role") != "source_locked":
                shot.setdefault("neighbor_contrast", {})[direction] = {"target": other, "changes": deepcopy(resolved)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--expand", type=Path, help="Write a derived validator-compatible ledger; no approvals added")
    group.add_argument("--route-digest", help="Print fingerprint for the proposed route id, without approving")
    group.add_argument("--scene-digest", help="Print fingerprint for the proposed scene id, without approving")
    group.add_argument("--addition-digest", help="Print fingerprint for the additional-action proposal id, without approving")
    args = parser.parse_args()
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8-sig"))
        if args.route_digest or args.scene_digest or args.addition_digest:
            if args.route_digest:
                key, identity, digest = "action_routes", args.route_digest, route_digest
            elif args.scene_digest:
                key, identity, digest = "scene_baselines", args.scene_digest, scene_digest
            else:
                key, identity, digest = "action_additions", args.addition_digest, addition_digest
            matches = [r for r in ledger.get(key, []) if isinstance(r, dict) and r.get("id") == identity]
            if len(matches) != 1:
                raise ValueError("提案id不存在或重复")
            print(digest(matches[0]))
        else:
            if args.expand.resolve() == args.ledger.resolve():
                raise ValueError("不能覆盖唯一创作台账；展开文件是派生产物")
            check_confirmations(ledger)
            result = expand(ledger)
            args.expand.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"已展开{len(result.get('shots', []))}镜；未增加任何确认或审查通过状态。")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, f"无法处理创作台账：{exc}\n")


if __name__ == "__main__":
    main()
