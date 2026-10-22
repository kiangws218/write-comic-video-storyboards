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

Use positive integer durations, reset numbering at 1 in every clip, and keep the summed duration at or below the clip ceiling. A continuous camera take has one numbered block with internal action phases; every true cut gets a new block. For a true multishot clip, state `硬切` at the new block and give each shot a coherent main action with its useful concurrent acting layers, a clear camera behavior, visible local background, and endpoint. Split when combined load is too high.

For 2.8.2 use precise numbered shots, including fights. Legacy auto-coverage examples are not final 2.8.2 output: preserve independent original shots and auditable actual neighbors.

## Reference roles

Assign each asset one role: exact composition/pose, environment geometry, style/palette, or another supported control role. Character identity and costume are handled by supplied character references, not repeatedly restated in the storyboard.

A comic panel/crop supplies an in-process/contact/result composition/pose anchor, never a first-frame/start-keyframe control. Preserve the approved opening-to-anchor action when compiling. Check the actual input mode before submission: follow core authoring's compatibility gate if it would bind the comic to frame zero. Do not silently remove a lead-in to make the tool accept that image; a separately approved opening asset has a different role.

Preserve each original-shot binding and its approved frame adaptation, not the panel’s accidental page crop. Added views keep their director role; do not label all shots source_locked. Copy exact frozen dialogue, voice-over segments, counted silence and actual endpoints; never shorten dialogue or remove an original shot for the prompt budget. If necessary split/regroup at a recoverable boundary, preserving all content.

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
