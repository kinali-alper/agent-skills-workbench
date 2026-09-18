# İncelenen, kurulmayan kaynaklar

| Kaynak | Tarih | Karar | Neden |
|---|---|---|---|
| **obra/superpowers** (b36e082, 2026-08-12, 288k★) | 2026-09-18 | **Kurulmadı** | SessionStart hook her oturuma `<EXTREMELY_IMPORTANT>` "skill çağırmak ZORUNDASIN" metni enjekte eder → tüm skill tetiklemesini etkiler, ilke 2 (hook = kritik) ile çatışır. `brainstorming/scripts/server.cjs` yerel Node sunucusu; tek dış istek primeradiant.com logo görseli (telemetri; `SUPERPOWERS_DISABLE_TELEMETRY=1`). 20+ betik. Kötü niyet yok; UI/UX değil, mühendislik süreci. Okunacak: `writing-skills`, `verification-before-completion`. |
| **emilkowalski performance-cheatsheet.md** | 2026-09-18 | Referans | 7 satırlık animasyon performans tablosu; gsap-performance + motion-design + Vercel guidelines zaten kapsıyor. Kendi skill'e A10 yanına eklenmesi fixture kanıtı ister. |
| **AccessLint/skills** | 2026-09-18 | Ertelendi | Plugin + tarayıcı MCP gerekir; playground axe aynı işi görür; eşsiz parçası `accessibility-fix`. |
| **Owl-Listener designer-skills** (heuristic-evaluation dışı) | 2026-09-18 | Gerekirse tek tek | Plugin komutlarına bağlı olmayan skill'ler aynı yolla alınabilir (design-research, design-ops handoff). |

## skill-creator — kullanılmayan parçalar (sırada)
- `scripts/improve_description.py` — ux-a11y-review Türkçe tetiklerinin doğru ateşlenip ateşlenmediğini ölçer.
- `eval-viewer/generate_review.py` — iteration raporlarını skill'li/skill'siz yan yana HTML'de gösterir (kullanıcının görebileceği çıktı).
