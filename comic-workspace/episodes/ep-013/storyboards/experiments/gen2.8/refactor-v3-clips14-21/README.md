# 第13话片段14—21：Gen2.8 V3 重构测试

- `storyboard.md`：逐张查看720p漫画格后完全重做的19镜测试稿。
- `source-ledger-v3.json`：V3源图、对白轮次、覆盖分组、镜头权限和表演估时台账。
- `comparison.md`：与重构前片段14—21的质量、结构和规则输入量对比。

验证命令（在漫画工作区仓库根目录执行）：

```powershell
python ..\write-comic-video-storyboards-gen27\write-comic-video-storyboards-gen2-8\scripts\validate_storyboard.py `
  comic-workspace\episodes\ep-013\storyboards\gen2.8\refactor-v3-clips14-21\storyboard.md `
  --image-dir C:\Users\86135\AppData\Local\Temp\comic-storyboard-720p\948454b2d1892b95 `
  --source-ledger comic-workspace\episodes\ep-013\storyboards\gen2.8\refactor-v3-clips14-21\source-ledger-v3.json `
  --require-source-ledger
```

当前结果：0错误、9条已人工复核的审阅警告。详见 `comparison.md`。
