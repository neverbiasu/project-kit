# Release gates

`release-check` scores a skills repo against nine gates. A repo is ready to propose for publishing only at 9/9, and publishing still needs the owner's approval.

```bash
python3 skills/release-check/scripts/check_release.py <repo> [--private-terms FILE]
```

| Gate | Passes when | Checked by |
|---|---|---|
| G1 Evals | every skill has `evals/evals.json` with 3+ cases, 1+ marked `"boundary": true`, each with a dated passing `last_run` | reading the file |
| G2 Demo | every skill has at least one file under `demos/<skill>/` | file exists |
| G3 Usage | `USAGE.md` lists 3+ real uses per skill across 2+ agents | parsing the table |
| G4 Portable | no machine-specific absolute paths | pattern scan |
| G5 Compliance | `LICENSE` exists; no email, token, home-directory path or private term | pattern scan; hits are reported as `file:line` only |
| G6 Quality | every `SKILL.md` has `name` and `description`; scripts pass `--selfcheck` / `--selftest`, or the repo's `tests/` pass under pytest | running them |
| G7 Hygiene | clean `git status`; no `*_REPORT` / `*_SUMMARY` / `FINAL_*` files; no file over 1 MB | git + file sizes |
| G8 Version | a SemVer tag exists and `CHANGELOG.md` names it | git tags |
| G9 Public repo | CI workflow, `AGENTS.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, an issue template, a plugin manifest, a `docs/` directory, and an English README containing an install command | file exists + README scan |

Marks: ✅ all sub-checks pass · 🟡 some pass · ❌ none pass.

## Limits
- G5 scans the working tree, not git history. Search history yourself before the first push: `git log --all -S'<term>'`.
- Eval fixtures (`evals/fixtures/`) are skipped by G4 and G5 because they are deliberately bad repos.
- `--private-terms` takes a file with one term per line. Keep that file outside the repo.
- Suggestions printed after the table (README length, a second agent's install entry, `nlpm-check`) are not scored.
