# Contributing

Thanks for helping. This repo is small on purpose; changes that keep it small are the easiest to accept.

## Before you open a pull request
1. Open an issue first for anything larger than a typo or a bug fix.
2. Run the checks in [AGENTS.md](AGENTS.md#before-you-commit). CI runs the same ones.
3. If you changed a `SKILL.md`, re-run its evals and update `last_run` in `evals.json` with the real result, date and agent.
4. Use [Conventional Commits](https://www.conventionalcommits.org/) and keep one change per commit.

## What gets accepted
- A fix for a rule an agent actually broke, with the eval case that shows it.
- A check in `check_release.py` or `check_docs.py` that is deterministic and has a self-check.
- Documentation that makes installation or first use shorter.

## What does not
- New roles, frameworks or process layers. See "Anti-over-documentation rules" in `skills/project-bootstrap/SKILL.md`.
- Skills copied from other repositories. Link to them instead.
- Evidence that did not happen: usage rows, eval results or demos written to pass a gate.

## Adding a skill
A new skill needs, in the same pull request: `SKILL.md` with `name` and a `description` that says when to use it, three eval cases (one boundary case), and a note in the README table. See [docs/release-gates.md](docs/release-gates.md).
