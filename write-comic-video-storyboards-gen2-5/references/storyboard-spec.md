# Storyboard specification

This file is the single authority for storyboard content rules. Read it for a new episode or substantial rewrite.

## 1. Source and references

Use originals for missing text, context, and order; use crop filenames for formal references.

Use a layered inspection pass:

1. Review all panels at 360–480 px only to recover order, text, locations, continuity, and risk.
2. Draft contiguous batches of about 3–6 panels after reopening that batch at about 720 px. Inspect the current panel and immediate neighbors and write before moving on.
3. Open original resolution only for unusual/strong perspective, fast action, overlapping limbs, hand/prop contact, complex creature or prop structure, heavy occlusion/effects, off-frame causes, or unresolved detail.
4. Audit the completed batch while its images remain open; at episode level reopen only flagged risk shots.

Before interpreting story function, freeze one compact internal **screen-fact lock** for the current panel: visible subjects and screen placement/facing; viewpoint/scale; visible hands, props, contacts, and occlusion; physical versus abstract background. Keep it terse and do not output it. Story continuity may explain the panel but cannot add a visible noun or relation to this lock.

Use `分镜参考` only when the referenced sub-shot matches the crop's:

- viewpoint and scale;
- subject count, placement, overlap, pose, silhouette, and gaze;
- left/right hand and prop assignment;
- foreground, background, occlusion, or abstract-effect hierarchy.

The reference may appear at the opening, middle, or endpoint. It need only become clearly readable; do not force a static hold. A different composition later in the same time block requires an explicit hard cut or uncited 补格/reverse-shot phase. Partial borrowing of identity, costume, prop, or background receives direct description but no formal citation.

When adjacent panels explicitly supply successive phases of one continuous action, keep the source-continuous action unit in one generated clip whenever it fits the model limit. List crop references in phase order within the relevant numbered shot, using internal hard cuts only when viewpoint changes. Each cited composition must become readable at its own phase. Never bury a reference-analysis note such as “参考上一格” inside the generatable description.

Judge vertical angle from camera position and visible perspective, never from head tilt or gaze. Keep horizontal viewing direction (`正面／略微斜侧面／斜侧面／纯侧面／背面`) separate from frame placement (`左侧三分之一／中央／右侧三分之一／边缘`). Never use `中央` as an uncertainty fallback.

For a cited crop with multiple subjects, strong occlusion, asymmetric placement, strong foreshortening, or plausible left/right confusion, create one compact internal composition lock before drafting. Record only visible screen facts, for example: `A=左侧前景/占幅大；B=右侧中景/被A遮挡；道具=由中部斜向右上`. Screen-left/right, depth, overlap, and prop direction are independent from speaking order, story importance, facing direction, and inferred world-space orientation. Do not output this lock.

Also trigger the composition lock for an unusual single-subject viewpoint such as floor-level, between-leg, extreme top-down, extreme low-angle, or strong foreshortening. For a complex creature, articulated object, unfamiliar tool, or adult prop, add a compact **topology lock**: count, connected parts, fixed and moving ends, visible gripping hand(s), contact point, and background type. Do not infer repeated parts, hidden hands, or connections from the object's story function.

After drafting that shot, mechanically compare every positional and action phrase in the compact description with the lock. Reject any swapped subject, reversed depth/occlusion, changed prop direction, or dialogue-order-based restaging. Use this gate selectively; ordinary single-subject or unambiguous crops need no lock.

Story continuity does not equal current-frame visibility. A previous-panel prop may still exist off-frame, but it may reappear only in a crop that shows it or in an uncited shot that positively establishes it. A gaze direction does not prove its target: when the current composition omits the supposed target, write only the visible screen-relative direction—such as `看向前方`, `看向画面下方`, or `转向左侧画外`—instead of naming the off-frame prop, person, or location.

After drafting, compare every visible person, prop, body part, contact, and background noun against the screen-fact lock or an explicitly cited adjacent action phase. Delete unsupported items or move a necessary composition change to an uncited shot.

## 2. Beat and action decision

Classify before adding motion:

- **State**: ongoing travel, waiting, rest, observation, vigilance, mood, or atmosphere. Continue the shown state with restrained gaze/expression, visible cloth/prop movement, medium response, environment, and light.
- **Action**: a process or result whose change matters. Identify the source-visible phase: preparation, execution, immediate response, result, or settled endpoint.
- **Reaction**: optional tag on State or Action. Choose only the minimum useful phase from perception, immediate response, readable emotion, recovery, or decision; never require the whole chain.
- **Mixed**: name the primary and secondary function and preserve both.

For a shown action B, default to B itself. Add at most one source-supported preceding phase A, following phase C, or a refinement of B when it materially improves continuity. If adjacent panels explicitly show A and B, connect A→B directly and cite both phases; this does not authorize an inferred C or complete action chain. An addition is admitted only if:

1. **Evidence**: the current or adjacent source supports the event;
2. **Visibility**: it can be seen in the declared framing and occlusion;
3. **Anchor safety**: within a cited sub-shot it preserves pose, hands/props, overlap, and composition.

If A or C changes composition, introduces a newly visible person/prop/contact, or leaves the crop, make it an explicit uncited shot. Do not invent off-frame bracing, hidden contact, props, body mechanics, travel paths, setup, follow-through, or recovery merely to complete motion.

When the source supports motion detail, state only the visible active hand, support limb, contact, movement direction, and endpoint that improve generation. Keep the same prop name and visible material/color through the beat. Do not trade anchor accuracy for a fuller-looking action.

Treat emotion as another inference that needs evidence. Strong labels such as fear, rage, grief, or mixed extremes require support from at least two of dialogue meaning, facial performance, and adjacent story context. Punctuation, speed lines, or an exertion grimace alone are insufficient; prefer observable, lower-inference performance such as strained, confused, impatient, startled, or embarrassed.

Long or dense dialogue may use a reverse shot, environment, prop, hand, or detail insert. Preserve event order and do not invent a new event.

When one comic panel contains multiple dialogue turns, choose one coverage strategy before splitting: continuous shared composition, speaker/listener reverse coverage, or a source-compatible environment/prop/detail insert. Added coverage may clarify an already established action, space, emotion, or rhythm, but cannot create a new event or displace the source-important composition. A new numbered shot must change at least one of subject focus, scale, viewpoint, composition, visible information, or dramatic function. A speaker change alone is not a visual increment. If two adjacent shots repeat the same reference and camera purpose, merge them; if the second needs a new composition, make it an explicit uncited hard cut or cite a different matching crop.

## 3. Timing and segmentation

Treat 15 seconds as a soft maximum. In each clip, reset shot numbering at 1 and label blocks `分镜N（X秒）`, where `X` is a positive integer duration. Sum durations instead of using start/end timecodes; split rather than accelerate.

Fallback non-dialogue timing:

| Beat | Typical time |
|---|---:|
| Micro reaction, glance, or discovery | 1–2s |
| Single reveal, fall, pull-out, or sudden vocal burst | 2–4s |
| Sustained effort or repeated struggle | 3–6s |
| Evolving state or atmosphere | 4–8s when visibly justified |

End the clip when the beat is complete. Never extend a short action with prolonged screaming, shaking, static holding, or camera motion merely to reach 15 seconds.

Time dialogue shots as `required pre-action + max(speech, concurrent performance) + required post-action`. Gaze shifts, expression changes, nods, small gestures, and posture adjustments normally run during speech and add no separate time. Add time only for actions or pauses that must occur before or after the line.

For dialogue-risk panels, use the internal ledger and complete its one-to-one source check before drafting. Sum sequential line estimates within each target shot; the shot's integer duration must be at least the rounded-up total. Establish clip boundaries after this calculation. The 15-second ceiling never authorizes shortening speech or dropping a source bubble.

Fallback Japanese speech timing:

| Line | Typical time |
|---|---:|
| Interjection or very short phrase | 1–2s |
| Short sentence | 2–4s |
| Medium sentence | 4–6s |
| Long explanation | 6–9s |
| Two connected long clauses | 8–12s |

Prefer boundaries at a location/time change, completed entrance/exit/reveal, dialogue turn, emotional reaction, or stable result. Never place a clip boundary inside a source-continuous physical action when the complete action unit fits within 15 seconds. Use hard cuts by default. A useful listener reaction absent from the speaker crop may be an uncited hard-cut sub-shot while dialogue continues off-screen.

## 4. Direct-prompt format

Each numbered shot block is a timed shot group with one total integer duration. Internal microcuts and cited phases are deliberately untimed so the video model can distribute them according to the stated rhythm. The block contains optional phase-specific `分镜参考 [crop.jpg]` lines and compact, directly generatable prose. Write in this approximate order without field headings:

1. vertical angle, meaningful horizontal direction, and scale;
2. essential placement, depth, prop relation, and occlusion;
3. one concise camera behavior, including a fixed camera when appropriate;
4. visible start state, ordered motion and performance, dialogue, local background/light, admitted effects, and endpoint.

Do not output separate `景别：`, `构图：`, `运镜：`, or `画面内容：` fields. For a real internal hard cut, microcut, reverse shot, environment shot, insert, or supplement inside the same generated clip, start a new line with `硬切：`, `碎切：`, `反打：`, `环境空镜：`, `插入镜头：`, or `补镜：`, then describe the new view directly. A speaker change alone does not justify a new cut.

State rhythm only where it changes decisions: where movement holds, where acceleration sharply increases, where in-betweens concentrate for legibility, where a brief slow-motion phase occurs, where impact compresses to one or two frames, and where the result settles. Internal sub-shots do not receive fixed durations. Descriptive phrases about speed, weight, impact, tension, pressure, or battle intensity are useful only when tied to visible staging or timing.

Every shot must describe all useful local background information actually visible in its framing. First classify it as physical environment or abstract comic background. For physical space, include whatever is present: foreground occluders, surfaces, objects, terrain, vegetation, architecture, depth layers, sky/weather, light/shadow, wear, and natural irregularities. For a source-supported solid, gradient, speed-line, or emotion background, preserve that function and do not restore the off-frame physical location. Detail is not capped; completeness is determined by visibility and generation value.

After every spoken or narrated sentence add `（音色、语气、情绪；必要时语速、停顿、重音）`. Storyboard blocks contain no sound effects, ambience, Foley, breath sounds, silence cues, BGM, or music.

Write only directly generatable visuals. Exclude asset planning, estimates, operator notes, moderation reasoning, partial-only references, and reference-analysis language such as “保持原格姿势／与原格一致／原格中／按照原格处理／依照参考图”. Do not use negative control prose such as “不出现湖岸实景／不增加其他人物／不要改变构图”; replace it with the positive visible background, subject set, composition, and motion. Use stable prop nouns; specify left/right hand, support limb, contact, direction, and endpoint only when source-supported and visible.

Use visually explicit creature and special-object names. When no matching reference asset is provided, replace lore-only names with a stable description containing the most useful visible anchors—normally scale, dominant color, surface/material, body type, and defining anatomy. Repeat the full description at the first appearance of each independently generated clip; shorten it consistently only within that clip.

Speed lines, solid backgrounds, and gradients are optional only when source-supported or genuinely useful to the beat. Monochrome manga effects may be colorized while preserving their visual purpose. Directional air distortion, screen wash, pressure ripples, brief black-white impact frames, camera response, and moving reflections require a matching speed, force, material, or light event and must preserve the cited pose and space. Rim light, lens flare, floating particles, glow, and volumetric beams require a visible source effect, an established physical light source, or a specific story need; never add them as generic beautification or subject separation.

## 5. Environments

Provide a compact prompt for every location, including locations that also receive structural assets.

- Simple or one-off: compact prompt only.
- Recurring and spatially complex: empty high-oblique structural line art, rendering language, and compact prompt.
- No standard top-down plan.

Environment assets contain physical space, materials, wear/natural traces, weather, and light only—no people, creatures, equipment, routes, staging zones, or narrative functions. Natural sites should be irregular and accumulated; built sites should be nonuniform, worn, repaired, and plausibly used.

Place `环境参考：【名称】` once below a clip title only when an environment image is actually used. Each shot still describes every visible local background element.

## 6. Adult master and platform-safe appendix

When requested, write the complete source-faithful adult/R18 master first without deleting, euphemizing, or overwriting content. Append complete replacements only for affected clips under:

```markdown
# 附录：平台安全替换稿
## 【平台安全替换·片段N】标题
```

Replacements preserve timing, story function, continuity, dialogue intent, and recognizable non-adult anchors. They are adaptations, not moderation-bypass promises.

## 7. SRT after approval

After storyboard approval, create `<storyboard-basename>_中文台词顺序表.srt` unless requested earlier. Do not create a Markdown dialogue table unless requested.

- Accumulate each clip's ordered shot durations into one continuous episode timeline.
- Split multiple turns into ordered, positive, non-overlapping entries.
- Output Chinese subtitle text only: no roles, Japanese, voice notes, camera notes, or production notes.
- Mark timing provisional when no final voice track exists.
- Generate a separately named safe SRT when replacement dialogue exists.

## 8. Audit

Structural validation checks format, shot numbering/durations, references, forbidden audio/meta text, and voice parentheses. It does not prove source fidelity.

Manually audit:

- source order, text, speakers, event, and result;
- current-panel screen facts before continuity; reject any visible noun supported only by the surrounding story;
- reference composition, angle, placement, hands/props, and occlusion at the exact declared phase; for a triggered composition lock, confirm screen-left/right, depth, overlap, and prop direction against the finished shot;
- for a triggered topology lock, confirm count, connections, visible hands, fixed/moving ends, contact, and background type;
- State/Action classification and every added A/B/C phase;
- adjacent repeated references and whether every numbered shot has a real visual or dramatic increment;
- complete visible local background;
- natural speech/action time and clean hard-cut boundaries;
- dialogue-risk ledger count against the still-open panel, bubble order/speaker/kind, exact target mapping, and rounded-up speech time;
- evidence for strong emotion and nontrivial lighting/effects;
- stable prop naming plus visible hand/support/contact/direction/endpoint anchors;
- source-continuous actions remain inside one generated clip unless they exceed the limit, and any split occurs at a stable pose with a fully restated continuation state;
- every animation effect has a visible cause, direction, endpoint, and single dramatic function without hiding a source anchor;
- unchanged adult master and complete safe replacements.
- safe replacements retain the corresponding main clip's shot-duration pattern unless a documented turn-count change requires a different split.

Template:

```markdown
## 【片段1】标题
环境参考：【环境A·版本】

**分镜1（3秒）：**
分镜参考 `[00.jpg]`
平视中近景，人物位于画面右侧三分之一；固定镜头。人物……“……”（……）。身后可见……，动作结束在……。
```
