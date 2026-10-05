# project-kit

Lightweight project governance skills: a starter harness and progress sync. Pairs with `manager-harness` (delivery management).

| Skill | What it does |
|---|---|
| `skills/project-bootstrap` | Creates AGENTS + `docs/project/{mainline,kanban}` + `docs/tasks/current` + an indexed `docs/{product,develop}` skeleton (same default paths as manager-harness) |
| `skills/project-sync` | Event-to-file sync table, end-of-unit sync, owner briefing, doc hygiene checks (`scripts/check_docs.py`) |

Install: `ln -s $PWD/skills/<name> ~/.claude/skills/<name>`

## Tests and evidence
- Eval cases: `skills/*/evals/evals.json` (3 per skill, 1 boundary case; `last_run` holds the latest result)
- Run them: `./run_evals.sh project-sync [case-id]` (headless Codex on throwaway copies of the fixtures; graded by hand against the expectations)
- Script self-check: `python3 skills/project-sync/scripts/check_docs.py --selfcheck`
- Demos: `demos/`; real usage log: `USAGE.md`

## License
[MIT](LICENSE)
