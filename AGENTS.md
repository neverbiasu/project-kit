# AGENTS.md — project-kit

Project governance skills for coding agents. Three skills, two scripts, no application code.
In scope: project harness docs, progress sync, handoff, release gate checks.
Out of scope: delivery orchestration, natural-language quality scoring (use [nlpm](https://github.com/xiaolai/nlpm)), publishing.

## Layout
- `skills/<name>/SKILL.md` — the skill; keep each under 80 lines, move detail to `references/` or `templates/`
- `skills/<name>/evals/evals.json` — 3+ cases per skill, 1+ boundary case, each with a dated `last_run`
- `skills/<name>/scripts/*.py` — stdlib only, each with `--selfcheck`
- `demos/<skill>/<date>-<project>/README.md` — one summary per real run; raw outputs stay local
- `USAGE.md` — one row per real use; `docs/` — user documentation

## Who decides
"Boss" in the skills means the human who owns the project. The Boss decides scope, publishing, deletion and data policy; agents propose.
Label consequential statements **[已验证事实]** (verified fact), **[Agent 提案]** (agent proposal) or **[Boss 决定]** (owner decision).

## Before you commit
```
python3 skills/project-sync/scripts/check_docs.py --selfcheck
python3 skills/release-check/scripts/check_release.py --selfcheck
python3 skills/release-check/scripts/check_release.py .
```
- Changed a `SKILL.md`? Re-run that skill's evals (`./run_evals.sh <skill>`) and record the result in `evals.json`.
- Conventional Commits; one change per commit. SemVer tags; `CHANGELOG.md` records only changes the owner accepted.

## Never
- Invent eval results, usage rows, demo outputs or dates.
- Commit private content: personal project names, people, home-directory paths, credentials.
- Push, publish, tag, change remotes or rewrite history without the owner's approval in the conversation.
