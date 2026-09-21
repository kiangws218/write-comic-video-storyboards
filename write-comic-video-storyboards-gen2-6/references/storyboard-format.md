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

## Per-shot executable format

Every ordinary numbered shot uses the following fields in this order. This follows the useful separation in the supplied `re0` reference while retaining Gen2.6 source grounding:

```markdown
**分镜1（6秒）：**
分镜参考 `[00.jpg]`
场景环境：当前镜头实际可见的空间、主体位置、前中后景、材质和环境运动。
环境音：当前空间持续存在的底噪、远近层次、遮挡和左右声像。
镜头设计：景别、焦段、机位高度与方位、构图、景深、焦点、起幅、单一运镜和落幅。
可见动作：从自足的起始姿态开始，按语义节点写人物、道具、头面朝向、微表情、重心与延迟运动，最后落到明确状态。
台词与语气：角色说：“……”（音色、语气、情绪、必要的停顿或重音）。无台词时写“无台词”。
光影布光：依据本镜头环境、光源方向、人物位置、遮挡和材质，写主光、辅光/反射、明暗分区、局部高光与必要的空气效果。
声音设计：可见动作拟音、呼吸/静默、台词距离与关键音画同步点。
```

`环境音`、`镜头设计`与`光影布光`必须独立成行；不要把声音、摄影和布光藏在可见动作段。仍然不要恢复旧式的`景别：`、`构图：`、`运镜：`或`画面内容：`碎片字段。

每个片段会被单独提交给视频模型，因此每一镜必须自足。直接重述当前起始姿态、人物朝向、位置、接触、背景和光源，不写`保持原有`、`上一格`、`上一镜`、`同一场面继续`、`只放大上一格`、`沿用前镜`等跨块指代。生成字段中也不写`不新增`、`不要`、`不出现`、`不使用`、`避免`等否定控制句；删除不被允许的内容，并把保留下来的画面改成正向、可见、可执行描述。

Use stable prop and creature labels. When no creature or special-object reference is supplied, use a visible label containing useful scale, dominant color, surface/material, body type, and defining anatomy; repeat the full label at the first appearance of each independently generated clip.

`环境音：`与`声音设计：`每镜必填。环境音只写空间底声与声像；声音设计只选一至两个最有作用的拟音、呼吸、静默或同步节点。让声音事件与可见原因同步，不在声音行藏入新的视觉动作。

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
