# REVIEW — wq-web-quality-audit

| Alan | Değer |
|---|---|
| Kaynak | addyosmani/web-quality-skills · skills/web-quality-audit · commit afa8da9 (2026-08-24) · MIT |
| Alınma | 2026-09-18, git clone --depth 1 → yalnız skill klasörü kopyalandı |
| Denetim | skill-audit.sh → KRİTİK (betik var) → elle incelendi, güvenli |
| Betik | `scripts/analyze.sh` — ELLE OKUNDU: salt-okunur (grep/find/jq), ağ yok, yazma yok, set -euo pipefail. Bağımlılık: **jq** (bu makinede yok → kurulmalı ya da betik kullanılmaz; SKILL.md betik olmadan da çalışır) |
| allowed-tools / hook | Yok (metadata: author, version) |
| Harici alanlar | web.dev, developer.chrome.com, MDN, w3.org gibi tanınmış kaynaklar |
| Katman | 5 · web kalitesi |
 **ONAYLI** |

## Notlar
- Skill adı çakışma riskine karşı `wq-` öneki ile kuruldu (frontmatter `name` alanı orijinal kaldı).
- Stack: bağımsız (React/Vue/Angular/Svelte/Next/Nuxt/Astro/HTML örnekleri var).

