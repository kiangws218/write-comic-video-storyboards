---
name: write-comic-video-storyboards-gen2-5
description: Turn ordered comic panels into rigorously source-faithful 2D animation storyboards with compact prose, continuous-action grouping, restrained performance, motivated effects, and optional Seedance auto-coverage for coherent fight sequences. Use when Gen2-level panel restoration must remain authoritative while improving shot flow, acting, or combat impact.
---

# Comic video storyboards Gen2.5

Create a source-faithful storyboard mother draft with selective cinematic polish. The comic is authoritative; polish is admitted only after panel composition, space, angle, pose, contact, and event order are locked.

## Load only what is needed

- New episode or substantial rewrite: read [references/storyboard-spec.md](references/storyboard-spec.md).
- Always read [references/gen2-5-cinematic-extension.md](references/gen2-5-cinematic-extension.md); it defines the compact format, continuous-action grouping, performance restraint, and animation-effects gate.
- Ambiguous order, long/multi-speaker panels, or requested pre-analysis: also read [references/pre-analysis-gen2.md](references/pre-analysis-gen2.md).
- Paste-ready Seedance prompt or failed-generation review: read [references/seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Fight or complex fast action: also read [references/2d-animation-execution.md](references/2d-animation-execution.md); it defines precise-shot and Seedance auto-coverage modes, combat continuity, rhythm, and integrated VFX quality. Its motion grammar remains subordinate to source fidelity in `storyboard-spec.md`.
- Small revision: read only the target and adjacent panels plus the relevant section of `storyboard-spec.md`.
- When modifying this skill itself: read [references/regression-cases.md](references/regression-cases.md) and rerun its cases before replacing the loaded version.

Run scripts directly; do not read them unless modifying them.

## Workflow

1. Confirm source/original and crop directories, reading order, output path, aspect ratio, target model, and the 15-second soft ceiling. Storyboard dialogue language is fixed to Japanese.
2. Make a 360–480 px global review set or contact sheets. Use this pass only for order, text, locations, continuity, color-source classification, and risk marking; do not draft exact composition from it. Classify the episode or each mixed-source sequence as color, monochrome, or partially colored before writing any palette language.
3. Draft in contiguous batches of about 3–6 panels. Reopen that batch at about 720 px, freeze each current panel's compact screen facts, inspect its immediate neighbors, and write while the images are fresh. Escalate only risky panels to original resolution: unusual or strong perspective, fast action, overlapping limbs, hand/prop contact, complex creature/prop topology, heavy occlusion/effects, off-frame causes, or unresolved text/details.
4. Recover missing text and order from originals; cite crop filenames in the storyboard. Resolve each visible identity from the current panel plus an explicit character-reference mapping or uniquely visible design evidence. Adjacent-story continuity may nominate a candidate but never proves identity; when current-frame evidence remains insufficient, use a descriptive role label instead of guessing. For an ordinary panel, keep the internal ledger minimal. Before drafting any panel with 3+ bubbles, 2+ speakers, dialogue plus inner speech, or a continuous turn reaching 28 meaningful Japanese characters or 3 complete clauses, create the dialogue-risk row defined in [references/pre-analysis-gen2.md](references/pre-analysis-gen2.md). Record every source bubble in reading order, including speaker, kind, source text, final line, estimated seconds, and target shot.
5. Pass the dialogue gate before writing the batch: estimate speech first, choose shared/reverse/insert coverage, then set shot and clip boundaries. Never shrink speech to fit space left in a preselected 15-second clip. Decide 保格／拆格／补格／并格 and State/Action/Reaction after the speech load is known; apply the performance and timing gate in `references/gen2-5-cinematic-extension.md` §4 before setting final integer durations. Count all dialogue in each actual shot, write the required visible acting in its compact prose, and estimate serial versus concurrent intervals.
6. For each cited sub-shot, compare the finished prompt with the current panel's frozen screen facts. Use the composition and topology locks in `storyboard-spec.md` when triggered. Remove any visible noun or relation supported only by story continuity. Adjacent shots must create a real visual or dramatic increment; otherwise merge them. Before closing the batch, pass the per-block background gate in `storyboard-spec.md`: every `分镜` or `战斗段` must contain a direct positive description of the visible physical setting, graphic background, or frame-filling surface.
7. Keep every source-continuous action phrase in one generated clip whenever it fits the model limit. Normally every actual camera shot is a separate `分镜N（X秒）` block. For a visually continuous, action-led fight that passes the admission gate in `references/2d-animation-execution.md`, one clip may instead use a single `战斗段1（X秒·自动分镜）` block: give only the total duration and an ordered beat list, allowing Seedance to plan internal cuts. Never mix the two timing modes in one clip. Preserve source anchors first, then add only admitted coverage, rhythm changes, and causally motivated effects.
8. While each batch is still open, compare the source bubbles with the dialogue-risk rows one by one, then compare those rows with the finished shots. For a new episode or substantial rewrite, pass the internal JSON ledger to `scripts/validate_storyboard.py --dialogue-ledger`; fix missing lines, wrong targets, or insufficient shot time before advancing. Check enacted performance density, long-take development, and speech/acting timing under the extension §4; then run the ordinary visual/source audit. A script pass is not evidence that the comic was reread or that screen facts are correct.
9. After the storyboard is approved, generate the Chinese SRT unless the user explicitly requests it earlier. Do not create a Markdown dialogue table unless requested.

## Core invariants

1. **Source before motion.** Never replace visible comic content with a dialogue-derived prop, scene, character, or action. Current-frame visibility outranks story continuity.
2. **References are phase-specific.** Cite a crop only when the referenced sub-shot matches the full composition. A later different composition must be an explicit hard cut or uncited 补格/reverse shot.
3. **Minimum motion.** State beats remain continuous and restrained. Action beats receive only a source-supported preceding phase, following phase, or refinement of the shown action when it helps the beat; never auto-complete an action chain or stretch a finished beat to 15 seconds.
4. **Action admission test.** A substantive added action must have source evidence, be visible in the framing, and preserve the cited pose/hand/prop/overlap anchors. Otherwise remove it or place a necessary composition change in an uncited shot.
5. **No off-frame mechanics.** Do not invent bracing, gripping, contact, hidden props, travel paths, setup, follow-through, or recovery merely to make motion physically complete.
6. **Visible local background is mandatory and uncapped.** In every shot, directly describe all useful background information actually visible in that framing—physical setting, solid color, gradient, speed field, or a close surface filling the frame. Write positive visible content such as `蓝灰云层压在深绿树冠上方` or `深酒红内衬与胡桃木盒壁铺满背景`. Keep classification and source-analysis notes internal; labels such as `无实体背景／无独立背景` and explanations such as `原格没有实景／不补画树林` never belong in the storyboard.
7. **Natural Japanese speech.** Write every spoken line, inner monologue, and narration line in natural Japanese, translating non-Japanese source text without changing meaning, order, speaker, or information. Do not place Chinese source dialogue in the storyboard; Chinese dialogue belongs only in the subtitle deliverable. Split rather than accelerate. Dialogue-risk panels cannot advance until every source bubble is mapped or explicitly justified as omitted and the target shot has enough time. After every spoken or narrated sentence add `（音色、语气、情绪；必要时语速、停顿、重音）`.
8. **Visual-only storyboard.** Write dialogue and narration, but no sound effects, ambience, Foley, breath sounds, silence cues, BGM, or musical instructions.
9. **Direct prompt language.** Do not write production notes, background classification labels, reference-analysis language, or negative control stacks such as `保持原格姿势／按照原格处理／无独立背景／原格没有实景／不补画树林`. State the positive visible pose, placement, motion, background, and endpoint directly.
10. **Adult delivery when requested.** Keep the complete source-faithful adult/R18 master first; append complete platform-safe replacements only for affected clips. Never overwrite or silently sanitize the master.
11. **Panel restoration is mandatory.** A cited comic composition must become recognizably readable at its declared phase; it is not merely inspiration. Added connective motion may not restage its angle, screen placement, overlap, pose silhouette, hand/prop relation, contact, or background hierarchy.
12. **Continuous-action clip boundary.** Do not end a generated clip between tightly coupled phases such as load→launch, swing→contact, fall→landing, or grab→pull when the whole phrase fits within 15 seconds. Internal cuts are allowed, and admitted combat auto-coverage may leave their exact allocation to Seedance, but the action phrase remains in one clip.
13. **Effects carry force and scale.** Write motivated effects directly beside the action that causes them. Give important effects a readable onset, peak, material response, local light interaction, and decay; vary intensity across the exchange. They may strengthen speed, contact, damage, or scale but never cover, replace, or deform a source anchor beyond recognition.
14. **Coverage may expand; story may not.** Uncited microcuts, environment/prop/reaction inserts, and necessary connective views are allowed when they clarify an existing action, space, rhythm, or emotion. They cannot replace a cited panel, contradict its screen facts, introduce a new story event, or become the only view of a source-important beat.
15. **Name what the model can see.** When no creature or special-object reference asset is supplied, do not rely on a lore name alone. Use a stable visual label built from scale, color, surface/material, body type, and defining anatomy; repeat the full label at the first appearance of every independently generated clip.
16. **Identity needs current-frame evidence.** Character names come from an explicit reference mapping or discriminating visible traits in the current panel. Narrative continuity, dialogue order, or a previous panel may help choose what to inspect but cannot by itself assign the identity. Use a descriptive role label when evidence is not strong enough.
17. **Color evidence has precedence.** Explicit user color directions and supplied reference assets outrank inferred palette choices. A visible color comic is authoritative for every subject, object, environment, effect, and background it actually shows. A monochrome comic supplies value, material, light, and shading evidence but does not mean that the depicted world is literally black, white, or gray; establish stable non-character colors instead, while character colors come from the supplied character references.

Use hard cuts by default. Speed lines, solid-color backgrounds, and gradients are optional only when source-supported or genuinely useful to the story beat; monochrome source effects may be colorized while preserving their function.

## Output and handoff

- Treat 15 seconds as a soft maximum, not a target.
- Use `战斗段N（X秒·自动分镜）` only under the combat reference's admission gate. Its ordered beats have rhythm and coverage cues but no fabricated per-shot durations.
- Begin the storyboard with `## 场景色彩基准`. Keep it globally reusable across all shots: describe only overall tone, visual style, rendering/texture quality, contrast/saturation behavior, and lighting approach. Do not inventory objects or prescribe colors for named characters, props, architecture, terrain, or other scene contents there.
- Apply the color-source gate in `references/storyboard-spec.md` §5. Preserve visible source colors when the comic is colored. For monochrome or partially uncolored source, add a concise `## 非人物上色锁定` after the global baseline and define recurring environment, architecture, prop, natural-element, effect, and solid/gradient-background colors; keep character colors tied to supplied character references.
- Put `环境参考：【名称】` once below a clip title only when an environment image is actually used.
- Use a compact environment prompt for every location. Add structural line art and rendering language only for recurring spatially complex locations; never create a standard overhead plan.
- Keep environment assets physically pure: space, materials, traces, weather, and light only—no character routes or narrative functions.
- Report clip count, approximate runtime, reference count, structural validation, manual source-audit status, and absolute output paths separately.

```powershell
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder>
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <crop-folder> --dialogue-ledger <internal-dialogue-ledger.json>
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
```
