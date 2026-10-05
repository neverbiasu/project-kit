---
name: release-check
description: Check whether a skills repo is ready to publish - scores release gates G1-G9 (evals, demo, usage evidence, portability, license and private content, selftests, git hygiene, version tag, public-repo infrastructure) with a deterministic script. Also use when creating a new skills repo, to scaffold what G9 requires from day one. Use before publishing or open-sourcing a skill, or when the user says "能不能发布", "发布前检查", "发布检查", "对标", "release check", "is this skill ready to ship". Does not publish, push, or fix evidence.
---

# Release Check

Tell the Boss (user) whether a skills repo can be published, with evidence. The script decides the score; you explain it.

## 1. Run the script
```
python3 <this-skill>/scripts/check_release.py <repo> [--private-terms FILE]
```
- Paste its gate table as-is. **Never change a mark by judgment**; if you think a mark is wrong, say so next to it and keep the script's mark.
- `--private-terms FILE`: one term per line (project names, people, places the Boss does not want public). Ask the Boss for it if none is given; keep the file outside the repo.
- Not a git repo → G7/G8 cannot pass. Report that; do not `git init`.

## 2. Explain each failed gate
For every 🟡/❌: which file, what is missing, the smallest fix. For private-content hits give `file:line` only — **never quote the matched text** in the report.

## 3. G9 and the unscored suggestions
**G9 is a gate**: CI, `AGENTS.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue template, plugin manifest, `docs/`, English README with an install command. A new skills repo gets these on day one — see the checklist in [references/top-repo-practices.md](references/top-repo-practices.md).
The script's「建议（不计分）」section (README length, a second agent's install entry, `nlpm-check`) is **not** part of the score: report it separately, never as a gate failure.
For each missing G9 item or suggestion, **name one repo from the reference that does it** (e.g. "plugin manifest — obra/superpowers"), so the Boss can look at a real example.
If `nlpm-check` is installed the script runs it for SKILL.md quality; if not, say it was not run. Do not download it yourself.

## 4. Rules
- **Evidence is not yours to write.** Never add USAGE rows, eval results, demo outputs or dates that did not happen, even when asked to "fill in" a gate. Say what real use is still needed.
- Do not fix findings unless the Boss asks; then fix only what was asked and re-run the script.
- No publish, push, remote, tag or `git init` without the Boss's approval in this conversation. A passing score is a reason to ask, not permission.

## 5. Report
1. Score `n/9` and one-line verdict (can / cannot publish, and why)
2. The gate table
3. Failed gates → smallest fix each
4. Unscored suggestions (separate)
5. One next step, then stop and wait for the Boss
