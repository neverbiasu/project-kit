#!/usr/bin/env python3
"""Score a skills repo against release gates G1-G9 and print a markdown report.

Usage: check_release.py <repo> [--private-terms FILE]   exit 0 only at 9/9
       check_release.py --selfcheck
Layout assumed: skills/<name>/SKILL.md, skills/<name>/evals/evals.json, demos/<name>/, USAGE.md.
"""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

MAX_FILE_KB = 1024                      # G7: larger tracked files count as binaries to remove
MIN_EVALS, MIN_USES, MIN_AGENTS = 3, 3, 2
MIN_README_LINES = 60                   # advisory only
MAX_README_CJK = 0.05                   # G9: share of CJK characters above which the README is not "in English"
INSTALL_CMD = re.compile(r"plugin install|plugin marketplace add|npx \S+|pipx? install|uv (tool|pip) install|npm i(nstall)? |brew install|cargo install")
ABS_PATH = re.compile(r"/(?:Users|home)/[^/\s]+/|[A-Z]:\\Users\\")
PRIVATE = [
    ("email", re.compile(r"(?<![\w.])(?!git@|noreply@)[\w.+-]+@(?!example\.)[\w-]+\.[a-z]{2,}")),
    ("token", re.compile(r"\b(sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b")),
    ("home path", re.compile(r"~/(workspace|\.codex/sessions|Documents|Desktop)\b")),
]
JUNK = re.compile(r"(_REPORT|_SUMMARY)\.md$|^FINAL_")  # case-sensitive: bug_report.md is an issue template, not a report
SEMVER = re.compile(r"^v?(\d+\.\d+\.\d+)$")


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def files(repo, is_git):
    if is_git:  # tracked + untracked-but-not-ignored, so a dirty tree is still scanned
        names = git(repo, "ls-files", "-co", "--exclude-standard")[1].splitlines()
        return [repo / n for n in names if (repo / n).is_file()]
    return [p for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts]


def scan(paths, repo, patterns):
    """-> ['label: file:line'] — never echoes the matched text, the report may be shared."""
    hits = []
    for p in paths:
        if p.stat().st_size > MAX_FILE_KB * 1024:
            continue
        for n, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
            for label, rx in patterns:
                if rx.search(line):
                    hits.append(f"{label}: {p.relative_to(repo)}:{n}")
    return hits


def usage_rows(repo):
    f = repo / "USAGE.md"
    rows = []
    for line in f.read_text().splitlines() if f.exists() else []:
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and len(c) >= 4 and not set(c[0]) <= set("-: ") and c[1] != "skill":
            rows.append((c[1], c[3]))
    return rows


def check(repo, private_terms=()):
    repo = Path(repo).resolve()
    top = git(repo, "rev-parse", "--show-toplevel")
    is_git = top[0] == 0 and Path(top[1]).resolve() == repo  # a folder inside someone else's repo is not a repo
    fs = files(repo, is_git)
    # ponytail: eval fixtures are deliberately bad repos, so G4/G5 skip them; a real leak placed there is missed
    clean_scope = [f for f in fs if "fixtures" not in f.relative_to(repo).parts]
    skills = sorted(p.parent for p in repo.glob("skills/*/SKILL.md"))
    G = {f"G{i}": [] for i in range(1, 10)}
    if not skills:  # an empty gate must not pass by default
        for g in ("G1", "G2", "G3", "G6"):
            G[g].append((False, "no skills/*/SKILL.md found"))
    rows = usage_rows(repo)
    suite = None  # repo-level pytest suite: None = absent, else passed?
    if any(repo.glob("tests/**/test_*.py")):
        suite = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests"],
                               cwd=repo, capture_output=True).returncode == 0
        G["G6"].append((suite, "tests/: pytest passes"))
    for s in skills:
        n = s.name
        # G1
        ev = s / "evals" / "evals.json"
        evals = json.loads(ev.read_text()).get("evals", []) if ev.exists() else []
        G["G1"].append((len(evals) >= MIN_EVALS, f"{n}: {len(evals)} evals (need {MIN_EVALS})"))
        G["G1"].append((any(e.get("boundary") for e in evals), f"{n}: boundary case"))
        bad = [str(e.get("id")) for e in evals
               if not (str((e.get("last_run") or {}).get("result", "")).startswith("pass") and (e.get("last_run") or {}).get("date"))]
        G["G1"].append((bool(evals) and not bad, f"{n}: last_run pass" + (f" — not passing: {', '.join(bad)}" if bad else "")))
        # G2
        d = repo / "demos" / n
        G["G2"].append((d.is_dir() and any(p.is_file() for p in d.rglob("*")), f"{n}: demos/{n}/"))
        # G3 — a USAGE cell like "bootstrap + sync" matches skills whose name contains a token
        mine = [a for cell, a in rows if any(t and t in n for t in re.split(r"[+,、/\s]+", cell))]
        agents = {a for a in mine if a and "待核实" not in a}
        G["G3"].append((len(mine) >= MIN_USES, f"{n}: {len(mine)} uses (need {MIN_USES})"))
        G["G3"].append((len(agents) >= MIN_AGENTS, f"{n}: {len(agents)} agents (need {MIN_AGENTS})"))
        # G6
        head = (s / "SKILL.md").read_text().split("---")
        fm = head[1] if len(head) > 2 else ""
        G["G6"].append((bool(re.search(r"^name:\s*\S", fm, re.M) and re.search(r"^description:\s*\S", fm, re.M)), f"{n}: frontmatter name + description"))
        for sc in sorted(s.glob("scripts/*.py")):
            flag = next((f for f in ("--selfcheck", "--selftest") if f in sc.read_text()), None)
            if flag:
                rc = subprocess.run([sys.executable, str(sc), flag], capture_output=True).returncode
                G["G6"].append((rc == 0, f"{n}: {sc.name} {flag}"))
            elif suite is None:
                G["G6"].append((False, f"{n}: {sc.name} has no --selfcheck / --selftest, and repo has no tests/"))
    # G4
    hits = scan(clean_scope, repo, [("abs path", ABS_PATH)])
    G["G4"].append((not hits, "no machine-specific absolute paths" + "".join(f"\n  - {h}" for h in hits[:20])))
    # G5
    G["G5"].append(((repo / "LICENSE").exists() or (repo / "LICENSE.md").exists(), "LICENSE"))
    terms = [("private term", re.compile(re.escape(t), re.I)) for t in private_terms]
    hits = scan([f for f in clean_scope if f.name != "LICENSE"], repo, PRIVATE + terms)
    G["G5"].append((not hits, f"no private content ({len(hits)} hits)" + "".join(f"\n  - {h}" for h in hits[:30])))
    # G7
    if is_git:
        dirty = git(repo, "status", "--porcelain")[1].splitlines()
        G["G7"].append((not dirty, f"git status clean ({len(dirty)} changed)"))
    else:
        G["G7"].append((False, "not a git repo — cannot verify"))
    junk = [str(f.relative_to(repo)) for f in fs if JUNK.search(f.name)]
    big = [str(f.relative_to(repo)) for f in fs if f.stat().st_size > MAX_FILE_KB * 1024]
    G["G7"].append((not junk, "no *_REPORT / *_SUMMARY / FINAL_* files" + (f": {junk}" if junk else "")))
    G["G7"].append((not big, f"no file over {MAX_FILE_KB} KB" + (f": {big}" if big else "")))
    # G8
    vers = [m.group(1) for t in (git(repo, "tag", "--list")[1].splitlines() if is_git else []) if (m := SEMVER.match(t))]
    G["G8"].append((bool(vers), "SemVer tag" + (f" ({vers[-1]})" if vers else "")))
    cl = repo / "CHANGELOG.md"
    G["G8"].append((cl.exists() and (not vers or any(v in cl.read_text() for v in vers)), "CHANGELOG.md names a tagged version"))

    # G9 — what a stranger needs to install, understand and contribute (references/top-repo-practices.md)
    readme = repo / "README.md"
    text = readme.read_text(errors="ignore") if readme.exists() else ""
    lines = len(text.splitlines())
    cjk = len(re.findall(r"[\u3400-\u9fff]", text))
    G["G9"] += [
        (any(repo.glob(".github/workflows/*.y*ml")), "CI workflow"),
        ((repo / "AGENTS.md").exists(), "AGENTS.md"),
        ((repo / "CONTRIBUTING.md").exists(), "CONTRIBUTING.md"),
        ((repo / "CODE_OF_CONDUCT.md").exists(), "CODE_OF_CONDUCT.md"),
        (any(repo.glob(".github/ISSUE_TEMPLATE/*")), "issue template"),
        ((repo / ".claude-plugin" / "plugin.json").exists(), "plugin manifest (.claude-plugin/plugin.json)"),
        (any(repo.glob("docs/*.md")), "docs/ directory"),
        (bool(text) and cjk <= MAX_README_CJK * len(text), "README.md in English"),
        (bool(INSTALL_CMD.search(text)), "README.md has an install command"),
    ]
    # advisory: never affects the score
    adv = [
        (lines >= MIN_README_LINES, f"README has {lines} lines (top repos: 100+, with an example)"),
        (any((repo / p).exists() for p in (".codex-plugin", ".opencode", "gemini-extension.json")), "install entry for a second agent"),
    ]
    nlpm = shutil.which("nlpm-check")
    if nlpm:
        adv.append((subprocess.run([nlpm, str(repo)], capture_output=True).returncode == 0, "nlpm-check passes"))
    return G, adv, bool(nlpm)


def mark(subs):
    ok = [o for o, _ in subs]
    return "✅" if all(ok) else "❌" if not any(ok) else "🟡"


NAMES = dict(G1="用例", G2="Demo", G3="使用证据", G4="可移植", G5="合规", G6="质量", G7="卫生", G8="版本", G9="公开仓库")


def report(G, adv, has_nlpm):
    passed = sum(mark(s) == "✅" for s in G.values())
    out = [f"## 发布门槛 {passed}/{len(G)}", "", "| 门槛 | 状态 | 依据 |", "|---|---|---|"]
    for g, subs in G.items():
        cell = "<br>".join(("✓ " if o else "✗ ") + m.replace("\n", "<br>") for o, m in subs)
        out.append(f"| {g} {NAMES[g]} | {mark(subs)} | {cell} |")
    out += ["", "## 建议（不计分）"] + [f"- {'✓' if o else '✗'} {m}" for o, m in adv]
    if not has_nlpm:
        out.append("- nlpm-check 未安装：SKILL.md 质量打分未跑（见 references/top-repo-practices.md）")
    return "\n".join(out), passed


def selfcheck():
    t = Path(tempfile.mkdtemp())
    try:
        s = t / "skills" / "demo-skill"
        (s / "evals").mkdir(parents=True)
        (s / "SKILL.md").write_text("---\nname: demo-skill\ndescription: does a thing\n---\n# Demo\n")
        run = {"date": "2026-01-01", "result": "pass"}
        (s / "evals" / "evals.json").write_text(json.dumps({"evals": [
            {"id": 1, "last_run": run}, {"id": 2, "last_run": run}, {"id": 3, "boundary": True, "last_run": run}]}))
        (t / "demos" / "demo-skill").mkdir(parents=True)
        (t / "demos" / "demo-skill" / "README.md").write_text("demo\n")
        (t / "USAGE.md").write_text("| 日期 | skill | 项目 | agent | 产出 |\n|---|---|---|---|---|\n"
                                    "| d | demo-skill | a | Claude Code | x |\n| d | demo-skill | b | Codex | x |\n| d | demo-skill | c | Codex | x |\n")
        (t / "LICENSE").write_text("MIT\n")
        (t / "CHANGELOG.md").write_text("## [0.1.0]\n")
        for f in ("AGENTS.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "docs/guide.md", ".claude-plugin/plugin.json",
                  ".github/workflows/ci.yml", ".github/ISSUE_TEMPLATE/bug.md"):
            (t / f).parent.mkdir(parents=True, exist_ok=True)
            (t / f).write_text("{}\n")
        (t / "README.md").write_text("# demo\n\n    claude plugin install demo@demo\n")
        g = ["git", "-C", str(t), "-c", "user.name=t", "-c", "user.email=t@local"]
        subprocess.run(["git", "-C", str(t), "init", "-q"], check=True)
        subprocess.run([*g, "add", "-A"], check=True)
        subprocess.run([*g, "commit", "-qm", "init"], check=True)
        subprocess.run([*g, "tag", "v0.1.0"], check=True)
        G, adv, n = check(t)
        text, passed = report(G, adv, n)
        assert passed == 9, text
        (t / "notes.md").write_text("see /Us" "ers/bob/secret and ask Zed-Advisor\n")
        (t / "LICENSE").unlink()
        (t / "README.md").write_text("# 演示\n这是一个只有中文说明、没有安装命令的仓库。\n")
        G, _, _ = check(t, ["zed-advisor"])
        assert mark(G["G4"]) == "❌" and mark(G["G5"]) == "❌" and mark(G["G7"]) == "🟡" and mark(G["G9"]) == "🟡", report(G, [], False)[0]
        assert "bob" not in report(G, [], False)[0] and "Zed" not in report(G, [], False)[0]  # matched text never echoed
    finally:
        shutil.rmtree(t)
    print("selfcheck ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selfcheck"]:
        selfcheck()
    elif a and not a[0].startswith("-"):
        terms = []
        if "--private-terms" in a:
            terms = [x.strip() for x in Path(a[a.index("--private-terms") + 1]).read_text().splitlines() if x.strip()]
        text, passed = report(*check(a[0], terms))
        print(text)
        sys.exit(0 if passed == 9 else 1)
    else:
        sys.exit(__doc__)
