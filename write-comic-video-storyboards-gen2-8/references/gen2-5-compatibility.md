# Gen2.5 non-regression contract

Read only for skill maintenance or compatibility audits, as routed by `SKILL.md`. Ordinary authoring must not depend on discovering a rule here. Source locks, beat/phase decisions, action admission and non-dialogue timing are owned by `core-authoring.md`; dialogue coverage and acting by `dialogue-performance.md`; camera behavior by `cinematic-rendering.md`.

## Episode prepass and source evidence

Use core authoring's image-first, one-to-three-panel 720p batches with conditional escalation. Gen2.5's global low-resolution preview is not a Gen2.8 prerequisite; do not add a contact-sheet/overview pass when the user declines it.

The source ledger is created from the open images before prose. `source_text` is the verbatim source-language bubble/box text; `script_text` is the final Japanese. Never reconstruct locks, bubbles, risk flags, viewing attestations, or performance cards from the completed storyboard. Mechanical extraction may copy filenames and final excerpts after drafting, but it cannot fabricate source evidence or an audit result.

## Reference and adjacent-shot admission

A formal citation belongs only to the camera phase that matches the panel's full viewpoint/scale, subject count and placement, depth/overlap, pose/gaze, visible hands/props/contact, and backing hierarchy. A digital crop, alternate focal length, identity borrowing, or newly invented reverse/insert is not another source-locked composition; make it explicitly `uncited_coverage` with purpose and evidence, or keep it in the original continuous shot.

Adjacent numbered shots must not formally cite the same comic panel. Keep the source-matching shot cited and make genuinely different later views uncited. The uncited view must change at least two meaningful dimensions among subject focus, scale, viewpoint/axis, composition/overlap, visible information, or dramatic function. A small zoom, focus transfer, eye-only crop, or camera motion alone is insufficient. When a speaker/semantic turn requires the cut, redesign the added view instead of merging away the turn; merge only a redundant continuation with no independent dialogue/reaction function.

The cited view and every added view derived from that panel form one panel coverage unit and stay in one clip. Preserve semantic turns first, then group adjacent short turns when one setup can carry them; replace a near-duplicate required shot with genuinely different speaker/listener/object/environment/detail coverage rather than deleting it. If this single-panel unit still exceeds the hard 15-second ceiling after correct timing, keep it together only with a V3 `manual_overflow` marker for user handling.

Several different panels may share one numbered shot only when they are successive phases of one camera setup, backing, axis, and causal action. Bind each panel to its own `【镜头设计】` phase bullet for crop/layout and use matching `【可见动作】` phase bullets for changing performance only. A setup, backing, axis, focus-subject, or discontinuous-action change starts another numbered shot.

## Beat, action, emotion, and duration

Audit `core-authoring.md` §Source locks and temporal action design and §Clip and coverage boundaries. Verify that ordinary routing exposes necessary-transition admission before P-card/camera polish, that an undrawn lead-in is not automatically rejected, and that the cited pose is restored at its declared phase rather than frozen for the whole shot. Also verify that inferred transitions are not mislabeled as observed facts and do not authorize additional mechanics/events. Maintain those rules there, not in a second compatibility-only implementation.

## Color, delivery, and audit

Start with `## 场景色彩基准`. For monochrome or mixed sources, add `## 非人物上色锁定` when recurring environment/prop/effect/graphic colors need continuity. Explicit references and verified colored occurrences outrank invented palette choices; screentone proves value/material/light, not literal gray color.

After storyboard approval, generate the Chinese SRT unless the user declines or requests it earlier. Preserve the complete adult master and keep any safe replacements separate with matching timing unless turn count genuinely changes.

Final delivery is not defined by `0 errors` alone. Classify every adjacent-reference, source-citation, dialogue-coverage, performance-density, camera-landing, long-shot, and multi-panel advisory. Resolve image-dependent issues against the affected images under `core-authoring.md`'s change-scoped review; check purely lexical or arithmetic false positives mechanically. Record a concrete disposition for every remaining advisory; do not waive a class of warnings in bulk. A repeated-reference advisory cannot remain because adjacent repeated formal citations are prohibited.
