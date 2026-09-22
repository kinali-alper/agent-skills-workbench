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

## Trigger measurement — does the description route the request to this skill? (2026-09-21, claude-opus-5)

Protocol pre-registered in [`trigger/README.md`](trigger/README.md) before the run (metrics, n = 3, threshold 0.5, acceptance rule
"≥ 8/10 positives **and** ≥ 8/10 negatives on `any_clean`"). Runner: [`trigger/trigger_eval.py`](trigger/trigger_eval.py)
(Windows-safe variant of skill-creator's `run_eval.py`; two metrics; one project copy per worker). Raw: [`trigger/results.json`](trigger/results.json).
Set: 20 queries — 10 should-trigger (TR/EN, 4 with a file path, 6 without), 10 near-miss negatives each tagged with the skill that *should* win.
Environment: realistic 5-file React+Vite project, fixture `BrokenForm.tsx` as `src/pages/RegisterForm.tsx`, real `ux-a11y-review` uninstalled
for the run, the other 27 skills installed (competitors live), `--max-turns 6`, edits disallowed. 60 runs, **$22.3**.

| # | Etiket | Beklenen | first | any_clean | geçerli n | Bitiş | İlk araç / rakip skill |
|---|---|---|---|---|---|---|---|
| 1 | TR·keyword·path | tetikle | 0/3 | 0/1 ✗ | 1 | kesildi,kesildi,ok | Bash/Bash/Read · rakip: web-design-guidelines |
| 2 | TR·intent·path | tetikle | 0/3 | 2/2 ✓ | 2 | kesildi,ok,ok | Glob/Glob/Read |
| 3 | TR·intent·nopath | tetikle | 0/3 | 0/0 ✗ | 0 | kesildi,ok,ok | Bash/Bash/Bash |
| 4 | TR·intent·nopath | tetikle | 0/3 | 0/0 ✗ | 0 | ok,ok,ok | Bash/Bash/Bash |
| 5 | TR·blindspot·nopath | tetikle | 0/3 | 0/0 ✗ | 0 | kesildi,ok,zaman | Bash/Bash/Bash |
| 6 | TR·nielsen·nopath | tetikle | 0/3 | 0/3 ✗ | 3 | ok,ok,ok | Glob/Glob/Glob · rakip: heuristic-evaluation |
| 7 | EN·intent·path | tetikle | 0/3 | 2/3 ✓ | 3 | kesildi,kesildi,ok | Glob/Glob/Glob · rakip: heuristic-evaluation, wq-accessibility |
| 8 | EN·intent·nopath | tetikle | 0/3 | 0/0 ✗ | 0 | kesildi,ok,ok | Bash/Bash/Bash |
| 9 | EN·detail·nopath | tetikle | 0/3 | 0/0 ✗ | 0 | kesildi,ok,ok | Bash/Glob/Bash |
| 10 | TR·razor·path | tetikle | 0/3 | 2/2 ✓ | 2 | kesildi,kesildi,kesildi | Glob/Bash/Glob |
| 11 | TR·edit→wq-accessibility | tetikleme | 0/3 | 0/0 ✓ | 0 | kesildi,kesildi,kesildi | Read/Read/Read · rakip: wq-accessibility |
| 12 | EN·edit→wq-accessibility | tetikleme | 0/3 | 0/2 ✓ | 2 | kesildi,kesildi,kesildi | Read/Read/Read |
| 13 | TR·perf→wq-performance | tetikleme | 0/3 | 0/3 ✓ | 3 | ok,ok,ok | Bash/Bash/Bash · rakip: wq-core-web-vitals |
| 14 | TR·seo→wq-seo | tetikleme | 0/3 | 0/2 ✓ | 2 | kesildi,ok,kesildi | Bash/Bash/Bash · rakip: wq-seo |
| 15 | TR·visual→design skills | tetikleme | 0/3 | 0/0 ✓ | 0 | kesildi,kesildi,kesildi | Bash/Bash/Bash · rakip: frontend-design, redesign-existing-projects |
| 16 | TR·knowledge | tetikleme | 0/3 | 0/3 ✓ | 3 | ok,ok,ok | None/None/None |
| 17 | EN·knowledge | tetikleme | 0/3 | 0/3 ✓ | 3 | ok,ok,ok | ToolSearch/ToolSearch/ToolSearch |
| 18 | TR·ux-research→ux-designer | tetikleme | 0/3 | 0/2 ✓ | 2 | ok,ok,ok | Skill/Bash/Bash · rakip: ux-designer |
| 19 | EN·tooling | tetikleme | 0/3 | 0/1 ✓ | 1 | kesildi,kesildi,kesildi | Bash/Bash/Bash |
| 20 | TR·bug→none | tetikleme | 0/3 | 0/3 ✓ | 3 | ok,ok,ok | Read/Read/Read |

Tetiklemeli geçen (any_clean): 3/10 · Tetiklememeli geçen: 10/10 · first metriğiyle geçen: 10/20
Kesilen koşu: 26/60 · self-read (geçersiz) koşu: 30/60 · maliyet $22.316 · model claude-opus-5 · 2026-09-21 · max-turns 6

`first` = skill was the model's very first tool call (skill-creator's original metric). `any_clean` = skill invoked within the turn budget,
counting only runs where the model did **not** open the test command file itself (`self_read`). Numbers before "✓/✗" are triggers/valid runs.

**What the numbers do and do not say**

- **Negatives: 10/10 pass, 0 false triggers in 30 runs** — including 11 runs where the model *did* read the test skill's description and still
  chose another route. Predicted competitors won as tagged: `wq-accessibility` for edit requests, `wq-seo`, `wq-core-web-vitals`,
  `frontend-design`/`redesign-existing-projects`, `ux-designer`. Knowledge questions used no skill at all. The description does not over-trigger.
- **Positives with a file path: 3 of 4 pass on `any_clean`** — q2, q7, q10 (2/2, 2/3, 2/2); the fourth, q1 (bare keyword), is discussed below.
  These are the only positive verdicts the protocol allows.
- **Positives without a path (q3, q4, q5, q8, q9): no verdict.** In all 15 runs the model ran `ls`/`find`, saw `.claude/commands/`, opened the test
  command file, then invoked the skill (`any_raw` = 15/15). The pre-registered rule counts these as invalid samples because the trigger cannot be
  separated from the discovery. This is a **methodology artifact** of placing the test command inside the project (skill-creator's approach) in
  front of a model that explores before acting — not evidence for or against the description. Note: skill-creator's own scorer
  counts a `Read` of the command file as a trigger, so upstream would score these 15 runs 15/15 and the acceptance rule would pass;
  this protocol pre-registered them as invalid because trigger and discovery cannot be separated.
- **q6 fails (0/3): a request phrased as "Nielsen heuristics, usability" routes to `heuristic-evaluation`.** The query asks for usability only, no
  accessibility; the dedicated skill winning is arguably correct routing, and `ux-a11y-review` itself delegates step 2 to that skill. The label
  "should trigger" is debatable — recorded as a finding, not a defect.
- **q1 — the literal Turkish trigger phrase "Arayüzü denetle: <path>"** — triggered late in 2/3 (both after self-read) and lost once to
  `web-design-guidelines`. Weak signal that the bare keyword is not enough for a stack-agnostic request; see proposal below.
- **`first` = 0/60: this skill was never the model's first call.** In 1/60 runs the first call was a competitor skill (`ux-designer`, q18);
  in the other 59 it was exploration (`Bash`/`Glob`/`Read`). The skill-creator "first call" metric carries no information here; kept as a diagnostic only.
- **Pre-registered acceptance rule: not met as written** (positives 3/10 on `any_clean`), but 6 of the 7 misses are "no valid sample", not
  "did not trigger". Honest summary: *no over-triggering; correct routing when intent is stated and a file is named; unmeasured for path-less requests.*

**Proposal (not applied — the user decides):** re-run the 6 path-less positives with the test command placed **outside** the project tree (user-level
commands dir) so `find` cannot reveal it (~$8, n = 3). Only if that run shows misses, consider adding intent verbs to the description
("incele, denetle, audit, review… erişilebilirlik/kullanılabilirlik raporu") — the description was not edited in this iteration.

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
- **Trigger measurement is one model, one day, n = 3, $22.** `first` is dead as a metric here (0/60); `any_clean` has no sample for path-less
  positives because the model discovers the test command by exploring the project (30/60 runs `self_read`). 26/60 runs hit `--max-turns 6`; for
  positives the cut came after the skill call in every triggered run, so it does not hide triggers — but a longer budget could turn some `any=False`
  runs into triggers. The runner is a Windows patch of skill-creator's, not the upstream script; differences are listed in its docstring.
- **`without` runs had other installed skills available** (heuristic-evaluation, wq-accessibility, web-design-guidelines could auto-fire). That is the honest "installed environment" baseline, not a pristine model.

## Skill status: draft
The fixture no longer discriminates on *finding*; further fixture-driven edits would be overfitting. The W3C BAD page has been
run in-browser (Tab pass, focus trap reproduced — see below); the description does not over-trigger (0/30).
Next gates: (1) an **unseen** public page in a browser session — discovery, not regression; (2) trigger re-run for the six
path-less queries with the test command outside the project tree.

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
