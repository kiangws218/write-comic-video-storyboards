# Gen2.6 re0 对齐与第15话重测交接

## 当前状态

- 工作分支：`codex/gen2.6-re0-full-benchmark`
- 本分支是阶段性存档，不是最终验收版本。
- 规则层已经完成第一轮升级；第15话 `ch15_p01_c001` 至 `ch15_p08_c002` 的测试稿仍需人工复核和修正。
- `re0` 指用户提供的 `学园提示词整理_纯文字版.docx`，只作为输出结构、人物表演密度、镜头设计和光影布光参考，不作为漫画事实来源。

## 已完成

1. 普通分镜改为七个自足字段：`场景环境`、`环境音`、`镜头设计`、`可见动作`、`台词与语气`、`光影布光`、`声音设计`。
2. 禁止 `保持原有`、`上一格`、`上一镜`、`只放大上一格` 等跨片段指代，以及生成字段中的否定控制句。
3. 补充人物头部与面部朝向、视线先行、头肩错拍、结束朝向规则。
4. 补充四至六秒对白的可见发展要求。
5. 验证器增加七字段、自足表达和长对白表演密度检查。
6. 验证器单元测试共 24 项，当前全部通过。

## 测试稿位置

- 生成脚本：`tests/build_ch15_gen26_first8_cinematic.py`
- 分镜草稿：`tests/results/gen2.6-cinematic/ch15-first8/storyboard.md`
- 源图台账：`tests/results/gen2.6-cinematic/ch15-first8/source-ledger.json`

## 测试稿未完成项

当前严格验证结果为：14个片段、17张参考图、1个错误、17个警告。

- `片段14/分镜1` 缺少可见背景，必须先修复。
- 若干双说话人镜头需要判断是否拆成说话者与听者反应。
- `片段13` 的两个6秒对白镜头表演阶段不足。
- 多处同图连续镜头需确认确有不同景别、主体或戏剧功能。
- 仍需逐格人工核对第5至第8页的对白归属、手部接触和画面权限。
- 尚未完成与 Gen2.5、re0 的质量、时长和 Token 三方报告。

## 已确认的源图风险

- `ch15_p05_c001` 同格包含春子提问与青回答。
- `ch15_p05_c002` 是晶石物件画面，包含青的疑问和矮人的解释。
- `ch15_p05_c003` 包含矮人“你想要？”以及青的画外拒绝。
- `ch15_p06_c001` 看不到完整开包双手，不应写成可见的双手取石动作。
- `ch15_p06_c002` 主要是对白气泡，不能伪装成有构图依据的引用镜头。
- `ch15_p06_c003` 是晶石、掌心和稳定手腕的接触关系。
- `ch15_p07_c002` 是矮人面部近景，不应补造指向晶石的手势。
- `ch15_p08_c001` 是晶石与指虎说明画面，不应新增成品武器旋转或怪物剪影。
- `ch15_p08_c002` 只有青的提问，不应把矮人的上一段解释塞进同镜。

## 继续工作时的建议顺序

1. 逐图打开上述18张源图，修正生成脚本、台账和分镜稿。
2. 运行严格验证，先达到0错误，再人工处理警告。
3. 运行24项单元测试及 Python 编译检查。
4. 生成 Gen2.5 / Gen2.6 / re0 的镜头数、时长、字符和 Token 代理对比。
5. 完成人工源图审计后，才把测试稿标记为可供视频A/B验证。

严格验证命令：

```powershell
python write-comic-video-storyboards-gen2-6/scripts/validate_storyboard.py tests/results/gen2.6-cinematic/ch15-first8/storyboard.md --max-seconds 15 --image-dir tests/fixtures/ch15-part1/source --source-ledger tests/results/gen2.6-cinematic/ch15-first8/source-ledger.json --require-source-ledger
```

单元测试命令：

```powershell
Set-Location write-comic-video-storyboards-gen2-6
python -m unittest scripts/test_validate_storyboard.py
```
