# Contributing

## Adding a third-party skill
1. `git clone --depth 1` the source into a temp folder. Point the audit at the **skill subfolder**, not the clone root.
2. `bash scripts/skill-audit.sh <folder>` — must not report KRİTİK unless you have read every flagged file and can explain it.
3. Read `SKILL.md` yourself. Then write `vendor/<name>/REVIEW.md`: source repo, commit, license, audit result, decision.
4. Copy the upstream `LICENSE` into `vendor/<name>/`. Add a row to `THIRD_PARTY_NOTICES.md`.
5. If the audit reports a false positive, add a pattern to `vendor/<name>/AUDIT-ALLOW` **and** the reason to `REVIEW.md`. The exit code must be 0 for every approved skill — that is the gate.
6. **Adding any file to a vendor folder changes its audit result** — re-run `skill-audit.sh` (this bit us once).
7. `bash scripts/gen-manifest.sh` regenerates `vendor/MANIFEST.md`; never edit it by hand.
8. `bash scripts/install.sh --only <name>` — refuses to install anything without `REVIEW.md`; backs up an existing folder before replacing it.

`npx skills add …` and `claude plugin marketplace add …` write straight into `~/.claude` — do not use them here.

## Writing or changing a skill
Read `vendor/writing-for-agents/SKILL.md` first (context pointers, information hierarchy, completion criteria, positive rules).

## Changing `skills/ux-a11y-review`
- Rules are stack-neutral; stack recipes go under `references/` behind a conditional pointer.
- Every step ends with a checkable completion criterion. Write rules positively (what to do), not as prohibitions.
- Run the evals (see `skills/ux-a11y-review/evals/evals.json`): fresh subagent, isolated fixture copy, with/without skill.
  Do not edit the skill in response to a single run; a change must be justified by a defect the eval exposed.

## Before pushing
`bash scripts/publish-check.sh` must print `TEMİZ`. It scans every tracked and untracked file for organisation names,
machine paths, e-mail addresses and 11-digit identifiers.
