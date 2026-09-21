## BrokenForm.tsx  ·  Kullanıcılar: veliler — mobil, ilk kez kullanan, düşük tekrar (kayıt yılda ~1)  ·  Dil: Türkçe  ·  render yok — statik denetim

Kapsam: tek bileşen dosyası (`BrokenForm.tsx`, 30 satır). CSS (`.broken`, `.fake-btn`, `.icon-only`, `.pulse`), `index.html` ve sayfa iskeleti elde yok; bunlara bağlı hükümler **doğrulanamaz** olarak İnsan TODO'ya yazıldı. Kullanıcı profili gereği hedef boyutu ve verimlilik (H7) kararlarında mobil dokunmatik ekran ve ilk kez kullanan veli esas alındı; kısayol/uzman verimliliği düşük öncelik.

### Bulgular (şiddete göre)

**Şiddet 4 — yayın öncesi zorunlu**

BrokenForm.tsx:17 — A7 · WCAG 2.1.1 · 4.1.2 · şiddet 4 — Formun ana eylemi "Kaydet" bir `div` + `onClick`; klavyeyle odaklanamaz, ekran okuyucuya rol/ad bildirmez, Enter/Space ile çalışmaz → alanları `<form onSubmit={…}>` içine al ve `<button type="submit">Kaydet</button>` kullan; böylece mobil klavyedeki "Git/Enter" de formu gönderir.

BrokenForm.tsx:17 — U1 · H1 · şiddet 4 — "Kaydet" işleyicisi boş (`() => {}`); gönderim ne bekleme göstergesi, ne durum mesajı, ne yönlendirme üretir. İlk kez kullanan veli kaydın alındığını bilemez, tekrar tıklar → gönderim sırasında butonu `disabled` yapıp "Kaydediliyor…" göster; sonuçta `<p role="status">Kayıt alındı. Onay e-postası gönderildi.</p>` ya da onay sayfası; başarısızlıkta "Kayıt yapılamadı: kimlik numarası alanını düzeltin."

**Şiddet 3 — önemli**

BrokenForm.tsx:9 — A4 · WCAG 3.3.2 · 1.3.1 · şiddet 3 — Üç `input` (satır 9–11) ve `select` (satır 12) programatik etikete bağlı değil; ad yalnız placeholder/ilk `option`tan geliyor → her denetime `id` ver ve kalıcı `<label htmlFor="adSoyad">Ad Soyad</label>` ekle (`select` için "Sınıf").

BrokenForm.tsx:9 — U7 · H6 · şiddet 3 — Placeholder etiket yerine kullanılıyor; yazmaya başlayınca "Ad Soyad / E-posta / TC Kimlik No" kaybolur, mobilde alan doluyken hangi kutunun ne olduğu hatırlanamaz → etiket alanın üstünde kalıcı dursun; placeholder yalnız örnek taşısın (`placeholder="örn. Ayşe Yılmaz"`).

BrokenForm.tsx:11 — U3 · H5 · H10 · şiddet 3 — "TC Kimlik No" alanı `type="text"`; mobilde harf klavyesi açılır, format ipucu ve doğrulama yok, hata metni hiç yok → `inputMode="numeric" pattern="[0-9]{11}" maxLength={11} autoComplete="off"` ver; etiket altına ipucu "11 rakam, örn. 12345678901"; hata durumunda alanın altında "Kimlik numarası 11 rakam olmalı (örn. 12345678901)" göster ve `aria-describedby` ile bağla.

BrokenForm.tsx:11 — A5 · WCAG 1.4.1 · 3.3.1 · şiddet 3 — Kırmızı kenarlık tek sinyal: yanında ne metin, ne ikon, ne `aria-invalid` var; renk körü ve ekran okuyucu kullanıcı hiçbir şey algılamaz → durum metni + ikon ekle, `aria-invalid="true"` ve `aria-describedby="tcHata"` bağla; zorunlu için kenarlık rengi yerine etiket sonunda `*` kullan.

BrokenForm.tsx:7 — U4 · H4 · şiddet 3 — Yönerge "tüm alanları doldurun" derken yalnız bir alan (satır 11) işaretli; "zorunlu = kırmızı" denmiş ama kırmızı arayüz geleneğinde **hata** rengidir — zorunlu ve hata sinyali çakışır (ayrıca 1.3.3: yönerge yalnız renge dayanıyor) → zorunlu alanları `required` + etiket sonunda `*` ile işaretle, form başına "* ile işaretli alanlar zorunludur" yaz; hatayı kırmızı kenarlık **+** ikon **+** alan altı metinle göster.

BrokenForm.tsx:4 — A1 · WCAG 1.3.1 · 2.4.6 · şiddet 3 — Sayfa başlığı "Öğrenci Kayıt" yalnız görsel olarak büyütülmüş `div`; başlık ağacı yok, ekran okuyucu başlıklar arasında gezemez → `<h1>Öğrenci Kayıt</h1>` yap (görünümü CSS ile koru). `main` landmark ve atlama linki sayfa düzeyinde → İnsan TODO.

BrokenForm.tsx:5 — A2 · WCAG 1.1.1 · şiddet 3 — `img` `alt` özniteliği yok; ekran okuyucu dosya adını/URL'yi okur → görsel süs ise `alt=""`; okul logosu/bilgi taşıyorsa anlamlı metin (`alt="<Okul adı> logosu"` gibi).

BrokenForm.tsx:6 — A3 · WCAG 1.4.3 · şiddet 3 — Yönerge paragrafı `#9a9a9a` / `#fff` ≈ **2,8:1**, 4,5:1 eşiğinin altında; güneş altında telefonda okunmaz → en az `#767676` (4,54:1), tercihen `#595959` (≈7:1) kullan.

BrokenForm.tsx:12 — A6 · WCAG 2.4.7 · 2.4.11 · şiddet 3 — `select` üzerinde `outline: 'none'`, eşdeğer gösterge yok; klavye kullanıcısı odağın nerede olduğunu göremez → satır içi `outline: none` değerini kaldır; `select:focus-visible { outline: 3px solid #005fcc; outline-offset: 2px }` ver.

BrokenForm.tsx:18 — A8 · WCAG 4.1.2 · 2.5.3 · şiddet 3 — Yalnız 🗑 emojisi taşıyan butonun erişilebilir adı yok; ekran okuyucu "çöp kutusu" ya da hiçbir şey okur, ne yaptığı belirsiz → `aria-label="Formu temizle"` ekle (tercihen görünür metin "Formu temizle"); form içine alınırsa `type="button"` şart.

BrokenForm.tsx:18 — U5 · H3 · şiddet 3 — Tek dokunuşla tüm alanlar silinir; onay ve geri alma yok; mobilde "Kaydet"in hemen yanında duran bu buton yanlışlıkla basılmaya açık → doluysa "Girdiğiniz bilgiler silinecek. Formu temizle / Vazgeç" onayı iste ya da 5–10 sn "Geri al" göster; butonu ana eylemden görsel olarak ayır. (Not: `document.querySelectorAll` ile doğrudan DOM sıfırlama React durumunu atlar ve `select` alanını temizlemez; form durumunu state ile sıfırla.)

BrokenForm.tsx:19 — A9 · WCAG 2.5.8 · şiddet 3 — "x" linki 16×16 px, 10 px yazı; 24×24 asgarinin altında, mobilde parmakla isabet neredeyse imkânsız → `min-width: 44px; min-height: 44px` (en az 24×24) ver, yazı ≥ 16 px; sayfa içi çapa değil eylemse `button` yap.

BrokenForm.tsx:21 — A11 · WCAG 1.3.1 · şiddet 3 — 2×2 not tablosunda `caption`, `thead` ve `th scope` yok; ekran okuyucu "Matematik 85" değerinin ne olduğunu söyleyemez (küçük tablo, axe yakalamaz) → `<caption>Deneme sınavı notları</caption>` ve `<thead><tr><th scope="col">Ders</th><th scope="col">Not</th></tr></thead>` ekle; satır başlarını `<th scope="row">` yap.

**Şiddet 2 — küçük**

BrokenForm.tsx:19 — U2 · H3 · şiddet 2 — Akışta İptal / Geri yok; tek çıkış adayı `href="#sil"` hedefli "x" linki — adı hedefini söylemiyor, yarım veri varken uyarısız → görünür "Vazgeç" butonu ekle (ikincil stil); alanlar doluysa çıkışta "Girdiğiniz bilgiler kaybolacak" uyarısı ver; "x" yerine `aria-label="Kaydı sil"` ya da açık metin.

BrokenForm.tsx:18 — A13 · WCAG 4.1.3 · şiddet 2 — Formu temizleme sessiz gerçekleşir; ekran okuyucu kullanıcısı alanların boşaldığını duymaz; sayfada hiçbir canlı bölge yok → `<div role="status">` içine "Form temizlendi" yaz; aynı bölgeyi gönderim sonucu ve doğrulama mesajları için kullan.

BrokenForm.tsx:20 — U6 · H8 · şiddet 2 — "Yeni!" rozeti hiçbir içeriğe bağlı değil; `pulse` sınıfı sürekli dikkat çekme niyetini gösterir; `aria-hidden="false"` etkisiz/gürültü → rozeti neyin yeni olduğuna bağla ("Yeni: 6. sınıf kontenjanı açıldı") ya da kaldır; `aria-hidden="false"` özniteliğini sil.

BrokenForm.tsx:27 — U8 · H2 · WCAG 2.4.4 · şiddet 2 — "buraya tıklayın" hedefi söylemez; link listesinde anlamsız, mobilde "tıklamak" yok → "Kayıt koşullarını görüntüle" ya da hedefe göre "Kayıt detaylarını görüntüle".

BrokenForm.tsx:9 — WCAG 1.3.5 (sweep) · şiddet 2 — Kişisel alanlarda `autocomplete` ve `name` yok; mobil tarayıcı otomatik doldurma çalışmaz, ilk kez kullanan veli her şeyi elle yazar → `autoComplete="name" name="adSoyad"` (satır 9), `autoComplete="email" name="eposta"` (satır 10).

BrokenForm.tsx:21 — H8 (sweep notu) · şiddet 1 — Kayıt formunda henüz kayıtlı olmayan öğrencinin not tablosu ve ilgisiz "Yeni!" rozeti bulunuyor → kayıt akışıyla ilgisiz içeriği bu ekrandan kaldır.

**WCAG 2.2 sweep — dosyayla ilgili diğer kriterler**
- 3.3.1 / 3.3.3 (hata tanımlama / öneri): dosyada hiçbir doğrulama ve hata metni yok → U3 ve A5 düzeltmeleriyle birlikte kapanır.
- 3.3.4 (hata önleme — veri gönderimi): kayıt bir veri taahhüdü; gönderim öncesi kontrol/onay adımı yok → gönderimden önce özet + "Kaydı onayla" adımı ya da gönderim sonrası düzenleme imkânı.
- 1.3.3 (duyusal özellik): satır 7 yönergesi yalnız renge dayanıyor → U4 düzeltmesiyle kapanır.
- 2.4.2 (sayfa başlığı) `<title>`: bileşen dosyasında görünmez → İnsan TODO.
- `<form>` sarmalayıcısı yok: Enter/"Git" ile gönderim ve tarayıcı doğrulaması (`required`, `pattern`) devre dışı → A7 düzeltmesiyle kapanır.
- 2.5.2, 3.2.1, 3.2.2, 2.1.4, 1.2.x, 2.5.1/2.5.7: ilgili desen dosyada yok, sorun görülmedi.

### Kontrol listesi hükümleri
A1 ihlal :4 · A2 ihlal :5 · A3 ihlal :6 · A4 ihlal :9 · A5 ihlal :11 · A6 ihlal :12 · A7 ihlal :17 · A8 ihlal :18 · A9 ihlal :19 · A10 doğrulanamaz (`.pulse` CSS'i dosyada yok) · A11 ihlal :21 · A12 doğrulanamaz (`html lang` index.html'de) · A13 ihlal :18
U1 ihlal :17 · U2 ihlal :19 · U3 ihlal :11 · U4 ihlal :7 · U5 ihlal :18 · U6 ihlal :20 · U7 ihlal :9 · U8 ihlal :27

### Klavye gezintisi
render yok — statik denetim. Kaynaktan öngörülen Tab sırası: satır 9 (Ad Soyad) → 10 (E-posta) → 11 (TC Kimlik No) → 12 (Sınıf `select`, odak göstergesi **görünmez**) → 18 (🗑, adsız) → 19 ("x", 16 px) → 27 ("buraya tıklayın"). **"Kaydet" (satır 17) klavyeyle hiç ulaşılamaz**; görsel sıra ile odak sırası bu yüzden örtüşmez (Kaydet atlanır, kullanıcı doğrudan silme butonuna düşer). Klavye tuzağı deseni görülmedi. Render edilebildiğinde Tab ile baştan sona gezip axe çalıştırılmalı (bkz. TODO).

### İnsan için TODO
- **Ekran okuyucu (NVDA / VoiceOver, mobilde TalkBack):** düzeltme sonrası dört alanın etiketi, 🗑 butonunun adı, tablo başlıkları ve `role="status"` duyuruları okunuyor mu.
- **%200 yakınlaştırma ve 320 px genişlik:** 320 px sabit `img` yatay kaydırma yaratıyor mu (1.4.10); yönerge metni ve tablo taşıyor mu (1.4.4).
- **Gerçek kullanıcı, 1 görev:** ilk kez gelen bir veli mobilde yardımsız "öğrenciyi kaydet" akışını tamamlayıp kaydın alındığını anlıyor mu; TC Kimlik No alanında hatalı giriş yapınca ne yaptığını çözebiliyor mu.
- **A10 doğrulanamaz:** `.pulse` CSS'ine bak — sonsuz animasyon ise durdurma yolu ve `@media (prefers-reduced-motion: reduce) { .pulse { animation: none } }` ekle; 3 Hz üstü yanıp sönme olmasın (2.3.1).
- **A12 doğrulanamaz:** `index.html` içinde `<html lang="tr">` var mı.
- **A1 sayfa düzeyi:** bileşeni saran `<main>` landmark ve "İçeriğe geç" atlama linki (2.4.1) sayfa iskeletinde var mı; `<title>` "Öğrenci Kayıt — <site adı>" biçiminde mi (2.4.2).
- **A9 CSS'e bağlı:** `.fake-btn` ve `.icon-only` gerçek boyutları ≥ 24×24 (mobil için 44×44) mi; birbirine yakın 🗑 ve "x" arasında boşluk var mı.
- **A6 CSS'e bağlı:** `input`, `button` ve linklerin `:focus-visible` göstergesi 3:1 kontrastı sağlıyor mu (yalnız `select` üzerindeki kaldırma dosyadan görüldü).
- **A5 CSS'e bağlı:** satır 27'deki gövde metni linki altı çizili mi; değilse renk dışı ayırt edici ekle.
- Render sonrası Playwright + axe çalıştır; `label`, `image-alt`, `color-contrast`, `td-headers-attr` id'lerini A4/A2/A3/A11 ile eşle.
