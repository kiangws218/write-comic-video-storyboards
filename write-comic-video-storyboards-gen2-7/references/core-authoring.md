# Core authoring contract

This normal source, format, timing, color, and sound module contains only rules that change generation decisions.

## Evidence and batch discipline

Use evidence in this order: current open panel; explicit supplied character/environment/prop/palette reference; adjacent panel only for chronology or continuous motion; story context only to decide what to inspect. An adjacent panel or ledger never proves current visibility.

Draft one to three contiguous panels at a time. Keep each image open at drafting resolution while freezing locks, mapping dialogue, writing its cited shot, and comparing prose back to the image. A contact sheet is insufficient for exact composition.

Record only decision-changing facts: angle/scale; left-right and near-far placement; overlap/occlusion; pose/gaze/visible limbs; hand/prop/grip/contact/action vector; visible backing; source phase; bubble owner/order; role and evidence. The ledger is an audit index, not replacement prose.

## Shot authority

- `source_locked`: the cited composition is recognizably present at its declared opening, middle, contact, result, or endpoint. Supported micro-performance, cloth/hair response, restrained camera, light, materials, and sound may develop without changing anchors.
- `source_supported_phase`: a missing phase of the same action visibly supported by current/adjacent panels. Record all evidence and preserve axis, grip, placement, topology, and endpoint.
- `uncited_coverage`: a separately numbered reverse, reaction, insert, environment, or connective view with stated purpose/evidence. It cannot create an event, identity, object, route, contact, attack, recovery, or result. Cite a panel only when the full composition matches.

Before closing a batch, map every drafted noun, identity, spatial relation, hand/contact, motion phase, and strong emotion to allowed evidence. Delete unsupported claims.

## Background and clip cold start

Every shot positively describes its visible backing as physical space, graphic field, or a frame-filling surface. Preserve an abstract panel backing rather than restoring the known location. Generic labels, source-comparison language, and negative exclusions are not executable.

At every clip reset visible people/counts/relations, off-screen targets, pose, direction, grip/contact, background, and light. Name a gaze target only when the clip establishes it; otherwise use an executable screen direction. Never write cross-clip pointers such as `保持原有/上一格/上一镜/只放大上一格/沿用前镜`, or negative controls such as `不新增/不要/不出现/不使用`, in generatable fields.

Use stable descriptive labels for unsupported creatures/special props: useful scale, dominant color, material/surface, body type, and defining anatomy. Repeat the full label at first appearance in each clip.

## Timing and coverage

A clip is one generated video; 15 seconds is a soft maximum. Keep a continuous physical phrase—load→launch, reach→grip→pull, swing→contact, fall→landing—in one clip when it fits. If split, end at a stable state and fully restate the next opening.

Each camera setup receives one numbered shot and positive integer duration. A hard cut, reverse, insert, reaction, environment view, or new composition starts another shot. Seven seconds triggers review, not an automatic cut. Added coverage must change focus, scale, viewpoint, visible information, or dramatic function. Compare a clip's terminal added shot with the next source shot and remove near-duplicates.

## Required output

```markdown
## 【片段1】
**分镜1（6秒）：**
分镜参考 `[00.jpg]`
场景环境：当前可见空间/图形场/近景表面，主体位置、层次、材质和环境运动。
环境音：连续空间底声、远近、遮挡和声像。
镜头设计：景别/焦段、机位与轴线、构图、景深、焦点、起幅、一个主运镜和落幅。
可见动作：自足起始姿态，经语义节点发展人物、道具、头脸、微表情、重心和延迟运动，落到明确状态。
台词与语气：角色说：“……”（音色、语气、情绪及必要的语速、停顿、重音）；无台词写“无台词”。
光影布光：光源方向、人物位置/遮挡、主辅光、明暗区、局部高光、材质和有依据的空气效果。
声音设计：可见动作拟音、呼吸/静默、台词距离和关键音画同步。
```

Keep all seven fields separate and complete. Do not output legacy `景别/构图/运镜/画面内容` fragments. Keep sound out of visual facts and new visual actions out of sound lines.

## Color, environment, and audio

State one reusable scene look: supplied or deliberately chosen work/studio/director references plus a few executable traits, hue/contrast/saturation, 2D texture, broad light, depth, and clarity. Do not repeat it per shot.

Color precedence: explicit direction/reference; visible colored occurrence of the same item; verified recurring colored occurrence; coherent production choice only for genuinely uncolored non-character elements. Monochrome proves value/material/depth/ink/light, not literal gray color. Lock recurring non-character colors once. Lighting may tint but not rewrite base color.

Environment reference assets contain space/material/weather/light, not people, equipment, routes, staging zones, or narrative functions.

`环境音` establishes location bed and perspective. `声音设计` selects one or two useful Foley, breath/body, silence, dialogue-treatment, or synchronization events. Every emphasized sound needs a visible/supportable cause or established environment. Bind it to `句首`, exact Japanese in `「」`, `句末`, contact, or action completion. Audio cannot imply an unseen impact, object, injury, word, or event.

## Ledger minimum and final audit

Use version 2 with `panels` and `shots`. Panel rows record image, actual viewing attestations, bubble count/audit, positive background, compact locks, coverage, and mapped bubbles. Shot rows record target, role, evidence images, purpose, background excerpt, actual viewed/audit attestations, and unsupported additions. Continuing bubbles use ordered segments whose text concatenates exactly. Validation proves consistency, not visual truth.

Confirm source order/event/result; cited composition/phase; background; color evidence; complete dialogue ownership/order; natural timing; stable labels; independent clip cold start; useful boundary coverage; supported performance; motivated camera/light/effects/sound; and unchanged adult master when applicable.
