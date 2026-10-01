# Gen2.5 non-regression contract

Read this file for every new episode, substantial rewrite, or final delivery. It contains source-fidelity and timing decisions that Gen2.8 must not trade away for token savings.

## Episode prepass and source evidence

Before drafting, review the ordered episode at low resolution only to establish panel order, locations/time changes, recurring subjects, color-source class, and risk candidates. Then draft one to three contiguous panels with exact 720p proxies open. Escalate perspective, contact, overlap, topology, fast action, identity, or unreadable text to 1080p/original resolution only when the 720p view is inconclusive, and record why.

The source ledger is created from the open images before prose. `source_text` is the verbatim source-language bubble/box text; `script_text` is the final Japanese. Never reconstruct locks, bubbles, risk flags, viewing attestations, or performance cards from the completed storyboard. Mechanical extraction may copy filenames and final excerpts after drafting, but it cannot fabricate source evidence or an audit result.

## Reference and adjacent-shot admission

A formal citation belongs only to the camera phase that matches the panel's full viewpoint/scale, subject count and placement, depth/overlap, pose/gaze, visible hands/props/contact, and backing hierarchy. A digital crop, alternate focal length, identity borrowing, or newly invented reverse/insert is not another source-locked composition; make it explicitly `uncited_coverage` with purpose and evidence, or keep it in the original continuous shot.

Adjacent numbered shots must not formally cite the same comic panel. Keep the source-matching shot cited and make genuinely different later views uncited. The uncited view must change at least two meaningful dimensions among subject focus, scale, viewpoint/axis, composition/overlap, visible information, or dramatic function. A small zoom, focus transfer, eye-only crop, or camera motion alone is insufficient. When a speaker/semantic turn requires the cut, redesign the added view instead of merging away the turn; merge only a redundant continuation with no independent dialogue/reaction function.

The cited view and every added view derived from that panel form one panel coverage unit and stay in one clip. Preserve semantic turns first, then group adjacent short turns when one setup can carry them; replace a near-duplicate required shot with genuinely different speaker/listener/object/environment/detail coverage rather than deleting it. If this single-panel unit still exceeds the hard 15-second ceiling after correct timing, keep it together only with a V3 `manual_overflow` marker for user handling.

Several different panels may share one numbered shot only when they are successive phases of one camera setup, backing, axis, and causal action. Bind each panel to its own `【镜头设计】` phase bullet for crop/layout and use matching `【可见动作】` phase bullets for changing performance only. A setup, backing, axis, focus-subject, or discontinuous-action change starts another numbered shot.

## Beat, action, emotion, and duration

Classify the source beat before extending it:

- `State`: continue an established condition with restrained supported change.
- `Action`: identify the visible preparation, execution, response, result, or settled phase.
- `Reaction`: add only the minimum useful perception/response/recovery/decision phase.
- `Mixed`: preserve the primary and secondary function without completing an inferred chain.

For visible action B, add at most one supported A or C phase when it improves continuity. Evidence, visibility in the declared framing, and anchor safety are all required. Never invent off-frame bracing, grip/contact, route, hand-off, follow-through, rebound, recovery, or a new result.

Strong emotion requires support from at least two of dialogue meaning, visible face/body performance, and adjacent story context. Prefer observable lower-inference behavior when evidence is incomplete.

Use these non-dialogue timing anchors before assigning integer duration:

| Beat | Typical duration |
|---|---:|
| Micro-reaction, glance, discovery | 1–2s |
| Single reveal, fall, pull-out, sudden vocal burst | 2–4s |
| Sustained effort or repeated struggle | 3–6s |
| Evolving state or atmosphere | 4–8s only with visible development |

End when the beat is complete. Do not stretch a short event with static holding, repeated shaking/screaming, particles, or camera drift to approach 15 seconds. Keep a source-continuous physical phrase in one clip when it fits; split only at a stable state and fully restate the next opening.

## Color, delivery, and audit

Start with `## 场景色彩基准`. For monochrome or mixed sources, add `## 非人物上色锁定` when recurring environment/prop/effect/graphic colors need continuity. Explicit references and verified colored occurrences outrank invented palette choices; screentone proves value/material/light, not literal gray color.

After storyboard approval, generate the Chinese SRT unless the user declines or requests it earlier. Preserve the complete adult master and keep any safe replacements separate with matching timing unless turn count genuinely changes.

Final delivery is not defined by `0 errors` alone. Resolve every adjacent-reference, source-citation, dialogue-coverage, performance-density, camera-landing, long-shot, and multi-panel advisory against the open images. Record a concrete disposition for every remaining advisory; do not waive a class of warnings in bulk. A repeated-reference advisory cannot remain because adjacent repeated formal citations are prohibited.
