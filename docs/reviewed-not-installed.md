# İncelenen, kurulmayan kaynaklar

| Kaynak | Tarih | Karar | Neden |
|---|---|---|---|
| **obra/superpowers** (b36e082, 2026-08-12, 288k★) | 2026-09-18 | **Kurulmadı** | SessionStart hook her oturuma `<EXTREMELY_IMPORTANT>` "skill çağırmak ZORUNDASIN" metni enjekte eder → tüm skill tetiklemesini etkiler, ilke 2 (hook = kritik) ile çatışır. `brainstorming/scripts/server.cjs` yerel Node sunucusu; tek dış istek primeradiant.com logo görseli (telemetri; `SUPERPOWERS_DISABLE_TELEMETRY=1`). 20+ betik. Kötü niyet yok; UI/UX değil, mühendislik süreci. Okunacak: `writing-skills`, `verification-before-completion`. |
| **emilkowalski performance-cheatsheet.md** | 2026-09-18 | Referans | 7 satırlık animasyon performans tablosu; gsap-performance + motion-design + Vercel guidelines zaten kapsıyor. Kendi skill'e A10 yanına eklenmesi fixture kanıtı ister. |
| **AccessLint/skills** | 2026-09-21 | **Önce doğrula** | 21 Eylül incelemesi "`accessibility-scan` MCP gerektirmez, CLI'a shell-out" diyor — 18 Eylül ertelememizle çelişiyor. Klon + SKILL.md okunmadan karar yok. `benchmark/` dizini bağımsız kıyas seti adayı. |
| **Owl-Listener designer-skills** (heuristic-evaluation dışı) | 2026-09-18 | Gerekirse tek tek | Plugin komutlarına bağlı olmayan skill'ler aynı yolla alınabilir (design-research, design-ops handoff). |

## skill-creator — kullanılmayan parçalar (sırada)
- `scripts/improve_description.py` — ux-a11y-review Türkçe tetiklerinin doğru ateşlenip ateşlenmediğini ölçer.
- `eval-viewer/generate_review.py` — iteration raporlarını skill'li/skill'siz yan yana HTML'de gösterir (kullanıcının görebileceği çıktı).
| **pixeljury** | 2026-09-21 | **Önce doğrula** | 21 Eylül incelemesi öneriyor (kontrast/taşma/hedef ölçümü, `--provider mock`). Bu projede ilk kez geçiyor; tam intake (audit → REVIEW) olmadan hüküm yok. |
| **emilkowalski `review-animations`** | 2026-09-21 | Hızlı intake sırada | 18 Eylül'de temiz markdown olarak görüldü; ux-a11y-review'un hareket boşluğunu (A10 tek satır) kapatır. |
| **Impeccable** (pbakaus, f2c7051) | 2026-09-21 | Kurulmadı — kurallar ödünç | Rust ikilileri, tarayıcı-enjekte JS, ajan TOML'ları, `.impeccable/` durum; bir çalışma zamanı. 61 kurallı klişe dedektörünün kural kaynağı `visual-design-review` için okunacak; sırası "önce niteliksel eleştiri, sonra ölçüm" benimsenecek. |
| **Owl-Listener `visual-critique`** (7 skill) | 2026-09-21 | Intake sırada (tetiklenmez-yalnız-okunur) | `visual-design-review` için referans; 7 description "critique a rendered screen" ile çakışır → `disable-model-invocation: true` ile alınacak. |
