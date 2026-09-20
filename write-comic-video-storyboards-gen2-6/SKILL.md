---
name: write-comic-video-storyboards-gen2-6
description: Turn ordered comic panels into source-grounded, cinematic 2D animation storyboards while the relevant panels remain visually open. Use when panel composition, dialogue coverage, backgrounds, continuous action, performance, and optional Seedance combat coverage must remain auditable without lowering cinematic quality.
---

# Comic video storyboards Gen2.6

Create a source-faithful storyboard mother draft with cinematic performance and action quality. The ledger constrains and audits the work; it never replaces the open comic image as the writing source.

## Read by task

- New episode or substantial rewrite: read [references/source-grounding.md](references/source-grounding.md), [references/dialogue-coverage.md](references/dialogue-coverage.md), and [references/storyboard-format.md](references/storyboard-format.md).
- Small revision: reopen the target and adjacent panels, then read only the relevant sections of those references.
- Performance, continuous action, or cinematic polish: also read [references/cinematic-quality.md](references/cinematic-quality.md).
- Fight or complex fast action: also read [references/2d-animation-execution.md](references/2d-animation-execution.md). Its motion and effects grammar remains subordinate to source grounding.
- Paste-ready Seedance prompt or failed-generation review: read [references/seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- When modifying or forward-testing this skill: read [references/regression-cases.md](references/regression-cases.md) and run the automated tests.

Run scripts directly; inspect their code only when changing them.

## Non-negotiable quality floor

1. **Open image is authoritative.** A ledger, earlier caption, neighboring panel, plot context, or dialogue never proves a visible fact in the current panel.
2. **Write while grounded.** Every cited `source_locked` shot is written while its exact source crop is open at drafting resolution. Do not analyze the whole episode, close the images, and later generate cited shots from the ledger alone.
3. **Restore before extending.** A cited composition must become recognizably readable at its declared phase. Preserve angle, scale, placement, depth, overlap, occlusion, pose silhouette, hands/props, contact, action vector, and background hierarchy.
4. **Cinematic quality remains required.** Source grounding does not mean static paraphrase. Preserve readable performance, continuous physical causality, temporal contrast, motivated camera behavior, material response, and restrained effects wherever the source supports them.
5. **Background is a source fact.** Every shot names the physical setting, graphic field, or frame-filling surface actually visible in that framing. Never substitute the known location for the current panel's backing.
6. **Dialogue is complete and naturally timed.** Preserve every bubble's meaning, owner, kind, and order in natural Japanese. Split coverage rather than compressing or dropping speech.
7. **Added views have limited authority.** An uncited reverse, insert, environment view, or connective shot may clarify an existing beat but cannot introduce a new event, object, contact, route, identity, or result.
8. **Fifteen seconds is a soft maximum, not a target.** Keep a source-continuous action phrase in one generated clip when it fits; end short beats naturally.

## Grounded batch workflow

1. Confirm source/original and crop directories, reading order, aspect ratio, target model, output path, and color-source class. Make a 360–480 px global review set only for order, text, locations, continuity, and risk marking.
2. Work in contiguous batches of 1–3 panels. Reopen the current batch at about 720 px; escalate unusual perspective, overlap, hand/prop contact, fast action, topology, occlusion, effects, or unresolved text to original resolution.
3. While each panel is open, create or update its compact version-2 source-ledger entry. Record exact bubbles, positive visible background, phase-specific source locks, forbidden inferences, and intended shot roles. Keep the ledger factual; do not turn it into replacement prose.
4. Before closing the panel, plan dialogue coverage and immediately write its `source_locked` shot. Add `source_supported_phase` or `uncited_coverage` shots only under their declared permissions. A genuine camera change receives a new numbered shot.
5. With the same images still open, run the source-diff audit: map every visible noun and relation in the draft to current-panel evidence or an explicitly declared uncited-coverage basis; compare background, composition, hands/props, bubble mapping, and endpoint. Delete unsupported content instead of explaining why it seems plausible.
6. Validate the open batch with the version-2 ledger before advancing. Fix errors, inspect warnings, and record a manual source-audit pass for every shot. After all batches pass, run one continuity and cinematic-quality pass across clip boundaries, then validate the complete deliverables.

## Shot authority

- `source_locked`: cites one or more panels and must visibly reproduce each cited phase. The exact source images must be open while writing and auditing it. Only source-supported micro-performance and motion are allowed.
- `source_supported_phase`: extends a visible A→B relation supported by the current or adjacent panels. Record the evidence images and preserve all anchors.
- `uncited_coverage`: a separately numbered reverse, insert, reaction, environment view, or connective view. Give it a specific purpose and evidence basis; do not cite a panel whose full composition it does not match.

Do not hide a cut inside prose with `画面切到`, `再切到`, or equivalent wording. Do not call an invented composition source-locked.

## Output and validation

- Begin with `## 场景色彩基准`; add `## 非人物上色锁定` only for monochrome or partially uncolored source.
- Use `分镜N（X秒）` for ordinary shots. Use one `战斗段N（X秒·自动分镜）` only when the combat admission gate passes; never mix modes in one clip.
- Keep prose directly generatable. Include dialogue and narration with voice direction, but no sound effects, ambience, Foley, BGM, production notes, or source-analysis language.
- Generate the Chinese SRT after storyboard approval unless requested earlier.
- Report clip count, approximate runtime, reference count, structural validation, ledger validation, manual source-audit status, and absolute output paths separately.

```powershell
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder> --source-ledger <source-ledger.json> --require-source-ledger
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
python -m unittest scripts/test_validate_storyboard.py
```
