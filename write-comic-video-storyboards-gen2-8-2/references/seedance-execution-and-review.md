# Seedance execution, review, and retake

Read this file only for paste-ready execution prompts or failed-generation review. Compile from the approved mother draft; do not rewrite the story.

## Compile

For each clip retain plot result, dialogue, timing, shot purpose, valid reference role, visible action causality, local background, lighting, and endpoint. Remove duplicated static details, repeated atmosphere, empty quality adjectives, redundant negatives, and operator notes.

Read the opening character color prompts with the shared character references before compiling. Keep the same canonical names and production palettes in every affected clip or its supplied character-reference asset; an unknown identity does not mean an uncolored design. Preserve each source-panel phase inside a merged continuous take. Do not turn phase-reference bullets into separate cuts or drop intermediate nodes to shorten the prompt. See [character-registry.md](character-registry.md) and the core contract.

Preserve concise environment sound, Foley, breath/body sound, silence and important non-dialogue synchronization from the approved mother draft when the target supports audio. Keep all speech treatment in `【台词与语气】`; never duplicate it in `【声音设计】`. Do not add BGM, score, melody or theme music. When the target is video-only, export these cues to the companion audio plan instead of silently deleting them.

Choose one structure. Default precise-shot structure:

```text
〖分镜〗
分镜1（3秒）：……
分镜2（5秒）：……
分镜3（7秒）：……
```

Use positive durations in 0.5-second increments, reset numbering at 1 in every clip, and keep the summed duration at or below the clip ceiling. Timing syntax and optional in-shot action ranges follow core-authoring.md; keep ranges local to each explicitly numbered shot (本镜内计时), starting at 0. Preserve simple action prose without adding ranges. A continuous camera take has one numbered block with internal action phases; every true cut gets a new block. For a true multishot clip, state `硬切` at the new block and give each shot a coherent main action with its useful concurrent acting layers, a clear camera behavior, visible local background, and endpoint. Split when combined load is too high.

For 2.8.2 use precise numbered shots, including fights. Legacy auto-coverage examples are not final 2.8.2 output: preserve independent original shots and auditable actual neighbors.

## Prompt wording

Use concise natural Chinese and familiar camera/animation terms. Preserve approved expression cues such as 金田系、作画感、作画爆发、Q弹、张力拉满、外连味、颜艺、夸张透视、smear frame when they carry the intended look or rhythm; do not strip them merely because they summarize style. Add the useful visible action if needed, without expanding every cue into a tutorial or a second action inventory. Never claim that a term guarantees a particular result.

Distinguish intentional squash/stretch, smear or SD acting from unintended identity drift, fused bodies or unmotivated deformation. A designed Q版/形变 passage must not receive contradictory blanket controls such as “全程正常比例、禁止任何变形”. Preserve its entry, important readable pose and exit. Keep source-panel bindings, full dialogue and actual endpoint.

Half-second ranges express the approved plan. Target timing response varies: the official [2.0 guide](https://docs.volcengine.com/docs/ark/seedance-2-0-prompt-guide?lang=en) notes unstable exact-time control, and the [2.5 guide](https://docs.volcengine.com/docs/ark/seedance-2-5-prompt-guide?lang=en) describes integer-second timestamps. Keep clear action order (先、突然、随后、停住) alongside numbers; do not silently round, drop phases or promise frame-accurate output. No new model adapter or duplicate global timeline is required.

## Reference roles

Assign each asset one role: exact composition/pose, environment geometry, style/palette, or another supported control role. Character identity and costume are handled by supplied character references, not repeatedly restated in the storyboard.

A comic panel/crop supplies an in-process/contact/result composition/pose anchor, never a first-frame/start-keyframe control. Preserve the approved opening-to-anchor action when compiling. Check the actual input mode before submission: follow core authoring's compatibility gate if it would bind the comic to frame zero. Do not silently remove a lead-in to make the tool accept that image; a separately approved opening asset has a different role.

Preserve each original-shot binding and its approved frame adaptation, not the panel’s accidental page crop. Added views keep their director role; do not label all shots source_locked. Copy exact frozen dialogue, voice-over segments, counted silence and actual endpoints; never shorten dialogue or remove an original shot for the prompt budget. If necessary split/regroup at a recoverable boundary, preserving all content.

Keep approved continuous speaker-to-speaker moves as one numbered take; do not automatically insert a cut at each new voice. Preserve a tall-panel tilt's opening, direction, important intermediate content and landing in the prompt, with the output frame and figure proportions stable. These camera choices follow [cinematic-rendering.md](cinematic-rendering.md#多人同格的连续运镜); compression must not turn them into a fixed crop, a stretched whole panel or a scroll of comic paper.

## Character budget

Use the actual surface limit. For a 2000-character field, target at most 1900. Count with `scripts/audit_seedance_prompt.py`.

Compress in this order:

1. duplicated static detail;
2. repeated atmosphere;
3. empty evaluators and synonyms;
4. redundant negative instructions;
5. decorative motion unrelated to the beat.

Do not remove dialogue pauses, action causality, critical material/color, valid reference roles, visible local background, or endpoint.

## Adult master and safe execution

Never sanitize or rewrite an adult/R18 master while compiling it. Apply platform-safe wording review only to the separately marked safe replacement draft. Do not use code words or claim guaranteed approval.

## Diagnose and retake

Classify before changing the prompt:

- **Keep**: primary target and fragile anchor succeeded.
- **Fix in post**: brief removable flaw.
- **Edit locally**: one isolated layer/object/interval is wrong.
- **Reroll**: prompt is clear and failure appears stochastic.
- **Rewrite**: the same semantic failure recurs or instructions conflict.
- **Split**: combined shot load is too high.

Change one meaningful variable per retry. After two identical failures, change wording or structure rather than rerolling unchanged. Do not modify later comic events to accommodate incidental output drift.

Output only the prompt body. Keep compliance reasoning, removed phrases, character counts, and retake notes outside it.
