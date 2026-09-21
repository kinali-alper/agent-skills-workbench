#!/usr/bin/env bash
# Tüm vendor skill'lerini denetler, vendor/.audit-status yazar, MANIFEST.md'yi üretir.
set -eu
PY=$(command -v python3 || command -v python)
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
: > "$ROOT/vendor/.audit-status"
for d in "$ROOT"/vendor/*/; do
  n=$(basename "$d"); bash "$ROOT/scripts/skill-audit.sh" "$d" >/dev/null 2>&1 && rc=0 || rc=$?
  echo "$n $rc" >> "$ROOT/vendor/.audit-status"
done
PYTHONIOENCODING=utf-8 "$PY" "$ROOT/scripts/gen-manifest.py"
bash "$ROOT/scripts/gen-integrity.sh"
