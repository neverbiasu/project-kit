---
name: project-sync
description: Keep docs/project/mainline.md, docs/project/kanban.md, docs/tasks/current.md and the docs index truthful as work happens - end-of-unit sync, Boss check-in briefs, and doc hygiene audits. Use after finishing a work unit, when status/direction changes, before handing off to the Boss, when resuming a project, or when the user says "同步进度", "更新 KANBAN", "整理文档", "让我了解项目". Also hands work between tools/agents (Claude Code/Codex/Antigravity/OpenCode) or before context runs out: "交接", "handoff", "接手", "继续上次的工作".
---

# Project Sync

Assumes the `project-bootstrap` layout. If the project's AGENTS.md names other paths, use those.

## What changed → which file
| Event | Update | Never |
|---|---|---|
| Unit started / progressed / done | `current.md` 状态 + kanban 进行中/总览 row | inflate % without evidence |
| Boss approved a new unit | `current.md` 单元 + 验收标准 | start work not in current.md |
| Boss accepted direction/constraint/positioning | mainline 约束/定位 + 轨迹 row, marked **[Boss 决定]** | record proposals as decisions |
| Product state or decision changed | `docs/product/<x>.md` | copy sub-project details |
| Structure / run / install / git changed | `docs/develop/<x>.md` | — |
| Boss accepted a user-visible change | `CHANGELOG.md` [Unreleased]; on release move to `[X.Y.Z] - date` + tag | log unaccepted work or process noise |
| Doc added / moved / deleted | `docs/README.md` | leave unindexed docs |
| Question only the Boss can answer | kanban 等待 Boss | silently pick |

Labels: **[已验证事实]** needs a file/command as evidence · **[Agent 提案]** · **[Boss 决定]**. Silence is not approval.
Progress bars are evidence estimates (`██████░░░░ 60%`); no evidence → `—`.

## End-of-unit sync (same unit as the work)
Sync records work; it never does work. Asked to mark something done or raise progress without evidence → list what remains and ask for evidence; do not implement the missing tasks to make the status true.
1. Update files per table; bump `更新于 YYYY-MM-DD` (absolute dates).
2. `python3 scripts/check_docs.py <root>`; fix all issues.
3. Sub-project has its own KANBAN → update it there; hub row stays a one-line summary.
4. Commit with Conventional Commits, one concern per commit, only per project git policy / Boss approval; never stage secrets.

## Boss check-in
Pause when: unit ends; project created/dropped/repositioned; publish/push/remote/`git init`; deletion or large restructure; conclusion conflicts with mainline; two consecutive uncertain direction calls.

Brief (≤ 2 min read, user's language), after updating the product doc:
1. 现在能做什么（链接） 2. 怎么验证 3. 还缺什么 4. 唯一下一步（带推荐，等批准）

## Hygiene audit (on resume or when asked)
- `check_docs.py` clean; kanban dates not older than each sub-project's `git log -1 --format=%cs`.
- `current.md` matches what is actually in progress.
- Flag report-style clutter, duplicated docs, stale 等待 Boss items. Propose deletions; delete only with approval.

## Handoff (switching tool/agent; same tool → use its resume instead)
Handoff = pointers + delta, never a copy of mainline/kanban/current. One file `docs/tasks/handoff.md`, overwritten each time (git keeps history).

**Write** (outgoing agent, only when asked):
1. Run End-of-unit sync first; anything that fits current/kanban/mainline goes there, not in the handoff.
2. Anchor: `git rev-parse --short HEAD` + `git status --short` (list uncommitted files, don't commit for the Boss); non-git → `无 git`. Note `current.md` 更新于 date.
3. Fill `templates/handoff.md` ≤ 40 lines: 目标+任务语义 · 必读路径 · 增量（labelled, with evidence path/command）· 已放弃 · 禁止/介入点 · 唯一下一步 · 返回格式. Index it in `docs/README.md` on first write.
4. Self-check: no `<...>` placeholders, no secrets/personal data (paths only), `check_docs.py` clean.
5. Tell the Boss the path and the starter line: `读 docs/tasks/handoff.md，按 project-sync 的 Handoff Resume 接手`.

**Resume** (incoming agent — verify, don't trust):
1. Read AGENTS.md → handoff.md → its 必读 list.
2. Verify: HEAD/worktree vs anchor (differs → `git log <anchor>..HEAD --oneline -- . ':!docs/tasks/handoff.md'`; any output → mark **陈旧**; ignore handoff.md itself in `git status`); 必读 paths exist; `check_docs.py` clean (project not on bootstrap layout, e.g. no `docs/README.md` → skip and note 不适用, not 冲突); `current.md` date newer than handoff → current wins; re-run 1–3 key **[已验证事实]** commands, else downgrade to 待核实.
3. Output a checkpoint table before any edit: 目标 / 已完成 / 未完成 / 下一步 / 核验（已核实·冲突·无法核实）.
4. Stale or conflict → repo docs win; list differences and pause for the Boss. Otherwise start 下一步 without widening task semantics.
