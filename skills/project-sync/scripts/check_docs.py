#!/usr/bin/env python3
"""Check governance docs: required files exist, every docs/*.md is indexed, relative links resolve.

Usage: check_docs.py [root]   (exit 1 on issues)
"""
import re
import sys
from pathlib import Path

REQUIRED = ["AGENTS.md", "docs/project/mainline.md", "docs/project/kanban.md", "docs/tasks/current.md", "docs/README.md"]
LINK = re.compile(r"\]\(([^)#\s]+)")


def check(root: Path) -> list[str]:
    issues = [f"missing {f}" for f in REQUIRED if not (root / f).exists()]
    index = root / "docs/README.md"
    if not index.exists():
        return issues
    linked = set()
    files = [root / f for f in REQUIRED if (root / f).exists()] + list((root / "docs").rglob("*.md"))
    for md in dict.fromkeys(files):
        for target in LINK.findall(md.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("mailto:"):
                continue
            path = (md.parent / target).resolve()
            if not path.exists():
                issues.append(f"{md.relative_to(root)}: broken link {target}")
            elif md == index:
                linked.add(path)
    for md in (root / "docs").rglob("*.md"):
        if md != index and md.resolve() not in linked:
            issues.append(f"unindexed {md.relative_to(root)}")
    return issues


def _selfcheck():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        r = Path(d)
        for d in ("docs/product", "docs/project", "docs/tasks"):
            (r / d).mkdir(parents=True)
        for f in REQUIRED[1:4]:
            (r / f).write_text("x")
        (r / "AGENTS.md").write_text("x")
        (r / "docs/product/a.md").write_text("a")
        (r / "docs/product/b.md").write_text("b")
        (r / "docs/README.md").write_text(
            "[m](project/mainline.md) [k](project/kanban.md) [c](tasks/current.md) [a](product/a.md) [gone](product/zzz.md)"
        )
        got = check(r)
        assert got == ["docs/README.md: broken link product/zzz.md", "unindexed docs/product/b.md"], got


if __name__ == "__main__":
    if sys.argv[1:] == ["--selfcheck"]:
        _selfcheck()
        print("selfcheck ok")
        sys.exit(0)
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    problems = check(root)
    print("\n".join(problems) or "docs ok")
    sys.exit(1 if problems else 0)
