# ux-a11y-review — eval results

Method: skill-creator style. Each eval runs twice in a **fresh subagent** with an isolated copy of the fixture
(no access to the repo or the answer key `evals/cases/broken-form/expected.md`): once with the skill, once without.
Baseline = the bare model with no skill (no other installed skill fired in any baseline run).
Raw subagent reports are not published (they echo local paths); `grading.json` per run holds the graded expectations.

## iteration-1 — broken fixtures (19 planted defects: 13 WCAG 2.2 + 6 Nielsen)

| Fixture | Without skill | With skill | Delta |
|---|---|---|---|
| React TSX | 18/19 (missed U2 "no cancel path"), 223 lines, free-form | 19/19, 82 lines, 21/21 explicit verdicts | +1 finding; 2.7× shorter; complete |
| Plain HTML | 18/19 (missed U2), 260 lines | 19/19, 85 lines, 21/21 | +1; 3× shorter |
| ASP.NET Razor | 18/19 (missed U2), 397 lines | 19/19, 77 lines, 21/21, Razor recipes | +1; 5× shorter |

**Honest reading:** the bare model already finds 18/19. The skill's measured contribution is *not* "finds more" —
it is completeness (every checklist row gets a verdict), consistency of format, severity scale, brevity,
stack-specific fix recipes, and the mandatory keyboard / human-TODO steps.

Two Razor runs were invalidated (`*_INVALID-leak`, not published): the fixture header leaked the defect count and the
answer-key filename. Header removed, runs repeated.

## iteration-1 — negative control (clean `FixedForm.tsx`)

| | Result | Cause |
|---|---|---|
| With skill | **FAIL** | verdict word "bulundu" was ambiguous (violation found vs. rule satisfied) → skill defect |
| Without skill | 14 findings, **3 real bugs** in the "clean" fixture | reset didn't clear controlled state; `required` blocked the custom error branch; dead anchor → fixture defect |

Fixes: skill got a four-state verdict vocabulary (`ihlal :N` / `uygun` / `uygulanamaz` / `doğrulanamaz`);
fixture bugs fixed; all six Playwright tests kept green.

## iteration-2 — negative control rerun

| | Result |
|---|---|
| With skill | **PASS** — 0 violations · 16 compliant · 4 unverifiable (CSS/shell) · 1 n/a; four borderline items rejected with reasons |
| Without skill | 10 notes, 2 legitimate nits (persistent Turkish errors on non-TC fields; star sentence read half by screen readers) → fixed in fixture |


## iteration-4 — three conditions, replicated (2026-09-21, model claude-opus-5)

Skill under test: `skills/ux-a11y-review` at commit `03010b2` (after the 21-Sep widening: A1 skip link, A5 colour-only links,
A6 focus persistence, A10 re-cite, sweep step). Fresh isolated subagent per run; fixture alone in a scratch dir, no header,
no repo access; installed `ux-a11y-review` removed for the duration. Token figures are the subagent's total usage.

| Condition | What the agent gets | Measures |
|---|---|---|
| `without` | bare prompt | the model alone (installed skills may auto-fire — honest environment baseline) |
| `plain` | bare prompt + **only** the A1–A13 / U1–U8 tables + one line "one of four verdicts per row" | value of the checklist **content** |
| `with` | full SKILL.md + references | value of the skill **mechanism** (steps, output template, sweep, mandatory browser/TODO) |

### Broken fixtures — 19 planted defects (F1–F19)

| Fixture | n | `without` | `plain` | `with` | Lines (w/o · plain · with) | Tokens (w/o · plain · with) |
|---|---|---|---|---|---|---|
| TSX | **3** | 18/19 · 18/19 · 18/19 | 19/19 · 19/19 · 19/19 | 19/19 · 19/19 · 19/19 | 137–274 · 150–263 · **48–80** | 74–79k · 78–94k · 84–90k |
| HTML | 1 | 18/19 | 19/19 | 19/19 | 199 · 200 · **68** | 80k · 80k · 84k |
| Razor | 1 | 18/19 | 19/19 | 19/19 | 380 · 168 · **76** | 91k · 80k · 94k |

The single miss in every `without` run, on every stack, is the same row: **F15/U2 — no cancel or exit path** (verified by
hand: zero matches for iptal/vazgeç/cancel/çıkış in all five `without` reports). Zero variance across the three TSX reps in
every condition. `plain` and `with` both produce all 21 verdicts.

### Negative control — clean `FixedForm.tsx`

| Condition | n | Violations (`ihlal`) | Notes raised | Tokens |
|---|---|---|---|---|
| `with` | **3** | **0 · 0 · 0** | 3 · 1 · 4 low-severity suggestions (emoji `aria-hidden`, focus timing) | 79–92k |
| `plain` | 1 | 0 | — | 72k |
| `without` | 1 | (no verdict concept) | 18 notes, two labelled "high" that are design preferences | 77k |

### Decomposition — what the skill actually adds

- `plain − without` = **+1 finding (U2) and +21 explicit verdicts.** Note what `plain` contained: the two tables **and** the
  one-line four-state verdict vocabulary — so the "content" bucket is tables + vocabulary; the "mechanism" bucket is steps,
  output template, sweep, references and the mandatory browser/TODO steps. The entire *finding* gain comes from the content. Given the same two tables as a plain prompt, the model finds exactly what the skill finds.
- `with − plain` = **0 findings, 0 verdicts.** The mechanism adds: reports 2–4× shorter (48–80 vs 150–263 lines), a
  severity scale, consistent `file:line → positive fix` format, the human TODO block, and the AA sweep (which surfaced
  1.4.10 reflow, 1.3.5, 3.2.4, 2.4.2 on HTML — items outside the compact list). Token cost is ~5–10k above `plain` for
  reading SKILL.md and references.
- False positives: **0 in 4 checklist-driven clean runs.** The four-state vocabulary held under replication.

Honest reading: `ux-a11y-review` is a **checklist plus a report discipline**, not a detection engine. The part no plain
prompt reproduces is step 4: every subagent run degraded to "render yok"; the browser pass exists only in the main session,
and it produced the severity-4 finding on the real page. That is the skill's irreplaceable component. Its finding power
equals the two tables; its mechanism buys brevity, consistency, severity, completeness and the mandatory browser/human steps.

### Real page regression — W3C WAI BAD "before" home (answer key known; main session, browser pane)

Focus trap reproduced: 16 Tabs → 15 links received and instantly lost focus, `activeElement` stayed `<body>`. The two rows
widened after the first run now yield measured evidence: `#main` links **8/8** without underline (1.4.1, colour-only —
A5), no in-demo skip link (2.4.1 — A1). Real-page tally moves from 15/19 to **17/19** AA; the two remaining partials
(1.3.2 layout-table order, 3.2.4 inconsistent naming) are unchanged. Labelled regression, not discovery.

## Limitations (read before citing any number above)

- **n = 1 per condition.** Every with/without pair was run once. LLM output varies between runs; 19/19 vs 18/19 is one
  draw, not a distribution. No repeats, no variance, no confidence interval.
- **"+1 finding" is one finding.** The skill's only extra hit was U2 ("no cancel path") on all three fixtures — the same
  planted defect found three times, not three independent gains.
- **Grading was inline, by the same agent, against `expected.md`.** No second grader, no inter-rater agreement. Raw
  subagent reports for iterations 1–3 are not published (they echoed local paths); **iteration-4's 20 raw reports are
  published** after the leak scan — the only edits were two invented example e-mail domains normalised to `ornek.com`.
- **Fixture and checklist share an author.** The 19 defects, the A/U checklist and the pass criteria were written by the
  same session. The negative control and the real page mitigate this; they do not remove it.
- **The real page is well known.** W3C's "Before and After Demo" is a canonical accessibility teaching example and is
  likely in model training data. Treat 15/19 as a floor-check, not as evidence about ordinary bad sites.
- **Value is model-relative.** "Bare model finds 18/19" is a statement about one model on one date. It will drift as
  models change; every future `grading.json` records `model` and `date`, and the baseline is re-run per model.
- **Grading in iteration-4 was again inline by the same agent** (keyword pre-scan + manual check of every miss). No second grader yet.
- **`without` runs had other installed skills available** (heuristic-evaluation, wq-accessibility, web-design-guidelines could auto-fire). That is the honest "installed environment" baseline, not a pristine model.

## Skill status: draft
 The fixture no longer discriminates on *finding*; further fixture-driven edits would be overfitting.
Next gate: a real, publicly reachable page, run in a session with a browser (step 4 — Tab-through — has not yet executed).

## Real page — W3C WAI "Before and After Demo" (inaccessible home page), 2026-09-18

Run in the main session with the browser pane (first execution of step 4). Report written **before** opening
W3C's own failure report; comparison appended afterwards. Files: `real-page-w3c-bad/`.

| | Count | Criteria |
|---|---|---|
| Found | **15 / 19** AA | 1.1.1 · 1.3.1 · 1.4.3 · 1.4.5 · 2.1.1 · 2.4.2 · 2.4.4 · 2.4.6 · 2.4.7 · 3.1.1 · 3.2.1 · 3.2.2 · 3.2.5 · 3.3.2 · 4.1.2 |
| Partial | 2 | 1.3.2 (layout-table reading order), 3.2.4 (inconsistent link naming) |
| Missed | 2 | **1.4.1** links distinguished by colour only · **2.4.1** no skip link |
| Out of scope | 8 | 7 AAA criteria; 4.1.1 (removed in WCAG 2.2) |

The top finding (severity 4) came from **step 4, not the checklist**: 16 Tab presses logged via `focusin`/`focusout`
showed every one of 14 links receiving focus and dropping it instantly (`onfocus="blur();"`) — keyboard users can
reach only 2 of 21 focusable elements. Static reading would have said "probably"; the browser proved it.

Both misses were checklist gaps, not oversight → A5 widened (colour-only applies to links, not just errors),
A1 widened (page-level skip link), A6 widened (focus must *persist*). First skill edit justified by real-page evidence.
Negative control re-run as iteration-3 to confirm the widened rules add no false `ihlal` on a clean file.

## iteration-3 — negative control after the real-page widening

| | Result |
|---|---|
| With skill | **PASS** — 0 violations · 14 compliant · 1 n/a · 6 unverifiable (A1 skip link, A3/A5/A6/A9 CSS, A12 host). The widened A1/A5/A6 produced no false `ihlal`; the "page-level" scoping on A1 resolved to `doğrulanamaz` on a component file, as intended. |
| Without skill | 11 notes; one legitimate nit ("aşağıda" in the status text while the region renders below the fields) → fixed in fixture. |
