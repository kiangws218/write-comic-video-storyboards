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

The shot must visibly pass through and briefly hold that reproduction point. Animate around it; split a composition-changing action into an uncited 补格 shot. Do not replace visible content with objects inferred from dialogue. Partial borrowing of identity, costume, prop, or background receives detailed text but no formal citation.

Judge camera angle from perspective and camera position relative to the subject, not from gaze or head tilt. Looking up does not mean a low-angle shot; looking down does not mean a high-angle shot. Check visible top/bottom planes, facial perspective, foreshortening, and camera height.

Before citing a crop, audit the written base fields against it: scale/angle, subject placement/overlap, pose/gaze, hands/props, and foreground/background hierarchy. Keep props outside the panel and any later push-in/pull-back state out of those base fields.

## 2. Dialogue, segmentation, and transitions

Fallback Japanese timing when read-aloud timing is unavailable:

| Line | Typical time |
|---|---:|
| Interjection/very short phrase | 1–2s |
| Short sentence | 2–4s |
| Medium sentence | 4–6s |
| Long explanation | 6–9s |
| Two connected long clauses | 8–12s |

Add breaths, hesitation, clause pauses, interruption, and listener reaction. Give every speaker a complete natural turn; split rather than speed up. Use continuous integer timecodes and a 15-second soft ceiling.

Prefer boundaries at location/time change, completed entrance/exit/reveal, dialogue turn, emotional reaction, or stable result. Begin with reproducible context and end with a reproducible state. Use hard cuts by default.

## 3. Required direct-prompt structure

Every timed block uses concise base fields followed by a detailed execution field:

1. optional `分镜参考 [crop.jpg]`;
2. `景别：` base camera angle plus base shot scale only, for example `平视，面部近景`;
3. `构图：` only essential subject placement, key prop, depth, or occlusion;
4. `运镜：` one concise base instruction such as `固定镜头`, `跟随镜头`, or `固定镜头，缓慢拉远`;
5. `画面内容：` detailed start state, ordered action, performance, environment/light, dialogue, sound, endpoint, and any timed change of scale, composition, or camera movement. Camera changes may be described here whenever they occur, especially multi-stage movement.

Do not repeat the same fact across the four fields. The base `景别` must describe the cited panel, not a later push-in result; put that change in `运镜` or, when timed/complex, in `画面内容`.

After every spoken or narrated sentence add `（音色、语气、情绪；必要时语速、停顿、重音）`. Add no BGM or musical cues.

Timed blocks contain no asset planning, editorial explanation, hidden estimates, operator notes, or partial-only references. Write intended visuals positively.

## 4. Behavior type and motion richness

Classify each beat before setting motion density:

- **State**: ongoing travel, waiting, rest, observation, vigilance, mood, or environment. Use the existing repeated action plus restrained gaze/expression, cloth/prop movement, medium feedback, and environment/light. Do not force every stage of an event arc.
- **Action**: an action whose process/result matters. Use as appropriate: start → setup/anticipation → execution → body/prop response → result → endpoint.
- **Reaction**: optional tag for either type: perception → response → readable emotion → recovery/decision.
- **Mixed**: mark primary and secondary type; neither source function may be displaced.

For Hold shots, prefer chewing, swallowing, gaze shifts, grip tension, prop sway, paper edges, hair/cloth settling, shadow, weather, and light that preserve or return to the original panel. Blinking and breathing alone rarely carry a long shot, but motion density never outranks fidelity.

For invented objects/crowds/accelerated passages, specify only relevant color, material, finish, form, quantity, scale, placement, action order, and final state. Show time passage through observable change.

## 5. Environment deliverables

Choose the lightest sufficient form:

- **Compact environment prompt**: default for simple or one-off locations. Write one directly usable paragraph covering visible spatial layout, main materials and wear/natural traces, time/weather/atmosphere, light direction and temperature when useful, and two or three irregular identifying details. Keep it local to what the shot can see; do not invent a full map. No reference image is required.
- **Structure line art**: add only for recurring locations whose entrances, levels, paths, openings, occlusion, or fixed landmarks must remain consistent. Use an empty high-oblique ultra-wide view with geometry, depth, elevations, contour hierarchy, and minimal tone.
- **Rendering language**: add to a structural package when consistent color, material, weather, atmosphere, shadows, haze, or reflections matter across clips.

Do not produce a top-down or overhead plan as a standard pre-analysis deliverable.

Environment prompts include no people, creatures, bodies, character equipment, assigned routes/positions, staging zones, sight cones, narrative functions, or future-use instructions.

Natural sites: irregular microtopography and boundaries, varied tree age/spacing/crowns, layered plants/soil/stones/deadwood, interrupted paths, varied line density. Built sites: plausible skew, sag, uneven spacing, wear, stains, dust, repairs, and deformation.

In the storyboard place `环境参考：【名称】` once under the clip title only when an environment reference image is used. Each angle still describes its visible background. For a compact-prompt location, place the relevant environment wording directly in the shot or in the pre-analysis environment section for copy-forward use.

## 6. Adult/R18 and platform-safe appendix

When requested, keep the complete source-faithful adult/R18 master first. Append only affected complete replacements under:

```markdown
# 附录：平台安全替换稿
## 【平台安全替换·片段N】标题
```

Safe blocks retain timing, story function, continuity, voice, sound, and recognizable non-adult anchors. They are explicit adaptations, not coded moderation bypasses or approval guarantees.

## 7. Compact audit

- Source text/order/speakers/results match originals and neighbors.
- Every cited crop has a readable reproduction point and correct hand/prop assignments.
- Added motion enriches rather than displaces the source.
- Timecodes are integer, continuous, natural, and ≤15s.
- Each block has fields in order; every voice has parentheses; no BGM.
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
画面内容：……“……”（……）音效：……
```
