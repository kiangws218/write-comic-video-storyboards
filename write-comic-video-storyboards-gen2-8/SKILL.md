---
name: write-comic-video-storyboards-gen2-8
description: Turn ordered comic panels into source-grounded cinematic 2D-animation storyboards by inspecting each image, planning dialogue coverage and performance only where needed, and validating source fidelity without compressing the six-field output. Use for comic-to-video storyboard generation or revision where quality and token efficiency both matter.
---

# Comic video storyboards Gen2.8

Gen2.8 is an image-first selective compiler. The open panel is primary evidence; OCR, ledgers and plans are indexes, never substitute visual sources.

## Load only the needed modules

- Every storyboard: read [core-authoring.md](references/core-authoring.md) and [dialogue-performance.md](references/dialogue-performance.md).
- Premium camera/light/material finish or named production target: also read [cinematic-rendering.md](references/cinematic-rendering.md).
- Ambiguous contact, overlap, topology, fast action, color evidence or added viewpoint: also read [source-risk.md](references/source-risk.md).
- Fight/complex fast action: also read [2d-animation-execution.md](references/2d-animation-execution.md).
- Paste-ready execution prompt or failed-generation review: read [seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Skill maintenance and compatibility audits only: read [gen2-5-compatibility.md](references/gen2-5-compatibility.md) and [regression-cases.md](references/regression-cases.md).

Run validators without loading their implementation unless changing them.

## Compile loop

Work on one to three contiguous panels. Keep the exact panel open until its shot text is compared back to it. Use cached 720p proxies by default; open 1080p/original only when a decision-changing detail remains unresolved and record why.

1. Freeze source facts: composition/backing, subjects/props, overlap, pose, head/face/gaze, hand/contact, action phase and bubbles.
2. While the panel is open, assign `D` dialogue/coverage, `P` expressive performance and `G` fragile geometry only where needed.
3. Resolve ordered dialogue turns and coverage groups before camera count. Build one compact image-grounded card for each `P` shot. Escalate a `G` detail beyond 720p only when necessary.
4. Immediately write the six-field shot, then compare every noun, relation, beat and endpoint with the still-open panel.
5. Validate the small batch and fix blockers before advancing. Never reconstruct source evidence from completed prose.

## Non-negotiable outcomes

- Preserve every bubble's meaning, owner, kind, order and natural Japanese. A named speech trigger quotes exact final Japanese inside `「」`; otherwise use a generic timing node such as `重音处` or `句末`.
- Restore a cited composition at its declared phase. Polish cannot invent a person, object, hand/contact, route, event, result, hidden motive or stronger unsupported emotion.
- Preserve semantic turns first, then group adjacent short turns when one setup can carry them without hiding a cut or burying an important reaction. Similar required coverage is redesigned, not deleted.
- A panel's cited shot and derived speaker/listener/object/environment/detail coverage stay in one clip. Fifteen seconds is a hard ceiling; only a single-panel coverage unit that still exceeds it after correct splitting may be marked for manual handling.
- A `P` shot has a self-contained opening, ordered meaning-changing development, local head/face/gaze transition, supported coupling or delayed response, performer endpoint and camera landing when moving.
- Each clip cold-starts with positive current pose, orientation, counts, contact, backing, light, gaze direction and stable labels. No cross-shot pointers or negative controls.
- Save tokens through routing, 720p inspection and mechanical validation—not by shortening the six-field storyboard.

## Delivery

- Ordinary shots use `分镜N（X秒）`; eligible combat may use one `战斗段N（X秒·自动分镜）`. Every real cut is numbered.
- Field order is `【镜头设计】`, `【可见动作】`, `【可见背景】`, `【台词与语气】`, `【光影布光】`, `【声音设计】`.
- `【镜头设计】` owns angle/axis, scale/focal length, crop/layout, depth/overlap/negative space, focus, camera move and landing. `【可见动作】` owns only time-varying performance and endpoints. `【可见背景】` owns only renderable backing.
- Preserve environment sound, Foley, breath, silence and dialogue treatment in `【声音设计】`; do not add BGM, score or theme music.
- Structural/source/performance blockers stop delivery. Heuristic advisories may remain only with a per-shot image-based disposition.

```powershell
python scripts/build_analysis_proxies.py <panel-folder>
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <proxy-folder> --source-ledger <source-ledger-v3.json> --require-source-ledger
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
python -m unittest discover -s scripts -p "test_*.py"
```

Report clip count, runtime, reference count, blocking validation, advisories by class, manual-overflow items, source audit, rule-input size and absolute output paths.
