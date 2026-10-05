# project-kit

Project governance skills for coding agents. They keep a project legible to its owner: what the goal is, what is in progress, what is waiting for a decision, and whether a skills repo is ready to publish.

[中文说明](README.zh-CN.md)

| Skill | What it does |
|---|---|
| `project-bootstrap` | Start or adopt a project with a small harness: `AGENTS.md`, `docs/project/{mainline,kanban}.md`, `docs/tasks/current.md`, and one product + develop doc per project, all indexed. |
| `project-sync` | Keep those files true as work happens: end-of-unit sync, a brief for the owner, doc hygiene checks, and handoff between tools or agents. |
| `release-check` | Score a skills repo against nine release gates with a deterministic script, and say what is still missing. |

The skills are written for a single owner (called "Boss" in the skill text) working with one or more agents. Three markers separate what is known from what is proposed: **[已验证事实]** verified fact, **[Agent 提案]** agent proposal, **[Boss 决定]** owner decision. Trigger phrases are in both English and Chinese.

## Install

Claude Code:
```bash
claude plugin marketplace add neverbiasu/project-kit
claude plugin install project-kit@project-kit
```

Codex CLI, symlinks and other agents: see [docs/install.md](docs/install.md).

## Quick start

Ask your agent, inside a project:

```
Set up project docs for this repo.            -> project-bootstrap
Sync progress: task 2 is done, tests pass.    -> project-sync
Write a handoff, I'm switching to Codex.      -> project-sync
```
```
Is this skills repo ready to publish?         -> release-check
```

`project-bootstrap` leaves you with this, and nothing else:

```
AGENTS.md                  rules, owner checkpoints, report format
docs/README.md             the only index
docs/project/mainline.md   direction and standing constraints
docs/project/kanban.md     progress
docs/tasks/current.md      the one active work unit
docs/product/<x>.md        what it is, for whom, decisions      (< 60 lines)
docs/develop/<x>.md        structure, how to run, git           (< 60 lines)
```

## What makes it different

- **Owner checkpoints.** Agents stop at the end of a work unit, before publishing, before deleting, and when direction is unclear.
- **Facts, proposals and decisions are labelled**, so a repeated proposal never turns into a fact.
- **A cap on documents.** One index, fixed files, no `*_REPORT.md`. `check_docs.py` enforces it.
- **Evidence in the repo.** Every skill has eval cases with dated results, a demo of a real run, and a usage log.

## Scripts

```bash
python3 skills/project-sync/scripts/check_docs.py <project>      # index, length and naming checks
```
```bash
python3 skills/release-check/scripts/check_release.py <repo>     # release gates, see docs/release-gates.md
```

Both use the Python standard library only and have `--selfcheck`.

## Evidence

- Eval cases: `skills/*/evals/evals.json`. Run them with `./run_evals.sh <skill> [case-id]` (headless Codex, on throwaway copies of the fixtures; graded by hand against the listed expectations).
- Demos of real runs: [demos/](demos/). Usage log: [USAGE.md](USAGE.md).

## Docs

- [Install](docs/install.md)
- [Release gates](docs/release-gates.md)
- [Contributing](CONTRIBUTING.md) · [Code of conduct](CODE_OF_CONDUCT.md) · [Changelog](CHANGELOG.md)

## License

[MIT](LICENSE)
