# Demo：release-check · 检查 ccfddl-skills（2026-10-05）

- **Agent**：Claude Code（Opus），真实仓库（已公开的项目），只检查、未改动
- **输入**：「按 release-check 检查这个仓库能不能发布」，带 4 个私有词
- **结果**：3/8。过：G4 可移植、G5 合规、G6 质量。未过：G1 无 evals、G2 无 demos、G3 无使用记录、G7 有 2 个未跟踪项、G8 无 tag 和 CHANGELOG
- **对标**：插件清单、241 行 README、第二个 agent 的安装入口都有；缺 CI
- **看点**：人工盘点曾记「14 个 superpowers 副本未署名」，脚本只找到 1 个 skill——那 14 个在被 `.gitignore` 排除的 `docs/` 里，从未进过公开仓库
- **据此修脚本**：仓库有 pytest 套件（27 个通过），但脚本只认 `--selfcheck`，首次判 G6 🟡 → 改为 `tests/` 下 pytest 通过也算，重跑 G6 ✅
- 完整输出在本目录 `output.md`，不入库
