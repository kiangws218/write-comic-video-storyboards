---
name: write-comic-video-storyboards-gen2-8
description: Turn ordered comic panels into source-grounded cinematic 2D-animation storyboards by inspecting each image, routing only risky shots through compact dialogue, performance, or geometry plans, and validating source fidelity and first-pass acting quality. Use for comic-to-video storyboard generation or revision where prompt quality and token efficiency both matter.
---

# Comic video storyboards Gen2.8

Gen2.8 is an image-first selective compiler. The open panel is always primary evidence. OCR, ledgers, captions, summaries, and performance cards are indexes or temporary plans; never close the image and render storyboard prose from those texts.

## Route only what the shot needs

- Every storyboard: read [core-authoring.md](references/core-authoring.md) and [dialogue-performance.md](references/dialogue-performance.md).
- Premium camera/light/material finish or named style target: also read [cinematic-rendering.md](references/cinematic-rendering.md).
- Ambiguous hand/prop/contact, overlap, topology, fast action, mixed color evidence, or added viewpoint: also read [source-risk.md](references/source-risk.md).
- Fight/complex fast action: also read [2d-animation-execution.md](references/2d-animation-execution.md).
- Paste-ready prompt or failed-generation review: read [seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Skill maintenance/forward tests only: read [regression-cases.md](references/regression-cases.md).

Run validators without loading their implementation unless changing it.

## Image-first compile loop

Work on one to three contiguous panels. Keep each cited image open from evidence extraction through final comparison.

1. Freeze decision-changing source facts: composition/backing, visible subjects/props, overlap, pose, head/face/gaze, hand/contact, action phase, and bubbles.
2. Assign risk flags: `D` dialogue/coverage, `P` expressive performance, `G` fragile geometry. Low-risk shots need none.
3. Resolve `D` coverage first. For `P`, make one compact performance card from the open image. For `G`, inspect original resolution and freeze the fragile relation.
4. Immediately write the six-field shot. Never create episode-wide cards first.
5. Compare every noun, relation, beat, and endpoint with the still-open image; validate the small batch and fix blocking errors before continuing.

## Invariants

- Preserve every bubble's meaning, owner, kind, order, and natural Japanese. A named dialogue trigger must quote exact final Japanese inside `「」`; otherwise use `重音处/句末`, never a Chinese semantic paraphrase.
- Restore the cited composition before extending it. Polish cannot add a person, prop, hand, contact, route, event, result, hidden motive, or stronger unsupported emotion.
- A `P` shot renders its card into an opening state, ordered semantic developments, local face/head/gaze transition, coupled hand/prop/weight/listener or delayed response, performer endpoint, and camera landing. Cropped anatomy uses a visible substitute.
- Many related micro-actions may fit three seconds; unrelated complete actions may not. Do not collapse causal acting into a gesture list or inflate a neutral panel.
- Every clip cold-starts with positive current pose, orientation, counts, contact, backing, light, gaze direction, and stable labels. No cross-shot pointers or negative controls.
- Save tokens through routing and mechanical extraction, never by shortening the six-field storyboard.

## Delivery

- Ordinary shots use `分镜N（X秒）`; eligible combat uses one `战斗段N（X秒·自动分镜）`. Keep a clip within 15 seconds when practical; every real cut gets a number.
- Field order is `【场景环境】`, `【镜头设计】`, `【可见动作】`, `【台词与语气】`, `【光影布光】`, `【声音设计】`. Background contains backing only; sound combines ambience, Foley, breath/silence, dialogue treatment, and synchronization once.
- Keep the ledger compact: mechanically derive mappings/excerpts where possible; model only source locks, evidence, risk flags, and `P` cards.
- Structural errors and `P`-performance errors block delivery. Repeated-reference/multi-speaker advisories may remain only after image-based review confirms a real coverage change or supported shared composition.

```powershell
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder> --source-ledger <source-ledger.json> --require-source-ledger
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
python -m unittest scripts/test_validate_storyboard.py
```

Report clip count, approximate runtime, reference count, blocking validation, advisories by class, manual source audit, and absolute output paths.
