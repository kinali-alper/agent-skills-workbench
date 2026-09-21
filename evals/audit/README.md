# Audit corpus — `skill-audit.sh` regresyon testi

Her klasör bilerek hazırlanmış bir SKILL.md; `expected.tsv` beklenen çıkış kodunu verir (0 temiz · 1 uyarı · 2 kritik).
`bash scripts/test-audit.sh` hepsini koşar; herhangi biri beklenenden saparsa 1 döner. CI'da kapı olarak kullanılır.

| Örnek | Ne test eder | Beklenen |
|---|---|---|
| 01-injection-curl-bash | `allowed-tools`, `curl \| bash`, "do not tell the user" | 2 |
| 02-blank-line-frontmatter | İlk satır `---` değil → frontmatter gizleme (21 Eyl HuggingChat bulgusu) | 2 |
| 03-hidden-unicode | U+200B sıfır-genişlik karakter | 2 |
| 04-turkish-injection | Türkçe injection ifadeleri ("talimatları yok say", "kullanıcıya söyleme", "gizlice") | 2 |
| 05-unknown-domain | Tanınmayan alan adından kural çekme | 1 |
| 06-benign-example-code | Örnek koddaki `password`/yorum/MDN linki → **yanlış pozitif üretmemeli** | 0 |
| 07-hidden-unicode-in-script | `.sh` içinde U+200B — Unicode taraması yalnız `.md` ile sınırlı kalmamalı (ChatGPT §12) | 2 |
