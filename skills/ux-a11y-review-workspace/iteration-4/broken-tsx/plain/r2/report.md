# UX ve Erişilebilirlik Denetimi — `BrokenForm.tsx`

**Denetlenen dosya:** `project/BrokenForm.tsx` (30 satır, tek React bileşeni)
**Yöntem:** Statik kaynak incelemesi. Sayfa render edilemedi; CSS (`.broken`, `.fake-btn`, `.icon-only`, `.pulse`), HTML kabuğu (`html lang`, `main`, atlama linki) ve çalışma zamanı davranışı dosyada yok. Bu yüzden bazı maddeler **doğrulanamaz** olarak işaretlendi.
**Hedef kitle:** Veliler, mobil, ilk kez kullanan. Bu bağlam bulguların ağırlığını artırır: dokunma hedefi, sanal klavye tipi, kaybolan placeholder ve güneş ışığında kontrast doğrudan bu kitleyi etkiler.

---

## 1. Hüküm tablosu

Her satır için tek hüküm: **ihlal :N** / **uygun** / **uygulanamaz** / **doğrulanamaz**.

### UX kontrolleri

| U | Kontrol | Hüküm | Not |
|---|---|---|---|
| U1 | Eylem görünür sonuç üretir (`role="status"`, yönlendirme, bekleme) | **ihlal :17** | `Kaydet` işleyicisi boş; hiçbir durum mesajı, yönlendirme veya bekleme göstergesi yok. Satır 18'deki temizleme de sessiz. |
| U2 | Her akıştan çıkış yolu (İptal / Geri; yarım veride uyarı) | **ihlal :17** | Eylem grubunda İptal/Geri yok; `<form>` yok, yarım veri uyarısı yok. |
| U3 | Biçimli alanlar doğru `type`/`inputmode`, format ipucu, örnek; hata metni ne + nasıl | **ihlal :11** | TC Kimlik No `type="text"`, `inputMode` yok, 11 hane / yalnız rakam ipucu yok, örnek yok, hata metni hiç yok. |
| U4 | Zorunlu işareti ve hata işareti ayrı sinyal; yönerge gerçek durumla örtüşür | **ihlal :7** | Metin "tüm alanları doldurun" derken aynı cümlede "zorunlular kırmızı" diyor; yalnız satır 11 kırmızı. Kırmızı kenarlık aynı zamanda evrensel hata sinyali; zorunlu ile hata karışıyor. |
| U5 | Yıkıcı eylem onay ister ya da geri alma verir | **ihlal :18** | Çöp kutusu butonu tüm alanları onaysız, geri alınamaz şekilde siliyor. |
| U6 | Rozet/uyarı bir içeriğe bağlı; bağlamsız dikkat çekici yok | **ihlal :20** | "Yeni!" hiçbir öğeye bağlı değil; ne yeni, nerede belli değil. |
| U7 | Etiketler kalıcı; placeholder etiket yerine geçmez | **ihlal :9** | 9, 10, 11'de tek etiket placeholder; 13'te `disabled` seçenek etiket görevi görüyor. Yazmaya başlayınca alan adı kaybolur. |
| U8 | Link/buton metni hedefi/eylemi arayüz dilinde söyler | **ihlal :27** | "buraya tıklayın" hedefi söylemiyor. Satır 18 (`🗑`) ve 19 (`x`) de eylemi söylemiyor. |

### Erişilebilirlik kontrolleri

| A | Kontrol | Hüküm | Not |
|---|---|---|---|
| A1 | Tek `h1`, hiyerarşik başlıklar, `main`; sayfa düzeyinde atlama linki | **ihlal :4** | Başlık `div` + `fontSize:28`; yapısal başlık yok. `main` ve atlama linki sayfa düzeyi → bileşende doğrulanamaz. |
| A2 | Bilgi taşıyan görselde anlamlı `alt`; süste `alt=""` | **ihlal :5** | `<img>` üzerinde `alt` özniteliği hiç yok; ekran okuyucu dosya adını/URL'yi okur. |
| A3 | Metin kontrastı ≥ 4.5:1 (büyük/UI ≥ 3:1) | **ihlal :6** | `#9a9a9a` / `#fff` = **2.81:1** (hesaplandı). Küçük yönerge metni için 4.5:1 gerekir. Satır 19'daki 10px "x" ve `.pulse` rengi CSS olmadığı için ayrıca doğrulanamaz. |
| A4 | Her form denetimi programatik etikete bağlı | **ihlal :9** | 9, 10, 11, 12'de `label`, `aria-label` veya `aria-labelledby` yok. |
| A5 | Renk tek sinyal değil (`aria-invalid` + `aria-describedby`); gövde linki altı çizili | **ihlal :11** | Zorunlu/hata durumu yalnız kırmızı kenarlıkla verilmiş; `aria-invalid`, `aria-describedby`, metin veya ikon yok. Satır 7 de "kırmızı ile işaretlidir" diyerek rengi tek sinyal ilan ediyor. Link altı çizgisi: CSS yok, doğrulanamaz. |
| A6 | Odak görünür ve kalır; kaldırılan outline yerine eşdeğer var | **ihlal :12** | `select` üzerinde `outline: 'none'`, eşdeğer odak göstergesi yok. |
| A7 | Etkileşimli öğe native (`button`, `a href`, form denetimi) | **ihlal :17** | `Kaydet` bir `div` + `onClick`; klavyeyle odaklanamaz, Enter/Space çalışmaz, rolü yok. |
| A8 | Yalnız ikon/emoji denetimde erişilebilir ad | **ihlal :18** | Buton içeriği yalnız `🗑` emojisi; ekran okuyucu "çöp kutusu" der, eylem (formu temizle) anlaşılmaz. Satır 19'daki "x" de aynı. |
| A9 | Tıklama hedefi ≥ 24×24 CSS px | **ihlal :19** | `width:16, height:16` → 16×16 px; mobilde parmakla vurulamaz. |
| A10 | 5 sn'den uzun otomatik hareket durdurulabilir; flaş yok; `prefers-reduced-motion` | **doğrulanamaz** | Satır 20 `className="pulse"` sürekli animasyon çağrıştırıyor ama CSS dosyada yok. Süre, flaş ve reduced-motion kuralı kontrol edilemedi. |
| A11 | Veri tablosunda `caption` ve `th scope` | **ihlal :21** | 2×2 tablo; `caption`, `thead`, `th` yok. Küçük tablo, axe yakalamaz; elle bulundu. |
| A12 | `html lang` doğru; dil değişen parçalarda `lang` | **doğrulanamaz** | `html lang` sayfa düzeyinde, dosyada yok. Bileşen içinde dil değiştiren parça yok (o kısım sorunsuz). |
| A13 | Canlı güncellemeler `aria-live` / `role="status"` ile duyurulur | **ihlal :18** | Alanların temizlenmesi ve (gelecekte) kaydetme sonucu için hiçbir canlı bölge yok; ekran okuyucu kullanıcısı değişimi duymaz. |

**Sayım:** 19 ihlal, 2 doğrulanamaz, 0 uygun, 0 uygulanamaz.

---

## 2. Bulgular — satır satır (sorun → düzeltme)

Öncelik: **Kritik** (kullanıcı görevi tamamlayamaz / veri kaybı), **Yüksek** (ciddi engel), **Orta** (kalite).

### BrokenForm.tsx:4 — Başlık `div` ile yapılmış
**Kontrol:** A1 · **Öncelik:** Yüksek
**Sorun:** `<div style={{fontSize:28, fontWeight:700}}>Öğrenci Kayıt</div>` görsel olarak başlık ama yapısal olarak değil. Ekran okuyucu başlık listesinde görünmez, kullanıcı sayfada "başlığa atla" yapamaz.
**Düzeltme:**
```tsx
<h1>Öğrenci Kayıt</h1>
```
Boyutu CSS ile ver, inline stil yerine. Sayfada başka `h1` yoksa bu tek `h1` olur; bileşen bir sayfanın alt bölümüyse `h2` yap.

### BrokenForm.tsx:5 — `alt` yok
**Kontrol:** A2 · **Öncelik:** Yüksek
**Sorun:** `<img src="https://picsum.photos/seed/okul/320/120" width={320} height={120} />` — `alt` yok. Rastgele stok görsel, bilgi taşımıyor. Ekran okuyucu URL'yi harf harf okur.
**Düzeltme:** Süs görseli ise:
```tsx
<img src="…" width={320} height={120} alt="" />
```
Okul fotoğrafı gibi anlam taşıyorsa: `alt="Okul binası ön cephe"`. Mobil için `width`/`height` yerine `max-width:100%` düşün; 320px sabit genişlik dar ekranda taşabilir.

### BrokenForm.tsx:6-8 — Yönerge metni: düşük kontrast + çelişkili + renk tek sinyal
**Kontrol:** A3, U4, A5 · **Öncelik:** Yüksek
**Sorun:**
- `color:'#9a9a9a'` / `background:'#fff'` → **2.81:1**. Küçük metin için 4.5:1 gerekir. Mobilde, dış mekânda bu metin okunmaz.
- "Lütfen **tüm** alanları doldurun" ile "**Zorunlu** alanlar kırmızı ile işaretlidir" aynı cümlede çelişiyor. Hepsi zorunluysa işaret gerekmez; bir kısmı zorunluysa "tüm" yanlış.
- Yönerge "kırmızı" diyerek zorunluluğu yalnız renkle iletiyor; renk körü kullanıcı ve ekran okuyucu bu bilgiye ulaşamaz.
- Gerçek durum: yalnız satır 11 kırmızı; satır 9, 10, 12 işaretsiz. Metin ile durum örtüşmüyor.
**Düzeltme:**
```tsx
<p id="form-yonerge" style={{ color: '#595959' }}>
  Tüm alanlar zorunludur. Zorunlu alanlar <span aria-hidden="true">*</span> ile işaretlidir.
</p>
```
`#595959` / `#fff` ≈ 7:1. Her zorunlu alana `required` + görünür `*` ekle; hata ayrı sinyal olsun (bkz. satır 11).

### BrokenForm.tsx:9 — "Ad Soyad" etiketi yok, placeholder etiket yerine
**Kontrol:** U7, A4 · **Öncelik:** Kritik
**Sorun:** `<input type="text" placeholder="Ad Soyad" />` — programatik etiket yok. Ekran okuyucu "düzenle, metin" der. Veli yazmaya başlayınca "Ad Soyad" kaybolur; ilk kez dolduran kullanıcı hangi alanda olduğunu unutur. Mobilde otomatik doldurma (`autoComplete`) yok.
**Düzeltme:**
```tsx
<label htmlFor="adSoyad">Ad Soyad <span aria-hidden="true">*</span></label>
<input id="adSoyad" name="adSoyad" type="text" required autoComplete="name" />
```
Placeholder kullanılacaksa yalnız örnek için: `placeholder="Örn. Ayşe Yılmaz"`.

### BrokenForm.tsx:10 — "E-posta" etiketi yok
**Kontrol:** U7, A4 · **Öncelik:** Kritik
**Sorun:** Aynı sorun. `type="email"` doğru (mobil klavyede @ çıkar), ama etiket ve `autoComplete` yok.
**Düzeltme:**
```tsx
<label htmlFor="eposta">E-posta <span aria-hidden="true">*</span></label>
<input id="eposta" name="eposta" type="email" required autoComplete="email" inputMode="email" />
```

### BrokenForm.tsx:11 — TC Kimlik No: yanlış tip, ipucu yok, renk tek sinyal, etiket yok
**Kontrol:** U3, U4, A4, A5, U7 · **Öncelik:** Kritik
**Sorun:**
- `type="text"` ve `inputMode` yok → mobilde harf klavyesi açılır; 11 rakam yazmak zorlaşır.
- Format ipucu (11 hane, yalnız rakam), örnek ve `maxLength` yok.
- `border:'2px solid red'` sabit; alan boşken de kırmızı. Bu "zorunlu" mu "hatalı" mı belirsiz (U4). Renk tek sinyal (A5); `aria-invalid`, `aria-describedby`, hata metni yok.
- Hata metni hiç yok; hata olsa bile "ne yanlış, nasıl düzelir" söylenmez (U3).
- Etiket yok (A4/U7).
**Düzeltme:**
```tsx
<label htmlFor="tckn">T.C. Kimlik No <span aria-hidden="true">*</span></label>
<p id="tckn-ipucu">11 haneli, yalnız rakam. Örn. 12345678901</p>
<input
  id="tckn" name="tckn" type="text" inputMode="numeric" pattern="[0-9]{11}"
  maxLength={11} required autoComplete="off"
  aria-describedby={hata ? 'tckn-ipucu tckn-hata' : 'tckn-ipucu'}
  aria-invalid={hata ? true : undefined}
/>
{hata && (
  <p id="tckn-hata" role="alert">
    <span aria-hidden="true">⚠</span> T.C. Kimlik No 11 haneli olmalı; siz 9 hane girdiniz.
  </p>
)}
```
Kırmızı kenarlık yalnız `aria-invalid` ile birlikte ve hata metniyle beraber görünsün; zorunluluk `*` + `required` ile ayrı sinyal olsun.

### BrokenForm.tsx:12-16 — `select`: odak kaldırılmış, etiket yok, placeholder seçenek
**Kontrol:** A6, A4, U7 · **Öncelik:** Yüksek
**Sorun:**
- `style={{ outline: 'none' }}` odak halkasını siler, eşdeğer yok. Klavye kullanıcısı nerede olduğunu göremez.
- `label` yok; "Sınıf seçin" `disabled` seçeneği etiket görevi görüyor. Bir sınıf seçildikten sonra alanın adı ekrandan kaybolur.
**Düzeltme:**
```tsx
<label htmlFor="sinif">Sınıf <span aria-hidden="true">*</span></label>
<select id="sinif" name="sinif" required defaultValue="">
  <option value="" disabled>Seçin</option>
  <option value="5">5. Sınıf</option>
  <option value="6">6. Sınıf</option>
</select>
```
`outline:'none'` kaldır. Özel görünüm isteniyorsa CSS'te `select:focus-visible { outline: 3px solid #1a56db; outline-offset: 2px; }` gibi ≥ 3:1 kontrastlı eşdeğer ver. `option` öğelerine `value` ekle.

### BrokenForm.tsx:17 — "Kaydet" bir `div`; hiçbir şey yapmıyor; İptal yok
**Kontrol:** A7, U1, U2 · **Öncelik:** Kritik
**Sorun:**
- `<div className="fake-btn" onClick={() => {}}>Kaydet</div>`: Tab ile odaklanamaz, Enter/Space çalışmaz, ekran okuyucu "buton" demez. Klavye ve ekran okuyucu kullanıcısı formu **gönderemez**.
- İşleyici boş → veli "Kaydet"e basar, hiçbir şey olmaz; başarı/hata/bekleme yok (U1). Çift gönderim, terk etme riski.
- İptal / Geri yok; `<form>` yok, yarım veri uyarısı yok (U2).
**Düzeltme:**
```tsx
<form onSubmit={handleSubmit} noValidate aria-describedby="form-yonerge">
  {/* alanlar */}
  <div className="actions">
    <button type="submit" disabled={gonderiliyor}>
      {gonderiliyor ? 'Kaydediliyor…' : 'Kaydet'}
    </button>
    <button type="button" onClick={handleIptal}>İptal</button>
  </div>
  <p role="status" aria-live="polite">{durumMesaji}</p>
</form>
```
Gönderim sonrası `durumMesaji` = "Kayıt alındı. Onay e-postası gönderildi." veya hata metni. İptal'de yarım veri varsa "Girdiğiniz bilgiler silinecek. Emin misiniz?" diye sor.

### BrokenForm.tsx:18 — Emoji buton: ad yok, onaysız siliyor, DOM'u doğrudan değiştiriyor
**Kontrol:** A8, U5, U8, A13 · **Öncelik:** Kritik
**Sorun:**
- İçerik yalnız `🗑`; erişilebilir ad yok. Ekran okuyucu "çöp kutusu, buton" der; velinin bunun "formu temizle" olduğunu bilmesi imkânsız (A8/U8).
- Tıklamayla **tüm** alanlar onaysız siliniyor; geri alma yok (U5). Mobilde yanlışlıkla dokunma çok olası.
- Silme sonrası hiçbir duyuru yok (A13).
- `document.querySelectorAll(...).forEach(i => i.value = '')` React state'i atlıyor; kontrollü bileşenlerde çalışmaz, `select` alanını da temizlemez.
**Düzeltme:**
```tsx
<button type="button" onClick={formuTemizleOnayla}>
  <span aria-hidden="true">🗑</span> Formu temizle
</button>
```
Yer darsa: `<button type="button" aria-label="Formu temizle">…</button>`. Onay: `confirm('Tüm alanlar silinecek. Devam edilsin mi?')` ya da erişilebilir bir dialog. Temizleme sonrası `durumMesaji = 'Form temizlendi.'`. State'i React ile sıfırla (`setForm(bos)`), DOM'a dokunma.

### BrokenForm.tsx:19 — 16×16 px "x" linki, eylem yapan link
**Kontrol:** A9, A8, U8, U5 · **Öncelik:** Yüksek
**Sorun:**
- `width:16, height:16, fontSize:10` → hedef 16×16 px, 24×24 altında; 10px metin okunmaz. Mobilde parmakla vurulamaz.
- Metin "x": ne yaptığı belli değil (kapat? sil?). `href="#sil"` silme çağrıştırıyor ama bu bir link; sayfa içi çapa. Yıkıcıysa onay yok.
**Düzeltme:** Ne yaptığı belirsiz; bir eylemse `button`, bir yere gidiyorsa açık metinli link olsun:
```tsx
<button type="button" aria-label="Kapat" style={{ minWidth: 44, minHeight: 44 }}>
  <span aria-hidden="true">×</span>
</button>
```
Gereksizse kaldır. Mobil için 44×44 hedef önerilir (24×24 minimumdur).

### BrokenForm.tsx:20 — Bağlamsız "Yeni!" rozeti, animasyon belirsiz, gereksiz `aria-hidden="false"`
**Kontrol:** U6, A10 · **Öncelik:** Orta
**Sorun:**
- "Yeni!" hiçbir öğeye bağlı değil; ne yeni belli değil. Dikkat çekiyor, bilgi vermiyor.
- `className="pulse"` sürekli animasyon çağrıştırıyor; CSS yok → süre, durdurulabilirlik, flaş ve `prefers-reduced-motion` doğrulanamadı. Sürekli nabız animasyonu vestibüler hassasiyeti olan kullanıcıyı rahatsız eder.
- `aria-hidden="false"` geçerli bir değer ama hiçbir şey yapmaz; kafa karıştırıcı.
**Düzeltme:** Rozeti ait olduğu öğeye bağla ya da kaldır:
```tsx
<label htmlFor="sinif">
  Sınıf <span className="badge">Yeni: 6. Sınıf eklendi</span>
</label>
```
CSS'te: `@media (prefers-reduced-motion: reduce) { .pulse { animation: none; } }`; animasyon 5 sn'den uzun sürmesin ya da kullanıcı etkileşiminde dursun. `aria-hidden="false"` kaldır.

### BrokenForm.tsx:21-26 — Tablo: `caption`, `th`, `scope` yok
**Kontrol:** A11 · **Öncelik:** Orta
**Sorun:** 2×2 tablo; başlık satırı yok. Ekran okuyucu "Matematik, 85" der ama 85'in ne olduğu (not? yüzde?) belli değil. Tablonun neyi gösterdiği (`caption`) yok. Küçük olduğu için otomatik araçlar yakalamaz.
**Düzeltme:**
```tsx
<table>
  <caption>Son dönem notları</caption>
  <thead>
    <tr><th scope="col">Ders</th><th scope="col">Not</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">Matematik</th><td>85</td></tr>
    <tr><th scope="row">Türkçe</th><td>92</td></tr>
  </tbody>
</table>
```
Not: Bu tablo bir **kayıt formunda** ne işe yarıyor, belirsiz; ilk kez kayıt olan velinin henüz notu olmaz. Kaldırılması düşünülmeli.

### BrokenForm.tsx:27 — "buraya tıklayın"
**Kontrol:** U8 · **Öncelik:** Orta
**Sorun:** Link metni hedefi söylemiyor. Ekran okuyucu link listesinde "buraya tıklayın" anlamsız. "Tıklayın" mobilde dokunma için yanlış fiil.
**Düzeltme:**
```tsx
<a href="#detay">Kayıt koşullarını görüntüle</a>
```
Gövde metni içindeyse altı çizili kalsın (CSS'te `text-decoration` kaldırılmasın).

---

## 3. Kontrol listesi dışında dikkat çeken noktalar

- **`<form>` öğesi yok.** Enter ile gönderim, tarayıcı doğrulaması (`required`, `pattern`), şifre yöneticisi/otomatik doldurma ve `onSubmit` toplu işleme çalışmaz. Tüm alanları bir `<form>` içine al.
- **`autoComplete` yok.** İlk kez kayıt yapan veli mobilde ad ve e-postayı elle yazmak zorunda; `autoComplete="name"` ve `"email"` ile tek dokunuşla dolar.
- **Mobil yerleşim:** `width={320}` sabit görsel dar ekranda taşabilir; inline stiller yerine CSS sınıfları kullan.
- **Veri gizliliği:** T.C. Kimlik No hassas veri; neden istendiği bir cümleyle açıklanmalı (güven, KVKK aydınlatma). Bu, veli kitlesinde terk oranını doğrudan etkiler.
- **Sıra:** Görsel ve rozet formun ortasında dikkat dağıtıyor; mobilde form alanları ilk ekranda görünmeli.

---

## 4. Öncelikli düzeltme sırası

1. **Kritik:** `Kaydet`'i `<button type="submit">` yap, `<form onSubmit>` ekle, `role="status"` ile sonuç bildir (satır 17).
2. **Kritik:** Tüm alanlara `label htmlFor` ekle; placeholder'ı etiket olarak kullanmayı bırak (satır 9-13).
3. **Kritik:** TC Kimlik No: `inputMode="numeric"`, `maxLength={11}`, ipucu + örnek, `aria-invalid`/`aria-describedby` ile hata metni (satır 11).
4. **Kritik:** Temizleme butonuna görünür/erişilebilir ad ve onay ekle; DOM'u değil state'i sıfırla (satır 18).
5. **Yüksek:** `h1`, `alt`, kontrast (`#9a9a9a` → en az `#595959`), `outline:none` kaldır, 16px hedefi büyüt (satır 4, 5, 6, 12, 19).
6. **Orta:** Rozeti bağla ya da kaldır, tabloya `caption`/`th`, link metnini düzelt (satır 20, 21, 27).

---

## Kısa özet

- 21 kontrolün 19'u ihlal; 2'si (`html lang`, animasyon CSS'i) dosyada olmadığı için doğrulanamadı.
- En ağır dört sorun: "Kaydet" bir `div` ve hiçbir şey yapmıyor; hiçbir alanın etiketi yok; TC Kimlik alanı mobilde sayı klavyesi açmıyor ve hata söylemiyor; çöp kutusu butonu adı olmadan, onaysız her şeyi siliyor.
- Geri kalan sorunlar (başlık, `alt`, kontrast, odak, 16px hedef, tablo başlığı, "buraya tıklayın") tek tek küçük ama hepsi birden ilk kez gelen veliyi mobilde yolda bırakır.