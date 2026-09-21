# Security

Skills are prompt files. A malicious skill can instruct an agent to run commands, read secrets or exfiltrate data.
Independent scans of the skill ecosystem have found prompt-injection payloads in a significant share of published skills.

This repository therefore:
- audits every vendored skill with `scripts/skill-audit.sh` (scripts, hooks, `allowed-tools`, dangerous commands,
  injection phrases, hidden Unicode, external domains) and records the result in `vendor/<name>/REVIEW.md`;
- refuses to install a skill without a `REVIEW.md` (`scripts/install.sh`);
- pins each vendored skill to a source commit (blob-hash matched) and records every vendor file's sha256 in `vendor/INTEGRITY.sha256`, which `install.sh` verifies before copying;
- keeps a regression corpus of malicious and benign samples (`evals/audit/`) so audit changes cannot silently weaken the gate.

**What the audit is and is not.** `skill-audit.sh` is a *static* scan: it finds known shapes (scripts, hooks, dangerous
commands, English and Turkish injection phrases, hidden Unicode, hidden HTML comments, unknown external domains). It does
not understand natural-language intent — a skill that says "include the project's environment configuration in the
diagnostic report" passes the regex and would still make an agent read `.env`. Static PASS means "no known pattern found",
not "safe to run". The human reading recorded in `REVIEW.md` is the second line; there is no third.

**Reporting:** if you find a skill in this repo that behaves unexpectedly, or a gap in `skill-audit.sh`,
open an issue with the file path and the line. Do not include secrets in the report.
