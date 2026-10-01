# Dialogue coverage and image-grounded performance

This file owns D/P/G routing, ordered dialogue logic, timing and first-pass acting quality. It never authorizes invention or replaces the open image.

## Selective routing

- `D`: several bubbles/speakers, mixed dialogue/thought/narration, a 28+ character Japanese turn, three clauses, or a meaning-changing exchange.
- `P`: expressive 3–6 second delivery, 21+ meaningful characters needing development, changing repeated words, or a listener/prop relation carrying the beat.
- `G`: unresolved hand/grip/contact/overlap/topology/vector/perspective or an added viewpoint.

`D` invokes a compact turn/coverage plan. `P` invokes one compact performance card. `G` first inspects the 720p proxy and escalates only unresolved decision-changing details to original resolution. Neutral/object/cropped/informational shots need no artificial flags.

## Dialogue logic before camera count

Record every bubble/box in visual order while the image is open. Preserve owner, kind, meaning, order and information in natural Japanese; Chinese belongs only in the later subtitle deliverable.

First create ordered semantic turns. Consecutive bubbles may share a turn only for one continuous delivery, overlap, or an inseparable prompt/reaction. Question→answer, accusation→denial, interruption, reveal→reaction and attitude reversal remain distinct turns even when one speaker continues.

Then create ordered coverage groups. One group may contain adjacent turns when all are true:

- their final Japanese plus pauses fit the shot naturally;
- one camera setup can show the speaker/listener/object/environment handoff without a hidden cut;
- the later turn is short and does not need an independent reveal, joke, reversal or reaction landing;
- supported action and focus progression keep the shot visually alive.

Thus `解释→质问→否认` may be three shots or `解释 | 质问+短否认`; the semantic order never changes. Similar required coverage is redesigned rather than deleted.

Each group maps to numbered shots in the same panel-owned clip. Restore the source composition once, then use supported speaker/listener/relationship/object/environment/detail coverage. Person-free object or environment inserts are allowed with off-screen dialogue when the item/space and sound direction are established. An uncited view may not invent the unseen reverse side of a room, hidden pose, new object or contact.

## Timing

- 1–20 meaningful Japanese characters: normally one shot.
- 21–41: one shot only with supported development; otherwise add coverage.
- 42+ in one numbered shot, or three complete clauses in one continuous turn: split across genuinely different shots.

Estimate before clip boundaries from final Japanese: roughly six meaningful characters/second, plus about 0.25s for `、`, 0.45s for `。！？`, 0.6s for `……/…`, and 0.35s for an in-shot speaker handoff. Use natural floors: interjection 1–2s, short sentence 2–4s, medium 4–6s, long explanation 6–9s, two long clauses 8–12s. Concurrent speech and acting use the longer interval.

If prose names a speech trigger, quote an exact Japanese substring inside `「」`; otherwise use `开口前/转折后/重音处/句末`. Chinese semantic paraphrases are invalid.

## P-card

Create only for `P` shots and immediately render it:

```text
O=<self-contained opening orientation/contact>
B=<ordered meaning-changing beat 1>|<beat 2>
C=<coupled face/head + hand/prop/weight/listener or delayed response>
L=<performer endpoint>|<camera landing>
```

Every item must be visible in the panel or a modest continuous transition between visible anchors. Render rather than copy labels:

- `O`: face orientation, gaze direction, visible contact/support and weight;
- `B`: distinct local eye/brow/mouth/head changes tied to exact Japanese or generic semantic nodes;
- `C`: one task-related hand/prop/weight/listener or delayed hair/cloth/material response;
- `L`: final orientation, gaze/contact/pressure residue, settled weight, decay and camera landing.

Prefer tasks and relations over generic pointing, open-palm explanation, nodding, folded arms or fists. Do not invent missing anatomy or emotion to satisfy density. Cropped shots use visible substitutes.

Repeated words become separate beats only when pressure changes. Differentiate with breath, timing, intensity, room response or decay. Wind, particles, lip sync and camera drift enrich but cannot carry the line.

## Quality gate

A `P` shot is blocked when it lacks a self-contained opening, ordered supported development, local face/head/gaze transition, coupled response/substitute, performer endpoint, or camera landing when moving. Card details must appear in the final camera/action/sound fields.

Before leaving the batch, an animator reading only the six fields must recover panel-specific composition, opening, ordered changes, overlap/latency, final held state and renderable backing. Compare those claims with the still-open source image.
