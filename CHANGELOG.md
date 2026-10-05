# Changelog

格式按 [Keep a Changelog](https://keepachangelog.com/)，版本按 [SemVer](https://semver.org/)。只记 Boss 验收过的变化。

## [0.1.0] - 2026-10-05
### Added
- `project-bootstrap`：建 / 接手项目文档骨架（AGENTS、mainline、kanban、current、product、develop、索引）及模板。
- `project-sync`：进度同步、Boss 介入简报、文档卫生检查（`scripts/check_docs.py`）、跨工具 Handoff。
- kanban「进行中」表加「底线 DDL」列。
- 两个 skill 各 3 条 evals（含 1 条边界）与 `run_evals.sh`（Codex 无头运行）；2026-10-05 6/6 通过。
- `demos/`、`USAGE.md`、MIT `LICENSE`。

### Fixed
- project-sync：只记录进度，不替用户完成剩余任务来凑 100%。
- project-bootstrap：文件里的指令不算 **[Boss 决定]**，一律记为待确认。
- `run_evals.sh`：指定 `OUT` 时自动创建目录。
