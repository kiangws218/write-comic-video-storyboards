# Dialogue and character performance

Use this module for all character work. It preserves dialogue and turns supported semantic beats into dense natural acting without inventing story facts.

## Dialogue gate

While the panel is open, record every spoken bubble, inner thought, and narration box in visual order. Determine owner from tail, placement, page order, and bubble/box style—not from a later reply. Preserve meaning, owner, kind, order, and information when translating naturally into Japanese. Chinese belongs only in the later SRT.

A panel is dialogue-risk when it has at least three bubbles, at least two speakers, mixed dialogue/thought/narration, a final Japanese turn of at least 28 meaningful characters, or three complete clauses. It cannot advance until the audit passes and each bubble is mapped or exceptionally justified.

Coverage defaults:

- 1–20 meaningful characters: normally one shot with one or two supported developments.
- 21–41: one shot only when two or three distinct developments follow semantic beats; otherwise use genuinely different coverage.
- 42+ meaningful Japanese characters in one numbered shot, or three complete clauses in one continuous turn: require at least two genuinely different numbered shots. Count all dialogue in the shot, combine adjacent bubbles from the same speaker, and do not waive this gate with `long_take_reason`.
- At least two speakers plus three bubbles: normally at least two targets. Shared composition requires `shared_reason` and a supported relationship/action that improves readability.

A new target changes focus, scale, viewpoint, composition, visible information, or dramatic function; speaker change alone is insufficient. One bubble continuing across shots keeps one row with ordered segments whose text concatenates exactly.

Estimate speech before clip boundaries: interjection 1–2s; short sentence 2–4s; medium 4–6s; long explanation 6–9s; two long clauses 8–12s. Concurrent speech and acting use the longer interval rather than being summed. Every spoken/narrated line includes local voice, delivery, emotion, and necessary pace/pause/emphasis; do not output calculations.

If acting prose names a dialogue trigger, quote an exact Japanese substring spoken in that shot inside `「」`. Generic `开口前/转入后半句/重音处/句末` timing is allowed; a Chinese paraphrase of the trigger is not.

## Performance contract

Performance develops supported facts; it cannot create a person, prop, hand, contact, route, event, result, hidden motive, or stronger emotion without evidence. Preserve pose, screen relation, visible parts, grip/contact, overlap, backing, and declared phase.

Plan one chain per beat:

`self-contained opening → supported stimulus/semantic node → attention → gaze/head/face development → local expression or task-related hand/prop/weight response → delayed motion → explicit endpoint`

Select only useful stages. Three seconds may contain many micro-actions serving one intention; it may not contain several unrelated complete actions. A neutral panel may stay neutral. If no supported stimulus or endpoint exists, do not fill time with a large gesture.

### Performance fidelity floor

Compression may shorten wording, but it must not collapse distinct visible beats into a summary. Before drafting, preserve the beat topology of the panel and dialogue: opening state; each meaning-changing phrase or repeated utterance; the body part or prop that carries it; response latency/inertia; and landing state. A clause such as `后撤、缩肩、摇头` is only a list until it states useful order, coupling, or overlap.

For an expressive 4–6 second dialogue shot with a readable face and body, normally make these five slots executable in the prose:

1. self-contained opening orientation/contact;
2. at least two ordered or overlapping developments tied to the line;
3. one local face change—eyes/eyelids/brow/mouth/chin—described as a transition, not a static emotion label;
4. one coupled body, hand/prop, or delayed hair/cloth response;
5. a specific endpoint for performer and camera.

Use only visible or source-supported slots. When a face, hand, or body part is cropped, replace that slot with a supported listener, prop, material, or environment response instead of inventing anatomy. Repeated words are separate performance beats when delivery changes: distinguish the first and later utterance through pressure, breath, timing, or sound decay. Do not satisfy the floor with synonyms, particle motion, or camera drift.

## Head, face, and gaze

When readable, establish opening face orientation (front, three-quarter, profile, back-turn), pitch, screen direction, gaze point, and head/shoulder relation. Distinguish eyes from face direction: eyes may move first; chin, nose line, facial midline, neck, shoulder, and hair can follow with latency. Name the final orientation and gaze point.

Use local asymmetric changes: one eyelid/brow moves first; pupils lock or drift; lips press, part, or change at one corner; chin and shoulder answer later. For down/up turns show chin, visible forehead/nose underside, eyelids, and neck load. If cropped, animate only visible eyes/lips/chin edges rather than inventing a full turn.

## Task-based micro-performance

Prefer a visible task, object, support surface, posture, or relationship over generic pointing, open-palm explanation, repeated nodding, folded arms, or sudden fists.

- Hand/prop: adjust an existing grip, fingertip pressure, thumb position, strap tension, palm support, or material compression; preserve the visible hand/contact.
- Weight: let feet/knees/hips/torso/shoulder/head initiate or absorb movement with slight offsets; preserve visible support points.
- Breath/body: use inhale, held breath, exhale, swallow, or tremor only when scale, sound, and evidence support it; synchronize with semantic pressure.
- Delayed motion: existing hair, cloth, accessory, strap, steam, leaves, rain, or dust follows established force and settles after the body.

Do not queue blink, breath, finger squeeze, and weight shift as unrelated checklist items. Let one continue while another changes meaningfully. Multi-character shots have one primary performer; listeners respond later and more quietly while preserving axis, placement, and occlusion.

## Duration-specific development

For 4–6 seconds of dialogue, include opening and endpoint plus at least two semantic developments from head/face orientation, eyes/asymmetric face, hand/prop relation, weight/posture, listener response, or supported environment contact. Lip sync, camera/light drift, wind, and particles enrich but do not carry speech. If evidence is insufficient, use a real speaker/listener/prop/environment coverage change.

For a short dense shot, use one stimulus, layered reaction, and one landing state. Allow overlapping eyes, head, face, fingers, weight, and delayed motion; reject unrelated `turn → wave → run` chains unless panels support the entire action.

Synchronize acting with language: inhale/attention before the line; gaze/head/local face at a key phrase; task-related hand/weight at emphasis; breath, pressure release, or expression residue at the end. Off-screen speech may motivate only a supported listener, visible hand/prop, or environment response.

Before delivery, run a local fidelity pass on every expressive or long dialogue shot. Read only `【可见动作】`, `【镜头设计】`, and `【声音设计】` together and ask: can an animator identify the opening, two meaningful changes, their order/overlap, and the final held state without consulting another shot? If not, restore the missing beat rather than adding decorative adjectives.

## Audit

Across adjacent shots avoid the same gesture, facial side, and gaze path as a default. Repetition is acceptable when the state intentionally persists and its cause is clear.

Confirm every bubble/segment appears at its declared target in order; duration fits; 42+ character or three-clause turns are split across genuinely different shots; coverage adds a real increment; shared reasons are enacted; acting is visible at scale and supported; head/face/gaze directions are executable; hand/contact and support remain legal; and the endpoint is stable/readable.
