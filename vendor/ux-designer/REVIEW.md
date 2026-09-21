# REVIEW — ux-designer

| Alan | Değer |
|---|---|
| Kaynak | szilu/ux-designer-skill · commit da9e9d0 (2026-08-14) · MIT · 62★ |
| Alınma | 2026-09-18, git clone --depth 1 → SKILL.md + references/ (24 dosya, ~11.700 satır) |
| Denetim | skill-audit.sh → 2 KRİTİK, ikisi de yanlış alarm (aşağıda) |
| Betik / binary | Yok (.git bulgusu tarama kökü hatasıydı) |
| Gizli unicode | `references/23-internationalization.md:196` U+200F ×2 — Arapça tarih örneği içinde doğal RTL işareti; talimat gizleme değil |
| allowed-tools / hook | Yok |
| Harici alanlar | nngroup.com, w3.org, apple, material — tanınmış |
| Yapı | SKILL.md (297 satır) referanslara **koşullu işaretçi** ile ulaşır ("For forms, see 07-…") → progressive disclosure doğru; 24 dosya her seferinde yüklenmez |
| Katman | 2 · UX bilgi tabanı |
 **ONAYLI** |

## Notlar
- Rol: **UX/kullanılabilirlik bilgi tabanı** — Nielsen, Gestalt, Laws of UX, form/navigasyon/hata/onboarding/UX writing. Bizim UX bacağının ana referansı.
- Kendi skill'imizde **kopyalamak yerine** ilgili referans dosyalarına işaret edilecek: 01-core-principles, 07-forms-and-inputs, 09-ux-writing, 21-data-tables.
- Adı klasörle uyumlu olsun diye `ux-designer` yapıldı.

- 2026-09-18: description'dan "accessibility audits (WCAG, EAA)" kırpıldı — wq-accessibility ve ux-a11y-review ile tetik çakışmasını önlemek için. Referans dosyası 03-accessibility.md yerinde duruyor.
