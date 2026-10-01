# Core authoring contract

This file owns source evidence, clip boundaries, output fields, color, sound and the V3 ledger. Dialogue/performance decisions live in `dialogue-performance.md`.

## Evidence and batch discipline

Evidence precedence is: current open panel; explicit supplied character/environment/prop/palette reference; adjacent panel only for chronology or continuous motion; story context only to decide what to inspect. An adjacent panel or ledger never proves current visibility.

Draft one to three contiguous panels at a time with their 720p proxies open. A contact sheet is insufficient for exact composition. Escalate only unresolved small text, identity, hand/contact, overlap, topology, perspective or fast motion to original resolution, and record the reason.

Freeze only decision-changing facts: angle/scale; left-right and near-far placement; overlap; pose/gaze/visible limbs; hand/prop/grip/contact/vector; visible backing; source phase; bubble owner/order. The ledger is an audit index, not replacement prose.

## Shot authority

- `source_locked`: restores a cited panel's complete composition at its declared opening, middle, contact, result or endpoint.
- `source_supported_phase`: adds a missing phase visibly supported by current/adjacent panels while preserving axis, grip, topology and endpoint.
- `uncited_coverage`: a separately numbered speaker, listener, relationship, object, environment, detail or action-phase view with stated source owner and purpose. It cannot create a new event, identity, object, route, contact or result.

A formal citation is used only when the full composition matches. Adjacent numbered shots never repeat the same formal citation. Keep the matching view cited once; derived views are uncited and must be meaningfully different.

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
【可见动作】：明确起态，经语义节点发展头脸、视线、手/道具、重心和延迟运动，落到明确终态。
【可见背景】：镜头内可见的物理环境、明确图形场或铺满画面的表面及其层次和运动。
【台词与语气】：角色说：“……”（音色、语气、情绪及必要节奏）；无台词写“无台词”。
【光影布光】：光源、方向、遮挡、主辅光、局部高光、阴影和材质响应。
【声音设计】：环境底声、声像/遮挡、动作拟音、呼吸/静默、对白距离和关键同步；不写BGM。
```

Keep all six fields separate and ordered. `【镜头设计】` alone contains static composition; `【可见动作】` contains only changing performance. Page margins, gutters, OCR gaps and speech-bubble whitespace are never background. Sound cannot imply an unseen event.

When several panels are successive phases of one camera setup, backing, axis and causal action, bind each panel to a separate phase bullet in `【镜头设计】` and use matching action-only bullets in `【可见动作】`. Otherwise create another numbered shot.

## Look, color and sound

State one reusable scene look with supplied or deliberately chosen work/studio/director references plus executable traits. Do not repeat the full style stack per shot.

Color precedence is: explicit direction/reference; verified colored occurrence of the same item; coherent production choice only for genuinely uncolored non-character elements. Screentone proves value/material/light, not literal gray. Lighting may tint but not rewrite base color.

`【声音设计】` starts with the continuous location bed, then adds useful Foley, breath/body, silence, dialogue treatment and synchronization. Preserve environment audio and sound effects in both mother draft and execution prompt when the target supports audio. BGM, score, melody and theme music are excluded.

## Source ledger V3

Use `version: 3`. Create evidence before prose. The minimum is:

- root: `source_language`, `panels`, `shots`, optional `performance`;
- panel: image/viewing/resolution audit, background, concrete locks, bubbles and coverage;
- dialogue-risk panel: ordered semantic `dialogue_turns` plus ordered `coverage_groups`;
- shot: target, role, purpose/evidence, background excerpt, source audit, D/P/G flags and basis;
- uncited shot: empty `source_images`, nonempty `derived_from`, `coverage_type`, at least two evidenced coverage changes;
- `P` shot: one compact card plus exact rendered excerpts and interval estimate.

`dialogue_turns` preserve story logic; `coverage_groups` decide camera economy. A group may combine consecutive short turns only when total speech fits naturally, one setup carries the handoff without a hidden cut, and no key reveal/reversal/reaction loses its landing. Record a concise `merge_basis` for a multi-turn group.

`manual_overflow` is allowed only on one panel and names the target segment, natural estimated duration, reason and `manual_handling_required: true`. Validation must reject every other over-15-second clip.

Mechanical validation proves consistency, not visual truth. Final audit checks source order/result, composition, background, dialogue ownership/order, timing, clip cold start, supported coverage, performance, light/effects/sound and unchanged endpoint.
