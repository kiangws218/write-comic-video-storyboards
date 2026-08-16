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

1. Establish source/original and crop directories, reading order, output path, dialogue language, target model, aspect ratio, and the default 15-second soft ceiling. Use generic character labels until references exist. Do not write BGM, ambience, Foley, or other sound-effect instructions in storyboard blocks.
2. Inventory images in natural order. Create non-destructive review copies at about 540 pixels wide while preserving aspect ratio and leaving source files unchanged. Inspect all panels once through contact sheets or these copies. For small text, hand–prop assignment, facial detail, complex action, or ambiguity, create or open a roughly 720-pixel copy; use full resolution only when 720 pixels remains insufficient. Do not repeatedly load high-resolution panels already understood. Check the current panel plus neighbors; expand to five only when ambiguity remains.
3. Build a compact internal ledger containing: crop↔original, location, characters, visible action/pose, dialogue, props split into `visible in current crop` versus `carried/existing off-frame`, entering/exiting state, 保格/拆格/补格/并格, behavior type (state/action; reaction as an optional tag), and ambiguity. For a risky action beat, also record the source-visible phase and the permitted action envelope. Do not output full analysis tables unless requested or needed for review.
4. For every 保格 candidate, identify the original-panel reproduction point: vertical camera angle, horizontal viewing direction, shot scale, subject placement, pose, left/right hand–prop assignment, expression/gaze, and layer hierarchy. The cited image may be the opening, middle, or endpoint of the timed block; reproduce it at its designated phase rather than forcing it to be the first frame.
5. Time dialogue before camera flourishes. Include hesitation, pauses, interruption, and listener reaction when useful; do not add sound-effect instructions. If the listener is not visible in the preserved speaker composition, use either a separate uncited shot-reverse-shot block or an explicitly marked hard-cut sub-shot inside the same timed block; never pull the listener into the cited frame. Split rather than accelerate. Use continuous integer timecodes.
6. Cluster locations and choose the lightest useful environment deliverable. Give simple or one-off locations a compact environment prompt for direct use without a reference image. For recurring spatially complex locations, provide structural line art, descriptive rendering language, and a compact prompt for direct generation without the reference image. Put `环境参考：【名称】` once below the clip title only when an environment image is actually used. Describe the distinct visible background in each shot.
7. Draft each block in this order: optional `分镜参考`; concise `景别`; concise `构图`; concise `运镜`; detailed `画面内容`. The first three fields define the shot's base state. Put any timed change of scale, composition, or camera—especially multi-stage camera movement—inside `画面内容`. End on a reproducible pose or object state.
8. Validate, then manually audit source fidelity and reference suitability. For revisions, patch only affected clips and their analysis rows unless a story change propagates farther.
9. Generate only a companion Chinese subtitle file alongside the storyboard unless the user explicitly requests a dialogue table. Order every spoken line, inner monologue, narration, and clearly voiced fantasy line by clip and timecode; keep each speaker turn separate. Use the filename `<storyboard-basename>_中文台词顺序表.srt`. Convert clip-local timecodes to a continuous episode timeline using each clip's actual duration; if no audio timing exists, mark the SRT timing as provisional in the handoff.

## Non-negotiable rules

### Source and reference fidelity

- Cite a crop only when the full target composition matches the specific referenced sub-shot.
- Preserve the reproduction point at its stated phase before or after enriching motion. A reference constrains only that referenced sub-shot, not every later phase in the same timed block. Added motion within that sub-shot may use only subjects, props, and contacts already visible in the crop and must stay inside its action envelope. Any newly visible character, prop, hand/contact relation, or composition phase absent from the crop requires a clearly marked hard-cut/uncited 补格 or reverse-shot phase.
- Source fidelity outranks motion density. Animate preserved panels with actions such as chewing, swallowing, gaze shifts, grip tension, visible-prop sway, visible-paper movement, wind, light, and return to pose.
- Do not turn dialogue concepts into replacement props or scenes. If the panel shows left-hand skewer and right-hand map, a line about money does not authorize coins.
- Use originals to recover omitted text and context; use crop filenames for formal references.
- Determine camera angle from camera position and perspective, never from where the character looks. A raised or lowered head does not itself imply a low or high camera.
- Keep horizontal viewing direction separate from composition position. Record `正面／略微斜侧面／斜侧面／纯侧面／背面` in `景别`; record `左侧三分之一／中央／右侧三分之一／边缘或其他偏心位置` in `构图`. A centered subject may still be seen from the side.
- Never use `中央` as a fallback. Infer placement from the cited panel's visual center of mass, negative space, overlap, and layer hierarchy. Preserve genuine centered compositions; do not force variety against the source.
- Before citing a crop, recheck base scale/angle, subject placement and overlap, pose/gaze, hands/props, and layer hierarchy. Keep off-panel characters, props, reactions, contacts, and later camera states out of the referenced sub-shot; they may appear only after an explicit hard cut or other clearly marked shot-phase change.

### Timing, structure, and sound

- Treat 15 seconds as a soft maximum, not a target. Short completed beats are valid.
- Keep one complete sentence inside one clip and give each speaker natural time.
- Use hard cuts by default; reserve special transitions for genuine story events.
- Use speed lines, solid-color backgrounds, or gradients only when they appear in the source or are genuinely needed for a story beat; they are optional effects, not default filler. When the source uses monochrome solid/gradient space, preserve its visual function and mood but allow suitable anime colorization instead of forcing black, white, or gray.
- After every spoken or narrated sentence, add full-width parentheses with timbre, tone, emotion, and useful pace/stress notes.
- Use dialogue and narration only. Do not write ambience, Foley, impacts, breath sounds, silence cues, BGM, or musical cues in storyboard blocks.

### Behavior type, visual fullness, and prompt purity

- Classify each beat before adding motion. **State** sustains travel, waiting, rest, observation, vigilance, atmosphere, or another ongoing condition; enrich it selectively with the existing repeated action, gaze/expression, prop/cloth motion, medium feedback, and environment/light, without forcing a complete event chain. **Action** means the shown process or result matters; it does not authorize an automatic setup → execution → response → result chain. Add **reaction** as an optional tag to either type for perception and emotional response. For mixed beats, name a primary and secondary type and preserve both source functions.
- Use a **source-bounded minimum action arc**. First identify which phase the current and adjacent panels actually show. Add only the smallest missing phase needed to connect known entering and exiting states. A substantive added body/prop action must pass all three checks: **evidence** (visible additions are supported by the current crop; adjacent panels may establish chronology but not current-frame visibility), **visibility** (observable inside the stated framing), and **anchor safety** (does not change the preserved pose, hand/prop relation, overlap, or composition). If any check fails, delete it or place a genuinely necessary composition-changing phase in a separate uncited 补格 shot.
- Never invent off-frame bracing, gripping, contact, props, body mechanics, travel paths, setup, follow-through, or recovery merely to make an action feel complete. A panel showing one decisive action phase may remain on that phase; enrich it with visible local response, cloth/prop settling, medium feedback, environment/light, or a return to the source pose.
- Give an action beat only the visible, source-supported change needed for its story function; a decisive source phase may remain controlled instead of becoming a full arc. Let state beats remain controlled and continuous.
- For long dialogue or dense multi-speaker exchanges, use a hard-cut reverse shot and/or brief environment, prop, hand, or detail insert when useful. Inserts must preserve event order and dialogue meaning and must not invent a new event.
- Keep **story continuity** separate from **frame visibility**. A prop seen in the previous panel may still exist in a pocket, hand, or off-frame, but that does not authorize showing it in the next cited crop. Reintroduce it visually only when the current crop shows it or in a separate uncited shot.
- For invented content, specify relevant color, material, finish, form, quantity, placement, motion order, and final state.
- Use positive observable instructions. Keep asset decisions, editorial notes, hidden estimates, and partial-only references outside timed prompts.
- Prefer direct visible descriptions over stacked prohibitions. Retain a negative constraint only when it prevents a likely source-fidelity failure; otherwise state the intended visible result and endpoint.
- Do not write meta-instructions such as “保持原格姿势／保持原格构图／与原格一致／原格中……”. Convert the reference analysis into direct visible descriptions of the subject, pose, object placement, background, motion, and endpoint. `分镜参考` carries the reference role; the timed prompt should describe only what the viewer sees.
- In the companion SRT, output Chinese subtitle text only. Translate the storyboard's Japanese dialogue naturally and retain line order, repetitions, interjections, inner-monologue labels, and fantasy labels. Do not include voice directions, sound effects, camera notes, role labels, or Japanese text. If a platform-safe appendix exists, generate a separate safe SRT; do not mix it into the master order.
- In the SRT, use Chinese subtitle text only, without role labels unless requested. Split multiple lines in one timed block into non-overlapping subtitle entries with natural reading duration; preserve chronological order and validate that entries are positive, ordered, and non-overlapping. When a safe appendix exists, generate a separate safe SRT or clearly mark the master and safe files; never silently mix adult-master and platform-safe lines.
- Keep 2D language consistent: hand-drawn line art, cel-shaded characters, layered backgrounds; avoid photographic camera jargon unless requested. Keep storyboard blocks visual and spoken-dialogue-only.
- For a multi-phase generation block, write each phase as an explicit shot state: reference role (if any), hard cut or camera change, one primary action, visible local background, and completed endpoint. Do not force every phase into a separate clip when the model can handle the load.

### Environments

- Simple or one-off location: provide a compact environment prompt describing only visible layout, materials, atmosphere/weather, light, and a few distinctive irregular details; use it directly without generating a reference image.
- Recurring spatially complex location: provide high-oblique structural line art, descriptive rendering language, and a compact prompt that can be used independently without the reference image. Do not generate an overhead plan.
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
