#!/usr/bin/env bash
# skills/ ve vendor/ altındaki skill'leri Claude Code skill klasörüne kurar.
#   bash scripts/install.sh                       # hepsi (REVIEW.md olmayan vendor kurulmaz)
#   bash scripts/install.sh --only ux-a11y-review # yalnız seçilenler (tekrarlanabilir)
#   bash scripts/install.sh --dry-run             # ne yapılacağını göster, dokunma
#   bash scripts/install.sh --force               # mevcut klasörü yedeksiz ez
#   bash scripts/install.sh --no-verify           # vendor bütünlük kontrolünü (INTEGRITY.sha256) atla — önerilmez
#   bash scripts/install.sh --only X --with-deps  # X'in frontmatter metadata.requires listesindekileri de kur
#   bash scripts/install.sh --prune-backups 2     # her skill için en yeni 2 .bak-* dışındakileri sil
# Hedef: $SKILLS_DEST ya da ~/.claude/skills. Mevcut aynı adlı klasör <ad>.bak-YYYYMMDD-HHMMSS olarak saklanır.
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${SKILLS_DEST:-$HOME/.claude/skills}"
ONLY=(); DRY=0; FORCE=0; NOVERIFY=0; WITHDEPS=0; PRUNE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --only) shift; ONLY+=("$1");;
    --dry-run) DRY=1;;
    --force) FORCE=1;;
    --no-verify) NOVERIFY=1;;
    --with-deps) WITHDEPS=1;;
    --prune-backups) shift; PRUNE="$1";;
    -h|--help) sed -n '2,7p' "$0"; exit 0;;
    *) echo "bilinmeyen seçenek: $1" >&2; exit 2;;
  esac; shift
done
wanted() { [ ${#ONLY[@]} -eq 0 ] && return 0; for o in "${ONLY[@]}"; do [ "$o" = "$1" ] && return 0; done; return 1; }
requires_of() { # SKILL.md frontmatter'ındaki metadata.requires → boşlukla ayrılmış liste
  awk 'NR<=40' "$1" 2>/dev/null | grep -E '^\s*requires:' | head -1 | sed -E 's/^[^:]*:\s*"?//; s/"?\s*$//' | tr ',' ' '
}
if [ ${#ONLY[@]} -gt 0 ]; then
  for o in "${ONLY[@]}"; do
    for cand in "$ROOT/skills/$o/SKILL.md" "$ROOT/vendor/$o/SKILL.md"; do
      [ -f "$cand" ] || continue
      for r in $(requires_of "$cand"); do
        wanted "$r" && continue
        if [ $WITHDEPS -eq 1 ]; then echo "bağımlılık eklendi: $r (gereksinim: $o)"; ONLY+=("$r")
        elif [ -d "$DEST/$r" ]; then :
        else echo "UYARI: $o, '$r' skill'ini gerektirir; kurulu değil ve --only listesinde yok (--with-deps ile ekle)"; fi
      done
    done
  done
fi
[ $DRY -eq 1 ] || mkdir -p "$DEST"
stamp=$(date +%Y%m%d-%H%M%S); n_ok=0; n_skip=0; n_bak=0
for src in "$ROOT"/skills/*/ "$ROOT"/vendor/*/; do
  [ -d "$src" ] || continue
  name=$(basename "$src")
  wanted "$name" || continue
  [ -f "$src/SKILL.md" ] || { echo "atla (SKILL.md yok): $name"; n_skip=$((n_skip+1)); continue; }
  case "$src" in */vendor/*)
    [ -f "$src/REVIEW.md" ] || { echo "ATLA (REVIEW.md yok, denetimsiz): $name"; n_skip=$((n_skip+1)); continue; }
    if [ $NOVERIFY -eq 0 ] && ! bash "$ROOT/scripts/verify-integrity.sh" "$name" >/dev/null 2>&1; then
      echo "REDDET (bütünlük: vendor/$name INTEGRITY.sha256 ile uyuşmuyor — içerik değişmiş ya da kayıtsız dosya var; --no-verify ile geç): $name"; n_skip=$((n_skip+1)); continue
    fi;; esac
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
if [ -n "$PRUNE" ] && [ $DRY -eq 0 ]; then
  for base in $(ls "$DEST" 2>/dev/null | grep -oE '^.+\.bak-[0-9]{8}-[0-9]{6}$' | sed -E 's/\.bak-.*//' | sort -u); do
    ls -d "$DEST/$base".bak-* 2>/dev/null | sort -r | tail -n +$((PRUNE+1)) | while read -r old; do echo "yedek silindi: $(basename "$old")"; rm -rf "$old"; done
  done
fi
echo "— $n_ok kuruldu, $n_skip atlandı, $n_bak yedeklendi → $DEST$( [ $DRY -eq 1 ] && echo ' (dry-run, dokunulmadı)')"
[ ${#ONLY[@]} -gt 0 ] && [ $n_ok -eq 0 ] && { echo "--only ile eşleşen skill yok" >&2; exit 1; }; exit 0
