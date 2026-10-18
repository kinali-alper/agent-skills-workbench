# agent-skills-workbench

Audited, pinned, evaluated [Claude Code](https://claude.com/claude-code) skills — with a security intake pipeline and a
measurable test bench. Two first-class review skills (both shipping as drafts) and 29 vendored skills
in six layers, each individually installable.

*Türkçe özet aşağıda.*

## Skills

| Skill | Status | What it does |
|---|---|---|
| [`ux-a11y-review`](skills/ux-a11y-review/SKILL.md) | **draft** — 3 eval iterations, 1 real page ([RESULTS](skills/ux-a11y-review-workspace/RESULTS.md)) | UX (Nielsen, 8 checks) + accessibility (WCAG 2.2 blind spots, 13 checks + a 36-criterion A/AA sweep reference) in one report. Four-state verdicts, `file:line` + positive fix, mandatory keyboard pass and human TODO. Report-only. Triggers in Turkish (*"arayüzü denetle"*) to avoid colliding with the English-triggered vendored skills. |
| [`visual-design-review`](skills/visual-design-review/SKILL.md) | **draft** — deterministic half measured (17 signals vs 0 on a fixture pair), model-side eval not run yet ([RESULTS](skills/visual-design-review-workspace/RESULTS.md)) | Visual craft in one report: scale and token discipline, hierarchy, surfaces, motion, micro-typography and the common "AI-made" signals. 18 countable signals via `scripts/visual-scan.py` (stdlib, report-only) plus a 12-row judgement list, each with a public source or an explicit `[öneri]` tag. Four-state verdicts, `file:line` + "instead", no beauty score. Step 4 needs a rendered page, so it runs only in a main session. |

## Vendored skills — six layers

Full table with upstream, pin, license, audit result and trigger phrases: [`vendor/MANIFEST.md`](vendor/MANIFEST.md) (generated).

| Layer | Skills | Role |
|---|---|---|
| 1 Review core | wq-accessibility · web-design-guidelines · heuristic-evaluation | Rule text and process `ux-a11y-review` orchestrates |
| 2 UX knowledge | ux-designer | 24 reference files (Nielsen, Laws of UX, forms, i18n…) behind conditional pointers |
| 3 Design direction | frontend-design · design-taste-frontend · high-end-visual-design · minimalist-ui · industrial-brutalist-ui · redesign-existing-projects · baseline-ui · interface-design | *Producing* visual design; input for `visual-design-review` |
| 4 Motion | motion-design · gsap-* (8) | Motion principles; GSAP only useful in GSAP projects |
| 5 Web quality | wq-seo · wq-performance · wq-core-web-vitals · wq-best-practices · wq-web-quality-audit | Lighthouse-family audits |
| 6 Process / skill writing | writing-for-agents · grill-me · to-spec | How this repo's own skills are written |

Every vendored skill is **pinned to an upstream commit and the pin is verified by blob hash**. Latest sweep 2026-10-16,
two-way (is our copy faithful to its pin, and has upstream moved past it): of the 24 vendors the API let us read,
**20 are byte-identical to their pin** and 4 differ only by an adaptation written down in their `REVIEW.md` —
ux-designer (`description`), web-design-guidelines (reads a pinned local copy of the rule list instead of fetching it at
run time), wq-accessibility and wq-best-practices (`name:` line). The other four `wq-*` carry the same one-line `name:`
edit but were rate-limited in this sweep. **No undocumented drift.** Upstream has moved past the pin for 4
(design-taste-frontend, minimalist-ui, redesign-existing-projects, ux-designer) — pinned on purpose; a bump means a
fresh audit, not a silent update. Re-run with [`scripts/pin-sweep.py`](scripts/pin-sweep.py). Each folder carries the
upstream `LICENSE` (28 MIT, 1 Apache-2.0) and a `REVIEW.md` security record. Where the audit flags example code as a false
positive, the exception lives in `AUDIT-ALLOW` with the reason in `REVIEW.md` — so **the audit's exit code is a real gate:
all 29 return 0, and the ten samples in [`evals/audit/`](evals/audit/) return exactly their expected codes** (`scripts/test-audit.sh`).
The audit is static; see [SECURITY.md](SECURITY.md) for what that does and does not mean. Every vendor file's sha256 is in
[`vendor/INTEGRITY.sha256`](vendor/INTEGRITY.sha256); `install.sh` refuses a vendor whose files do not match it. All of this
runs in CI on every push ([`gate.yml`](.github/workflows/gate.yml)).

## Install

```bash
git clone https://github.com/kinali-alper/agent-skills-workbench
cd agent-skills-workbench
bash scripts/install.sh --only ux-a11y-review --with-deps     # the skill + the three it declares in metadata.requires
# everything:  bash scripts/install.sh        (--dry-run to preview; existing folders are backed up, not overwritten; --prune-backups 2)
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
| `vendor/` | 29 third-party skills + `MANIFEST.md` |
| `scripts/` | `skill-audit.sh` (8-point scan, gating exit code, `AUDIT-ALLOW` exceptions) · `install.sh` (`--only`, `--dry-run`, backup) · `publish-check.sh` (pre-push leak scan) · `gen-manifest.sh` |
| `evals/cases/` | Fixtures: a Turkish school-registration form with 19 planted defects in TSX/HTML/Razor + a clean twin |
| `playground/` | Vite app serving the fixtures; Playwright + axe-core + Lighthouse |
| `docs/` | Standards, skill-writing rules, reviewed-but-not-installed sources, history, [roadmap](docs/roadmap.md), [pin sweep](docs/pin-sweep.md) |

Standards: WCAG 2.2 Level **AA** (EN 301 549 v4.1.1). License: MIT — see [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

---

## Türkçe

**Ne:** Güvenlik denetiminden geçmiş, kaynak commit'ine sabitlenmiş ve ölçülmüş Claude Code skill'leri için bir **tezgâh**.
Kendi skill'lerimiz: `ux-a11y-review` (taslak — kullanılabilirlik + erişilebilirlik tek raporda) ve `visual-design-review` (hazırlanıyor —
tutarlılık, hiyerarşi, klişe, metin; güzellik puanı **vermez**). 29 üçüncü taraf skill altı katmanda; `install.sh --only <ad>` ile tek tek kurulur.

**İlkeler**
1. Skill'ler yapıdan ve projeden bağımsızdır; yapıya özgü reçeteler `references/` altında, yalnız gerektiğinde yüklenir. Kullanıcıları ve dili projeden tespit eder, bulamazsa sorar.
2. Hiçbir üçüncü taraf skill denetimsiz kurulmaz: `skill-audit.sh` → SKILL.md okuma → `REVIEW.md` + upstream `LICENSE` + pin → `install.sh`. Yanlış alarmlar `AUDIT-ALLOW`'da gerekçeli; çıkış kodu gerçek kapı.
3. Kanıtsız "iyi" denmez: taze izole alt-ajanla skill'li/skill'siz koşu, negatif kontrol, gerçek sayfa.
4. Neden Türkçe tetik: kurulu İngilizce skill'ler "accessibility audit" ifadesini paylaşıyor; `arayüzü denetle`, `erişilebilirlik kontrolü`, `kullanılabilirlik incelemesi` hiçbiriyle çakışmaz.
