# visual-design-review — eval results

Status on 2026-10-16, the day the skill was written. **Only the deterministic half has been measured.** The
with/without isolated-subagent comparison that `ux-a11y-review` went through has **not** been run yet; until it is,
nothing here says the skill improves a model's visual review.

## 1. What exists

| Piece | State |
|---|---|
| `SKILL.md` (103 lines, 5 steps, four-state verdicts, per-surface mode) | written |
| `references/isaretler.md` — G1–G12, each row with a public source or an explicit `[öneri]` tag | written |
| `scripts/visual-scan.py` — 18 countable signals, stdlib only, report-only, exit 0/2 | **measured** |
| `evals/slop.html` + `evals/temiz.html` + `BEKLENEN.md` | **measured** |
| `evals/evals.json` — 4 evals (slop, clean negative control, mode fit, render-less) | defined, **not run** |
| Isolated with/without runs, replication, blind judge | **not started** |

## 2. Measured — the scanner discriminates

| Fixture | Signals | Exit code |
|---|---|---|
| `slop.html` (deliberately generic admin screen) | **17** | 2 |
| `temiz.html` (same screen, disciplined) | **0** | 0 |

Both fixtures are the same screen with the same content, so the difference is the visual language alone and not the
subject matter. Thresholds carry their provenance in the output: `[kaynak]` = verified in an external document,
`[öneri]` = proposed by the 2026 research round and **not independently measured here**.

## 3. What self-testing caught (and the skill owes to it)

- **Hex-written purple/indigo was invisible.** The first version matched class names only (`indigo-500`, `from-purple`),
  so `slop.html`'s `#7c3aed` / `#6366f1` / `#4f46e5` passed as "no purple accent" — on a fixture built specifically to
  contain that cliché. Fixed by converting saturated colours (chroma ≥ 0.08) to OKLCH and checking the hue band
  255–330°. `slop.html` went 16 → 17 signals; `temiz.html` stayed at 0. Lesson: a cliché detector that matches a
  framework's vocabulary misses the same cliché written by hand.
- **Our own audit flagged the skill.** `skill-audit.sh skills/visual-design-review` returned KRİTİK because the folder
  ships a `.py` and two `.html` files — exactly what the check is for. Resolved the way vendors are: a file-specific
  `AUDIT-ALLOW` with the reason written out (stdlib only, no network, no subprocess, no file writes; fixtures are
  static and excluded from installation). Strict mode (`--no-allow`) still reports it, which is correct.

## 4. Honest limits

- **No model-side evidence.** Everything above measures a Python script. Whether the skill makes a model's visual
  review better, shorter or more consistent is unmeasured.
- **One fixture pair, one author.** The fixtures, the G-list and the thresholds were written in the same session;
  `temiz.html` is the author's idea of disciplined. The negative control mitigates this, it does not remove it.
- **The `[öneri]` thresholds are borrowed.** They come from a research round whose measured claims all trace to a
  single model family. Treat them as starting points; a false positive in a real project is a reason to discuss the
  threshold, not to bend the finding.
- **Step 4 needs a rendered page and a main session.** Subagents have no browser; on this machine the in-app pane does
  not paint, so a headless browser screenshot is the workaround. Any run without it is labelled "render yok".
- **Turkish only in the output.** The G-list and the scanner report are Turkish, like `ux-a11y-review`'s references;
  the trigger phrase is Turkish on purpose so it does not collide with the English-triggered vendored design skills.

## 5. Next gates

1. **Isolated with/without runs** on both fixtures (the `ux-a11y-review` recipe: fixture alone in a temp folder, skill
   copy without `evals/`, subagent cannot see this repo), replicated ×3, plus the clean fixture as the negative
   control. Pass = the skill version writes all G1–G12 verdicts with zero invented violations and the bare model does
   not.
2. **A real page**, not a fixture: run the skill on one public page and report what the scanner missed and the G-list
   caught (and the reverse).
3. **Blind A/B of the skill text itself** if it is ever edited for "quality" rather than coverage: 50 prompts, two
   variants, blind judge on brief fit / polish / usability / distinctiveness, sign test. Method borrowed from the
   `frontend-design` PR that measured 21/28 (p = 0.006) — that PR is open and unmerged, so it is a method, not a
   verdict.

Until gate 1 passes, the skill stays `status: draft` and the README says so.
