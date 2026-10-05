# What top skill repos ship

Checked 2026-10-05 from installed copies and the GitHub API. Re-check before quoting numbers.
The first seven rows are gate **G9** [owner decision 2026-10-05]; a second agent's install entry and README length stay suggestions.

## Day-one checklist for a new skills repo (G9)
Create these with the first skill, not before release:
- `.github/workflows/<name>.yml` running every script's `--selfcheck` (and `check_release.py .`)
- `AGENTS.md` (layout, who decides, checks before commit, never-do list) with `CLAUDE.md` symlinked to it
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/ISSUE_TEMPLATE/` (bug report + feature request)
- `.claude-plugin/plugin.json` and `marketplace.json`; validate with `claude plugin validate .`
- `README.md` in English: what it does, the install command, a quick start; a translated README may sit beside it
- `docs/` with at least an install page

## What the top repos do

| Practice | Who does it | Why it matters |
|---|---|---|
| Plugin manifest, one-command install (`.claude-plugin/plugin.json`, often `marketplace.json`) | obra/superpowers, addyosmani/agent-skills, mattpocock/skills, xiaolai/nlpm | A manual symlink is a step most visitors will not take |
| Install entry for more than one agent (`.codex-plugin/`, `.opencode/`, `gemini-extension.json`, `.cursor-plugin/`) | superpowers (9), agent-skills (4), nlpm (3) | Skills are portable; the packaging usually is not |
| README of 100–350 lines: what it does, install, quick start, one worked example | superpowers (400), agent-skills (409), mattpocock/skills (234) | The README is the only thing a visitor reads |
| Release notes per version (`CHANGELOG.md` / `RELEASE-NOTES.md`, changesets) | superpowers, mattpocock/skills | Users can see what changed before updating |
| In-repo `AGENTS.md` | superpowers, agent-skills, mattpocock/skills, nlpm | Agents working on the repo read it first |
| `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue templates | superpowers (code of conduct, 5 issue templates, PR template), agent-skills (`CONTRIBUTING.md`, issue template) | Tells a stranger how to report and how to help |
| `docs/` directory | superpowers, agent-skills, mattpocock/skills | Keeps the README short |
| CI that tests installation or runs a self-check | addyosmani/agent-skills (`test-plugin-install.yml`), nlpm (`nlpm-self-check.yml`, `pre-release-quality-gate.yml`), mattpocock/skills (`release.yml`) | Catches a skill missing from the manifest before users do |
| Tests or evals kept in the repo | superpowers (`tests/`), addyosmani/agent-skills (`evals/cases/`), i-have-adhd (`evals/` + runner), nlpm (`.nlpm-test/*.spec.md`) | Shows the skill was run, not just written |
| `description` on every SKILL.md that says when to use it | all of the above | It is what the agent matches on |

## From xiaolai/nlpm specifically
- **Deterministic scoring**: fixed penalty per issue, same input → same score. `check_release.py` follows this: marks come from the script, not from the agent.
- **Standalone validator** (`bin/nlpm-check`, one Python file) usable in pre-commit and CI without an agent. Use it for SKILL.md quality; this skill does not re-implement its 50 rules.
- **Manifest-vs-disk check**: a SKILL.md on disk but absent from `plugin.json` is invisible after install. Run `nlpm-check` once a manifest exists.
- **Every rule has a real-world good example.** When suggesting a practice, name a repo that does it.

Install `nlpm-check` (the Boss runs this; see the nlpm README for the current command): https://github.com/xiaolai/nlpm
