# Vendor manifest

Üretildi: `scripts/gen-manifest.py` — elle düzenleme; kaynak `vendor/*/REVIEW.md`, `SKILL.md`, `AUDIT-ALLOW`.

Katmanlar: **1** inceleme çekirdeği · **2** UX bilgi tabanı · **3** tasarım yönü (üretim) · **4** hareket · **5** web kalitesi · **6** süreç / skill yazımı. Katman, skill'in bu depodaki rolünü söyler; hepsi `install.sh --only <ad>` ile tek tek kurulabilir.

| Skill | Katman | Upstream | Pin | Lisans | Audit | SKILL.md satır | Tetik (description) |
|---|---|---|---|---|---|---|---|
| heuristic-evaluation | 1 · inceleme çekirdeği | Owl-Listener/designer-skills | `9a6930c` 2026-09-05 | MIT | TEMİZ | 41 | Run an expert review against Nielsen's heuristics and domain criteria,… |
| web-design-guidelines | 1 · inceleme çekirdeği | vercel-labs/agent-skills | `063bee9` 2026-08-28 | MIT | TEMİZ (1 istisna) | 39 | review my UI, check accessibility, audit design, review UX |
| wq-accessibility | 1 · inceleme çekirdeği | addyosmani/web-quality-skills | `afa8da9` 2026-08-24 | MIT | TEMİZ (3 istisna) | 464 | improve accessibility, a11y audit, WCAG compliance, screen reader support |
| ux-designer | 2 · UX bilgi tabanı | szilu/ux-designer-skill | `da9e9d0` 2026-08-14 | MIT | TEMİZ (5 istisna) | 322 | UX/UI design principles for building and critiquing interfaces. Use fo… |
| design-taste-frontend | 3 · tasarım yönü (üretim) | Leonxlnx/taste-skill | `3c7017d` 2026-05-26 | MIT | TEMİZ (1 istisna) | 1206 | Anti-slop frontend skill for landing pages, portfolios, and redesigns.… |
| frontend-design | 3 · tasarım yönü (üretim) | anthropics/claude-code | `dbdd79c` 2026-09-02 | Apache-2.0 | TEMİZ | 71 | Guidance for distinctive, intentional visual design when building new … |
| high-end-visual-design | 3 · tasarım yönü (üretim) | Leonxlnx/taste-skill | `3206dd4` 2026-03-20 | MIT | TEMİZ | 98 | Teaches the AI to design like a high-end agency. Defines the exact fon… |
| industrial-brutalist-ui | 3 · tasarım yönü (üretim) | Leonxlnx/taste-skill | `3206dd4` 2026-03-20 | MIT | TEMİZ | 92 | Raw mechanical interfaces fusing Swiss typographic print with military… |
| minimalist-ui | 3 · tasarım yönü (üretim) | Leonxlnx/taste-skill | `3206dd4` 2026-03-20 | MIT | TEMİZ | 85 | Clean editorial-style interfaces. Warm monochrome palette, typographic… |
| redesign-existing-projects | 3 · tasarım yönü (üretim) | Leonxlnx/taste-skill | `3206dd4` 2026-03-20 | MIT | TEMİZ | 178 | Upgrades existing websites and apps to premium quality. Audits current… |
| gsap-core | 4 · hareket | greensock/gsap-skills | `96c4b01` 2026-03-09 | MIT | TEMİZ | 254 | Official GSAP skill for the core API — gsap.to(), from(), fromTo(), ea… |
| gsap-frameworks | 4 · hareket | greensock/gsap-skills | `7f8b61e` 2026-04-10 | MIT | TEMİZ | 266 | Official GSAP skill for Vue, Svelte, and other non-React frameworks — … |
| gsap-performance | 4 · hareket | greensock/gsap-skills | `96c4b01` 2026-03-09 | MIT | TEMİZ | 79 | Official GSAP skill for performance — prefer transforms, avoid layout … |
| gsap-plugins | 4 · hareket | greensock/gsap-skills | `5b909b9` 2026-04-21 | MIT | TEMİZ | 433 | Official GSAP skill for GSAP plugins — registration, ScrollToPlugin, S… |
| gsap-react | 4 · hareket | greensock/gsap-skills | `96c4b01` 2026-03-09 | MIT | TEMİZ | 136 | Official GSAP skill for React — useGSAP hook, refs, gsap.context(), cl… |
| gsap-scrolltrigger | 4 · hareket | greensock/gsap-skills | `96c4b01` 2026-03-09 | MIT | TEMİZ | 296 | Official GSAP skill for ScrollTrigger — scroll-linked animations, pinn… |
| gsap-timeline | 4 · hareket | greensock/gsap-skills | `96c4b01` 2026-03-09 | MIT | TEMİZ | 107 | Official GSAP skill for timelines — gsap.timeline(), position paramete… |
| gsap-utils | 4 · hareket | greensock/gsap-skills | `96c4b01` 2026-03-09 | MIT | TEMİZ | 284 | Official GSAP skill for gsap.utils — clamp, mapRange, normalize, inter… |
| motion-design | 4 · hareket | LottieFiles/motion-design-skill | `b6606e1` 2026-03-12 | MIT | TEMİZ | 315 | Applies motion design principles to create emotionally-driven, technic… |
| wq-best-practices | 5 · web kalitesi | addyosmani/web-quality-skills | `afa8da9` 2026-08-24 | MIT | TEMİZ (4 istisna) | 480 | apply best practices, security audit, modernize code, code quality review |
| wq-core-web-vitals | 5 · web kalitesi | addyosmani/web-quality-skills | `afa8da9` 2026-08-24 | MIT | TEMİZ (2 istisna) | 228 | improve Core Web Vitals, fix LCP, reduce CLS, optimize INP |
| wq-performance | 5 · web kalitesi | addyosmani/web-quality-skills | `afa8da9` 2026-08-24 | MIT | TEMİZ (2 istisna) | 399 | speed up my site, optimize performance, reduce load time, fix slow loading |
| wq-seo | 5 · web kalitesi | addyosmani/web-quality-skills | `afa8da9` 2026-08-24 | MIT | TEMİZ (3 istisna) | 409 | improve SEO, optimize for search, fix meta tags, add structured data |
| wq-web-quality-audit | 5 · web kalitesi | addyosmani/web-quality-skills | `afa8da9` 2026-08-24 | MIT | TEMİZ (1 istisna) | 209 | audit my site, review web quality, run lighthouse audit, check page quality |
| grill-me | 6 · süreç / skill yazımı | mattpocock/skills | `c55ee46` 2026-09 | MIT | TEMİZ | 7 | A relentless interview to sharpen a plan or design. |
| to-spec | 6 · süreç / skill yazımı | mattpocock/skills | `c55ee46` 2026-09 | MIT | TEMİZ | 75 | Turn the current conversation into a spec and publish it to the projec… |
| writing-for-agents | 6 · süreç / skill yazımı | mattpocock/skills | `c55ee46` 2026-09 | MIT | TEMİZ | 81 | Writing documents for agents. Use when creating or editing skills, or … |

Toplam 27 skill · pinli 27 · audit TEMİZ 27.
