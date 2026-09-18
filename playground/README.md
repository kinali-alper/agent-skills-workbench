# playground

Skill ve araç laboratuvarı. **Yalnız test amaçlı** — buradaki React+Vite seçimi skill'leri bağlamaz.

- `?page=broken` — bilerek 13 WCAG hatası (`src/pages/BrokenForm.tsx`, düzeltme!)
- `?page=fixed` — aynı formun AA uyumlu hali (`src/pages/FixedForm.tsx`)

```bash
npm run dev            # http://localhost:5173  (Claude: preview_start "playground")
npm run test:a11y      # Playwright + axe-core, WCAG 2.x A/AA + 2.2 AA + best-practice
npm run lh -- broken   # Lighthouse accessibility (sunucu açıkken)
```
Raporlar `reports/` altına düşer (git dışı). Beklenen bulgular: `../evals/cases/broken-form/expected.md`

Not: Playwright `channel: 'chrome'` ile sistemdeki Chrome'u kullanır; Chromium indirmek isterseniz `playwright.config.ts`'te bu satırı kaldırın.
