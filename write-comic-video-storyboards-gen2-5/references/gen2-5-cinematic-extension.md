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

Treat one numbered block as one actual camera shot and give it one positive integer duration. A genuine hard cut, reverse shot, microcut, insert, environment shot, or newly composed view inside the same generated clip starts the next numbered block. Continuous phases without a cut stay in one block. Do not create a second numbered block merely because the speaker changes.

## 3. Continuous-action unit

Before setting clip boundaries, identify action units. One unit has one uninterrupted intention and physical consequence, for example:

- crouch/load → push-off → airborne rise;
- reach → grip → pull → object moves;
- weapon wind-up → travel → contact → immediate recoil;
- slip → fall → ground/water contact → first settled pose;
- throw → flight → impact;
- tail/body sweep → character displacement → landing or splash.

Keep the whole unit in one generated clip when its natural duration is within 15 seconds. This is more important than equal clip length. A clip may contain several cited source phases and several numbered shots when the camera cuts, but it must not hand an unfinished motion to the next clip.

Split only at a physically stable state, an intentional hold, a completed contact/result, a clear change of intention, a time/location jump, or an unavoidable model-duration limit. If the unit exceeds 15 seconds, split at the strongest stable pose and restate that exact pose, screen direction, grip/contact, speed state, and background relation at the next clip opening.

Do not combine merely adjacent actions that have different intentions. Dialogue followed by a new attack can be separate even if the character has not changed location.

## 3.1 Rhythm inside a shot

Design temporal contrast instead of giving every phase equal weight:

- **Anticipation or emotional hold:** more in-betweens, small readable changes, stable camera, and a brief hold when tension needs to accumulate.
- **Acceleration or rush:** fewer in-betweens during the fastest travel, stronger spacing between poses, directional camera follow or screen wash, and delayed hair/cloth/debris response.
- **Readable complex motion:** concentrate in-betweens around a grip change, body unfolding, balance correction, or other phase whose mechanics must remain legible.
- **Slow motion:** use selectively around a decisive realization, near miss, airborne apex, or pre-contact instant; keep spatial direction and source pose clear.
- **Impact:** the contact instant may compress to one or two graphic frames, followed by a short readable recoil, deformation, debris, water, or camera-settle phase.
- **Aftermath:** reduce motion and allow the result pose or changed environment to register before the next intention begins.

Write these rhythm changes directly in the shot prose, for example `蓄力阶段动作细密缓慢；发力一刻中割骤减、速度陡升；空中展开时中割重新集中，使四肢和武器轨迹清楚；接触瞬间插入一至两帧高反差冲击帧，色相服从已锁定配色，随后短暂保持受力结果`. Use only the phases that materially help the beat.

Atmosphere and action-quality language such as `速度感强烈`, `力量感突出`, `冲击力集中`, `紧张逼迫`, `严肃压抑`, or `激烈近身交锋` is allowed when the visible staging, rhythm, light, or effects actually produce that quality. Attach it to the relevant phase; do not use it as a generic quality suffix.

## 4. Performance and timing gate

Use this gate after source locks and dialogue coverage planning. It is the single authority for performance density, long-take admission, and performance timing; other references link here rather than restating it.

### Visible performance scaled to speech

Count all spoken and inner Japanese lines in one actual numbered shot, across speakers and bubbles; exclude spaces, punctuation, voice notes, and narration. Splitting quotes does not reduce this total.

| Meaningful Japanese characters in the shot | Required performance treatment | Default coverage |
|---|---|---|
| 1–20 | Write 1–2 visible performance details suited to the line. | Normally keep one shot unless the speaking turn changes the visual focus or lands a distinct response/punchline. |
| 21–41 | Write 2–3 distinct visible performance details, distributed over semantic beats. | A single speaker may remain in one shot when the written performance develops; use a reverse or insert when the semantic target, observed object, or listener state changes. |
| 42+ | A justified retained long take needs 3–4 supported details forming sustained visible development. | Default to genuinely different shots divided at semantic turns. Use the existing `long_take_reason` only when an unbroken supported action or relationship would be harmed by cutting. |

A detail is a readable change or explicitly sustained expressive state in eyes, face, head/body, or a visible hand/prop relation. Give it a speech/event trigger or a clear temporal role. Articulation alone, repeated wording of one gesture, camera movement, wind-driven hair, and scenery do not count as additional acting details. A held expressive state can count once; keep source-supported neutrality rather than inventing suppressed emotion. For multiple speakers, address each visible speaker and the listener where meaningful; off-screen speech may run over visible listener or hand performance.

Do not turn the quota into simultaneous gesture stacking. Write the fewest qualifying details, ordered through the shot, and choose actions readable at the declared scale. If the crop leaves insufficient supported freedom, split coverage or shorten the shot after redistributing dialogue; never manufacture a grip, step, tears, hidden motive, or new event to fill time. Added coverage obeys the same performance gate.

Internally establish source-supported purpose and trigger; finally write only directly visible behavior in compact prose. AU codes and a full eight-dimension table are optional analysis aids, not output fields. Use relative timing such as 开口前／说到「実際の日本語の語句」时／句末; precise subsecond scheduling belongs after voice alignment.

When acting is triggered by dialogue, every word, phrase, or meaning from that dialogue mentioned in the visual prose must use the exact Japanese text spoken in that shot, normally inside `「」`. Never identify a Japanese trigger with a Chinese translation or paraphrase such as `说到爱她时`, `提到结婚纪念日时`, or `接着嘱咐别偷看时`; write `说到「愛してる」时`, `说到「結婚記念日」时`, or `说到「こっそり開けるなよ」时`. Generic timing that does not restate dialogue content—such as 开口前, 转入后半句, 回答后, or 句末—is allowed. Apply the same rule inside voice-direction parentheses. The cited Japanese trigger must occur verbatim in that shot's final dialogue; if translation or line segmentation changes, update its acting triggers too.

### Coverage gate

Clip continuity and camera continuity are separate decisions. Keep a continuous physical action in one generated clip when required by §3, but give every speaker view, reverse, reaction, prop/environment insert, and other actual camera change its own consecutively numbered shot inside that clip. Never hide a cut in prose with `画面切到`, `再切到`, `切至`, or equivalent wording.

Use the fewest shots that create real visual or dramatic increments:

- A speaker change alone does not force a cut. When the next turn is an answer, rebuttal, reveal, joke landing, or clear attitude change, default to the new speaker or the listener reaction unless a source-supported shared action makes the unchanged composition more informative.
- For a single 21–41-character turn, retain one shot only when its visible performance develops across the semantic beats. Camera movement, lip motion, wind, or repeated versions of one gesture do not supply coverage.
- At 42+ characters, divide coverage at semantic turns by default. A retained long take must pass the existing enacted-development test and record `long_take_reason`; do not keep it merely because the character continues speaking.
- For exposition or off-screen explanation, use source-compatible subject, prop, environment, process, or result inserts when they clarify the stated information. Do not let an unchanged wide shot carry the whole explanation, and do not invent illustrative events absent from the source.
- Seven seconds is an audit trigger, not a universal cut point. Inspect any ordinary shot at or above it for a genuine developing performance or continuous action. Split when the visual focus changes; retain it when cutting would damage a supported unbroken action or relationship.
- Multiple cited panels in one ordinary shot are acceptable only when they are phases of the same camera setup and continuous action. Different composition, scale, angle, subject focus, or overlap requires another numbered shot. Combat auto-coverage remains governed by its own admission gate.

### Long-take admission must be enacted

The existing 42-character/three-clause continuous-turn trigger still plans coverage across source bubbles. An exception requires a source-supported start state → specific trigger → readable development → settled endpoint actually written in the shot. Lips moving, a stiff shoulder, a list of separately quoted sentences, or the phrase 持续表演 is insufficient. Check the finished shot, not the intention in the ledger. If development is absent, the exception fails and coverage must be replanned. Ordinary blinks or tiny gestures do not by themselves justify an extended take.

### Estimate speech and acting together

For one concurrent interval: required pre-action + max(sequential speech, concurrent performance) + required post-action. When one act must finish before the next line or action begins, estimate each interval separately and add them; do not hide serial acts inside one max. A pause already included in the speech estimate is not added twice. Round the complete shot upward to positive integer seconds, sum shots into clips, and split at a stable result when the natural unit exceeds the model limit.

Keep an optional `performance` array in the existing dialogue ledger for every shot above 20 characters, every long-take exception, and any necessary serial/pre/post action. Each entry contains `target`, concise source `evidence`, `details` (exact visible-behavior excerpts occurring in that shot), and `intervals` with nonnegative `speech_seconds` and `acting_seconds`. Intervals are sequential; speech and acting inside each interval are concurrent. Speech-only and acting-only intervals use zero for the other value. Each mapped line's seconds remain speech-only. A long-take entry also has `long_take_reason`, which must describe the written development. Do not create another ledger or put estimates into generatable prose.

The validator checks mappings, declared excerpts/counts, and interval arithmetic, not whether the acting is convincing, source-supported, or whether every prose paraphrase of dialogue was found. Manually verify evidence, readability, distinctness, exact-Japanese dialogue triggers, endpoint, and whether the density fits the duration. Visible breathing may be described when supported; breath sounds, added interjections, Foley, and ambient audio remain excluded.

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
