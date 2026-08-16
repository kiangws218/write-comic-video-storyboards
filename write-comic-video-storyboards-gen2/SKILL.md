---
name: write-comic-video-storyboards-gen2
description: Turn ordered comic, manga, manhua, or webtoon originals and crops into source-faithful, production-ready 2D animation storyboards and optional Seedance prompts. Use for original-panel preservation, missing-text recovery, preserve/split/fill/merge analysis, natural dialogue timing, local-background prompting, adult/R18 master plus platform-safe replacements, combat prompting, validation, or generation retakes.
---

# Comic video storyboards Gen2

Create a source-faithful storyboard mother draft. The comic is authoritative; an approved mother draft is authoritative for later execution prompts.

## Load only what is needed

- New episode or substantial rewrite: read [references/storyboard-spec.md](references/storyboard-spec.md).
- Ambiguous order, long/multi-speaker panels, or requested pre-analysis: also read [references/pre-analysis-gen2.md](references/pre-analysis-gen2.md).
- Paste-ready Seedance prompt or failed-generation review: read [references/seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Fight or complex fast action: also read [references/2d-animation-execution.md](references/2d-animation-execution.md); its motion grammar remains subordinate to source fidelity in `storyboard-spec.md`.
- Small revision: read only the target and adjacent panels plus the relevant section of `storyboard-spec.md`.
- When modifying this skill itself: read [references/regression-cases.md](references/regression-cases.md) and rerun its cases before replacing the loaded version.

Run scripts directly; do not read them unless modifying them.

## Workflow

1. Confirm source/original and crop directories, reading order, output path, dialogue language, aspect ratio, target model, and the 15-second soft ceiling.
2. Make non-destructive review copies about 540 px wide. Use about 720 px for small text, hand/prop relations, facial detail, or ambiguity; use full resolution only if still necessary. Inspect all panels once, then revisit only the current panel and neighbors.
3. Recover missing text and order from originals; cite crop filenames in the storyboard. Build the smallest useful internal ledger. Expand it only for risky or ambiguous beats.
4. Decide 保格／拆格／补格／并格, then classify each beat as State or Action with an optional Reaction tag. Establish natural dialogue timing before camera flourishes.
5. For each cited sub-shot, verify viewpoint, scale, placement, overlap, pose/gaze, hands/props, and foreground/background hierarchy. The cited composition may occur at the opening, middle, or endpoint.
6. Draft integer time blocks in this order: optional `分镜参考`; concise `景别`; concise `构图`; concise `运镜`; detailed `画面内容`. Describe only visible, generatable content.
7. Validate structure with `scripts/validate_storyboard.py`, then manually audit source fidelity. A script pass is not evidence that the comic was reread or that content is correct.
8. After the storyboard is approved, generate the Chinese SRT unless the user explicitly requests it earlier. Do not create a Markdown dialogue table unless requested.

## Core invariants

1. **Source before motion.** Never replace visible comic content with a dialogue-derived prop, scene, character, or action.
2. **References are phase-specific.** Cite a crop only when the referenced sub-shot matches the full composition. A later different composition must be an explicit hard cut or uncited 补格/reverse shot.
3. **Minimum motion.** State beats remain continuous and restrained. Action beats receive only a source-supported preceding phase, following phase, or refinement of the shown action when it helps the beat; never auto-complete an action chain.
4. **Action admission test.** A substantive added action must have source evidence, be visible in the framing, and preserve the cited pose/hand/prop/overlap anchors. Otherwise remove it or place a necessary composition change in an uncited shot.
5. **No off-frame mechanics.** Do not invent bracing, gripping, contact, hidden props, travel paths, setup, follow-through, or recovery merely to make motion physically complete.
6. **Visible local background is mandatory and uncapped.** In every shot, describe all useful background information actually visible in that framing—foreground occluders, surfaces, objects, terrain, structures, depth layers, weather, light, wear, and irregular detail. Write whatever is visibly present; do not reduce it to a fixed quota and do not invent off-frame space.
7. **Natural speech.** Split rather than accelerate. After every spoken or narrated sentence add `（音色、语气、情绪；必要时语速、停顿、重音）`.
8. **Visual-only storyboard.** Write dialogue and narration, but no sound effects, ambience, Foley, breath sounds, silence cues, BGM, or musical instructions.
9. **Direct prompt language.** Do not write production notes or meta-language such as “保持原格姿势／与原格一致／原格中……”. Describe the visible pose, placement, motion, background, and endpoint directly.
10. **Adult delivery when requested.** Keep the complete source-faithful adult/R18 master first; append complete platform-safe replacements only for affected clips. Never overwrite or silently sanitize the master.

Use hard cuts by default. Speed lines, solid-color backgrounds, and gradients are optional only when source-supported or genuinely useful to the story beat; monochrome source effects may be colorized while preserving their function.

## Output and handoff

- Treat 15 seconds as a soft maximum, not a target.
- Put `环境参考：【名称】` once below a clip title only when an environment image is actually used.
- Use a compact environment prompt for every location. Add structural line art and rendering language only for recurring spatially complex locations; never create a standard overhead plan.
- Keep environment assets physically pure: space, materials, traces, weather, and light only—no character routes or narrative functions.
- Report clip count, approximate runtime, reference count, structural validation, manual source-audit status, and absolute output paths separately.

```powershell
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder>
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
```
