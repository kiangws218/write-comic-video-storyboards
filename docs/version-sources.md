# 版本来源与迁移记录

整理日期：2026-10-15。版本成熟度以项目维护者本次确认的定位为准。

| 目录 | 状态 | 内容来源 |
| --- | --- | --- |
| `write-comic-video-storyboards-gen2-5` | 成熟 | workspace 提交 `fd9b08550afa23a6ee7e29b8f0b709b2a2246be5`，同名目录 |
| `write-comic-video-storyboards-gen2-6` | 保留 | 同上，同名目录 |
| `write-comic-video-storyboards-gen2-7` | 保留 | 同上，同名目录 |
| `write-comic-video-storyboards-gen2-8` | 成熟 | 同上，同名目录；保留工作区已使用的 Gen2.8，不混入测试流程 |
| `write-comic-video-storyboards-gen2-8-1` | 测试中 | router 提交 `cdacb60b4bff3ed5c487e10923d92050622b980f` 的 `write-comic-video-storyboards-gen2-8` 目录 |

## 为什么需要单独说明 2.8.1

历史上存在两个名称均带 2.8.1 的实现：

1. 用户确认的新测试流程位于 `codex/gen2.8-performance-router/write-comic-video-storyboards-gen2-8`，其 metadata.version 为 2.8.1，包含总览和两遍局部精读，最后更新于 2026-10-13。
2. workspace 中原有独立的 `write-comic-video-storyboards-gen2-8-1` 最后更新于 2026-10-11，内容不同。

本次 main 中的 **2.8.1 测试版采用第一项**。为满足五个版本并存的要求，仅作以下包装修改：

- SKILL.md 的 name 改为独立目录名，description 标明测试用途，metadata.status 为 experimental。
- 标题和入口说明明确其为独立测试版，保留 V3 台账兼容性。
- agents/openai.yaml 的显示名标记测试版，默认提示调用独立标识。

其余参考模块、脚本和测试文件均沿用 router 固定提交，不在整理时修改创作规则。

原同名实验稿仍可从[整理前 workspace 固定提交](https://github.com/kiangws218/write-comic-video-storyboards/tree/fd9b08550afa23a6ee7e29b8f0b709b2a2246be5/write-comic-video-storyboards-gen2-8-1)访问，历史没有删除。

## 素材与历史

`comic-workspace/`、现有素材 LFS 指针和工作区测试资料沿用 workspace 固定提交；本次只更新漫画工作区 README 的默认分支说明。性能分支的独有历史和架构说明一并保留。

本地未提交的漫画草稿和其他并行工作没有进入本次仓库整合，也未被重置。
