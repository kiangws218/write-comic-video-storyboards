# Dialogue coverage and image-grounded performance

This file owns D/P/G routing, ordered dialogue logic, timing and first-pass acting quality. Use its acting principles for all character shots; selective cards reduce planning overhead, not performance quality. Action admission and phase anchors remain owned by `core-authoring.md`.

## Selective routing

- `D`: several bubbles/speakers, mixed dialogue/thought/narration, a 28+ character Japanese turn, three clauses, or a meaning-changing exchange.
- `P`: a supported expressive change, changing repeated words, or a task/listener/contact relation that needs staged development, including short or silent beats. A 21+ character delivery prompts a development review, not automatic gestures: an evidenced neutral hold or object insert may clear P with a concrete `risk_basis` and natural timing.
- `G`: unresolved hand/grip/contact/overlap/topology/vector/perspective or an added viewpoint.

`D` invokes a compact turn/coverage plan. `P` invokes one compact performance card. `G` first inspects the 720p proxy and escalates only unresolved decision-changing details to original resolution. Neutral/object/cropped/informational shots need no artificial flags.

Long delivery still needs a performance/timing entry with rendered evidence, even when P is cleared; an intentional hold can be that evidence. A cropped expressive action can need P: cropping limits the available anatomy, not the right to develop the visible task.

## Dialogue logic before camera count

Record every bubble/box in visual order while the image is open. Preserve owner, kind, meaning, order and information in natural Japanese; Chinese belongs only in the later subtitle deliverable.

First create ordered semantic turns. Consecutive bubbles may share a turn only for one continuous delivery, overlap, or an inseparable prompt/reaction. Question→answer, accusation→denial, interruption, reveal→reaction and attitude reversal remain distinct turns even when one speaker continues.

Then create ordered coverage groups. One group may contain adjacent turns when all are true:

- their final Japanese plus pauses fit the shot naturally;
- one camera setup can show the speaker/listener/object/environment handoff without a hidden cut;
- the later turn is short and does not need an independent reveal, joke, reversal or reaction landing;
- supported action and focus progression keep the shot visually alive.

Thus `解释→质问→否认` may be three shots or `解释 | 质问+短否认`; the semantic order never changes. Similar required coverage is redesigned rather than deleted.

Each group maps to numbered shots in the same panel-owned clip. Restore the source composition once, then use supported speaker/listener/relationship/object/environment/detail coverage. Before prose, assign every added shot a distinct visual function and compare `dominant subject | scale | viewpoint/axis | placement/overlap | visible information` with both the preceding planned shot and the next source-panel composition. At least two meaningful dimensions must change against each available neighbor; a new focal length, focus transfer or tighter crop alone is insufficient. Redesign or merge before writing if this cannot be achieved from visible evidence. Person-free object or environment inserts are allowed with off-screen dialogue when the item/space and sound direction are established. An uncited view may not invent the unseen reverse side of a room, hidden pose, new object or contact.

## Timing

- 1–20 meaningful Japanese characters: normally one shot.
- 21–41: review supported development or a purposeful source-grounded hold; add justified coverage when one setup cannot carry the delivery readably.
- 42+ in one numbered shot, or three complete clauses in one continuous turn: split across genuinely different shots.

Estimate before clip boundaries from final Japanese: roughly six meaningful characters/second, plus about 0.25s for `、`, 0.45s for `。！？`, 0.6s for `……/…`, and 0.35s for an in-shot speaker handoff. Use natural floors: interjection 1–2s, short sentence 2–4s, medium 4–6s, long explanation 6–9s, two long clauses 8–12s. Concurrent speech and acting use the longer interval.

If prose names a speech trigger, quote an exact Japanese substring inside `「」`; otherwise use `开口前/转折后/重音处/句末`. Chinese semantic paraphrases are invalid.

## Natural acting before the card

Start with the admitted principal action or an already visible task/contact/posture. Ask what the character is doing now, what supported stimulus changes it, and how the response alters the ongoing behavior. An embrace must actually form when its necessary lead-in is admitted; a speaking character already walking continues the evidenced travel. Lips, hair or camera motion cannot replace these main actions. If there is no task, an evidenced attention shift, reaction or deliberate hold is sufficient; never invent a busywork prop or errand.

Choose one supported immediate intention for the beat, not a new backstory. Let attention, expression, hands and weight serve that intention. Dialogue meaning may organize admitted local acting, but does not authorize the physical event it mentions. Speech and body may differ when source attitude supports it: a polite reply with attention elsewhere, or restrained words with an existing tense grip. Do not automatically illustrate each spoken noun, intensify emotion or invent concealed motives.

Useful organization is `ongoing action/state → supported stimulus → selective response → changed or continuing task/relation → readable endpoint`. This is a reasoning aid, not a sequence every shot must display. A response can interrupt an action, hesitate partway, fail to complete or resume it only when that behavior is supported/admitted; do not invent a failed grab, release or transfer to add personality.

### Expressive detail and timing

When the face is readable, distinguish eye direction from head direction and describe the useful local transition: lids/brow tension, one mouth corner, lip compression or chin angle. Eyes, head, shoulder and hand need not move together; use asymmetry or offsets only when they clarify this response. Give the animator direction, useful extent/speed and final orientation/contact, rather than an emotion adjective or a list of body parts. A neutral face need not change just because the hand is acting; a cropped hand needs no imagined eyes.

Prefer existing grip pressure, strap tension, supported posture or weight and contact response to generic pointing, nodding and fists. Layer only consequences of established force: hair follows a head turn, cloth compresses at contact, a carried object answers a supported stop. One action may continue while another reacts. Select onset, acceleration, hesitation, pressure and settling from the beat, not a fixed half-beat delay. Do not append blink, breath, finger squeeze and hair rebound to every shot.

Keep silence and holds when they carry recognition, awkwardness, contrast or sustained effort. They need a clear entry and meaningful held state, not compulsory motion in every frame. Conversely, do not make every admitted action `微微/极小/轻轻`; choose its magnitude from evidence and framing. A rich sequence has contrast between decisive movement, small response and stillness, not uniformly dense gestures.

### Relationships and continuity

In a shared shot, choose an attention hierarchy rather than freezing everyone except the speaker. Visible listeners may continue established tasks and respond at different times/intensities; the response can affect the next speaker's supported behavior. Preserve each person's distinct source-supported attitude, posture and contact. Do not make everyone nod, turn or react together by default, or require every background figure to perform. An absent listener remains absent; use a justified derived view if their reaction needs coverage.

Carry the task, attention, pressure and supported emotional residue across adjacent shots rather than restarting the same facial arc at each cut. Plan from adjacent continuity, but render only anatomy/targets established in the current view. Every independently generated clip positively restates its current opening under core authoring; restatement is not a dramatic reset or replay of an already completed lead-in. Character references establish identity/design, not automatic personality or hidden intent.

## P-card

Create only for `P` shots and immediately render it:

```text
O=<self-contained opening, ongoing task/contact and supported immediate intention>
B=<the supported change(s), with useful order/overlap>
C=<how the change affects or preserves the visible task/body/listener/contact>
L=<performer endpoint>|<camera landing>
```

Every item must be visible in the panel or admitted under core authoring's temporal action design, including a bounded necessary lead-in to a single established anchor; two separately drawn poses are not required. A named target must be established in the current shot; otherwise use the visible screen-relative direction. Render rather than copy labels:

- `O`: current orientation and supported task/contact, including an admitted preparatory state;
- `B`: the principal enacted change and useful semantic developments, tied to exact Japanese or generic nodes when speech drives their timing;
- `C`: their physical/social connection, not an obligatory extra hand gesture or delayed hair motion;
- `L`: final orientation/contact/task state and useful residue; camera landing belongs to camera design when moving.

Retain the existing `opening/beats/coupling/landing` fields, rendered `details` excerpts and serial/concurrent `intervals`; no new card or ledger version. `beats` records the actual supported developments, with no universal count. Longer expressive delivery normally needs more development or coverage, but word count alone cannot require another gesture. Evidence excerpts prove that planned acting was rendered, not that a quota was filled.

Repeated words become separate beats only when pressure changes. Differentiate with breath, timing, intensity, room response or decay. Wind, particles, lip sync and camera drift enrich but cannot carry the line.

## Semantic quality gate

Render each detail only in its owning field: static composition/camera landing in `【镜头设计】`, subject/object motion in `【可见动作】`, and evidenced non-dialogue audio in `【声音设计】`. Judge equivalent wording by the enacted meaning, not the presence of `先/随后/迟半拍/最后` or a body-part vocabulary.

Before leaving the batch, compare the prose with the still-open image and ask:

- Can an animator recover the admitted main action, its entry into the anchor, useful order/overlap and endpoint? A populated card with only decorative motion fails an admitted moving beat.
- Does each development answer this task/stimulus/relation? Remove interchangeable checklist actions. If the intended change is unreadable at this scale or time, replan timing or justified coverage.
- Do performer and visible listener responses preserve source attitude/contact, and does the next opening carry rather than reset the supported state? Do not add absent participants or unsupported reversals.
- Is a hold purposeful, and is any movement amplitude or latency appropriate? Neither continuous motion nor compulsory facial change is a universal requirement.

Unsupported facts, omitted admitted principal action, erased meaning-changing developments, an unintelligible temporal phrase or missing needed endpoint/landing block delivery. A lexical advisory is only a review hint: resolve it from the meaning and available evidence, not by inserting matching words. Structural validation does not certify source fidelity or natural acting.
