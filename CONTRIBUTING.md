# Contributing

## Adding a third-party skill
1. `git clone --depth 1` the source into a temp folder. Point the audit at the **skill subfolder**, not the clone root.
2. `bash scripts/skill-audit.sh <folder>` — must not report KRİTİK unless you have read every flagged file and can explain it.
3. Read `SKILL.md` yourself. Then write `vendor/<name>/REVIEW.md`: source repo, commit, license, audit result, decision.
4. Copy the upstream `LICENSE` into `vendor/<name>/`. Add a row to `THIRD_PARTY_NOTICES.md`.
5. `bash scripts/install.sh` — refuses to install anything without `REVIEW.md`.

`npx skills add …` and `claude plugin marketplace add …` write straight into `~/.claude` — do not use them here.

## Changing `skills/ux-a11y-review`
- Rules are stack-neutral; stack recipes go under `references/` behind a conditional pointer.
- Every step ends with a checkable completion criterion. Write rules positively (what to do), not as prohibitions.
- Run the evals (see `skills/ux-a11y-review/evals/evals.json`): fresh subagent, isolated fixture copy, with/without skill.
  Do not edit the skill in response to a single run; a change must be justified by a defect the eval exposed.

## Before pushing
`bash scripts/publish-check.sh` must print `TEMİZ`. It scans every tracked and untracked file for organisation names,
machine paths, e-mail addresses and 11-digit identifiers.
