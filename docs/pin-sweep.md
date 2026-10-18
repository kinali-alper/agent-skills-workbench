# Vendor pin sweep — 2026-10-16

Produced by `scripts/pin-sweep.py` (see **Re-running**).

Two questions per vendor, answered by blob hash, not by reading:

1. **Is our copy faithful to its pin?** local `git hash-object SKILL.md` vs the blob at the pinned commit.
2. **Has upstream moved past the pin?** blob at the pinned commit vs blob at upstream HEAD.

Separating the two matters: a difference in (1) means *we* changed something and it must be documented; a difference
in (2) means upstream released something new, which is exactly what pinning is for — it is a review trigger, not a bug.

| Vendor | Pin | Our copy vs pin | Upstream vs pin |
|---|---|---|---|
| baseline-ui | `3434a76` | faithful | same |
| design-taste-frontend | `3c7017d` | faithful | **moved** |
| frontend-design | `dbdd79c` | faithful | same |
| grill-me | `c55ee46` | faithful | same |
| gsap-core | `96c4b01` | faithful | same |
| gsap-frameworks | `7f8b61e` | faithful | same |
| gsap-performance | `96c4b01` | faithful | same |
| gsap-plugins | `5b909b9` | faithful | same |
| gsap-react | `96c4b01` | faithful | same |
| gsap-scrolltrigger | `96c4b01` | faithful | same |
| gsap-timeline | `96c4b01` | faithful | same |
| gsap-utils | `96c4b01` | faithful | same |
| heuristic-evaluation | `9a6930c` | faithful | same |
| high-end-visual-design | `3206dd4` | faithful | same |
| industrial-brutalist-ui | `3206dd4` | faithful | same |
| interface-design | `2f9be32` | faithful | same |
| minimalist-ui | `3206dd4` | faithful | **moved** |
| motion-design | `b6606e1` | faithful | same |
| redesign-existing-projects | `3206dd4` | faithful | **moved** |
| to-spec | `c55ee46` | faithful | same |
| ux-designer | `da9e9d0` | differs: 2 lines, only `name`/`description` (documented) | **moved** |
| web-design-guidelines | `063bee9` | differs: 18 lines — the documented adaptation (reads a pinned local `command.md` instead of fetching the rule list at run time) | same |
| wq-accessibility | `afa8da9` | differs: 1 line, `name:` (documented) | same |
| wq-best-practices | `afa8da9` | differs: 1 line, `name:` (documented) | rate-limited |
| wq-core-web-vitals | `afa8da9` | rate-limited | same |
| wq-performance | `afa8da9` | rate-limited | same |
| wq-seo | `afa8da9` | rate-limited | same |
| wq-web-quality-audit | `afa8da9` | rate-limited | same |
| writing-for-agents | `c55ee46` | rate-limited | same |

**Totals (24 readable of 29):** 20 faithful · 4 differ by a documented adaptation · 0 undocumented drift ·
**4 vendors where upstream moved past the pin** · 5 unread (the unauthenticated API allows ~60 calls/hour and this
sweep needs two per vendor).

## What this changed

- The six `wq-*` REVIEW records each said *"frontmatter `name` alanı orijinal kaldı"* (the `name` field stayed
  original). **That was wrong** — all six carry `name: wq-…`, and the sweep proves the pin difference is exactly that
  one line. The records were corrected on 2026-10-16.
- No undocumented drift anywhere: every difference between our copy and its pin now has a written reason.

## Open decisions (not actions)

The four moved vendors stay on their pins until someone decides to bump. A bump is a full intake again:
`skill-audit.sh` → read the diff by hand → update `REVIEW.md` (new commit + what changed) → `gen-manifest.sh`.
`design-taste-frontend`, `minimalist-ui` and `redesign-existing-projects` all come from the same upstream repo
(`Leonxlnx/taste-skill`), so one review covers the three.

## Re-running

`python scripts/pin-sweep.py` (stdlib only, report-only; `--json` for the raw rows). It reads the `| Kaynak |` row of
each `REVIEW.md`, then asks the GitHub contents API for the blob at the pinned commit and at HEAD — two calls per
vendor. The unauthenticated limit is about 60 calls/hour, which is why 5 rows above are unread; set `GITHUB_TOKEN`
to get the full table. Exit code 2 means a difference exists that no `REVIEW.md` explains.
