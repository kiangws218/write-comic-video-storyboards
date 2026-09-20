# 第15话第一批测试夹具

这是一套用于比较 Gen2.5 与 Gen2.6 的固定输入，不是技能运行目录。

- 来源：远端 `test` 分支，提交 `37df5f2` 中的 `15话第一批.zip`
- `source/`：36 张原始 JPG，仅把 ZIP 内乱码文件名规范为 `ch15_p页码_c格号.jpg`，像素内容不变
- `manifest.json`：规范文件名、字节数与 SHA-256，便于确认后续测试使用同一输入
- `baseline/gen2.5-storyboard.md`：ZIP 内随附的 Gen2.5 结果，作为只读基线
- Gen2.6 结果：`tests/results/gen2.6/ch15-part1/`

测试夹具与正式技能代码分开，避免把临时压缩包、基线结果和发布目录混在一起。原远端 `test` 分支保留，未删除或改写。

