# 2D combat choreography and effects

Read this file for fights or complex fast action. `core-authoring.md` remains authoritative: combat polish cannot manufacture an unsupported attack, route, grip, contact, injury, recovery, or result. Use `cinematic-rendering.md` for the shared rhythm and effects quality floor.

## 1. Choose the timing mode

Use **precise-shot mode** by default. Every actual camera shot is a `分镜N（X秒）` block. Choose it when dialogue timing matters, a supplied composition must occur at an exact cut, contact or weapon topology is fragile, the fight axis is ambiguous, three or more participants compete for target ownership, or a specific reveal must land at a controlled moment.

Use **combat auto-coverage mode** only when all of these are true:

- the clip is primarily visual action and the whole continuous phrase fits within 15 seconds;
- the supplied panels establish an ordered action chain, stable participants, readable space, and a definite endpoint;
- Seedance may choose internal cuts and their exact durations without changing the story result;
- dialogue is absent or limited to a short exclamation that does not require a separate timing plan;
- every fragile source composition can still be named as an ordered beat rather than depending on an exact frame allocation.

Write one `战斗段1（X秒·自动分镜）` block for the clip. Give the total integer duration only. Inside `战斗过程`, list the action beats in source order with rhythm and coverage cues but no per-beat seconds. Do not mix this mode with `分镜N（X秒）` blocks in the same clip. If the model must not improvise a cut, return to precise-shot mode.

Auto-coverage delegates camera scheduling, not story invention. It may select coherent wide, medium, close, insert, tracking, panning, whip-pan, or brief slow-motion coverage. It may not reorder source anchors, swap attacker and recipient, cross the combat axis without re-establishing it, change a grip or weapon, redirect a hit, add a new exchange, or replace the endpoint.

## 2. Freeze combat continuity

Before drafting, keep a compact internal ledger for each meaningful beat:

| Field | Record |
|---|---|
| source phase | supplied panel or necessary uncited connective beat |
| attacker / recipient | who initiates and who receives, blocks, or evades |
| start state | screen side, depth, facing, grounded/airborne state, relevant injury |
| action vector | left/right/up/down/depth direction and target |
| contact topology | limb or weapon, gripping hand, striking surface, contact point |
| result | block, miss, recoil, displacement, damage, dropped or embedded weapon |
| environment change | only persistent breakage, debris, smoke, fire, water, or terrain change |
| end state | exact state inherited by the next beat |

For two-person exchanges, preserve the combat axis and screen direction until a neutral view, visible crossing, or clear re-establishing shot permits a reversal. For multi-person combat, name the target of every attack and keep non-participants' positions readable. A weapon keeps its length, orientation, gripping hand, and damage state unless a supplied phase visibly changes them.

## 3. Build the action chain

Identify only the phases actually supported by the comic: intention or anticipation, launch, defense or evasion, contact, displacement, immediate reaction, follow-through, landing, or stable aftermath. Connect adjacent supplied phases with the smallest visible motion needed to make causality legible.

- A contact-only panel may remain a contact-centered beat.
- Adjacent load→launch→contact→recoil panels may become one continuous clip when they fit the limit.
- A needed composition change becomes an uncited view; it cannot create a new route or event.
- Every beat must change position, advantage, injury, weapon state, environmental state, or dramatic information. Merge decorative repetitions.
- End on a readable state that the next clip can inherit. Do not finish inside an unresolved tightly coupled phrase when the phrase fits in the same clip.

In auto-coverage mode, use enough ordered beats to express the action, usually four to eight rather than a list of frame-level instructions. One beat may contain several tightly coupled motions when their cause and result stay clear.

## 4. Control combat rhythm

Do not make every moment equally fast. Shape a readable contrast across the clip:

- **Hold or restrained motion:** standoff, aim, breath, weight shift, weapon settling, delayed realization.
- **Normal or medium speed:** footwork, repositioning, readable defense, recovery, pursuit.
- **Rapid acceleration:** launch, dash, evasive burst, short exchange; concentrate in-betweens around the readable start and end poses.
- **Hit-stop / impact frame:** compress decisive contact to one or two animation frames when the source supports a hard hit.
- **Brief slow motion:** reserve for a decisive near miss, weapon collision, bodily deformation at impact, reversal, or major environmental fracture; show information that normal speed would hide.
- **Return to normal speed:** reveal recoil, landing, debris fall, injury, or the new balance of power.

Use professional camera and animation terms only when they determine visible behavior: low-angle tracking, lateral tracking, pan, tilt, whip-pan, crash zoom, locked wide shot, first-person insert, time ramp, smear frame, multiples, impact frame, held key pose, dense in-betweens, or slow-motion close-up. Avoid strings of terms that do not change the image.

Prefer a legible rhythm such as restraint→burst→contact compression→reaction expansion→settle. A large attack feels stronger when surrounded by quieter phases. Use one dominant camera behavior within a continuous view; a real viewpoint change is either a precise numbered shot or an auto-coverage beat.

## 5. Integrate effects with the action

Write effects in the same beat as their cause. Do not append a detached effect inventory. For an important effect, describe the useful parts of its lifecycle:

1. **Onset:** where it originates and what triggers it;
2. **Peak:** its dominant shape, direction, scale, and shortest high-energy moment;
3. **Interaction:** what material, body, light, air, or environment it affects;
4. **Decay:** how it fragments, trails, disperses, dims, falls, or clears enough to reveal the result.

Build force from a small hierarchy rather than a pile of synonyms:

- **Primary effect:** the readable strike trail, energy mass, muzzle burst, impact flash, shockwave, or pressure cut.
- **Secondary response:** sparks, fragments, dust ring, liquid spray, cloth/hair lag, surface cracks, or displaced smoke.
- **Tertiary scale cue:** delayed distant debris, background light change, layered smoke, foreground particles, or a structure reacting after the main impact.

Match effect intensity to event importance:

| Level | Use | Typical visible treatment |
|---|---|---|
| light | feint, graze, parry, foot burst | narrow trail, few sparks or dust, little camera response |
| medium | clean block, body hit, short energy discharge | compact flash, directional fragments, brief shake, local light spill |
| heavy | decisive strike, wall break, knockback | impact frame or hit-stop, pressure ring, layered debris, clear displacement and delayed fallout |
| climax | finishing move or source-supported large destruction | staged buildup, one dominant silhouette/effect shape, foreground-to-background response, controlled white/black flash, readable aftermath |

Do not give every hit the climax treatment. Preserve escalation.

## 6. Effects quality and texture

Quality comes from coherent shape, timing, depth, light, and material response rather than adjectives such as “high quality” or “explosive.” Use only the clauses relevant to the current effect.

- **2D shape language:** hand-drawn contours, cel-shaded masses, clean opaque cores, controlled translucent fringes, tapered brush-shaped streaks, and deliberate frame-to-frame shape change. Keep silhouettes readable before and after peak speed.
- **Directional coherence:** trails, speed lines, smear frames, debris cones, shockwaves, and smoke displacement follow the action vector and contact normal. They do not radiate arbitrarily.
- **Depth and occlusion:** place effects across foreground, character, midground, and background layers with correct overlap and different movement rates. Particles pass behind or in front of bodies consistently instead of forming a flat screen overlay.
- **Local illumination:** luminous effects cast a brief, directionally consistent color spill, rim edge, reflection, or moving light band on nearby surfaces. The light peaks with the effect and decays with it; it does not permanently recolor the scene.
- **Material specificity:** metal yields hard sparks and sharp highlights; concrete yields angular chips and heavy dust; earth throws clods and granular dust; glass produces thin shards; water forms sheets, droplets, mist, and rings. Gravity, drag, collision, and inertia remain visible after emission.
- **Motion clarity:** motion blur and stretched particles follow precise motion vectors. Keep the contact point and endpoint crisp enough to read; do not smear two crossing bodies into one mass.
- **Density control:** maintain a clear primary silhouette and contact point. Let smoke, glow, particles, and debris peak at different moments and clear toward the result instead of filling the screen continuously.
- **Grand scale:** show a near response, a midground propagation, and a delayed background consequence when the source supports large force. Scale comes from staggered response and parallax, not particle count alone.
- **Clean compositing:** avoid clipped halos, dirty transparent edges, random full-frame bloom, persistent lens flare, uniform particle size, and identical repeated bursts. Keep glow concentrated around a luminous core and vary particle size, speed, and lifetime within one material family.

These principles adapt established VFX practice: emitters have origin, direction, lifetime, forces, drag, collision, light, and render layers; luminous particles appear more grounded when they illuminate nearby surfaces; precise motion vectors improve fast-effect blur. Translate those ideas into visible prompt language rather than engine settings.

## 7. Camera response and scale

Camera motion supports the action vector instead of competing with it. Use a locked or smoothly tracking view while geography is being established; reserve whip-pans, crash zooms, short shake, and extreme perspective for a motivated burst or contact. Start camera shake at the impact, make its amplitude proportional to force, and let it settle quickly. Continuous shaking weakens every hit.

For a large exchange, a useful coverage progression is establishing wide→moving medium/wide→contact close-up or insert→consequence wide→reaction or landing. This is a choice, not a quota. Auto-coverage may select another sequence when the ordered beats, screen direction, and endpoint remain clear.

## 8. Medium and layers

Use hand-drawn 2D animation, clean line art, cel-shaded characters, and layered painted or line-art backgrounds unless the user requests another medium. Avoid sensor, ISO, lens-breathing, and photographic bokeh language for ordinary 2D work.

Use only relevant layers: foreground occluders or debris, character cels, weapons/opponents, midground environment, background layout, and weather/light/effect composites. Assign different movement rates when parallax matters; do not move every layer equally.

At peak speed, reduce detailed facial demands. Keep the face readable before or after the burst and let silhouette, pose, trails, background scroll, and impact shapes carry the motion.

## 9. Failure correction

- **Floaty action:** clarify weight transfer, action vector, contact/result, and endpoint; strengthen material response without inventing another phase.
- **Weak hit:** create rhythm contrast, shorten the contact peak, add one proportional primary effect and one material response, then show displacement or recoil.
- **Effect soup:** choose one dominant effect, reduce simultaneous layers, stagger their peaks, and clear the contact point.
- **Flat effect:** add depth overlap, local illumination, material-specific particles, and a decay path.
- **Melting bodies or faces:** reduce detail at peak speed, simplify the exchange, or return to precise-shot mode.
- **Broken geography:** re-establish the axis and positions with a wide or neutral view; remove camera flourishes until the action reads.
- **Weapon or target swap:** restore ledger state and use precise-shot mode for the fragile beat.
- **Static-panel feeling:** add a source-supported phase change, visible environment response, or camera phase.
- **Uniform background motion:** differentiate layer speeds or hold one layer.
- **Photoreal drift:** remove capture terminology and restate 2D contours, cel shading, and layered effects.

## 10. Auto-coverage example

```text
**战斗段1（12秒·自动分镜）：**
分镜参考 `[load.jpg]`、`[contact.jpg]`、`[landing.jpg]`
开局状态：持刀者位于画面左侧低位，巨兽位于右侧高位，双方隔着断裂楼板对峙，刀刃斜指右上。
战斗过程：
1. 【克制慢速·大全景缓推】持刀者压低重心，刀身周围的细窄电弧从护手向刀尖聚拢，只在临近金属边缘留下短促冷光，巨兽抬起前爪封住正面路线。
2. 【急加速·低机位侧向跟拍】持刀者沿左至右方向蹬裂楼板冲出，紫色窄电轨紧贴刀路，脚后混凝土碎屑形成低矮扇形并按惯性落后于身体。
3. 【高速交锋·中近景甩镜】巨兽前爪向下截击，刀刃由下向上格开爪尖；接触点迸出短促白紫冲击闪和少量硬质火星，局部光线扫过双方轮廓，画面保持两条肢体与接触点清楚可辨。
4. 【接触瞬间·极短慢镜】刀锋切入巨兽胸前甲壳，紧凑高反差冲击帧以已锁定的白紫色相闪过，随后出现椭圆压力环；甲壳裂纹从接触点定向扩开，较大的碎片先飞出，细尘随后涌起，镜头只在命中时轻震并迅速稳定。
5. 【恢复正常速度·大全景后拉】巨兽向右后方撞穿残墙，近处碎块掠过前景，中景尘浪追随倒飞路线，远处承重结构延迟半拍坍落；持刀者停在左侧落地滑行，电轨断成细小光屑并迅速熄灭。
结束状态：巨兽倒在右后方尘雾中，胸前甲壳破裂；持刀者仍在左侧握刀，双方位置、伤势与环境破坏可由下一片段直接继承。
```
