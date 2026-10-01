# Comic Video Storyboard Skills

将有序漫画、漫画原图与裁切分格转换为可供 AI 视频生成使用的结构化二维动画分镜。

## Skills

- `write-comic-video-storyboards/`：初代稳定版，适合按原漫画恢复对白、拆分约 15 秒片段并编写详细分镜。
- `write-comic-video-storyboards-gen2/`：第二代版本，强化原格保留、状态／动作判定、自然对白计时、环境提示词、成人原版加平台安全替换稿、战斗镜头与 Seedance 执行审查。
- `write-comic-video-storyboards-gen2-5/`：二点五代版本，在 Gen2 严格还原原漫画的基础上，支持连续动作镜头组、必要碎切与环境空镜、镜内节奏和中割密度设计、直观怪物描述及克制的动画特效。
- `write-comic-video-storyboards-gen2-6/`：二点六代版本，要求原格锁定镜头在对应图片保持打开时写作，以版本 2 源图台账审计背景、对白拆镜、镜头权限和新增画面事实，同时保留 Gen2.5 的表演、连续动作、战斗节奏和特效质量下限。
- `write-comic-video-storyboards-gen2-7/`：二点七代版本，保持 Gen2.6 的七字段输出、人物表演、镜头与布光质量，通过核心规则合并、风险模块按需加载和验证器承接机械约束来减少运行时 Token。
- `write-comic-video-storyboards-gen2-8/`：二点八代版本，采用“逐图证据→语义轮次→覆盖分组→镜头正文”的 V3 架构；720p 为默认看图层，明确区分原格镜头与有依据的增镜，并以 15 秒硬上限、同格覆盖归属和表演卡校验防止漏拆、重复增镜及质量退化。

每个目录都是独立 Skill，包含 `SKILL.md`、相关参考规则、验证脚本与 Codex 界面配置。

## Install

将需要的整个 Skill 目录复制到 Codex Skills 目录中，保持目录名与 `SKILL.md` 中的 `name` 一致。

```text
~/.codex/skills/write-comic-video-storyboards/
~/.codex/skills/write-comic-video-storyboards-gen2/
~/.codex/skills/write-comic-video-storyboards-gen2-5/
~/.codex/skills/write-comic-video-storyboards-gen2-6/
~/.codex/skills/write-comic-video-storyboards-gen2-7/
~/.codex/skills/write-comic-video-storyboards-gen2-8/
```

也可以从此 GitHub 仓库路径安装其中一个子目录。

## Tests

- `tests/fixtures/`：版本化的固定输入与旧版基线；不放进任何 Skill 发布目录。
- `tests/results/<version>/`：对应版本的分镜、源图台账和评估报告。
- `tests/build_ch15_gen26_fixture.py`：重建第15话第一批测试结果与文件校验清单，保证 A/B 可复现。
- `tests/build_ch15_gen27_first8_cinematic.py`：重建 Gen2.7 前八图完整质量测试。
- `tests/compare_gen27_token_quality.py`：复现 Gen2.6/Gen2.7 规则、输出、时长和质量代理指标。

## Notes

- Gen2.8 将 15 秒视为硬上限；唯一例外是单一漫画格的必要覆盖经正确拆镜和自然语速估时后仍超限，此时保持同一片段并明确标记为人工处理。
- 分镜引用使用裁切图文件名；原漫画可用于恢复裁切图缺失的对白与上下文。
- Gen2 的成人内容交付采用完整原作主版，并在文末附受影响片段的平台安全替换稿。
- Gen2.5 以漫画关键格为强制锚点；新增镜头只能补充既有动作、空间、节奏或情绪，不能替换或改写原作事件。
- Gen2.6 的台账是约束和审计索引，不是原图的文本替代品；引用原格的镜头必须在图片当前可见时写作与复核。
- Gen2.7 只压缩运行时规则，不以缩短最终分镜为目标；普通、电影化、源图风险、战斗和 Seedance 模块按任务条件加载。
- Gen2.8 的语义轮次不直接等同于镜头数：相邻短轮次可在同一覆盖组中用一个可读机位承载；物品、环境、细节或动作阶段也可作为有源依据的无人物增镜。声音设计保留环境音、拟音、呼吸、静默与对白处理，不生成 BGM。
