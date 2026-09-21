#!/usr/bin/env bash
# vendor/ içeriğini INTEGRITY.sha256 ile karşılaştırır. Çıkış 0 = birebir; 1 = değişmiş/eksik/fazla dosya var.
#   bash scripts/verify-integrity.sh            # tümü
#   bash scripts/verify-integrity.sh gsap-core  # tek skill
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
F=vendor/INTEGRITY.sha256; [ -f "$F" ] || { echo "INTEGRITY.sha256 yok — önce gen-integrity.sh" >&2; exit 1; }
only="${1:-}"; rc=0
# 1) kayıtlı dosyalar değişmiş/silinmiş mi
lines=$(if [ -n "$only" ]; then grep -E "^[0-9a-f]{64} [ *]vendor/$only/" "$F"; else grep -v '^#' "$F"; fi)
[ -n "$lines" ] || { echo "  INTEGRITY.sha256'da ${only:-vendor} için kayıt yok"; rc=1; }
[ -n "$lines" ] && { echo "$lines" | sha256sum -c --quiet 2>&1 | sed 's/^/  /'; [ ${PIPESTATUS[1]} -eq 0 ] || rc=1; }
# 2) kayıtsız yeni dosya var mı (sessizce eklenen dosya = denetimsiz içerik)
known=$(mktemp); grep -v '^#' "$F" | sed -E 's/^[0-9a-f]{64} [ *]//' | sort > "$known"
extra=$(find "vendor/${only:-}" -type f ! -name INTEGRITY.sha256 ! -name .audit-status 2>/dev/null | sort | comm -23 - "$known" || true); rm -f "$known"
if [ -n "$extra" ]; then echo "  KAYITSIZ DOSYA (bütünlük listesinde yok):"; echo "$extra" | sed 's/^/    /'; rc=1; fi
[ $rc -eq 0 ] && echo "bütünlük: birebir${only:+ ($only)}" || echo "bütünlük: SAPMA — vendor içeriği INTEGRITY.sha256 ile uyuşmuyor; gen-integrity.sh yalnız bilinçli değişiklikten sonra"
exit $rc
