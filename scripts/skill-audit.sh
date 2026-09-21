#!/usr/bin/env bash
# Skill güvenlik taraması. Kullanım: bash scripts/skill-audit.sh <skill-klasörü> [...]
# Çıkış kodu: 0 = temiz, 1 = incelenmesi gereken bulgu var, 2 = kritik (betik/yetki/injection)
set -u
PY=$(command -v python3 || command -v python)   # Ubuntu: python3; Git Bash/msys: python
RED=$'\e[31m'; YEL=$'\e[33m'; GRN=$'\e[32m'; NC=$'\e[0m'
overall=0
NOALLOW=0; [ "${1:-}" = "--no-allow" ] && { NOALLOW=1; shift; echo "(katı kip: AUDIT-ALLOW yok sayılıyor — ham bulgular)"; }

# Tasarım metinlerinde normal olan sözcükleri eleyen istisna listesi
BENIGN='design token|tokens?\b|color token|spacing token|token strategy|token system|--token|tokeniz|overflow: ?hidden|overflow-hidden|aria-hidden|visibility: ?hidden|visually-hidden|sr-only|hidden (state|element|content|menu|field|nav|layer|input|label|text|until|behind|on mobile|by default|skip)|skip-link|silently (fail|ignor|using)|telemetry (ui|interface|&)|tactical telemetry|hidden gems|hidden complexity|auth token|license key|api[_-]?key%|SHOPIFY_API_KEY|type="password"|for="password"|id="password|password-requirements|remembering a password|passwordless|current-password|password[- ](field|manager|strength|requirement|input|hint|reset|visibility|toggle)s?|paste in password'

# AUDIT-ALLOW: skill klasöründe, satır başına bir ERE deseni (göreli yol veya bulgu metnine karşı).
# Eşleşen bulgular hükme girmez; REVIEW.md'de gerekçesi yazılı olmalı. Boş/yorum satırları (#) yok sayılır.
allow_filter() {  # stdin: bulgular (göreli yollu) → stdout: izin listesinde OLMAYANLAR
  local f="$1"
  if [ "${NOALLOW:-0}" = "1" ]; then cat; return; fi
  if [ -f "$f" ]; then
    local pat; pat=$(grep -vE '^\s*(#|$)' "$f" | paste -sd'|' -)
    if [ -n "$pat" ]; then grep -vE -- "$pat" || true; else cat; fi
  else cat; fi
}

scan_one() {
  local dir="${1%/}"; local crit=0; local warn=0
  local rel="s|^$dir/||"
  local ALLOW="$dir/AUDIT-ALLOW"
  [ -f "$ALLOW" ] && echo "    (AUDIT-ALLOW: $(grep -cvE '^\s*(#|$)' "$ALLOW") istisna)"
  echo "=================================================================="
  echo " $dir"
  echo "=================================================================="
  [ -d "$dir" ] || { echo "${RED}klasör yok${NC}"; return 2; }

  echo "--- 1. Dosya envanteri"
  local total; total=$(find "$dir" -type f -not -path "*/.git/*" | wc -l)
  local nonmd; nonmd=$(find "$dir" -type f -not -path "*/.git/*" ! -iname "*.md" ! -iname "*.txt" ! -iname "LICENSE*" ! -iname "*.json" ! -iname "*.yaml" ! -iname "*.yml" ! -iname "*.png" ! -iname "*.jpg" ! -iname "*.svg" ! -name AUDIT-ALLOW | sed "$rel" | allow_filter "$ALLOW")
  echo "    toplam dosya: $total"
  if [ -n "$nonmd" ]; then
    echo "${RED}    [KRİTİK] Markdown dışı çalıştırılabilir/betik dosyalar — elle incele:${NC}"; echo "$nonmd" | sed 's/^/      /'; crit=1
  else echo "${GRN}    betik/binary yok${NC}"; fi

  echo "--- 2. Frontmatter (allowed-tools, hooks, metadata)"
  local sk="$dir/SKILL.md"
  if [ -f "$sk" ]; then
    local first; first=$(head -c 3 "$sk" | od -An -tx1 | tr -d ' 
')
    local l1; l1=$(sed -n '1p' "$sk" | tr -d '
')
    if [ "$l1" != "---" ]; then
      echo "${RED}    [KRİTİK] SKILL.md ilk satırı '---' değil (BOM/boş satır/gizli önek: $([ "$first" = "efbbbf" ] && echo 'UTF-8 BOM' || echo "'${l1:0:40}'")) — spesifikasyon dışı, frontmatter gizlenmiş olabilir${NC}"; crit=1
    fi
  fi
  # frontmatter bloğunu ilk 5 satır içinde başladığı yerden oku (gizlemeye karşı)
  local fm; fm=$(find "$dir" -name "SKILL.md" -exec awk 'NR<=5&&!p&&/^ï?»?¿?---
?$/{p=1;next} p&&/^---
?$/{exit} p' {} \; | grep -viE "^(name|description|license):" | grep -vE "^\s*$")
  if echo "$fm" | grep -qiE "allowed-tools|hooks?:|pre[_-]?run|post[_-]?run|command:"; then
    echo "${RED}    [KRİTİK] Yetki/hook alanı var:${NC}"; echo "$fm" | sed 's/^/      /'; crit=1
  elif [ -n "$fm" ]; then echo "${YEL}    [BİLGİ] Ek alanlar:${NC}"; echo "$fm" | sed 's/^/      /'
  else echo "${GRN}    yalnız name/description${NC}"; fi

  echo "--- 3. Tehlikeli komut kalıpları"
  local danger; danger=$(grep -rniE "\bcurl\b|\bwget\b|Invoke-WebRequest|Invoke-Expression|\biex\b|\beval\(|\bexec\(|base64|\bnc -|\brm -rf|chmod \+x|\bsudo\b|\.env\b|api[_-]?key|secret|password|credential|\bssh\b|\btoken\b" --include="*.md" "$dir" 2>/dev/null | grep -viE "$BENIGN" | sed "$rel" | allow_filter "$ALLOW")
  if [ -n "$danger" ]; then echo "${YEL}    [UYARI] İncele:${NC}"; echo "$danger" | cut -c1-200 | sed 's/^/      /'; warn=1
  else echo "${GRN}    yok${NC}"; fi

  echo "--- 4. Prompt injection ifadeleri"
  local inj; inj=$(grep -rniE "ignore (all |any )?(previous|prior|above|earlier)|disregard (the |your )?(instructions|rules|system)|you are now|new system prompt|do not (tell|inform|show|mention) (the |to )?user|without (telling|informing|asking|notifying) the user|\bsecretly\b|exfiltrat|send (this|the|all|your) .{0,40}(to|via) (http|url|endpoint|server|email)|upload .{0,30}to http|report back to|analytics endpoint|phone home|run this (script|command) first|before (anything|you begin), (run|execute|fetch)|(önceki|yukarıdaki|tüm) talimatları (yok say|unut|görmezden gel)|kullanıcıya (söyleme|bildirme|gösterme)|kullanıcıya haber vermeden|gizlice|sistem (istemi|promptu)n[ıi] (değiştir|yok say)|artık sen .{0,30}s[ıi]n" --include="*.md" "$dir" 2>/dev/null | grep -viE "$BENIGN" | sed "$rel" | allow_filter "$ALLOW")
  if [ -n "$inj" ]; then echo "${RED}    [KRİTİK] İncele:${NC}"; echo "$inj" | cut -c1-200 | sed 's/^/      /'; crit=1
  else echo "${GRN}    yok${NC}"; fi

  echo "--- 5. Gizli HTML yorumları"
  local cm; cm=$(grep -rn "<!--" --include="*.md" "$dir" 2>/dev/null | grep -viE "TODO|mock|example|placeholder|CONTENT HERE|position: fixed|❌|✅|<!-- [a-zA-Z ()—-]{2,60} -->" | sed "$rel" | allow_filter "$ALLOW")
  if [ -n "$cm" ]; then echo "${YEL}    [UYARI] Örnek kod dışı yorum:${NC}"; echo "$cm" | cut -c1-200 | sed 's/^/      /'; warn=1
  else echo "${GRN}    yok / yalnız örnek kod içinde${NC}"; fi

  echo "--- 6. Görünmez / yön-değiştiren Unicode (tüm metin dosyaları)"
  local uni; uni=$("$PY" - "$dir" <<'PY' | sed "$rel" | allow_filter "$ALLOW"
import sys,pathlib,re
bad=re.compile('[​-‏ -‮⁠-⁤﻿]|[\U000e0000-\U000e007f]')
root=pathlib.Path(sys.argv[1])
EXT={'.md','.txt','.sh','.bash','.js','.cjs','.mjs','.ts','.json','.yaml','.yml','.html','.css','.toml','.py','.cmd','.ps1'}
for p in root.rglob('*'):
    if '.git' in p.parts or not p.is_file(): continue
    if p.suffix.lower() not in EXT and p.name not in ('AUDIT-ALLOW','LICENSE'): continue
    for i,l in enumerate(p.read_text(encoding='utf-8',errors='replace').splitlines(),1):
        if bad.search(l): print(f"{p.relative_to(root).as_posix()}:{i}")
PY
)
  if [ -n "$uni" ]; then echo "${RED}    [KRİTİK] Gizli karakter:${NC}"; echo "$uni" | sed 's/^/      /'; crit=1
  else echo "${GRN}    yok${NC}"; fi

  echo "--- 7. Harici alan adları"
  local urls; urls=$(grep -rhoiE "https?://[a-zA-Z0-9._-]+" --include="*.md" "$dir" 2>/dev/null | sort | uniq -c | sort -rn)
  if [ -n "$urls" ]; then
    echo "$urls" | sed 's/^/      /'
    local KNOWN='github\.com|githubusercontent\.com|w3\.org|developer\.mozilla\.org|web\.dev|developer\.chrome\.com|gsap\.com|greensock\.com|anthropic\.com|claude\.com|vercel\.com|nngroup\.com|apple\.com|material\.io|microsoft\.com|google\.com|shopify\.(com|dev)|atlassian\.(com|design)|radix-ui\.com|shadcn\.com|tailwindcss\.com|getbootstrap\.com|primer\.style|carbondesignsystem\.com|designsystem\.digital\.gov|design-system\.service\.gov\.uk|fluent2\.microsoft\.design|picsum\.photos|simpleicons\.org|npmjs\.com|npm\.im|dequeuniversity\.com|webaim\.org|schema\.org|json-ld\.org|csswg\.org|whatwg\.org|wikipedia\.org|youtube\.com|lottiefiles\.com|figma\.com|easing\.dev|easings\.co|pagespeed\.web\.dev|search\.google\.com|framer\.com|motion\.dev|react\.dev|nextjs\.org|vitejs\.dev|nuxt\.com|vuejs\.org|svelte\.dev|astro\.build|angular\.dev|storybook\.js\.org|playwright\.dev|jestjs\.io|vitest\.dev|learn\.microsoft\.com|docs\.microsoft\.com|developer\.android\.com|khronos\.org|caniuse\.com|chromestatus\.com|webkit\.org|mozilla\.org|ietf\.org|rfc-editor\.org|owasp\.org|localhost|example\.com|ornek\.com|[a-z-]+\.example|(external|trusted|trusted-cdn|cdn|api|app|site|mysite|yoursite|yourdomain|domain)\.com|fonts\.googleapis\.com|fonts\.gstatic\.com|twitter\.com|x\.com|linkedin\.com|facebook\.com'
    local unk; unk=$(echo "$urls" | awk '{print $2}' | sed -E 's#https?://##' | grep -viE "(^|\.)($KNOWN)$" | allow_filter "$ALLOW" || true)
    if [ -n "$unk" ]; then echo "${YEL}    [UYARI] Tanınmayan alan adı — REVIEW'da gerekçelendir ya da AUDIT-ALLOW:${NC}"; echo "$unk" | sed 's/^/      /'; warn=1; fi
  else echo "      (yok)"; fi

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
