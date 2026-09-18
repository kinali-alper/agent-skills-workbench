# ux-a11y-skills

Audited, evaluated [Claude Code](https://claude.com/claude-code) skills for **UX + accessibility review** —
with a security intake pipeline and a measurable test bench. Stack-agnostic: the same rules run on React, plain HTML,
ASP.NET Razor, Vue, Svelte or Framer output.

*Türkçe özet aşağıda.*

## What's here

| Folder | Contents |
|---|---|
| `skills/ux-a11y-review/` | Our skill: WCAG 2.2 AA (13 checks) + Nielsen heuristics (8 checks), four-state verdicts, `file:line` findings with a positive fix, mandatory keyboard pass and human TODO. Report-only. Triggers in Turkish (*"arayüzü denetle"*) to avoid colliding with the vendored English-triggered skills. |
| `skills/ux-a11y-review-workspace/` | Eval results (`RESULTS.md`, `grading.json` per run). |
| `vendor/` | 27 third-party skills, each pinned to a commit, with upstream `LICENSE` and a `REVIEW.md` security audit record. |
| `scripts/skill-audit.sh` | 8-point scan for any skill folder: scripts, hooks/`allowed-tools`, dangerous commands, injection phrases, hidden Unicode, external domains, size. Exit code is a gate. |
| `scripts/install.sh` | Syncs `skills/` + `vendor/` into `~/.claude/skills`. Refuses anything without `REVIEW.md`. |
| `scripts/publish-check.sh` | Pre-push leak scan (org names, machine paths, e-mails, ID numbers). |
| `evals/cases/broken-form/` | Test fixture: a Turkish school-registration form with 19 planted defects (13 WCAG + 6 Nielsen) in TSX, HTML and Razor, plus a clean twin as negative control. `expected.md` is the answer key: which tool caught what. |
| `playground/` | Vite app serving the fixture; Playwright + axe-core + Lighthouse. `npm run test:a11y`. |
| `docs/` | Standards (WCAG 2.2 / EN 301 549), skill-writing rules, reviewed-but-not-installed sources, history. |

## Why

- Automated tools are not enough. On the fixture, axe caught **4 of 13** WCAG defects and Lighthouse scored the broken page **84/100**.
  The 9 misses (placeholder-as-label, colour-only error, removed focus ring, `div` button, emoji-only button, 16 px target,
  no reduced-motion, headerless small table, "click here") are exactly what a review skill must cover.
- Skills are prompt files and can carry prompt injection. Nothing is installed here without an audit and a written review.
- "It works" needs evidence. The skill was evaluated with fresh, isolated subagents, with and without the skill, on three
  stacks and a negative control — see [RESULTS.md](skills/ux-a11y-review-workspace/RESULTS.md). Honest finding: the bare
  model already finds 18/19; the skill adds completeness, consistency, brevity and the mandatory browser/human steps.

## Install

```bash
git clone https://github.com/kinali-alper/ux-a11y-skills
cd ux-a11y-skills
bash scripts/install.sh          # → ~/.claude/skills (28 skills)
```
Then in Claude Code: `arayüzü denetle src/pages/Login.tsx` — or invoke `/ux-a11y-review`.

Requirements for the skill: `heuristic-evaluation`, `wq-accessibility`, `web-design-guidelines` (all vendored here).
Playground: Node 22, Chrome (Playwright uses `channel: 'chrome'`).

## Standards
WCAG 2.2 Level **AA** (EN 301 549 v4.1.1). WCAG 3.0 is a Working Draft and not referenced.

## License
MIT — see [LICENSE](LICENSE). Vendored skills keep their upstream licenses (MIT; frontend-design Apache-2.0) — see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

---

## Türkçe

**Ne:** Erişilebilirlik (WCAG 2.2 AA) ve kullanılabilirlik (Nielsen) denetimi için Claude Code skill'leri; güvenlik denetiminden
geçmiş 27 üçüncü taraf skill; ve "skill gerçekten çalışıyor mu?" sorusuna sayıyla cevap veren bir test tezgâhı.

**Neden Türkçe tetik:** Kurulu İngilizce skill'ler "accessibility audit" ifadesini paylaşıyor; üçüncüsü aynı kelimeyi kullansaydı
hangisinin tetikleneceği belirsiz olurdu. `arayüzü denetle`, `erişilebilirlik kontrolü`, `kullanılabilirlik incelemesi` hiçbir
kurulu skill'le çakışmaz.

**İlkeler**
1. Skill'ler yapıdan bağımsızdır; yapıya özgü reçeteler `references/` altında, yalnız gerektiğinde yüklenir.
2. Hiçbir üçüncü taraf skill denetimsiz kurulmaz: `skill-audit.sh` → SKILL.md okuma → `REVIEW.md` → `install.sh`.
3. Kanıtsız "iyi" denmez: axe + Lighthouse + klavye/ekran okuyucu; skill testleri taze, izole alt-ajanla.
4. Skill, kullanıcıları ve arayüz dilini projeden tespit eder; bulamazsa sorar. İçinde proje bilgisi yoktur.

Kurulum ve klasörler için yukarıdaki İngilizce bölüme bakın.
