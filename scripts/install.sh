#!/usr/bin/env bash
# skills/ ve vendor/ altındaki skill'leri ~/.claude/skills'e kopyalar (mevcutları günceller).
# vendor/<ad>/REVIEW.md olmayan skill KURULMAZ.
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# SKILLS_DEST ile hedef değiştirilebilir (test için)
DEST="${SKILLS_DEST:-$HOME/.claude/skills}"
mkdir -p "$DEST"
for src in "$ROOT"/skills/*/ "$ROOT"/vendor/*/; do
  [ -d "$src" ] || continue
  name=$(basename "$src")
  [ -f "$src/SKILL.md" ] || { echo "atla (SKILL.md yok): $name"; continue; }
  case "$src" in */vendor/*) [ -f "$src/REVIEW.md" ] || { echo "ATLA (REVIEW.md yok, denetimsiz): $name"; continue; };; esac
  rm -rf "$DEST/$name"; mkdir -p "$DEST/$name"
  # REVIEW.md kurulum hedefine gitmez (skill'in parçası değil)
  (cd "$src" && find . -type f ! -name REVIEW.md ! -path './evals/*' -exec cp --parents {} "$DEST/$name/" \;)
  echo "kuruldu: $name"
done
