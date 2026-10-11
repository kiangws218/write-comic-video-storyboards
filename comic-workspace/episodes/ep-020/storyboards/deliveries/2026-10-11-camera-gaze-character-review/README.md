# 第20话运镜、视线与三无角色修订

最终制作稿与本目录 `storyboard.md` 内容相同。请先读 `第20话_运镜视线角色复查报告.md` 和 `final-review-metrics.json`，逐镜细节在来源台账与修改计划。

复现本次交付：先运行 `apply_revision.py`，再运行 `audit_current.py`。前者从不可变的 `../gen2.8/` 基线应用已审阅的 `revision_choices.py`，后者校验保存稿并登记审阅。若之后手工修改当前稿，请在修改稿上继续复查，勿直接重跑基线生成脚本覆盖新成果。

源图代理复用 `../gen2.8/proxies/`；角色基调的唯一主档为 `comic-workspace/character-references/角色映射.md`。安装skill同步来源与哈希在 `skill-sync.json`，同步前文件保存于 `skill-before-sync/`。
