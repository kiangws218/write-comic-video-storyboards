# Storyboard format, color, and delivery

Use this file for ordinary shot structure, timing, color, environment and sound prompts, adult alternatives, and SRT delivery. Source permissions live in `source-grounding.md`; dialogue coverage lives in `dialogue-coverage.md`; sound choices live in `audio-design.md`.

## Clip and shot timing

A `片段` is one generated clip. Treat 15 seconds as a soft maximum. End when the beat is complete; never pad with prolonged holding, shaking, screaming, decorative camera motion, or repeated gestures.

For ordinary clips, reset shot numbering at 1 and give every actual camera shot one positive integer duration:

```markdown
## 【片段1】标题

**分镜1（3秒）：**
分镜参考 `[00.jpg]`
……

**分镜2（5秒）：**
……
```

A hard cut, reverse, insert, environment shot, reaction, microcut, or newly composed view starts the next numbered block. Continuous phases in one camera setup remain one block. Do not hide cuts with `画面切到` or similar wording.

Keep a source-continuous physical phrase—load→launch, swing→contact, fall→landing, grab→pull—in one generated clip when it fits. If it exceeds the limit, split at the strongest stable state and fully restate pose, direction, grip/contact, speed state, and background relation at the next opening.

An action-led fight that passes `2d-animation-execution.md` may instead use one `战斗段1（12秒·自动分镜）` block with ordered untimed beats. Never mix ordinary and automatic-combat timing modes in one clip.

## Compact direct prose

Write one paragraph in this approximate order:

`angle/scale → placement/depth/overlap → camera/focus behavior → visible start → ordered action/performance → dialogue → local background/light/material → motivated effects → endpoint`

Do not output separate `景别：`, `构图：`, `运镜：`, or `画面内容：` fields. Write directly generatable visuals, not source comparison, asset planning, estimates, operator notes, moderation reasoning, or negative control stacks.

Forbidden examples include `保持原格姿势`, `按照原格处理`, `无独立背景`, `原格没有实景`, and `不补画树林`. Replace them with positive visible pose, subject set, background, motion, and endpoint.

Use stable prop and creature labels. When no creature or special-object reference is supplied, use a visible label containing useful scale, dominant color, surface/material, body type, and defining anatomy; repeat the full label at the first appearance of each independently generated clip.

After the visible paragraph, add one compact `声音设计：` line when a beat has meaningful ambience, Foley, breath, silence, audio perspective, or BGM. Keep sound events ordered and synchronized to visible causes. Do not hide new visual actions in the sound line.

## Color-source gate

Begin every storyboard with `## 场景色彩基准`. This is a reusable look envelope only: source-compatible work/studio/director-style references supplied by the user or deliberately selected under `cinematic-rendering.md`, overall hue tendency, saturation/contrast behavior, 2D rendering and texture, light softness/hardness and broad direction, atmospheric depth, and image clarity. State the style stack once rather than repeating it in every shot. Do not inventory concrete objects or assign named character, prop, building, terrain, or creature colors there.

Apply this precedence:

1. explicit user color directions and supplied reference assets;
2. visible colored comic evidence for the same subject/object/location/effect;
3. a verified colored occurrence of the same recurring item in a mixed source;
4. coherent production choices only for genuinely uncolored non-character elements.

A monochrome comic provides value, material, depth, light, ink, and screentone evidence, not literal gray world color. Add a compact `## 非人物上色锁定` after the global baseline for recurring environments, architecture, props, natural elements, effects, and abstract backgrounds. Character colors come from supplied character references.

Copy relevant locked colors into each environment prompt or shot where visible. Lighting may tint a surface temporarily but does not rewrite its base color.

## Environment prompts

Provide a compact prompt for every location. Simple or one-off locations need only the prompt. Recurring, spatially complex locations may also receive empty high-oblique structural line art and rendering guidance; do not create a standard top-down plan.

Environment assets contain physical space, materials, wear or natural traces, weather, and light only—no people, creatures, equipment, routes, staging zones, or narrative functions. Put `环境参考：【名称】` once below a clip title only when an environment image is actually used. Every shot still describes its visible local backing.

## Adult master and safe appendix

When requested, write the complete source-faithful adult/R18 master first without deleting, euphemizing, or silently sanitizing content. Append complete replacements only for affected clips under:

```markdown
# 附录：平台安全替换稿
## 【平台安全替换·片段N】标题
```

Replacements preserve timing, story function, continuity, dialogue intent, and recognizable non-adult anchors. They are adaptations, not approval guarantees. Preserve the corresponding shot-duration pattern unless the number of turns genuinely changes.

## SRT after approval

After storyboard approval, create `<storyboard-basename>_中文台词顺序表.srt` unless requested earlier.

- Accumulate ordered shot durations into one episode timeline.
- Split turns into positive, ordered, non-overlapping entries.
- Output Chinese subtitle text only: no roles, Japanese, voice notes, camera notes, or production notes.
- Mark timing provisional when no final voice track exists.
- Generate a separately named safe SRT when replacement dialogue exists.

Do not create a Markdown dialogue table unless requested.

## Final manual audit

Confirm source order, event and result; exact cited composition; background type and content; color-source fidelity; dialogue completeness and ownership; natural speech/action time; stable prop naming; action continuity across clips; motivated effects; and unchanged adult master. Structural validation never substitutes for this visual verdict.
