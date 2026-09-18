// Kullanım: node scripts-lighthouse.mjs [broken|fixed]   (dev sunucusu 5173'te çalışıyor olmalı)
import lighthouse from 'lighthouse'
import { launch } from 'chrome-launcher'
import { mkdirSync, writeFileSync } from 'node:fs'

const page = process.argv[2] ?? 'broken'
const chrome = await launch({ chromeFlags: ['--headless=new'] })
const { lhr, report } = await lighthouse(`http://localhost:5173/?page=${page}`, {
  port: chrome.port, output: 'json', onlyCategories: ['accessibility', 'best-practices'],
})
await chrome.kill()
mkdirSync('reports', { recursive: true })
writeFileSync(`reports/lighthouse-${page}.json`, report)
const a11y = lhr.categories.accessibility
console.log(`[${page}] Lighthouse accessibility: ${Math.round(a11y.score * 100)}/100`)
for (const ref of a11y.auditRefs) {
  const a = lhr.audits[ref.id]
  if (a.score !== null && a.score < 1) console.log(`  FAIL ${a.id.padEnd(30)} ${a.title}`)
}
