# Demo：project-sync · 一个文献阅读项目的进度同步（2026-09-25）

- **Agent**：Claude Code（Opus），真实会话，非测试 fixture
- **输入**：Boss 说「更新一下 KANBAN，告诉我现在进度」；kanban / current 停在 2026-09-24，而 git 里已有 5 次之后的 demo 提交
- **做了什么**：按 project-sync「What changed → which file」表，从 `git log` 与 `research-log.md` 取证据，更新 `current.md` 任务状态、kanban 总览 / 进行中 / 等待 Boss；跑 `check_docs.py` → `docs ok`；本地提交
- **输出**：kanban 与 current 各一处更新，摘录见下（源仓提交 `1daff94` → `028f83e`）
- **看点**：进度 90% 附「验收 4/5」依据；过期的「等 Boss 选实验」被移出；未核实的 Zotero 项标「未核实是否已做」而不是删掉
- **已脱敏（2026-10-05）**：项目名、人名、模型与论文名、外部链接换成代号；任务结构、状态变化和日期未改

| 位置 | 同步前 | 同步后 |
|---|---|---|
| kanban 进行中 | `████████░░ □ 1–9 完成`，阻塞「等 Boss 选」 | `█████████░ 90%（验收 4/5）`，下一步 □ 13，无阻塞 |
| kanban 等待 Boss | 「选实验：方案对比 / 模型 G / 模型 K」 | 该项移出；Zotero 项加注「未核实是否已做」 |
| current 任务 11–12 | 🟡 2 个模型，其余未跑 | ✅ 6 个模型，列出 3 个未跑及原因 |
| current 验收标准 | 2/5 勾选 | 4/5 勾选 |
