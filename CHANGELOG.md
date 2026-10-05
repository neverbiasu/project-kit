# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/); versions follow [SemVer](https://semver.org/). Only changes the owner has accepted are listed.

## [0.2.0] - 2026-10-05
### Added
- `release-check` skill: `scripts/check_release.py` scores a skills repo against release gates G1–G9 and prints unscored suggestions; `references/top-repo-practices.md` lists what top skill repos ship and a day-one checklist.
- Public-repo scaffold: CI workflow, `AGENTS.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue templates, plugin manifest for one-command install, `docs/`.
- English `README.md` with install commands; the Chinese README moved to `README.zh-CN.md`.
- `project-bootstrap`: for a skills or library repo, create the public-repo scaffold on day one (eval case 4).

### Changed
- Demos keep one summary per run; raw outputs are ignored by git.

### Fixed
- `run_evals.sh` no longer passes the docs-check hint to `release-check` cases.

## [0.1.0] - 2026-10-05
### Added
- `project-bootstrap`: create or adopt a project harness (AGENTS, mainline, kanban, current, product, develop, index) with templates.
- `project-sync`: progress sync, owner briefing, doc hygiene checks (`scripts/check_docs.py`), handoff between tools.
- A "floor deadline" column in the kanban in-progress table.
- Three eval cases per skill (one boundary case) and `run_evals.sh` (headless Codex); 6/6 passing on 2026-10-05.
- `demos/`, `USAGE.md`, MIT `LICENSE`.

### Fixed
- `project-sync` records progress only; it no longer finishes remaining tasks to reach 100%.
- `project-bootstrap` treats instructions found in files as unverified, never as an owner decision.
- `run_evals.sh` creates `OUT` when it is given.
