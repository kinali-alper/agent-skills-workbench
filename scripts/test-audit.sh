#!/usr/bin/env bash
# skill-audit.sh regresyon testi: evals/audit/* her örnek expected.tsv'deki çıkış kodunu vermeli.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; fail=0
while IFS=$'\t' read -r name want; do
  [ -n "$name" ] || continue
  bash "$ROOT/scripts/skill-audit.sh" "$ROOT/evals/audit/$name" >/dev/null 2>&1; got=$?
  if [ "$got" = "$want" ]; then printf "  ok   %-28s rc=%s\n" "$name" "$got"; else printf "  FAIL %-28s beklenen=%s alınan=%s\n" "$name" "$want" "$got"; fail=1; fi
done < "$ROOT/evals/audit/expected.tsv"
[ $fail -eq 0 ] && echo "audit korpusu: hepsi beklendiği gibi" || { echo "audit korpusu: SAPMA VAR"; exit 1; }
