## FixedForm.tsx  ·  Kullanıcılar: veliler — mobil, ilk kez (tekrar: dönemde bir)  ·  Dil: Türkçe  ·  **Statik denetim** (render yok)

Bağlam: kullanıcı tarafından verildi (veliler, mobil, ilk kez); dosyadaki metinler ve adlar ("Öğrenci Kayıt", "Veli e-postası") bunu doğruluyor. Tek seferlik akış → H7 (uzman kısayolu) baskısı düşük; öncelik anlaşılır etiket, doğru mobil klavye ve net hata metni.

### Bulgular (şiddete göre)
İhlal yok. A1–A13 ve U1–U8 içinde kaynak dosyada çiğnenen kural bulunmadı; 5 madde kanıtı CSS / sayfa kabuğunda olduğu için doğrulanamaz (aşağıda ve İnsan TODO'da).

Kanıt özeti (uygun hükümlerin dayanağı):
- U1 · H1 — Kaydet/Temizle her durumda `setStatus` üretir (:42, :46, :52) ve `<p role="status" aria-live="polite">` ilk render'dan itibaren DOM'da (:101); İptal gerçek gezinti (`href="/"`, :99).
- U2 · H3 — İptal linki var (:99); kirli formda çıkış uyarısı (`dirty && confirm`, :55–57).
- U3 · H5/H10 — TC: `inputMode="numeric"`, `maxLength={11}`, kalıcı ipucu "11 rakam, boşluksuz." (:87), hata "11 rakamdan oluşmalıdır (örn. …)" (:17); e-posta: `type="email"`, `autoComplete="email"` (:86), hata örnekli (:15). Ne yanlış + nasıl düzelir ikisi de var.
- U4 · H4 — Zorunlu sinyali: etikette `*` (:65) + form başında açıklama (:81); hata sinyali: ⚠ ikon + metin + `aria-invalid` (:67, :69). Tüm alanlar zorunlu ve tümü `*` taşıyor → yönerge gerçek durumla örtüşüyor.
- U5 · H3 — Sıfırlama `confirm` ister (:50); kirli çıkış `confirm` ister (:56).
- U6 · H8 — "Yeni" rozeti "Sınıf listesi 2026-27 dönemine güncellendi" içeriğine bağlı (:104).
- U7 · H6 — Dört alanda kalıcı `<label htmlFor>` (:65); select'teki "Sınıf seçin" seçeneği etiketin yerine geçmiyor (:88–90).
- U8 · H2 — "Kaydet", "Formu temizle", "İptal", "Kayıt koşullarını görüntüle" (:97–99, :104) — hepsi eylemi/hedefi Türkçe söylüyor.
- A2 — Banner görseli süs: `alt=""` (:78).
- A4 — Her denetim `id`/`htmlFor` ile bağlı (:65–66).
- A5 — Hata renk dışı iki sinyal taşıyor (ikon + metin) ve `aria-describedby` ile denetime bağlı (:62, :67, :69).
- A7 — Tüm etkileşimli öğeler native: `input`, `select`, `button`, `a href` (:85–99).
- A8 — Yalnız ikon taşıyan denetim yok; 🗑 yanında görünür metin var (:98).
- A11 — 2×2 küçük tablo elle bakıldı: `caption` (:107), `th scope="col"` (:108), `th scope="row"` (:110–111).
- A13 — Durum mesajı `role="status"` + `aria-live="polite"` (:101); gönderimde odak ilk hatalı alana taşınıyor (:43), alan hataları `aria-describedby` ile okunuyor.

WCAG 2.2 sweep (A-listesi dışı 36 kriter, dosyada ilgili olanlar):
- 1.3.5 Girdi amacı — Veli e-postası `autocomplete="email"` (:86) uygun. "Öğrencinin adı soyadı" ve TC, kullanıcıya (veliye) değil öğrenciye ait → `autocomplete="off"` (:85) kriteri çiğnemez.
- 1.3.3 Duyusal özellikler — Yönerge "Yıldızla (*) işaretli" (:81) şekil/konuma dayanmıyor; uygun.
- 2.4.4 Link amacı — "Kayıt koşullarını görüntüle" → `#detay` bölümü `h2` ile başlıyor (:104, :115–116); uygun.
- 2.5.2 İşaretçi iptali — Eylemler `onClick`/`onSubmit`/`onReset`'te (:84, :99); uygun.
- 3.2.1 / 3.2.2 — `onfocus` yönlendirmesi yok; select `onChange` yalnız state günceller (:33–34); uygun.
- 3.3.3 Hata önerisi — Her hata düzeltme yolu söylüyor (:13–18); uygun.
- 3.3.4 Hata önleme — Yıkıcı eylemler onaylı (:50, :56); gönderim öncesi tüm alanlar istemci tarafında kontrol edilip odak hataya taşınıyor (:40–44). Kayıt "veli onayı ve kontenjan kontrolü sonrası kesinleşir" (:117) → süreçte geri alınabilir; uygun.
- 3.3.8 Erişilebilir kimlik doğrulama — CAPTCHA, yapıştırma engeli yok; uygulanamaz.
- 2.4.2 Sayfa başlığı, 1.4.4 / 1.4.10 / 1.4.12 (render), 2.1.2 (render) → İnsan TODO.

İhlal sayılmayan iyileştirme notu (şiddet 1): :98 `🗑` emojisi `aria-hidden` taşımıyor; ekran okuyucu düğme adını "çöp kutusu Formu temizle" diye okur. `<span aria-hidden="true">🗑 </span>Formu temizle` ile gürültü kalkar. Görünür metin erişilebilir adın içinde olduğu için 2.5.3 sağlanıyor; A8 hükmü değişmez.

### Kontrol listesi hükümleri
A1 doğrulanamaz (tek `h1` :76, `h2` :116, `main` :75 uygun; atlama linki sayfa kabuğunda) · A2 uygun · A3 doğrulanamaz (CSS; tek inline kanıt :80 `#4a4a4a`/`#fff` = 8,9:1 geçer; ipucu/hata/rozet/buton renkleri dosyada yok) · A4 uygun · A5 uygun (gövde linki :104 alt çizgisi tarayıcı varsayılanı; CSS kaldırmadıysa geçer → TODO) · A6 doğrulanamaz (CSS; kaynakta `onfocus=blur` yok, programatik odak :43 doğru) · A7 uygun · A8 uygun (🗑 metinle birlikte, bkz. not) · A9 doğrulanamaz (CSS; `.actions` içindeki İptal linki :99 inline metin değil, 24×24 hedefi CSS'e bağlı) · A10 uygulanamaz (hareket/animasyon yok) · A11 uygun · A12 doğrulanamaz (`html lang` sayfa kabuğunda; dil değişen parça yok) · A13 uygun
U1 uygun · U2 uygun · U3 uygun · U4 uygun · U5 uygun · U6 uygun · U7 uygun · U8 uygun

Sayım: ihlal 0 · uygun 15 · uygulanamaz 1 · doğrulanamaz 5

### Klavye gezintisi
render yok — statik denetim. Kaynaktan beklenen Tab sırası (DOM = görsel sıra, CSS `order`/`float` yok): Öğrencinin adı soyadı → Veli e-postası → TC Kimlik No → Sınıf → Kaydet → Formu temizle → İptal → "Kayıt koşullarını görüntüle". Tüm hedefler native öğe, `tabIndex` müdahalesi yok; başarısız gönderimde odak ilk hatalı alana gider (:43). `confirm()` native diyaloğu klavye tuzağı oluşturmaz. Odak görünürlüğü ve gerçek sıra render ile doğrulanmalı.

### İnsan için TODO
- **A1 (doğrulanamaz)** — Sayfa kabuğunda (layout/App) "İçeriğe geç" atlama linki var mı; tekrarlayan üst blok varsa gerekli.
- **A3 (doğrulanamaz)** — CSS'te `.hint`, `.error`, `.badge`, `.status`, buton ve link renklerinin kontrastı: metin ≥ 4,5:1, UI/ikon ≥ 3:1. Özellikle `.hint` gri ve `.badge` üstündeki metin.
- **A5 (not)** — CSS `a { text-decoration: none }` içermiyorsa :104 linki geçer; içeriyorsa alt çizgi ya da renk dışı ayırt edici ekle.
- **A6 (doğrulanamaz)** — CSS'te `outline: none` var mı; varsa `:focus-visible` ile ≥ 3:1 kontrastlı gösterge tanımlı mı. Harici klavye ile Tab gezintisinde odak her adımda görünür mü.
- **A9 (doğrulanamaz)** — `.actions` içindeki üç hedef (özellikle `a.cancel`) ≥ 24×24 CSS px mi; mobil için 44×44 önerilir.
- **A12 (doğrulanamaz)** — `index.html`'de `<html lang="tr">` var mı.
- **2.4.2** — `<title>` sayfayı ve siteyi tanımlıyor mu (ör. "Öğrenci Kayıt · Okul Adı").
- **Ekran okuyucu (NVDA/VoiceOver, mobilde TalkBack/VoiceOver)** — Etiketler "zorunlu" ile birlikte okunuyor mu (etiketteki `*` + `aria-required` çift bildirim yaratıyorsa `*`'ı `aria-hidden` span'e al); alan terk edilince hata `aria-describedby` ile okunuyor mu; gönderimde `role="status"` mesajı duyuruluyor mu; tablo başlıkları hücrelerle birlikte okunuyor mu.
- **%200 yakınlaştırma ve 320 px genişlik (1.4.4 / 1.4.10)** — 320 px banner görseli (`width={320}`) taşma yapıyor mu; `.actions` üç hedefi yatay kaydırmasız sığıyor mu; hata metinleri kırpılıyor mu.
- **1.4.12 metin aralığı** — Satır/harf aralığı artırılınca etiket ve hata metinleri üst üste biniyor mu.
- **Gerçek kullanıcı testi** — Bir veli, mobil cihazda ilk kez, yardımsız: öğrenci adı + e-posta + TC + sınıf girip "Kayıt alındı" mesajını görüyor mu; TC'ye 10 rakam girip hata metnini anlayıp düzeltebiliyor mu; "Formu temizle" onayını anlıyor mu.