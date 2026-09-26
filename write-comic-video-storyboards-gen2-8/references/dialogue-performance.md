# Dialogue routing and image-grounded performance

Use this module for every character scene. It decides which shots need extra planning; it does not authorize invention or replace the open panel.

## D/P/G routing

Assign flags per planned shot while the exact panel is open:

- `D` dialogue risk: at least three bubbles, at least two speakers, mixed dialogue/thought/narration, one Japanese turn at 28+ meaningful characters, or three complete clauses.
- `P` performance risk: an expressive or meaning-changing 3–6 second line with readable face/body; 21+ meaningful dialogue characters needing staged development; repeated words whose delivery changes; or a listener/prop relation carrying the beat.
- `G` geometry risk: ambiguous or fragile hand, grip, contact, overlap, topology, action vector, extreme perspective, or added viewpoint.

Flags select work; they are not output prose. `D` invokes coverage planning, `P` invokes one compact performance card, and `G` invokes original-resolution source locking. A neutral panel, pure object shot, cropped face, or short informational line may remain unflagged when no development is supported.

## Dialogue gate

Record every bubble/box in visual order while the image is open. Determine owner from tail, placement, page order, and bubble/box style. Preserve meaning, owner, kind, order, and information in natural Japanese; Chinese belongs only in the later SRT.

- 1–20 meaningful characters: normally one shot with one or two supported developments.
- 21–41: one shot only when two or three supported developments follow semantic beats; otherwise use genuinely different coverage.
- 42+ meaningful characters in one numbered shot, or three complete clauses in one continuous turn: at least two genuinely different numbered shots; no long-take waiver.
- At least two speakers plus three bubbles: normally at least two targets. A shared source composition needs a supported relationship/action and `shared_reason`.

New coverage changes focus, scale, viewpoint, composition, visible information, or dramatic function. Speaker change alone is insufficient. Continuing one bubble across shots uses ordered segments whose Japanese concatenates exactly.

Estimate speech before clip boundaries: interjection 1–2s; short sentence 2–4s; medium 4–6s; long explanation 6–9s; two long clauses 8–12s. Concurrent speech and acting use the longer interval. Every line includes local voice, delivery, emotion, and useful pace/pause/emphasis.

If prose names a spoken trigger, quote an exact Japanese substring from that shot inside `「」`. Otherwise use `开口前/转折后/重音处/句末`. Chinese paraphrases such as `“闭嘴”出口时`, `提出抢攻时`, or `提到入口时` are invalid.

## P-card: plan before prose, from the open image

Create a card only for `P` shots and immediately write that shot before moving on:

```text
O=<self-contained opening orientation/contact>
B=<ordered meaning-changing beat 1>|<beat 2>
C=<coupled face/head + hand/prop/weight/listener or delayed response>
L=<performer endpoint>|<camera landing>
```

Keep it short: concrete body parts, visible targets, existing props, order/overlap, and landing. It is not a scene description. Every item must be visible in the current panel or a modest continuous transition between its visible anchors. The card never proves visibility and never becomes a substitute text source.

Example quality anchor:

```text
O=晶石仍压在掌心，矮人从下托住
B=首句手腕后撤带动肩缩|重复拒绝时视线晶石→矮人，唇角压紧
C=摇头后发梢衣摆迟半拍；矮人拇指避开指节
L=两人手指停在接触处|轻手持跟随双手后稳住
```

Bad compression: `后撤、缩肩、摇头、视线折返，最后停住。` It lists gestures but loses causal order, local expression, contact mechanics, latency, and camera landing.

## Rendering the card

Render rather than copy labels:

- `O` establishes face orientation, gaze point/screen direction, visible contact, support, and weight.
- `B` ties distinct changes to exact Japanese or generic semantic nodes. Eyes may lead; chin/nose line, head, neck/shoulders, and hair follow with readable latency.
- `C` uses a local asymmetric face transition plus one task-related hand/prop/weight/listener or delayed material response. Cropped anatomy uses a visible substitute.
- `L` names the final orientation, gaze/contact/pressure residue, settled weight, delayed-motion decay, and where the moving camera stabilizes.

Prefer tasks and relations over generic pointing, open-palm explanation, nodding, folded arms, or sudden fists. Use fingertip pressure, thumb position, grip adjustment, strap tension, material compression, support transfer, breath, swallow, posture load, or listener latency only when supported.

Repeated words are separate beats when pressure changes. Differentiate first/later delivery through breath, timing, intensity, room response, or decay. Wind, particles, lip sync, and camera drift enrich but cannot carry the line.

## Performance blockers and advisories

For a `P` shot, delivery is blocked when the card or prose lacks a self-contained opening, supported ordered beats, local transition, coupled response/substitute, performer endpoint, or camera landing when the camera moves. It is also blocked when card details never appear in the final camera/action/sound fields.

Do not force a neutral or cropped shot to invent missing anatomy or emotion. Record why it is not `P`, or use real speaker/listener/prop/environment coverage if the line cannot be carried in one view.

Repeated reference images, multiple speakers, or long takes are advisories when the planned shots genuinely change viewpoint/function or preserve a supported shared composition. Inspect them; do not add decorative actions merely to silence a warning.

Before leaving each batch, read only `【镜头设计】`, `【可见动作】`, `【台词与语气】`, and `【声音设计】`. An animator must recover opening, ordered changes, overlap/latency, and final held state without another shot. Then compare those claims with the still-open source image.
