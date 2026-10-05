# 漫画协作工作区

这里集中存放团队可复用的人设参考、漫画单格和已交付分镜。第1—18话均已建立统一目录。

## 目录约定

```text
character-references/
  turnarounds/                 角色三视图与补充设定图
episodes/
  ep-001/ ... ep-018/
    source/
      monochrome-panels/       去重后的单色单格漫画
      panels/                  已上传的上色单格（仅部分话数存在）
    storyboards/
      current/                 当前建议直接使用的最新制作稿
      deliveries/              历次正式交付及其审计资料
      experiments/             局部测试、重构和评估稿
      archive/                 已被新版本替代的旧稿
    STATUS.md                  本话素材、分镜覆盖与缺口
```

## 使用方式

1. 安装 Git LFS。
2. 克隆仓库或切换到 `codex/comic-workspace` 分支。
3. 执行 `git lfs pull` 下载漫画图片。
4. 优先查看对应话数的 `STATUS.md`，再从 `storyboards/current/` 领取当前稿。

## 素材约束

- 只上传已切分的漫画单格，不上传原始整页。
- 单色版与上色版分目录保存，互不覆盖。
- 单色单格按文件内容去除完全重复项；不对图像做压缩、重绘或改名。
- `current/` 只保留当前制作所需稿件；非当前资料按交付、试验和归档分类。
- 人设参考图统一放在 `character-references/`，不与具体话数漫画混放。
- 所有 `source/` 内容均为源素材，不在原文件上覆盖修改。
- 审核图、总览图、临时缩略图和视频输出不进入漫画源素材目录。
