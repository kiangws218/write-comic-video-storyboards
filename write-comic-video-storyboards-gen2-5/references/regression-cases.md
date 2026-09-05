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
| One speaker has 28+ meaningful Japanese characters in one continuous turn | Trigger visual-load planning by character count before timing. Preserve the source composition, then add source-compatible coverage when one view lacks meaningful change; at 42+ characters or three clauses, normally use at least two numbered shots. |
| One panel contains five bubbles from two speakers | Trigger the dialogue ledger before drafting, preserve bubble order and ownership, estimate speech before clip boundaries, and split coverage rather than compressing all turns into the remaining seconds. |
| A clerk's small opening bubble is followed by a guest apology and inner thought | Record three rows with clerk/dialogue, guest/dialogue, and guest/inner ownership; do not assign the opening line to the guest or omit the final thought. |
| A crowded panel ends with a small listener reaction after two bystander lines | Map the final reaction as its own bubble; a structurally valid storyboard that omits it fails dialogue-source audit. |
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
| A cited action panel is called a key pose but the prompt changes its camera angle, left/right placement, overlap, silhouette, or contact | Fail the source audit. Restore the cited composition at its declared phase; place any different view in an uncited internal cut. |
| A source-faithful action clip benefits from foot/hand microcuts, an environment pause, or a reaction insert | Allow the uncited coverage when it clarifies the existing beat and preserves every source anchor; reject it if it creates a new route, contact, event, or replaces the source-important view. Every actual cut receives the next shot number and its own integer duration, while the shots remain in one clip when continuity requires it. |
| A continuous attack contains anticipation, acceleration, a readable body unfold, contact, and recoil | Keep the complete action in one clip when it fits 15 seconds. State the rhythm contrast and in-between concentration; when the camera cuts, give each resulting shot a number and integer duration. |
| A monster has no supplied reference asset and its lore name is visually opaque | Use a stable visual label with scale, color, surface, body type, and defining anatomy at the first appearance of each clip; do not rely on the lore name alone or alternate labels. |
| A character looks toward a poster shown only in the previous panel, while the current crop contains no poster | Describe the visible gaze as forward, downward, or toward the relevant screen edge. Do not put the poster in the character's hand or name it as the current-frame target unless a new uncited view establishes it. |
| Adjacent panels show load→launch→airborne rise and the complete phrase fits within 15 seconds | Keep all phases in one generated clip with references in order. Do not end one clip after launch and restart the next in midair. |
| Adjacent panels show strike travel→contact→immediate recoil and the complete phrase fits within 15 seconds | Keep the physical cause and consequence in one generated clip; a camera cut starts the next numbered shot with its own integer duration, but not a new clip. |
| A high-speed body crosses frame | A narrow directional air-distortion or screen-wash effect may follow the leading edge and collapse after passage; it must not alter the cited pose or screen direction. |
| A weapon makes decisive contact | A brief black-white impact frame or compact pressure ring may occur exactly at contact, followed by proportional material/environment response; do not stack unrelated flare, smoke, particles, and distortion. |
| A blade rotates under an established light source | A brief highlight may travel along the reflective edge and fade as the angle changes; do not add a generic rim around the whole character. |
| A panel follows a known character carrying someone, but the current panel is small, occluded, or visually ambiguous | Do not assign either person's identity from plot continuity alone. Confirm the name from the current panel plus an explicit character mapping or unique visible trait; otherwise use descriptive role labels. |
| A storyboard needs one look statement usable by every shot | Start with `场景色彩基准` covering only global tone, style, rendering or texture, contrast or saturation, and lighting behavior. Do not list concrete objects or prescribe object-specific colors there. |
| One generated clip contains a speaker view, a reverse shot, and a prop insert | Output three consecutively numbered shots with a positive integer duration for each; do not hide the reverse shot or insert as an untimed line inside the first shot. |
| A combat panel contains a large cropped black shape crossing buildings and adjacent geometry shows a sweeping tapered body part | Trigger the topology lock and identify the supported tail/wing/limb plus its vector; do not downgrade it to a generic shadow, wall, or impact mass when contour and debris direction establish the body part. |

Forward-test on raw panels and compare against these required results. Structural validation passing is insufficient; record a separate manual source-fidelity verdict.
