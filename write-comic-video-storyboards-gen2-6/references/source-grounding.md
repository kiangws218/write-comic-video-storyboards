# Source grounding and version-2 ledger

This file is authoritative for what may appear in a cited shot. The ledger is an audit contract and index; it is not a substitute description from which the storyboard may be generated after the image is closed.

## Evidence order

Use visible evidence in this order:

1. the current open panel at drafting resolution;
2. an explicit character, environment, prop, or palette reference supplied for that purpose;
3. an adjacent panel only for chronology, continuous motion, or off-frame continuity;
4. story context only to decide what to inspect.

Items 3 and 4 never prove that a person, object, hand, contact, route, or background is visible in the current panel. When current-frame identity remains ambiguous, use a descriptive role label.

## Grounded micro-batch

Work with one to three contiguous panels:

1. Open them at about 720 px and keep them visible.
2. Freeze factual locks for the current panel. Escalate risky geometry or text to original resolution.
3. Fill the compact ledger entry while looking at the panel.
4. Plan coverage and write the corresponding source-locked shot before closing it.
5. Compare the finished prose with the same open panel.
6. Validate the batch, then advance.

The global contact sheet is for order, scene recognition, source-color class, and risk selection only. Never draft exact composition from it.

## Phase-specific source lock

For every cited phase freeze only facts that change generation decisions:

- vertical angle, horizontal viewing direction, and shot scale;
- screen-left/right placement, near/far depth, overlap, and occlusion;
- pose silhouette, gaze, visible limbs, and grounded/airborne state;
- hand, prop, grip, connection, action vector, and contact point;
- physical setting, graphic field, or frame-filling surface;
- whether the panel is opening, middle, contact, result, or endpoint.

Do not record decorative prose. A lock should make a contradiction obvious without attempting to replace the image.

## Shot roles and permissions

### `source_locked`

The cited panel composition must be recognizably present at its declared phase. Write it while the exact image is open. Source-supported micro-performance, cloth/hair response, medium response, and camera restraint are allowed; a different viewpoint, rearranged subject, invented hand/contact, or substituted background is not.

### `source_supported_phase`

Use only when the current or adjacent panels visibly support a missing phase of the same action. Record all evidence images. Preserve the established axis, grip, placement, topology, and endpoint. Do not auto-complete a full action chain.

### `uncited_coverage`

Use for a separately numbered reverse, reaction, insert, environment shot, or connective view that clarifies an established beat. Record its purpose and evidence basis. It may not add a new story event, identity, object, route, contact, attack, recovery, or result. Do not attach a formal panel citation unless the full composition matches.

## Per-shot background gate

Classify the visible backing internally as:

- `physical`: setting, surface, architecture, terrain, vegetation, sky, weather, depth, and light actually visible;
- `graphic`: solid color, gradient, speed field, impact field, radiating lines, or deliberate white/blank field;
- `surface`: a close object, wall, cloth, box lining, skin, or other surface filling the frame.

Write a positive, concrete description. `背景`, `森林背景`, `原格没有实景`, and `按照原格背景` are not descriptions. Preserve an abstract source background instead of restoring the known physical location. The ledger's `background_excerpt` must occur verbatim in the corresponding shot, but the open-image audit remains authoritative for correctness.

## Source-diff audit

Before closing a batch, inspect every visible noun and relation in the draft:

| Draft claim | Allowed evidence |
|---|---|
| person/object/background is visible | current panel, or declared uncited-coverage basis |
| left/right, depth, overlap, hand, grip, contact | current panel for a cited shot |
| movement phase | current/adjacent panel evidence recorded for that phase |
| character identity | explicit mapping or discriminating current-frame trait |
| emotion stronger than observable performance | at least two of dialogue, face/body performance, and adjacent context |

Delete unsupported claims. Do not retain them with negative wording or a justification.

## Version-2 source ledger

Keep this JSON internal unless requested. Include every panel used by the current batch and every timed storyboard block. Panels without dialogue use `source_bubble_count: 0`, `coverage: "none"`, and an empty `bubbles` array.

```json
{
  "version": 2,
  "panels": [
    {
      "image": "panel_009_002.jpg",
      "viewed_at_drafting": true,
      "source_bubble_count": 1,
      "bubble_audit": "pass",
      "background": {
        "type": "graphic",
        "description": "暖象牙色向淡天蓝渐变，深蓝灰放射线从握点向外扩张",
        "evidence": "current_panel"
      },
      "locks": {
        "composition": "平视手部特写，手在左下，椭圆末端在右上",
        "visible_subjects": ["一只手", "一根细绳", "一个椭圆末端"],
        "relations": ["手握一根细绳", "细绳连接椭圆末端"],
        "forbidden_inferences": ["第二只手", "珠链", "实体房间"]
      },
      "coverage": "shared",
      "coverage_reason": "单句台词与手部动作同步",
      "bubbles": [
        {
          "id": "b1",
          "speaker": "店员",
          "speaker_evidence": "气泡尾指向画外店员",
          "kind": "dialogue",
          "source_text": "那个……客人？",
          "status": "mapped",
          "script_text": "あの……お客さん？",
          "seconds": 2,
          "target": "片段13/分镜1"
        }
      ]
    }
  ],
  "shots": [
    {
      "target": "片段13/分镜1",
      "role": "source_locked",
      "source_images": ["panel_009_002.jpg"],
      "evidence": "current_panel",
      "purpose": "原格手部与台词节点",
      "background_excerpt": "暖象牙色向淡天蓝渐变",
      "viewed_while_writing": true,
      "source_audit": "pass",
      "unsupported_additions": []
    }
  ],
  "performance": []
}
```

The validator proves ledger/storyboard consistency, not visual truth. `viewed_at_drafting`, `viewed_while_writing`, `bubble_audit`, and `source_audit` are explicit workflow attestations; set them to pass only after actually performing the open-image comparison.
