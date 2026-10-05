# Demo：project-bootstrap · 接手 research-slides（2026-09-26）

- **Agent**：Claude Code（Opus），在真实项目的副本上运行；原仓未改动
- **输入**：`research-slides` 仓库 当日状态——README（7 行）、CHANGELOG（0.1.1）、1 个 skill、本地 git 2 次提交、无 remote、无项目文档
- **做了什么**：按 SKILL.md §1 取证（`git log`、`git remote -v`、CHANGELOG、SKILL.md）→ §2 套模板 → §5 `check_docs.py`
- **输出**：7 个文档 + `CLAUDE.md` 软链，共 99 行；`check_docs.py` → `docs ok`（生成的文件未入库，结构见下）
- **看点**：事实都带出处（CHANGELOG 版本、提交日期）；定位标 **[Agent 提案]** 而非决定；把发布门槛缺项放进「等待 Boss」；没有 `git init` / 提交
- **附带发现**：总仓 kanban 写的最近提交是 09-24，实际是 09-25（0.1.1）

```
AGENTS.md  (CLAUDE.md -> AGENTS.md)
docs/README.md
docs/project/mainline.md   docs/project/kanban.md
docs/tasks/current.md
docs/product/overview.md   docs/develop/overview.md
```
