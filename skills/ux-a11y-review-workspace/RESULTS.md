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

## Status
Draft. The fixture no longer discriminates on *finding*; further fixture-driven edits would be overfitting.
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
