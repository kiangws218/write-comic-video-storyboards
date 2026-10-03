# Core authoring contract

This file owns source evidence, phase-specific anchors, temporal action design, clip boundaries, output fields, color, sound and the V3 ledger. Dialogue/performance decisions live in `dialogue-performance.md`; its cards supplement rather than replace the physical action phrase.

## Evidence and batch discipline

Evidence precedence is: current open panel; explicit supplied character/environment/prop/palette reference; adjacent panel for chronology/continuous motion and the bounded background-continuity admission below; story context only to decide what to inspect. An adjacent panel or ledger never proves current visibility. Admitted environment reconstruction is a production decision, not a claim that the current manga panel draws it.

Draft one to three contiguous panels at a time with their 720p proxies open. A contact sheet is insufficient for exact composition. Escalate only unresolved small text, identity, hand/contact, overlap, topology, perspective or fast motion to original resolution, and record the reason.

Freeze only decision-changing image facts before interpreting the scene. `composition_lock` records angle/scale, crop/layout, depth and overlap. `source_facts.entities/actions/relations` are short atomic allowlists copied from renderable visual evidence. Printed manga overlays belong in `page_overlays`, not in the background, composition lock or source facts: this includes SFX glyphs, speech balloons, caption/label boxes, page numbers, borders and other page furniture. `story_context` records plot meaning, continuity-only identity and dialogue intent for reasoning only; `non_renderable_terms` names context words that would create unsupported people, objects or actions if they leaked into generatable fields. Never move an item from context or a page overlay into source facts without reopening image evidence.

An SFX overlay may supply only a concrete audio cue. Do not describe its language, shape, color, size or screen position in a generatable field. When a panel has no renderable visual content beyond typography/page furniture, mark it `renderable_visual: false`, map its SFX to the nearest adjacent visible shot, and create no standalone visual shot for that panel.

Treat those facts as a current-shot closure. Every named target of gaze, gesture, touch, transfer, movement, camera tracking, light/effect or sound must be established in the current source-locked or approved derived view. A person/object known only from adjacent panels, dialogue or story context is not renderable in this shot. If the image proves only direction, write `看向画面左侧外/镜头下方/画面右侧` rather than naming the unseen target. Apply this to all targets, not gaze alone.

Dialogue and plot intention are lookup hints, never motion evidence. A line meaning `快跑/抢攻/把它给我` cannot by itself authorize running, attacking or handing over. Admit substantive displacement, body reorientation, contact change or prop operation through the temporal action design below; a failed candidate is rejected, not a reason to freeze all other supported movement.

## Background authority and field boundary

`【可见背景】` describes physical environment or non-diegetic graphic backing: location surfaces/landscape, useful layers, palette/texture and their own movement. Performer faces, skin, hair, costume, hands and the main prop are not background merely because they sit behind another body part. Static occlusion/layout belongs to camera; subject motion to action; highlights/shadows/material response to lighting. A wall or ground may fill a shot; a face or armor surface does not become environment by filling it. Established set furnishings may be scenery when they serve that role; do not ban every object or every cloth surface by vocabulary alone.

Resolve one of four modes before writing:

- **Physical:** retain the current panel's actual environment and geometry. Mood grading respects established base colors, rather than repainting known objects at each line.
- **Continuity:** when manga omits scenery during a continuous scene, prefer restrained reconstruction from inspected adjacent same-location views or a supplied environment reference. Admit only already established environmental portions compatible with current axis, crop, depth and occlusion. Preserve foreground placement/count/silhouette/contact. Do not expose an unseen room side, door, route, new furnishing or interaction target; dialogue alone cannot establish location. If geometry is uncertain, narrow to an established soft/distant plane and record the limit, or request the missing reference when it matters. This exception grants backing only, not new people, props, actions or named gaze/contact targets.
- **Graphic:** preserve or design an intentional emotional/comedic/impact field when this beat supports it. Gray gradients or blank areas alone cannot distinguish deliberate abstraction from manga economy; assess the scene and neighboring drawn environment. Physical scenery is the usual baseline, but there is no real/abstract percentage quota; a supported sustained stylized sequence remains legitimate.
- **Occluded:** when the established crop leaves no independent backing visible, write the factual visibility statement `独立背景完全被主体遮住。` (equivalent natural wording is valid). Keep subject detail in its owning fields. This is not a negative instruction; do not invent a colored sliver, widen the crop or mislabel a cheek/hair/armor as background to fill the field. Verify the full-frame crop semantically; the sentence itself is not proof.

For reconstruction, graphic selection/recoloring, occlusion or an ambiguous backing decision, record compact `background_decision` in the existing V3 shot: `mode` (`physical/continuity/graphic/occluded`), `basis`, and `source_refs` for continuity (registered inspected panel filenames, or absolute local paths to inspected adjacent-panel/environment references). Reuse `background_excerpt` for rendered text. Keep current-panel `background` and `source_facts` observational: `omitted` and `occluded` are valid panel background types. Do not backfill reconstructed scenery, production colors or decorative effects as drawn facts; do not relabel an intentional source graphic as an omission for convenience.

A cited foreground composition can remain source-locked with admitted omitted-background reconstruction or production palette choice; record the limited backing adaptation internally instead of claiming exact backing fidelity. Foreground/camera rearrangement still needs justified uncited coverage. Read `background-design.md` for treatments and research. No parallel background ledger or new ledger version.

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

Treat this as usable creative space, not an exception to request only after an inert draft. Within the established participants, framing, attitude, anatomy and sustained contacts, develop how they engage in the current exchange: head facing/pitch, visible shoulder/torso participation, an already established hand gesture or task, and their meaningful timing may work together. These choices are animation interpretation of the shown beat; they do not require a separate drawing of every intermediate pose. Do not reduce the whole performance because one proposed new event or hidden mechanism is inadmissible; reject that candidate and compose a fuller response from the remaining visible possibilities.

The visible attitude, task/posture and a supported immediate stimulus may ground a local head-facing, head-pitch/tilt, visible shoulder/torso lean or withdrawal, or weight shift within the same beat. Weight development needs an established stance/support or a visible upper-body result; it cannot invent a supporting foot, step, seat or off-screen brace. Admit a candidate when its purpose is consistent with that evidence, its useful extent fits the framing, it preserves persistent constraints and required sustained contact, and it restores the source pose/orientation at the declared anchor. Every intermediate pose need not be separately drawn. Dialogue alone does not establish a new reaction, stronger emotion or absent target; references establish design, not permission to invent behavior. Keep observed facts in `source_facts` and identify this inferred development in the existing admission and `motion_decision`.

A head turn at a fixed camera is actor motion, not a new camera angle; it does not need a new shot merely for changing face orientation. It may not mirror the panel, invent an unseen prop/costume surface or anatomy, or expose an unresolved character design. Use supplied design references where needed; trigger G for decision-changing geometry, and narrow or reject the turn if it cannot be resolved. Head direction is a phase anchor, not an all-frame lock, but sustained grip/support/contact can limit how far the body turns. Local expressive development within B does not consume a separate inferred A/C connective for every pose; it also does not authorize walking away, a new prop operation, release, transfer or any independent physical event.

Restoring the cited pose at its anchor does not require every response to end by returning to a neutral head or the opening pose. Carry a supported expressive endpoint into the next beat when compatible with source continuity. The inferred A/C limit applies to connective physical phases, not to the number of local expressive developments or concurrent acting layers within the same beat.

For each substantive candidate record the existing action admission: `visual_evidence`, `visible_in_framing: true`, and `anchor_safe: true`. In `visual_evidence`, separate the observed pose/vector/contact/attitude from any inferred necessary transition or expressive pose development and explain how the latter meets its boundary above. Anchor safety means restoring the cited phase **and** preserving persistent constraints, not keeping every joint fixed throughout. The start/end positions and path must fit the source constraints and crop. An admitted formation of the source contact is not an additional contact event; hidden bracing, grip changes, hand-offs, rebound, recovery or new results still need their own evidence. An uncited shot solves a justified composition change, never authorizes an unrelated event.

These explanations belong only in the internal ledger, never the formal storyboard's fields, parenthetical notes, comments or appendix. There, render positive executable starting poses, changes and endpoints, not `证据说明/推断依据/图像支持/准入通过` or an explanation of why the motion is allowed. Formal image-reference lines remain references, not an evidence essay. Mechanical action-family matching assists admission bookkeeping; equivalent wording does not authorize a different action, and unrecognized wording still needs semantic review. Clearly text-only evidence fails; mixed visual/context explanations and negations need meaning-based review, not rejection merely for mentioning `台词/剧情`.

Use a clear action name in the internal admission `claim` (for example `前倾/后仰/重心转移`), while keeping the formal action prose natural. If a wording-family mismatch is reported, compare the actual action and repair the internal mapping; do not alter good performance merely to satisfy a keyword, merge physically different actions or fabricate observed source facts.

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

A **panel** is a source anchor, a **shot** is one camera setup, and a **clip** is one generated video containing one or more numbered shots. Their boundaries are independent: a change of camera setup starts a shot, not automatically a clip; a new panel is not automatically either boundary.

Normally keep one panel's cited view and all its derived coverage in one clip: **one clip may contain multiple consecutive complete panel units.** This is non-fragmentation, not one-panel exclusivity. The natural single-panel overflow exception below is the only reason to split that unit across clips. Preserve distinct formal references for distinct source panels even when their shots share a clip.

Before opening the next clip, inspect the immediate chronological neighbor and choose the boundary from the enacted scene beat and natural timing:

- Prefer grouping an uninterrupted action and its immediate response/result, a short question/answer or stimulus/reaction, or compatible establishing/details within the same scene beat. Retain all source anchors and dialogue turns; use multiple numbered shots when camera setups differ. Do not silently fuse different compositions into one shot.
- Assemble consecutive complete units toward 15 seconds where natural, with total duration no greater than 15; this is a packing target, not a minimum or an excuse to pad. A 3-second prompt plus a 6-second answer can share one 9-second clip with two shots, and a supported following 6-second response can bring the same scene beat to 15. A fully supported 2+3+4-second continuous phrase can also remain one shorter clip at its actual dramatic landing. Do not shorten acting, accelerate dialogue or append a static tail to hit the target.
- Start another clip at a supported scene/time/causal discontinuity, a purposeful dramatic landing, or when the next complete unit would exceed the applicable limit. Short standalone clips are legitimate for these concrete reasons, not merely because a panel or drafting batch ended. Preserve a natural 11–15-second continuous unit rather than fragmenting it under an invented 10-second target. An explicit lower user ceiling instead requires a stable, source-faithful boundary.

Fifteen seconds is the default hard ceiling; use a lower explicit user ceiling when provided. If the complete natural Japanese dialogue and necessary admitted performance of a **single panel** still exceed it after correct shot planning, split that unit into consecutive clips at a complete speech thought/turn or stable action state. Prefer this to speeding speech, dropping information or thinning acting. Keep every resulting clip within the ceiling; cold-start the next clip with the actual continued pose/contact/attention, not a replay of the lead-in. Do not cut through a fragile contact or unfinished sentence merely to fill 15 seconds.

Record one compact `overflow_split` on that panel: `estimated_seconds` (natural full-unit estimate above the applicable ceiling), `segments` (the actual consecutive clip numbers), `boundary_reason` (specific semantic/action landing), and `continuity_state` (pose/task/contact carried into the next opening). Preserve one source bubble with ordered segments if its delivery spans shots; no duplication or omitted tail. Cite the full source composition once; genuinely different later coverage remains uncited with the usual contrast/admission checks. The metadata stays internal. A split tail may group with the next complete panel unit when the scene and remaining time permit; it need not become another tiny exclusive clip. Clips below the ceiling, convenient camera changes, unrelated intervening material and padded holds cannot justify this exception.

When no safe split can preserve the source phrase, retain the existing single-panel `manual_overflow` marker for explicit manual handling, not as a compliant over-limit video. This fallback cannot combine several panels, unrelated events or padded holds.

Inspection batches of one to three panels control working memory only. Keep the current clip tentative across batch boundaries and finalize it after the immediate neighbor is assessed; already audited prose need not be rewritten or every image reopened for this bookkeeping. At final review, audit adjacent short clips and an episode-wide one-panel-per-clip pattern for missed grouping. Record actual merge/retain reasons and affected targets in the existing `revision_audit` or `final_audit`, not the formal script. Duration-only validator hints identify candidates, not proof of scene continuity or an automatic merge instruction.

If a continuous physical phrase must split, end at a stable state and fully restate the next opening. Every clip resets visible people/counts/relations, off-screen direction, pose, grip/contact, backing, light and stable labels. Never use `保持原有/上一格/上一镜/只放大上一格/沿用前镜` or negative controls such as `不新增/不要/不出现` in generatable fields.

## Required output

```markdown
## 【片段1】
**分镜1（6秒）：**
分镜参考 `[00.jpg]`
【镜头设计】：角度与轴线、景别/焦段、裁切与主体布局、深度/遮挡、焦点、主运镜和落幅。
【可见动作】：明确当前姿态与已建立的任务/接触，写出回应此情境的获准主动作或可读姿态变化，交代必要衔接、顺序/交叠和清楚的落定状态；表情与次级运动按需补充。
【可见背景】：实景环境或有段落目的的图形底场，写清必要层次、配色与自身运动；满幅主体确实遮住背景时只陈述这一可见性状态。
【台词与语气】：角色说：“……”（音色、语气、情绪、语速、停顿、重音、距离及必要声像）；无台词写“无台词”。
【光影布光】：光源、方向、遮挡、主辅光、局部高光、阴影和材质响应。
【声音设计】：环境底声、动作拟音、呼吸/身体声、静默及必要同步；不复述对白表演，不写BGM。
```

Keep all six fields separate and ordered. `【镜头设计】` alone contains static composition and camera behavior; `【可见动作】` is the single source of truth for subject/object motion and changing performance. Camera, background, dialogue, light and sound may describe only their own result and cannot restate or newly assert that motion. Page margins, gutters, OCR gaps, speech-bubble whitespace and all printed manga overlays are never background or video content. Sound cannot imply an unseen event or name its unseen source.

Background ownership and complete occlusion follow the section above; a mandatory field does not require visible scenery in every crop.

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

An `overflow_split` is allowed only for a naturally over-limit single-panel unit and must match its actual contiguous ownership/clip numbers, retain natural timing and record its stable continuation. It never waives an individual clip's ceiling. `manual_overflow` remains a single-panel manual fallback with target segment, natural estimated duration, reason and `manual_handling_required: true`; validation rejects every other over-limit clip.

Mechanical validation proves consistency, not visual truth. Final audit checks source order/result, composition, background, dialogue ownership/order, timing, clip cold start, supported coverage, performance, light/effects/sound and unchanged endpoint.

`fact_claims.entities/actions/relations` must copy atomic entries from the owning panels' `source_facts`; prose cannot use `non_renderable_terms`. Do not backfill an inferred preparatory pose or expressive development into those observed facts. Record admitted necessary transitions and expressive pose development in the existing action admissions/motion decision, explicitly tied to the observed anchor. Major action verbs in `【可见动作】` must have a matching admission grounded in that visual evidence rather than dialogue/story meaning alone. Mechanical checks establish ledger consistency; the bounded-inference decision and motion realization remain a visual/manual audit.
