# project-kit

轻量项目治理 skills：启动骨架 + 进度同步。与 `manager-harness`（交付管理）配合使用。

| skill | 用途 |
|---|---|
| `skills/project-bootstrap` | 建 AGENTS + `docs/project/{mainline,kanban}` + `docs/tasks/current` + `docs/{product,develop}` 索引骨架（与 manager-harness 默认路径一致） |
| `skills/project-sync` | 事件→文件同步表、单元结束同步、Boss 介入简报、文档卫生检查（`scripts/check_docs.py`） |
| `skills/release-check` | 发布前检查：`scripts/check_release.py` 给 G1–G8 打分，另列头部仓库的做法（不计分）；质量打分交给 [nlpm](https://github.com/xiaolai/nlpm) |

[English](README.md)

## 安装
```bash
claude plugin marketplace add neverbiasu/project-kit
claude plugin install project-kit@project-kit
```
软链接、Codex 及其他 agent 见 [docs/install.md](docs/install.md)。

## 测试与证据（发布门槛见 [docs/release-gates.md](docs/release-gates.md)）
- 用例：`skills/*/evals/evals.json`（每个 skill 3 条，含 1 条边界；`last_run` 记最近结果）
- 跑用例：`./run_evals.sh project-sync [case-id]`（Codex 无头运行，fixture 复制到临时目录；按 expectations 人工判定）
- 脚本自检：`python3 skills/project-sync/scripts/check_docs.py --selfcheck`、`python3 skills/release-check/scripts/check_release.py --selfcheck`
- Demo：`demos/`；真实使用记录：`USAGE.md`

## License
[MIT](LICENSE)
