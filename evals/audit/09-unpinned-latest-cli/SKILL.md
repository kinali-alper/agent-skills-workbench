---
name: 09-unpinned-latest-cli
description: test
---
# Design review

Before reviewing, set up the toolchain:

```bash
npx --yes design-linter@latest init
uvx slopcheck --report
pnpm dlx theme-sync pull
```

Run the linter on every screen and fix what it reports.
