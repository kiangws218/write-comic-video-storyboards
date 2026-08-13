# Storyboard specification

## 1. Pre-analysis

Use a three-panel window for every decision; expand to five panels when the speaker, action, or continuity remains ambiguous.

Treat source layers as complementary:

| Source | Purpose |
|---|---|
| Original comic page | Recover omitted dialogue, narration, order, and wider context |
| Cropped screenshot | Supply a possible formal reference filename and principal panel composition |

Build a scene ledger before drafting:

| Crop | Original | Location | Characters | Entering state | Action | Exiting state | Dialogue | Props | Ambiguity |
|---|---|---|---|---|---|---|---|---|---|

Then mark each beat as 保格、拆格、补格、or 并格. Record immutable source results separately so connective animation cannot alter the plot.

## 2. Dialogue timing and multi-speaker panels

Time dialogue before camera flourishes. Use these ranges only when read-aloud timing is unavailable:

| Japanese line size | Typical delivery |
|---|---:|
| Interjection or very short phrase | 1–2 seconds |
| Short sentence | 2–4 seconds |
| Medium sentence | 4–6 seconds |
| Long explanation | 6–9 seconds |
| Two connected long clauses | 8–12 seconds |

Add time for hesitation, clause pauses, breaths, interruption, and listener reaction. When one panel has long dialogue or several bubbles:

1. identify speaker order from tails, gaze, pose, and adjacent panels;
2. assign a complete natural duration to each turn;
3. split at a question-answer boundary, interruption, reaction, or completed action;
4. give listeners observable reactions while another person speaks;
5. keep a complete sentence inside one clip.

Fifteen seconds is a soft ceiling. Short clips are valid; unnaturally fast delivery is not. Use integer timecodes only.

## 3. Reference suitability

A cropped image may appear after `分镜参考` only when the generated shot preserves its complete principal composition:

- comparable framing and viewing angle;
- matching subject count and screen arrangement;
- matching pose relationship and gaze direction;
- matching foreground/background hierarchy;
- no new major action that contradicts the pictured pose.

Do not cite a crop merely to borrow a face, costume, prop, body part, or background fragment. Describe those details in the new composition instead. Re-audit references after adding animation; a new lift, turn, stride, weapon action, or end pose may invalidate the original citation.

Maintain a reference table in the pre-analysis report:

| Image | Source information | Allowed complete composition | Mismatch examples | Used in final storyboard |
|---|---|---|---|---|

## 4. Environment packages

Group shots by physical location before drafting. Build a three-part reusable package only for recurring locations.

### Environment prompt purity

Environment assets are empty spatial references, not storyboards. Name each package with neutral physical terms such as terrain, material, weather, time, or condition: `【环境B·森林荒地凹地阴天湿地版】`. Do not put character names, creature names, occupations, battles, deaths, visits, intended actions, or story outcomes into the label.

Describe only the physical site and objective traces already present in it. Exclude:

- people, creatures, bodies, silhouettes, equipment carried by characters, and character-specific light or shadows;
- entry or exit routes assigned to a character, where someone can stand, where a creature can occupy, and who can see what;
- labels such as observation area, rescue entrance, combat zone, testing area, resting area, or any other narrative-purpose zone;
- instructions that explain how the environment will be used later.

Convert narrative staging into neutral physical description. For example:

- replace `豪斯可从前方进入、甲角龙可盘踞后方` with `前缘连接一条缓坡，后缘树线中央留有不规则缺口，二者之间隔着椭圆碎石凹地`;
- replace `中央留出两名猎人的休息区` with `中央为被踩低的短草与裸土混合地面，旁侧散落两块扁石和一截朽木`.

### Structure line-art prompt

Describe an empty, high-oblique, ultra-wide establishing view. Expose architectural structure, depth, openings, physical paths, fixed landmarks, elevation, and occlusion. Request monochrome structural line art with clear contour hierarchy and minimal tonal fill.

For natural terrain, explicitly break artificial regularity:

- use low mounds, shallow depressions, drainage channels, erosion rills, exposed roots, and uneven ground instead of one smooth plane;
- shape forest edges and clearings with irregular concave and convex transitions, clustered protrusions, recessed bays, broken sightlines, and asymmetrical gaps instead of smooth arcs or perfect ovals;
- vary tree age, trunk thickness, lean, spacing, crown height, and canopy size;
- layer saplings, shrubs, ferns, tall grass, short grass, moss, bare soil, stones, leaf litter, deadwood, and occasional fallen branches;
- let paths change width, split or fade, show interrupted ruts, grass encroachment, puddles, and eroded edges;
- vary contour thickness, stroke density, sparse and dense hatching, overlap, occlusion, and foreground-to-background detail so the drawing reads as accumulated ecology rather than a designed park.

For interiors and built sites, avoid showroom order. Use slightly skewed or non-square geometry where plausible, sagging shelves, uneven compartments, naturally varying passage widths, and objects with different sizes, spacing, and orientations. Include wear, chipped edges, scratches, stains, dust, patched surfaces, and small structural deformation appropriate to the setting.

### Overhead-plan prompt

Describe a true top-down view. Show floor plan, entrances, doors, windows, roads, drainage, terrain breaks, paths, rocks, vegetation masses, fixed objects, relative distance, elevation boundaries, and orientation. Optimize for spatial understanding rather than dramatic rendering. Use only physical relationships; do not draw or name character routes, positions, sight cones, action areas, or semantic story zones.

### Descriptive rendering language

State:

- fixed geometry and spatial relationships;
- walls, floor, ceiling, terrain, openings, and landmarks;
- materials, wear, texture, gloss, transparency, and reflectivity;
- dominant, secondary, and accent colors;
- weather, atmosphere, time of day, and background activity;
- base light source position and direction, color temperature, shadow behavior, haze, and reflections;
- geometry-preserving variants such as daytime, night, clean, damaged, or years-later versions.

Describe illumination only through environmental surfaces and fixed objects: light across ground relief, wall planes, shelves, rocks, foliage, dust, water, windows, and structural shadows. Do not anchor lighting to armor, skin, hair, a creature, or an implied person.

For a one-off location, put the visible setting directly in the relevant `画面内容`. Never insert asset-planning notes into the formal prompt.

In the storyboard, place one line below the clip title:

`环境参考：【环境B·遗迹版】`

Do not repeat environment references inside each timed shot. From each camera angle, describe the particular wall, doorway, path, shelf, tree line, terrain, or light visible behind the subject.

## 5. Clip segmentation

Choose boundaries in this order: location/time change; completed entrance, exit, or reveal; dialogue turn; emotional reaction; stable end state or hook.

Begin with reproducible context and end with a state the next clip can reproduce. Use a hard cut by default. Use a special transition only for a meaningful plot event, with visible start and end states.

## 6. Required shot structure

Every time block uses this order:

1. optional `分镜参考 [crop.jpg]` on its own line;
2. `景别：` — framing, angle, and any within-shot change;
3. `构图：` — subject positions, depth, foreground, background, gaze, and visual focus;
4. `运镜：` — locked shot, pan, tilt, push, pull, track, rack focus, or a clear combination;
5. `画面内容：` — start state, action order, performance, secondary motion, environment, light, voice, sound, and end state.

The framing may evolve inside one block, such as medium shot to close-up. Camera instructions should say what the camera does, not list motions it must avoid.

## 7. Motion and visual fullness

Build a visible action arc rather than a static panel with minor movement:

1. establish the initial pose and prop state;
2. perform a meaningful major action;
3. show bodily follow-through and prop response;
4. add supporting facial or micro-performance;
5. add environment or secondary motion;
6. use selective light/material change when it serves the shot;
7. end on a concrete pose, object state, or composition.

Useful layers include lifting or shouldering a weapon, lowering it before placing a hand on the chest, turning toward camera, taking a step, shifting weight, opening a door, flipping pages, lighting materials, handling goods, leaves crossing the lens, cloud shadows moving, fabric reacting to wind, reflections changing, coins falling, and inventory visibly emptying.

Blinking, breathing, hair drift, and cloth flutter are supporting motion, not a complete several-second shot. For dead or immobile characters, keep the body logically still and move the camera, weather, light, surrounding rescuers, shadows, liquid, or loose cloth instead.

## 8. Added-content specificity

Content absent from the source needs more—not less—specificity.

For objects, state color, material, finish, translucency, form, quantity, scale, and placement. For crowds or hands, vary skin tone, clothing color/material, entry direction, action order, and exit direction. For accelerated passages, use observable cues such as jump-cut positions, moving shadows, rapid hand activity, visibly decreasing stock, and a precise final state.

Preserve the source result and add only the connective action required to make it animate.

## 9. Voice and sound

After every character line or narration sentence, immediately append full-width parentheses containing:

- voice timbre and approximate age/gender presentation when useful;
- tone and emotion;
- speaking pace and pauses when relevant;
- keyword stress or volume change when relevant.

Example:

`旁白说道：“……”（低沉厚实的成年男性音色，语速沉稳，语气庄严克制，在关键词处加重）`

Annotate each speaker separately. Use dialogue, narration, ambience, Foley, impacts, breath, and deliberate reduction of environmental sound. Do not add BGM, score, melody, or musical cues.

## 10. Positive prompt language

Write the intended visible result directly:

- replace “不增加其他怪物” with the actual subjects and background occupying the frame;
- replace “不使用环绕镜头” with “固定侧面中景，接触时快速推进并停住”;
- replace “不出现人物” with “镜头视野完全由天空、树冠和飞鸟组成”.

Remove unnecessary negative generation tails from `构图` and `运镜`. Retain negative wording when it carries story information or a visible condition, such as “族谱没有妹妹记录” or “身体没有呼吸反应”.

## 11. Prompt purity

Numbered shot blocks are direct video-generation prompts. Keep these outside them:

- asset decisions such as “一次性场景”“不单独生成环境图”;
- editing notes such as “后期添加”“用于衔接”;
- explanations to the human operator;
- hidden duration estimates;
- reference images that supply only partial visual information.

## 12. Output template

```markdown
## 【片段1】场景名称
环境参考：【环境A·白天版】

**0-3s：**
分镜参考 `[00.jpg]`
景别：超远景，平视。
构图：……
运镜：镜头缓慢向左横移。
画面内容：……旁白说道：“……”（温和清晰的成年女性音色，语速舒缓，语气平静）音效：……镜头结束时……

**4-8s：**
景别：中景缓慢转为近景，微仰视。
构图：……
运镜：向前缓慢推进，最终停在人物面部。
画面内容：……
```

One-off locations omit the clip-level environment line and receive complete visible setting detail in the shot.

## 13. Quality audit

### Source and references

- Originals supplied all omitted text and context.
- Speakers, props, positions, and completed actions match adjacent panels.
- Every cited crop matches the complete target composition.
- Partial borrowing and newly composed shots rely on text, not a distracting citation.

### Timing and voice

- Timecodes are integer, continuous, and within the limit.
- Dialogue has natural breath and reaction space.
- Every spoken or narrated sentence has its own parenthetical voice direction.
- Formal prompts contain no BGM or musical cue.

### Structure and motion

- Every block contains 景别、构图、运镜、画面内容 in order.
- Major action, secondary motion, environment detail, and end state make the shot visibly evolve.
- Negative production tails have been replaced by positive composition and camera instructions.

### Environment and purity

- Recurring locations have line-art, overhead, and descriptive environment assets.
- Environment labels use neutral physical terms and contain no character, creature, role, event, or narrative-purpose wording.
- Actual line-art, overhead, and rendering prompts contain only the physical scene and objective pre-existing traces; they contain no character placement, assigned route, staging zone, or future-use instruction.
- Natural environments show irregular microtopography, nonuniform boundaries, varied vegetation, layered ground cover, interrupted paths, and varied line density rather than smooth ovals, uniform spacing, or repeated decorative patterns.
- Built environments show plausible misalignment, wear, varied spacing, and accumulated use rather than showroom order.
- Light is described on environmental surfaces and fixed objects only.
- The environment reference appears once at the clip header.
- Each angle receives a distinct visible background.
- Shot bodies contain no asset-planning or editorial notes.
