# History

- **2026-09-17** — Repository founded. Security intake pipeline (`skill-audit.sh`, `install.sh`, `vendor/*/REVIEW.md`).
  14 existing design/motion skills audited and vendored. Playground (Vite + Playwright + axe + Lighthouse) with a
  deliberately broken Turkish school-registration form: 13 WCAG 2.2 defects; axe caught 4, Lighthouse scored it 84/100.
- **2026-09-18** — Accessibility skills vendored (Vercel web-design-guidelines, addyosmani web-quality-skills).
  Both scored 8/9 on the automated-tool blind spots; both missed table headers. Plain-HTML and Razor twins added —
  same findings on all three stacks. UX leg: szilu ux-designer + Owl-Listener heuristic-evaluation vendored;
  6 Nielsen defects added to the fixture; heuristic-evaluation 6/6, Vercel 2/6.
  `ux-a11y-review` drafted (orchestrator over the vendored skills + gap checks), evaluated over two iterations with
  fresh isolated subagents — see `skills/ux-a11y-review-workspace/RESULTS.md`. Published.
- **2026-09-18 (later)** — Real-page test on W3C WAI's intentionally inaccessible "CityLights" demo: 15/19 AA criteria
  found, 2 partial, 2 missed (1.4.1 colour-only links, 2.4.1 skip link). Browser step (Tab-through) produced the
  severity-4 finding. Checklist widened (A1, A5, A6) on that evidence; negative control re-run (iteration-3).
