## 结论

**[已验证事实] 发布门槛：3/8，当前不能发布。** 主要阻塞是缺少可复现 eval 结果、Demo、真实使用证据、许可证，以及公开内容清理。

仓库未作任何修改；Git 工作区保持 clean。两个现有 `--selftest` 均通过，文档检查通过。

## 门槛表（脚本原样输出）

| 门槛 | 状态 | 依据 |
|---|---|---|
| G1 用例 | 🟡 | ✓ phd-atas-hll: 3 evals (need 3)<br>✗ phd-atas-hll: boundary case<br>✗ phd-atas-hll: last_run pass — not passing: 1, 2, 3<br>✓ phd-compare-offers: 3 evals (need 3)<br>✗ phd-compare-offers: boundary case<br>✗ phd-compare-offers: last_run pass — not passing: 1, 2, 3<br>✓ phd-csc-docs: 3 evals (need 3)<br>✗ phd-csc-docs: boundary case<br>✗ phd-csc-docs: last_run pass — not passing: 1, 2, 3<br>✓ phd-draft-outreach: 3 evals (need 3)<br>✗ phd-draft-outreach: boundary case<br>✗ phd-draft-outreach: last_run pass — not passing: 1, 2, 3<br>✓ phd-fill-application: 3 evals (need 3)<br>✗ phd-fill-application: boundary case<br>✗ phd-fill-application: last_run pass — not passing: 1, 2, 3<br>✓ phd-find-supervisors: 3 evals (need 3)<br>✗ phd-find-supervisors: boundary case<br>✗ phd-find-supervisors: last_run pass — not passing: 1, 2, 3 |
| G2 Demo | ❌ | ✗ phd-atas-hll: demos/phd-atas-hll/<br>✗ phd-compare-offers: demos/phd-compare-offers/<br>✗ phd-csc-docs: demos/phd-csc-docs/<br>✗ phd-draft-outreach: demos/phd-draft-outreach/<br>✗ phd-fill-application: demos/phd-fill-application/<br>✗ phd-find-supervisors: demos/phd-find-supervisors/ |
| G3 使用证据 | ❌ | ✗ phd-atas-hll: 0 uses (need 3)<br>✗ phd-atas-hll: 0 agents (need 2)<br>✗ phd-compare-offers: 0 uses (need 3)<br>✗ phd-compare-offers: 0 agents (need 2)<br>✗ phd-csc-docs: 0 uses (need 3)<br>✗ phd-csc-docs: 0 agents (need 2)<br>✗ phd-draft-outreach: 0 uses (need 3)<br>✗ phd-draft-outreach: 0 agents (need 2)<br>✗ phd-fill-application: 0 uses (need 3)<br>✗ phd-fill-application: 0 agents (need 2)<br>✗ phd-find-supervisors: 0 uses (need 3)<br>✗ phd-find-supervisors: 0 agents (need 2) |
| G4 可移植 | ✅ | ✓ no machine-specific absolute paths |
| G5 合规 | ❌ | ✗ LICENSE<br>✗ no private content (6 hits)<br>  - home path: AGENTS.md:44<br>  - home path: CLAUDE.md:44<br>  - home path: README.md:20<br>  - home path: docs/design.md:30<br>  - home path: docs/develop/overview.md:6<br>  - email: skills/phd-find-supervisors/scripts/check.py:412 |
| G6 质量 | 🟡 | ✓ phd-atas-hll: frontmatter name + description<br>✓ phd-compare-offers: frontmatter name + description<br>✓ phd-csc-docs: frontmatter name + description<br>✓ phd-draft-outreach: frontmatter name + description<br>✓ phd-fill-application: frontmatter name + description<br>✓ phd-find-supervisors: frontmatter name + description<br>✗ phd-find-supervisors: check.py has no --selfcheck<br>✗ phd-find-supervisors: export.py has no --selfcheck |
| G7 卫生 | ✅ | ✓ git status clean (0 changed)<br>✓ no *_REPORT / *_SUMMARY / FINAL_* files<br>✓ no file over 1024 KB |
| G8 版本 | ✅ | ✓ SemVer tag (1.1.0)<br>✓ CHANGELOG.md names a tagged version |

## 未通过项与最小修复

- **G1：** 六个 skill 各指定至少一个真实边界用例，并在真实执行后记录带日期的 `last_run.result=pass`。不能补写未发生的运行。
- **G2：** 为六个 skill 各提供一个脱敏、可复现的 `demos/<skill>/` 示例。
- **G3：** 新增 `USAGE.md`；每个 skill 需要至少 3 次真实使用、覆盖至少 2 个 agent。当前 mainline 中“真实跑通”不能直接替代 release-check 要求的结构化证据。
- **G5：** 先选择许可证，再审查上述六个位置。私密命中仅报告 `file:line`，未复述内容。此次未提供 Boss 自定义私密词表，因此还不能证明不存在项目名、人名或地点泄漏。
- **G6：** release-check 只识别 `--selfcheck`，而现有脚本提供 `--selftest`。实际运行结果是两项 `selftest ok`；若要通过该门槛，需兼容 `--selfcheck` 或由 Boss 决定调整检查规范，但本次必须保留脚本原判分。

## 对标头部仓库的差距（不计入 3/8）

| 缺口 | 可参考仓库 |
|---|---|
| Plugin manifest、一条命令安装 | `obra/superpowers` |
| 第二种 Agent 的安装入口 | `addyosmani/agent-skills` |
| README 达到 100–350 行并含完整 worked example | `i-have-adhd` |
| CI 自动跑安装与自检 | `xiaolai/nlpm` |
| 仓内保留可执行 eval/test 及结果 | `obra/superpowers` |
| 独立 SKILL 质量检查 | `xiaolai/nlpm`；本机未安装 `nlpm-check`，本次未运行 |

版本记录与每个 SKILL 的触发描述已经具备，不属于当前差距。

**唯一下一步：** **[Agent 提案]** 先由 Boss 决定是否进入“公开发布准备”，并选择许可证；获批后再围绕 G1–G6 建立真实证据，暂不发布。