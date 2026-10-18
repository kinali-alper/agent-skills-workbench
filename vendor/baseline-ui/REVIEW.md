# REVIEW — baseline-ui

| Alan | Değer |
|---|---|
| Kaynak | ibelick/ui-skills · skills/baseline-ui · commit 3434a76 (2026-10-16) · MIT |
| Alınma | 2026-10-16, git clone --depth 1 → yalnız `skills/baseline-ui/SKILL.md`; LICENSE depo kökünden. Blob `98477ee` upstream ile birebir |
| Denetim | skill-audit.sh → TEMİZ (1 istisna: `base-ui.com` okuma linki); SKILL.md elle okundu (85 satır) |
| Betik / binary | Yok (tek SKILL.md) |
| allowed-tools / hook | Yok (frontmatter yalnız name + description) |
| Harici alanlar | `base-ui.com` (SKILL.md:33) — bileşen kütüphanesi belgesi, yalnız Markdown linki; ajan bir şey indirmez |
| Katman | 3 · tasarım yönü (üretim) |
| Karar | **ONAYLI** |

## Notlar
- Rol: arayüz kodu için kısa MUST / SHOULD / NEVER zanaat tabanı (yığın, bileşen, etkileşim, animasyon, tipografi, düzen, performans, tasarım). `/baseline-ui <dosya>` ile ihlali satır alıntısı + gerekçe + düzeltme olarak raporlar.
- **Yığın görüşlü:** Tailwind varsayılanları, `motion/react`, `cn` (clsx + tailwind-merge), Base UI / React Aria / Radix. Tailwind/React olmayan projede kuralların bir kısmı uymaz; skill bunu kendisi ayırt etmiyor. Vanilla HTML/CSS işlerinde kural metnini *ilke* olarak okuyun.
- "NEVER add animation unless it is explicitly requested" kuralı, hareket katmanı (motion-design, gsap-*) ile birlikte tetiklenirse çelişebilir; kullanıcı açıkça istediğinde animasyon serbest.
- Çakışma: description ("deslop UI code … fast cleanup or polish pass") `redesign-existing-projects` ve `design-taste-frontend` ile kısmen örtüşür; ikisi uzun ve yön veren, bu kısa ve kural listesi. İzlenecek.
- Aynı depodaki diğer skill'ler alınmadı: `ui-skills-root` her UI işini `npx ui-skills` uzak kayıt defterinden yönlendirir (RED); `create-design-md` doğrulama için sürümsüz `npx @google/design.md` çalıştırır (KOŞULLU); `fixing-accessibility` / `fixing-metadata` / `fixing-motion-performance` mevcut wq-* ve gsap-performance ile tetik çakışması; `improve-ui` temiz ama ihtiyaç dışı; `component-canvas` kapsam dışı. Ayrıntı: dış rapor (beceri-guvenlik-raporu).
