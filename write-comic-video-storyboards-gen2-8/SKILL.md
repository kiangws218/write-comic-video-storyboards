---
name: write-comic-video-storyboards-gen2-8
description: Turn ordered comic panels into source-grounded cinematic 2D-animation storyboards by inspecting each image, routing only risky shots through compact dialogue, performance, or geometry plans, and validating source fidelity and first-pass acting quality. Use for comic-to-video storyboard generation or revision where prompt quality and token efficiency both matter.
---

# Comic video storyboards Gen2.8

Gen2.8 is an image-first selective compiler. The open panel is always primary evidence. OCR, ledgers, captions, summaries, and performance cards are indexes or temporary plans; never close the image and render storyboard prose from those texts.

## Route only what the shot needs

- Every storyboard: read [core-authoring.md](references/core-authoring.md), [dialogue-performance.md](references/dialogue-performance.md), and the compact [Gen2.5 non-regression contract](references/gen2-5-compatibility.md).
- Premium camera/light/material finish or named style target: also read [cinematic-rendering.md](references/cinematic-rendering.md).
- Ambiguous hand/prop/contact, overlap, topology, fast action, mixed color evidence, or added viewpoint: also read [source-risk.md](references/source-risk.md).
- Fight/complex fast action: also read [2d-animation-execution.md](references/2d-animation-execution.md).
- Paste-ready prompt or failed-generation review: read [seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Skill maintenance/forward tests only: read [regression-cases.md](references/regression-cases.md).

Run validators without loading their implementation unless changing it.

## Image-first compile loop

Work on one to three contiguous panels. Keep each cited image open from evidence extraction through final comparison. Inspect a cached 720p proxy by default; open the 1080p/original asset only when text, identity, hand/contact, overlap, topology, or another decision-changing fact is not reliable at 720p, and record the reason in the ledger.

1. Freeze decision-changing source facts: composition/backing, visible subjects/props, overlap, pose, head/face/gaze, hand/contact, action phase, and bubbles.
2. Assign risk flags: `D` dialogue/coverage, `P` expressive performance, `G` fragile geometry. Low-risk shots need none.
3. Resolve `D` coverage first. For `P`, make one compact performance card from the open image. For `G`, inspect the 720p proxy first, then escalate only unresolved fragile relations to original resolution and freeze them.
4. Immediately write the six-field shot. Never create episode-wide cards first.
5. Compare every noun, relation, beat, and endpoint with the still-open image; validate the small batch and fix blocking errors before continuing.

Create source evidence and risk decisions before prose. Never generate a successful-looking ledger by copying the completed storyboard back into source locks, bubble rows, flags, or performance cards.

## Invariants

- Preserve every bubble's meaning, owner, kind, order, and natural Japanese. A named dialogue trigger must quote exact final Japanese inside `「」`; otherwise use `重音处/句末`, never a Chinese semantic paraphrase.
- Restore the cited composition before extending it. Polish cannot add a person, prop, hand, contact, route, event, result, hidden motive, or stronger unsupported emotion.
- A `P` shot renders its card into an opening state, ordered semantic developments, local face/head/gaze transition, coupled hand/prop/weight/listener or delayed response, performer endpoint, and camera landing. Cropped anatomy uses a visible substitute.
- Many related micro-actions may fit three seconds; unrelated complete actions may not. Do not collapse causal acting into a gesture list or inflate a neutral panel.
- Adjacent numbered shots never formally cite the same comic panel. A later genuine cut is uncited coverage and changes at least two meaningful visual/dramatic dimensions; otherwise merge it into the cited shot.
- Treat every comic panel and all shots derived from it as one coverage unit: its cited shot and any uncited reverse/insert/reaction stay in the same clip. Do not start a new clip merely to continue dialogue or add a near-identical crop from that panel.
- Every clip cold-starts with positive current pose, orientation, counts, contact, backing, light, gaze direction, and stable labels. No cross-shot pointers or negative controls.
- Save tokens through routing and mechanical extraction, never by shortening the six-field storyboard.

## Delivery

- Ordinary shots use `分镜N（X秒）`; eligible combat uses one `战斗段N（X秒·自动分镜）`. Keep a clip within 15 seconds when practical; every real cut gets a number.
- Field order is `【镜头设计】`, `【可见动作】`, `【可见背景】`, `【台词与语气】`, `【光影布光】`, `【声音设计】`. `【镜头设计】` exclusively carries shooting angle/axis, scale/focal length, crop and subject layout, depth/overlap/negative space, focus, camera move and landing. `【可见动作】` carries only time-varying pose, head/face/gaze, hands/props, weight, secondary motion and endpoints; do not restate static composition there. `【可见背景】` contains only physical backing, an intentional graphic field, or a frame-filling surface; speech-bubble/page/gutter whitespace is never scenery. Sound combines ambience, Foley, breath/silence, dialogue treatment, and synchronization once.
- Cite one source normally. If one numbered shot legitimately merges several same-setup panels, do not stack references above the fields: bind each image to a separate phase bullet inside `【镜头设计】` (`参考 [image]（起幅/发展/结果）：...`) with its panel-specific crop/layout and the shared camera path. Use matching phase bullets in `【可见动作】` without repeating composition. Split the shot when camera setup, background, axis, or action continuity changes.
- Keep the ledger compact: mechanically derive mappings/excerpts where possible; model only source locks, evidence, risk flags, and `P` cards.
- Structural errors and `P`-performance errors block delivery. Repeated formal citations are errors. Other advisories may remain only with a per-shot image-based disposition; a blanket waiver or `0 errors` summary is not a quality verdict.

```powershell
python scripts/build_analysis_proxies.py <panel-folder>
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder> --source-ledger <source-ledger.json> --require-source-ledger
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
python -m unittest discover -s scripts -p "test_*.py"
```

Report clip count, approximate runtime, reference count, blocking validation, advisories by class, manual source audit, and absolute output paths.
