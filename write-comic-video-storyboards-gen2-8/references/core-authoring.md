# Core authoring contract

This file owns source evidence, phase-specific anchors, temporal action design, clip boundaries, output fields, color, sound and the V3 ledger. Dialogue/performance decisions live in `dialogue-performance.md`; its cards supplement rather than replace the physical action phrase.

## Evidence and batch discipline

Evidence precedence is: current open panel; explicit supplied character/environment/prop/palette reference; adjacent panel only for chronology or continuous motion; story context only to decide what to inspect. An adjacent panel or ledger never proves current visibility.

Draft one to three contiguous panels at a time with their 720p proxies open. A contact sheet is insufficient for exact composition. Escalate only unresolved small text, identity, hand/contact, overlap, topology, perspective or fast motion to original resolution, and record the reason.

Freeze only decision-changing image facts before interpreting the scene. `composition_lock` records angle/scale, crop/layout, depth and overlap. `source_facts.entities/actions/relations` are short atomic allowlists copied from renderable visual evidence. Printed manga overlays belong in `page_overlays`, not in the background, composition lock or source facts: this includes SFX glyphs, speech balloons, caption/label boxes, page numbers, borders and other page furniture. `story_context` records plot meaning, continuity-only identity and dialogue intent for reasoning only; `non_renderable_terms` names context words that would create unsupported people, objects or actions if they leaked into generatable fields. Never move an item from context or a page overlay into source facts without reopening image evidence.

An SFX overlay may supply only a concrete audio cue. Do not describe its language, shape, color, size or screen position in a generatable field. When a panel has no renderable visual content beyond typography/page furniture, mark it `renderable_visual: false`, map its SFX to the nearest adjacent visible shot, and create no standalone visual shot for that panel.

Treat those facts as a current-shot closure. Every named target of gaze, gesture, touch, transfer, movement, camera tracking, light/effect or sound must be established in the current source-locked or approved derived view. A person/object known only from adjacent panels, dialogue or story context is not renderable in this shot. If the image proves only direction, write `看向画面左侧外/镜头下方/画面右侧` rather than naming the unseen target. Apply this to all targets, not gaze alone.

Dialogue and plot intention are lookup hints, never motion evidence. A line meaning `快跑/抢攻/把它给我` cannot by itself authorize running, attacking or handing over. Admit substantive displacement, body reorientation, contact change or prop operation through the temporal action design below; a failed candidate is rejected, not a reason to freeze all other supported movement.

## Source locks and temporal action design

Restore facts first, extend their time course second. This is a normal authoring step for every shot, including shots with no D/P/G flag. A comic supplies a visible phase, not a requirement that the entire video remain in that pose.

Distinguish two scopes in the existing lock/evidence entries:

- **Persistent constraints:** established participant/object identities, anatomy and object connections, hand/prop ownership, supported space/action axis and backing authority. These cannot change merely for animation polish. Visible count/overlap/contact at the source instant belongs to the phase anchor: the same established person or hand may enter the crop during an admitted transition; this is not an extra person or hand. A changed physical relation needs supplied phase evidence or the bounded necessary-transition admission below; local expressive pose development follows its own boundary below and cannot authorize a new contact or event.
- **Phase-specific anchor:** exact viewpoint/scale, placement/depth/overlap, silhouette, gaze, visible limbs, grounded state and hand/grip/contact configuration at the cited instant. For a comic reference, declare `anchor_phase` as middle, contact, result or endpoint. The full source composition must be recognizable there; supported displacement, expression or pose development before/after it need not match that instant at every frame. At the anchor, every original relation still matches. A changed camera setup remains separate justified coverage.

Select the physical phase before drafting the opening. **Never lock the original comic panel/crop to the video's first frame or submit it as a start-keyframe asset.** Comics normally show a process or result, not the beginning of the animation. Restore their composition as an in-process/contact/result anchor; do not relabel a depicted B as A to suit a tool's input mode.

Design the independent opening from a supplied earlier phase, an admitted necessary transition or an evidenced continuing state. A genuinely preparatory panel still needs its physical phase identified correctly; do not invent another action just to move its reference later. For already ongoing travel/contact or a purposeful held state, preserve that continuity without replaying a lead-in. A similar opening pose is not inherently forbidden; binding the comic image as the first-frame control is.

Execution must support this reference role. If a tool would bind the supplied comic to frame zero, change to a compatible reference workflow or use a separate opening asset based on the approved opening, only when preparing that asset is authorized. If neither is available, report the execution blocker instead of deleting A, freezing B or claiming the prompt alone can override the tool. A separate opening asset is not the original comic reference; retain the later comic anchor.

Classify the visible beat:

- `State`: an ongoing condition, including travel or sustained effort; continue its evidenced activity. State does not mean motionless.
- `Action`: identify whether the image shows preparation, execution, contact, response, result or settlement.
- `Reaction`: select the useful evidenced perception/response/settlement rather than inventing a full emotional chain.
- `Mixed`: preserve the primary physical phrase and secondary function.

For shown phase **B**, actively assess a preceding **A**, following **C**, or temporal development within **B** when it makes the existing beat readable. A/B/C are relative physical phases, not image order, opening/middle/endpoint positions, or the `B` beats and `C` coupling labels of the P-card. A hand already at an ear or arms already enclosing someone establishes execution/contact B for that gesture, not preparation A merely because it is the first image of a shot. Add at most one inferred connective A or C; this does not limit development within the depicted B. When adjacent panels explicitly supply several continuous phases, connect those phases in order without inventing another result.

### Necessary transitions, not new events

A panel that visibly establishes an action/contact can support its **shortest compatible local lead-in**, even when no other panel draws the preparatory pose. This is bounded animation inference, not a directly observed source fact. When the action begins in this beat, include an admissible lead-in by default instead of opening already posed at B; checking a box that A was considered is insufficient. Use the current pose, active side, contact target, visible direction, motion cues and adjacent continuity to constrain it. If the exact path is underdetermined, choose the simplest local approach compatible with those constraints, not a complex invented route.

Admit it only when it uses the same established actor/limb/object and target, performs the same depicted action, reaches the source pose/contact, fits the visible crop, and adds no independent event, new prop, hidden support/contact, changed ownership or new consequence. Examples: lift the established right hand into the crop to reach the depicted ear contact; bring already established participants together to form the depicted embrace. A hand can start just below a frame edge; describe its visible emergence and trajectory without inventing what it did off-screen. Do not add pocket-searching, a tool, extra walking steps, a run-up, a jump, a detour or a later release to make the action feel complete.

For `第9話_24_002`, the anatomical right hand appears on screen-left. Unless preceding continuity already establishes ongoing ear-picking, use right-hand lift/entry → index finger reaches the right-ear anchor → local finger/wrist motion compatible with the shown gesture. Do not open with the finger already parked at the ear by default. For a newly initiated embrace such as `第9話_19_002`, use a short approach from the source-compatible side → arms close into the depicted embrace; restore the exact two-person placement/overlap at B. These examples illustrate the admission boundary, not mandatory gestures for unrelated panels.

Do not replay a lead-in when adjacent continuity establishes the gesture/contact is already sustained or when the source intentionally presents a held state. A tool's first-frame constraint is an execution incompatibility to resolve above, not a reason to omit the admitted transition. Reject or narrow a candidate when limb ownership, target or contact mechanics remain materially ambiguous. Record that specific reason; “A was not drawn” alone does not justify replacing an admissible lead-in with tiny B-only motion.

### Bounded expressive pose development

The visible attitude, task/posture and a supported immediate stimulus may ground a local head-facing, head-pitch/tilt or visible shoulder/torso adjustment within the same beat. Admit a candidate when its purpose is consistent with that evidence, its useful extent fits the framing, it preserves persistent constraints and required sustained contact, and it restores the source pose/orientation at the declared anchor. Every intermediate pose need not be separately drawn. Dialogue alone does not establish a new reaction, stronger emotion or absent target; references establish design, not permission to invent behavior. Keep observed facts in `source_facts` and identify this inferred development in the existing admission and `motion_decision`.

A head turn at a fixed camera is actor motion, not a new camera angle; it does not need a new shot merely for changing face orientation. It may not mirror the panel, invent an unseen prop/costume surface or anatomy, or expose an unresolved character design. Use supplied design references where needed; trigger G for decision-changing geometry, and narrow or reject the turn if it cannot be resolved. Head direction is a phase anchor, not an all-frame lock, but sustained grip/support/contact can limit how far the body turns. Local expressive development within B does not consume a separate inferred A/C connective for every pose; it also does not authorize walking away, a new prop operation, release, transfer or any independent physical event.

For each substantive candidate record the existing action admission: `visual_evidence`, `visible_in_framing: true`, and `anchor_safe: true`. In `visual_evidence`, separate the observed pose/vector/contact/attitude from any inferred necessary transition or expressive pose development and explain how the latter meets its boundary above. Anchor safety means restoring the cited phase **and** preserving persistent constraints, not keeping every joint fixed throughout. The start/end positions and path must fit the source constraints and crop. An admitted formation of the source contact is not an additional contact event; hidden bracing, grip changes, hand-offs, rebound, recovery or new results still need their own evidence. An uncited shot solves a justified composition change, never authorizes an unrelated event.

Keep one concise `motion_decision` in the existing shot record: beat kind, physical source phase, anchor placement in the video, selected development with direct/inferred basis, or the specific reason for a held state/omitted lead-in. It is authoring metadata, not a new ledger version or mechanical guarantee. Complete it before final action prose; do not retrospectively justify a frozen draft.

Render the admitted phrase in `【可见动作】`: positive starting pose/contact → visible body/object change with direction and useful extent/speed → cited anchor at its declared phase → supported endpoint. Use supplied stages and admitted necessary transitions, without labeling inference in generatable prose. A moving beat needs a readable change in the main body/object state; lips, a blink, tiny shoulder/finger adjustments, hair and dust are supporting layers, not substitutes for that change. In an ear-picking shot the finger motion performs B, but does not replace an admitted hand-lift A. Do not qualify every movement as `微微/极小/轻轻` to satisfy grounding; choose magnitude from evidence and framing, not a movement quota. A deliberate hold, fragile contact or neutral state remains valid with appropriate duration; unsupported additional events remain excluded.

Review source fidelity and motion realization separately while the image is open: can the animator locate the source anchor, and can they recover the admitted temporal change from the action field alone? An Action draft that opens and ends in the same B pose with only mouth/hair/particle movement needs replanning or an explicit supported hold decision. Neither a completed P-card, camera movement nor zero validator errors proves that the physical phrase is animated.

Strong emotion requires support from at least two of dialogue meaning, visible face/body performance, and adjacent story context. Prefer observable lower-inference behavior when evidence is incomplete.

Estimate non-dialogue beats naturally: micro-reaction/glance/discovery about 1–2s; a single reveal/fall/pull-out/burst about 2–4s; sustained effort about 3–6s; evolving state/atmosphere about 4–8s only with visible development. These are planning guides, not quotas. End when the beat is complete; do not pad with static holding, repetitive shaking, particles or camera drift toward 15 seconds. Combine serial/concurrent motion and speech under the dialogue module before rounding shot duration.

## Character identity and canonical names

Use one project character registry, embedded as optional `character_registry` in the existing V3 ledger or supplied as a project reference; do not maintain two competing name maps. An entry records a stable `id`, `canonical_name`, actual reference path(s), aliases, discriminating design traits, and confirmation status. A filename can supply the user's canonical name, but only a visual match or an explicit user mapping establishes which comic character it names. Group verified reference variants under one identity; do not infer a name from a generic filename or map a multi-character sheet without identifying its subject.

Match current visible traits such as ear shape, hair silhouette, distinctive costume construction or markings. Color-only traits cannot establish a match in monochrome panels. Shared hair color, dialogue order, plot continuity and expected presence nominate candidates, not proof. A cropped/back-view occurrence may use a confirmed name only when the visible traits or an explicit supplied mapping support that occurrence. Otherwise retain a stable role label or the explicit original name and record the unresolved candidate; never force a best guess.

Render confirmed canonical names consistently in camera, action, background, speaker, lighting and sound fields. Retain visual anatomy/material descriptions where useful (`青的尖耳`, `欧铂的角状盔面`); do not leave a known character under an interchangeable label such as `浅发少女`. A named off-screen speaker does not establish that person's visual presence or authorize a named gaze target. References establish identity, not the current pose, contact, props, backing or costume variant. Explicit monochrome output remains monochrome even when identity references are colored.

When identity is revised, preserve original bubble text and the previous evidence. Record the mapping basis at the affected occurrence, then synchronize names in prose, speaker mappings, facts and exact excerpts. Mechanical replacement alone is not a visual audit.

## Change-scoped risk reinspection

Finish the source comparison before leaving each drafting batch. After a batch is approved, reopen only images whose decision-changing evidence is unresolved or affected by a later edit:

- name/identity: affected occurrence and relevant character reference;
- crop, axis, movement path or landing: owning panel; immediate neighbor only when continuity or added-coverage contrast depends on it;
- visible action, contact, count, backing or color: owning panel and only the adjacent evidence actually used;
- unreadable dialogue or changed ownership: original bubble region and relevant continuation.

Punctuation, numbering, field formatting and arithmetic-only fixes need mechanical checks, not image reinspection, provided their visual/speaker/semantic claims are unchanged. A heuristic warning first needs classification: resolve a purely lexical false positive from the relevant fields; reopen images when the disposition depends on visual evidence. Never waive an entire warning class.

Keep a compact `revision_audit` in the existing ledger when revising: affected targets/images, reason, resolution, decision and reviewed scope. Preserve earlier audit history; a text-only edit cannot set a new visual-pass attestation. Reuse valid 720p proxies and escalate only an unresolved detail that could change the decision. Final order/coverage/timing/identity-consistency checks do not require reopening every approved panel. Reopen the whole set only when source order/scope changes invalidate the earlier audit or a demonstrated systemic error requires it.

## Shot authority

- `source_locked`: restores a cited panel's complete composition at its declared middle, contact, result or endpoint; never binds that comic asset as frame zero.
- `source_supported_phase`: adds a supplied continuous phase or an admitted necessary transition into the current source action; preserve axis, ownership, topology and the source endpoint, and distinguish direct evidence from inference in its admission.
- `uncited_coverage`: a separately numbered speaker, listener, relationship, object, environment, detail or action-phase view with stated source owner and purpose. It cannot create a new event, identity, object, route, contact or result.

A formal citation is used only when the full composition matches. Adjacent numbered shots never repeat the same formal citation. Keep the matching view cited once; derived views are uncited and must be meaningfully different.

Before writing an `uncited_coverage` shot, make one compact internal coverage strip for the current panel-owned unit: `visual function | dominant subject | scale | viewpoint/axis | placement/overlap | visible information`. Compare each candidate with the immediately previous planned shot and, by looking ahead one panel, the next source composition. It must change at least two meaningful dimensions against each available neighbor. Focal-length changes, focus pulls, small reframes or tighter crops of the same subject placement do not count by themselves. If the contrast cannot be achieved from visible evidence, merge the beat or choose a different supported speaker/listener/object/environment/detail view. This is a pre-draft gate; ledger labels never substitute for the comparison.

## Clip and coverage boundaries

A clip is one generated video. Fifteen seconds is a hard ceiling. Keep a continuous physical phrase and one panel's complete coverage unit together when they fit.

The cited view and every derived speaker/listener/object/environment/detail view owned by one panel stay in one clip. If correct semantic splitting and natural Japanese timing still make that single-panel unit exceed 15 seconds, it is the only allowed overflow: keep it together, mark `manual_overflow`, and surface a prominent manual warning for the user. The exception cannot combine several source panels, unrelated events or padded holds.

If a continuous physical phrase must split, end at a stable state and fully restate the next opening. Every clip resets visible people/counts/relations, off-screen direction, pose, grip/contact, backing, light and stable labels. Never use `保持原有/上一格/上一镜/只放大上一格/沿用前镜` or negative controls such as `不新增/不要/不出现` in generatable fields.

## Required output

```markdown
## 【片段1】
**分镜1（6秒）：**
分镜参考 `[00.jpg]`
【镜头设计】：角度与轴线、景别/焦段、裁切与主体布局、深度/遮挡、焦点、主运镜和落幅。
【可见动作】：明确当前姿态与已建立的任务/接触，写出回应此情境的获准主动作或可读姿态变化，交代必要衔接、顺序/交叠和清楚的落定状态；表情与次级运动按需补充。
【可见背景】：镜头内可见的物理环境、明确图形场或铺满画面的表面及其层次和运动。
【台词与语气】：角色说：“……”（音色、语气、情绪、语速、停顿、重音、距离及必要声像）；无台词写“无台词”。
【光影布光】：光源、方向、遮挡、主辅光、局部高光、阴影和材质响应。
【声音设计】：环境底声、动作拟音、呼吸/身体声、静默及必要同步；不复述对白表演，不写BGM。
```

Keep all six fields separate and ordered. `【镜头设计】` alone contains static composition and camera behavior; `【可见动作】` is the single source of truth for subject/object motion and changing performance. Camera, background, dialogue, light and sound may describe only their own result and cannot restate or newly assert that motion. Page margins, gutters, OCR gaps, speech-bubble whitespace and all printed manga overlays are never background or video content. Sound cannot imply an unseen event or name its unseen source.

When several panels are successive phases of one camera setup, backing, axis and causal action, bind each panel to a separate phase bullet in `【镜头设计】` and use matching action-only bullets in `【可见动作】`. Otherwise create another numbered shot.

## Look, color and sound

State one reusable scene look with supplied or deliberately chosen work/studio/director references plus executable traits. Do not repeat the full style stack per shot.

Color precedence is: explicit direction/reference; verified colored occurrence of the same item; coherent production choice only for genuinely uncolored non-character elements. Screentone proves value/material/light, not literal gray. Lighting may tint but not rewrite base color.

`【台词与语气】` owns all speech treatment, including voice, emotion, pace, pause, stress, distance, direction and occlusion/reverb when relevant. `【声音设计】` starts with the continuous location bed, then adds only useful Foley, breath/body sound, silence and synchronization. It may say `句末/重音后` to place a non-dialogue cue, but must not say `喊声/对白/话音/尾音/语气/语速/音色` or otherwise repeat how a line sounds. Preserve environment audio and sound effects in both mother draft and execution prompt when the target supports audio. BGM, score, melody and theme music are excluded.

## Source ledger V3

Use `version: 3`. Create evidence before prose. The minimum is:

- root: `source_language`, `panels`, `shots`, optional `performance`;
- panel: image/viewing/resolution audit, `renderable_visual`, `page_overlays`, background, `composition_lock`, atomic `source_facts`, separate `story_context`, `non_renderable_terms`, bubbles and coverage;
- dialogue-risk panel: ordered semantic `dialogue_turns` plus ordered `coverage_groups`;
- shot: target, role, purpose/evidence, background excerpt, D/P/G flags and basis, exact `fact_claims`, and one three-gate `action_admission` for each major action;
- uncited shot: empty `source_images`, nonempty `derived_from`, `coverage_type`, at least two evidenced changes from the previous planned shot, plus at least two evidenced changes from the next source composition when one exists;
- `P` shot: one compact card plus exact rendered excerpts and interval estimate.

`dialogue_turns` preserve story logic; `coverage_groups` decide camera economy. A group may combine consecutive short turns only when total speech fits naturally, one setup carries the handoff without a hidden cut, and no key reveal/reversal/reaction loses its landing. Record a concise `merge_basis` for a multi-turn group.

`manual_overflow` is allowed only on one panel and names the target segment, natural estimated duration, reason and `manual_handling_required: true`. Validation must reject every other over-15-second clip.

Mechanical validation proves consistency, not visual truth. Final audit checks source order/result, composition, background, dialogue ownership/order, timing, clip cold start, supported coverage, performance, light/effects/sound and unchanged endpoint.

`fact_claims.entities/actions/relations` must copy atomic entries from the owning panels' `source_facts`; prose cannot use `non_renderable_terms`. Do not backfill an inferred preparatory pose into those observed facts. Record admitted necessary transitions in the existing action admissions/motion decision, explicitly tied to the observed B anchor. Major action verbs in `【可见动作】` must have a matching admission grounded in that visual evidence rather than dialogue/story meaning alone. Mechanical checks establish ledger consistency; the bounded-inference decision and motion realization remain a visual/manual audit.
