---
name: write-comic-video-storyboards-gen2
description: Turn ordered comic, manga, manhua, or webtoon originals and crops into source-faithful, production-ready 2D animation storyboards and optional Seedance prompts. Use for original-panel preservation, missing-text recovery, preserve/split/fill/merge analysis, natural dialogue timing, reusable environments, adult/R18 master plus platform-safe replacements, combat prompting, validation, or generation retakes.
---

# Comic video storyboards Gen2

Produce a detailed storyboard mother draft. Create a separate compressed Seedance execution draft only when requested. The comic and approved mother draft remain authoritative.

## Resource routing

Read only what the task needs:

- New full episode or substantial rewrite: read [references/storyboard-spec.md](references/storyboard-spec.md).
- Ambiguous ordering, long/multi-speaker panels, or requested analysis artifact: also read [references/pre-analysis-gen2.md](references/pre-analysis-gen2.md).
- Directly pasteable Seedance prompts or failed-generation review: read [references/seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Fight or complex fast action: read [references/2d-animation-execution.md](references/2d-animation-execution.md).
- Small revision: read only the target clip, adjacent clips, cited panels, and the relevant section of `storyboard-spec.md`; do not reload the episode or every reference.

Do not read scripts unless modifying them. Run validation scripts directly.

## Workflow

1. Establish source/original and crop directories, reading order, output path, dialogue language, target model, aspect ratio, and the default 15-second soft ceiling. Use generic character labels until references exist. Add no BGM.
2. Inventory images in natural order. Inspect all panels once at overview scale; reopen only cited, text-critical, ambiguous, or visually complex panels at full resolution. Check the current panel plus neighbors; expand to five only when ambiguity remains.
3. Build a compact internal ledger containing: crop↔original, location, characters, visible action/pose, dialogue, props, entering/exiting state, 保格/拆格/补格/并格, behavior type (state/action; reaction as an optional tag), and ambiguity. Do not output full analysis tables unless requested or needed for review.
4. For every 保格 candidate, lock an original-panel reproduction point: framing/viewpoint, subject placement, pose, left/right hand–prop assignment, expression/gaze, and layer hierarchy. The generated shot must clearly pass through and briefly hold it.
5. Time dialogue before camera flourishes. Include breath, hesitation, pauses, interruption, and listener reaction. Split rather than accelerate. Use continuous integer timecodes.
6. Cluster locations and choose the lightest useful environment deliverable. Give simple or one-off locations a compact environment prompt for direct use without a reference image; create a structural line-art reference only for recurring spatially complex locations. Put `环境参考：【名称】` once below the clip title only when an environment image is actually used. Describe the distinct visible background in each shot.
7. Draft each block in this order: optional `分镜参考`; concise `景别`; concise `构图`; concise `运镜`; detailed `画面内容`. The first three fields define the shot's base state. Put any timed change of scale, composition, or camera—especially multi-stage camera movement—inside `画面内容`. End on a reproducible pose or object state.
8. Validate, then manually audit source fidelity and reference suitability. For revisions, patch only affected clips and their analysis rows unless a story change propagates farther.

## Non-negotiable rules

### Source and reference fidelity

- Cite a crop only when the full target composition matches it.
- Preserve the reproduction point before enriching motion. Added action may occur before, during, or after it; if it changes a locked anchor, make a separate uncited 补格 shot.
- Source fidelity outranks motion density. Animate preserved panels with actions such as chewing, swallowing, gaze shifts, grip tension, prop sway, paper movement, wind, light, and return to pose.
- Do not turn dialogue concepts into replacement props or scenes. If the panel shows left-hand skewer and right-hand map, a line about money does not authorize coins.
- Use originals to recover omitted text and context; use crop filenames for formal references.
- Determine camera angle from camera position and perspective, never from where the character looks. A raised or lowered head does not itself imply a low or high camera.
- Before citing a crop, recheck base scale/angle, subject placement and overlap, pose/gaze, hands/props, and layer hierarchy. Do not put off-panel props or a planned later camera state into the cited panel's base fields.

### Timing, structure, and sound

- Treat 15 seconds as a soft maximum, not a target. Short completed beats are valid.
- Keep one complete sentence inside one clip and give each speaker natural time.
- Use hard cuts by default; reserve special transitions for genuine story events.
- After every spoken or narrated sentence, add full-width parentheses with timbre, tone, emotion, and useful pace/stress notes.
- Use dialogue, narration, ambience, Foley, impacts, breath, and silence only; never add BGM or musical cues.

### Behavior type, visual fullness, and prompt purity

- Classify each beat before adding motion. **State** sustains travel, waiting, rest, observation, vigilance, atmosphere, or another ongoing condition; enrich it selectively with the existing repeated action, gaze/expression, prop/cloth motion, medium feedback, and environment/light, without forcing a complete event chain. **Action** changes an object or story state; expand it as needed through setup → execution → response → result → settled endpoint. Add **reaction** as an optional tag to either type for perception and emotional response. For mixed beats, name a primary and secondary type and preserve both source functions.
- Give action beats a visible arc. Let state beats remain controlled and continuous rather than filling every stage of that arc.
- For invented content, specify relevant color, material, finish, form, quantity, placement, motion order, and final state.
- Use positive observable instructions. Keep asset decisions, editorial notes, hidden estimates, and partial-only references outside timed prompts.
- Keep 2D language consistent: hand-drawn line art, cel-shaded characters, layered backgrounds; avoid photographic camera jargon unless requested.

### Environments

- Simple or one-off location: provide a compact environment prompt describing only visible layout, materials, atmosphere/weather, light, and a few distinctive irregular details; use it directly without generating a reference image.
- Recurring spatially complex location: provide high-oblique structural line art plus descriptive rendering language. Do not generate an overhead plan.
- Environment prompts contain only physical space, materials, natural traces, weather, and light—no character/creature names, assigned routes, staging zones, or narrative functions.
- Make natural terrain irregular and accumulated; make built spaces worn, nonuniform, and plausibly used.
- One-off locations receive complete visible background description inside the shot and no separate environment asset.

### Adult/R18 plus platform-safe delivery

When both versions are requested:

1. Write the complete source-faithful adult/R18 master first without deleting, sanitizing, euphemizing, or overwriting source content.
2. Append `# 附录：平台安全替换稿`.
3. Add complete replacements only for affected clips as `## 【平台安全替换·片段N】标题`.
4. Each replacement must be directly generatable and preserve story function, timing, continuity, and non-adult source anchors.
5. Treat it as explicit content adaptation, never moderation bypass; use no code words or approval guarantees.
6. Keep any standalone approved safe draft unchanged unless asked to revise it.

## Optional Seedance execution draft

Compile from the approved mother draft; do not rewrite the story. Preserve timing, dialogue, shot purpose, reference roles, causality, endpoint, and fragile anchors. Remove duplicated static detail and empty quality adjectives first. Use the actual input limit; target 1900 characters only for a 2000-character field. Retain the no-BGM rule.

## Validation

```powershell
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder>
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
```

Fix all errors. Report clip count, approximate runtime, reference count, validation result, and absolute output paths.

For a failed generation, classify keep / fix in post / local edit / reroll / rewrite / split. Change one meaningful variable per retry; after the same failure twice, change wording or structure rather than rerolling identically.
