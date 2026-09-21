#!/usr/bin/env bash
# skills/ ve vendor/ altındaki skill'leri Claude Code skill klasörüne kurar.
#   bash scripts/install.sh                       # hepsi (REVIEW.md olmayan vendor kurulmaz)
#   bash scripts/install.sh --only ux-a11y-review # yalnız seçilenler (tekrarlanabilir)
#   bash scripts/install.sh --dry-run             # ne yapılacağını göster, dokunma
#   bash scripts/install.sh --force               # mevcut klasörü yedeksiz ez
# Hedef: $SKILLS_DEST ya da ~/.claude/skills. Mevcut aynı adlı klasör <ad>.bak-YYYYMMDD-HHMMSS olarak saklanır.
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${SKILLS_DEST:-$HOME/.claude/skills}"
ONLY=(); DRY=0; FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --only) shift; ONLY+=("$1");;
    --dry-run) DRY=1;;
    --force) FORCE=1;;
    -h|--help) sed -n '2,7p' "$0"; exit 0;;
    *) echo "bilinmeyen seçenek: $1" >&2; exit 2;;
  esac; shift
done
wanted() { [ ${#ONLY[@]} -eq 0 ] && return 0; for o in "${ONLY[@]}"; do [ "$o" = "$1" ] && return 0; done; return 1; }
[ $DRY -eq 1 ] || mkdir -p "$DEST"
stamp=$(date +%Y%m%d-%H%M%S); n_ok=0; n_skip=0; n_bak=0
for src in "$ROOT"/skills/*/ "$ROOT"/vendor/*/; do
  [ -d "$src" ] || continue
  name=$(basename "$src")
  wanted "$name" || continue
  [ -f "$src/SKILL.md" ] || { echo "atla (SKILL.md yok): $name"; n_skip=$((n_skip+1)); continue; }
  case "$src" in */vendor/*) [ -f "$src/REVIEW.md" ] || { echo "ATLA (REVIEW.md yok, denetimsiz): $name"; n_skip=$((n_skip+1)); continue; };; esac
  if [ -d "$DEST/$name" ]; then
    if [ $FORCE -eq 0 ]; then
      echo "yedek: $name → $name.bak-$stamp"; [ $DRY -eq 1 ] || mv "$DEST/$name" "$DEST/$name.bak-$stamp"; n_bak=$((n_bak+1))
    else
      [ $DRY -eq 1 ] || rm -rf "$DEST/$name"
    fi
  fi
  echo "kur: $name"
  if [ $DRY -eq 0 ]; then
    mkdir -p "$DEST/$name"
    (cd "$src" && find . -type f ! -name REVIEW.md ! -name AUDIT-ALLOW ! -path './evals/*' -exec cp --parents {} "$DEST/$name/" \;)
  fi
  n_ok=$((n_ok+1))
done
echo "— $n_ok kuruldu, $n_skip atlandı, $n_bak yedeklendi → $DEST$( [ $DRY -eq 1 ] && echo ' (dry-run, dokunulmadı)')"
[ ${#ONLY[@]} -gt 0 ] && [ $n_ok -eq 0 ] && { echo "--only ile eşleşen skill yok" >&2; exit 1; }; exit 0
