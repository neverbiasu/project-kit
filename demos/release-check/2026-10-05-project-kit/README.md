# Demo：release-check · 检查 project-kit 自己（2026-10-05）

- **Agent**：Claude Code（Opus），真实运行，非测试 fixture
- **输入**：project-kit 在 `v0.1.0` 之后、`release-check` 开发中的工作树；`--private-terms` 为 4 个私有词（文件在仓库外）
- **命令**：`python3 skills/release-check/scripts/check_release.py . --private-terms <file>`
- **输出**：4/8（G1–G3 🟡、G5 🟡、G7 🟡）；完整表格可用上面的命令重跑
- **看点**：G5 报出 USAGE 与两个 demo 里的 23 处私有内容，只给 `file:line`，不回显内容——与当天手动 grep 的结论一致；新 skill 自己还没 demo / 使用记录，所以 G1–G3 掉成 🟡，脚本不给自己开后门
- **后续**：10-05 已按此报告脱敏，复检 G5 ✅
- **已知**：运行时工作树未提交，G7 报 1 处改动
