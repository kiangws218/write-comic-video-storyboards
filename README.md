# Comic Video Storyboard Skills

将有序漫画分格转换为可执行的二维动画分镜。`main` 同时保存各版本 skill、漫画协作项目与测试资料；选择版本时，以本页和 [versions.json](versions.json) 为准。

## 版本选择

| 版本 | 状态 | Skill 目录 | 使用定位 |
| --- | --- | --- | --- |
| **2.5** | **成熟版** | [write-comic-video-storyboards-gen2-5](write-comic-video-storyboards-gen2-5/SKILL.md) | 已确认的成熟版本，保留原有创作与连续动作规则。 |
| 2.6 | 保留版本 | [write-comic-video-storyboards-gen2-6](write-comic-video-storyboards-gen2-6/SKILL.md) | 源图台账、图像事实与生成边界规则。 |
| 2.7 | 保留版本 | [write-comic-video-storyboards-gen2-7](write-comic-video-storyboards-gen2-7/SKILL.md) | 模块路由、规则整合和相应代际的验证工具。 |
| **2.8** | **成熟版** | [write-comic-video-storyboards-gen2-8](write-comic-video-storyboards-gen2-8/SKILL.md) | 成熟的 V3 来源台账、表演与覆盖流程。 |
| **2.8.1** | **测试中** | [write-comic-video-storyboards-gen2-8-1](write-comic-video-storyboards-gen2-8-1/SKILL.md) | 单主对话、缩略总览、两遍局部精读及定向复查的实验流程。 |
| **2.8.2** | **测试中** | [write-comic-video-storyboards-gen2-8-2](write-comic-video-storyboards-gen2-8-2/SKILL.md) | 原镜完整写作与角色化导演创作、关键动作路径确认、精简台账。 |

2.5 和 2.8 的成熟状态由项目维护者确认；2.8.1、2.8.2 尚在测试，不替换 2.8。2.6、2.7 均完整保留，本次整理没有改变它们的成熟度定位。

2.8.1 使用独立的 `write-comic-video-storyboards-gen2-8-1` 标识、界面名称与默认提示，和成熟 2.8 分开安装。具体输出字段、时长边界和校验要求由各版本自己的 `SKILL.md` 定义。

初代 [write-comic-video-storyboards](write-comic-video-storyboards/SKILL.md) 与 [Gen2](write-comic-video-storyboards-gen2/SKILL.md) 也保留，作为早期版本入口。

## 安装

从 `main` 选择需要的目录，完整复制到 Codex 的 skills 目录，保持目录名与 `SKILL.md` 的 `name` 相同。六个版本可以分别安装：

```text
~/.codex/skills/write-comic-video-storyboards-gen2-5/
~/.codex/skills/write-comic-video-storyboards-gen2-6/
~/.codex/skills/write-comic-video-storyboards-gen2-7/
~/.codex/skills/write-comic-video-storyboards-gen2-8/
~/.codex/skills/write-comic-video-storyboards-gen2-8-1/
~/.codex/skills/write-comic-video-storyboards-gen2-8-2/
```

调用时明确选择版本，例如 `$write-comic-video-storyboards-gen2-8` 或 `$write-comic-video-storyboards-gen2-8-1`。生产使用可选择成熟的 2.5 或 2.8；评估本次优化时调用 `$write-comic-video-storyboards-gen2-8-2`（2.8.2）；2.8.1 独立保留。实现与验证见 [2.8.2 发布说明](docs/releases/gen2.8.2/implementation-audit.md)。

## 仓库内容

```text
write-comic-video-storyboards-gen2-5/    成熟版 2.5
write-comic-video-storyboards-gen2-6/    保留版本 2.6
write-comic-video-storyboards-gen2-7/    保留版本 2.7
write-comic-video-storyboards-gen2-8/    成熟版 2.8
write-comic-video-storyboards-gen2-8-1/  测试版 2.8.1
write-comic-video-storyboards-gen2-8-2/  测试版 2.8.2
comic-workspace/                       漫画、人设、字幕、设计资产与历次交付
tests/                                 固定输入、重建脚本及历史评估
docs/                                  版本来源与仓库维护约定
versions.json                          机器可读的版本与成熟度清单
CHANGELOG.md                           仓库整理与版本入口变更
```

- 漫画协作从 [comic-workspace/README.md](comic-workspace/README.md) 和各话 `STATUS.md` 进入，正式稿优先查看 `storyboards/current/`。
- 漫画图片沿用 Git LFS；需要图片时安装 Git LFS，并在仓库中执行 `git lfs pull`。仅安装 skill 不需要下载漫画素材。
- `tests/fixtures/` 保存固定输入；`tests/results/` 保存历史结果。这些资料不随单个 skill 目录安装。
- 不同代际的规则各自维护，测试新版本时不直接覆盖成熟版本。

## 来源与维护

[版本来源与迁移记录](docs/version-sources.md) 记录各目录的固定来源提交，以及原同名实验稿的历史入口。[维护约定](docs/repository-maintenance.md) 说明分支和版本清单如何配合使用。

此前的 `codex/comic-workspace` 和 `codex/gen2.8-performance-router` 已为本次整理提供历史与内容。后续选用仓库中的 skill 时，以 `main` 的版本目录为准，不再通过旧开发分支猜测版本。
