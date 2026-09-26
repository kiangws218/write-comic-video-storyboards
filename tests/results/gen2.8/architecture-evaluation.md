# Gen2.8 architecture evaluation

Gen2.8 changes the ordinary authoring path from “draft every shot, then use warnings to discover weak acting” to an image-first selective compiler:

1. keep the current panel open;
2. assign only relevant `D`/`P`/`G` risks;
3. make a compact performance card only for `P` shots;
4. immediately render the six-field shot from the open image and card;
5. block delivery on structural or `P`-performance failures, while leaving genuine coverage advisories for image-based review.

The card is not an OCR summary and cannot replace the panel. Episode-wide card generation is forbidden. Low-risk environment, object, and neutral shots receive no card.

## Rule-load comparison

Default cinematic route: `SKILL.md` + `core-authoring.md` + `dialogue-performance.md` + `cinematic-rendering.md`.

| Version | Characters | Token proxy |
|---|---:|---:|
| Gen2.7 | 23,843 | 7,070 |
| Gen2.8 | 20,735 | 6,288 |
| Change | -13.0% | -11.1% |

Token proxy uses the repository's CJK/ASCII comparison method and is not an API bill. Gen2.8 deliberately keeps a modest rule reduction rather than repeating the Gen2.7 failure of compressing away actionable performance detail. Its variable overhead is limited to compact cards on `P` shots and is expected to replace, rather than add to, broad post-generation rewrites.

## Deterministic checks

- 42 validator tests pass.
- Chinese semantic trigger paraphrases such as `“闭嘴”出口时` and `提出抢攻时` fail.
- Explicit `P` risk without a compact card fails.
- A valid `P` card requires opening, at least two beats, coupling, and landing.
- `P` prose must contain ordering, supported face transition when readable, coupled/delayed response, endpoint, and camera landing when moving.

The architecture still requires forward testing on raw images. Structural validation alone cannot prove source fidelity or video-model motion quality.
