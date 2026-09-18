#!/usr/bin/env bash
# Yayın öncesi sızıntı taraması: izlenen + izlenmeyen tüm dosyalarda özel/kurumsal/makine bilgisi arar.
# Çıkış 0 = temiz, 1 = bulgu var. Kullanım: bash scripts/publish-check.sh
# Yeni bir kurum/proje/makine adı eklemek için ORG veya PATHS'e | ile ekleyin.
set -u
cd "$(dirname "$0")/.."

# Kurum / proje / kişi
ORG='impark|rokodemi|editor@|@impark|detect-question|pdf2pptx|\bK12\b'
# Makine yolları ve oturum kalıntıları (Windows ters bölü, POSIX /c/Users, temp klasörleri)
PATHS='[a-z]:\|\users\|/c/users/|/users/[a-z]+/|\masaüstü|/masaüstü/|appdata\local\temp|scratchpad\|/scratchpad/|claudelocalsessions|2c5661ab'
PATTERN="$ORG|$PATHS"

files() { git ls-files -z --cached --others --exclude-standard | grep -zv '^scripts/publish-check.sh$'; }

hits=$(files | xargs -0 grep -niE -- "$PATTERN" 2>/dev/null)
if [ -n "$hits" ]; then
  echo "SIZINTI ŞÜPHESİ:"; echo "$hits" | cut -c1-180; echo
  echo "$(echo "$hits" | wc -l) satır — yayınlamadan önce temizle."; exit 1
fi

# 11 haneli sayı (kimlik no olabilir) — belgelenmiş örnek 12345678901 hariç
ids=$(files | xargs -0 grep -noE -- '\b[0-9]{11}\b' 2>/dev/null | grep -v 12345678901)
if [ -n "$ids" ]; then echo "11 haneli sayı bulundu (kimlik no?):"; echo "$ids"; exit 1; fi

# E-posta adresleri — noreply ve örnek alan adları hariç
mails=$(files | xargs -0 grep -noE -- '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}' 2>/dev/null | grep -viE 'noreply|ornek\.com|example\.com|company\.com|@ex\.com|anthropic\.com|fsck\.com|@w3\.org')
if [ -n "$mails" ]; then echo "E-posta adresi bulundu:"; echo "$mails"; exit 1; fi

echo "TEMİZ — $(git ls-files --cached --others --exclude-standard | wc -l) dosya tarandı."
