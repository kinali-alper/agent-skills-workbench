## BrokenForm.cshtml  ·  Kullanıcılar: okul sekreterleri — masaüstü, deneyimli, günde ~30 kez  ·  Dil: Türkçe  ·  **Statik denetim** (sayfa render edilemedi; yalnız kaynak dosya)

Kapsam: `Öğrenci Kayıt` görünümü — kayıt formu (ad, e-posta, TC kimlik no, sınıf), Kaydet / temizle / Sil eylemleri, not tablosu, koşullar linki. Kullanıcı grubu deneyimli ve tekrar sıklığı yüksek olduğu için H7 (verimlilik) ve hedef boyutu kararları "hızlı, klavyeyle, hatasız" ölçütüyle verildi. `_Layout.cshtml`, ViewModel ve CSS elde yok; onlara bağlı kontroller **doğrulanamaz** olarak işaretlendi ve İnsan TODO'ya yazıldı.

### Bulgular (şiddete göre)

**Şiddet 4**

BrokenForm.cshtml:18 — A7 · WCAG 2.1.1 · 4.1.2 · şiddet 4 — Sayfanın tek ana eylemi "Kaydet" bir `div onclick` ile yapılmış: klavyeyle odaklanamaz, Enter/Space çalışmaz, ekran okuyucuya "buton" olarak bildirilmez; ayrıca `$('form')` sayfadaki **tüm** formları (layout'taki çıkış/antiforgery formları dahil) gönderir → `<button type="submit" class="btn btn-primary">Kaydet</button>` yaz; `div.fake-btn` ve onclick'i kaldır (native submit zaten yalnız kendi formunu gönderir).

BrokenForm.cshtml:21 — U5 · H3 · H5 · WCAG 3.3.4 · şiddet 4 — Formun hemen yanında "x" gibi görünen 16×16 px'lik link bir kapatma düğmesi izlenimi verirken **kaydı siler** (`asp-action="Sil"`), GET ile, onaysız ve geri alma penceresi olmadan. Günde 30 kez bu ekrana gelen bir sekreter er ya da geç yanlışlıkla tıklar → Silmeyi `method="post"` bir forma taşı, düğme metnini "Kaydı sil" yap, tıklamada erişilebilir `<dialog>` ile "X öğrencisinin kaydı silinsin mi? — Sil / İptal" onayı iste; düğmeyi formun eylem satırından ayır (ikincil/tehlike stili, `btn-outline-danger`).

**Şiddet 3**

BrokenForm.cshtml:12 — A4 · WCAG 1.3.1 · 3.3.2 · şiddet 3 — Dört form denetiminin (12 AdSoyad, 13 Eposta, 14 TcKimlikNo, 15 SinifId) hiçbirinde programatik etiket yok; `asp-for` id/name üretir ama label üretmez → her alanın önüne `<label asp-for="AdSoyad">Ad Soyad</label>` (13: "E-posta", 14: "TC Kimlik No", 15: "Sınıf") ekle.

BrokenForm.cshtml:12 — U7 · H6 · şiddet 3 — Etiket görevini placeholder yapıyor (12–14); yazmaya başlanınca kaybolur, sekreter dolu formu kontrol ederken hangi kutuda ne olduğunu göremez → A4'teki kalıcı `<label>`'ları ekle; placeholder'ı yalnız örnek için kullan (`placeholder="örn. 12345678901"`).

BrokenForm.cshtml:18 — U1 · H1 · şiddet 3 — Kaydet'in görünür sonucu yok: bekleme göstergesi, durum mesajı ya da onay sayfası tanımlı değil; başarılı/başarısız gönderim ayrımı yapılamaz → Controller'da POST sonrası `RedirectToAction` ile onay sayfası **ya da** `TempData["Durum"] = "Kayıt alındı. Onay e-postası gönderildi."` ve layout'ta `<p role="status">@TempData["Durum"]</p>`; gönderim sırasında butonu `disabled` yapıp "Kaydediliyor…" göster.

BrokenForm.cshtml:11 — A13 · WCAG 4.1.3 · şiddet 3 — Formda doğrulama sonucunu duyuran canlı bölge yok: ne `asp-validation-summary`, ne alan başına `asp-validation-for`, ne `role="status"`/`aria-live` → formun başına `<div asp-validation-summary="ModelOnly" role="alert"></div>`, her alanın altına `<span asp-validation-for="…" class="text-danger" role="alert"></span>` ekle.

BrokenForm.cshtml:14 — A5 · WCAG 1.4.1 · 3.3.1 · şiddet 3 — TC Kimlik No alanındaki hata durumu yalnız `is-invalid` sınıfı (kırmızı kenarlık) ile veriliyor; metin, ikon, `aria-invalid`, `aria-describedby` yok → `is-invalid` sınıfını koddan sabit yazma; sınıfı doğrulama hata anında eklesin (varsayılan sınıf `input-validation-error`; Bootstrap `is-invalid` için `$.validator.setDefaults({ errorClass: "is-invalid" })` gibi bir eşleme gerekir); alanın altına `<span asp-validation-for="TcKimlikNo" class="text-danger" role="alert"></span>` koy, hata anında `aria-invalid="true"` ve `aria-describedby` ile bu span'a bağla.

BrokenForm.cshtml:9 — U4 · H4 · şiddet 3 — Yönerge "Zorunlu alanlar kırmızı ile işaretlidir" diyor ama hiçbir alanda zorunlu işareti yok; aynı anda "Lütfen tüm alanları doldurun" (hepsi zorunlu?) diyor; ve 14. satırda sabit `is-invalid` kırmızısı zorunlu işaretiyle karışıyor — zorunlu ve hata aynı sinyali paylaşıyor → Zorunlu: etiket sonunda `*` + form başında "* ile işaretli alanlar zorunludur". Hata: kırmızı kenarlık **+** ikon **+** alan altında metin (A5). Yönergeyi gerçek durumla eşle.

BrokenForm.cshtml:14 — U3 · H5 · H10 · WCAG 3.3.3 · şiddet 3 — TC Kimlik No alanında format ipucu, örnek, `inputmode`, `maxlength` yok; hata metni tanımlı değil (ne yanlış / nasıl düzelir söylenmez). Günde 30 kez 11 haneli numara giren kullanıcı için her yanlış giriş tekrar demek → `<input asp-for="TcKimlikNo" inputmode="numeric" maxlength="11" placeholder="örn. 12345678901" autocomplete="off">`; ViewModel'de `[RegularExpression(@"^\d{11}$", ErrorMessage = "Kimlik numarası 11 rakam olmalı (örn. 12345678901)")]`; Eposta için `type="email"` / `[EmailAddress]`. (Üretilen `type` ViewModel'deki `[DataType]`'a bağlı → İnsan TODO.)

BrokenForm.cshtml:15 — A6 · WCAG 2.4.7 · 2.4.11 · şiddet 3 — `<select>` üzerinde `style="outline:none"`: odak göstergesi kaldırılmış, yerine eşdeğer yok; klavyeyle sınıf seçen kullanıcı nerede olduğunu göremez → inline `outline:none`'ı kaldır; `:focus-visible { outline: 3px solid <≥3:1 kontrastlı renk>; outline-offset: 2px }` ile görünür gösterge ver.

BrokenForm.cshtml:19 — A8 · WCAG 4.1.2 · 2.5.3 · şiddet 3 — Buton yalnız 🗑 emojisi taşıyor; erişilebilir adı yok (ekran okuyucu "çöp kutusu" ya da hiçbir şey okur); üstelik çöp kutusu simgesi "sil" çağrışımı yaparken eylem formu **temizlemek** (H4 tutarsızlığı) → `<button type="reset" class="btn btn-link" aria-label="Formu temizle">🗑 <span>Formu temizle</span></button>` — görünür metin en iyisi; en azından `aria-label="Formu temizle"`.

BrokenForm.cshtml:19 — U5 · H3 · WCAG 3.3.4 · şiddet 3 — Formu sıfırlayan buton onaysız çalışıyor ve Kaydet'in hemen yanında duruyor; dolu formda yanlış tık = tüm veri kaybı → `type="reset"` kullan ve `onclick="return confirm('Girdiğiniz bilgiler silinsin mi?')"` (tercihen erişilebilir `<dialog>`); butonu Kaydet'ten görsel olarak ayır (link stili, sağa yasla).

BrokenForm.cshtml:21 — A9 · WCAG 2.5.8 · şiddet 3 — Sil linki 16×16 CSS px hedef ve 10 px yazı; minimum 24×24 altı, üstelik yıkıcı eylem → Düğmeyi en az 24×24 px yap (`btn btn-sm` bile 31 px verir), 10 px yazıyı kaldır, metnini "Kaydı sil" yap (bkz. şiddet 4 bulgusu).

**Şiddet 2**

BrokenForm.cshtml:7 — A1 · WCAG 1.3.1 · 2.4.6 · şiddet 2 — Sayfa başlığı stil verilmiş `div`; belge ana hattında `h1` yok, ekran okuyucu başlık gezintisi çalışmaz → `<h1>@ViewData["Title"]</h1>` yaz, boyutu CSS ile ver. (`main` landmark ve atlama linki `_Layout.cshtml`'de olmalı → İnsan TODO.)

BrokenForm.cshtml:23 — A11 · WCAG 1.3.1 · şiddet 2 — Not tablosunda `caption`, `thead`, `th scope` yok; `@foreach` doğrudan `<table>` altında satır üretiyor; hücreler ekran okuyucuda başlıksız okunur. 2 sütunlu küçük tablo — axe'ten kaçar → `<table class="table"><caption>Ders notları</caption><thead><tr><th scope="col">Ders</th><th scope="col">Puan</th></tr></thead><tbody>@foreach … </tbody></table>`; `Model.Notlar` boşsa tablo yerine "Henüz not girilmedi." metni göster.

BrokenForm.cshtml:22 — U6 · H8 · şiddet 2 — "Yeni!" rozeti hiçbir içeriğe bağlı değil (neyin yeni olduğu belirsiz) ve `pulse` sınıfı sürekli hareket ima ediyor; günde 30 kez gören kullanıcı için gürültü → Rozeti kaldır ya da bağla: "Yeni: sınıf listesi güncellendi" ve ilgili öğenin yanına koy; animasyonu tek seferlik yap (bkz. A10 TODO).

BrokenForm.cshtml:29 — U8 · H2 · WCAG 2.4.4 · şiddet 2 — Link metni "buraya tıklayın": hedefi söylemiyor, link listesinde anlamsız → `<a asp-action="Kosullar">Kayıt koşullarını görüntüle</a>`. (Aynı sorun :21'deki "x" ve :19'daki adsız 🗑 için de geçerli — yukarıda ele alındı.)

BrokenForm.cshtml:11 — U2 · H3 · şiddet 2 — Formdan çıkış yolu yok (İptal / listeye dön); yanlış öğrenciye girilmiş formdan geri dönmek için tarayıcı Geri'ye kalıyor → eylem satırına `<a asp-action="Index" class="btn btn-link">İptal</a>` ekle; yarım veri varsa çıkışta `beforeunload` uyarısı.

BrokenForm.cshtml:8 — A2 · WCAG 1.1.1 · şiddet 2 — `<img src="~/img/okul.jpg">` `alt` taşımıyor; ekran okuyucu dosya adını okur → Süs ise `alt=""`; bilgi taşıyorsa (logo, okul adı) `alt="Okul adı logosu"` gibi anlamlı metin.

BrokenForm.cshtml:9 — A3 · WCAG 1.4.3 · şiddet 2 — Yönerge metni `color:#9a9a9a`; Bootstrap varsayılan beyaz zeminde kontrast ≈ 2,8:1 (< 4,5:1). Küçük gri metin, zorunlu alanları anlatan tek yönerge → inline rengi kaldır, `text-muted`'ın varsayılanı (#6c757d, 4,7:1) ya da daha koyu bir renk kullan. (Zemin rengi CSS'te → İnsan TODO'da doğrulama.)

**Şiddet 1**

BrokenForm.cshtml:12 — WCAG 1.3.5 (sweep) · şiddet 1 — Kişisel alanlarda `autocomplete` yok → 12: `autocomplete="name"`, 13: `autocomplete="email"`; TC Kimlik No için `autocomplete="off"`.

Sweep notları (hüküm gerekmez): 2.4.2 `<title>` `_Layout` tarafından `ViewData["Title"]` ile üretilir, layout yok → TODO. 3.2.1/3.2.2 odakta/girdide bağlam değişimi yok — uygun. 2.5.2 eylemler `click`'te — uygun. 1.4.5 `okul.jpg` (320×120) yazı içeriyorsa metin görseli olur → TODO. 3.3.4 Sil ve sıfırlama için U5 bulgularında ele alındı. 1.2.x, 1.3.4, 1.4.2, 2.1.4, 2.2.1, 2.5.1, 2.5.4, 2.5.7, 3.3.7, 3.3.8 — dosyada konu yok.

### Kontrol listesi hükümleri
A1 ihlal :7 · A2 ihlal :8 · A3 ihlal :9 · A4 ihlal :12 · A5 ihlal :14 · A6 ihlal :15 · A7 ihlal :18 · A8 ihlal :19 · A9 ihlal :21 · A10 doğrulanamaz (CSS `.pulse`) · A11 ihlal :23 · A12 doğrulanamaz (`_Layout.cshtml`) · A13 ihlal :11
U1 ihlal :18 · U2 ihlal :11 · U3 ihlal :14 · U4 ihlal :9 · U5 ihlal :21 · U6 ihlal :22 · U7 ihlal :12 · U8 ihlal :29

### Klavye gezintisi
**render yok — statik denetim.** Kaynaktan çıkarılan öngörü (gözlemlenmiş davranış değil): Tab sırası 12 AdSoyad → 13 Eposta → 14 TcKimlikNo → 15 SinifId (odak göstergesi yok) → 19 🗑 (adsız, formu siler) → 21 "x" (Sil) → 29 "buraya tıklayın". **18 Kaydet Tab sırasında hiç yok** — klavye kullanıcısı formu gönderemez; formun içinde Enter'a basmak da çalışmaz (implicit submission için `type="submit"` buton gerekir). Sıfırla ve Sil ardışık iki odak noktası; ikisi de onaysız. Render sonrası doğrulanmalı.

### İnsan için TODO
- A10 · `.pulse` CSS'i (:22): 5 sn'den uzun sürekli animasyon mu, `prefers-reduced-motion` var mı, flaş frekansı 3 Hz altında mı — stil dosyasında kontrol et.
- A12 · `_Layout.cshtml`: `<html lang="tr">` var mı.
- A1 (layout kısmı) · `_Layout.cshtml`: `<main>@RenderBody()</main>` landmark'ı ve sayfa başında "İçeriğe geç" atlama linki var mı; `<title>` `ViewData["Title"]` + site adı üretiyor mu (2.4.2).
- A3 · Sayfa zemin rengini CSS'te doğrula; koyu tema varsa #9a9a9a kontrastı yeniden hesapla.
- A6 · Diğer denetimlerde (input, button, link) `:focus-visible` göstergesi ≥ 3:1 mi; site CSS'inde global `outline:none` var mı.
- U3 · `OgrenciKayitViewModel`: `[DataType(DataType.EmailAddress)]`, `[RegularExpression]`, `[Required(ErrorMessage=…)]` ve Türkçe hata metinleri var mı; `_ValidationScriptsPartial` sayfaya dahil mi.
- 1.4.5 · `okul.jpg` yazı içeriyor mu (metin görseli); içeriyorsa gerçek metinle değiştir.
- Ekran okuyucu (NVDA): düzeltmeler sonrası form etiketleri, hata duyuruları (`role="alert"`), tablo başlıkları ve onay diyaloğu okunuyor mu.
- %200 yakınlaştırma ve 320 px genişlikte: form alanları, eylem satırı ve tablo içerik kaybı / yatay kaydırma üretiyor mu.
- Gerçek kullanıcıyla 1 görev: bir okul sekreteri yalnız klavyeyle bir öğrenciyi kaydedip sonucu görebiliyor mu; "x" düğmesinin ne yaptığını tıklamadan söyleyebiliyor mu.
