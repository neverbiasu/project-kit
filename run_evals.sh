#!/usr/bin/env bash
# Run a skill's evals headlessly in Codex on throwaway copies of the fixtures.
# Usage: ./run_evals.sh <skill> [case-id]   -> outputs in $OUT (default: mktemp)
# ponytail: grading is by hand against evals.json expectations; automate when cases pass ~10.
set -euo pipefail
PK=$(cd "$(dirname "$0")" && pwd); SKILL=$1; ONLY=${2:-}
EV=$PK/skills/$SKILL/evals; OUT=${OUT:-$(mktemp -d)}; mkdir -p "$OUT"
python3 - "$EV/evals.json" <<'PY' | while IFS=$'\x1f' read -r id fixture setup prompt; do
import json,sys
for e in json.load(open(sys.argv[1]))["evals"]:
    print(e["id"], e["fixture"], e.get("setup",""), e["prompt"], sep="\x1f")
PY
  [ -n "$ONLY" ] && [ "$id" != "$ONLY" ] && continue
  W=$OUT/$SKILL-$id; rm -rf "$W"; cp -R "$EV/$fixture" "$W"
  if [ "$setup" = stale-handoff ]; then
    (cd "$W" && git init -q && git add -A && git -c user.name=eval -c user.email=eval@local commit -qm "chore: baseline"
     A=$(git rev-parse --short HEAD)
     printf '# Handoff\n- anchor: `%s`，git status 干净；current.md 更新于 2026-09-20\n- 目标：v0.2 导出功能\n- 唯一下一步：实现任务 2 export 命令\n' "$A" > docs/tasks/handoff.md
     sed -i '' 's#- \[product\]#- [handoff](tasks/handoff.md) · [product]#' docs/README.md
     git add -A && git -c user.name=eval -c user.email=eval@local commit -qm "docs: handoff"
     printf '\n\ndef export_json(rows):\n    raise NotImplementedError\n' >> src/ledger.py
     git add -A && git -c user.name=eval -c user.email=eval@local commit -qm "feat: start json export")
  fi
  P="$prompt（skill 文件：$PK/skills/$SKILL/SKILL.md）"
  [ "$SKILL" != release-check ] && P="${P%）}；check 脚本：$PK/skills/project-sync/scripts/check_docs.py）"
  codex exec --skip-git-repo-check -s workspace-write -C "$W" --json -o "$W.reply.md" "$P" \
    > "$W.log.jsonl" 2>&1 < /dev/null || echo "case $id: codex exit $?"
  echo "case $id -> $W"
done
echo "outputs: $OUT"
