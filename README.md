# Comic Video Storyboard Skills

将有序漫画、漫画原图与裁切分格转换为可供 AI 视频生成使用的结构化二维动画分镜。

## Skills

- `write-comic-video-storyboards/`：初代稳定版，适合按原漫画恢复对白、拆分约 15 秒片段并编写详细分镜。
- `write-comic-video-storyboards-gen2/`：第二代版本，强化原格保留、状态／动作判定、自然对白计时、环境提示词、成人原版加平台安全替换稿、战斗镜头与 Seedance 执行审查。

每个目录都是独立 Skill，包含 `SKILL.md`、相关参考规则、验证脚本与 Codex 界面配置。

## Install

将需要的整个 Skill 目录复制到 Codex Skills 目录中，保持目录名与 `SKILL.md` 中的 `name` 一致。

```text
~/.codex/skills/write-comic-video-storyboards/
~/.codex/skills/write-comic-video-storyboards-gen2/
```

也可以从此 GitHub 仓库路径安装其中一个子目录。

## Notes

- 默认将 15 秒视为软上限，不强制硬切满 15 秒。
- 分镜引用使用裁切图文件名；原漫画可用于恢复裁切图缺失的对白与上下文。
- Gen2 的成人内容交付采用完整原作主版，并在文末附受影响片段的平台安全替换稿。
