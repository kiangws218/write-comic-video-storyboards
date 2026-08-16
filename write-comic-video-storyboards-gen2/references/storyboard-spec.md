# Storyboard specification

Read this file for a new episode or substantial rewrite. For a small revision, read only the relevant section.

## 1. Source, original-panel reproduction, and references

Use originals for missing dialogue/context/order and crop filenames for formal references. Inspect current plus adjacent panels; expand to five only if ambiguous.

A crop may follow `分镜参考` only when the shot matches:

- framing and viewpoint;
- subject count, position, scale, and overlap;
- pose, silhouette, and gaze;
- left/right hand and prop assignment;
- foreground/background or abstract effect hierarchy.

The referenced sub-shot must visibly reproduce and briefly hold that point. The reference may be the opening, middle, or endpoint of a timed block. Animate around it; mark any later composition-changing action as a hard-cut or uncited 补格 phase. Do not replace visible content with objects inferred from dialogue. Partial borrowing of identity, costume, prop, or background receives detailed text but no formal citation.

Judge camera angle from perspective and camera position relative to the subject, not from gaze or head tilt. Looking up does not mean a low-angle shot; looking down does not mean a high-angle shot. Check visible top/bottom planes, facial perspective, foreshortening, and camera height.

Before citing a crop, audit the written base fields and detailed action against it: scale/angle, subject placement/overlap, pose/gaze, hands/props, and foreground/background hierarchy. Keep off-panel characters, listener reactions, props, contacts, and later camera states out of the referenced sub-shot, not merely its base fields. A later phase in the same timed block is allowed only when its hard cut or shot change is explicit.

Separate narrative continuity from current-frame visibility. A prop shown in the previous panel may still exist narratively while remaining in a pocket, hand below the crop, or off-frame. The previous panel never authorizes drawing it into the next cited composition. If it must become visible again, use a current crop that shows it or a separate uncited time block.

## 2. Dialogue, segmentation, and transitions

Fallback Japanese timing when read-aloud timing is unavailable:

| Line | Typical time |
|---|---:|
| Interjection/very short phrase | 1–2s |
| Short sentence | 2–4s |
| Medium sentence | 4–6s |
| Long explanation | 6–9s |
| Two connected long clauses | 8–12s |

Add breaths, hesitation, clause pauses, interruption, and listener reaction when useful. Give every speaker a complete natural turn; split rather than speed up. If a listener is absent from the preserved speaker composition, keep the speaker shot intact and either use a separate uncited reverse shot or hard-cut to one inside the same timed block. For long or dense dialogue, also insert brief environment, prop, hand, or detail shots when useful; these must not invent a new event or alter dialogue order. Do not make the listener enter from the edge of the cited frame. Use continuous integer timecodes and a 15-second soft ceiling.

Prefer boundaries at location/time change, completed entrance/exit/reveal, dialogue turn, emotional reaction, or stable result. Begin with reproducible context and end with a reproducible state. Use hard cuts by default.

## 3. Required direct-prompt structure

Every timed block uses concise base fields followed by a detailed execution field:

1. optional `分镜参考 [crop.jpg]`;
2. `景别：` base vertical camera angle, horizontal viewing direction when visually meaningful, and base shot scale only, for example `轻微仰视，略微斜侧面，全身中景` or `平视，面部近景`;
3. `构图：` only essential subject placement, key prop, depth, or occlusion; identify left/right thirds or other off-center placement when present, and never default to `中央`;
4. `运镜：` one concise base instruction such as `固定镜头`, `跟随镜头`, or `固定镜头，缓慢拉远`;
5. `画面内容：` detailed start state, ordered action, performance, environment/light, dialogue, sound, endpoint, and any timed change of scale, composition, or camera movement. Camera changes may be described here whenever they occur, especially multi-stage movement.

Do not repeat the same fact across the four fields. The base `景别` must describe the cited panel, not a later push-in result; put that change in `运镜` or, when timed/complex, in `画面内容`. For each phase, make the visible local background spatially locatable—such as a tree trunk at frame edge, a bench plank below, a low wall behind, or blurred roofs in the distance—without expanding beyond the stated framing.

Treat viewing direction and frame placement as independent axes. Use the plain prompt terms `正面`, `略微斜侧面`, `斜侧面`, `纯侧面`, or `背面` for direction; reserve `左侧三分之一`, `中央`, `右侧三分之一`, `边缘`, and other off-center descriptions for composition. Determine placement from the source panel's visual weight, negative space, overlap, and foreground/background relationship. Preserve a genuinely centered source panel, but never select center merely because placement is uncertain.

After every spoken or narrated sentence add `（音色、语气、情绪；必要时语速、停顿、重音）`. Do not write sound effects, ambience, Foley, breath sounds, silence cues, BGM, or musical cues in storyboard blocks. Speed lines, solid-color backgrounds, and gradients are optional and should follow the source or a genuine story beat; monochrome source backgrounds may be colorized while preserving their visual function and mood.

Timed blocks contain no asset planning, editorial explanation, hidden estimates, operator notes, partial-only references, or reference-analysis meta-language. Do not write “保持原格姿势／保持原格构图／与原格一致／原格中……”. The cited image already carries its reference role; write the visible pose, placement, background, motion, and endpoint directly.

## 4. Behavior type and motion richness

Classify each beat before setting motion density:

- **State**: ongoing travel, waiting, rest, observation, vigilance, mood, or environment. Use the existing repeated action plus restrained gaze/expression, cloth/prop movement, medium feedback, and environment/light. Do not force every stage of an event arc.
- **Action**: an action whose shown process or result matters. Identify the source-visible phase first: setup, execution, immediate response, result, or settled endpoint. Do not automatically manufacture the other phases.
- **Reaction**: optional tag for either type: perception → response → readable emotion → recovery/decision.
- **Mixed**: mark primary and secondary type; neither source function may be displaced.

For Hold shots, prefer chewing, swallowing, gaze shifts, grip tension, prop sway, paper edges, hair/cloth settling, shadow, weather, and light that preserve or return to the original panel. Blinking and breathing alone rarely carry a long shot, but motion density never outranks fidelity.

Use a source-bounded minimum action arc:

1. Compare the current panel with its immediate neighbors and record the known entering state, visible phase, and known exiting state.
2. Add only the smallest phase required to bridge those known states. “Action” is a motion-density classification, not permission to complete a full biomechanical chain.
3. For every substantive added body or prop action, ask:
   - **Evidence**: Is a visible addition shown by the current crop? Adjacent panels may prove chronology or continued possession, but not visibility inside the current cited composition.
   - **Visibility**: Can the viewer actually see it within the declared shot scale, angle, crop, and occlusion?
   - **Anchor safety**: Does it preserve the cited panel's pose, hands/props, overlap, and composition?
4. If any answer is no, remove the action. If the missing phase is genuinely necessary and changes composition, put it in a separate uncited 补格 shot.

Do not infer an unseen supporting hand, off-frame surface contact, hidden prop, preparatory step, path, follow-through, recovery, or full-body mechanics merely because it would make the movement physically complete. For a close-up cough, for example, use only visible shoulder, face, sleeve, hair, breath, or liquid response unless the panel or neighbor actually shows a hand bracing against furniture. If a shot needs more visual change, use a source-supported preceding or following phase, a restrained local response, or a clearly marked hard-cut insert—not a speculative action chain.

For invented objects/crowds/accelerated passages, specify only relevant color, material, finish, form, quantity, scale, placement, action order, and final state. Show time passage through observable change.

## 5. Environment deliverables

Choose the lightest sufficient form:

- **Compact environment prompt**: default for simple or one-off locations. Write one directly usable paragraph covering visible spatial layout, main materials and wear/natural traces, time/weather/atmosphere, light direction and temperature when useful, and two or three irregular identifying details. Keep it local to what the shot can see; do not invent a full map. No reference image is required.
- **Structure line art**: add only for recurring locations whose entrances, levels, paths, openings, occlusion, or fixed landmarks must remain consistent. Use an empty high-oblique ultra-wide view with geometry, depth, elevations, contour hierarchy, and minimal tone.
- **Rendering language**: add to a structural package when consistent color, material, weather, atmosphere, shadows, haze, or reflections matter across clips.
- **Compact prompt for every structural package**: even when structure line art and rendering language are provided, also supply one independently usable compact environment prompt for workflows that skip the reference image.

Do not produce a top-down or overhead plan as a standard pre-analysis deliverable.

Environment prompts include no people, creatures, bodies, character equipment, assigned routes/positions, staging zones, sight cones, narrative functions, or future-use instructions.

Natural sites: irregular microtopography and boundaries, varied tree age/spacing/crowns, layered plants/soil/stones/deadwood, interrupted paths, varied line density. Built sites: plausible skew, sag, uneven spacing, wear, stains, dust, repairs, and deformation.

In the storyboard place `环境参考：【名称】` once under the clip title only when an environment reference image is used. Each angle still describes its visible background. For a compact-prompt location, place the relevant environment wording directly in the shot or in the pre-analysis environment section for copy-forward use.

## 6. Companion Chinese subtitle file

Create one subtitle file named `<storyboard-basename>_中文台词顺序表.srt`. Do not create a separate Markdown dialogue-order table unless the user explicitly asks for one.

- Convert each clip-local timecode into a continuous episode timeline by cumulatively adding the actual durations of preceding clips. Do not copy `0-15s` clip-local times directly into the episode SRT.
- Split multiple lines within one storyboard block into separate, naturally readable, non-overlapping entries. Keep entries in chronological order, with positive duration.
- Use Chinese subtitle text only; omit role labels, Japanese text, voice notes, sound effects, camera fields, and production notes unless the user explicitly requests them.
- If no recorded audio is available, use provisional timings derived from dialogue order and natural pauses, and state that they should be retimed against the final voice track.
- When a platform-safe version exists, generate a separate safe SRT or clearly named safe file; never mix master adult lines and safe replacements in one unmarked file.

## 7. Adult/R18 and platform-safe appendix

When requested, keep the complete source-faithful adult/R18 master first. Append only affected complete replacements under:

```markdown
# 附录：平台安全替换稿
## 【平台安全替换·片段N】标题
```

Safe blocks retain timing, story function, continuity, voice, sound, and recognizable non-adult anchors. They are explicit adaptations, not coded moderation bypasses or approval guarantees.

## 8. Compact audit

- Source text/order/speakers/results match originals and neighbors.
- Every cited crop has a readable reproduction point and correct hand/prop assignments.
- Added motion enriches rather than displaces the source.
- Every substantive added body/prop action passes evidence, visibility, and anchor-safety checks; no off-frame mechanics are invented for completeness.
- Previous-panel props remain off-frame unless the current crop shows them or a separate uncited shot reintroduces them.
- Listener reactions absent from the speaker crop use a separate uncited reverse shot or an explicit hard-cut sub-shot and never alter the preserved frame.
- The SRT exists beside the storyboard, uses a continuous timeline, and has positive, ordered, non-overlapping entries.
- Timecodes are integer, continuous, natural, and ≤15s.
- Each block has fields in order; every voice has parentheses; no audio-effect or BGM instructions appear.
- Environment assets are physically pure and irregular/plausibly worn.
- Prompt bodies contain no production notes or unnecessary negative tails.
- Adult master remains intact; each safe replacement is complete and directly generatable.

Template:

```markdown
## 【片段1】标题
环境参考：【环境A·版本】

**0-3s：**
分镜参考 `[00.jpg]`
景别：……
构图：……
运镜：……
画面内容：……“……”（……）
```
