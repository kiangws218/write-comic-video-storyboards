# Regression cases for skill maintenance

Read only when modifying or forward-testing this skill. These cases protect behavior; do not turn each case into a duplicated rule.

| Case | Required result |
|---|---|
| Panel shows left-hand skewer and right-hand map; dialogue mentions money | Keep eating and reading the map; do not replace them with coins. |
| Character wades through cave water behind rock columns | Treat as State; use water ripples and passing rock-column occlusion, not wall-bracing or crawling. |
| Close-up cough does not show the supporting hand | Do not add a hand bracing on a bench or wall. |
| Previous panel shows a medicine bottle; current face close-up does not | Keep the bottle off-frame unless an uncited shot reintroduces it. |
| Listener is absent from the cited speaker composition | Use an uncited reverse shot or hard-cut sub-shot; do not pull the listener into the cited frame. |
| Character looks upward in a high-camera view | Determine angle from perspective; do not label it low-angle because of gaze. |
| Subject is left-third or side-view | Preserve placement and viewing direction as separate facts; do not default to centered/front. |
| A two-person cited crop has one large foreground subject on the left, a partly occluded subject behind on the right, and a prop extending rightward | Trigger the compact composition lock; preserve screen-left/right, depth, overlap, and prop direction. Never rearrange subjects by speaking order, narrative importance, or inferred world-space direction. |
| A floor-level crop looks through a standing character's legs while two large object halves fill both foreground sides | Trigger the unusual-viewpoint composition lock; preserve the between-leg camera, near/far hierarchy, and visible object placement instead of rebuilding an ordinary distant full shot. |
| A close-up shows one hand gripping one cord connected to one oval moving end against a white background | Trigger the topology lock; keep the count, connections, gripping hand, moving end, and white background. Do not infer a second hand, repeated beads, or physical scenery from context. |
| A cited comic composition occurs midway or at the endpoint | Reference that phase directly; do not force it to be the opening frame or a static hold. |
| Adjacent panels explicitly show compression followed by launch | The phases may be connected in one continuous shot with both references in order; do not add circling, landing, or another attack. |
| Two adjacent numbered shots repeat one dialogue-panel reference, viewpoint, scale, and camera purpose | Merge them, or turn the later block into a genuinely different uncited reverse/insert. A new speaker alone is not a new shot. |
| Timed prompt contains “保持原格姿势”, “按照原格处理”, “不出现湖岸实景”, or sound-effect text | Fail structural validation; rewrite as positive visible content and remove audio production instructions. |
| Long or multi-speaker dialogue | Allocate natural time; use reverse/environment/prop/detail inserts without inventing events. |
| Combat panel shows only contact | Do not auto-create anticipation, travel path, recovery, and landing unless the source supplies them. |
| Every shot in a known location | Describe all useful local background actually visible; do not impose a fixed detail quota or repeat unseen environment text. |
| A root creature opens its mouth and screams in one reaction panel | Use a short burst of roughly 2–4 seconds; end early instead of filling the clip with prolonged screaming or shaking. |
| An exertion face and `?!` accompany “why won’t it come out?” | Describe strain, confusion, or impatience; do not infer combined shock and rage from punctuation alone. |
| A clean gradient portrait has no established backlight | Keep the gradient; do not add rim light, glow, flare, or particles for generic polish. |
| A forest scene switches to a source-supported solid or speed-line panel | Preserve the abstract background; do not reinsert trees, shrubs, or terrain into that cited composition. |
| A supported pulling action shows hand, stance, direction, and endpoint | State those visible anchors precisely and keep the prop name/material/color stable; do not add unsupported mechanics. |
| A dialogue shot contains a gaze shift, nod, and small hand movement | Run them during speech; duration is pre-action + max(speech, concurrent performance) + post-action, not a sum of every gesture. |
| A clip formerly used `0-3s` and `4-8s` ranges | Output `分镜1（3秒）` and `分镜2（5秒）`; reset numbering per clip and validate the summed duration. |
| A panel uses strong foreshortening, overlapping limbs, impact debris, or an off-frame attacker | Review it at original resolution after the default 720 px pass; verify motion direction, airborne/grounded state, contact, and foreground/background hierarchy before writing. |

Forward-test on raw panels and compare against these required results. Structural validation passing is insufficient; record a separate manual source-fidelity verdict.
