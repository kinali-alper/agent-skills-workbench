#!/usr/bin/env bash
# Yayın öncesi sızıntı taraması: izlenen + izlenmeyen tüm dosyalarda makine yolu, e-posta, kimlik numarası
# ve — varsa — scripts/publish-check.local'daki (git dışı) kurum/proje/kişi adlarını arar.
# Çıkış 0 = temiz, 1 = bulgu var. Kullanım: bash scripts/publish-check.sh
set -u
cd "$(dirname "$0")/.."

# Genel desenler (herkes için geçerli): Windows/POSIX makine yolları, temp/oturum klasörleri
PATHS='[a-z]:\|\users\|/c/users/|/users/[a-z]+/|appdata\local\temp|scratchpad\|/scratchpad/|claudelocalsessions'
PATTERN="$PATHS"
# Yerel desenler: kurum/proje/kişi adları — izlenmeyen dosyadan
LOCAL="scripts/publish-check.local"
if [ -f "$LOCAL" ]; then
  extra=$(grep -vE '^\s*(#|$)' "$LOCAL" | paste -sd'|' -)
  [ -n "$extra" ] && PATTERN="$PATTERN|$extra"
  echo "(publish-check.local: $(grep -cvE '^\s*(#|$)' "$LOCAL") yerel desen yüklendi)"
else
  echo "UYARI: scripts/publish-check.local yok — yalnız genel desenler taranıyor. Kurum/proje adlarını oraya yazın." >&2
fi

files() { git ls-files -z --cached --others --exclude-standard; }   # bu betik dahil, kendini de tarar

hits=$(files | xargs -0 grep -niE -- "$PATTERN" 2>/dev/null | grep -vE "^scripts/publish-check\.sh:[0-9]+:PATHS=")   # yalnız kendi desen tanımı hariç
if [ -n "$hits" ]; then
  echo "SIZINTI ŞÜPHESİ:"; echo "$hits" | cut -c1-180; echo
  echo "$(echo "$hits" | wc -l) satır — yayınlamadan önce temizle."; exit 1
fi

# 11 haneli sayı (kimlik no olabilir) — belgelenmiş örnek 12345678901 hariç
ids=$(files | xargs -0 grep -noE -- '\b[0-9]{11}\b' 2>/dev/null | grep -v 12345678901)
if [ -n "$ids" ]; then echo "11 haneli sayı bulundu (kimlik no?):"; echo "$ids"; exit 1; fi

# E-posta adresleri — noreply ve örnek/kamusal alan adları hariç
mails=$(files | xargs -0 grep -noE -- '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}' 2>/dev/null | grep -viE 'noreply|ornek\.com|example\.com|company\.com|@ex\.com|anthropic\.com|fsck\.com|@w3\.org')
if [ -n "$mails" ]; then echo "E-posta adresi bulundu:"; echo "$mails"; exit 1; fi

echo "TEMİZ — $(git ls-files --cached --others --exclude-standard | wc -l) dosya tarandı."
