# REVIEW — web-design-guidelines

| Alan | Değer |
|---|---|
| Kaynak | vercel-labs/agent-skills · skills/web-design-guidelines · commit 063bee9 (2026-08-28) · MIT |
| Kural dosyası | vercel-labs/web-interface-guidelines · `command.md` · commit 434b7f9 (2026-10-05) · MIT — blob `3eb3a21` upstream ile birebir |
| Alınma | 2026-09-18, git clone --depth 1 → yalnız skill klasörü kopyalandı; 2026-10-16 kural dosyası yerele alındı (aşağıda Uyarlama) |
| Denetim | skill-audit.sh → TEMİZ, istisnasız (`--no-allow` ile de 0); SKILL.md ve command.md elle okundu |
| Betik / binary | Yok (SKILL.md 35 satır + command.md 191 satır) |
| allowed-tools / hook | Yok (metadata: author, version, argument-hint) |
| Harici alanlar | Yok — çalışma anında ağ çağrısı da yok (Uyarlama sonrası) |
| Katman | 1 · inceleme çekirdeği |
| Karar | **ONAYLI** (uyarlanmış) |

## Uyarlama — uzak kural çekme kaldırıldı (2026-10-16)
- **Sorun:** upstream SKILL.md her incelemede kuralları `raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` adresinden WebFetch ile çekip "tüm kuralları uygula" diyordu. Uzak dosya değişirse (ya da ele geçirilirse) asistanın davranışı, bu depodaki denetim ve sabitleme olmadan değişir; çevrimdışı da çalışmaz. (Eski not "vercel.com/design/guidelines'tan çeker" diyordu; doğru adres yukarıdaki.)
- **Değişiklik:** kural listesi `command.md` olarak skill klasörüne kondu (upstream 434b7f9, birebir). SKILL.md'deki "How It Works", "Guidelines Source" ve "Usage" bölümleri uzak adres ve WebFetch yerine bu yerel dosyayı okutacak biçimde yeniden yazıldı; frontmatter (name, description, metadata) değişmedi.
- **Fark (18 Eyl kopyası → 434b7f9):** tek satır eklendi (`command.md:107`, Interactions / Overscroll): masaüstünde `@media (pointer: fine)` içinde `<html>` için `overscroll-behavior: none`, dokunmatikte varsayılanın korunması. Komut, URL, talimat değişikliği yok. Eski `command-snapshot-2026-09-18.md` kaldırıldı (git geçmişinde duruyor); dosya-düzeyi AUDIT-ALLOW istisnası da artık gereksiz olduğu için silindi (CONTRIBUTING md. 8).
- **Yenileme:** upstream'i ayrı klasöre klonla → `diff` ile yerel `command.md`'ye karşı farkı oku (URL, komut, talimat ara) → güvenliyse kopyala, bu tabloda pin ve tarihi güncelle → `skill-audit.sh` → `gen-manifest.sh` → `install.sh --only web-design-guidelines`. SKILL.md'ye dokunmak gerekmez (dosya adı sabit).

## Notlar
- Kapsam: erişilebilirlik, focus, form, animasyon, layout, içerik, performans, copywriting — "denetim" modu.
- Stack: bağımsız (dosya/desen alır).
- 2026-09-18: BrokenForm testi 8/9 (uzak kural listesiyle; yerel kopya o günkü listeyle bir satır dışında aynı).
