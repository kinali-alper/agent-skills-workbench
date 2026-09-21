# UX ve Erişilebilirlik Denetimi — `broken.html`

**Kapsam:** Tek dosya, `broken.html` (38 satır). Sayfa render edilmedi; denetim yalnız kaynak kod okunarak yapıldı. Kontrast oranları WCAG formülüyle hex değerlerinden hesaplandı; gerçek düzen, dokunma hedefi boyutları ve odak görünümü tarayıcıda doğrulanmadı.
**Bağlam:** Arayüz Türkçe. Hedef kullanıcı: veliler, mobil cihaz, siteyi ilk kez kullanıyor. Sayfa bir öğrenci kayıt formu.
**Ölçüt:** WCAG 2.2 AA + temel kullanılabilirlik ilkeleri.

---

## Özet

| Önem | Adet | Başlıklar |
|---|---|---|
| Kritik | 5 | Etiketsiz ve `<form>` dışında kalan form alanları (gönderilemiyor), div ile yapılmış "Kaydet" düğmesi, isimsiz sil düğmesi, TC Kimlik alanı, odak göstergesi kaldırılmış |
| Yüksek | 6 | Görselde `alt` yok, yardım metni kontrastı, görünür odak stili ve taban yazı boyutu yok, 16×16 piksel "x" bağlantısı, sonsuz animasyon, başlıksız tablo |
| Orta | 4 | `div` ile sayfa başlığı ve landmark yokluğu, "buraya tıklayın", "Yeni!" rozet kontrastı, kırık `#sil` / `#detay` hedefleri |
| Düşük | 2 | `alert()` ile geri bildirim, yıkıcı düğmelerin Kaydet'in hemen yanında olması |

**Doğru olanlar (korunmalı):** `lang="tr"` (2. satır), `charset` ve `viewport` meta etiketleri (4–5), `<title>` (6), gövde için `max-width: 640px` (8), `select`'te devre dışı yer tutucu seçenek (24), `.fake-btn` renk çifti `#2b6cb0` / `#fff` ≈ **5,4:1** — AA'yı geçiyor (10).

---

## Bulgular (satır sırasıyla)

### 1. `broken.html:17` — Sayfa başlığı `div` ile yapılmış; sayfada hiç landmark yok
**Önem:** Orta · WCAG 1.3.1, 2.4.6
**Sorun:** `<div style="font-size:28px;font-weight:700">Öğrenci Kayıt</div>` görsel olarak başlık ama ekran okuyucu için sıradan metin. Sayfada `<h1>`, `<main>`, `<form>` yok; ekran okuyucu kullanıcısı başlıklar arasında atlayamaz, "form" bölgesine gidemez.
**Öneri:**
```html
<main>
  <h1>Öğrenci Kayıt</h1>
  <form action="/kayit" method="post" novalidate> … </form>
</main>
```
`h1` için stil CSS'te verilmeli (`h1 { font-size: 28px; font-weight: 700 }`), inline style kaldırılmalı.

### 2. `broken.html:18` — Görselde `alt` özniteliği yok
**Önem:** Yüksek · WCAG 1.1.1
**Sorun:** `<img src="https://picsum.photos/seed/okul/320/120" …>` alternatif metinsiz. Ekran okuyucu dosya adını ya da URL'yi okur. Rastgele stok fotoğraf içerik taşımıyor. Ek olarak 320 piksel sabit genişlik dar ekranlarda taşabilir.
**Öneri:** Dekoratif ise `alt=""` verin; anlam taşıyorsa kısa Türkçe açıklama yazın. Genişliği esnek yapın.
```html
<img src="…" alt="" width="320" height="120" style="max-width:100%;height:auto">
```

### 3. `broken.html:19` — Yardım metni kontrastı yetersiz; yönerge çelişkili
**Önem:** Yüksek · WCAG 1.4.3, 3.3.2
**Sorun:** `color:#9a9a9a` / `background:#fff` ≈ **2,8:1**, AA eşiği 4,5:1. Güneş altında telefondan bakan veli okuyamaz. Metin ayrıca "Lütfen tüm alanları doldurun" derken "zorunlu alanlar kırmızı ile işaretlidir" diyor — ya hepsi zorunlu ya bazıları; ilk kez gelen kullanıcı hangisine güveneceğini bilemez. Yalnız renkle işaret sorunu için 5. bulguya bakın.
**Öneri:** Rengi en az `#595959` (≈7:1) yapın. Metni tek ve net hale getirin: *"Yıldızlı (*) alanlar zorunludur."* ya da tüm alanlar zorunluysa *"Tüm alanlar zorunludur."*

### 4. `broken.html:20-22` — Form alanlarında `<label>`, `name`, `required`, `autocomplete` yok; alanlar `<form>` içinde değil
**Önem:** Kritik · WCAG 1.3.1, 3.3.2, 4.1.2, 1.3.5
**Sorun:**
- Etiket yalnız `placeholder`. Kullanıcı yazmaya başlayınca etiket kaybolur; veli "Bu kutuya ne yazacaktım?" diye geri dönemez. Ekran okuyucular placeholder'ı güvenilir şekilde etiket olarak okumaz.
- Hiçbir alanda `name` yok → alan değeri sunucuya gidemez; sayfa hiçbir zaman gerçekten kayıt yapamaz.
- `required` / `aria-required` yok → hata denetimi yok, hata mesajı yok (3.3.1, 3.3.3).
- `autocomplete` yok → mobilde tarayıcı otomatik doldurma (ad, e-posta) çalışmaz; ilk kez kullanan veli için en büyük zaman kazancı kaçırılıyor.
- `<form>` yok → mobil klavyedeki "Git/Gönder" tuşu işlevsiz.
**Öneri:**
```html
<form action="/kayit" method="post">
  <label for="adsoyad">Veli Ad Soyad <span aria-hidden="true">*</span></label>
  <input id="adsoyad" name="adsoyad" type="text" required autocomplete="name">

  <label for="eposta">E-posta <span aria-hidden="true">*</span></label>
  <input id="eposta" name="eposta" type="email" required autocomplete="email" inputmode="email">
  …
</form>
```
Etiket her zaman görünür kalmalı; placeholder yalnız örnek için (`placeholder="ornek@ornek.com"`) kullanılmalı. Hata durumunda alanın altına metin hata mesajı + `aria-describedby` ve `aria-invalid="true"` eklenmeli.

### 5. `broken.html:22` — TC Kimlik No alanı: yalnız renkle zorunluluk, metin tipi, sayısal klavye yok
**Önem:** Kritik · WCAG 1.4.1, 1.3.5, 3.3.2
**Sorun:**
- `style="border:2px solid red"` — zorunluluk yalnız renkle iletiliyor. Renk körü kullanıcı ve ekran okuyucu bunu almaz.
- `type="text"` — mobilde tam klavye açılır; 11 haneli sayı girmek zorlaşır, harf girilirse hata yakalanmaz.
- Uzunluk ve biçim denetimi yok.
- Bu alan hassas kişisel veri (KVKK kapsamı). Velinin neden istendiğini ve nasıl korunacağını görmesi güveni artırır; şu an hiçbir açıklama yok.
**Öneri:**
```html
<label for="tckn">Öğrenci TC Kimlik No <span aria-hidden="true">*</span></label>
<input id="tckn" name="tckn" type="text" inputmode="numeric" pattern="[0-9]{11}"
       maxlength="11" required aria-describedby="tckn-yardim">
<p id="tckn-yardim">11 haneli, boşluksuz. Yalnız kayıt doğrulaması için kullanılır.</p>
```
Kırmızı çerçeve yalnız **hata anında** ve metinle birlikte kullanılmalı.

### 6. `broken.html:23` — `select` üzerinde `outline:none`; etiket yok
**Önem:** Kritik · WCAG 2.4.7, 2.4.11, 1.3.1
**Sorun:** `style="outline:none"` klavye odak göstergesini tamamen kaldırıyor. Klavye ya da anahtar erişimi kullanan kişi hangi alanda olduğunu göremez. Ayrıca `select`'in görünür etiketi yok; "Sınıf seçin" seçildikten sonra kaybolur.
**Öneri:** `outline:none` kaldırılsın. Tüm odaklanabilir öğeler için görünür odak stili tanımlansın:
```css
:focus-visible { outline: 3px solid #1a56db; outline-offset: 2px; }
```
```html
<label for="sinif">Sınıf</label>
<select id="sinif" name="sinif" required> … </select>
```

### 7. `broken.html:28` — "Kaydet" düğmesi `div` + `onclick`
**Önem:** Kritik · WCAG 2.1.1, 4.1.2
**Sorun:** `<div class="fake-btn" onclick="alert('kaydedildi')">` klavyeyle odaklanamaz (tabindex yok), Enter/Boşluk çalışmaz, ekran okuyucuya "düğme" olarak tanıtılmaz, anlamsal adı yok. Sekmelerle gezen kullanıcı formu asla gönderemez. `alert()` ise hiçbir şey kaydedilmediği halde "kaydedildi" diyor (bkz. bulgu 17).
**Öneri:**
```html
<button type="submit" class="btn">Kaydet</button>
```
`.fake-btn` stilini `.btn`'e taşıyın; `min-height: 44px` ekleyin. Başarı/hata durumunu sayfa içinde `role="status"` bölgesine yazın.

### 8. `broken.html:29` — Simge-tek düğme: erişilebilir adı yok, yıkıcı işlem onaysız
**Önem:** Kritik · WCAG 4.1.2, 2.5.8, 3.3.4
**Sorun:** `<button class="icon-only">🗑</button>` — ekran okuyucu ya "çöp kutusu" emoji adını okur ya da hiçbir şey. Neyi sileceği belirsiz (form? bir kayıt?). Onay yok. `type` belirtilmemiş; bir `<form>` içine alınırsa varsayılan `submit` olur ve formu gönderir. 18px yazı boyutuyla dokunma hedefi yaklaşık 24×24'ün altında kalabilir.
**Öneri:**
```html
<button type="button" class="icon-only" aria-label="Formu temizle">
  <span aria-hidden="true">🗑</span>
</button>
```
Hedef en az 44×44 CSS piksel olsun (`min-width:44px;min-height:44px`). Yıkıcı ise onay adımı ekleyin ya da geri alma sunun. Mümkünse simge yanına metin ("Temizle") koyun; ilk kez kullanan veli için simge tek başına yetmez.

### 9. `broken.html:30` — 16×16 piksel, 10px yazılı "x" bağlantısı
**Önem:** Yüksek · WCAG 2.5.8, 2.4.4, 1.4.4
**Sorun:** `width:16px;height:16px;font-size:10px` — dokunma hedefi 24×24 minimumun altında; mobilde parmakla isabet ettirmek neredeyse imkânsız. Bağlantı metni "x" anlamsız. Bir "sil" işlemi `<a href="#sil">` ile yapılmış; bağlantı sayfada gezinme içindir, işlem için `<button>` kullanılır. `#sil` hedefi sayfada yok.
**Öneri:** Bağlantıyı kaldırın; işlevi 8. bulgudaki düğmeyle birleştirin ya da:
```html
<button type="button" aria-label="Kapat" style="min-width:44px;min-height:44px">×</button>
```

### 10. `broken.html:12-13, 31` — Sonsuz "pulse" animasyonu, hareket azaltma tercihi yok
**Önem:** Yüksek · WCAG 2.3.3, 2.2.2
**Sorun:** `animation: pulse 1s infinite` durmaksızın büyüyüp küçülen bir rozet. Vestibüler rahatsızlığı ya da dikkat dağınıklığı olan kullanıcılar için sorun; `prefers-reduced-motion` dikkate alınmıyor; durdurma kontrolü yok. Rozet metni "Yeni!" bağlamsız — yeni olan ne?
**Öneri:**
```css
@media (prefers-reduced-motion: reduce) { .pulse { animation: none; } }
```
Daha iyisi: animasyonu kaldırın (2–3 tekrar ya da hiç). Rozeti ait olduğu öğeye bağlayın: *"Yeni: not tablosu"*.

### 11. `broken.html:31` — "Yeni!" rozetinde kontrast yetersiz
**Önem:** Orta · WCAG 1.4.3
**Sorun:** `#e53e3e` zemin / `#fff` metin ≈ **4,1:1**. Normal boyutlu metin için AA eşiği 4,5:1; rozet küçük yazılı olduğu için başarısız.
**Öneri:** Zemini `#c53030` (≈5,5:1) ya da daha koyu yapın.

### 12. `broken.html:32-35` — Tablo başlıksız, `caption`/`th` yok; bağlamdan kopuk
**Önem:** Yüksek · WCAG 1.3.1
**Sorun:** İki sütunlu tablo yalnız `td` hücrelerinden oluşuyor. Ekran okuyucu "Matematik, 85" der; 85'in ne olduğu (not? yüzde? sınıf mevcudu?) belirsiz. Kayıt formu sayfasında not tablosunun neden olduğu da belirsiz — ilk kez gelen veli için kafa karıştırıcı.
**Öneri:**
```html
<table>
  <caption>Deneme sınavı sonuçları</caption>
  <thead><tr><th scope="col">Ders</th><th scope="col">Puan</th></tr></thead>
  <tbody>
    <tr><th scope="row">Matematik</th><td>85</td></tr>
    <tr><th scope="row">Türkçe</th><td>92</td></tr>
  </tbody>
</table>
```
Tablo bu sayfaya ait değilse kaldırılmalı.

### 13. `broken.html:36` — "buraya tıklayın" bağlantı metni
**Önem:** Orta · WCAG 2.4.4
**Sorun:** Bağlantı metni nereye gittiğini söylemiyor; ekran okuyucunun bağlantı listesinde "buraya tıklayın" anlamsız. Mobilde "tıklamak" yok, dokunulur. `#detay` hedefi sayfada yok — bağlantı kırık.
**Öneri:** `<a href="/kayit-detay">Kayıt koşullarını görüntüle</a>` gibi hedefi anlatan metin; `href` gerçek bir hedefe işaret etmeli.

### 14. `broken.html:30, 36` — Kırık sayfa içi hedefler (`#sil`, `#detay`)
**Önem:** Orta · WCAG 2.4.4
**Sorun:** Her iki `id` sayfada tanımlı değil. Tıklama URL'yi değiştirir ama hiçbir şey olmaz; veli "bozuk mu?" diye tereddüt eder.
**Öneri:** Hedefleri tanımlayın ya da bağlantıları kaldırın/düğmeye çevirin (9 ve 13. bulgular).

### 15. Genel — Görünür odak stili tanımlı değil; taban yazı boyutu yok
**Önem:** Yüksek · WCAG 2.4.7, 1.4.4
**Sorun:** CSS'te hiçbir `:focus` / `:focus-visible` kuralı yok; tarayıcı varsayılanına bırakılmış ve 23. satırda bir öğede kaldırılmış. `body` için `font-size` tanımlı değil; 30. satırda 10px kullanılmış. Girdilerde `padding: 6px` mobil için dar; dokunma yüksekliği ~30px kalır.
**Öneri:**
```css
body { font-size: 16px; line-height: 1.5; }
input, select, button { min-height: 44px; font-size: 16px; padding: 10px 12px; width: 100%; box-sizing: border-box; }
:focus-visible { outline: 3px solid #1a56db; outline-offset: 2px; }
```
16px altı girdi yazısı iOS'ta odaklanınca otomatik yakınlaştırma yapar; 16px bunu önler.

### 16. `broken.html:28-31` — Yıkıcı ve ilgisiz kontroller "Kaydet"in hemen yanında
**Önem:** Düşük (UX) · Nielsen: hata önleme
**Sorun:** Kaydet düğmesinin sağında sıra ile sil simgesi, küçük "x" ve animasyonlu rozet var. Mobilde baş parmak Kaydet'e uzanırken sil'e değebilir. İlk kez gelen veli birincil eylemi ayırt edemez.
**Öneri:** Birincil eylem tek başına, tam genişlikte ve en altta olsun. İkincil/yıkıcı eylemler görsel olarak ayrılsın (üstte "Formu temizle" metin bağlantısı gibi) ve arada en az 8px boşluk bırakılsın.

### 17. `broken.html:28` — Geri bildirim `alert()` ile
**Önem:** Düşük (UX) · WCAG 4.1.3
**Sorun:** Tarayıcı `alert`'i sayfa akışını keser, stil verilemez, ekran okuyucuda tutarsız duyurulur, mobilde bazı tarayıcılarda engellenir. Ayrıca hiçbir şey gönderilmeden "kaydedildi" denmesi yanıltıcı.
**Öneri:** Gerçek gönderim sonrasında sayfa içinde `role="status"` bölgesine *"Kayıt alındı. E-postanıza onay gönderildi."* yazılmalı; hata varsa `role="alert"` ile ilk hatalı alana odak taşınmalı.

---

## Önerilen düzeltme sırası

1. **Form iskeleti** (bulgu 4, 5, 6, 7): `<form>` + `<label>` + `name` + `required` + `autocomplete` + gerçek `<button type="submit">`. Bu olmadan sayfa işlevsel değil.
2. **Odak ve dokunma hedefleri** (6, 8, 9, 15): `outline:none` kaldır, `:focus-visible` tanımla, tüm kontroller 44×44.
3. **Renk ve kontrast** (3, 5, 11): `#9a9a9a` → `#595959`; kırmızı çerçeveyi yalnız hata için; rozet zeminini koyult.
4. **İçerik ve semantik** (1, 2, 12, 13, 14): `h1`/`main`, `alt`, tablo başlıkları, anlamlı bağlantı metinleri, kırık `#` hedefleri.
5. **Hareket ve geri bildirim** (10, 16, 17): animasyonu kaldır/azalt, sayfa içi durum mesajı, birincil eylemi ayır.

## Doğrulama notu

Render yapılamadığı için şunlar tarayıcıda ayrıca kontrol edilmelidir: gerçek dokunma hedefi boyutları (özellikle 29. ve 30. satır), 320px genişlikte yatay kaydırma olup olmadığı (18. satırdaki sabit 320px görsel + 24px gövde boşluğu = 368px, muhtemelen taşar), odak sırası ve ekran okuyucu (TalkBack/VoiceOver) ile form etiketlerinin okunuşu.