# 仓库维护约定

## 当前入口

`main` 保存项目可选择的完整版本集合。新增或调整版本状态时，同时检查根目录 README、versions.json、对应 SKILL.md 与 agents/openai.yaml，确保目录、skill 标识、界面显示名和默认调用一致。

当前成熟版本为 2.5、2.8；2.8.1 为测试版；2.6、2.7 保留。成熟度由维护者确认，自动化检查通过不自动将测试版升级为成熟版。

## 分支与变更范围

- `main` 是正式素材、参考图、参考音频、分镜交付与 skill 版本的统一入口。“上传工作区”和“同步最新脚本”默认以远端 `main` 为准。
- 新功能、规则试验和修复使用短期 `codex/*` 分支，说明影响哪个版本，再合回 main。
- 每次任务从最新 `main` 开始；完成验证后合回 `main` 并确认远端已更新，不能仅推送到开发分支就视为正式交付。并行工作在合并前先纳入最新 `main`。
- `codex/comic-workspace` 不再作为独立的长期正式入口；`test` 可保留试验，正式采用的成果须合回 `main`。历史版本用目录、版本清单和发布标签标识，不依赖长期版本分支。
- 测试版的规则不直接覆盖成熟版；需要回移的修复应单独审查。
- 老开发分支保留历史或尚未整合工作；不要仅凭分支名、分支总体更新时间决定安装哪份 skill。
- 不在整理任务中重置其他工作区或自动纳入未提交文件。

## 验证

更新某个版本的规则或工具时，运行该目录已有的相关检查，例如：

```text
python -m unittest discover -s write-comic-video-storyboards-gen2-8/scripts -p "test_*.py"
python -m unittest discover -s write-comic-video-storyboards-gen2-8-1/scripts -p "test_*.py"
```

安装目录保持与 frontmatter.name 相同；界面 default_prompt 指向本目录的 `$skill-name`。维护版本清单时核对目录存在、版本号和状态，避免同一补丁号对应不明来源。

## 项目资料

原漫画、角色设定与正式交付保存在 comic-workspace；固定回归样例和历史评估保存在 tests。源素材保留文件名与内容，图像继续遵循现有 Git LFS 配置。

清理可再生代理图、重复快照或历史实验是独立任务：先确认引用、可重建性和独有内容，再处理。本次整合不删除这些资料。
