# Contributing

## Adding a third-party skill
1. `git clone --depth 1` the source into a temp folder. Point the audit at the **skill subfolder**, not the clone root.
2. `bash scripts/skill-audit.sh <folder>` — must not report KRİTİK unless you have read every flagged file and can explain it.
3. Read `SKILL.md` yourself. Then write `vendor/<name>/REVIEW.md`: source repo, commit, license, audit result, decision.
4. Copy the upstream `LICENSE` into `vendor/<name>/`. Add a row to `THIRD_PARTY_NOTICES.md`.
5. If the audit reports a false positive, add a pattern to `vendor/<name>/AUDIT-ALLOW` **and** the reason to `REVIEW.md`. The exit code must be 0 for every approved skill — that is the gate.
6. **Adding any file to a vendor folder changes its audit result** — re-run `skill-audit.sh` (this bit us once).
7. `bash scripts/gen-manifest.sh` regenerates `vendor/MANIFEST.md` **and** `vendor/INTEGRITY.sha256` (it wraps `gen-manifest.py` + `gen-integrity.sh`); never edit either by hand. `install.sh` refuses a vendor whose files do not match INTEGRITY.sha256; `scripts/verify-integrity.sh` checks it standalone.
8. AUDIT-ALLOW patterns must be **file:line specific** (vendor files are pinned, so lines are stable). A pattern that matches any future line in a folder is fail-open and will be rejected in review. `skill-audit.sh --no-allow <dir>` shows raw findings with exceptions ignored.
9. A skill that needs other skills declares them in frontmatter `metadata.requires: "a, b"`; `install.sh --only X` warns when they are missing, `--with-deps` installs them.
10. `bash scripts/install.sh --only <name>` — refuses to install anything without `REVIEW.md`; backs up an existing folder before replacing it.

`npx skills add …` and `claude plugin marketplace add …` write straight into `~/.claude` — do not use them here.

## Writing or changing a skill
Read `vendor/writing-for-agents/SKILL.md` first (context pointers, information hierarchy, completion criteria, positive rules).

## Changing `skills/ux-a11y-review`
- Rules are stack-neutral; stack recipes go under `references/` behind a conditional pointer.
- Every step ends with a checkable completion criterion. Write rules positively (what to do), not as prohibitions.
- Run the evals (see `skills/ux-a11y-review/evals/evals.json`): fresh subagent, isolated fixture copy, with/without skill.
  Do not edit the skill in response to a single run; a change must be justified by a defect the eval exposed — **or by an external review, in which case a full eval run is owed before the change ships.** Every `grading.json` records `model` and `date`.

## Line endings (Windows)
The repo is LF-only (`.gitattributes`). On Windows run `git config core.autocrlf false` in this clone; otherwise checkout
produces CRLF working copies and `verify-integrity.sh` (which hashes the working copy) reports a false mismatch against
`INTEGRITY.sha256`, which is generated from LF content. CI runs on Linux and sees LF.

## Before pushing
`bash scripts/publish-check.sh` must print `TEMİZ`. The tracked script scans for machine paths, e-mail addresses and
11-digit identifiers. **Organisation, project and person names live in `scripts/publish-check.local`** (gitignored, one
pattern per line) — the tracked script never contains them, so the leak scanner cannot itself leak. Create that file on
each machine you push from.

## Audit regression corpus
`evals/audit/` holds deliberately malicious and deliberately benign SKILL.md samples with expected exit codes
(`expected.tsv`). `bash scripts/test-audit.sh` must pass after any change to `skill-audit.sh`. Add a sample whenever a
bypass is found (the blank-line-before-frontmatter case came from an external review).
