import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'
import { mkdirSync, writeFileSync } from 'node:fs'

const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']

async function scan(page: import('@playwright/test').Page, name: string) {
  const results = await new AxeBuilder({ page }).withTags(TAGS).analyze()
  mkdirSync('reports', { recursive: true })
  writeFileSync(`reports/axe-${name}.json`, JSON.stringify(results, null, 2))
  const summary = results.violations.map(v =>
    `${v.impact?.padEnd(8)} ${v.id.padEnd(28)} x${v.nodes.length}  ${v.help}`)
  console.log(`\n[${name}] ${results.violations.length} ihlal, ${results.passes.length} geçti\n` + summary.join('\n'))
  return results
}

test('broken: ihlaller yakalanmalı', async ({ page }) => {
  await page.goto('/?page=broken')
  const r = await scan(page, 'broken')
  expect(r.violations.length).toBeGreaterThan(0)
})

test('fixed: sıfır ihlal', async ({ page }) => {
  await page.goto('/?page=fixed')
  const r = await scan(page, 'fixed')
  expect(r.violations, JSON.stringify(r.violations.map(v => v.id))).toHaveLength(0)
})

test('fixed: klavye ile tüm form gezilebilir', async ({ page }) => {
  await page.goto('/?page=fixed')
  const focusable = ['ad', 'eposta', 'tc', 'sinif']
  await page.locator('#ad').focus()
  for (const id of focusable.slice(1)) {
    await page.keyboard.press('Tab')
    await expect(page.locator(`#${id}`)).toBeFocused()
  }
})

test('broken.html (düz HTML ikizi): axe aynı ihlalleri bulmalı', async ({ page }) => {
  await page.goto('/broken.html')
  const r = await scan(page, 'broken-html')
  const ids = r.violations.map(v => v.id).sort()
  // TSX sürümünde bulunan çekirdek kural seti — stack fark etmemeli
  for (const must of ['color-contrast', 'image-alt', 'select-name', 'page-has-heading-one'])
    expect(ids, `${must} eksik`).toContain(must)
})

test('fixed: Kaydet görünür durum mesajı verir (H1), 🗑 onay ister (H3)', async ({ page }) => {
  await page.goto('/?page=fixed')
  await page.locator('#ad').fill('Ayşe Yılmaz')
  await page.locator('#eposta').fill('ayse@ornek.com')
  await page.locator('#tc').fill('12345678901')
  await page.locator('#sinif').selectOption({ label: '5. Sınıf' })
  await page.getByRole('button', { name: 'Kaydet' }).click()
  await expect(page.getByRole('status')).toContainText('Kayıt alındı')
  let asked = false
  page.once('dialog', d => { asked = true; d.dismiss() })
  await page.getByRole('button', { name: 'Formu temizle' }).click()
  expect(asked, 'onay kutusu çıkmadı').toBe(true)
})

test('broken: Kaydet hiçbir geri bildirim vermez (U1)', async ({ page }) => {
  await page.goto('/?page=broken')
  await page.getByText('Kaydet').click()
  await expect(page.getByRole('status')).toHaveCount(0)
  await expect(page.getByRole('alert')).toHaveCount(0)
})
