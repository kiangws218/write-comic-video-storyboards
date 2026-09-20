# Seedance execution, review, and retake

Read this file only for paste-ready execution prompts or failed-generation review. Compile from the approved mother draft; do not rewrite the story.

## Compile

For each clip retain plot result, dialogue, timing, shot purpose, valid reference role, visible action causality, local background, lighting, and endpoint. Remove duplicated static details, repeated atmosphere, empty quality adjectives, redundant negatives, and operator notes.

Do not add sound effects, ambience, Foley, breath cues, silence cues, BGM, or music. Voice directions attached to dialogue remain.

Choose one structure. Default precise-shot structure:

```text
〖分镜〗
分镜1（3秒）：……
分镜2（5秒）：……
分镜3（7秒）：……
```

Use positive integer durations, reset numbering at 1 in every clip, and keep the summed duration at or below the clip ceiling. For a continuous take, blocks are phases of one camera/action path. For a true multishot clip, state `硬切` at the new block and give each shot one primary action, one camera behavior, visible local background, and endpoint. Split when combined load is too high.

For an action-led fight that already passed the mother draft's combat auto-coverage gate, preserve its single total-duration structure:

```text
〖战斗自动分镜〗
战斗段1（12秒·自动分镜）：
开局状态：……
战斗过程：
1. 【中速·大全景跟拍】……
2. 【急加速·侧向甩镜】……
3. 【接触瞬间·极短慢镜】……
4. 【恢复正常速度·中景】……
结束状态：……
```

Do not invent per-shot seconds when compiling this mode. Keep the ordered source anchors, attack/defense causality, rhythm changes, integrated effects, and endpoint. Do not convert a dialogue-heavy or continuity-fragile clip into auto-coverage merely to shorten the prompt.

## Reference roles

Assign each asset one role: exact composition/pose, environment geometry, style/palette, or another supported control role. Character identity and costume are handled by supplied character references, not repeatedly restated in the storyboard.

Only call a crop a formal storyboard reference when the full referenced sub-shot matches it. If it provides only a local detail, omit the citation and describe the target directly.

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
