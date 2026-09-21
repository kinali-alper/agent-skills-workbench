# UX ve Erişilebilirlik Denetimi — `BrokenForm.tsx`

**Kapsam:** Yalnız kaynak dosya (`project/BrokenForm.tsx`, 30 satır). Sayfa render edilemedi; CSS (`.broken`, `.fake-btn`, `.icon-only`, `.pulse`), üst düzey `html`/`main` yapısı ve gerçek piksel ölçüleri dosyada yok. Bu yüzden görsel/CSS'e bağlı maddeler "doğrulanamaz" olarak işaretlendi.
**Bağlam:** Arayüz dili Türkçe; kullanıcılar veliler, mobil, ilk kez kullanıyor. Bu kitle için etiket kalıcılığı, dokunma hedefi boyutu, sayısal klavye ve geri alınabilir eylemler kritik.
**Yöntem:** Verilen kontrol listesi (U1–U8, A1–A13) satır satır uygulandı; her satıra tam olarak bir hüküm verildi: **ihlal :N** / **uygun** / **uygulanamaz** / **doğrulanamaz**.

---

## Özet tablo

| Kod | Hüküm | Kısa gerekçe |
|---|---|---|
| U1 | **ihlal :17** | "Kaydet" `onClick={() => {}}` — hiçbir sonuç, durum mesajı, bekleme göstergesi yok |
| U2 | **ihlal :17** | Akışta İptal / Geri yok; yarım veri için çıkış uyarısı yok |
| U3 | **ihlal :11** | TC Kimlik No `type="text"`, `inputMode`/`maxLength`/`pattern`/format ipucu yok; hata metni hiç yok |
| U4 | **ihlal :7** | Yönerge "tüm alanları doldurun" derken zorunluyu "kırmızı"yla işaretliyor; kırmızı kenarlık (:11) hem zorunlu hem hata sinyali olarak okunur |
| U5 | **ihlal :18** | 🗑 butonu tüm alanları onaysız ve geri alınamaz şekilde siliyor; `#sil` linki (:19) de onaysız |
| U6 | **ihlal :20** | "Yeni!" rozeti hiçbir içeriğe bağlı değil; `pulse` sınıfıyla bağlamsız dikkat çekici |
| U7 | **ihlal :9** | Üç `input` (:9–:11) yalnız `placeholder` taşıyor; kalıcı `label` yok |
| U8 | **ihlal :27** | "buraya tıklayın" hedefi söylemiyor; "x" (:19) eylemi söylemiyor |
| A1 | **ihlal :4** | Başlık `div`+stil, `h1` yok; `main` yok. Atlama linki: bileşen dosyası → doğrulanamaz (liste notu gereği) |
| A2 | **ihlal :5** | `img`'de `alt` yok (ne anlamlı metin ne `alt=""`) |
| A3 | **ihlal :6** | `#9a9a9a` / `#fff` ≈ 2.85:1 < 4.5:1 (normal metin) |
| A4 | **ihlal :9** | Dört form denetimi (:9, :10, :11, :12) hiçbirinde `label for` / `aria-labelledby` yok |
| A5 | **ihlal :11** | Zorunlu/hata durumu yalnız kırmızı kenarlıkla; `aria-invalid`/`aria-describedby`/metin/ikon yok |
| A6 | **ihlal :12** | `select`'te `outline: 'none'`, eşdeğer gösterge yok; `.fake-btn` (:17) zaten odak alamıyor |
| A7 | **ihlal :17** | `div` + `onClick` ile "Kaydet"; native `button` değil, klavye/AT için erişilemez |
| A8 | **ihlal :18** | Yalnız emoji (🗑) taşıyan `button`'da `aria-label`/gizli metin yok |
| A9 | **ihlal :19** | Link 16×16 CSS px, inline metin linki değil (`display:inline-block`); 24×24 altında |
| A10 | **doğrulanamaz** | `.pulse` (:20) sürekli animasyon ima ediyor; CSS dosyada yok — süre, durdurma, `prefers-reduced-motion` kontrol edilemedi |
| A11 | **ihlal :21** | Tablo 2×2, `caption` ve `th scope` yok — tam da "axe'ten kaçan küçük tablo" örneği |
| A12 | **doğrulanamaz** | `html lang` bileşen dosyasının dışında; dosya içinde dil değişen parça yok |
| A13 | **ihlal :18** | Alanların silinmesi (ve :17 kaydetme) hiçbir `aria-live`/`role="status"` bölgesiyle duyurulmuyor |

**Sonuç:** 21 satırdan 19 ihlal, 2 doğrulanamaz, 0 uygun, 0 uygulanamaz.

---

## Ayrıntılı bulgular (dosya:satır → sorun → düzeltme)

### U — Kullanılabilirlik

**U1 — Eylem sonucu görünür değil · ihlal · `BrokenForm.tsx:17`**
Sorun: `<div className="fake-btn" onClick={() => {}}>Kaydet</div>` — tıklama boş fonksiyon çalıştırır; kullanıcı kaydedildi mi, hata var mı, bekliyor mu bilemez. İlk kez kullanan bir veli tekrar tekrar basar.
Düzeltme: Bileşeni `<form onSubmit={handleSubmit}>` içine al; gönderimde `isSubmitting` durumu ile butonu `disabled` yap ve "Gönderiliyor…" metni göster; sonuçta `<p role="status">Kayıt alındı. Onay e-postası gönderildi.</p>` ya da yönlendirme. Hatada `role="alert"` ile özet.

**U2 — Çıkış yolu yok · ihlal · `BrokenForm.tsx:17`**
Sorun: Formun tek eylemi "Kaydet"; İptal/Geri yok. Yarım doldurulmuş veriyle sayfadan çıkışta uyarı yok.
Düzeltme: "Kaydet" yanına ikincil `<button type="button">Vazgeç</button>` (geri yönlendirme). Form kirliyse (`isDirty`) `beforeunload` / router guard ile "Girdiğiniz bilgiler kaydedilmedi. Çıkmak istiyor musunuz?" onayı.

**U3 — Biçimli alan desteği yok · ihlal · `BrokenForm.tsx:11`**
Sorun: `<input type="text" placeholder="TC Kimlik No" />` — mobilde tam klavye açılır, 11 hane sınırı yok, format ipucu/örnek yok, hata metni hiç yok. E-posta (:10) için de format ipucu ve hata metni yok.
Düzeltme:
```tsx
<label htmlFor="tckn">T.C. Kimlik No</label>
<input id="tckn" type="text" inputMode="numeric" pattern="[0-9]{11}" maxLength={11}
       autoComplete="off" aria-describedby="tckn-hint tckn-err" required />
<p id="tckn-hint">11 haneli, yalnız rakam. Örnek: 12345678901</p>
{error && <p id="tckn-err" role="alert">Kimlik numarası 11 hane olmalı; siz 9 hane girdiniz.</p>}
```
Hata metni **ne** yanlış (hane sayısı) ve **nasıl** düzelir (11 rakam) söylesin. E-posta için `inputMode="email"`, `autoComplete="email"`, hata: "E-posta adresinde @ işareti eksik."

**U4 — Zorunlu ve hata işareti aynı sinyal; yönerge durumla çelişiyor · ihlal · `BrokenForm.tsx:7`**
Sorun: Metin "Lütfen **tüm** alanları doldurun" derken aynı cümlede "Zorunlu alanlar kırmızı ile işaretlidir" diyor — hepsi zorunluysa işarete gerek yok, değilse "tüm" yanlış. Tek kırmızı kenarlık `:11`'de; zorunlu mu, hatalı mı ayrılamıyor. Kalan alanlarda (:9, :10, :12) hiç işaret yok.
Düzeltme: Yönergeyi gerçek durumla eşle: "Tüm alanlar zorunludur." (işaret yok) **veya** "* ile işaretli alanlar zorunludur" + her etikette `<span aria-hidden="true">*</span>`. Hata için ayrı sinyal: `aria-invalid="true"` + hata metni + ikon; kırmızı kenarlığı yalnız hata için kullan.

**U5 — Yıkıcı eylem onaysız · ihlal · `BrokenForm.tsx:18`**
Sorun: 🗑 butonu `document.querySelectorAll('.broken input').forEach(i => (i.value = ''))` ile tüm girişleri anında siliyor; onay yok, geri alma yok. Mobilde "Kaydet"in hemen yanında — yanlış dokunma kaçınılmaz. `:19`'daki `#sil` linki de adıyla yıkıcı eylem ima ediyor, onaysız.
Düzeltme: Silmeden önce `confirm`/modal: "Tüm alanlar temizlenecek. Devam edilsin mi?" ya da 5–10 sn "Geri al" içeren `role="status"` bildirimi. Butonu "Kaydet"ten uzağa, ikincil stile al. `#sil` linkini ya kaldır ya da net etiketli, onaylı `button`a çevir.

**U6 — Bağlamsız rozet · ihlal · `BrokenForm.tsx:20`**
Sorun: `<div className="pulse" aria-hidden="false">Yeni!</div>` — neyin yeni olduğu belirsiz, hiçbir içeriğe bağlı değil, `pulse` ile sürekli dikkat çekiyor. `aria-hidden="false"` etkisizdir (varsayılan zaten görünür).
Düzeltme: Rozeti ilgili öğeye bağla ve içerik ver: `<span className="badge">Yeni: 2026–27 kayıt dönemi açıldı</span>`; ya da tamamen kaldır. `aria-hidden="false"` niteliğini sil.

**U7 — Placeholder etiket yerine kullanılmış · ihlal · `BrokenForm.tsx:9` (ayrıca :10, :11)**
Sorun: Üç girişte yalnız `placeholder="Ad Soyad" / "E-posta" / "TC Kimlik No"`. Kullanıcı yazmaya başlayınca etiket kaybolur; ilk kez dolduran veli hangi alanda olduğunu unutur; hata düzeltmede alan adı görünmez.
Düzeltme: Her giriş için görünür `<label htmlFor>`; placeholder yalnız örnek için ("örn. Ayşe Yılmaz") ya da hiç.

**U8 — Link/buton metni hedefi söylemiyor · ihlal · `BrokenForm.tsx:27` (ayrıca :19)**
Sorun: `<a href="#detay">buraya tıklayın</a>` — ekran okuyucu link listesinde anlamsız; hedef belirsiz. `:19` `x` metni eylemi söylemiyor.
Düzeltme: `<a href="#detay">Kayıt koşullarını görüntüle</a>` (gerçek hedefe göre). `:19` için görünür/erişilebilir metin: "Formu temizle" ya da "Kapat".

### A — Erişilebilirlik (WCAG 2.2)

**A1 — Başlık/landmark yapısı · ihlal · `BrokenForm.tsx:4`**
Sorun: Sayfa başlığı `<div style={{fontSize:28,fontWeight:700}}>Öğrenci Kayıt</div>` — görsel başlık, programatik başlık değil (1.3.1, 2.4.6). `main` landmark yok. Atlama linki sayfa düzeyi olduğu için bu dosyadan doğrulanamaz (liste notu gereği).
Düzeltme: `<main><h1>Öğrenci Kayıt</h1>…</main>` (stil CSS'te kalsın). Alt bölümler (notlar tablosu vb.) `h2`.

**A2 — Görselde alt yok · ihlal · `BrokenForm.tsx:5`**
Sorun: `<img src="https://picsum.photos/seed/okul/320/120" width={320} height={120} />` — `alt` niteliği yok; ekran okuyucu dosya adını/URL'yi okur.
Düzeltme: Süs görselse `alt=""`; bilgi taşıyorsa anlamlı Türkçe metin ("Okul binası ön cephesi"). Ayrıca `picsum.photos` rastgele üçüncü taraf görsel — üretimde yerel varlık kullan.

**A3 — Metin kontrastı düşük · ihlal · `BrokenForm.tsx:6`**
Sorun: `color:'#9a9a9a'` / `background:'#fff'` → yaklaşık **2.85:1**; normal boyut metin için 4.5:1 gerekir. Bu paragraf form yönergesi — kritik bilgi.
Düzeltme: En az `#767676` (4.54:1); önerilen `#595959` (7:1). Diğer renkler CSS'te olduğundan doğrulanamadı.

**A4 — Form denetimleri etiketsiz · ihlal · `BrokenForm.tsx:9` (ayrıca :10, :11, :12)**
Sorun: Üç `input` ve `select`'in hiçbirinde `id`+`label htmlFor` ya da `aria-labelledby` yok. `select`'te `disabled` placeholder seçeneği ("Sınıf seçin") etiket yerine geçmez.
Düzeltme: Her denetim için `id` ve `<label htmlFor="...">`; `select` için `<label htmlFor="sinif">Sınıf</label>`. `autoComplete="name"`, `autoComplete="email"` ekle (1.3.5).

**A5 — Renk tek sinyal · ihlal · `BrokenForm.tsx:11`**
Sorun: `style={{ border: '2px solid red' }}` — zorunlu/hata durumu yalnız renkle; `aria-invalid`, `aria-describedby`, metin veya ikon yok. `:27` gövde linki için alt çizgi CSS'te — dosyadan doğrulanamaz (tarayıcı varsayılanı altı çizili, `.broken a` kuralı bilinmiyor).
Düzeltme: `aria-invalid={!!error}` + `aria-describedby="tckn-err"` + görünür hata metni ve ikon (`<svg aria-hidden="true">` + metin). Zorunluluk için `required` + görünür `*`.

**A6 — Odak göstergesi kaldırılmış · ihlal · `BrokenForm.tsx:12`**
Sorun: `<select style={{ outline: 'none' }}>` — klavye odağı görünmez, eşdeğer gösterge yok (2.4.7). `:17` `div` hiç odak alamıyor; `:18`/`:19` için CSS bilinmiyor.
Düzeltme: `outline:'none'` sil; global `:focus-visible { outline: 3px solid #1a56db; outline-offset: 2px; }` (arka planla ≥ 3:1). Odağı script ile düşüren kod (`onfocus=blur`) yok — bu alt madde uygun.

**A7 — Etkileşimli öğe native değil · ihlal · `BrokenForm.tsx:17`**
Sorun: `<div className="fake-btn" onClick>` — Tab ile ulaşılamaz, Enter/Space çalışmaz, rolü "button" değil; ekran okuyucu düz metin okur.
Düzeltme: `<button type="submit" className="btn-primary">Kaydet</button>` ve `<form onSubmit>`. `role="button"`+`tabIndex`+key handler yaması yerine native öğe.

**A8 — Yalnız emoji denetimde erişilebilir ad yok · ihlal · `BrokenForm.tsx:18`**
Sorun: `<button className="icon-only">🗑</button>` — erişilebilir adı emoji karakterinin Unicode adı ("wastebasket" / yerelleştirilmiş) olur; Türkçe ve eylem belirtmez. Sesli kontrol için de ad yok (2.5.3).
Düzeltme: `<button type="button" aria-label="Formu temizle">` + `<span aria-hidden="true">🗑</span>`; tercihen görünür metin "Temizle" (mobil veli için ikon tek başına belirsiz).

**A9 — Tıklama hedefi çok küçük · ihlal · `BrokenForm.tsx:19`**
Sorun: `width:16, height:16, fontSize:10, display:'inline-block'` — 16×16 CSS px, 24×24 minimumun altında; inline metin linki istisnası uygulanmaz (blok gibi konumlanmış bağımsız denetim). Mobilde parmakla isabet neredeyse imkânsız.
Düzeltme: En az 24×24 (mobil için 44×44 önerilir): `min-width:44px; min-height:44px; display:inline-flex; align-items:center; justify-content:center`. `:18` emoji butonunun boyutu CSS'te — doğrulanamadı, aynı kural uygulanmalı.

**A10 — Otomatik hareket · doğrulanamaz · (`BrokenForm.tsx:20` risk)**
Sorun: `className="pulse"` adıyla sürekli animasyon ima ediyor; CSS dosyada yok — süre (>5 sn?), durdurma kontrolü, flaş frekansı, `prefers-reduced-motion` doğrulanamadı.
Düzeltme (önleyici): Eğer `.pulse` sonsuz `animation` ise `@media (prefers-reduced-motion: reduce) { .pulse { animation: none; } }` ekle ya da animasyonu 3 iterasyonla sınırla; en iyisi U6 gereği rozeti kaldır.

**A11 — Veri tablosunda caption/th yok · ihlal · `BrokenForm.tsx:21`**
Sorun: `<table><tbody><tr><td>Matematik</td><td>85</td></tr>…` — `caption` yok, `thead`/`th scope` yok. 2×2 boyutunda: otomatik araçlar (axe) tipik olarak atlar; elle kontrolde ihlal. Ekran okuyucu "85"in ne olduğunu söyleyemez.
Düzeltme:
```tsx
<table>
  <caption>Dönem notları</caption>
  <thead><tr><th scope="col">Ders</th><th scope="col">Not</th></tr></thead>
  <tbody><tr><th scope="row">Matematik</th><td>85</td></tr>…</tbody>
</table>
```

**A12 — `html lang` · doğrulanamaz**
Sorun: `<html lang>` bileşen dosyasının dışında (index.html / root layout). Dosya içinde dil değişen parça yok — parça düzeyinde `lang` gerekmiyor.
Düzeltme (kontrol için): Kök belgede `<html lang="tr">` olduğunu doğrula.

**A13 — Canlı güncellemeler duyurulmuyor · ihlal · `BrokenForm.tsx:18` (ayrıca :17)**
Sorun: 🗑 tüm alanları siliyor ama hiçbir `aria-live`/`role="status"` bölgesi yok; ekran okuyucu kullanıcısı formun boşaldığını fark etmez. "Kaydet" sonucu (var olsa bile) duyurulacak bir bölge yok. Doğrulama hataları için de canlı bölge tanımlı değil.
Düzeltme: Form içinde kalıcı `<div role="status" aria-live="polite" className="sr-only">{statusMsg}</div>`; temizlemede "Form temizlendi", kaydetmede sonuç mesajı; alan hataları `role="alert"` ya da `aria-describedby` ile bağlı.

---

## Kontrol listesi dışı ek gözlemler

1. **`<form>` öğesi yok** (`:3`–`:28`): Enter ile gönderim, tarayıcı doğrulaması (`required`, `pattern`), otomatik doldurma çalışmaz. Tüm denetimleri `<form onSubmit>` içine al.
2. **Doğrudan DOM manipülasyonu** (`:18`): `document.querySelectorAll(...)` ile değer sıfırlama React durumunu atlar; kontrollü bileşenlerde görsel/durum uyumsuzluğu yaratır. `useState`/`reset()` kullan.
3. **`autoComplete` eksik** (`:9`, `:10`): WCAG 1.3.5 — `name`, `email` değerleri mobil velinin yazma yükünü azaltır.
4. **Mobil yazı boyutu** (`:9`–`:12`): iOS Safari 16px altı girişlerde yakınlaştırır; `font-size: 16px` garanti et (CSS doğrulanamadı).
5. **Yıkıcı eylemler birincil eylemin yanında** (`:17`–`:19`): "Kaydet" → 🗑 → "x" ardışık; mobilde başparmak hatası kaçınılmaz. Yıkıcı eylemleri ayrı hizaya, ikincil stile al.
6. **`#sil` / `#detay` hash linkleri** (`:19`, `:27`): Hedef bölüm dosyada yok; kırık iç bağlantı olabilir — doğrulanamaz.
7. **Harici rastgele görsel** (`picsum.photos`, `:5`): Her yüklemede farklı içerik olabilir; `alt` yazılamaz hale gelir; gizlilik ve performans riski.

---

## Öncelik sırası (veli / mobil / ilk kez bağlamı için)

1. `:17` `div` → native `button` + `form onSubmit` + `role="status"` sonuç mesajı (A7, U1, A13)
2. `:9`–`:12` kalıcı `label`lar + `autoComplete` (U7, A4)
3. `:18` onay/geri alma + `aria-label` (U5, A8)
4. `:11` TC Kimlik `inputMode="numeric"`, `maxLength=11`, ipucu, hata metni, `aria-invalid`/`aria-describedby` (U3, A5, U4)
5. `:6` kontrast `#595959`; `:12` outline geri; `:19` hedef ≥ 44px; `:5` alt; `:4` h1/main; `:21` caption/th; `:27` link metni; `:20` rozeti kaldır

---

**Kısa özet:**
- 21 kontrol satırının 19'u ihlal; yalnız 2'si (animasyon, `html lang`) dosyadan doğrulanamadı.
- En ağır sorunlar: "Kaydet" gerçek buton değil ve hiç çalışmıyor; hiçbir alanın etiketi yok; çöp kutusu onaysız her şeyi siliyor.
- TC Kimlik alanı mobilde sayısal klavye açmıyor, hane sınırı ve hata mesajı yok.
- Düşük kontrastlı yönerge, alt'sız görsel, 16px'lik "x" linki ve başlıksız tablo hızlı düzeltilebilir.