# REVIEW — interface-design

| Alan | Değer |
|---|---|
| Kaynak | Dammyjay93/interface-design · .claude/skills/interface-design · commit 2f9be32 (2026-06-20) · MIT |
| Alınma | 2026-10-16, git clone --depth 1 → yalnız `SKILL.md`; LICENSE depo kökünden. Blob `92e1df4` upstream ile birebir. `agents/openai.yaml` alınmadı (Codex arayüz meta verisi, emsal: THIRD_PARTY_NOTICES) |
| Denetim | skill-audit.sh → TEMİZ; SKILL.md (320 satır) ve depodaki tüm dosyalar (15) elle okundu |
| Betik / binary | Skill klasöründe yok. Depoda `.githooks/pre-commit` var — aşağıda |
| allowed-tools / hook | Yok (frontmatter yalnız name + description) |
| Harici alanlar | Yok |
| Katman | 3 · tasarım yönü (üretim) |
| Karar | **ONAYLI** |

## Notlar
- Rol: panel / SaaS / araç arayüzü için zanaat disiplini — niyet (kim, ne yapacak, nasıl hissettirecek), alan keşfi (alan, renk dünyası, imza, reddedilen varsayılanlar), görsel hiyerarşi, token mimarisi, durumlar, hareket; "Not for marketing pages". Kararları kullanıcı onaylarsa `.interface-design/system.md`'ye yazar (SKILL.md:303 "Always offer to save … If yes").
- Dosya yazma: yalnız onaylı `system.md`; UI düzenlemesi sonrası "run the relevant build/typecheck/tests when available" (SKILL.md:270) — projenin kendi komutları, ağ yok.
- SKILL.md:262 "Be invisible. Don't announce modes or narrate process" — süreç anlatımını kısaltma talimatı; eylem gizleme değil (değişiklikler ve öneriler kullanıcıya söylenir).
- **Depo kancası:** `.githooks/pre-commit` (18 satır) her commit'te `sed -i ''` ile plugin.json / marketplace.json sürümünü günceller ve `git add` yapar. Yalnız `git config core.hooksPath .githooks` ile etkinleşir; klonlamak çalıştırmaz. Bu vendor'a alınmadı, çalıştırılmadı.
- `.claude/commands/design-review.md` ve `design-deslop.md` (plugin komutları) okundu, temiz; install.sh yalnız skill klasörünü kurduğu için **kurulmadı**. SKILL.md:317-318 bu komutlara atıf yapar; komut yoksa skill aynı işi satır içi yapar (SKILL.md:320).
- Depo hijyeni: upstream `website/.vercel/project.json` dosyasında kendi Vercel proje/org kimliklerini yayımlamış. Bizi etkilemez; vendor'a alınmadı.
- Çakışma: description "reviewing, auditing … product UI" ifadeleri `web-design-guidelines` ("audit design") ve `frontend-design` ile kısmen örtüşür; kapsamı panel/ürün UI ile sınırlı, pazarlama sayfasını açıkça dışlıyor. İzlenecek.
