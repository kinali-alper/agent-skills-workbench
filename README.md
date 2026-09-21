# agent-skills-workbench

Audited, pinned, evaluated [Claude Code](https://claude.com/claude-code) skills — with a security intake pipeline and a
measurable test bench. Two first-class review skills (one shipping as a draft, one in preparation) and 27 vendored skills
in six layers, each individually installable.

*Türkçe özet aşağıda.*

## Skills

| Skill | Status | What it does |
|---|---|---|
| [`ux-a11y-review`](skills/ux-a11y-review/SKILL.md) | **draft** — 3 eval iterations, 1 real page ([RESULTS](skills/ux-a11y-review-workspace/RESULTS.md)) | UX (Nielsen, 8 checks) + accessibility (WCAG 2.2 blind spots, 13 checks + a 36-criterion A/AA sweep reference) in one report. Four-state verdicts, `file:line` + positive fix, mandatory keyboard pass and human TODO. Report-only. Triggers in Turkish (*"arayüzü denetle"*) to avoid colliding with the English-triggered vendored skills. |
| `visual-design-review` | planned | Token discipline, hierarchy, AI-cliché detection, copy — findings, not a beauty score. Needs a rendered page. |

## Vendored skills — six layers

Full table with upstream, pin, license, audit result and trigger phrases: [`vendor/MANIFEST.md`](vendor/MANIFEST.md) (generated).

| Layer | Skills | Role |
|---|---|---|
| 1 Review core | wq-accessibility · web-design-guidelines · heuristic-evaluation | Rule text and process `ux-a11y-review` orchestrates |
| 2 UX knowledge | ux-designer | 24 reference files (Nielsen, Laws of UX, forms, i18n…) behind conditional pointers |
| 3 Design direction | frontend-design · design-taste-frontend · high-end-visual-design · minimalist-ui · industrial-brutalist-ui · redesign-existing-projects | *Producing* visual design; input for `visual-design-review` |
| 4 Motion | motion-design · gsap-* (8) | Motion principles; GSAP only useful in GSAP projects |
| 5 Web quality | wq-seo · wq-performance · wq-core-web-vitals · wq-best-practices · wq-web-quality-audit | Lighthouse-family audits |
| 6 Process / skill writing | writing-for-agents · grill-me · to-spec | How this repo's own skills are written |

Every vendored skill is **pinned to the upstream commit whose blob matches ours** (verified by hash, 2026-09-21), carries the
upstream `LICENSE` (26 MIT, 1 Apache-2.0), and has a `REVIEW.md` security record. Where the audit flags example code as a false
positive, the exception lives in `AUDIT-ALLOW` with the reason in `REVIEW.md` — so **the audit's exit code is a real gate:
all 27 return 0, and a planted malicious sample returns 2.**

## Install

```bash
git clone https://github.com/kinali-alper/agent-skills-workbench
cd agent-skills-workbench
bash scripts/install.sh --only ux-a11y-review --only wq-accessibility --only web-design-guidelines --only heuristic-evaluation
# or everything:  bash scripts/install.sh        (--dry-run to preview; existing folders are backed up, not overwritten)
```
Then in Claude Code: `arayüzü denetle src/pages/Login.tsx`, or `/ux-a11y-review`.

## Why

- Automated tools are not enough: on the fixture, axe caught **4 of 13** WCAG defects and Lighthouse scored the broken page **84/100**.
- Skills are prompt files and can carry prompt injection. Nothing is installed here without an audit and a written review ([SECURITY](SECURITY.md)).
- "It works" needs evidence: fresh isolated subagents, with and without the skill, three stacks, a negative control, one real
  public page. Honest finding: the bare model already finds 18/19; the skill adds completeness, consistency, brevity and the
  mandatory browser step — which on the real page produced the severity-4 finding.

## Repo layout

| Folder | Contents |
|---|---|
| `skills/<name>/` | Our skills; `evals/evals.json` per skill; `<name>-workspace/` holds graded results |
| `vendor/` | 27 third-party skills + `MANIFEST.md` |
| `scripts/` | `skill-audit.sh` (8-point scan, gating exit code, `AUDIT-ALLOW` exceptions) · `install.sh` (`--only`, `--dry-run`, backup) · `publish-check.sh` (pre-push leak scan) · `gen-manifest.sh` |
| `evals/cases/` | Fixtures: a Turkish school-registration form with 19 planted defects in TSX/HTML/Razor + a clean twin |
| `playground/` | Vite app serving the fixtures; Playwright + axe-core + Lighthouse |
| `docs/` | Standards, skill-writing rules, reviewed-but-not-installed sources, history |

Standards: WCAG 2.2 Level **AA** (EN 301 549 v4.1.1). License: MIT — see [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

---

## Türkçe

**Ne:** Güvenlik denetiminden geçmiş, kaynak commit'ine sabitlenmiş ve ölçülmüş Claude Code skill'leri için bir **tezgâh**.
Kendi skill'lerimiz: `ux-a11y-review` (taslak — kullanılabilirlik + erişilebilirlik tek raporda) ve `visual-design-review` (hazırlanıyor —
tutarlılık, hiyerarşi, klişe, metin; güzellik puanı **vermez**). 27 üçüncü taraf skill altı katmanda; `install.sh --only <ad>` ile tek tek kurulur.

**İlkeler**
1. Skill'ler yapıdan ve projeden bağımsızdır; yapıya özgü reçeteler `references/` altında, yalnız gerektiğinde yüklenir. Kullanıcıları ve dili projeden tespit eder, bulamazsa sorar.
2. Hiçbir üçüncü taraf skill denetimsiz kurulmaz: `skill-audit.sh` → SKILL.md okuma → `REVIEW.md` + upstream `LICENSE` + pin → `install.sh`. Yanlış alarmlar `AUDIT-ALLOW`'da gerekçeli; çıkış kodu gerçek kapı.
3. Kanıtsız "iyi" denmez: taze izole alt-ajanla skill'li/skill'siz koşu, negatif kontrol, gerçek sayfa.
4. Neden Türkçe tetik: kurulu İngilizce skill'ler "accessibility audit" ifadesini paylaşıyor; `arayüzü denetle`, `erişilebilirlik kontrolü`, `kullanılabilirlik incelemesi` hiçbiriyle çakışmaz.
