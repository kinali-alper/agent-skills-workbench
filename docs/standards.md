# Standart referansları (2026-09)

- **WCAG 2.2** — hedef seviye AA. https://www.w3.org/TR/WCAG22/
- **EN 301 549 v4.1.1** — AB teknik standardı, WCAG 2.2'yi içerir (Eylül 2026)
- **EAA** — Avrupa Erişilebilirlik Yasası, Haz 2025'ten beri yürürlükte
- **WCAG 3.0** — Working Draft; yasal referans değil; APCA yalnız "ekstra"
- **ARIA APG** — bileşen desenleri. https://www.w3.org/WAI/ARIA/apg/
- **Nielsen 10 heuristik** — kullanılabilirlik değerlendirme çerçevesi
- Kontrast eşikleri (2.2 AA): metin 4.5:1, büyük metin / UI bileşeni / grafik 3:1
- Hedef boyutu (2.5.8, AA): en az 24×24 CSS px
- Focus görünürlüğü (2.4.11, AA): odak göstergesi gizlenemez

## Skill yazım kuralları (writing-for-agents'tan, kendi skill'lerimiz için)
- **Description = context pointer**: ilk kelime tetikleyici; her dal için tek tetikleyici; eş anlamlı yığmak yok.
- **Bilgi hiyerarşisi**: adımlar üstte → dosya içi referans → ayrı dosyaya itilmiş referans (yalnız bazı dalların ihtiyacı olanı it).
- **Tamamlama kriteri** her adımda: "her kural uygulandı", "tabloda 9 satırın hepsi değerlendirildi" gibi kontrol edilebilir ve kapsayıcı.
- **Olumlu kural**: "outline kaldırma" değil → ":focus-visible ile görünür odak ver". Yasak yalnız kaçınılmazsa, yanında olumlu hedefle.
- **Leading word**: modelin zaten bildiği yoğun kavramlar (POUR, landmark, focus ring, hit target). Uydurma terim yerine mevcut terim.
- **Budama**: ortamın söylediğini tekrarlama (package.json, config); no-op cümleyi tamamen sil; tek doğruluk kaynağı.
- **Model- vs user-invoked**: ajan kendi başına ulaşmalıysa description'lı; yalnız elle çağrılacaksa `disable-model-invocation: true` (context maliyeti sıfır).

## Eval formatı (skill-creator ile hizalı)
- Skill içi: `skills/<ad>/evals/evals.json` → `{skill_name, evals:[{id, prompt, expected_output, files, expectations[]}]}`
- Sonuçlar: `skills/<ad>-workspace/iteration-N/<eval-name>/{with_skill,without_skill}/` + `grading.json` (`text/passed/evidence`)
- Ortak malzeme: `evals/cases/<vaka>/` (hatalı dosyalar + karne `expected.md`); evals.json `files` alanı buraya işaret eder.

## Animasyon performansı (emilkowalski cheatsheet, 2026-09) — erişilebilirlikle kesişim
transform/opacity dışını animasyonlama · `transition: all` yerine özellik listesi · animasyonlu blur < 20px · uzun liste → sanallaştır ·
React'te her karede state değil `ref.current.style` · `will-change` yalnız görülen 1px kayma için. Kaynak: gsap-performance, motion-design, web-design-guidelines.
