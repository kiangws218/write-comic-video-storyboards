---
name: write-comic-video-storyboards-gen2-8
description: Turn ordered comic panels into source-grounded cinematic 2D-animation storyboards with enacted action, natural character performance and dialogue coverage, inspecting cached image proxies and validating source fidelity without compressing the six-field output. Use for comic-to-video storyboard generation or revision where quality and token efficiency both matter.
---

# Comic video storyboards Gen2.8

## 创作前置声明

这是一项高经费、高品质二维动画项目的正式分镜创作委托。请以资深动画导演的专业水准全力投入，充分发挥你的创作能力与审美判断，认真推敲和完善作品，交付你能够完成的最佳版本。具体执行遵循下文规则。

Gen2.8 is an image-first selective compiler. The open panel is primary evidence; OCR, ledgers and plans are indexes, never substitute visual sources.

## Load only the needed modules

- Every storyboard: read [core-authoring.md](references/core-authoring.md) for source locks **and temporal action design**, then [dialogue-performance.md](references/dialogue-performance.md) for dialogue coverage and task/relationship-led acting, including its linked cold-start calibration. All character shots use its acting principles; D/P/G select planning effort, not permission to animate.
- Camera planning/revision, premium light/material finish or named production target: also read [cinematic-rendering.md](references/cinematic-rendering.md).
- Omitted/ambiguous comic backing, emotional/graphic treatment, background palette or background revision: read [background-design.md](references/background-design.md). Core authoring owns field boundaries and environment-continuity admission; this reference owns treatment selection and visual examples.
- Ambiguous contact, overlap, topology, fast action, color evidence or added viewpoint: also read [source-risk.md](references/source-risk.md).
- Fight/complex fast action: also read [2d-animation-execution.md](references/2d-animation-execution.md).
- Paste-ready execution prompt or failed-generation review: read [seedance-execution-and-review.md](references/seedance-execution-and-review.md).
- Skill maintenance and compatibility audits only: read [gen2-5-compatibility.md](references/gen2-5-compatibility.md) and [regression-cases.md](references/regression-cases.md).

Run validators without loading their implementation unless changing them.

## Compile loop

Work on one to three contiguous panels. Keep the exact panel open until its shot text is compared back to it. Use cached 720p proxies by default; open 1080p/original only when a decision-changing detail remains unresolved and record why.

When character references are supplied, resolve their names under the identity gate in `core-authoring.md` before rendering character labels. Choose camera behavior by the purpose/evidence gate in `cinematic-rendering.md`, not by a fixed-camera default or a movement quota. For revisions and final review, use the change-scoped reinspection rules in `core-authoring.md`; unchanged approved images do not need a blanket second pass.

1. Record `composition_lock` and atomic `source_facts` (`entities/actions/relations`) from the open image. Distinguish persistent source constraints from phase-specific pose/composition under core authoring; do not freeze the full shot. Separate printed manga overlays into `page_overlays`; glyphs, speech balloons, captions, labels and page furniture are evidence to interpret, never renderable scenery or composition. Put plot meaning, identities inferred only from continuity and dialogue intent in `story_context`; list their tempting but invisible render words in `non_renderable_terms`. Context is never render evidence.
2. Classify State/Action/Reaction/Mixed and establish the supported temporal phrase under core authoring as the boundary for full performance design: distinguish the physical phase from its placement in the video, declare where the source pose lands, and include an admissible necessary lead-in when the depicted action begins here. The comic need not draw every intermediate pose. Provisionally apply core's cross-shot continuity gate to identify direct cuts, coordinated local C/A or bounded action bridges; actual boundaries are confirmed after acting and coverage are planned. Retain an intentional state only for an evidenced reason. While the panel is open, assign `D` dialogue/coverage, `P` expressive performance and `G` fragile geometry only where needed; these flags do not replace this motion decision.
3. Resolve ordered dialogue turns and coverage groups before camera count. Design the scene's supported performance within core authoring's admission boundary before choosing added close-ups; preserve the anatomy and partner relation needed to read it. For every added view, assign a distinct visual function and compare a compact composition signature against both the immediately previous planned shot and the next source-panel composition; it must differ from each available neighbor on at least two meaningful dimensions or be redesigned/merged. Use dialogue-performance's calibration and scene patterns to develop the current task/interaction, then record one compact card for each `P` shot. Confirm actual outgoing endpoints and incoming openings under core's continuity gate, including any bridge and its time, before grouping complete panel units under the clip-boundary gate. Neither a new panel nor an inspection-batch boundary starts a clip. Escalate a `G` detail beyond 720p only when necessary.
4. Apply the three admission gates to the planned temporal phrase. Before background prose, resolve visible environment, bounded continuity reconstruction, purposeful graphic treatment or complete occlusion under core authoring; gray/blank manga backing alone does not select the graphic route. Then render the opening, readable change and endpoint in the six-field shot. Dialogue/story meaning alone fails the evidence gate. Record exact `fact_claims` and major-action admissions; compare source fidelity **and whether the supported action was actually enacted**, not just anatomy keywords, with the still-open panel. Resolve duration after speech and motion intervals are known.
5. Validate the small batch and fix blockers before advancing. Under core's continuity gate, audit actual affected cut/clip boundaries after prose and any state-changing revision, including returns after reaction coverage; retain the concrete outcome in the existing audit. Separately apply dialogue-performance's comparative acting review; safety, a populated card and zero errors certify neither continuity nor acting quality. Never reconstruct source evidence from completed prose.

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
- `【台词与语气】` alone owns speech, speaker, voice, emotion, pace, pause, stress, distance and dialogue spatial treatment. `【声音设计】` contains only environment sound, Foley, breath/body sound and silence; it may use `句末/重音后` only as a synchronization marker, never restate a voice or dialogue delivery. Do not add BGM, score or theme music.
- Keep all evidence explanations, inference/admission reasons, performance cards and review results in the internal source ledger, not the formal script's fields, notes or appendix. Rich short-shot acting is valid when its actual serial/concurrent timing fits; no action-count or body-part quota.
- Structural/source/performance blockers stop delivery. Heuristic advisories may remain only with a per-shot image-based disposition.

```powershell
python scripts/build_analysis_proxies.py <panel-folder>
python scripts/validate_storyboard.py <storyboard.md> --max-seconds 15 --image-dir <proxy-folder> --source-ledger <source-ledger-v3.json> --require-source-ledger
python scripts/audit_seedance_prompt.py <execution.md> --max-seconds 15 --max-chars 1900
python -m unittest discover -s scripts -p "test_*.py"
```

Report clip count, runtime, reference count, blocking validation, advisories by class, manual-overflow items, source audit, rule-input size and absolute output paths.
