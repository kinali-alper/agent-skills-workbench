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

## Corpus-named, not yet opened (2026-10-16)

Named by a 2026 research round on "skills and methods that make AI assistants produce non-generic UI" (14 answers;
its measured claims come from a single model family and are unverified). **Nothing below has been opened by us**, so
none of it has a verdict — they are intake candidates and declines-with-a-reason, nothing more.

| Source | Why it is on the list | What the corpus says | Next action |
|---|---|---|---|
| `funboy322/avoid-ai-design` | Catalogue of the *second wave* of AI tells (cream + serif + terracotta, near-black + acid accent) plus a zero-dependency scanner | "including the 'tasteful' defaults that replaced the purple gradient" | clone + audit; likely borrow the tell list |
| `nutlope/hallmark` (Together AI) | Picks a page structure per brief, 21 themes, 57 "slop gates", self-critique; treats `design.md` as data | 558 lines / 65.9 KB — over the 500-line guidance; no published eval | read only; borrow ideas |
| Google Labs `DESIGN.md` spec (Apache-2.0) | Token + rationale file in the repo root, as grounding for agents | "open-source, maintained by Google Labs" | adopt as a *format*, not a skill |
| `amzn/style-dictionary` + W3C DTCG token format | Token pipeline: one source → CSS/JS/JSON | tool, not a skill | read; would support an eval harness |
| `garris/backstopjs` | Visual regression — would automate "deviation from the approved mock" | tool, not a skill | read |
| `abi/screenshot-to-code` | Shows image-conditioned generation and its sameness risk | tool, not a skill | read |
| `superdesigndev/superdesign-skill` | **Decline:** drives a hosted service, `npx --yes …@latest` (effectively auto-updating), source files leave the machine | "MUST pass relevant source files via --context-file" | record the decline; our audit step 3b now flags this shape |
| `nextlevelbuilder/ui-ux-pro-max-skill` | **Decline:** runs a local Python style DB, conflicts with anti-slop rules (Inter, purple), worst result in the one third-party detector run | "79 searchable styles, 192 product palettes" | record the decline; borrow only the product-type → palette idea |
| `emilkowalski/skills` (`emil-design-eng`) | Motion craft rules with concrete easing tokens; the repo was already reviewed for `review-animations` | quoted for stagger 30–80 ms and `cubic-bezier(0.23,1,0.32,1)` | fold into the queued `review-animations` intake |

