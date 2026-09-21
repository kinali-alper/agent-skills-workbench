# UX ve Erişilebilirlik Denetimi — BrokenForm.tsx

**Denetlenen dosya:** `BrokenForm.tsx` (30 satır, tek dosya)
**Yöntem:** Statik kaynak incelemesi. Sayfa render edilemedi; CSS sınıfları (`.broken`, `.fake-btn`, `.icon-only`, `.pulse`) projede yok, bu yüzden renk/boyut/animasyon gibi CSS'e bağlı değerler kaynaktan doğrulanamadı ve ayrı listelendi.
**Bağlam:** Arayüz dili Türkçe; hedef kullanıcı veliler, mobil cihaz, ilk kez kullanan.
**Referans:** WCAG 2.2 (AA), temel form UX ilkeleri.

Önem dereceleri: **Kritik** (görev tamamlanamaz / ekran okuyucu-klavye kullanıcısı için engel), **Yüksek** (ciddi hata riski veya yasal uyum sorunu), **Orta** (kullanılabilirliği düşürür), **Düşük** (iyileştirme).

---

## Özet tablo

| # | Satır | Önem | Sorun (kısa) | WCAG |
|---|-------|------|--------------|------|
| 1 | 9–16 | Kritik | Hiçbir form alanının etiketi yok; yalnız placeholder | 1.3.1, 3.3.2, 4.1.2 |
| 2 | 17 | Kritik | "Kaydet" bir `<div onClick>`; klavye/ekran okuyucuyla kullanılamaz, işlevi boş | 2.1.1, 4.1.2 |
| 3 | 1–30 | Kritik | `<form>` yok, `onSubmit` yok, doğrulama/hata/başarı geri bildirimi yok | 3.3.1, 3.3.3 |
| 4 | 12 | Yüksek | `outline: 'none'` — odak göstergesi kaldırılmış | 2.4.7 |
| 5 | 6–8 | Yüksek | Gri metin kontrastı ~2.8:1; zorunluluk yalnız renkle bildiriliyor; metin kendisiyle çelişiyor | 1.4.3, 1.4.1 |
| 6 | 18 | Yüksek | Yalnız emoji içeren silme düğmesi; onaysız tüm formu temizliyor; `type` yok | 4.1.2, 3.3.4 |
| 7 | 19 | Yüksek | 16×16 px "x" bağlantısı; anlamsız metin; silme işlemi link olarak | 2.5.8, 2.4.4 |
| 8 | 11 | Yüksek | TC Kimlik No: sayısal klavye yok, uzunluk sınırı yok, neden istendiği açıklanmıyor (KVKK) | 1.3.5, 3.3.2 |
| 9 | 5 | Orta | Görselde `alt` yok; sabit 320 px genişlik dar ekranda taşar | 1.1.1, 1.4.10 |
| 10 | 4 | Orta | Başlık `<div>` ile yapılmış, `<h1>` değil | 1.3.1 |
| 11 | 21–26 | Orta | Tabloda `<th>`, `scope`, `<caption>` yok; kayıt formunda not tablosu kapsam dışı | 1.3.1 |
| 12 | 27 | Orta | "buraya tıklayın" bağlantı metni | 2.4.4 |
| 13 | 20 | Orta | `aria-hidden="false"` anlamsız; "pulse" animasyonu için hareket azaltma yok; "Yeni!" bağlamsız | 2.2.2 |
| 14 | 9–10 | Düşük | `autoComplete` ve `name` yok; mobilde otomatik doldurma çalışmaz | 1.3.5 |
| 15 | 18 | Düşük | Alanlar `document.querySelectorAll` ile sıfırlanıyor; React durumu atlanıyor | — |

---

## Ayrıntılı bulgular

### 1. Form alanlarının hiçbirinde etiket yok — **Kritik**
**Dosya:satır:** `BrokenForm.tsx:9`, `:10`, `:11`, `:12`
**Sorun:** Üç `<input>` ve bir `<select>` yalnız `placeholder` (veya select için devre dışı ilk seçenek) ile tanımlanıyor. `<label>`, `id`, `name`, `aria-label` yok. Ekran okuyucu alanları "düzenleme kutusu" olarak okur, ne girileceğini söylemez. Placeholder yazmaya başlanınca kaybolur; ilk kez kullanan bir veli hangi alana ne yazdığını unutabilir. Placeholder metinleri tarayıcı varsayılanında düşük kontrastlıdır. Zorunlu alan bilgisi (`required` / `aria-required`) da yok.
**WCAG:** 1.3.1 Bilgi ve İlişkiler, 3.3.2 Etiketler veya Yönergeler, 4.1.2 Ad, Rol, Değer
**Düzeltme:**
```tsx
<label htmlFor="adSoyad">Ad Soyad <span aria-hidden="true">*</span></label>
<input id="adSoyad" name="adSoyad" type="text" required autoComplete="name" />

<label htmlFor="eposta">E-posta *</label>
<input id="eposta" name="eposta" type="email" required autoComplete="email" inputMode="email" />

<label htmlFor="tckn">TC Kimlik No *</label>
<input id="tckn" name="tckn" type="text" required inputMode="numeric" pattern="\d{11}" maxLength={11} />

<label htmlFor="sinif">Sınıf *</label>
<select id="sinif" name="sinif" required defaultValue="">
  <option value="" disabled>Sınıf seçin</option>
  ...
</select>
```
Etiketler görünür kalmalı (yalnız `aria-label` yeterli değil; görsel kullanıcı da etiket görmeli). Placeholder korunabilir ama etiket yerine kullanılmamalı.

---

### 2. Birincil eylem "Kaydet" bir `<div>` — **Kritik**
**Dosya:satır:** `BrokenForm.tsx:17`
**Sorun:** `<div className="fake-btn" onClick={() => {}}>Kaydet</div>`. Bir `div` Tab ile odaklanamaz, Enter/Boşluk ile tetiklenmez, ekran okuyucuya "düğme" olarak duyurulmaz. Klavye ve yardımcı teknoloji kullanıcısı formu hiç gönderemez. Üstelik `onClick` boş — dokunmatik kullanıcı bile bassa hiçbir şey olmaz ve hiçbir geri bildirim almaz.
**WCAG:** 2.1.1 Klavye, 4.1.2 Ad, Rol, Değer
**Düzeltme:**
```tsx
<button type="submit">Kaydet</button>
```
`.fake-btn` stilini `button` öğesine taşı. Mobilde dokunma hedefi en az 44×44 px, tam genişlik tercih edilir.

---

### 3. `<form>` öğesi, gönderim ve geri bildirim yok — **Kritik**
**Dosya:satır:** `BrokenForm.tsx:3` (kapsayıcı `div`), `:17`
**Sorun:** Alanlar bir `<form>` içinde değil; `onSubmit` yok; hiçbir doğrulama, hata mesajı veya başarı bildirimi yolu tanımlanmamış. Enter tuşu formu göndermez. Veli yanlış e-posta yazsa veya alan boş bıraksa bunu asla öğrenemez. "Kaydet" sonrasında ne olduğu belirsiz.
**WCAG:** 3.3.1 Hata Tanımlama, 3.3.3 Hata Önerisi
**Düzeltme:**
- Kapsayıcıyı `<form onSubmit={handleSubmit} noValidate>` yap.
- Her alan için hata metnini alanın hemen altında göster; `aria-describedby` ile bağla; `aria-invalid="true"` ver.
- Gönderim sonrası `role="status"` bölgesinde "Kayıt alındı" gibi başarı mesajı; hata varsa özet + ilk hatalı alana odak.
- Gönderim sırasında düğmeyi devre dışı bırak ve "Kaydediliyor…" göster.

---

### 4. Odak göstergesi kaldırılmış — **Yüksek**
**Dosya:satır:** `BrokenForm.tsx:12`
**Sorun:** `<select style={{ outline: 'none' }}>`. Klavye kullanıcısı select'e geldiğinde nerede olduğunu göremez.
**WCAG:** 2.4.7 Odak Görünür
**Düzeltme:** `outline: 'none'` satırını sil. Özel odak stili isteniyorsa CSS'te `select:focus-visible { outline: 3px solid #1a56db; outline-offset: 2px; }` gibi görünür bir gösterge tanımla.

---

### 5. Yönerge metni: düşük kontrast, yalnız renk, çelişkili — **Yüksek**
**Dosya:satır:** `BrokenForm.tsx:6–8`
**Sorun:**
- `color: '#9a9a9a'` / `background: '#fff'` → kontrast oranı yaklaşık **2.8:1**. Normal metin için 4.5:1 gerekir; büyük metin sınırı 3:1'i bile geçmez. Güneş altında telefondan okuyan veli için okunmaz.
- "Zorunlu alanlar kırmızı ile işaretlidir" → zorunluluk yalnız renkle iletiliyor. Renk körü kullanıcı ve ekran okuyucu bu bilgiyi alamaz.
- Metin kendisiyle çelişiyor: "tüm alanları doldurun" diyor, sonra "zorunlu alanlar kırmızı" diyor; oysa yalnız TC Kimlik (satır 11) kırmızı çerçeveli. Veli "diğerleri isteğe bağlı mı?" diye kalır.
**WCAG:** 1.4.3 Kontrast (Minimum), 1.4.1 Renk Kullanımı
**Düzeltme:**
- Rengi en az `#595959` (7:1) veya `#6b6b6b` (~5.3:1) yap.
- Metni netleştir: "Yıldız (*) ile işaretli alanlar zorunludur." Her zorunlu etikete `*` ekle ve `required` ver; kırmızı çerçeveyi yalnız **hata durumunda** kullan.
- Hangi alanlar zorunlu ise tutarlı biçimde tümüne uygula.

---

### 6. Yalnız emoji içeren, onaysız silme düğmesi — **Yüksek**
**Dosya:satır:** `BrokenForm.tsx:18`
**Sorun:** `<button className="icon-only">🗑</button>`. Erişilebilir adı yalnız "çöp kutusu" emojisi; ne sildiği belirsiz. Tek dokunuşla **tüm** alanları siler, onay yok, geri alma yok. "Kaydet"in hemen yanında duruyor — mobilde başparmak kayması ile veli girdiği her şeyi kaybeder. `type` belirtilmemiş; form eklendiğinde varsayılan `submit` olur ve yanlışlıkla formu gönderir.
**WCAG:** 4.1.2 Ad, Rol, Değer, 3.3.4 Hata Önleme, 2.5.8 Hedef Boyutu (`.icon-only` boyutu doğrulanamadı)
**Düzeltme:**
```tsx
<button type="button" onClick={handleReset} aria-label="Formu temizle">
  <span aria-hidden="true">🗑</span> Temizle
</button>
```
- Görünür metin ekle ("Temizle"); yalnız ikon kalacaksa `aria-label` zorunlu.
- Onay adımı ekle ("Girdiğiniz bilgiler silinecek. Emin misiniz?").
- Birincil düğmeden uzağa, ikincil görünümle yerleştir.
- Bu ekran için bu düğmeye gerçekten gerek var mı diye değerlendir; veliler nadiren tüm formu sıfırlar.

---

### 7. 16×16 px "x" bağlantısı — **Yüksek**
**Dosya:satır:** `BrokenForm.tsx:19`
**Sorun:** `<a href="#sil" style={{ width: 16, height: 16, fontSize: 10 }}>x</a>`. Dokunma hedefi 16×16 px (minimum 24×24, mobil için 44–48 önerilir). Metin 10 px — okunmaz. Bağlantı metni "x" anlamsız; ekran okuyucu "x, bağlantı" der. `href="#sil"` bir eylem (silme) için link kullanılmış; linkler sayfa içi gezinme içindir. Ne sildiği belli değil.
**WCAG:** 2.5.8 Hedef Boyutu (Minimum), 2.4.4 Bağlantı Amacı
**Düzeltme:** `<button type="button" aria-label="[Neyi sildiğini yaz]">` yap; en az 44×44 px hedef; ikon kullanılacaksa gerçek bir SVG "kapat" ikonu + `aria-label`. Gerçekten silme yapmıyorsa öğeyi kaldır.

---

### 8. TC Kimlik No alanı — **Yüksek**
**Dosya:satır:** `BrokenForm.tsx:11`
**Sorun:**
- `type="text"` → mobilde alfabe klavyesi açılır; 11 haneli sayı girmek zorlaşır.
- Uzunluk/biçim sınırı yok (`maxLength`, `pattern`).
- Kırmızı çerçeve (`border: '2px solid red'`) hata varmış izlenimi verir; oysa henüz hiçbir şey girilmedi. İlk kez gelen veli "ne yaptım?" diye tedirgin olur.
- Hassas kişisel veri (KVKK kapsamında) neden istendiği açıklanmadan toplanıyor.
**WCAG:** 1.3.5 Girdi Amacını Belirleme, 3.3.2 Etiketler veya Yönergeler
**Düzeltme:**
```tsx
<label htmlFor="tckn">Öğrenci TC Kimlik No *</label>
<input id="tckn" name="tckn" type="text" inputMode="numeric" pattern="\d{11}" maxLength={11}
       autoComplete="off" required aria-describedby="tckn-hint" />
<p id="tckn-hint">11 haneli, yalnız rakam. E-Okul kaydı için gereklidir.</p>
```
Kırmızı çerçeveyi kaldır; yalnız doğrulama hatasında göster. Kimin kimliği istendiğini (öğrenci mi veli mi) etikette belirt.

---

### 9. Görsel: `alt` yok, sabit genişlik — **Orta**
**Dosya:satır:** `BrokenForm.tsx:5`
**Sorun:** `<img>` öğesinde `alt` özniteliği hiç yok; ekran okuyucu dosya adını veya URL'yi okur. `width={320}` sabit; 320 px'den dar viewport'larda (veya büyük yazı tipi ile) yatay kaydırmaya yol açar. Görsel "picsum" rastgele fotoğraf — bilgi taşımıyor.
**WCAG:** 1.1.1 Metin Olmayan İçerik, 1.4.10 Yeniden Akış
**Düzeltme:** Dekoratifse `alt=""`; anlamlıysa kısa açıklama ("Okul binası"). Stil: `style={{ maxWidth: '100%', height: 'auto' }}`; `width`/`height` özniteliklerini oran koruma için tut.

---

### 10. Başlık bir `<div>` — **Orta**
**Dosya:satır:** `BrokenForm.tsx:4`
**Sorun:** `<div style={{ fontSize: 28, fontWeight: 700 }}>Öğrenci Kayıt</div>`. Görsel olarak başlık, yapısal olarak değil. Ekran okuyucu kullanıcısı başlıklar arasında gezinemez, sayfanın ne hakkında olduğunu anlayamaz.
**WCAG:** 1.3.1 Bilgi ve İlişkiler, 2.4.6 Başlıklar ve Etiketler
**Düzeltme:** `<h1>Öğrenci Kayıt</h1>` (veya sayfada zaten h1 varsa `<h2>`). Stilini CSS'te ver.

---

### 11. Tablo başlıksız ve kapsam dışı — **Orta**
**Dosya:satır:** `BrokenForm.tsx:21–26`
**Sorun:** Tabloda `<thead>`, `<th scope="col">`, `<caption>` yok. Ekran okuyucu "Matematik, 85" der; 85'in ne olduğu (not? yüzde? sıra?) belirsiz. Ayrıca bu bir **kayıt formu** ve kullanıcı **ilk kez** gelen veli — henüz kayıtlı öğrenci yokken ders notları göstermek kafa karıştırıcı; veli "bu kimin notu?" diye düşünür.
**WCAG:** 1.3.1 Bilgi ve İlişkiler
**Düzeltme:** Tabloyu bu ekrandan kaldır ya da açıkça ayrı bir bölüme al. Kalacaksa:
```tsx
<table>
  <caption>Örnek ders notları</caption>
  <thead><tr><th scope="col">Ders</th><th scope="col">Not (100 üzerinden)</th></tr></thead>
  <tbody>...</tbody>
</table>
```

---

### 12. "buraya tıklayın" bağlantısı — **Orta**
**Dosya:satır:** `BrokenForm.tsx:27`
**Sorun:** Bağlantı metni hedefi anlatmıyor. Ekran okuyucu bağlantı listesinde "buraya tıklayın" anlamsız. Mobilde "tıklayın" yerine "dokunun" beklenir; en iyisi eylem fiili hiç kullanmamak.
**WCAG:** 2.4.4 Bağlantı Amacı (Bağlam İçinde)
**Düzeltme:** `<a href="#detay">Kayıt sürecinin ayrıntılarını görüntüle</a>` gibi hedefi anlatan metin.

---

### 13. "Yeni!" rozeti: yanlış ARIA, animasyon, bağlamsız — **Orta**
**Dosya:satır:** `BrokenForm.tsx:20`
**Sorun:**
- `aria-hidden="false"` hiçbir şey yapmaz; muhtemelen `"true"` niyetiyle yazıldı ya da hiç gerekmez.
- `pulse` sınıfı sürekli animasyon ima ediyor (CSS doğrulanamadı). Hareket hassasiyeti olan kullanıcılar için `prefers-reduced-motion` desteği yok; 5 saniyeden uzun sürüyorsa durdurma yolu yok.
- "Yeni!" neyin yeni olduğunu söylemiyor; formun ortasında dikkat dağıtıyor.
**WCAG:** 2.2.2 Duraklat, Durdur, Gizle; ek olarak `prefers-reduced-motion` en iyi uygulaması
**Düzeltme:** `aria-hidden` özniteliğini kaldır. Rozeti ilgili öğenin yanına taşı ve bağlam ver ("Yeni: Sınıf seçimi"). CSS'te `@media (prefers-reduced-motion: reduce) { .pulse { animation: none; } }`. Gerekli değilse kaldır.

---

### 14. `autoComplete` ve `name` eksik — **Düşük**
**Dosya:satır:** `BrokenForm.tsx:9–10`
**Sorun:** Ad Soyad ve E-posta alanlarında `autoComplete="name"` / `autoComplete="email"` ve `name` yok. Mobil tarayıcı otomatik doldurma öneremez; veli her şeyi elle yazar. Bilişsel engelli kullanıcılar için otomatik doldurma önemli bir destek.
**WCAG:** 1.3.5 Girdi Amacını Belirleme
**Düzeltme:** Bulgu 1'deki kod örneğine bak.

---

### 15. DOM üzerinden sıfırlama — **Düşük (teknik borç)**
**Dosya:satır:** `BrokenForm.tsx:18`
**Sorun:** `document.querySelectorAll('.broken input').forEach(i => i.value = '')`. React durumu atlanıyor; alanlar kontrollü bileşene dönüştürülünce bu kod çalışmaz veya tutarsız durum yaratır. `select` de sıfırlanmıyor.
**Düzeltme:** Form durumunu `useState` (veya form kütüphanesi) ile tut; sıfırlamayı durum üzerinden yap ya da `<form>` içinde `formRef.current.reset()` kullan.

---

## Kaynaktan doğrulanamayan, canlı sayfada kontrol edilmesi gerekenler

Bu maddeler tek dosyadan çıkarılamaz; render edilen sayfada kontrol listesi olarak kullanılmalı:

- `<html lang="tr">` var mı? (WCAG 3.1.1) — Türkçe telaffuz için şart.
- `<meta name="viewport" content="width=device-width, initial-scale=1">` var mı? `maximum-scale` veya `user-scalable=no` ile yakınlaştırma engellenmiş mi? (1.4.4)
- `.fake-btn`, `.icon-only` gerçek boyutları (≥ 44×44 px hedef; 2.5.8) ve renk kontrastları.
- `.pulse` animasyon süresi ve `prefers-reduced-motion` desteği.
- Sayfa `<main>`, `<header>` gibi landmark'lar içinde mi?
- Placeholder metin rengi (tarayıcı varsayılanı çoğu zaman 4.5:1'i geçmez).
- Odak sırası: görsel sıra ile DOM sırası tutarlı mı?
- Form gönderim sonrası odak yönetimi ve canlı bölge duyuruları.

---

## Öncelikli düzeltme sırası (veli + mobil + ilk kullanım bağlamında)

1. `<form>` + gerçek `<button type="submit">` + görünür etiketler (Bulgu 1, 2, 3) — bunlar olmadan form kullanılamaz.
2. Zorunluluk göstergesini renkten bağımsız yap, yönerge metnini düzelt ve kontrastı yükselt (Bulgu 5).
3. Silme eylemlerini güvenli hale getir: onay, görünür etiket, büyük hedef, birincil düğmeden ayır (Bulgu 6, 7).
4. TC Kimlik alanına sayısal klavye, uzunluk sınırı ve neden istendiği açıklaması (Bulgu 8).
5. Odak göstergesini geri getir (Bulgu 4).
6. Kalan yapısal düzeltmeler: h1, alt, tablo başlıkları, bağlantı metinleri, rozet (Bulgu 9–13).

---

## Kısa özet

- Form şu an klavye ve ekran okuyucu ile **hiç kullanılamıyor**: etiket yok, "Kaydet" gerçek bir düğme değil, `<form>` yok.
- Zorunlu alan bilgisi yalnız kırmızı renkle veriliyor ve açıklama metni okunamayacak kadar soluk.
- İki silme kontrolü (çöp kutusu, "x") onaysız, küçük ve isimsiz; veli tek dokunuşla her şeyi kaybedebilir.
- TC Kimlik alanı mobilde sayısal klavye açmıyor ve neden istendiği söylenmiyor.
- CSS elimizde olmadığı için düğme boyutları, animasyon ve `lang`/viewport ayarları canlı sayfada ayrıca kontrol edilmeli.