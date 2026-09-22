---
name: write-comic-video-storyboards-gen2-7
description: Turn ordered comic panels into source-grounded, cinematic 2D-animation storyboards with detailed acting, camera, lighting, dialogue, and sound while loading a compact task-specific rule set. Use for comic-to-video storyboard writing and revision where panel fidelity and prompt quality must remain auditable.
---

# Comic video storyboards Gen2.7

Gen2.7 preserves Gen2.6 output density and validation while reducing instruction context. Read only the modules routed below; never load every reference by default.

## Route the task

- Every storyboard or substantial rewrite: read [references/core-authoring.md](references/core-authoring.md) and [references/dialogue-performance.md](references/dialogue-performance.md).
- Camera, lighting, atmosphere, materials, studio/work/director references, or premium finish: also read [references/cinematic-rendering.md](references/cinematic-rendering.md).
- Ambiguous hands/props, overlap, topology, fast action, mixed color evidence, or an added viewpoint: also read [references/source-risk.md](references/source-risk.md).
- Fight or complex fast action: also read [references/2d-animation-execution.md](references/2d-animation-execution.md).
- Paste-ready Seedance prompt or failed-generation review: read [references/seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Skill maintenance and forward tests only: read [references/regression-cases.md](references/regression-cases.md). Do not load it during ordinary generation.

Run scripts directly. Inspect their implementation only when changing them.

## Quality floor

1. Write each cited shot while its exact panel is open at drafting resolution; the ledger indexes evidence but never replaces the image.
2. Restore the cited composition before extending it: preserve angle, scale, placement, depth, overlap, occlusion, pose silhouette, visible hands/props, contact, action vector, background class, and declared phase.
3. Preserve every bubble's meaning, owner, kind, order, and natural Japanese delivery. Set duration from speech and supported action, not from a preselected container.
4. Make performance a supported causal chain, not a gesture quota: stimulus/semantic beat → attention and head/face change → local expression or task-related hand/weight response → delayed motion → explicit endpoint.
5. Keep camera, focus, lighting, atmosphere, materials, and sound concrete and motivated. Polish may develop presentation but cannot add a fact, event, hidden motive, contact, route, or result.
6. Every generated clip must cold-start independently with positive current pose, orientation, people/counts, contact, background, light, gaze direction, and stable prop labels. Never rely on an earlier clip.
7. Retain the full seven-field output. Gen2.7 optimizes loaded rules, not storyboard detail.

## Compact workflow

1. Confirm ordered source crops, originals, references, aspect ratio, target model, output path, and color-source class. Use a small contact sheet only for order, scene recognition, continuity, and risk marking.
2. Work in contiguous batches of one to three panels. Open them at about 720 px; inspect original resolution for small text or risky geometry.
3. While each panel is open, record only decision-changing ledger facts: bubble mapping, positive background excerpt, composition/subject/contact locks, phase, shot role, evidence, and forbidden inferences.
4. Plan dialogue coverage and immediately write the corresponding shot. Use `source_locked`, `source_supported_phase`, or `uncited_coverage` according to `core-authoring.md`.
5. Compare every visible noun and relation in the draft with the same open image. Delete unsupported additions rather than explaining them with negative prompts.
6. Add supported performance, sound, camera, focus, lighting, atmosphere, and material response. Complete the current batch before opening the next.
7. Run the validator per batch and at delivery. Fix errors; inspect every warning. Finish with manual source, dialogue, clip-cold-start, cross-boundary, performance-diversity, sound, and cinematic audits.

## Output and validation

- Begin with `## 场景色彩基准`; add `## 非人物上色锁定` only when the source is monochrome or partly uncolored.
- Use `分镜N（X秒）` for ordinary shots. Use one `战斗段N（X秒·自动分镜）` only when the combat admission gate passes; never mix both timing modes in one clip.
- Every ordinary shot uses, in order: `场景环境`, `环境音`, `镜头设计`, `可见动作`, `台词与语气`, `光影布光`, `声音设计`.
- A real hard cut, reverse, insert, reaction, or changed viewpoint receives a new numbered shot. Continuous phases in one camera setup remain one shot.
- Keep each clip within 15 seconds when practical, but end with the beat rather than padding or cutting an unfinished physical phrase.
- Generate the Chinese SRT after storyboard approval unless requested earlier.
- Report clip count, approximate runtime, reference count, structural/ledger validation, manual source-audit status, and absolute output paths.

```powershell
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder> --source-ledger <source-ledger.json> --require-source-ledger
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
python -m unittest scripts/test_validate_storyboard.py
```
