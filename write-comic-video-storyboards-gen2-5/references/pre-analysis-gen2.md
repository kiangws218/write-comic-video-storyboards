# Gen2 pre-analysis

Read this file only for a new/full episode, ambiguous panels, long or multi-speaker dialogue, or a requested analysis artifact. `storyboard-spec.md` remains authoritative for action and reference rules.

## Decisions

- **保格**: preserve a recognizably important composition and beat.
- **拆格**: split long dialogue, multiple speakers/actions, or incompatible camera purposes.
- **补格**: add a necessary establishing, connective, reaction, insert, or result shot; never manufacture a complete action chain.
- **并格**: combine adjacent low-information panels that share one beat and natural timing.

Record whether adjacent panels form a continuous action, successive scene, or independent/montage relationship. Choose continuous take, phased take, or multishot hard cut; never label one clip both continuous and hard-cut.

## Two-level ledger

Use the minimal row for ordinary beats:

| Crop↔original | Location | Dialogue | State/Action + reaction | Visible people/props | 保拆补并 | Reference? | Ambiguity |
|---|---|---|---|---|---|---|---|

Add a risk note only when inference, hand/prop assignment, reference suitability, or continuity is fragile:

`entering state｜source-visible B｜known exit｜allowed A/C｜off-frame continuity｜forbidden visible additions｜viewpoint/placement/overlap/hands-props anchors`

Adjacent panels establish chronology and off-frame continuity, not current-frame visibility. If an added phase fails evidence, visibility, or anchor safety, delete it or make a necessary composition change an uncited shot.

Character identity is not a continuity inference. Use a name only when the current panel contains a mapped or discriminating visible trait; the preceding and following panels may suggest whom to compare but cannot decide the label. When the current view is too small, occluded, silhouetted, or visually ambiguous, record a descriptive role label and mark identity ambiguity instead of borrowing a name from the plot.

## Dialogue and load

Translate and count before segmentation, then estimate speech time. Split at a question/answer, clause boundary, interruption, completed action, reaction, or stable endpoint. Long dialogue may continue over a reverse shot or visible environment/prop/detail insert. Do not reserve 15-second containers first; dialogue and required action determine the clip boundary.

### Mandatory dialogue gate

Create an internal dialogue-risk entry before drafting when a panel has any of:

- 3 or more source bubbles;
- 2 or more speakers;
- both spoken dialogue and inner speech/narration;
- one speaker's continuous final Japanese turn reaches 28 meaningful characters after removing spaces, punctuation, and performance notes, or contains 3 complete clauses.

Use source-language length only to flag a likely case before translation. For a 28–41-character turn, record whether the source composition has enough evolving action or performance to remain one shot. At 42 characters or three complete clauses, choose at least two genuinely different numbered shots unless the ledger records a deliberate long-take reason. Suitable coverage includes a source panel, listener or creature reaction, environment, prop/detail, or a new viewpoint that clarifies the established beat.

Inspect the panel at the drafting resolution and record every bubble in visual reading order. A small bubble, interjection, final reaction, or inner monologue is still a row. Do not infer speaker ownership from the later reply; establish it from bubble tails, placement, panel order, and the original page. Before leaving the batch, compare the declared `source_bubble_count` with the open image and compare each mapped `script_text` with its target shot.

Use this compact JSON sidecar only for triggered panels; ordinary panels stay on the minimal ledger. It is an internal validation artifact and is not delivered unless requested.

```json
{
  "version": 1,
  "panels": [
    {
      "image": "panel_009_002.jpg",
      "source_bubble_count": 3,
      "coverage": "reverse",
      "bubbles": [
        {
          "id": "b1",
          "speaker": "店员",
          "speaker_evidence": "气泡尾指向左侧店员",
          "kind": "dialogue",
          "source_text": "那个……客人？",
          "status": "mapped",
          "script_text": "あの……お客さん？",
          "seconds": 2,
          "target": "片段13/分镜3"
        }
      ]
    }
  ]
}
```

Allowed `coverage`: `shared`, `reverse`, `insert`, `mixed`. Allowed `kind`: `dialogue`, `inner`, `narration`. When a panel has multiple speakers, every row also records concise `speaker_evidence` from the open image, such as bubble-tail direction, bubble placement plus turn order, narration-box form, or inner-bubble style. Each row uses `status: mapped` with `script_text`, positive `seconds`, and `target`, or `status: omitted` with a nonempty `omission_reason`. Omission is exceptional and must preserve the user's requested source fidelity.

The gate passes only when:

1. the open source image and `source_bubble_count` agree;
2. every bubble has the correct speaker and kind;
3. every mapped line occurs in the declared target shot;
4. sequential speech mapped to a shot fits that shot's integer duration;
5. the chosen coverage creates a real visual or dramatic increment;
6. affected platform-safe replacements preserve the passed shot-duration pattern unless their number of turns genuinely changes.

For a multi-turn panel, record one compact coverage choice: `shared composition｜speaker/listener reverse｜environment/prop/detail insert`. If splitting creates no change in subject focus, scale, viewpoint, composition, visible information, or dramatic function, merge the shots. Dialogue turn alone does not justify a duplicate shot.

Only for high-load clips record:

- primary generation target;
- one secondary target;
- fragile anchor;
- deliberate simplification.

## Output policy

Keep the ledger internal unless requested or ambiguity is extensive. Normally output only:

- uncertain mappings or decisions needing review;
- compact prompts for every location;
- structural line-art/rendering packages only for recurring complex locations;
- material source deviations;
- affected platform-safe mappings.

Generate the SRT after storyboard approval unless requested earlier. Do not create a generated-footage continuity ledger; the comic remains authoritative.
