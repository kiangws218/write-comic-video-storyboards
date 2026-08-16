# Gen2 pre-analysis

Read this file only for a new/full episode, ambiguous panels, long or multi-speaker dialogue, or a requested analysis artifact. Keep the working ledger internal and compact by default.

## Core classifications

- **保格**: preserve a panel whose composition and beat should appear recognizably.
- **拆格**: split long dialogue, multiple speakers/actions, or incompatible camera purposes.
- **补格**: add only necessary establishing, connective, reaction, or result material. Do not use it to manufacture every missing phase of a complete action arc.
- **并格**: combine adjacent low-information panels sharing one beat and natural timing.

Adjacent relationship: continuous action chain / successive scene / independent scene or montage.

Video structure: continuous take / phased continuous take / multishot hard cut. Do not call one clip both continuous and hard-cut.

Image behavior:

- **Hold**: retain the reproduction point; animate with motivated micro-actions that preserve or return to it.
- **React**: ongoing state → perception → response → readable full emotion → recovery/decision/result.

Behavior type precedes motion density:

- **State**: an ongoing condition such as travel, waiting, rest, observation, vigilance, or atmosphere. Use restrained continuity: existing repeated action, gaze/expression, prop/cloth movement, medium feedback, and environment/light.
- **Action**: an act whose shown process or result changes a prop, body, location, or story state. Record the source-visible phase; do not assume setup → execution → response → result → endpoint must all be supplied.
- **Reaction** is an optional tag, not a peer replacement for State/Action. For mixed beats, record primary and secondary types and preserve both.

## Compact ledger

Record one row per beat:

| Crop↔original | Location | Characters | Visible action/pose | Dialogue | Props/hands: visible｜off-frame continuity | Enter→exit / visible phase | 保拆补并 | State/Action + reaction tag | Relationship/structure | Reproduction anchors | Ambiguity |
|---|---|---|---|---|---|---|---|---|---|---|---|

For 保格, reproduction anchors must cover framing/viewpoint, arrangement, pose, left/right hand–prop assignment, expression/gaze, and layer hierarchy.

For an action beat that invites inference, add one compact note to the row: `allowed:` actions supported by the current crop and visible in-frame; `forbidden:` off-frame contact, unseen props/body mechanics, or phases not shown in the current crop. Adjacent panels establish chronology and off-frame continuity only; they do not authorize visible additions to a cited composition. Before drafting, test each substantive added body/prop action for source evidence, in-frame visibility, and anchor safety. Failing any one means delete it or move a genuinely necessary composition change to a separate uncited 补格 shot.

Never infer replacement visuals from dialogue nouns: money does not imply coins, danger does not imply a visible monster, and memory does not imply a flashback. Put a genuinely necessary new composition in an uncited 补格 shot.

## Dialogue and generation load

Time each speaker naturally before segmentation. Split at question/answer, interruption, completed action, or reaction. If a useful listener reaction is not visible in the preserved speaker crop, plan it as a brief separate uncited reverse shot while the speaker continues off-screen; do not add the listener to the cited composition.

Only when generation complexity is high, note:

- primary target;
- one secondary target;
- fragile anchor;
- deliberate simplifications.

Do not generate a separate full load table for every ordinary clip.

## Output policy

Normally output only:

- uncertain source mappings or decisions needing review;
- a compact environment prompt for each simple or one-off location that can be generated without a reference image;
- structural line-art and rendering packages only for recurring spatially complex locations, with an additional compact prompt for every such package; never output an overhead plan;
- material deviations from the source;
- affected safe-version mappings.
- the companion Chinese SRT, ordered by clip/time/speaker and separated into master and platform-safe files when applicable.

Output the full ledger/table only when the user requests it or ambiguity is extensive. Do not add a generated-footage continuity ledger; the comic remains authoritative.
