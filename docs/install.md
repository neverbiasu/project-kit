# Install

## Claude Code (plugin)
```bash
claude plugin marketplace add neverbiasu/project-kit
claude plugin install project-kit@project-kit
```
Update with `claude plugin marketplace update project-kit`.

## Claude Code (symlink, for local development)
```bash
git clone https://github.com/neverbiasu/project-kit
for s in project-kit/skills/*; do ln -s "$PWD/$s" ~/.claude/skills/$(basename "$s"); done
```

## Codex CLI and other agents
Skills are plain `SKILL.md` folders. Link or copy them into the agent's skills directory:
```bash
for s in project-kit/skills/*; do ln -s "$PWD/$s" ~/.codex/skills/$(basename "$s"); done
```
Or point the agent at a file directly: "Follow `project-kit/skills/project-sync/SKILL.md` and sync progress."

## Requirements
Python 3.9+ for the two scripts (standard library only). `git` for the release check. `pytest` only if the repo you check has a `tests/` directory.

## Verify
```bash
python3 skills/project-sync/scripts/check_docs.py --selfcheck
python3 skills/release-check/scripts/check_release.py --selfcheck
```
