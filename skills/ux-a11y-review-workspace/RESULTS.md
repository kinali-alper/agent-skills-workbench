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
