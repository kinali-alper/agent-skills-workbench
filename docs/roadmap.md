# Roadmap — gates, not wishes

State on 2026-10-16. Every item says what evidence closes it, what it costs, and who decides. Nothing here is started.
Declined ideas are listed at the end so they are not re-proposed.

CI is green on `187a3e2` (run 2026-10-08) and the 2026-10-06 tooling fixes are in `main`. **The working tree is not
clean**: a parallel session on 2026-10-16 fixed a real bug in `scripts/skill-audit.sh` (the awk program that reads the
frontmatter block carried literal newlines from an earlier substitution, so step 2 silently never fired —
`evals/audit/08-allowed-tools-frontmatter` was added as the proof sample, expected exit 2), vendored two new skills
(`baseline-ui`, `interface-design`) and reworked `web-design-guidelines` (snapshot → `command.md`, AUDIT-ALLOW
dropped). Those changes, plus this roadmap, are uncommitted. **Commit them before starting anything below.**

Sources marked **[corpus]** come from a 2026 web-design research round run in a separate private repo
(14 answers to a prompt on "skills and methods that make AI assistants produce non-generic UI"). Only the answer read
end to end is cited, by row id; its measured claims are **single-model-family and unverified** — treat them as leads.

---

## 0. Repo hygiene — two minutes, only the owner can do it

GitHub still shows the description as the literal string `Copyright (c) 2026 ` and **no topics**. Flagged since
September. Paste-ready:

- **Description:** `Audited, pinned and evaluated Claude Code skills — security intake pipeline plus a measurable eval bench.`
- **Topics:** `claude-code` · `agent-skills` · `accessibility` · `wcag` · `ux-review` · `security-audit` · `evals`

## 1. `ux-a11y-review` — two open gates, then the draft/stable call

**Both gates closed on 2026-10-16.** What remains is the `draft → stable` call, which is the user's. Both were written in [RESULTS "Next gates"](../skills/ux-a11y-review-workspace/RESULTS.md).

| Gate | What closes it | Cost | Decides |
|---|---|---|---|
| ~~**G1 · Trigger re-run for path-less queries**~~ | **CLOSED 2026-10-16 — 6/6 on `any_clean`, `self_read` 0/18**: the artifact was the method, not the description. Pre-registered rule now met (positives 9/10, negatives 10/10). Actual cost **$20.54**, 3× the ~$7 estimate (13/18 runs hit the 6-turn ceiling). | — | done |
| ~~**G2 · Unseen real page**~~ | **CLOSED 2026-10-16** — an unnamed Turkish municipality home page, read-only, real Tab presses logged via `focusin`; 8 findings, A3/A9 left `doğrulanamaz` because the pane does not paint. The browser step proved its value: 13 consecutive nameless Tab stops, and `outline: none` 14 vs `:focus-visible` 4. | — | done |

**Status convention when these close:** keep the repo's own three-way wording per claim — `doğrulanan` (measured),
`kâğıt üstünde` (written but never exercised), `sağlanmayan` (known gap). Today's honest split:

- *doğrulanan*: finding power on 3 stacks ×3 conditions (it-4), four-state verdicts, zero false positives on the clean
  control (4/4), in-browser focus-trap reproduction on W3C BAD (17/19), description does not over-trigger (0 false
  triggers in 30 runs).
- *kâğıt üstünde*: axe/Playwright pairing in step 4, the 36-criterion sweep reference (never the deciding evidence in
  any run), `references/stack-razor.md` beyond one fixture.
- *sağlanmayan*: screen-reader checks, 200 % zoom / 320 px reflow, any human-user task — all three are in the skill's
  human-TODO block by design.

`draft → stable` remains the user's call; G1 + G2 are the evidence it should rest on.

## 2. `visual-design-review` — **built 2026-10-16, draft**

Written and shipping as a draft: router SKILL.md + `references/isaretler.md` (G1–G12 with public sources) +
`scripts/visual-scan.py` (18 signals, stdlib) + fixture pair (**17 vs 0**) + `evals/evals.json` (4 evals, not yet run)
+ [workspace RESULTS](../skills/visual-design-review-workspace/RESULTS.md). The cross-repo scanner question below was
decided by porting: the public copy is project-agnostic (`[zevk]` labels reclassified, personal references removed) and
the same fix was applied to both copies to stop drift. **Remaining gate: the isolated with/without model-side eval** —
until it passes, no claim that the skill improves a model's review.

### How it was scoped (kept for the record)

Planned since September. The research round supplies what was missing — a rule source and an eval method:

| Piece | Where it comes from | Note |
|---|---|---|
| Per-surface **mode** (persuade / operate / read / experience) | Impeccable's router, **[corpus D1-1, D4-4]** | Already decided as "borrow rules only" in [`reviewed-not-installed.md`](reviewed-not-installed.md); unchanged |
| **NEVER + INSTEAD** pairing | **[corpus D3-8]** — the only design-skill change with a published significance test (21/28, p = 0.006) | The PR is **open, not merged** (checked 2026-10-16); cite it as a proposal, not an Anthropic decision |
| Second-wave cliché list (cream + serif + terracotta, near-black + acid accent) | `funboy322/avoid-ai-design` **[corpus D1-8, D4-7]** | Not yet opened by us → intake first |
| Dashboard guardrails (85 lines, MUST/SHOULD/NEVER) | `baseline-ui` — **already vendored 2026-10-16**, layer 3 | Its rules can be cited directly instead of re-derived |
| Deterministic signals (distinct font sizes, neutral chroma, spacing conformity, `transition: all`, >400 ms transitions, layout-animating properties, `backdrop-filter`, gradient interpolation space, `font-display`) | prompt B5 / C5 of the same round | **See the cross-repo question below** |
| Eval method | **[corpus D2-1]**: 50 prompts × 2 variants, screenshots, blind judge on 5 criteria, sign test | Same shape as this repo's existing eval bench |

**Honest limitation to write into the skill from day one:** it needs a *rendered* page, and the in-app browser does not
paint on this machine — the workaround is a headless Edge screenshot, which means the visual step runs **only in a main
session**, exactly like `ux-a11y-review`'s step 4. Subagents cannot do it.

**Cross-repo question (not a decision to make alone):** a static scanner covering ~80 % of this skill's deterministic
half already exists — `tasarim_tara.py`, written 2026-10-16 in the user's private knowledge repo (pure stdlib,
report-only, exit 0/2, validated against a slop/clean fixture pair: 16 flags vs 0). Options: (a) port it here as the
skill's `scripts/`, re-labelled in English, with its fixture pair; (b) keep two scanners and let them drift; (c) keep
the scanner private and have this skill call it only when present. (a) is the only one that keeps a single source of
truth, but it moves Turkish-labelled work from a private repo into a public one, so the user decides.

## 3. Intake queue — re-ordered, with the corpus's reasons to decline

Every row still goes through the existing pipeline: `skill-audit.sh` → read every file by hand → `REVIEW.md` + upstream
`LICENSE` → `gen-manifest.sh` (MANIFEST + INTEGRITY) → `install.sh`. **A corpus mention is not a shortcut**; nothing
below has been opened by us yet except where noted.

| Candidate | Why | First action | Expected verdict |
|---|---|---|---|
| ~~`ibelick/ui-skills` → `baseline-ui`~~ | **Done 2026-10-16** — vendored (commit `3434a76`, MIT, 85 lines, audit clean with one reading-link exception) and installed **[corpus D1-3]** | — | **adopted** |
| ~~`Dammyjay93/interface-design`~~ | **Done 2026-10-16** — vendored (commit `2f9be32`, MIT, 320 lines, audit clean); corpus named it in 3 answers | — | **adopted** |
| `funboy322/avoid-ai-design` | second-wave tell catalogue + optional zero-dependency scanner **[corpus D1-8]** | clone + audit | **borrow ideas** |
| `emilkowalski/review-animations` | already queued since 21 Sep; closes `ux-a11y-review`'s motion gap (A10 is one line) | quick intake | **adopt or borrow** |
| `AccessLint/skills` | queued since 21 Sep with a contradiction to resolve; its `benchmark/` is an independent comparison set | clone + read `SKILL.md` | unknown — verify first |
| `pixeljury` | contrast/overflow/target measurement, `--provider mock` | full intake | unknown |
| Owl-Listener `visual-critique` (7 skills) | reference for `visual-design-review`; 7 descriptions all say "critique a rendered screen" → must come in with `disable-model-invocation: true` | intake | **reference only** |
| `nutlope/hallmark` | structure-per-brief + 57 slop gates; **558 lines / 65.9 KB**, over the 500-line guidance; no published eval **[corpus D1-2, D2-7]** | read only | **borrow ideas** |
| Google `DESIGN.md` spec (Apache-2.0) | token + rationale file in the repo root; gives agents grounding **[corpus D1-5]** | read spec | **adopt as a format**, not a skill |
| `superdesigndev/superdesign-skill` | **decline**: `npx --yes @latest` (effectively auto-updating) and source files leave the machine **[corpus D5-6]** | record the reason | **avoid** |
| `nextlevelbuilder/ui-ux-pro-max-skill` | **decline**: runs local Python over a style DB, conflicts with anti-slop rules (Inter, purple), worst result in the one third-party detector run **[corpus D2-6]** | record the reason | **avoid** (borrow the product-type → palette idea only) |
| `pbakaus/impeccable` | unchanged from 21 Sep ("rules only"): downloads a binary on first run, opt-out telemetry **[corpus D5-7]** | no change | **rules only** |

Also name in `reviewed-not-installed.md`, as *corpus-named, not yet opened*: `garris/backstopjs` (visual regression),
`amzn/style-dictionary` + W3C DTCG (token pipeline), `abi/screenshot-to-code`. These are tools, not skills; they would
support an eval harness rather than ship as skills.

## 4. Intake-pipeline hardening the corpus justifies

`skill-audit.sh` already flags scripts, `allowed-tools`/`hooks`, dangerous commands, EN+TR injection phrases, hidden
HTML comments, invisible Unicode, unknown domains and telemetry. Two patterns seen in the corpus are **not** yet checks:

1. **Unpinned auto-updating invocation**: `npx --yes <pkg>@latest`, `uvx`, `pipx run` without a version **[corpus D5-6]**.
2. **Runtime binary download**: a skill that fetches an executable on first run into a dot-directory **[corpus D5-7]**.

**Both shipped on 2026-10-16** as audit step 3b (severity UYARI), with corpus samples `09-unpinned-latest-cli` and
`10-runtime-binary-download` (expected rc 1 each). 29/29 vendors still return 0; one real exception documented
(`design-taste-frontend` documents `npx shadcn@latest` for the reader → file:line `AUDIT-ALLOW` + REVIEW row). While
doing it, two latent problems were fixed: our own `REVIEW.md`/`AUDIT-ALLOW` were scanned as if they were skill content
(they are never installed), and grep's `--exclude` **widens** the file set in Git Bash when combined with `--include`
(it pulled `LICENSE.txt` into the URL scan and invented an `apache.org` finding) → replaced with a `drop_meta` filter.

Supporting evidence for the posture, if ever needed in `SECURITY.md`: 13.4 % of 3,984 marketplace skills carried at
least one critical finding (Snyk) and an academic crawl of 42,447 skills found 26.1 % with a vulnerability
**[corpus D5-1, D5-2]** — both snippet-level in the corpus, so verify at source before quoting.

## 5. Vendor maintenance

- **Pin freshness, verified 2026-10-16:** `vendor/frontend-design/SKILL.md` blob `a533345…` is **byte-identical to
  upstream HEAD** (`anthropics/claude-code`, last touched `dbdd79c`, 2026-09-02). No drift. The corpus claim that
  "frontend-design was rewritten and the blacklist replaced" refers to **PR #210, which is open and unmerged**
  (checked today) — our pin and `REVIEW.md` need no change, and the claim should be recorded as *proposal, not release*.
- **Done 2026-10-16:** the full two-way sweep ran for all 29 ([`pin-sweep.md`](pin-sweep.md)) — 20 faithful,
  4 documented adaptations, **0 undocumented drift**, 4 where upstream moved past the pin, 5 rate-limited.
  It also corrected a false record in all six `wq-*` REVIEWs (`name` was changed, not kept).
- **Open:** decide whether to bump the four moved pins (design-taste-frontend, minimalist-ui,
  redesign-existing-projects, ux-designer). A bump = full intake again; three of the four share one upstream repo.
  Re-check the 5 rate-limited rows with an authenticated token.

## 6. Measurement tooling

`trigger_eval.py` (Windows-safe, two metrics, per-worker project isolation) has now produced one full measurement and
is the only runner we have for description triggering. Promote it from workspace evidence to `scripts/` **only if**
`visual-design-review` will also be trigger-tested; until then it stays where the evidence that produced it lives.

A second grader for iteration-4 and `docs/skill-checklist.md` (from the research round's §8) remain queued from
September; neither blocks anything.

## Declined — do not re-propose (recorded 2026-09-21)

TypeScript CLI rewrite · sandboxed execution of skills · a skill registry · a dashboard · SARIF output · a semantic
(model-based) injection classifier. The 2026 corpus raised none of these with new evidence.

---

## Türkçe özet

- **Sahibi yapacak (2 dakika):** GitHub açıklaması hâlâ `Copyright (c) 2026 ` yazıyor, konu etiketi yok. Hazır metin §0'da.
- **`ux-a11y-review`** için iki kapı kaldı: (G1) yol vermeyen tetik sorgularını komut dosyası proje **dışında** olacak
  şekilde yeniden koşmak (~$8) ve (G2) **görülmemiş** bir gerçek sayfayı tarayıcılı oturumda denetlemek. `draft → stable`
  kararı bu ikisine dayanmalı; bugünkü dürüst bölüm "doğrulanan / kâğıt üstünde / sağlanmayan" diye §1'de yazılı.
- **`visual-design-review`** eylül'den beri yalnız README satırı; araştırma turu eksik olan kural kaynağını ve ölçüm
  yöntemini getirdi. Dikkat: render edilmiş sayfa gerektiriyor, bu makinede yalnız headless ekran görüntüsüyle ve
  **ana oturumda** çalışır. Açık soru: bugün yazılan `tasarim_tara.py` buraya mı taşınsın, özel depoda mı kalsın?
- **Intake kuyruğu** yeniden sıralandı; korpus yalnız alınacakları değil **reddedilecekleri** de gerekçeledi
  (superdesign: `npx @latest` + kod makineden çıkıyor; ui-ux-pro-max: çakışan kurallar). Her aday yine audit → REVIEW →
  MANIFEST → INTEGRITY hattından geçer.
- **Denetim betiğine iki yeni desen**: sürümsüz `npx @latest` ve çalışma zamanında ikili indirme; her biri korpusa
  örnek dosya ekleyerek.
- **Pin tazeliği bugün doğrulandı**: `frontend-design` kopyamız upstream HEAD ile birebir; korpusun "yeniden yazıldı"
  dediği şey **açık ve merge edilmemiş** bir PR.
