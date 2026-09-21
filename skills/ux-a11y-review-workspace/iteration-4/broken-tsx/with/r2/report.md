## BrokenForm.tsx  ·  Kullanıcılar: veliler · mobil · ilk kez · tek seferlik (yılda bir kayıt)  ·  Dil: Türkçe  ·  Statik denetim (render yok)

Bağlam: Öğrenci kayıt formu. Kullanıcı grubu formu telefondan, ilk ve muhtemelen tek kez dolduran veliler; deneyimsiz, tekrar sıklığı düşük. Bu yüzden H7 (uzman kısayolları) ikincil; kalıcı etiket, format ipucu, büyük dokunma hedefi ve görünür sonuç birincil.

### Bulgular (şiddete göre)

BrokenForm.tsx:17 — A7 · WCAG 2.1.1 · 4.1.2 · şiddet 4 — Ana eylem "Kaydet" `div` + `onClick`; klavye/ekran okuyucu için erişilemez, rolü yok, `onClick` boş → `<button type="submit">Kaydet</button>` yap ve `<form onSubmit>` içine al.
BrokenForm.tsx:17 — U1 · H1 · şiddet 4 — "Kaydet" hiçbir görünür sonuç üretmiyor (bekleme yok, mesaj yok, yönlendirme yok) → gönderimde "Kaydediliyor…" ve sonunda `role="status"` ile "Kayıt alındı. Onay e-postası gönderildi." / "Kayıt yapılamadı: kimlik numarası alanını düzeltin." göster.
BrokenForm.tsx:3 — H4 · H5 · WCAG 3.3.4 · şiddet 3 — Alanlar `<form>` içinde değil; mobil klavyedeki "Git/Enter" göndermez, `required`/native doğrulama çalışamaz, gönderim öncesi kontrol adımı yok → kök `div`i `<form onSubmit={…}>` yap (native doğrulamayı `noValidate` ile kapatıyorsan hata metnini kendin `aria-describedby` + `role="status"` ile göster), gönderim öncesi özet/onay göster.
BrokenForm.tsx:9 — A4 · WCAG 1.3.1 · 3.3.2 · şiddet 3 — Ad Soyad, E-posta (:10), TC Kimlik No (:11) ve sınıf `select` (:12) yalnız placeholder/ilk seçenek ile adlandırılmış; programatik etiket yok → her denetime `id` ve `<label htmlFor="…">` ekle (`<label htmlFor="adSoyad">Ad Soyad *</label>`, `<label htmlFor="sinif">Sınıf</label>`).
BrokenForm.tsx:9 — U7 · H6 · şiddet 3 — Placeholder etiket yerine geçiyor; veli yazmaya başlayınca alan adı kaybolur (:9–:13) → kalıcı `<label>` ekle; placeholder'ı yalnız örnek için kullan ("örn. Ayşe Yılmaz").
BrokenForm.tsx:11 — U3 · H5 · H10 · WCAG 3.3.3 · şiddet 3 — TC Kimlik No `type="text"`, `inputMode` yok, uzunluk sınırı yok, format ipucu/örnek yok, hata metni hiç yok → `inputMode="numeric" pattern="[0-9]{11}" maxLength={11} autoComplete="off"`, etiket altına "11 rakam (örn. 12345678901)" ipucu, hata metni "Kimlik numarası 11 rakam olmalı (örn. 12345678901)" + `aria-invalid` + `aria-describedby`.
BrokenForm.tsx:7 — U4 · H4 · şiddet 3 — Yönerge "tüm alanları doldurun" derken yalnız bir alan (:11) işaretli; hiçbir alanda `required`/`aria-required` yok; zorunlu işareti (kırmızı kenarlık) hata işaretiyle aynı sinyal → etiket sonuna `*`, form başına "* ile işaretli alanlar zorunludur", alanlara `required`; hatayı kırmızı kenarlık + ikon + alan altı metinle ayrı sinyal yap.
BrokenForm.tsx:11 — A5 · WCAG 1.4.1 · 3.3.1 · 1.3.3 · şiddet 3 — Zorunluluk yalnız renkle (kırmızı kenarlık) iletiliyor; :7 yönergesi de yalnız renge dayanıyor ("kırmızı ile işaretlidir") → yönergeyi "* ile işaretli alanlar zorunludur" yap; hata durumunda `aria-invalid="true"` + `aria-describedby="tc-hata"` + metin + ikon.
BrokenForm.tsx:6 — A3 · WCAG 1.4.3 · şiddet 3 — Yönerge metni `#9a9a9a` / `#fff` ≈ 2,8:1 (<4,5:1); veli için tek yönerge güneşte okunmaz → `#595959` (≈7:1) ya da en az `#767676` (≈4,5:1) kullan.
BrokenForm.tsx:12 — A6 · WCAG 2.4.7 · şiddet 3 — `select` üzerinde `outline: 'none'`; klavye odağı görünmez → inline stili kaldır, `:focus-visible { outline: 3px solid <marka rengi>; outline-offset: 2px }` (≥3:1) ver.
BrokenForm.tsx:18 — A8 · WCAG 4.1.2 · 2.5.3 · şiddet 3 — Yalnız emoji (🗑) taşıyan butonun erişilebilir adı yok → `aria-label="Formu temizle"` ekle (emoji'ye `aria-hidden="true"`).
BrokenForm.tsx:18 — U5 · H3 · şiddet 3 — Tüm alanları onaysız, geri alınamaz siler; ayrıca yalnız `input`ları temizler, `select` kalır (H4 tutarsızlık) → onay iste ("Girdiğiniz bilgiler silinsin mi?") ya da 5–10 sn geri alma; temizlemeyi React state ile yap ve `select`i de sıfırla.
BrokenForm.tsx:19 — A9 · WCAG 2.5.8 · şiddet 3 — `<a href="#sil">x</a>` 16×16 px, 10 px yazı; mobilde dokunulamaz → en az 24×24 (tercihen 44×44) hedef, `min-width/min-height`, `display:inline-flex`.
BrokenForm.tsx:19 — U2 · H3 · şiddet 2 — Akıştan etiketli çıkış yolu yok (İptal / Geri); tek aday "x" linki hedefini söylemiyor, `#sil` hedefi yıkıcı olabilir → `<button type="button">İptal</button>` ekle; yarım veri varsa çıkışta "Girdiğiniz bilgiler kaybolacak" uyarısı.
BrokenForm.tsx:18 — A13 · WCAG 4.1.3 · şiddet 2 — Temizleme ve gönderim sonucunda hiçbir canlı bölge yok; ekran okuyucu değişimi duymaz → `<p role="status" aria-live="polite">` ile "Form temizlendi" / "Kayıt alındı" duyur.
BrokenForm.tsx:4 — A1 · WCAG 1.3.1 · 2.4.6 · şiddet 2 — Başlık `div` + `fontSize:28`; `h1` yok, hiyerarşi yok → `<h1>Öğrenci Kayıt</h1>` yap (görsel boyutu CSS'te ver).
BrokenForm.tsx:5 — A2 · WCAG 1.1.1 · şiddet 2 — `img` `alt` özniteliği yok; ekran okuyucu dosya adını okur → süs görselse `alt=""`, okul görseli anlam taşıyorsa `alt="… Okulu ana bina"`.
BrokenForm.tsx:21 — A11 · WCAG 1.3.1 · şiddet 2 — 2×2 not tablosunda `caption` ve `th` yok (axe bu boyutta yakalamaz); hücre "85"in neyin notu olduğu programatik olarak belirsiz → `<caption>Son sınav notları</caption>`, `<thead><tr><th scope="col">Ders</th><th scope="col">Not</th></tr></thead>`, ders adlarına `<th scope="row">`.
BrokenForm.tsx:27 — U8 · H2 · WCAG 2.4.4 · şiddet 2 — "buraya tıklayın" hedefi söylemiyor; :19 "x" ve :18 "🗑" de eylemi söylemiyor → "Kayıt koşullarını görüntüle" / "Not detaylarını görüntüle"; "x" yerine "Kaydı iptal et".
BrokenForm.tsx:20 — U6 · H8 · şiddet 2 — "Yeni!" rozeti hiçbir içeriğe bağlı değil, `pulse` sınıfı sürekli dikkat çekiyor → "Yeni: 2026 kayıt koşulları güncellendi" gibi bağlamlı metin; bağlam yoksa kaldır.
BrokenForm.tsx:9 — WCAG 1.3.5 · şiddet 2 — Kişisel alanlarda `autoComplete` yok (:9 ad, :10 e-posta); mobilde otomatik doldurma çalışmaz → `autoComplete="name"`, `autoComplete="email"`.
BrokenForm.tsx:20 — WCAG 4.1.2 (ARIA kullanımı) · şiddet 1 — `aria-hidden="false"` etkisiz/yanıltıcı öznitelik → kaldır.

### Kontrol listesi hükümleri
A1 ihlal :4 · A2 ihlal :5 · A3 ihlal :6 · A4 ihlal :9 · A5 ihlal :11 · A6 ihlal :12 · A7 ihlal :17 · A8 ihlal :18 · A9 ihlal :19 · A10 doğrulanamaz (`.pulse` animasyonu CSS'te) · A11 ihlal :21 · A12 doğrulanamaz (`html lang` layout'ta) · A13 ihlal :18
U1 ihlal :17 · U2 ihlal :19 · U3 ihlal :11 · U4 ihlal :7 · U5 ihlal :18 · U6 ihlal :20 · U7 ihlal :9 · U8 ihlal :27

WCAG 2.2 AA tarama (A-listesi dışı, ilgili olanlar): 1.3.3 ihlal :7 (yalnız renge dayanan yönerge) · 1.3.5 ihlal :9, :10 (autocomplete) · 2.4.4 ihlal :19, :27 · 3.3.3 ihlal :11 (hata önerisi yok) · 3.3.4 ihlal :3 (veri gönderimi öncesi kontrol/onay yok) · 4.1.2 ihlal :20 (`aria-hidden="false"`) · 2.4.2 doğrulanamaz (`<title>` layout'ta) · 1.4.10 doğrulanamaz (320 px sabit `img` reflow — render gerekir) · 1.2.x, 2.1.4, 2.2.1, 2.5.1, 2.5.7, 3.3.7, 3.3.8 uygulanamaz.

### Klavye gezintisi
render yok — statik denetim. Kaynaktan öngörü: Tab sırası :9 → :10 → :11 → :12 → :18 (🗑) → :19 (x) → :27; "Kaydet" (:17) sıraya hiç girmez — formun ana eylemi klavyeyle ulaşılamaz. `select` (:12) odak alır ama gösterge yok (outline kapalı). Klavye tuzağı yok.

### İnsan için TODO
- A10 · `.pulse` (:20) keyframe'lerini CSS'te kontrol et: 5 sn'den uzun sürekli animasyonsa durdurma yolu ekle, `prefers-reduced-motion: reduce` için kapat; saniyede 3'ten fazla yanıp sönmediğini doğrula.
- A12 · Layout/`index.html` içinde `<html lang="tr">` var mı; 2.4.2 · `<title>` sayfayı tanımlıyor mu ("Öğrenci Kayıt — <site adı>").
- A9 · `.icon-only` (:18) ve `.fake-btn` (:17) boyutlarını CSS'te ölç: ≥24×24, mobil için 44×44 hedefle.
- A1 · Sayfa düzeyinde `main` landmark ve tekrarlayan blok için atlama linki var mı.
- A5 · CSS'te gövde metni linklerinin (:27) altı çizili kalıyor mu (`text-decoration: none` verilmiş mi).
- 1.4.10 · 320 px genişlikte sabit 320 px `img` (:5) yatay kaydırma yaratıyor mu; `max-width:100%; height:auto` gerekebilir.
- Ekran okuyucu (NVDA / VoiceOver, Türkçe ses): etiketler eklendikten sonra dört alan adı, tablo başlıkları ve durum duyuruları okunuyor mu; 🗑 emoji ek olarak "çöp kutusu" diye okunmuyor mu.
- %200 yakınlaştırma ve 320 px genişlikte içerik/işlev kaybı var mı.
- Gerçek kullanıcıyla 1 görev: ilk kez kayıt yapan bir veli, telefonda, yardımsız "çocuğunu 5. sınıfa kaydet" akışını tamamlayıp sonucu anlayabiliyor mu (özellikle TC Kimlik No hatasını düzeltebiliyor mu).