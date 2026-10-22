#!/usr/bin/env python3
"""Expand compact 2.8.2 authoring data, or print a proposed route's fingerprint."""
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path

FORMAT = "compact-2.8.2"
FIELDS = ("镜头设计", "可见动作", "可见背景", "台词与语气", "光影布光", "声音设计")


def route_digest(route):
    value = {key: route.get(key) for key in ("id", "source_images", "path")}
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def check_routes(ledger):
    """Check recorded human confirmation, never create one or infer it from time."""
    required = ledger.get("requires_route_confirmation", False)
    if not isinstance(required, bool):
        raise ValueError("requires_route_confirmation须为布尔值")
    routes = ledger.get("action_routes", [])
    if not isinstance(routes, list) or (required and not routes):
        raise ValueError("关键动作路径尚未提交用户确认：action_routes不能为空")
    images = [p.get("image") for p in ledger.get("panels", []) if isinstance(p, dict)]
    ids = set()
    for route in routes:
        if not isinstance(route, dict):
            raise ValueError("action_routes须为对象数组")
        identity, refs, path = route.get("id"), route.get("source_images"), route.get("path")
        if not isinstance(identity, str) or not identity.strip() or identity in ids:
            raise ValueError("动作路径id缺失或重复")
        ids.add(identity)
        if (not isinstance(refs, list) or not refs or any(not isinstance(v, str) or v not in images for v in refs)
                or len(set(refs)) != len(refs) or refs != sorted(refs, key=images.index)):
            raise ValueError(f"{identity}路径须按顺序关联真实原格")
        if not isinstance(path, str) or not path.strip():
            raise ValueError(f"{identity}缺少可读的动作路径")
        confirmation = route.get("user_confirmation")
        if (not isinstance(confirmation, dict) or not isinstance(confirmation.get("quote"), str)
                or not confirmation["quote"].strip()):
            raise ValueError(f"{identity}动作路径尚未获用户明确确认，不能进入第二遍写作")
        if confirmation.get("sha256") != route_digest(route):
            raise ValueError(f"{identity}路径已改变或确认指纹缺失，须重新请用户确认")


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
    args = parser.parse_args()
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8-sig"))
        if args.route_digest:
            matches = [r for r in ledger.get("action_routes", []) if isinstance(r, dict) and r.get("id") == args.route_digest]
            if len(matches) != 1:
                raise ValueError("路径id不存在或重复")
            print(route_digest(matches[0]))
        else:
            if args.expand.resolve() == args.ledger.resolve():
                raise ValueError("不能覆盖唯一创作台账；展开文件是派生产物")
            check_routes(ledger)
            result = expand(ledger)
            args.expand.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"已展开{len(result.get('shots', []))}镜；未增加任何确认或审查通过状态。")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, f"无法处理创作台账：{exc}\n")


if __name__ == "__main__":
    main()
