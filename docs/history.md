# History

- **2026-09-17** — Repository founded. Security intake pipeline (`skill-audit.sh`, `install.sh`, `vendor/*/REVIEW.md`).
  14 existing design/motion skills audited and vendored. Playground (Vite + Playwright + axe + Lighthouse) with a
  deliberately broken Turkish school-registration form: 13 WCAG 2.2 defects; axe caught 4, Lighthouse scored it 84/100.
- **2026-09-18** — Accessibility skills vendored (Vercel web-design-guidelines, addyosmani web-quality-skills).
  Both scored 8/9 on the automated-tool blind spots; both missed table headers. Plain-HTML and Razor twins added —
  same findings on all three stacks. UX leg: szilu ux-designer + Owl-Listener heuristic-evaluation vendored;
  6 Nielsen defects added to the fixture; heuristic-evaluation 6/6, Vercel 2/6.
  `ux-a11y-review` drafted (orchestrator over the vendored skills + gap checks), evaluated over two iterations with
  fresh isolated subagents — see `skills/ux-a11y-review-workspace/RESULTS.md`. Repository published (skill status: draft).
- **2026-09-18 (later)** — Real-page test on W3C WAI's intentionally inaccessible "CityLights" demo: 15/19 AA criteria
  found, 2 partial, 2 missed (1.4.1 colour-only links, 2.4.1 skip link). Browser step (Tab-through) produced the
  severity-4 finding. Checklist widened (A1, A5, A6) on that evidence; negative control re-run (iteration-3).
- **2026-09-21** — Deep review in a separate session, same tooling (v3 rubric, 6.0 "dikkatli kullan") verified claim by claim; all facts held.
  Response: 15 pinless vendors pinned by blob-hash match to their true upstream commits (none drifted); `install.sh`
  gained `--only`/`--dry-run` and backs up before overwrite; `AUDIT-ALLOW` per-vendor exceptions make the audit exit
  code a real gate (27/27 return 0, malicious sample still fails); `vendor/MANIFEST.md` generated from REVIEW files
  with a layer column; SKILL.md gained "Ne için kullanılmaz", lost its hardcoded path, states honestly that A1–A13 are
  blind spots (19 criteria) and points to `references/wcag22-aa-sweep.md` for the other 36 A/AA criteria; A10's 2.3.3
  (AAA) mis-cite fixed. Repo reframed as a skills **workbench** (Yol B): two first-class skills planned
  (`ux-a11y-review`, `visual-design-review`), vendors kept and layered.
- **2026-09-21 (later)** — Fifteen external reviews (nine vendors) triaged; five read the repo, others reviewed README only,
  one hallucinated, one reviewed the wrong repo. Two verified defects fixed the same day: the leak scanner's tracked source
  carried organisation names (moved to gitignored `publish-check.local`; script now scans itself) and a frontmatter bypass
  (a leading blank line hid `allowed-tools` — now KRİTİK). Audit gained Turkish injection phrases and an unknown-domain
  warning; a six-sample regression corpus with expected exit codes lives in `evals/audit/`. `history.md` wording: the
  21-Sep review was a separate session with the same tooling, not independent — the fifteen external reviews are.
- **2026-09-21 (evening)** — Security set from the fifteen-review synthesis, chosen with the advisor as "needed, not vision":
  `vendor/INTEGRITY.sha256` (sha256 of all 145 vendor files; `install.sh` refuses mismatches; `verify-integrity.sh`
  detects edits and unregistered files) — the pin is now a mechanism, not a note. Unicode scan covers all text files, not
  just `.md` (corpus sample 07). `AUDIT-ALLOW` broad `.*password` pattern replaced by explicit file:line lists (fail-open
  closed, verified by planting a new hit); `skill-audit.sh --no-allow` strict mode. `metadata.requires` in the skill's
  frontmatter; `install.sh --only` warns on missing dependencies, `--with-deps` installs them, `--prune-backups N`.
  RESULTS.md gained a Limitations block (n=1, same-U2×3, inline grading, well-known real page, model-relative value,
  iteration-4 owed). `.github/workflows/gate.yml`: audit 27+1 → 0, corpus, strict report, integrity, manifest freshness,
  leak scan, install smoke test. Declined as vision: TS CLI, sandbox, registry, dashboard, SARIF, semantic classifier.
- **2026-09-21 (night)** — iteration-4: 20 fresh isolated subagent runs in three conditions (`without` / `plain` = tables
  only / `with` = full skill); TSX and clean control replicated ×3. Result: `without` 18/19 on every stack, `plain` and
  `with` 19/19 everywhere, zero variance; clean control 0 violations in 4/4 checklist runs; `with` reports 2–4× shorter.
  Decomposition: finding power = checklist content; mechanism = brevity, severity, completeness, sweep, browser/TODO.
  W3C regression with the widened rules: 15 → 17/19 (1.4.1 colour-only links 8/8, no skip link measured in-browser; focus
  trap reproduced). Decision: **no skill edit** — fixture saturated. Raw it-4 reports published after leak scan.
- **2026-09-21 (late night)** — Trigger measurement for the `ux-a11y-review` description, protocol pre-registered
  (`skills/ux-a11y-review-workspace/trigger/README.md`): 20 queries (10 should / 10 near-miss negatives tagged with the
  skill that should win) × 3 runs, `claude -p --model claude-opus-5 --max-turns 6`, competitors installed, real skill
  removed for the run; Windows-safe runner derived from skill-creator's `run_eval.py` (thread reader, two metrics,
  per-worker project copies). Result: negatives 10/10, **0 false triggers in 30 runs**; path-bearing positives 3/3;
  path-less positives **no verdict** — the model found the test command by exploring the project in 15/15 runs
  (`self_read`); skill-creator's "first call" metric 0/60 (model always explores first). Description **not edited**;
  proposal: re-run the 6 path-less queries with the command outside the project. Cost $22.3.
- **2026-10-06 (night)** — Two tooling bugs found on 30 Sep fixed (local only, not committed). `publish-check.sh`: the
  `PATHS` pattern wrote backslashes as `\|`, which ERE reads as a literal pipe, so backslash-style Windows paths never
  matched; now `\\` (verified by planting such a path in an untracked file: exit 1; removed: TEMİZ, 277 files). The
  decision row of all 27 `vendor/*/REVIEW.md` had lost its `| Karar |` cell to a U+0001 left by an earlier substitution;
  restored. `INTEGRITY.sha256` regenerated (27 hashes), `MANIFEST.md` unchanged. Checks: integrity, audit corpus,
  publish-check green.
- **2026-10-16** — `docs/roadmap.md` written: open gates costed (trigger re-run for the six path-less queries ~$8;
  one unseen real page in a browser session), `visual-design-review` scoped against a 2026 research round (modes,
  NEVER+INSTEAD, second-wave tells, deterministic signals, the 50-prompt blind-judge eval shape), intake queue
  re-ordered with reasons to **decline** (superdesign: `npx @latest` + code leaves the machine; ui-ux-pro-max:
  conflicting rules, worst detector run), two new audit patterns proposed (unpinned `@latest`, runtime binary
  download) each owing a corpus sample. Verified at source today: `vendor/frontend-design` blob is byte-identical to
  upstream HEAD (no drift), and the "frontend-design was rewritten" claim is **PR #210, open and unmerged** — recorded
  as proposal, not release. Nothing implemented; the roadmap is a plan.
- **2026-10-16 (later)** — **G1 closed**: the six path-less trigger queries re-run with the test command in
  `~/.claude/commands` instead of the project (`trigger_eval.py --commands-dir`). **6/6 pass on `any_clean`,
  `self_read` 0/18** — the discovery artifact is eliminated, so the earlier "no verdict" was the method, not the
  description. Pre-registered rule now met: positives 9/10, negatives 10/10; description still unedited. Cost
  **$20.54** for 18 runs against a ~$7 estimate (3x over): without a findable command file the model explores longer
  and 13/18 runs hit the 6-turn ceiling. **Audit step 3b added** to `skill-audit.sh`: unpinned self-updating
  invocation (`npx --yes …@latest`, `uvx`, `pnpm dlx`, `go run …@latest`) and runtime binary download
  (`releases/download`, `~/.x/bin`, `install.sh | sh`), both UYARI, with corpus samples `09-unpinned-latest-cli` and
  `10-runtime-binary-download` (expected rc 1 each). One real exception documented: `design-taste-frontend` documents
  `npx shadcn@latest` for the user (SKILL.md:99, 1006, 1007) → file:line `AUDIT-ALLOW` + reason row in its REVIEW.
  Also fixed while doing it: our own `REVIEW.md`/`AUDIT-ALLOW` were being scanned as if they were skill content
  (they are never installed), and the first attempt to exclude them with grep's `--exclude` **widened** the file set
  in Git Bash (LICENSE.txt entered the URL scan, inventing an `apache.org` finding) — replaced with a `drop_meta`
  output filter. Checks: 29/29 vendors → 0, 10/10 corpus samples as expected.
- **2026-10-16 (parallel session, recorded afterwards)** — Intake and a real bug fix not authored in the session above:
  `scripts/skill-audit.sh` step 2 was dead — the awk program that reads the frontmatter block carried literal newlines
  from an earlier substitution, so `allowed-tools` / `hooks` were never detected; fixed, with
  `evals/audit/08-allowed-tools-frontmatter` added as the proof sample (body clean, frontmatter hostile, expected rc 2;
  sample 01 had been passing for other reasons and so hid the hole — as recorded in `evals/audit/README.md`). Two vendors taken in: **baseline-ui**
  (ibelick/ui-skills, `3434a76`, MIT, 85 lines) and **interface-design** (Dammyjay93/interface-design, `2f9be32`, MIT,
  320 lines, `agents/openai.yaml` left out) — both audited clean, blob-matched, installed. **web-design-guidelines**
  stopped fetching its rule list at run time: the upstream `command.md` (vercel-labs/web-interface-guidelines,
  `434b7f9`) is now vendored and pinned by blob, the run-time network call and its AUDIT-ALLOW are gone.
- **2026-10-16 (evening)** — First two-way **vendor pin sweep**, runner published as `scripts/pin-sweep.py` ([`docs/pin-sweep.md`](pin-sweep.md)): our copy vs its
  pin, and the pin vs upstream HEAD, by blob hash. Of 24 readable vendors, 20 are byte-identical to their pin, 4 differ
  only by a documented adaptation, **0 undocumented drift**; upstream has moved past the pin for 4
  (design-taste-frontend, minimalist-ui, redesign-existing-projects, ux-designer — three share one upstream repo, so
  one review would cover them). 5 rows hit the unauthenticated API rate limit. The sweep also caught a **false record**:
  all six `wq-*` REVIEWs claimed the frontmatter `name` was untouched while every one of them carries `name: wq-…`;
  corrected, with the measurement cited. README counts updated from 27 to 29 and from measured values.
- **2026-10-16 (night)** — **`visual-design-review` written** and moved from "planned" to `draft`. Shape: router
  SKILL.md (103 lines, five steps, the same four-state verdict dictionary as `ux-a11y-review`, per-surface mode
  persuade/operate/read/experience), `references/isaretler.md` (G1–G12, every row carrying a public source — Anthropic
  frontend-design, Vercel guidelines, Lucide spec, Wathan's indigo post, `avoid-ai-design` — or an explicit `[öneri]`
  tag), and `scripts/visual-scan.py` (18 countable signals, stdlib only, report-only, exit 0/2). The scanner is a port
  of one written the same day in a private knowledge repo: the `[zevk]` (personal-taste) provenance label was
  reclassified as `[kaynak]`/`[öneri]` and every reference to a person or project removed, so the published version is
  project-agnostic. Fixture pair ported with it: **slop 17 signals / clean 0**. Two things self-testing caught:
  hex-written purple (`#7c3aed`) was invisible because the check matched only framework class names — fixed by an
  OKLCH hue test, and the fix was applied to both copies so they do not drift; and **our own audit flagged our own
  skill** KRİTİK for shipping a `.py` plus two `.html`, resolved with a file-specific `AUDIT-ALLOW` and a written
  reason, strict mode still reporting it. `evals/evals.json` defines four evals; **none of them has been run** — the
  isolated with/without comparison is gate 1 in the new workspace RESULTS, and the skill stays `draft` until it passes.
- **2026-10-16 (late)** — **G2 closed**: `ux-a11y-review` run on an unseen public page (a Turkish municipality home
  page, not named in the repo — public body, owner's call), read-only, no form submitted
  ([`real-page-2/report.md`](../skills/ux-a11y-review-workspace/real-page-2/report.md)). The in-app browser does not
  paint on this machine, so the accessibility tree was empty; the DOM and stylesheets were read with JavaScript and the
  keyboard pass used real Tab presses captured by a `focusin` listener. Eight findings, six verdict categories used.
  The browser step earned its place twice: **the first 13 Tab stops are all nameless** (a fact invisible in the source,
  where those 13 elements look like unrelated small defects) and **`outline: none` in 14 rules against `:focus-visible`
  in 4** (a ratio only visible across all stylesheets at once). Contrast and target size stayed `doğrulanamaz` because
  layout was unavailable — the four-state dictionary refusing to invent numbers on a real page. With G1 and G2 closed,
  `draft → stable` is now a decision rather than a missing measurement.

