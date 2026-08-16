# Seedance execution, review, and retake

Use this reference only when producing directly pasteable execution prompts or diagnosing a generated result. Keep the detailed storyboard mother draft as the source of truth.

## 1. Compile instead of rewriting

For each approved clip:

1. copy immutable plot result, dialogue, timing, shot purpose, and valid references;
2. identify whether the clip is a continuous take, phased single take, or actual multishot clip;
3. retain the primary generation target and fragile anchor from pre-analysis;
4. remove repeated static details already carried by a valid reference image;
5. retain concrete movement, composition, environment, material, lighting, voice, and sound details that affect generation;
6. remove empty evaluators such as “高级”“震撼”“电影级” unless translated into observable form;
7. preserve natural speech time rather than compressing dialogue to meet a character budget.

If shortening would damage the shot, split the generated clip or ask the user to select a larger supported limit.

## 2. Choose one prompt skeleton

For a Chinese Seedance surface that accepts a timeline, use:

```text
〖时间轴〗
0-3秒：……
4-8秒：……
9-15秒：……
```

Use integer timecodes. Do not mix this with `Shot 1 / Shot 2` labels.

For a continuous take, time blocks describe phases of the same camera path and action chain. Do not insert “硬切” between them.

For a genuine multishot clip, state the hard cut at the beginning of the new time block. Give each shot one primary action, one camera behavior, and one completed visual endpoint. A 10–15 second generation usually supports two or three substantial shots; more cuts require simpler actions or separate generation.

## 3. Reference-role discipline

Assign every referenced asset one explicit role:

- exact composition and pose;
- character identity or costume;
- environment geometry;
- style or palette;
- first frame or another supported control role.

Only call a crop a formal storyboard reference when it matches the full target composition. If it supplies only a local detail, omit it and describe the target shot directly.

For image-led video, prompt what the image cannot show: motion, timing, camera behavior, reaction, sound, light change, transformation, and required preservation. Avoid re-describing every visible static attribute.

## 4. Character budget

Treat the input limit as surface-specific. If the active field supports 2000 characters, target at most 1900 to leave editing room. Count actual Unicode characters with the supplied audit script; never estimate by sight.

When compression is required, remove in this order:

1. duplicated static description;
2. repeated atmosphere declarations;
3. empty quality adjectives and synonym stacking;
4. redundant negative instructions already expressed positively;
5. minor decorative motion unrelated to the shot purpose.

Do not remove dialogue pauses, action causality, critical material/color information, valid reference roles, or the visible endpoint merely to save characters.

## 5. Review for platform-safe wording

Review the execution prompt before delivery:

- state character adulthood clearly when age could be ambiguous and adult context is essential;
- describe visible actions, clothing, framing, injuries, and physical consequences objectively;
- avoid exploitative sexualization, graphic gore, instructions for wrongdoing, or other disallowed content;
- remove contradictory wording and risky combinations created accidentally by stacked adjectives;
- preserve safe plot function where possible, but do not invent code words, euphemisms, misspellings, or substitutions intended to evade platform review;
- if the requested result cannot be expressed safely, flag it for revision instead of claiming it will pass review.

Compliance review is a safety and clarity pass, not a moderation-bypass pass.

## 6. No-BGM rule

Storyboard mother drafts contain dialogue and narration only; do not add BGM, ambience, Foley, impacts, breath sounds, silence cues, or other audio-production instructions to them. Handle any separate audio-design pass outside the storyboard text.

## 7. Output format

````markdown
## 【片段1】标题

```text
〖时间轴〗
0-3秒：……
4-8秒：……
9-15秒：……
```
````

Keep compliance reasoning, removed phrases, character counts, and operator notes outside the fenced prompt.

## 8. Diagnose and retake

Classify the result before changing the prompt:

- **Keep**: primary target and fragile anchor succeeded.
- **Fix in post**: a brief removable flaw does not affect story or continuity.
- **Edit locally**: one isolated layer, object, or short interval is wrong.
- **Reroll**: prompt is clear and failure appears stochastic.
- **Rewrite**: the same semantic failure recurs or instructions conflict.
- **Split**: the shot exceeds the model's combined load.

Change one meaningful variable per retry: one clause, one reference role, one camera behavior, one action density choice, or one generation mode. Record:

`Take N · changed: … · result: … · verdict: …`

Two attempts with the same flaw require a wording or structural change. Do not modify later comic events to accommodate incidental output drift.
