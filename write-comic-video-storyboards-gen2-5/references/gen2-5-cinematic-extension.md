# Gen2.5 cinematic extension

This reference adds finish to Gen2 without loosening its source locks. If a cinematic choice conflicts with `storyboard-spec.md`, source fidelity wins.

## 1. Restore first, extend second

For every cited panel, freeze its exact phase-specific anchor before designing movement:

- camera height and vertical angle;
- horizontal viewing direction and shot scale;
- screen-left/right placement, depth, overlap, and occlusion;
- pose silhouette, gaze, visible limbs, and grounded/airborne state;
- hand, prop, grip, connection, action vector, and contact point;
- physical or abstract background hierarchy.

The finished shot must visibly arrive at that composition during its declared opening, middle, contact, result, or endpoint phase. Do not call a panel a key pose while changing its angle, spatial relation, silhouette, or contact. If the desired new angle differs, write an uncited phase and hard-cut back to a cited phase that actually matches.

Preserve every required source anchor, then design coverage around it. Uncited microcuts, environment or prop inserts, reaction shots, and connective views are allowed when they make the existing action, space, rhythm, or emotion clearer. Admit a new view only when it has a specific dramatic job, is compatible with the current and adjacent source facts, introduces no new plot event or unsupported mechanic, and still lets every source-important panel appear recognizably at the correct phase. Do not invent a route, wall contact, rebound, aerial turn, grip change, secondary attack, or recovery merely because it makes the sequence more spectacular.

## 2. Compact prose format

Use one paragraph in this approximate order:

`angle/scale → subject placement and overlap → camera behavior → visible start state → ordered action/performance → dialogue → local background/light → admitted effects → endpoint`

Do not output `景别：`, `构图：`, `运镜：`, or `画面内容：` headings. The information remains; only the labels disappear.

```markdown
## 【片段1】标题

**分镜1（5秒）：**
分镜参考 `[00.jpg]`
平视中近景，人物位于右侧三分之一；固定镜头。人物……“……”（音色、语气、情绪）。身后可见……，动作结束在……。
```

Treat one numbered block as a timed shot group. Give the group one total duration; do not assign separate second counts to its internal phases. For a genuine hard cut or insert inside the same generated clip, start a new line with `硬切：`, `碎切：`, `反打：`, `环境空镜：`, `插入镜头：`, or `补镜：`. State its new angle and visible composition directly. Do not create a second numbered block merely because the speaker changes.

## 3. Continuous-action unit

Before setting clip boundaries, identify action units. One unit has one uninterrupted intention and physical consequence, for example:

- crouch/load → push-off → airborne rise;
- reach → grip → pull → object moves;
- weapon wind-up → travel → contact → immediate recoil;
- slip → fall → ground/water contact → first settled pose;
- throw → flight → impact;
- tail/body sweep → character displacement → landing or splash.

Keep the whole unit in one generated clip when its natural duration is within 15 seconds. This is more important than equal clip length. A clip may contain several cited source phases and necessary internal hard cuts, but it must not hand an unfinished motion to the next clip.

Split only at a physically stable state, an intentional hold, a completed contact/result, a clear change of intention, a time/location jump, or an unavoidable model-duration limit. If the unit exceeds 15 seconds, split at the strongest stable pose and restate that exact pose, screen direction, grip/contact, speed state, and background relation at the next clip opening.

Do not combine merely adjacent actions that have different intentions. Dialogue followed by a new attack can be separate even if the character has not changed location.

## 3.1 Rhythm inside a shot group

Design temporal contrast instead of giving every phase equal weight:

- **Anticipation or emotional hold:** more in-betweens, small readable changes, stable camera, and a brief hold when tension needs to accumulate.
- **Acceleration or rush:** fewer in-betweens during the fastest travel, stronger spacing between poses, directional camera follow or screen wash, and delayed hair/cloth/debris response.
- **Readable complex motion:** concentrate in-betweens around a grip change, body unfolding, balance correction, or other phase whose mechanics must remain legible.
- **Slow motion:** use selectively around a decisive realization, near miss, airborne apex, or pre-contact instant; keep spatial direction and source pose clear.
- **Impact:** the contact instant may compress to one or two graphic frames, followed by a short readable recoil, deformation, debris, water, or camera-settle phase.
- **Aftermath:** reduce motion and allow the result pose or changed environment to register before the next intention begins.

Write these rhythm changes directly in the shot-group prose, for example `蓄力阶段动作细密缓慢；发力一刻中割骤减、速度陡升；空中展开时中割重新集中，使四肢和武器轨迹清楚；接触瞬间插入一至两帧黑白闪，随后短暂保持受力结果`. Use only the phases that materially help the beat.

Atmosphere and action-quality language such as `速度感强烈`, `力量感突出`, `冲击力集中`, `紧张逼迫`, `严肃压抑`, or `激烈近身交锋` is allowed when the visible staging, rhythm, light, or effects actually produce that quality. Attach it to the relevant phase; do not use it as a generic quality suffix.

## 4. Performance enrichment

Add performance only inside the visible freedom left by the panel:

- eye target and focus shift;
- one motivated blink at a thought transition;
- small head/shoulder or weight change;
- source-compatible hand or prop movement;
- delayed hair/cloth response to a visible primary motion.

Run compatible performance during speech. Do not change the source emotion, pose silhouette, facing, or composition merely to avoid stillness. A held look with subtle breathing can be the correct performance.

## 5. Animation-effects gate

An effect is admitted only when all are true:

1. a visible motion, impact, material, weather, or light source justifies it;
2. it has one clear job: speed, force, contact, depth, material response, or attention;
3. its origin, direction, duration, and fade are stated;
4. it preserves the cited panel's readable subjects and spatial relations;
5. it does not duplicate another effect doing the same job.

Prefer one primary effect and, when needed, one supporting response per beat. Dense source effects may justify more.

### High-speed movement

- A narrow transparent air-distortion band may form around the leading edge of a very fast body, weapon, or projectile, trail in the travel direction, and collapse after it passes.
- Directional screen wash may appear as translucent streaks aligned with movement. Keep the focal silhouette and source background hierarchy readable.
- Hair, cloth, dust, leaves, water, and loose debris react after the primary body or object, with magnitude proportional to speed.

### Impact

- At the exact contact instant, use a one- or two-frame black-white impact flash, high-contrast silhouette frame, or compact graphic impact shape when the beat benefits from a sharper hit.
- A pressure ring or air ripple starts at the contact point and expands along the available space; it pushes nearby dust, water, cloth, or foliage in the same direction.
- Camera shake begins at contact, has one dominant direction related to force, and settles quickly. It does not precede the hit.

### Reflection and glint

- A moving highlight or brief glint follows a real reflective edge and an established light direction, usually when a blade, wet surface, glass, eye, or polished armor changes angle.
- The highlight travels across the material surface and fades; it is not a generic rim placed around the subject.

### Heat, pressure, and refraction

- Localized refraction or waviness belongs behind strong heat, magical energy, blast pressure, or exceptionally fast displacement. Anchor it to the source and keep body topology stable.

Describe the visible effect directly. Do not write `后期添加`, node names, compositing software, or a generic effects stack.

## 6. Effects restraint audit

Remove an effect when it:

- exists only to make the shot look expensive;
- hides the manga key pose or changes its silhouette;
- contradicts the source's abstract or plain background;
- appears before its cause or persists after the beat has settled;
- uses a light color/direction unsupported by the scene;
- stacks flash, flare, shake, chromatic fringe, particles, smoke, and distortion on one minor action.

## 7. Visually explicit naming

When the video model has no reference asset for a creature or special object, a story-world name alone is not a usable visual anchor. At the first appearance of every independently generated clip, use a stable descriptive label such as `黑色巨型鳞甲龙，身体覆盖厚重黑色鳞甲，头部长有向后弯曲的粗大尖角`. Within the same clip, a shorter stable form such as `黑色鳞甲巨龙` may follow. Do not alternate between lore names and several visual names for the same subject.
