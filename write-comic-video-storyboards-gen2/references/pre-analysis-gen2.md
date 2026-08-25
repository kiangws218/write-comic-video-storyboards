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

## Dialogue and load

Time speech before segmentation. Split at a question/answer, interruption, completed action, reaction, or stable endpoint. Long dialogue may continue over a reverse shot or visible environment/prop/detail insert.

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
