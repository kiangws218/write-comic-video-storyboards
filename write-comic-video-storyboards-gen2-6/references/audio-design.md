# Audio design layer

Keep audio in the same shot block as the visual prompt. Use a separate `环境音：` line for the continuous location bed, distance, occlusion, and stereo perspective; use `声音设计：` for action Foley, breath/body sound, silence, dialogue treatment, and synchronization. Audio can reinforce timing, space, weight, and acting; it cannot add a visual event or change source facts. If the target tool accepts video-only prompts, retain these layers as production notes and omit them from the visual text.

## Audio fields

- **环境音：** location bed and perspective: wind, room tone, classroom/crowd murmur, traffic, rain, insects, machinery, or a purposeful drop into near-silence. Keep it consistent with the setting and shot scale.
- **动作拟音：** only sounds caused by visible actions or supported materials: footsteps, cloth, hair/accessory movement, bag strap, door hinge, chair, tray/crockery, paper, metal, glass, water, dust, or impact. Give the sound a clear onset and decay.
- **呼吸与身体声：** audible inhale/exhale, swallow, small breath catch, or voice tremor when supported by the acting; do not invent words, interjections, or unseen exertion.
- **台词音色：** speaker, distance, volume, pace, pitch, articulation, emotional restraint/pressure, and whether the line is on-screen or off-screen. Preserve the exact dialogue text and line order from the dialogue ledger.
- **声像与空间：** left/right/front/back placement, distance, occlusion, room reverb, and a controlled perspective change when the camera or subject visibly moves. Do not let sound placement contradict screen geography.
- **音画同步：** bind important sounds to visible timing: inhale before a line, footfall at contact, cloth/prop sound when grip pressure changes, door/metal/glass at the visible action, and impact at the supported contact frame. Mention `句首/说到「原文短语」时/句末/接触瞬间/动作结束` rather than fragile sub-second numbers unless exact timing is required.

## Compact format

```text
画面：……
环境音：林间风和远处叶声从画面右后方持续传来。
声音设计：袖口与道具轻响；句前短吸气；在「原文短语」句末与可见动作同步。
```

Use one or two salient layers per beat instead of an exhaustive sound inventory. Silence, a lowered ambience, or a delayed off-screen sound may be the primary audio choice when it clarifies attention or emotion. Do not put music, Foley, or ambience into visual clauses where the video model could interpret them as objects, light, or particles.

## Audio audit

Verify that every emphasized sound has a visible/supportable cause or a clearly established environment; dialogue coverage and exact text remain unchanged; sounds start, travel, and decay plausibly; reverb and perspective match the space; and audio intensification does not imply an unsupported impact, injury, prop, or off-screen event.
