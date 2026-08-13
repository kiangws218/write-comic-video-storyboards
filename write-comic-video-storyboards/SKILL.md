---
name: write-comic-video-storyboards
description: Turn ordered comic, manga, manhua, or webtoon originals and cropped panels into source-faithful, production-ready AI video storyboards. Use when Codex must recover text missing from crops, run a preserve/split/fill/merge pre-analysis, time dialogue naturally, create structured short clips capped at about 15 seconds, cite only composition-matching reference images, plan reusable environments with line-art and overhead assets, or revise and audit comic-to-video prompts.
---

# Write Comic Video Storyboards

Create detailed short-form animation storyboards that preserve the comic while giving the video model enough visible action, environment motion, and performance direction to produce animation rather than a lightly moving panel.

## Workflow

### 1. Establish constraints

Determine or reasonably default:

- original-page and cropped-reference directories;
- reading order and original-to-crop correspondence;
- maximum clip duration, defaulting to 15 seconds as a soft ceiling;
- dialogue language, character naming, output format, and destination;
- voice style and whether the user supplied character-reference images.

Use generic labels such as “女孩”“男孩”“女仆” until character references are supplied. Do not add BGM; retain dialogue, narration, ambience, and action sound only.

### 2. Inventory both source layers

List images in natural numeric order. Create non-destructive review copies before visual inspection: default to about 540 pixels wide while preserving aspect ratio; keep originals unchanged. Inspect all originals and crops once through contact sheets or these review copies. Create or open a roughly 720-pixel copy only when small text, hand–prop assignment, facial detail, complex action, or ambiguity cannot be resolved at 540 pixels; open the full-resolution source only as a final exception. Do not repeatedly load full-resolution panels already understood.

- Read original pages for missing dialogue, narration, order, and wider context.
- Use cropped filenames for every formal `分镜参考` citation.
- Inspect the previous, current, and next panel before assigning speakers, positions, props, or movement; expand to five panels when ambiguous.

### 3. Complete a pre-analysis before drafting

Build a scene ledger with crop filename, original page, location, characters, entering state, visible action, exiting state, dialogue, props, and ambiguities.

For each beat, decide:

- **保格** — retain a panel whose composition and beat already work;
- **拆格** — split long dialogue, multiple speakers, or multiple actions into separate timed shots;
- **补格** — add the minimum connective action, establishing shot, reaction, or result required for animation continuity;
- **并格** — combine adjacent low-information panels that share one beat and comfortably fit the timing budget.

When one panel contains long dialogue or two to three speakers, allocate time by dialogue turn. Use listener reactions, question-answer boundaries, or completed actions as split points. Keep one complete sentence inside one generated clip.

Create a reference-suitability table before writing the formal storyboard: source information, allowed complete composition, forbidden mismatch, and actual-use decision. Keep workflow reasoning in the pre-analysis document, outside video prompts.

### 4. Budget dialogue before segmenting

Time spoken content at natural delivery speed, including breath, hesitation, clause pauses, interruption, and listener reaction. Use actual read-aloud timing when practical; otherwise read [references/storyboard-spec.md](references/storyboard-spec.md).

Allocate dialogue first, then acting and camera movement. Split the clip instead of accelerating speech. Use integer timecodes such as `0-2s`, `3-5s`, `6-10s`, `11-15s`. Never write internal estimates such as “预计发声约3.8秒”.

### 5. Plan environments before shots

Cluster the ledger by physical location.

For a recurring location, assign a stable label and create an environment package outside the formal storyboard:

1. **Structure line-art prompt** — empty establishing view, very wide shot from a high oblique angle, clear architecture, depth, openings, landmarks, elevation, and fixed-object layout; monochrome structural line art without rendered color styling.
2. **Overhead-plan prompt** — true top-down view that exposes floor plan, entrances, paths, relative distances, elevation changes, and fixed object placement.
3. **Descriptive rendering language** — geometry, materials, wear, palette, weather, atmosphere, time of day, light-source position and direction, color temperature, shadows, reflections, and permissible variants.

Name every environment with neutral physical terms such as geography, material, weather, time, or condition. Keep character names, creature names, story events, and intended actions out of both the label and all three prompts. Describe only the empty physical site and objective traces already present in it. Do not assign character entrances, positions, routes, observation areas, combat zones, or narrative functions.

Prevent environment assets from looking artificially planned:

- for natural terrain, vary microtopography, boundary curvature, vegetation age and density, ground cover, exposed soil, stones, roots, leaf litter, deadwood, path width, erosion, contour weight, hatching density, occlusion, and depth;
- for interiors and built sites, vary alignment, compartment size, spacing, object scale and orientation, passage width, wear, scratches, stains, dust, and small structural deformation;
- in overhead plans, express only physical spatial relationships;
- in rendering language, describe light falling on terrain, architecture, vegetation, and fixed objects, never on an implied character or creature.

For a one-off location, describe the visible background directly in its shot. Do not create an environment asset merely to fill a template.

Place `环境参考：【环境名】` once below the clip title. Do not repeat it in every time block. Describe the specific background visible from each shot angle so shots in one location do not inherit an identical backdrop.

### 6. Cite reference images only for matching compositions

Write `分镜参考 [文件名]` only when the target shot substantially preserves the crop's framing, viewpoint, subject arrangement, pose relationship, and principal composition.

If a shot borrows only a character, object, costume, or local detail, omit the citation and describe the new composition fully in text. Recheck citation suitability after enriching actions: remove the reference when the new major action, orientation, or end pose departs from the panel.

### 7. Split at narrative beats

Prefer boundaries at location or time changes, completed entrances/exits/reveals, dialogue turns, emotional reactions, and stable end states. Fifteen seconds is a maximum, not a target. End early when the beat is complete; do not add filler merely to reach 15 seconds.

Use hard cuts by default. Reserve a special transition for a genuine story event or key turning point, and describe its visible start and end states.

### 8. Write structured direct-generation prompts

Read [references/storyboard-spec.md](references/storyboard-spec.md) before drafting or substantially revising. Write every time block in this order:

1. optional `分镜参考 [文件名]`;
2. `景别：` framing and angle, including changes such as medium shot to close-up;
3. `构图：` subject positions, foreground, background, gaze, and depth;
4. `运镜：` positive, executable camera behavior;
5. `画面内容：` start state, ordered action, performance, secondary motion, light, dialogue, sound, and final state.

Make the picture evolve visibly:

- give the main subject a meaningful action arc with a start, change, and end pose;
- add prop feedback, cloth or hair response, environmental motion, and selective light changes;
- use blinking, breathing, or hair movement as support, not as the only motion holding several seconds;
- keep a dead, unconscious, restrained, or otherwise immobile character logically still and create movement through camera, weather, light, surrounding people, or props;
- specify colors, materials, finish, translucency, quantity, placement, motion order, and end condition for invented content.

After every character line or narration sentence, immediately add full-width parentheses describing voice timbre, tone, and emotion; add pace, pause, and keyword stress when useful. Annotate each speaker separately.

Write positive, observable instructions. Remove unnecessary negative prompt tails such as “不增加其他怪物”“不使用环绕镜头”“不推拉”; state the intended subject, composition, and camera behavior instead. Preserve negative wording only when it is a story fact or visible state, such as a missing record or a body with no breathing.

The formal storyboard body must contain only text that can be sent directly to the video model. Keep asset decisions, editorial explanations, and hidden timing notes outside numbered shot blocks.

### 9. Validate and re-check

Run:

```powershell
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15
```

Add `--image-dir <cropped-reference-folder>` to verify filenames. Treat unused duration as a warning. Fix all errors, then manually audit source fidelity, natural speech, reference suitability, environment continuity, prompt purity, action richness, and reproducible end states.

For every environment package, also audit the label and actual prompt paragraphs: they must contain no character, creature, role, route, staging-zone, or narrative-purpose language. Check that organic scenes avoid regular ovals, smooth arcs, uniform tree spacing, repeated vegetation, and mechanically even linework; check that built spaces show plausible irregularity and use rather than showroom order.

## Deliverables

Provide:

1. a pre-analysis and environment-package Markdown file containing the scene ledger, preserve/split/fill/merge decisions, reference-suitability audit, clip plan, and recurring environment assets;
2. a formal structured storyboard Markdown file containing only clip headers, clip-level environment references, integer time blocks, exact matching image references, and direct-generation prompts.

Report clip count, approximate runtime, reference count, validation result, and absolute output paths.
