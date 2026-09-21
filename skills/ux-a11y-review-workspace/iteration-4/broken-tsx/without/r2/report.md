# UX ve Erişilebilirlik Denetimi — `BrokenForm.tsx`

**Kapsam:** Yalnız kaynak dosya (`BrokenForm.tsx`, 30 satır) statik olarak incelendi; sayfa render edilemedi.
**Bağlam:** Arayüz dili Türkçe; kullanıcılar veliler, mobil cihazdan, formu ilk kez dolduruyor.
**Referans:** WCAG 2.2 (AA), mobil dokunma hedefi ≥ 44×44 px, form UX iyi uygulamaları.

## Özet

| Önem | Adet | Başlıca konular |
|---|---|---|
| Kritik | 5 | Etiketsiz alanlar, `div` ile yapılmış "Kaydet" düğmesi, form/gönderim yok, isimsiz silme düğmesi, odak göstergesinin kapatılması |
| Yüksek | 4 | Tıklanamayacak kadar küçük "x" bağlantısı, renk-tek başına zorunluluk işareti + düşük kontrast, alt metni olmayan görsel, başlık semantiği yok |
| Orta | 3 | Tablo başlığı/başlıkları yok, genel "buraya tıklayın" bağlantısı, `pulse` animasyonu (hareket azaltma yok) |
| Düşük | 1 | `aria-hidden="false"` gereksiz; "Yeni!" etiketi neye ait belirsiz |

## Bulgular (önem sırasına göre)

### K1 — Form alanlarının görünür/programatik etiketi yok; sadece `placeholder` var
**Konum:** `BrokenForm.tsx:9`, `:10`, `:11`, `:12`
**Sorun:** Üç `input` ve `select` için `<label>`, `id`, `name`, `required`, `autoComplete` yok. Placeholder yazmaya başlanınca kaybolur; ilk kez form dolduran bir veli üç alanı doldurduktan sonra hangisinin ne olduğunu göremez. Ekran okuyucu alanı "düzenleme kutusu" olarak okur, adı yoktur. Tarayıcı otomatik doldurma çalışmaz (mobilde en büyük zaman kazandırıcı). WCAG 1.3.1, 1.3.5, 3.3.2, 4.1.2.
**Öneri:**
```tsx
<label htmlFor="adSoyad">Ad Soyad</label>
<input id="adSoyad" name="adSoyad" type="text" required autoComplete="name" />

<label htmlFor="eposta">E-posta</label>
<input id="eposta" name="eposta" type="email" required autoComplete="email" inputMode="email" />

<label htmlFor="tcKimlik">T.C. Kimlik No <span aria-hidden="true">*</span></label>
<input id="tcKimlik" name="tcKimlik" type="text" required inputMode="numeric"
       maxLength={11} pattern="[0-9]{11}" aria-describedby="tcKimlik-ipucu tcKimlik-hata" />
<p id="tcKimlik-ipucu">11 haneli, yalnız rakam.</p>

<label htmlFor="sinif">Sınıf</label>
<select id="sinif" name="sinif" required defaultValue="">…</select>
```
Placeholder kalabilir ama etiketin yerine geçmemeli. Ayrıca T.C. Kimlik No gibi hassas bir verinin bu formda gerçekten gerekli olup olmadığı (KVKK, veri minimizasyonu) ürün tarafında teyit edilmeli; gerekliyse neden istendiği bir cümleyle açıklanmalı.

### K2 — "Kaydet" birincil eylemi `div` ile yapılmış
**Konum:** `BrokenForm.tsx:17`
**Sorun:** `<div className="fake-btn" onClick>` klavye ile odaklanamaz, Enter/Boşluk ile tetiklenmez, ekran okuyucuya "düğme" olarak bildirilmez, `onClick` de boştur (hiçbir şey kaydetmiyor). Formun ana eylemi klavye ve yardımcı teknoloji kullanıcıları için hiç yok. WCAG 2.1.1, 4.1.2.
**Öneri:** `<button type="submit">Kaydet</button>` kullanılmalı ve form gönderimi `<form onSubmit>` içinde ele alınmalı (bkz. K3). `.fake-btn` stili gerçek düğmeye taşınabilir; en az 44×44 px dokunma alanı sağlanmalı.

### K3 — `<form>` ve gönderim akışı yok; sonuç geri bildirimi yok
**Konum:** `BrokenForm.tsx:3-28`
**Sorun:** Alanlar `<div className="broken">` içinde. `<form>` olmadığı için mobil klavyedeki "Git/Enter" tuşu çalışmaz, tarayıcının yerleşik zorunlu alan doğrulaması devreye girmez, gönderim sonrası başarı/hata mesajı için hiçbir yer yok. Veli "Kaydet"e basıp ne olduğunu anlayamaz. Sayfada bir bölge (landmark) da yok. WCAG 3.3.1, 3.3.3, 4.1.3.
**Öneri:**
```tsx
<form onSubmit={handleSubmit} noValidate aria-labelledby="baslik">
  <h1 id="baslik">Öğrenci Kayıt</h1>
  <fieldset><legend>Öğrenci bilgileri</legend>…</fieldset>
  <div role="status" aria-live="polite">{mesaj}</div>
  <button type="submit" disabled={gonderiliyor}>Kaydet</button>
</form>
```
Hata mesajları ilgili alanın hemen altında, alanla `aria-describedby` ile bağlı ve `aria-invalid="true"` ile işaretlenmiş olmalı. Başarı durumunda açık bir onay ("Kayıt alındı") gösterilmeli.

### K4 — Silme düğmesi isimsiz, yıkıcı ve "Kaydet"in hemen yanında
**Konum:** `BrokenForm.tsx:18`
**Sorun:** Düğmenin tek içeriği çöp kutusu emojisi; erişilebilir adı yok, ekran okuyucu "çöp kutusu" ya da hiçbir şey okuyabilir. Tıklanınca tüm alanları onaysız siler. Mobilde birincil eylem "Kaydet"e komşu olması yanlışlıkla dokunma riskini artırır; veli 3 alanı doldurup her şeyi kaybedebilir. `document.querySelectorAll` ile DOM'a doğrudan yazmak React durumunu (state) baypas eder; kontrollü bileşenlerde çalışmaz. `type` belirtilmediği için K3'teki `<form>` uygulanınca bu düğme varsayılan olarak **submit** olur — yani formu temizlemek yerine gönderir. WCAG 4.1.2, 2.5.8.
**Öneri:**
```tsx
<button type="button" onClick={formuTemizle} aria-label="Formu temizle">
  <span aria-hidden="true">&#x1F5D1;</span> Temizle
</button>
```
Görünür metin eklenmeli ("Temizle"), onay adımı konmalı (ya da "Geri al" seçeneği), düğme birincil eylemden uzağa ve ikincil görünümle yerleştirilmeli. Temizleme React state üzerinden yapılmalı. Not: K2 ve K3 uygulanırken bu düğmeye `type="button"` eklenmesi **zorunlu**; yoksa form beklenmedik şekilde gönderilir.

### K5 — `select`te odak göstergesi kapatılmış
**Konum:** `BrokenForm.tsx:12`
**Sorun:** `style={{ outline: 'none' }}` klavye odağını görünmez yapar. Harici klavye/switch kullanan ya da odağı takip eden kullanıcı nerede olduğunu göremez. WCAG 2.4.7 (AAA referansı: 2.4.13).
**Öneri:** `outline: none` kaldırılmalı. Özel görünüm isteniyorsa `:focus-visible { outline: 3px solid …; outline-offset: 2px; }` ile en az 3:1 kontrastlı bir odak halkası verilmeli.

### Y1 — 16×16 px, 10 px yazı boyutunda "x" bağlantısı
**Konum:** `BrokenForm.tsx:19`
**Sorun:** Dokunma hedefi 16×16 px (WCAG 2.5.8 için en az 24×24 px; mobil için 44×44 px önerilir), yazı 10 px, metin "x" (ne sildiğini söylemiyor), bir eylem (`#sil`) için `<a>` kullanılmış. Veli parmakla vuramaz, ekran okuyucu "x, bağlantı" okur. WCAG 2.5.8, 2.4.4, 4.1.2.
**Öneri:** Eylemse `<button type="button" aria-label="…yi kaldır">` olmalı; görünür metin ya da en az 44×44 px dokunma alanı (`min-width/min-height: 44px` ya da padding) verilmeli. Bağlantı olarak kalacaksa hedef bu dosyada tanımlı değil (`#sil`) — bu da doğrulanmalı.

### Y2 — Zorunlu alanlar yalnız renkle işaretli; yönerge metni çelişkili ve düşük kontrastlı
**Konum:** `BrokenForm.tsx:6-8`, `:11`
**Sorun:** (a) `#9a9a9a` üzerine `#fff`: kontrast yaklaşık 2,8:1; normal metin için 4,5:1 gerekir. Güneş altında telefon ekranında okunmaz. WCAG 1.4.3. (b) "Zorunlu alanlar kırmızı ile işaretlidir" — zorunluluk yalnız renkle iletiliyor (`border: 2px solid red`); renk körü kullanıcı ayrımı göremez. WCAG 1.4.1. (c) Metin çelişkili: "tüm alanları doldurun" diyor, sonra "zorunlu alanlar işaretli" diyor — o zaman diğerleri isteğe bağlı mı? İlk kez dolduran veli için kafa karıştırıcı.
**Öneri:** Metin rengi en az `#767676` (4,5:1) — tercihen `#595959`. Yönerge şu şekilde sadeleştirilmeli: "Yıldızlı (*) alanlar zorunludur." Zorunlu alanlara etikette `*` (veya "(zorunlu)") metni ve `required` niteliği eklenmeli; kırmızı kenarlık yalnız **hata** durumunda, yanında açıklayıcı hata metniyle kullanılmalı.

### Y3 — Görselin `alt` niteliği yok
**Konum:** `BrokenForm.tsx:5`
**Sorun:** `<img>` alt metni olmadan ekran okuyucuya dosya adı/URL olarak okunur. Kaynak da bir yer tutucu servisi (`picsum.photos`) — üretimde rastgele, konuyla ilgisiz görsel gelir. Sabit `width={320}` küçük ekranlarda (320 px viewport, kenar boşluklarıyla) yatay kaymaya yol açabilir. WCAG 1.1.1, 1.4.10.
**Öneri:** Dekoratif ise `alt=""`; bilgi taşıyorsa anlamlı Türkçe `alt` ("… Okulu logosu"). Gerçek bir varlık kullanılmalı; `style={{ maxWidth: '100%', height: 'auto' }}` eklenmeli.

### Y4 — Sayfa başlığı `div` ile yapılmış
**Konum:** `BrokenForm.tsx:4`
**Sorun:** `<div style={{fontSize:28, fontWeight:700}}>` görsel olarak başlık ama semantik olarak değil; ekran okuyucu başlık listesinde görünmez, sayfanın ne olduğu anlaşılmaz. WCAG 1.3.1, 2.4.6.
**Öneri:** `<h1>Öğrenci Kayıt</h1>` (stil CSS ile). K3'te formu `aria-labelledby` ile bu başlığa bağlamak formu da isimlendirir.

### O1 — Tablonun başlığı ve sütun başlıkları yok
**Konum:** `BrokenForm.tsx:21-26`
**Sorun:** `<caption>`, `<thead>`, `<th>` yok. Ekran okuyucu "Matematik, 85" okur; 85'in ne olduğu (not? yüzde? devamsızlık?) belli değil. Görsel kullanıcı da tablonun neyi gösterdiğini tahmin etmek zorunda. WCAG 1.3.1.
**Öneri:**
```tsx
<table>
  <caption>Dönem notları</caption>
  <thead><tr><th scope="col">Ders</th><th scope="col">Not</th></tr></thead>
  <tbody>…</tbody>
</table>
```
Kayıt formunun içinde not tablosunun ne işi olduğu da sorgulanmalı; kayıt akışını uzatıyorsa ayrı bir ekrana alınmalı.

### O2 — "buraya tıklayın" bağlantı metni
**Konum:** `BrokenForm.tsx:27`
**Sorun:** Bağlantı metni hedefi söylemiyor; ekran okuyucunun bağlantı listesinde anlamsız. "Tıklayın" mobilde/klavyede fare varsayar. WCAG 2.4.4.
**Öneri:** `<a href="#detay">Not detaylarını görüntüle</a>` gibi hedefi anlatan metin. `#detay` hedefi bu dosyada yok; gerçek bir hedefe bağlanması doğrulanmalı.

### O3 — "pulse" animasyonu hareket azaltma tercihine bakmıyor
**Konum:** `BrokenForm.tsx:20`
**Sorun:** `.pulse` sınıfı (CSS bu dosyada değil) sürekli bir dikkat çekme animasyonu ima ediyor. Vestibüler hassasiyeti olan kullanıcılar için rahatsız edici; form doldururken dikkati dağıtır. WCAG 2.2.2; `prefers-reduced-motion` desteği iyi uygulama olarak önerilir.
**Öneri:** CSS'te `@media (prefers-reduced-motion: reduce) { .pulse { animation: none; } }`; animasyon kısa süreli olmalı (ör. 3 tekrar) ya da tamamen kaldırılmalı.

### D1 — `aria-hidden="false"` gereksiz; "Yeni!" etiketi neye ait belirsiz
**Konum:** `BrokenForm.tsx:20`
**Sorun:** `aria-hidden="false"` varsayılan davranıştır, etkisi yoktur ve niyetin karıştığını gösterir. "Yeni!" hangi öğeye ait? Tek başına duran bir rozet; bağlam yok.
**Öneri:** Niteliği kaldır. Rozet bir özelliğe aitse o öğenin içine/yanına alınmalı ve metni açık olmalı ("Yeni: not tablosu"). Sadece görsel süs ise `aria-hidden="true"` düşünülebilir.

## Düzeltmeler arası etkileşim (dikkat)
- K3 (`<form>` sarmalama) uygulanınca `:18` satırındaki `<button>` `type` belirtilmediği için **submit** davranır; K4'teki `type="button"` mutlaka eklenmeli.
- K1'de `required` eklendikten sonra tarayıcı varsayılan hata baloncukları İngilizce/işletim sistemi dilinde çıkabilir; Türkçe özel hata mesajları için `noValidate` + kendi doğrulama önerilir (K3).

## Sınırlamalar
- Yalnız statik okuma; `.broken`, `.fake-btn`, `.icon-only`, `.pulse` sınıflarının CSS'i görülemedi. Dokunma hedefi boyutu, odak halkası ve animasyon ile ilgili bulgular render ortamında doğrulanmalı.
- `#sil` ve `#detay` bağlantı hedefleri bu dosyada yok.
- `<html lang="tr">` bu bileşenin dışında; sayfa şablonunda tanımlı olduğu teyit edilmeli (WCAG 3.1.1).
- Sayfa başlığı (`<title>`), gezinme ve genel yerleşim bu bileşenin kapsamı dışında.

## Önerilen uygulama sırası
1. `<form>` + `<h1>` + gerçek `<button type="submit">` (K2, K3, Y4)
2. Her alana `label`/`id`/`name`/`required`/`autoComplete` (K1)
3. Silme düğmesi: `type="button"`, ad, onay, konum (K4); "x" bağlantısı -> düğme, 44 px (Y1)
4. Kontrast ve zorunlu alan işareti (Y2); odak halkası (K5)
5. `alt`, tablo başlıkları, bağlantı metni, animasyon, rozet (Y3, O1, O2, O3, D1)