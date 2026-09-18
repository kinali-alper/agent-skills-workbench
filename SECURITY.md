# Security

Skills are prompt files. A malicious skill can instruct an agent to run commands, read secrets or exfiltrate data.
Independent scans of the skill ecosystem have found prompt-injection payloads in a significant share of published skills.

This repository therefore:
- audits every vendored skill with `scripts/skill-audit.sh` (scripts, hooks, `allowed-tools`, dangerous commands,
  injection phrases, hidden Unicode, external domains) and records the result in `vendor/<name>/REVIEW.md`;
- refuses to install a skill without a `REVIEW.md` (`scripts/install.sh`);
- pins each vendored skill to a source commit.

**Reporting:** if you find a skill in this repo that behaves unexpectedly, or a gap in `skill-audit.sh`,
open an issue with the file path and the line. Do not include secrets in the report.
