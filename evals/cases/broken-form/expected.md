# broken-form — beklenen bulgular

İki bölüm: **A** erişilebilirlik (WCAG 2.2), **U** kullanılabilirlik (Nielsen heuristikleri). Aynı dosyalar, aynı satırlar; bazı satırlar çift kodlu.

Kaynak: `playground/src/pages/BrokenForm.tsx` · Düzeltilmiş: `FixedForm.tsx`
Ölçüm (2026-09-17): axe-core 4.13 → 6 ihlal · Lighthouse 12.8 → 84/100 (3 fail)

> **Fixture'larda açıklama yorumu yok** (2026-09-18'de silindi): cevap anahtarı yalnız bu dosyadır. Skill testleri
> skill-creator yöntemiyle **taze bağlamlı alt-ajanla** (with-skill / without-skill) yapılır; aşağıdaki tablolardaki
> skill skorları o tarihten önce **cevap anahtarı görünürken, satır içi** alınmıştır → *kural setinin kapsamını* gösterir,
> taze bir ajanın *bulma oranını* değil. "Gösterge niteliğinde" okunmalı.

| F# | Yerleştirilen hata | WCAG 2.2 | SKILL.md id | axe | Lighthouse | wq-a11y | Vercel | Kim yakalar? |
|---|---|---|---|---|---|---|---|---|
| F1 | Başlık `div` ile yapılmış, `h1` yok | 1.3.1, 2.4.6 | A1 | ✅ page-has-heading-one | ❌ | ✅ | ✅ | otomatik |
| F2 | Bilgi taşıyan görselde `alt` yok | 1.1.1 | A2 | ✅ image-alt | ✅ | ✅ | ✅ | otomatik |
| F3 | Metin kontrastı ~2.3:1 | 1.4.3 | A3 | ✅ color-contrast | ✅ | ✅ | ✅ | otomatik |
| F4 | Ad/E-posta input'larında `label` yok, yalnız placeholder | 1.3.1, 3.3.2 | A4 · U7 | ❌ | ❌ | ✅ | ✅ | **skill/insan** — axe placeholder'ı erişilebilir isim sayar; ama placeholder yazınca kaybolur, ekran okuyucu bağlamı düşer |
| F5 | Hata yalnız kırmızı kenarlıkla bildiriliyor | 1.4.1, 3.3.1 | A5 | ❌ | ❌ | ✅ | ✅ | **skill/insan** — renk körü kullanıcı hatayı göremez; metin gerekir |
| F6 | `select`'te `outline: none` | 2.4.7, 2.4.11 | A6 | ❌ | ❌ | ✅ | ✅ | **skill/insan** — odak durumu statik taramada görünmez |
| F7 | `select` etiketsiz | 4.1.2 | A4 | ✅ select-name | ✅ | ✅ | ✅ | otomatik |
| F8 | `div` + onClick ile buton: Tab ile erişilemez, rolü yok | 2.1.1, 4.1.2 | A7 | ❌ | ❌ | ✅ | ✅ | **skill/insan** — axe rolü olmayan div'i denetlemez; klavye testi şart |
| F9 | Yalnız emoji içeren buton (🗑) | 4.1.2, 2.5.3 | A8 | ❌ | ❌ | ✅ | ✅ | **skill/insan** — emoji "wastebasket" diye okunur, işlev ("temizle") anlaşılmaz |
| F10 | 16×16 px tıklama hedefi | 2.5.8 | A9 | ❌ | ❌ | ✅ | ✅ | **skill/insan** — axe target-size etrafında boşluk varsa istisna uygular |
| F11 | Sonsuz `pulse` animasyonu, `prefers-reduced-motion` yok | 2.3.3 | A10 | ❌ | ❌ | ✅ | ✅ | **skill/insan** — CSS animasyonu otomatik denetlenmez |
| F12 | Tablo `th`/`caption` yok | 1.3.1 | A11 | ❌ | ❌ | ❌ | ❌ | **skill/insan** — axe küçük tabloları (3×3 altı) denetlemez |
| F13 | "buraya tıklayın" link metni | 2.4.4 | U8 | ❌ | ❌ | ✅ | ✅ | **skill/insan** — link-name yalnız *var mı* bakar, anlamlı mı bakmaz |
| — | `main` landmark yok, içerik landmark dışında | 1.3.1 (best-practice) | A1 | ✅ landmark-one-main, region | ❌ | ✅ | ✅ | otomatik |

**Skor:** 13 yerleştirilen hatadan otomatik araçlar **4**'ünü yakaladı (%31; F1, F2, F3, F7). Lighthouse 84/100 verdi.
→ "Lighthouse yeşil = erişilebilir" **yanlıştır**. Skill'imizin asıl değeri 9 kaçırılan satırda.

## Skill geçme kriteri

> **iteration-1 sonrası not (2026-09-18):** Taze ajan, skill'siz de F1–F19'un 18'ini buldu (yalnız F15/U2 kaçtı, 3/3 fixture'da tutarlı).
> Bu fixture artık *bulma* konusunda ayırt etmiyor; asıl kapılar **negatif kontrol** (temiz forma hata uydurmama) ve **gerçek sayfa**
> (tarayıcıda Tab gezintisi — adım 4). Skill'in ölçülen katkısı: 21/21 açık hüküm, tutarlı biçim, 3-5× kısa rapor, stack reçetesi, zorunlu klavye/TODO adımı.
Skill BrokenForm.tsx'i incelediğinde F4, F5, F6, F8, F9, F10, F11, F12, F13 satırlarının **en az 7'sini** raporlamalı; uydurma bulgu eklememeli.

## Skill sonuçları (satır içi, cevap anahtarı görünür — gösterge niteliğinde; puanlar eski "9 kör nokta" = F4,F5,F6,F8,F9,F10,F11,F12,F13)

| Skill | 9 kör noktadan | Sonuç | Tarih | Not |
|---|---|---|---|---|
| wq-accessibility (addyosmani) | **8/9** | GEÇTİ | 2026-09-18 | Tek boşluk: tablo (`th`/`caption`) kuralı skill'de yok. Uydurma bulgu yok. WCAG no + gerekçe verir. |
| web-design-guidelines (Vercel) | **8/9** | GEÇTİ | 2026-09-18 | Aynı boşluk: tablo. Ek yakaladığı: autocomplete/name/spellCheck, inputMode, placeholder "…" — form UX katmanı. Kurallar web'den çekilir; snapshot vendor/'da. |

## Kendi skill'imize (ux-a11y-review) girecek boşluklar
- Tablo: `th scope`, `caption`; küçük tabloların axe'ten kaçtığı notu
- Emoji-buton için açık ❌/✅ örneği (eğitim arayüzlerinde emoji yaygın)
- Türkçe link metni örnekleri: "buraya tıklayın", "devamı", "tıkla" ❌
- Türkçe form bağlamı: kimlik no (11 hane, inputmode=numeric), sınıf seçimi, veli/öğrenci rolleri

## U — Kullanılabilirlik hataları (Nielsen)

Otomatik araçların (axe, Lighthouse) hiçbiri bu satırları **tasarım gereği** göremez: davranış ve anlam hatası, işaretleme hatası değil. Sütunlar bu yüzden yok; yalnız skill/insan.

| F# | Yerleştirilen hata | Heuristik | SKILL.md id | Nerede |
|---|---|---|---|---|
| F14 | Kaydet'e basınca hiçbir görünür geri bildirim yok (başarı/hata mesajı, yönlendirme yok) | H1 durum görünürlüğü | U1 | TSX:18 · cshtml:24 |
| F15 | İptal / geri yolu yok; kullanıcı formdan çıkamaz | H3 kullanıcı kontrolü | U2 | form geneli |
| F16 | TC alanı harf kabul eder; "11 rakam" ipucu yok; ne yanlış olduğu söylenmez | H5 hata önleme · H10 yardım | U3 | TSX:12 · cshtml:20 |
| F17 | Metin "zorunlu alanlar kırmızı ile işaretlidir" der; kırmızı olan tek alan aslında HATA durumu; zorunlu (*) işareti hiç yok | H4 tutarlılık | U4 | TSX:7 · cshtml:15 |
| F18 | 🗑 tüm formu onay sormadan siler, geri alma yok | H3 kullanıcı kontrolü | U5 | TSX:19 · cshtml:25 |
| F19 | "Yeni!" rozeti neyin yeni olduğunu söylemez, hiçbir içeriğe bağlı değil | H8 minimalizm | U6 | TSX:21 · cshtml:28 |

**Çift kodlu fixture satırları:** F4 placeholder-etiket → A4 + U7 (H6) · F5 renk-tek-sinyal → A5 (+H9) · F13 "buraya tıklayın" → U8 (H2).

> **İki numaralama:** F1–F19 = fixture'a **yerleştirilen hatalar** (bu dosya). A1–A13 / U1–U8 = skill'in **kontrol listesi kuralları** (SKILL.md). "SKILL.md id" sütunu ikisini eşler; puanlamada bu sütun kullanılır.

**Geçme kriteri (U):** F14–F19'un en az **5**'i için heuristik adı + sorun + düzeltme önerisi. Şiddet (0-4) verilmesi artı puan.

### U skill sonuçları (2026-09-18 — satır içi, gösterge niteliğinde)

| Skill | 6 U satırından | Sonuç | Not |
|---|---|---|---|
| web-design-guidelines (Vercel) | 2 tam + 1 kısmi | KALDI | U3 (inputmode/örnek/hata-metni), U5 (destructive→confirm) ✅; U1 kısmi (spinner/aria-live var, "başarı mesajı" yok); U2, U4, U6 için kural yok. Form-UX katmanı var, **davranış/anlam** heuristikleri yok. |
| heuristic-evaluation (Owl-Listener) | **6/6** | GEÇTİ | Şiddet 0-4 verdi; çift kodlu A4/A5/A13'ü heuristik diliyle de buldu; fixture dışı 1 ek bulgu (eylem stili tutarsızlığı, H4). 41 satır — Nielsen adları leading word olarak yetiyor. |

**UX boşluğu (ölçülmüş):** Vercel + wq ile U2, U4, U6 açık kalıyor; heuristic-evaluation kapatıyor. Kendi skill'imiz için UX'te yeni kural icat etmek gerekmiyor — Nielsen sürecini **zorunlu adım** yapmak ve Türkçe örnekleri eklemek yetiyor.

**Negatif kontrol (FixedForm) — iteration-1'de KALDI, iki nedenle:** (1) skill'de "bulundu" iki anlamlıydı → hüküm sözlüğü 4 duruma ayrıldı (ihlal/uygun/uygulanamaz/doğrulanamaz); (2) FixedForm'da taze ajanın bulduğu **gerçek buglar** vardı: reset kontrollü `tc` state'ini temizlemiyordu, `noValidate` olmadığından Türkçe hata dalı hiç çalışmıyordu, `#detay` hedefi yoktu, İptal kirli formdan uyarısız çıkıyordu (skill'in kendi U2 kuralı), TC ilk rakamda `role="alert"` ile hata veriyordu. Hepsi düzeltildi; ayrıca `th scope="row"`, süs görsele `alt=""`, ⚠'a `aria-hidden`, etiketlere kimin bilgisi olduğu (öğrenci/veli) eklendi. Önceden kabul edilen tek not: `confirm()` native diyalog (şiddet ≤1). Kriter: **≤2 bulgu, hepsi şiddet ≤1; hiçbir A/U `ihlal` değil.**

FixedForm çözümleri: `role="status"` canlı bölge (U1), İptal bağlantısı (U2), `inputMode/pattern/maxLength` + ipucu metni + örnek (U3), `*` işareti + açıklama (U4), `type="reset"` + `confirm` (U5), "Yeni — Sınıf listesi 2026-27'ye güncellendi" (U6). Playwright testleri U1 ve U5'i doğrular.

## Stack-bağımsızlık kanıtı (2026-09-18)

Aynı 13 hata üç yapıda: `playground/src/pages/BrokenForm.tsx` (React) · `playground/public/broken.html` (düz HTML) · `BrokenForm.cshtml` (ASP.NET Razor, tag helper).

| Yapı | axe ihlal | Vercel kural seti | Boşluk |
|---|---|---|---|
| React TSX | 6 | 8/9 | tablo |
| Düz HTML | 6 (aynı id'ler) | — (axe test `/broken.html`) | tablo |
| Razor .cshtml | (render yok) | 8/9 | tablo |

Razor notu: `asp-for` id/name üretir ama label üretmez → skill "label yok" dedi ve `<label asp-for>` / `<span asp-validation-for>` reçetesi verebildi. Kendi skill'imizde `## Stack notları` altında Razor reçeteleri bu şekilde olacak.
