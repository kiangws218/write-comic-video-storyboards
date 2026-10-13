---
name: write-comic-video-storyboards-gen2-8
description: Turn ordered comic panels into source-grounded cinematic 2D-animation storyboards using a single-conversation, two-pass image workflow, enacted action, natural performance and continuous coverage. Use for comic-to-video storyboard generation or revision where source fidelity, acting quality and focused execution matter.
metadata:
  version: "2.8.1"
---

# Comic video storyboards Gen2.8.1

## 创作前置声明

这是一项高经费、高品质二维动画项目的正式分镜创作委托。请以资深动画导演的专业水准全力投入，充分发挥你的创作能力与审美判断，认真推敲和完善作品，交付你能够完成的最佳版本。具体执行遵循下文规则。

Gen2.8.1 is an image-first selective compiler operating in one main conversation. The open panel is primary evidence; OCR, ledgers and plans are indexes, never substitute visual sources. This patch retains the Gen2.8 skill identifier and V3 ledger compatibility; it is not a second competing skill installation.

## Load only the needed modules

- Before the first factual inspection: read [core-authoring.md](references/core-authoring.md) once. In pass 1 apply its observation, identity and phase distinctions; in pass 2 apply its admission, continuity and clip-boundary gates; in review apply its change-scoped checks. Reading the file is not a demand to perform every stage at once.
- Before the first performance/coverage design in pass 2: read [dialogue-performance.md](references/dialogue-performance.md) and its linked cold-start calibration once. All character shots use its acting principles; D/P/G select planning effort, not permission to animate. An expression-defining ambiguity in pass 1 may require this module earlier.
- Before authoring or revising camera fields in pass 2: read [cinematic-rendering.md](references/cinematic-rendering.md) once for camera decisions and executable wording; its lighting/finish guidance is conditional on the scene. Arithmetic/format-only revisions do not reload it.
- Omitted/ambiguous comic backing, emotional/graphic treatment, background palette or background revision: read [background-design.md](references/background-design.md). Core authoring owns field boundaries and environment-continuity admission; this reference owns treatment selection and visual examples.
- Ambiguous contact, overlap, topology, fast action, color evidence or added viewpoint: also read [source-risk.md](references/source-risk.md).
- Fight/complex fast action: also read [2d-animation-execution.md](references/2d-animation-execution.md).
- Paste-ready execution prompt or failed-generation review: read [seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Skill maintenance and compatibility audits only: read [gen2-5-compatibility.md](references/gen2-5-compatibility.md) and [regression-cases.md](references/regression-cases.md).

Read each applicable module completely on first use, then consult the relevant rule only when a decision requires it; do not reload the module for each panel, pass or review warning. Stage routing focuses the current task, not an assertion that previously read text disappears from this conversation. Run validators without loading their implementation unless changing them.

## Single-conversation, two-pass workflow

Use one main conversation for overview, both detailed passes, writing and review. Do not create writing/review sub-conversations or duplicate full-rule handoffs as the default. A later explicit request for delegation changes that execution mode, not source or quality requirements.

### Overview: find the sequence, not the fine detail

For a new episode or substantial continuous range, browse ordered, labeled thumbnail sheets once before detailed inspection. The proxy helper's `--overview` option produces small paginated sheets and a filename index. Confirm the source order; use the preview only to propose continuous scene/beat ranges, locate drawn environment references and flag likely gaps or difficult panels. Keep only that compact map in the existing audit. No episode-wide transcription, performance plans or source-pass attestations come from thumbnails. A single giant sheet is not a readable overview. A narrow revision or an explicit user opt-out skips this stage.

### Pass 1 — observe and understand

Within the current continuous beat, inspect one to three contiguous panels individually at cached 720p. Finish their factual pass before drafting their shots; then do pass 2 on that same local window before moving onward. Long beats may span windows; a window is a memory aid, never a shot or clip boundary. Consult the immediate neighbor when needed to understand the phase or future boundary, not to transcribe the rest of the episode.

Update the existing V3 panel records from the images: composition (including camera pitch versus head facing and gaze), visible entities/actions/relations, decisive expression shape, original bubble text/owner/kind/order, actual or omitted backing, and typography-only overlays. Resolve canonical identity against supplied references; flag uncertainty instead of guessing. Separate observations from story context and identify the physical source phase and persistent versus phase-specific constraints. Note only consequential open questions and possible continuity gaps. These observations do not yet decide final shot count, motion path, background treatment or duration, and a source pose is not a frozen video or first-frame input.

The exit condition is usable, honest evidence for the current window, not a fully populated final ledger. Resolve a decision-critical uncertainty at useful resolution or leave the affected decision explicitly blocked. Do not invent off-screen facts or perform a full creative/validation checklist during this pass.

### Pass 2 — look again, design and write

Reinspect each current panel individually while creating its shots; keep it visually available through comparison with the prose. This is a deliberate second detailed reading, not merely rereading pass-1 notes. Reuse the same 720p proxy; escalate to 1080p/original only for a still unresolved decision-changing detail, recording why. Correct pass-1 evidence if this view reveals an error, rather than treating its record as superior to the image.

Resolve present characters' confirmed performance profiles, final Japanese and ordered semantic turns. Within core's temporal-action admission boundary, develop the necessary lead-in, depicted phase and supported continuation, then task/interaction-led acting using dialogue-performance's calibration. Plan acting before optional close-ups; complete the existing `motion_decision`, D/P/G decisions and selective P-card before formal prose. Choose coverage and purpose-led camera behavior with concrete openings/landings, not a fixed-camera default or movement quota. Compare added coverage with both neighboring compositions under core's contrast gate. Finalize physical/continuity/graphic/occluded backing from inspected evidence, not thumbnail tone or gray screentone alone.

Confirm actual outgoing/incoming states and any necessary bridge, then group neighboring complete panel units by natural timing under the 15-second ceiling. Render the full six fields and compare source fidelity **and enacted temporal change** against the images. Keep one set of observed facts, admissions, cards and exact rendered excerpts in the existing V3 records; there is no pass-2 copy of the evidence ledger. A newly added view is separately planned coverage, not an excuse to omit the source panel's second reading.

### Review — targeted correction, not a mandatory third reading

Validate the current window and resolve blockers before advancing. Apply comparative acting review to the exchange and audit its actual cut/clip boundary states; zero errors alone is not approval. Keep a tentative clip open across windows until the immediate next unit is assessed. Carry only the current task/contact/facing/ownership state, relevant environment/palette, tentative clip time and unresolved decisions into the next window; the existing ledger remains the authoritative history, not a summary rewritten each time.

After the two detailed passes and prose comparison, reopen only decision-changing evidence affected by a warning or revision under core's change-scoped reinspection rules. Formatting/arithmetic fixes do not trigger new image reads. Order/scope changes or demonstrated systemic visual errors can require broader reinspection. An already approved narrow revision uses this scoped path, not a forced new overview and two complete episode passes.

The same conversation retains prior context: avoid printing full historical ledgers, completed scripts and whole modules repeatedly. Reuse exact approved records and inspect current targets. Do not claim a token-saving percentage or visual-pass completion from read counters, script execution or booleans; record only work actually performed. This workflow changes attention allocation, not the required richness of acting or the six-field output.

## Non-negotiable outcomes

- Preserve every bubble's meaning, owner, kind, order and natural Japanese. A named speech trigger quotes exact final Japanese inside `「」`; otherwise use a generic timing node such as `重音处` or `句末`.
- Never bind a comic panel/crop as the video's first frame or start-keyframe input. Treat it as an in-process/contact/result anchor, restored at its declared phase rather than every frame. Core authoring owns opening design, bounded cross-shot transitions and execution-mode compatibility; a first-frame-only tool is not an excuse to omit an admitted lead-in. Transitions enact an established action or reconcile supported states; they cannot invent additional people, objects, unsupported contacts/routes, independent events/results, hidden motives or stronger unsupported emotions.
- Close every renderable target against the current shot. A named target of gaze, gesture, touch, movement, camera tracking, light/effect or sound must be visibly established by that shot's source/approved derived view; story continuity and dialogue meaning do not establish it. When only direction is visible, use screen-relative wording such as `看向画面左侧外/镜头下方` and omit the unseen name.
- A dialogue verb or intention never proves matching visible motion: `快跑/攻击/给我` does not authorize running, attacking or handing over. Admit substantive action from a directly supplied phase or core authoring's bounded necessary-transition/cross-shot gate. Its visible part must fit the crop and restore source anchors; absence of an explicitly drawn lead-in is not by itself a rejection reason.
- Manga typography is never video content. Do not describe visible glyphs, language, lettering, balloons, caption boxes, labels or page furniture in any generatable field. Convert an SFX overlay only to its concrete sound; if a panel contains no renderable visual content, map that sound into an adjacent visible shot and omit the standalone visual shot.
- Preserve semantic turns first, then group adjacent short turns when one setup can carry them without hiding a cut or burying an important reaction. Similar required coverage is redesigned, not deleted. A new shot cannot duplicate either the preceding shot or the following source-panel composition; focal-length changes, focus pulls or tighter crops alone do not establish a new composition.
- Normally keep a panel's complete coverage in one clip; that clip may contain several consecutive panels and numbered shots. This is non-fragmentation, not one-panel exclusivity. Core authoring owns grouping toward 15 seconds without exceeding that ceiling or padding. An explicit lower user limit wins. When one panel's natural full dialogue/necessary performance still exceeds the ceiling after correct shot planning, use core's documented overflow split at stable semantic/action boundaries; each resulting clip remains within the ceiling. This exception does not permit routine per-panel fragmentation or thinning acting.
- Plan character participation through the exchange under `dialogue-performance.md`, using its calibration, P-card and time-course/interaction review. A current state at the cut need not be motionless. Core authoring owns physical admission and continuity; acting choices and semantic quality have one owner, not a duplicate checklist here.
- Each clip cold-starts with positive current pose, orientation, counts, contact, backing, light, gaze direction and stable labels. No cross-shot pointers or negative controls.
- Save tokens through routing, 720p inspection and mechanical validation—not by shortening the six-field storyboard.

## Delivery

- Ordinary shots use `分镜N（X秒）`; eligible combat may use one `战斗段N（X秒·自动分镜）`. Every real cut is numbered.
- Field order is `【镜头设计】`, `【可见动作】`, `【可见背景】`, `【台词与语气】`, `【光影布光】`, `【声音设计】`.
- `【镜头设计】` owns angle/axis, scale/focal length, crop/layout, depth/overlap/negative space, focus, camera move and landing. `【可见动作】` is the single owner of subject/object motion, performance and endpoints. Other fields must not restate or newly assert that motion. `【可见背景】` owns environment or graphic backing, never performer anatomy/clothing/prop surfaces used as filler. Core authoring defines the legitimate fully occluded case. Physical scenery is the normal spatial baseline; graphic treatment serves a supported beat, not every undrawn manga background.
- `【台词与语气】` alone owns speech, speaker, voice, vocal emotion, pace, pause, stress, distance and dialogue spatial treatment. `【声音设计】` contains only environment sound, Foley, breath/body sound and silence; it may use `句末/重音后` only as a synchronization marker, never restate a voice or dialogue delivery. Do not add BGM, score or theme music.
- Keep all evidence explanations, inference/admission reasons, performance cards and review results in the internal source ledger, not the formal script's fields, notes or appendix. Rich short-shot acting is valid when its actual serial/concurrent timing fits; no action-count or body-part quota.
- Structural/source/performance blockers stop delivery. Heuristic advisories may remain only with a per-shot image-based disposition.

```powershell
python scripts/build_analysis_proxies.py <panel-folder> --overview
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <proxy-folder> --source-ledger <source-ledger-v3.json> --require-source-ledger
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
python -m unittest discover -s scripts -p "test_*.py"
```

Report clip count, runtime, reference count, blocking validation, advisories by class, manual-overflow items, source audit, rule-input size and absolute output paths.
