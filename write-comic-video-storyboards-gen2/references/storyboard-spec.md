# Storyboard specification

This file is the single authority for storyboard content rules. Read it for a new episode or substantial rewrite.

## 1. Source and references

Use originals for missing text, context, and order; use crop filenames for formal references. Inspect the current panel and immediate neighbors, expanding farther only when ambiguity remains.

Use `分镜参考` only when the referenced sub-shot matches the crop's:

- viewpoint and scale;
- subject count, placement, overlap, pose, silhouette, and gaze;
- left/right hand and prop assignment;
- foreground, background, occlusion, or abstract-effect hierarchy.

The reference may appear at the opening, middle, or endpoint. It need only become clearly readable; do not force a static hold. A different composition later in the same time block requires an explicit hard cut or uncited 补格/reverse-shot phase. Partial borrowing of identity, costume, prop, or background receives direct description but no formal citation.

Judge vertical angle from camera position and visible perspective, never from head tilt or gaze. Keep horizontal viewing direction (`正面／略微斜侧面／斜侧面／纯侧面／背面`) separate from frame placement (`左侧三分之一／中央／右侧三分之一／边缘`). Never use `中央` as an uncertainty fallback.

Story continuity does not equal current-frame visibility. A previous-panel prop may still exist off-frame, but it may reappear only in a crop that shows it or in an uncited shot.

## 2. Beat and action decision

Classify before adding motion:

- **State**: ongoing travel, waiting, rest, observation, vigilance, mood, or atmosphere. Continue the shown state with restrained gaze/expression, visible cloth/prop movement, medium response, environment, and light.
- **Action**: a process or result whose change matters. Identify the source-visible phase: preparation, execution, immediate response, result, or settled endpoint.
- **Reaction**: optional tag on State or Action. Choose only the minimum useful phase from perception, immediate response, readable emotion, recovery, or decision; never require the whole chain.
- **Mixed**: name the primary and secondary function and preserve both.

For a shown action B, default to B itself. Add at most one source-supported preceding phase A, following phase C, or a refinement of B when it materially improves continuity. An addition is admitted only if:

1. **Evidence**: the current or adjacent source supports the event;
2. **Visibility**: it can be seen in the declared framing and occlusion;
3. **Anchor safety**: within a cited sub-shot it preserves pose, hands/props, overlap, and composition.

If A or C changes composition, introduces a newly visible person/prop/contact, or leaves the crop, make it an explicit uncited shot. Do not invent off-frame bracing, hidden contact, props, body mechanics, travel paths, setup, follow-through, or recovery merely to complete motion.

Long or dense dialogue may use a reverse shot, environment, prop, hand, or detail insert. Preserve event order and do not invent a new event.

## 3. Timing and segmentation

Treat 15 seconds as a soft maximum. Use continuous integer timecodes and split rather than accelerate.

Fallback Japanese speech timing:

| Line | Typical time |
|---|---:|
| Interjection or very short phrase | 1–2s |
| Short sentence | 2–4s |
| Medium sentence | 4–6s |
| Long explanation | 6–9s |
| Two connected long clauses | 8–12s |

Prefer boundaries at a location/time change, completed entrance/exit/reveal, dialogue turn, emotional reaction, or stable result. Use hard cuts by default. A useful listener reaction absent from the speaker crop may be a separate uncited block or an explicit hard-cut sub-shot while dialogue continues off-screen.

## 4. Direct-prompt format

Each timed block contains, in order:

1. optional `分镜参考 [crop.jpg]`;
2. `景别：` vertical angle, meaningful horizontal direction, and base scale only;
3. `构图：` essential placement, depth, prop, and occlusion only;
4. `运镜：` one concise base instruction, including `固定镜头` when appropriate;
5. `画面内容：` visible start state, ordered motion, performance, local background/light, dialogue, camera changes, and endpoint.

Do not repeat the same information across fields. Put timed or multi-stage changes inside `画面内容`.

Every shot must describe all useful local background information actually visible in its framing. Include whatever is present: foreground occluders, surfaces, furniture/objects, terrain, vegetation, architecture, depth layers, sky/weather, light/shadow, wear, and natural irregularities. Detail is not capped; completeness is determined by visibility and generation value. Do not copy an entire environment package when it is outside the frame, and do not invent unseen space.

After every spoken or narrated sentence add `（音色、语气、情绪；必要时语速、停顿、重音）`. Storyboard blocks contain no sound effects, ambience, Foley, breath sounds, silence cues, BGM, or music.

Write only directly generatable visuals. Exclude asset planning, estimates, operator notes, moderation reasoning, partial-only references, and meta-language such as “保持原格姿势／与原格一致／原格中……”. Prefer positive visible results over negative instruction stacks.

Speed lines, solid backgrounds, and gradients are optional only when source-supported or genuinely useful to the beat. Monochrome manga effects may be colorized while preserving their visual purpose.

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

- Convert clip-local timecodes into one continuous episode timeline.
- Split multiple turns into ordered, positive, non-overlapping entries.
- Output Chinese subtitle text only: no roles, Japanese, voice notes, camera notes, or production notes.
- Mark timing provisional when no final voice track exists.
- Generate a separately named safe SRT when replacement dialogue exists.

## 8. Audit

Structural validation checks format, timecodes, references, forbidden audio/meta text, and voice parentheses. It does not prove source fidelity.

Manually audit:

- source order, text, speakers, event, and result;
- reference composition, angle, placement, hands/props, and occlusion;
- State/Action classification and every added A/B/C phase;
- complete visible local background;
- natural speech time and clean hard-cut boundaries;
- unchanged adult master and complete safe replacements.

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
