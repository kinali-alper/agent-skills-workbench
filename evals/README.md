# evals

Her vaka bir klasör: `cases/<ad>/`
- `expected.md` — skill'in yakalaması beklenen bulgular (WCAG kriter no + hangi araç yakaladı + kim yakalamalı) ve **geçme kriteri**
- `notes.md` — vakanın neden seçildiği, hangi skill'i test ettiği, nasıl çalıştırıldığı
- Girdi: ya `input.*` dosyası burada, ya da `playground/` içindeki kaynağa işaret (broken-form böyle)
- Stack-bağımsızlık kanıtı: aynı vakanın **düz HTML** ve **Razor (.cshtml)** ikizleri (broken-form'da var)

Skill "geçti" = expected.md'deki geçme kriterini sağladı, uydurma bulgu eklemedi.

Not: Anthropic `skill-creator` kendi eval formatını taşır; kendi skill'imizi yazmadan önce bu format
onunla hizalanacak (tek format, çift bakım yok).
