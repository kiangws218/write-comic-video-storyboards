---
name: write-comic-video-storyboards-gen2-5
description: Turn ordered comic panels into rigorously source-faithful 2D animation storyboards with compact prose, continuous-action clip grouping, restrained performance enrichment, and motivated animation effects. Use when Gen2-level panel restoration must remain authoritative while improving shot flow and production finish.
---

# Comic video storyboards Gen2.5

Create a source-faithful storyboard mother draft with selective cinematic polish. The comic is authoritative; polish is admitted only after panel composition, space, angle, pose, contact, and event order are locked.

## Load only what is needed

- New episode or substantial rewrite: read [references/storyboard-spec.md](references/storyboard-spec.md).
- Always read [references/gen2-5-cinematic-extension.md](references/gen2-5-cinematic-extension.md); it defines the compact format, continuous-action grouping, performance restraint, and animation-effects gate.
- Ambiguous order, long/multi-speaker panels, or requested pre-analysis: also read [references/pre-analysis-gen2.md](references/pre-analysis-gen2.md).
- Paste-ready Seedance prompt or failed-generation review: read [references/seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Fight or complex fast action: also read [references/2d-animation-execution.md](references/2d-animation-execution.md); its motion grammar remains subordinate to source fidelity in `storyboard-spec.md`.
- Small revision: read only the target and adjacent panels plus the relevant section of `storyboard-spec.md`.
- When modifying this skill itself: read [references/regression-cases.md](references/regression-cases.md) and rerun its cases before replacing the loaded version.

Run scripts directly; do not read them unless modifying them.

## Workflow

1. Confirm source/original and crop directories, reading order, output path, aspect ratio, target model, and the 15-second soft ceiling. Storyboard dialogue language is fixed to Japanese.
2. Make a 360–480 px global review set or contact sheets. Use this pass only for order, text, locations, continuity, and risk marking; do not draft exact composition from it.
3. Draft in contiguous batches of about 3–6 panels. Reopen that batch at about 720 px, freeze each current panel's compact screen facts, inspect its immediate neighbors, and write while the images are fresh. Escalate only risky panels to original resolution: unusual or strong perspective, fast action, overlapping limbs, hand/prop contact, complex creature/prop topology, heavy occlusion/effects, off-frame causes, or unresolved text/details.
4. Recover missing text and order from originals; cite crop filenames in the storyboard. Resolve each visible identity from the current panel plus an explicit character-reference mapping or uniquely visible design evidence. Adjacent-story continuity may nominate a candidate but never proves identity; when current-frame evidence remains insufficient, use a descriptive role label instead of guessing. For an ordinary panel, keep the internal ledger minimal. Before drafting any panel with 3+ bubbles, 2+ speakers, dialogue plus inner speech, or a continuous turn reaching 28 meaningful Japanese characters or 3 complete clauses, create the dialogue-risk row defined in [references/pre-analysis-gen2.md](references/pre-analysis-gen2.md). Record every source bubble in reading order, including speaker, kind, source text, final line, estimated seconds, and target shot.
5. Pass the dialogue gate before writing the batch: estimate speech first, choose shared/reverse/insert coverage, then set shot and clip boundaries. Never shrink speech to fit space left in a preselected 15-second clip. Decide 保格／拆格／补格／并格 and State/Action/Reaction after the speech load is known; run ordinary performance concurrently with speech.
6. For each cited sub-shot, compare the finished prompt with the current panel's frozen screen facts. Use the composition and topology locks in `storyboard-spec.md` when triggered. Remove any visible noun or relation supported only by story continuity. Adjacent shots must create a real visual or dramatic increment; otherwise merge them.
7. Keep every source-continuous action phrase in one generated clip whenever it fits the model limit. A `片段` is one generated clip; every actual camera shot inside it is a separate `分镜N（X秒）` block with its own positive integer duration. Any hard cut, reverse shot, microcut, insert, environment shot, or newly composed view starts the next numbered shot; do not hide an untimed cut inside another shot. Preserve source anchors first, then add only admitted coverage and state useful rhythm changes. Keep continuous action in the same `片段` while allowing several numbered shots; do not restore separate field headings.
8. While each batch is still open, compare the source bubbles with the dialogue-risk rows one by one, then compare those rows with the finished shots. For a new episode or substantial rewrite, pass the internal JSON ledger to `scripts/validate_storyboard.py --dialogue-ledger`; fix missing lines, wrong targets, or insufficient shot time before advancing. Then run the ordinary visual/source audit. A script pass is not evidence that the comic was reread or that screen facts are correct.
9. After the storyboard is approved, generate the Chinese SRT unless the user explicitly requests it earlier. Do not create a Markdown dialogue table unless requested.

## Core invariants

1. **Source before motion.** Never replace visible comic content with a dialogue-derived prop, scene, character, or action. Current-frame visibility outranks story continuity.
2. **References are phase-specific.** Cite a crop only when the referenced sub-shot matches the full composition. A later different composition must be an explicit hard cut or uncited 补格/reverse shot.
3. **Minimum motion.** State beats remain continuous and restrained. Action beats receive only a source-supported preceding phase, following phase, or refinement of the shown action when it helps the beat; never auto-complete an action chain or stretch a finished beat to 15 seconds.
4. **Action admission test.** A substantive added action must have source evidence, be visible in the framing, and preserve the cited pose/hand/prop/overlap anchors. Otherwise remove it or place a necessary composition change in an uncited shot.
5. **No off-frame mechanics.** Do not invent bracing, gripping, contact, hidden props, travel paths, setup, follow-through, or recovery merely to make motion physically complete.
6. **Visible local background is mandatory and uncapped.** In every shot, describe all useful background information actually visible in that framing—physical or abstract. Write whatever is present; do not impose a quota, invent off-frame space, or restore a physical location behind a source-supported solid, gradient, or speed-line background.
7. **Natural Japanese speech.** Write every spoken line, inner monologue, and narration line in natural Japanese, translating non-Japanese source text without changing meaning, order, speaker, or information. Do not place Chinese source dialogue in the storyboard; Chinese dialogue belongs only in the subtitle deliverable. Split rather than accelerate. Dialogue-risk panels cannot advance until every source bubble is mapped or explicitly justified as omitted and the target shot has enough time. After every spoken or narrated sentence add `（音色、语气、情绪；必要时语速、停顿、重音）`.
8. **Visual-only storyboard.** Write dialogue and narration, but no sound effects, ambience, Foley, breath sounds, silence cues, BGM, or musical instructions.
9. **Direct prompt language.** Do not write production notes, reference-analysis language, or negative control stacks such as “保持原格姿势／按照原格处理／不出现湖岸实景”. State the positive visible pose, placement, motion, background, and endpoint directly.
10. **Adult delivery when requested.** Keep the complete source-faithful adult/R18 master first; append complete platform-safe replacements only for affected clips. Never overwrite or silently sanitize the master.
11. **Panel restoration is mandatory.** A cited comic composition must become recognizably readable at its declared phase; it is not merely inspiration. Added connective motion may not restage its angle, screen placement, overlap, pose silhouette, hand/prop relation, contact, or background hierarchy.
12. **Continuous-action clip boundary.** Do not end a generated clip between tightly coupled phases such as load→launch, swing→contact, fall→landing, or grab→pull when the whole phrase fits within 15 seconds. Internal cuts are allowed, but the action phrase remains in one clip.
13. **Effects are subordinate.** Air distortion, directional wash, impact flash, glint, shockwave, debris, or camera response must express a source-supported speed, force, material, or light event. They may strengthen an anchor but never cover, replace, or deform it beyond recognition.
14. **Coverage may expand; story may not.** Uncited microcuts, environment/prop/reaction inserts, and necessary connective views are allowed when they clarify an existing action, space, rhythm, or emotion. They cannot replace a cited panel, contradict its screen facts, introduce a new story event, or become the only view of a source-important beat.
15. **Name what the model can see.** When no creature or special-object reference asset is supplied, do not rely on a lore name alone. Use a stable visual label built from scale, color, surface/material, body type, and defining anatomy; repeat the full label at the first appearance of every independently generated clip.
16. **Identity needs current-frame evidence.** Character names come from an explicit reference mapping or discriminating visible traits in the current panel. Narrative continuity, dialogue order, or a previous panel may help choose what to inspect but cannot by itself assign the identity. Use a descriptive role label when evidence is not strong enough.

Use hard cuts by default. Speed lines, solid-color backgrounds, and gradients are optional only when source-supported or genuinely useful to the story beat; monochrome source effects may be colorized while preserving their function.

## Output and handoff

- Treat 15 seconds as a soft maximum, not a target.
- Begin the storyboard with `## 场景色彩基准`. Keep it globally reusable across all shots: describe only overall tone, visual style, rendering/texture quality, contrast/saturation behavior, and lighting approach. Do not inventory objects or prescribe colors for named characters, props, architecture, terrain, or other scene contents there.
- Put `环境参考：【名称】` once below a clip title only when an environment image is actually used.
- Use a compact environment prompt for every location. Add structural line art and rendering language only for recurring spatially complex locations; never create a standard overhead plan.
- Keep environment assets physically pure: space, materials, traces, weather, and light only—no character routes or narrative functions.
- Report clip count, approximate runtime, reference count, structural validation, manual source-audit status, and absolute output paths separately.

```powershell
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder>
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder> --dialogue-ledger <internal-dialogue-ledger.json>
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
```
