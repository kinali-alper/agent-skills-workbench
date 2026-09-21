# UX ve Erişilebilirlik Denetimi — `BrokenForm.tsx`

**Kapsam:** Yalnız kaynak dosya (`BrokenForm.tsx`, 30 satır). Sayfa render edilemedi; CSS sınıfları (`.broken`, `.fake-btn`, `.icon-only`, `.pulse`) projede tanımlı değil. Bu yüzden dokunma hedefi boyutları, animasyon ve görsel yerleşim **kaynaktan çıkarımdır**, ölçüm değildir.

**Hedef kitle:** Veliler, mobil cihaz, formu ilk kez dolduruyor. Arayüz dili Türkçe.

**Şiddet ölçeği:** Kritik (görevi tamamlamayı engeller) · Yüksek (önemli kullanıcı grubunu dışlar) · Orta (zorlaştırır) · Düşük (cila).

---

## Özet tablo

| # | Satır | Şiddet | Sorun | WCAG |
|---|-------|--------|-------|------|
| 1 | 1–29 | Kritik | `<form>` yok; gönderim mekanizması yok | 1.3.1, 3.3.x |
| 2 | 17 | Kritik | `<div onClick>` "Kaydet" düğmesi; klavye/okuyucu erişemez, işlev boş | 2.1.1, 4.1.2 |
| 3 | 9–11 | Kritik | Etiket yok; placeholder etiket yerine kullanılmış | 1.3.1, 3.3.2, 4.1.2 |
| 4 | 18 | Yüksek | Yıkıcı "tümünü sil" düğmesi etiketsiz, onaysız, Kaydet'in hemen yanında | 4.1.2, 3.3.4 |
| 5 | 11 + 7 | Yüksek | Zorunlu alan yalnız kırmızı kenarlıkla belirtilmiş | 1.4.1, 3.3.2 |
| 6 | 6–7 | Yüksek | Yardım metni kontrastı ≈ 2.8:1 | 1.4.3 |
| 7 | 12 | Yüksek | `outline: none` odak halkasını kaldırıyor; select etiketsiz | 2.4.7, 1.3.1 |
| 8 | 19 | Yüksek | 16×16 px hedef, "x" metni, belirsiz yıkıcı bağlantı | 2.5.8, 2.4.4 |
| 9 | 4 | Orta | Başlık `<div>` ile yapılmış | 1.3.1, 2.4.6 |
| 10 | 5 | Orta | `alt` yok; rastgele görsel | 1.1.1 |
| 11 | 21–26 | Orta | Tablo başlıksız; bağlam dışı not içeriği | 1.3.1 |
| 12 | 20 | Orta | Sürekli animasyon ("pulse"), `aria-hidden="false"` anlamsız, "Yeni!" referanssız | 2.2.2 |
| 13 | 27 | Orta | "buraya tıklayın" bağlantı metni | 2.4.4 |
| 14 | 11 | Orta | TC Kimlik No: sayısal klavye, uzunluk, KVKK açıklaması yok | 3.3.2, 3.3.8 |
| 15 | 9–10 | Düşük | `autoComplete`, `name`, `id` yok | 1.3.5 |
| 16 | 1–29 | Orta | Doğrulama, hata ve başarı geri bildirimi hiç yok | 3.3.1, 3.3.3, 4.1.3 |

---

## Bulgular

### 1. `BrokenForm.tsx:1-29` — `<form>` öğesi yok (Kritik)

**Sorun:** Alanlar düz `<div>` içinde. Enter tuşu formu göndermez, tarayıcının yerleşik doğrulaması (`required`, `type="email"`) devreye girmez, ekran okuyucular "form" bölgesi duyurmaz. Mobilde klavyedeki "Git/Bitti" tuşu hiçbir şey yapmaz.

**Düzeltme:**
```tsx
<form onSubmit={handleSubmit} aria-labelledby="kayit-baslik">
  ...
  <button type="submit">Kaydet</button>
</form>
```
Tüm alanları ve gönder düğmesini bu form içine alın; `handleSubmit` içinde `event.preventDefault()` ve doğrulama yapın.

---

### 2. `BrokenForm.tsx:17` — Sahte düğme (`<div onClick>`) (Kritik)

**Sorun:** `<div className="fake-btn" onClick={() => {}}>Kaydet</div>`
- Sekme sırasına girmez → klavye kullanıcısı ulaşamaz.
- `role` yok → ekran okuyucu "Kaydet" metnini düğme olarak değil düz yazı olarak okur.
- Enter/Space tetiklemez.
- İşlev `() => {}` → dokunulunca hiçbir şey olmuyor; veli "kaydettim mi?" belirsizliğinde kalır.

**Düzeltme:**
```tsx
<button type="submit" className="btn-primary">Kaydet</button>
```
Gerçek `<button>` kullanın; odak, rol ve klavye desteği ücretsiz gelir. Yükleme sırasında `disabled` + `aria-busy="true"` verin.

---

### 3. `BrokenForm.tsx:9-11` — Etiket yok, placeholder etiket gibi kullanılıyor (Kritik)

**Sorun:** Üç `<input>` da yalnız `placeholder` taşıyor. Kullanıcı yazmaya başlayınca ipucu kaybolur; veli "bu alana ne yazıyordum?" diye geri döner (mobilde alan küçük, bağlam yok). Ekran okuyucuların bir kısmı placeholder'ı ad olarak okumaz. `id`/`name` yok → tarayıcı otomatik doldurma çalışmaz.

**Düzeltme (her alan için):**
```tsx
<label htmlFor="adSoyad">Ad Soyad <span aria-hidden="true">*</span></label>
<input id="adSoyad" name="adSoyad" type="text" required
       autoComplete="name" aria-describedby="adSoyad-hata" />
<p id="adSoyad-hata" role="alert" className="hata"></p>
```
E-posta için `autoComplete="email"`, `inputMode="email"`. Placeholder'ı yalnız örnek göstermek için kullanın ("örn. ayse@ornek.com"), etiket yerine değil.

---

### 4. `BrokenForm.tsx:18` — Etiketsiz, onaysız yıkıcı düğme (Yüksek)

**Sorun:** `<button className="icon-only">🗑</button>`
- Erişilebilir adı yok; okuyucu emoji adını ("çöp kutusu") veya boş okur. Ne sileceği belli değil.
- Tek dokunuşla **tüm alanları** temizler, onay yok, geri alma yok.
- Kaydet'in hemen yanında duruyor → mobilde yanlış parmak dokunuşuyla veli girdiği her şeyi kaybeder.
- `document.querySelectorAll(...).value = ''` React durumunu atlar; kontrollü bileşene geçildiğinde çalışmaz.

**Düzeltme:**
```tsx
<button type="reset" className="btn-secondary"
        aria-label="Formu temizle"
        onClick={onTemizle}>
  <TrashIcon aria-hidden="true" /> Temizle
</button>
```
- Görünür metin ekleyin ("Temizle"), ikon dekoratif kalsın.
- Onay isteyin ("Girdiğiniz bilgiler silinecek. Emin misiniz?").
- Kaydet'ten görsel ve mekânsal olarak ayırın (ikincil stil, farklı satır veya en az 8 px boşluk).
- Formu React state ile sıfırlayın, DOM'u elle değiştirmeyin.

---

### 5. `BrokenForm.tsx:11` ve `:7` — Zorunlu alan yalnız renkle işaretli (Yüksek)

**Sorun:** Satır 7 açıkça "Zorunlu alanlar kırmızı ile işaretlidir" diyor; satır 11'de TC Kimlik alanı `border: '2px solid red'`. Renk körü kullanıcılar (erkeklerde ~%8) ve ekran okuyucu kullanıcıları bu bilgiyi alamaz. Ayrıca kırmızı kenarlık forma ilk giren veliye "hata var" mesajı verir — daha hiçbir şey yazmamış olsa da.

**Düzeltme:**
- Her zorunlu etikete yıldız + form üstüne açıklama: "* ile işaretli alanlar zorunludur."
- `<input required aria-required="true">`.
- Kırmızı kenarlığı **yalnız doğrulama hatasından sonra** gösterin, yanında metin hata mesajıyla.
- Satır 7 metnini değiştirin: "Yıldızlı (*) alanlar zorunludur."

---

### 6. `BrokenForm.tsx:6-7` — Yetersiz kontrast (Yüksek)

**Sorun:** `color: '#9a9a9a'` / `background: '#fff'` → kontrast ≈ **2.8:1**. WCAG AA normal metin için en az 4.5:1 ister. Güneş altında telefon ekranında bu metin görünmez; oysa formun tek yönlendirme metni bu.

**Düzeltme:** `#595959` (7:1) veya en azından `#6b6b6b` (5.3:1) kullanın. Yardım metni "ikincil" görünmeli ama okunmalı.

---

### 7. `BrokenForm.tsx:12-16` — Odak halkası kaldırılmış, select etiketsiz (Yüksek)

**Sorun:**
- `style={{ outline: 'none' }}` → klavye kullanıcısı select'e geldiğinde nerede olduğunu göremez (2.4.7).
- `<label>` yok; disabled placeholder seçeneği "Sınıf seçin" görsel ipucu verir ama erişilebilir ad değildir.
- Yalnız 5. ve 6. sınıf var; başka sınıflar hedef dışıysa bunu belirtin, değilse liste eksik.

**Düzeltme:**
```tsx
<label htmlFor="sinif">Sınıf *</label>
<select id="sinif" name="sinif" required defaultValue="">
  <option value="" disabled>Seçin</option>
  <option value="5">5. Sınıf</option>
  <option value="6">6. Sınıf</option>
</select>
```
`outline: none` satırını silin; özel odak stili istiyorsanız `:focus-visible { outline: 3px solid ...; outline-offset: 2px }` ile değiştirin, kaldırmayın.

---

### 8. `BrokenForm.tsx:19` — 16×16 px "x" bağlantısı (Yüksek)

**Sorun:** `<a href="#sil" style={{ width: 16, height: 16, fontSize: 10 }}>x</a>`
- Dokunma hedefi 16×16 px; WCAG 2.5.8 en az 24×24, mobil için önerilen 44×44.
- Bağlantı metni "x" → okuyucu "x, bağlantı" der; amaç bilinmez.
- `href="#sil"` silme çağrısı yapıyor gibi; bağlantı (`<a>`) ile yıkıcı eylem yapılmamalı.
- Neyi kapattığı/sildiği belirsiz — yanındaki hiçbir öğeyle ilişkisi yok.

**Düzeltme:** Öğeyi ya kaldırın ya da amaca göre gerçek düğmeye çevirin:
```tsx
<button type="button" aria-label="Bildirimi kapat" className="btn-icon-44">
  <CloseIcon aria-hidden="true" />
</button>
```
Minimum 44×44 px dokunma alanı (görsel ikon küçük kalabilir, `padding` ile alanı büyütün).

---

### 9. `BrokenForm.tsx:4` — Başlık `<div>` ile taklit edilmiş (Orta)

**Sorun:** `<div style={{ fontSize: 28, fontWeight: 700 }}>Öğrenci Kayıt</div>` görsel olarak başlık, yapısal olarak değil. Ekran okuyucu kullanıcısı başlıklar arasında gezinerek sayfayı anlayamaz.

**Düzeltme:** `<h1 id="kayit-baslik">Öğrenci Kayıt</h1>` ve form öğesine `aria-labelledby="kayit-baslik"`. Stil CSS'e taşınsın.

---

### 10. `BrokenForm.tsx:5` — `alt` özniteliği yok, rastgele görsel (Orta)

**Sorun:** `<img src="https://picsum.photos/seed/okul/320/120" ... />` `alt` yok → okuyucu dosya adını/URL'yi okur. Görsel picsum'dan rastgele geliyor; içerik kontrolsüz, üretimde uygun olmayan bir fotoğraf gelebilir. Sabit `width={320}` küçük ekranlarda taşabilir.

**Düzeltme:**
- Dekoratifse `alt=""`; anlam taşıyorsa açıklayıcı Türkçe alt ("Okul binası önü").
- Gerçek, kontrollü bir görsel kullanın; `style={{ maxWidth: '100%', height: 'auto' }}`.

---

### 11. `BrokenForm.tsx:21-26` — Tablo başlıksız, bağlam dışı (Orta)

**Sorun:**
- `<th>`, `scope`, `<caption>` yok → okuyucu "Matematik, 85" der; 85'in ne olduğu (not? yüzde? sıra?) bilinmez.
- Kayıt formunda not tablosu olması bağlam dışı: yeni kaydolan öğrencinin henüz notu yok. Veli kafası karışır ("bu kimin notu?"). Muhtemelen başka bir görünümden sızmış içerik.

**Düzeltme:** Tabloyu bu bileşenden çıkarın. Kalması gerekiyorsa:
```tsx
<table>
  <caption>Örnek ders notları</caption>
  <thead><tr><th scope="col">Ders</th><th scope="col">Not (100 üzerinden)</th></tr></thead>
  <tbody>...</tbody>
</table>
```

---

### 12. `BrokenForm.tsx:20` — Sürekli animasyon, anlamsız ARIA, referanssız "Yeni!" (Orta)

**Sorun:** `<div className="pulse" aria-hidden="false">Yeni!</div>`
- `.pulse` sınıfı sürekli animasyon ima ediyor (CSS görülemedi; çıkarım). 5 saniyeden uzun otomatik hareket durdurulabilir olmalı (2.2.2); vestibüler bozukluğu olan kullanıcılar için `prefers-reduced-motion` gerekir.
- `aria-hidden="false"` varsayılan değerdir, hiçbir şey yapmaz; kafa karıştırıcı gürültü.
- "Yeni!" neyin yeni olduğunu söylemiyor; hiçbir öğeye bağlı değil.

**Düzeltme:** Rozeti ait olduğu öğenin yanına taşıyın ve anlamlandırın ("Yeni: Sınıf seçimi eklendi"), ya da tümüyle kaldırın. Animasyon kalacaksa:
```css
@media (prefers-reduced-motion: reduce) { .pulse { animation: none; } }
```
ve animasyonu birkaç tekrar sonra durdurun. `aria-hidden` özniteliğini silin.

---

### 13. `BrokenForm.tsx:27` — "buraya tıklayın" bağlantı metni (Orta)

**Sorun:** Bağlantı metni hedefini söylemiyor; okuyucu bağlantı listesinde "buraya tıklayın" der. Mobilde "tıklayın" da yanlış eylem fiili (dokunulur).

**Düzeltme:** `<a href="/kayit/detay">Kayıt koşullarını görüntüle</a>` gibi hedefi anlatan metin.

---

### 14. `BrokenForm.tsx:11` — TC Kimlik No alanı için mobil ve güven eksikleri (Orta)

**Sorun:**
- `type="text"` → mobilde harf klavyesi açılır; 11 haneli sayı girmek zorlaşır.
- Uzunluk/biçim kısıtı yok; yanlış girişi ancak sunucu yakalar.
- Kimlik numarası hassas veri. İlk kez kaydolan veli "neden istiyorlar, ne yapacaklar?" diye durur. Hiçbir açıklama, KVKK/aydınlatma bağlantısı yok.

**Düzeltme:**
```tsx
<label htmlFor="tckn">Öğrencinin TC Kimlik No *</label>
<input id="tckn" name="tckn" inputMode="numeric" pattern="[0-9]{11}"
       maxLength={11} autoComplete="off" required
       aria-describedby="tckn-yardim" />
<p id="tckn-yardim">11 haneli, yalnız rakam. Kimlik bilgisi yalnız öğrenci kaydı için kullanılır. <a href="/kvkk">Aydınlatma metni</a></p>
```
Kimin kimliği istendiğini de netleştirin (öğrencinin mi velinin mi?).

---

### 15. `BrokenForm.tsx:9-10` — `autoComplete`, `name`, `id` yok (Düşük)

**Sorun:** Tarayıcı ve şifre yöneticileri alanı tanıyamaz; veli her şeyi elle yazar. WCAG 1.3.5 (Girdi Amacını Belirleme) karşılanmaz.

**Düzeltme:** `autoComplete="name"` (Ad Soyad), `autoComplete="email"` (E-posta), her alana benzersiz `id` ve `name`.

---

### 16. `BrokenForm.tsx:1-29` — Doğrulama, hata ve başarı geri bildirimi yok (Orta)

**Sorun:** Boş gönderim, geçersiz e-posta, kısa TC No için hiçbir mesaj üretilmiyor. Kaydet'e basıldığında ne olacağı belirsiz: sayfa değişir mi, e-posta gelir mi, okul arar mı? İlk kez form dolduran veli için en büyük terk nedeni.

**Düzeltme:**
- Alan bazlı hata mesajları: etiketin altında, `aria-describedby` ile bağlı, `role="alert"` veya `aria-live="polite"` bölgesinde.
- Hata metni ne yapılacağını söylesin: "E-posta adresi geçerli değil. Örnek: ayse@ornek.com".
- Gönderim sonrası açık başarı durumu: "Kaydınız alındı. 2 iş günü içinde e-posta ile bilgilendirileceksiniz."
- Kaydet düğmesinin yanına beklentiyi ayarlayan kısa not: "Kaydet'e bastıktan sonra onay e-postası alacaksınız."

---

## Kaynaktan doğrulanamayanlar (render gerektiren)

- `.broken`, `.fake-btn`, `.icon-only`, `.pulse` sınıflarının CSS'i yok; gerçek dokunma hedefi boyutları, boşluklar ve animasyon davranışı ölçülemedi.
- Input ve select yükseklikleri (mobilde 44 px hedef) bilinmiyor.
- Sayfa düzeni, alanların yığılma sırası ve yatay taşma (320 px sabit görsel) test edilemedi.
- Gerçek ekran okuyucu ve klavye davranışı doğrulanmadı; bulgular HTML/ARIA semantiğine dayanır.

## Öncelik sırası (mobil veli senaryosu için)

1. `<form>` + gerçek `<button type="submit">` (bulgu 1, 2) — form şu an çalışmıyor.
2. Görünür etiketler + zorunlu işareti + hata mesajları (bulgu 3, 5, 16).
3. Sil düğmesini etiketle, onay iste, Kaydet'ten uzaklaştır (bulgu 4, 8).
4. Kontrast ve odak halkası (bulgu 6, 7).
5. TC Kimlik alanı için sayısal klavye ve güven metni (bulgu 14).
6. Kalanlar: başlık, alt, tablo, animasyon, bağlantı metinleri.