# Dialogue recovery, timing, and coverage

Use this module to preserve speech and plan coverage. Use `performance-choreography.md` after mapping the lines to turn each supported semantic beat into natural acting rather than a generic gesture.

This file is authoritative for dialogue completeness and shot coverage. Perform the dialogue gate while the source panel is open and before final shot or clip boundaries are chosen.

## Recover every bubble

For each panel, inspect the crop and original page at drafting resolution. Record every spoken bubble, inner thought, and narration box in visual reading order. Small interjections and final reactions remain separate source bubbles.

Establish ownership from bubble tails, placement, original-page order, narration-box form, and inner-bubble style. Do not assign a speaker from the later reply alone. For two or more speakers, record concise `speaker_evidence` for every row.

Translate non-Japanese source dialogue into natural Japanese without changing meaning, owner, kind, order, or information. Chinese dialogue belongs only in the later Chinese SRT.

## Dialogue-risk gate

A panel is dialogue-risk when any condition holds:

- three or more source bubbles;
- two or more speakers;
- dialogue plus inner speech or narration;
- one continuous final Japanese turn has 28 or more meaningful characters after removing spaces, punctuation, and voice notes;
- one turn contains three complete clauses.

Dialogue-risk panels cannot advance until `bubble_audit` is `pass`, every bubble is mapped or exceptionally justified as omitted, and coverage and timing validate.

## Split policy

- **1–20 meaningful characters in a shot:** normally one shot; write one or two visible, supported performance details.
- **21–41:** one shot is allowed only when two or three distinct supported performance details develop across semantic beats. Otherwise split with a real visual increment.
- **42+ or three complete clauses in one continuous turn:** map the turn to at least two genuinely different numbered shots by default. A retained single shot requires a nonempty `long_take_reason`, three or four enacted supported performance details, and a timing entry that fits.
- **Two or more speakers and three or more bubbles:** use at least two shot targets by default. A shared composition is allowed only with a nonempty `shared_reason` explaining the source-supported shared action or relationship that makes all turns more readable.

A new shot must change subject focus, scale, viewpoint, composition, visible information, or dramatic function. Speaker change alone does not justify a duplicate shot. Conversely, one clip may contain several numbered shots; clip continuity does not mean camera continuity.

Suitable coverage includes the source panel, a source-supported listener/creature reaction, prop/detail insert, environment view, or a new viewpoint that clarifies an established beat. Added coverage follows the permissions in `source-grounding.md` and cannot invent an illustrative event.

## Bubble segments

When one bubble continues across shots, keep one bubble row and add ordered `segments`. The bubble-level `script_text` is the exact concatenation of segment text.

```json
{
  "id": "b3",
  "speaker": "店员",
  "kind": "dialogue",
  "source_text": "...",
  "status": "mapped",
  "script_text": "完整日文台词",
  "segments": [
    {"script_text": "前半句", "seconds": 3, "target": "片段13/分镜1"},
    {"script_text": "后半句", "seconds": 3, "target": "片段13/分镜2"}
  ]
}
```

Do not count segments as source bubbles.

## Performance scaled to speech

Count all spoken and inner Japanese lines in one actual numbered shot across speakers and bubbles. Narration affects timing but does not require character acting.

A performance detail is a readable change or clearly sustained state in eyes, face, head/body, or a visible hand/prop relation. Give it a semantic trigger or temporal role. Lip articulation, camera motion, wind-driven hair, scenery, and repeated wording of one gesture do not count as additional acting details.

Choose the fewest supported details. Do not stack simultaneous gestures or invent tears, grips, steps, hidden motives, or new events to satisfy a quota. A neutral source performance may remain neutral; use coverage when further acting is unsupported.

When visual prose names a dialogue trigger, quote the exact Japanese words spoken in that shot inside `「」`. Do not use a Chinese paraphrase such as `提到暗石区入口时` or `监管信息到来时`; write `说到「暗石区の入口」时` or quote the relevant final Japanese substring. The quoted trigger must occur verbatim in that shot's final dialogue. Generic timing such as `开口前`, `转入后半句`, `重音处`, or `句末` is allowed.

For a 4–6 second dialogue shot, require visible development at a minimum of two semantic stages in addition to the opening state and endpoint. Count supported changes in head/face orientation, eyes or asymmetric face, hand/prop relation, weight/posture, listener response, or environmental interaction. Camera movement, lighting drift, lip sync, wind, and decorative particles enrich the image but do not by themselves carry the speech. If the source cannot support this development, split coverage rather than stretching a static expression.

## Timing

Estimate speech before clip boundaries. Use natural delivery; never accelerate dialogue to fill a preselected 15-second container.

Fallback Japanese speech timing:

| Line | Typical time |
|---|---:|
| Interjection or very short phrase | 1–2s |
| Short sentence | 2–4s |
| Medium sentence | 4–6s |
| Long explanation | 6–9s |
| Two connected long clauses | 8–12s |

For each shot, estimate sequential and concurrent intervals. Duration is the sum of sequential intervals; within a concurrent interval use `max(speech, acting)`. For example, one second of recognition, five seconds of speech concurrent with three seconds of expression, and one final hold require `1 + max(5,3) + 1 = 7` seconds.

Every spoken or narrated sentence in the storyboard is followed by `（音色、语气、情绪；必要时语速、停顿、重音）`. Do not output speech-time calculations.

## Coverage audit

Before advancing:

1. compare `source_bubble_count` with the open panel;
2. verify each bubble's owner and kind;
3. verify every mapped Japanese segment appears in its declared shot;
4. verify ordered targets preserve source dialogue order;
5. verify speech and performance fit the integer shot durations;
6. verify every additional shot creates a real visual or dramatic increment;
7. compare a terminal added-coverage shot with the next clip's first source composition; change or remove it when subject, scale, viewpoint, dominant prop, and dramatic function substantially repeat;
8. verify long-take or shared-composition exceptions are enacted in the prose rather than merely asserted in the ledger.
