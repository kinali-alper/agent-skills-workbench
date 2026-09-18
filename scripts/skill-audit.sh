#!/usr/bin/env bash
# Skill güvenlik taraması. Kullanım: bash scripts/skill-audit.sh <skill-klasörü> [...]
# Çıkış kodu: 0 = temiz, 1 = incelenmesi gereken bulgu var, 2 = kritik (betik/yetki/injection)
set -u
RED=$'\e[31m'; YEL=$'\e[33m'; GRN=$'\e[32m'; NC=$'\e[0m'
overall=0

# Tasarım metinlerinde normal olan sözcükleri eleyen istisna listesi
BENIGN='design token|tokens?\b|color token|spacing token|token strategy|token system|--token|tokeniz|overflow: ?hidden|overflow-hidden|aria-hidden|visibility: ?hidden|visually-hidden|sr-only|hidden (state|element|content|menu|field|nav|layer|input|label|text|until|behind|on mobile|by default|skip)|skip-link|silently (fail|ignor|using)|telemetry (ui|interface|&)|tactical telemetry|hidden gems|hidden complexity|auth token|license key|api[_-]?key%|SHOPIFY_API_KEY|type="password"|for="password"|id="password|password-requirements|remembering a password|passwordless|current-password'

scan_one() {
  local dir="$1"; local crit=0; local warn=0
  local rel="s|^$dir/||"
  echo "=================================================================="
  echo " $dir"
  echo "=================================================================="
  [ -d "$dir" ] || { echo "${RED}klasör yok${NC}"; return 2; }

  echo "--- 1. Dosya envanteri"
  local total; total=$(find "$dir" -type f -not -path "*/.git/*" | wc -l)
  local nonmd; nonmd=$(find "$dir" -type f -not -path "*/.git/*" ! -iname "*.md" ! -iname "*.txt" ! -iname "LICENSE*" ! -iname "*.json" ! -iname "*.yaml" ! -iname "*.yml" ! -iname "*.png" ! -iname "*.jpg" ! -iname "*.svg")
  echo "    toplam dosya: $total"
  if [ -n "$nonmd" ]; then
    echo "${RED}    [KRİTİK] Markdown dışı çalıştırılabilir/betik dosyalar — elle incele:${NC}"; echo "$nonmd" | sed "$rel" | sed 's/^/      /'; crit=1
  else echo "${GRN}    betik/binary yok${NC}"; fi

  echo "--- 2. Frontmatter (allowed-tools, hooks, metadata)"
  local fm; fm=$(find "$dir" -name "SKILL.md" -exec awk 'NR==1&&/^---/{p=1;next} p&&/^---/{exit} p' {} \; | grep -viE "^(name|description|license):" | grep -vE "^\s*$")
  if echo "$fm" | grep -qiE "allowed-tools|hooks?:|pre[_-]?run|post[_-]?run|command:"; then
    echo "${RED}    [KRİTİK] Yetki/hook alanı var:${NC}"; echo "$fm" | sed 's/^/      /'; crit=1
  elif [ -n "$fm" ]; then echo "${YEL}    [BİLGİ] Ek alanlar:${NC}"; echo "$fm" | sed 's/^/      /'
  else echo "${GRN}    yalnız name/description${NC}"; fi

  echo "--- 3. Tehlikeli komut kalıpları"
  local danger; danger=$(grep -rniE "\bcurl\b|\bwget\b|Invoke-WebRequest|Invoke-Expression|\biex\b|\beval\(|\bexec\(|base64|\bnc -|\brm -rf|chmod \+x|\bsudo\b|\.env\b|api[_-]?key|secret|password|credential|\bssh\b|\btoken\b" --include="*.md" "$dir" 2>/dev/null | grep -viE "$BENIGN")
  if [ -n "$danger" ]; then echo "${YEL}    [UYARI] İncele:${NC}"; echo "$danger" | sed "$rel" | cut -c1-200 | sed 's/^/      /'; warn=1
  else echo "${GRN}    yok${NC}"; fi

  echo "--- 4. Prompt injection ifadeleri"
  local inj; inj=$(grep -rniE "ignore (all |any )?(previous|prior|above|earlier)|disregard (the |your )?(instructions|rules|system)|you are now|new system prompt|do not (tell|inform|show|mention) (the |to )?user|without (telling|informing|asking|notifying) the user|\bsecretly\b|exfiltrat|send (this|the|all|your) .{0,40}(to|via) (http|url|endpoint|server|email)|upload .{0,30}to http|report back to|analytics endpoint|phone home|run this (script|command) first|before (anything|you begin), (run|execute|fetch)" --include="*.md" "$dir" 2>/dev/null | grep -viE "$BENIGN")
  if [ -n "$inj" ]; then echo "${RED}    [KRİTİK] İncele:${NC}"; echo "$inj" | sed "$rel" | cut -c1-200 | sed 's/^/      /'; crit=1
  else echo "${GRN}    yok${NC}"; fi

  echo "--- 5. Gizli HTML yorumları"
  local cm; cm=$(grep -rn "<!--" --include="*.md" "$dir" 2>/dev/null | grep -viE "TODO|mock|example|placeholder|CONTENT HERE|position: fixed|❌|✅|<!-- [a-zA-Z ()—-]{2,60} -->")
  if [ -n "$cm" ]; then echo "${YEL}    [UYARI] Örnek kod dışı yorum:${NC}"; echo "$cm" | sed "$rel" | cut -c1-200 | sed 's/^/      /'; warn=1
  else echo "${GRN}    yok / yalnız örnek kod içinde${NC}"; fi

  echo "--- 6. Görünmez / yön-değiştiren Unicode"
  local uni; uni=$(python - "$dir" <<'PY'
import sys,pathlib,re
bad=re.compile('[​-‏ -‮⁠-⁤﻿]|[\U000e0000-\U000e007f]')
for p in pathlib.Path(sys.argv[1]).rglob('*.md'):
    if '.git' in p.parts: continue
    for i,l in enumerate(p.read_text(encoding='utf-8',errors='replace').splitlines(),1):
        if bad.search(l): print(f"{p}:{i}")
PY
)
  if [ -n "$uni" ]; then echo "${RED}    [KRİTİK] Gizli karakter:${NC}"; echo "$uni" | sed "$rel" | sed 's/^/      /'; crit=1
  else echo "${GRN}    yok${NC}"; fi

  echo "--- 7. Harici alan adları"
  local urls; urls=$(grep -rhoiE "https?://[a-zA-Z0-9._-]+" --include="*.md" "$dir" 2>/dev/null | sort | uniq -c | sort -rn)
  if [ -n "$urls" ]; then echo "$urls" | sed 's/^/      /'; else echo "      (yok)"; fi

  echo "--- 8. Boyut"
  find "$dir" -name "*.md" -exec wc -l {} + | sort -rn | head -3 | sed "$rel" | sed 's/^/      /'
  local big; big=$(find "$dir" -name "SKILL.md" -exec wc -l {} \; | awk '$1>800{print $1}')
  [ -n "$big" ] && { echo "${YEL}    [BİLGİ] SKILL.md 800+ satır — context maliyeti yüksek${NC}"; }

  echo
  if [ $crit -eq 1 ]; then echo "${RED}SONUÇ: KRİTİK — kurmadan önce elle incele${NC}"; return 2
  elif [ $warn -eq 1 ]; then echo "${YEL}SONUÇ: UYARI — bulguları gözden geçir${NC}"; return 1
  else echo "${GRN}SONUÇ: TEMİZ${NC}"; return 0; fi
}

for d in "$@"; do scan_one "$d"; rc=$?; [ $rc -gt $overall ] && overall=$rc; echo; done
exit $overall
