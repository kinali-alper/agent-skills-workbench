# UX ve Erişilebilirlik Denetimi — `BrokenForm.tsx`

**Kapsam:** Yalnız `project/BrokenForm.tsx` (30 satır). CSS (`.broken`, `.fake-btn`, `.icon-only`, `.pulse`), `index.html` ve sayfa iskeleti yok; render yapılamadı. Sayfa düzeyi kontroller (skip link, `html lang`) ve CSS'e bağlı kontroller (animasyon, link altı çizgisi) statik kaynaktan hükme bağlandı; kesin bilinemeyenler **doğrulanamaz** olarak işaretlendi.
**Bağlam:** Arayüz dili Türkçe; kullanıcı velidir, mobilde, formu ilk kez görüyor. Bu nedenle "ilk kez gören mobil kullanıcı ne anlar, dokunabilir mi, sonucu görür mü" ana ölçüt alındı.

## Özet tablo

| Kod | Hüküm | Satır | Kısa sorun |
|---|---|---|---|
| U1 | **ihlal** | :17, :18 | Kaydet hiçbir şey yapmaz; silme sessizce çalışır, durum mesajı yok |
| U2 | **ihlal** | :17 | Formdan çıkış yolu (İptal/Geri) yok |
| U3 | **ihlal** | :11 | TC Kimlik No `type="text"`, `inputMode` yok, format ipucu/örnek yok, hata metni yok |
| U4 | **ihlal** | :7, :11 | Yönerge "tüm alanlar" der, yalnız bir alan kırmızı; kırmızı kenarlık hem zorunlu hem hata sinyali |
| U5 | **ihlal** | :18 | Çöp kutusu tüm alanları onaysız ve geri alınamaz siler |
| U6 | **ihlal** | :20 | "Yeni!" rozeti bağlamsız |
| U7 | **ihlal** | :9–11 | Etiket yok, yalnız placeholder |
| U8 | **ihlal** | :27, :19 | "buraya tıklayın" ve "x" hedefi söylemez |
| A1 | **ihlal** | :4 | Başlık `div`, `h1` yok, `main` yok (skip link: doğrulanamaz) |
| A2 | **ihlal** | :5 | `img` `alt` taşımıyor |
| A3 | **ihlal** | :6 | `#9a9a9a` / `#fff` ≈ 2.8:1 (< 4.5:1) |
| A4 | **ihlal** | :9–12 | Dört form denetiminin hiçbirinde programatik etiket yok |
| A5 | **ihlal** | :11, :7 | Hata/zorunlu yalnız renkle; `aria-invalid`/`aria-describedby` yok |
| A6 | **ihlal** | :12 | `outline: 'none'`, eşdeğer odak göstergesi yok |
| A7 | **ihlal** | :17 | `div` + `onClick` buton |
| A8 | **ihlal** | :18 | Yalnız emoji (çöp kutusu) taşıyan butonda erişilebilir ad yok |
| A9 | **ihlal** | :19 | 16×16 px hedef, bağımsız link (inline metin değil) |
| A10 | **doğrulanamaz** | :20 | `.pulse` sınıfı animasyon ima eder; CSS dosyada yok |
| A11 | **ihlal** | :21 | Tabloda `caption` ve `th scope` yok (2×2, axe kaçırır) |
| A12 | **doğrulanamaz** | — | `html lang` bileşen dışında; bileşen içinde dil değişimi yok |
| A13 | **ihlal** | :18 | Sil eylemi durumu değiştirir, `aria-live`/`role="status"` yok |

**Sonuç:** 21 kontrolün 19'u ihlal, 2'si doğrulanamaz, 0'ı uygun. Öncelik sırası aşağıdaki "Düzeltme sırası" bölümünde.

---

## Kullanılabilirlik (U)

### U1 — Her eylem görünür sonuç üretir — **ihlal :17, :18**
- **Sorun (:17):** `<div className="fake-btn" onClick={() => {}}>Kaydet</div>` — tıklama boş fonksiyon çalıştırır. Veli "Kaydet"e basar, hiçbir şey olmaz; kayıt oldu mu, hata mı var bilinemez. İlk kez kullanan mobil kullanıcı için en kritik güven kırılması.
- **Sorun (:18):** Çöp kutusu butonu tüm alanları temizler ama ekranda "Form temizlendi" gibi bir mesaj yok; inputlar birden boşalır.
- **Düzeltme:** Kaydet'i gerçek `<button type="submit">` yap, `onSubmit` içinde bekleme durumu (`disabled` + "Kaydediliyor…") göster, sonuçta `role="status"` bölgeye "Kayıt alındı" / hata metni yaz veya başarı sayfasına yönlendir. Temizleme sonrasında aynı `role="status"` bölgeye "Form temizlendi" yaz.

### U2 — Her akıştan çıkış yolu var — **ihlal :17**
- **Sorun:** Formda İptal / Geri / Vazgeç yok; tek eylem "Kaydet" (çalışmayan) ve çöp kutusu. Yarım doldurulmuş veriyle sayfadan ayrılınca uyarı yok.
- **Düzeltme:** Kaydet'in yanına ikincil `<button type="button">İptal</button>` (veya "Geri" linki) ekle. Alanlarda veri varken çıkışta `beforeunload` / rota koruması ile "Girdiğiniz bilgiler kaybolacak" uyarısı göster.

### U3 — Biçimli alanlar doğru `type`/`inputmode`, format ipucu, açıklayıcı hata — **ihlal :11**
- **Sorun:** `TC Kimlik No` alanı `type="text"`; mobilde harf klavyesi açılır. `inputMode="numeric"`, `maxLength={11}`, `pattern`, `autoComplete` yok. Format ipucu ("11 haneli, boşluksuz") ve örnek yok. Hata durumunda ne yanlış / nasıl düzelir söyleyen metin yok — yalnız kırmızı kenarlık (:11 `border: '2px solid red'`).
- **Ek (:10):** `type="email"` doğru; ancak `autoComplete="email"` ve etiket eksik (U7/A4).
- **Düzeltme:** `<input id="tc" type="text" inputMode="numeric" pattern="[0-9]{11}" maxLength={11} aria-describedby="tc-hint tc-err">` + `<p id="tc-hint">11 haneli, yalnız rakam. Örn: 12345678901</p>`. Hata metni: "TC Kimlik No 11 haneli olmalı; 9 hane girdiniz."

### U4 — Zorunlu ve hata işareti ayrı; yönerge gerçekle örtüşür — **ihlal :7, :11**
- **Sorun:** :7 "Lütfen tüm alanları doldurun. Zorunlu alanlar kırmızı ile işaretlidir." — iki cümle çelişir (tümü zorunluysa işaretlemeye gerek yok). Fiilen yalnız TC alanı (:11) kırmızı; ad, e-posta, sınıf işaretsiz. Kırmızı kenarlık aynı zamanda evrensel "hata" sinyali; veli daha yazmadan alanı hatalı sanır.
- **Düzeltme:** Zorunlu için etiket yanında `*` + üstte "* ile işaretli alanlar zorunludur" yönergesi ve `required`/`aria-required`. Hata için ayrı sinyal: kırmızı kenarlık **+ ikon + metin**, yalnız gönderimden sonra. Yönergeyi gerçek durumla eşitle.

### U5 — Yıkıcı eylem onay ister ya da geri alma verir — **ihlal :18**
- **Sorun:** Çöp kutusu butonu `document.querySelectorAll('.broken input').forEach(i => i.value = '')` ile tüm alanları anında siler; onay yok, geri alma yok. Mobilde yanlışlıkla dokunulması kolay (Kaydet'in hemen yanında). Ayrıca `href="#sil"` (:19) adıyla ikinci bir "sil" bağlantısı var; ne sildiği belirsiz.
- **Düzeltme:** Temizleme öncesi onay (erişilebilir dialog: "Tüm alanlar silinecek. Emin misiniz?") veya 5–10 sn "Geri al" içeren `role="status"` toast. Butonu Kaydet'ten uzaklaştır ve ikincil stilde göster. Ayrıca DOM'a doğrudan yazmak yerine React state'i sıfırla (kontrollü inputlar).

### U6 — Rozet/uyarı bir içeriğe bağlı — **ihlal :20**
- **Sorun:** `<div className="pulse" aria-hidden="false">Yeni!</div>` — neyin yeni olduğu yok; hiçbir öğeye bağlı değil. `pulse` sınıfı dikkat çekici animasyon ima eder. `aria-hidden="false"` anlamsız (varsayılan zaten görünür).
- **Düzeltme:** Rozeti ilgili öğeye bağla ve içeriği söyle: "Yeni: 6. Sınıf kaydı açıldı". Bağlı içerik yoksa rozeti kaldır. `aria-hidden="false"` özniteliğini sil.

### U7 — Etiketler kalıcı; placeholder etiket yerine geçmez — **ihlal :9, :10, :11, :13**
- **Sorun:** Üç `input` (:9–11) yalnız `placeholder` taşır; yazmaya başlayınca "Ad Soyad / E-posta / TC Kimlik No" kaybolur, veli hangi kutuya ne yazdığını göremez. `select` (:12) etiketi `disabled` option (:13) ile taklit edilmiş; seçim yapıldığında kaybolur.
- **Düzeltme:** Her denetimin üstüne kalıcı `<label htmlFor="...">`. Placeholder yalnız örnek için ("Örn: Ayşe Yılmaz").

### U8 — Link/buton metni hedefi söyler — **ihlal :27, :19**
- **Sorun (:27):** `<a href="#detay">buraya tıklayın</a>` — hedef yok; ekran okuyucu link listesinde "buraya tıklayın" anlamsız.
- **Sorun (:19):** `<a href="#sil">x</a>` — "x" ne kapatır, ne siler belli değil.
- **Sorun (:18):** Buton metni emoji; eylem sözcüğü yok (bkz. A8).
- **Düzeltme:** "Kayıt detaylarını görüntüle", "Formu temizle", "Kapat" gibi arayüz dilinde eylem+hedef metni.

---

## Erişilebilirlik (A)

### A1 — Tek `h1`, hiyerarşik başlıklar, `main`, skip link — **ihlal :4** (skip link: doğrulanamaz)
- **Sorun:** :4 `<div style={{ fontSize: 28, fontWeight: 700 }}>Öğrenci Kayıt</div>` — görsel başlık, programatik başlık değil. Sayfada `h1` yok; ekran okuyucu başlık gezinmesi boş. `main` landmark yok; kök `<div className="broken">`. Skip link sayfa düzeyinde olduğundan bileşen dosyasından doğrulanamaz.
- **Düzeltme:** `<main>` sarmalayıcı (sayfa iskeleti sağlamıyorsa), `<h1>Öğrenci Kayıt</h1>`, form bölümleri için `h2`. Stil CSS ile.

### A2 — Görselde anlamlı `alt` — **ihlal :5**
- **Sorun:** `<img src="https://picsum.photos/seed/okul/320/120" width={320} height={120} />` — `alt` özniteliği yok; ekran okuyucu dosya adını/URL'yi okur.
- **Düzeltme:** Süs görseliyse `alt=""`; bilgi taşıyorsa (okul logosu vb.) `alt="… Okulu logosu"`. Mobilde `width={320}` sabit; `max-width: 100%` ile taşmayı önle.

### A3 — Metin kontrastı ≥ 4.5:1 — **ihlal :6**
- **Sorun:** `color: '#9a9a9a'` üzerinde `background: '#fff'` → hesaplanan oran ≈ **2.8:1** (gereken 4.5:1). Bu metin zorunlu alan yönergesi; okunmaması veliyi formu yanlış doldurmaya iter. Ayrıca :19 `fontSize: 10` — kontrast bilinmiyor ama 10 px metin mobilde okunmaz.
- **Düzeltme:** Metin rengini en az `#767676` (4.54:1) veya tercihen `#595959` (7:1) yap. :19'daki 10 px metni kaldır ya da ≥ 14 px.

### A4 — Her form denetimi programatik etikete bağlı — **ihlal :9, :10, :11, :12**
- **Sorun:** Hiçbir `input`/`select` öğesinde `id`, `<label htmlFor>`, `aria-label` veya `aria-labelledby` yok. Ekran okuyucu "düzenleme kutusu" der. Placeholder bazı okuyucularda okunur ama standart etiket sayılmaz ve yazınca kaybolur.
- **Düzeltme:** `<label htmlFor="ad">Ad Soyad</label><input id="ad" name="ad" autoComplete="name" …>`; select için `<label htmlFor="sinif">Sınıf</label>`.

### A5 — Renk tek sinyal değil — **ihlal :11, :7**
- **Sorun:** :11 zorunlu/hata bilgisi yalnız `border: '2px solid red'`. `aria-invalid`, `aria-describedby`, ikon, metin yok. :7 yönergesi de "kırmızı ile işaretlidir" diyerek yalnız renge dayanır; renk körü veli işareti göremez. Gövde içi linklerin (:27, :19) altı çizili mi bilinmiyor — CSS yok, doğrulanamaz; varsayılan tarayıcı stili korunuyorsa uygundur.
- **Düzeltme:** Hata: `aria-invalid="true"` + `aria-describedby="tc-err"` + görünür ikonlu hata metni. Zorunlu: `*` + `required`. Yönergeyi "* ile işaretli" olarak değiştir.

### A6 — Odak görünür ve kalır — **ihlal :12**
- **Sorun:** `<select style={{ outline: 'none' }}>` — odak halkası kaldırıldı, eşdeğer gösterge (`box-shadow`, `border-color` vb.) yok. Klavye/ekran okuyucu kullanıcısı select'e odaklandığını göremez. Diğer öğelerde `onfocus=blur` yok (uygun).
- **Düzeltme:** `outline: none` sil; `:focus-visible { outline: 3px solid #005a9c; outline-offset: 2px }` (≥ 3:1) uygula.

### A7 — Etkileşimli öğe native — **ihlal :17**
- **Sorun:** `<div className="fake-btn" onClick>` — klavyeyle odaklanamaz (tabindex yok), Enter/Space çalışmaz, ekran okuyucu buton olarak tanımaz, form `submit` tetiklemez. Ana eylem tamamen klavye/ekran okuyucu dışı.
- **Düzeltme:** `<button type="submit" className="fake-btn">Kaydet</button>`; tüm alanları `<form onSubmit>` içine al.

### A8 — Yalnız ikon/emoji denetimde erişilebilir ad — **ihlal :18**
- **Sorun:** `<button className="icon-only">` içinde yalnız çöp kutusu emojisi — erişilebilir ad emoji'nin Unicode adı ("wastebasket" / "çöp kutusu", tarayıcıya göre) olur; eylem ("Formu temizle") söylenmez; bazı okuyucularda hiç okunmaz.
- **Düzeltme:** `<button aria-label="Formu temizle">` veya `<span aria-hidden="true">[emoji]</span><span className="sr-only">Formu temizle</span>`.

### A9 — Tıklama hedefi ≥ 24×24 CSS px — **ihlal :19**
- **Sorun:** `<a href="#sil" style={{ display: 'inline-block', width: 16, height: 16, fontSize: 10 }}>x</a>` — 16×16 px, bağımsız (inline metin akışında değil, `inline-block`). Mobilde parmakla isabet neredeyse imkânsız; yanındaki çöp kutusu butonuyla karışır. :18 `.icon-only` boyutu CSS'te; doğrulanamaz ama emoji tek karakter olduğu için küçük kalma riski yüksek.
- **Düzeltme:** En az 24×24 (mobilde 44×44 önerilir); `padding` ile büyüt. Gerçekten silme eylemiyse `<button>` yap ve U5 onayına bağla.

### A10 — Otomatik hareket durdurulabilir, `prefers-reduced-motion` — **doğrulanamaz :20**
- **Durum:** `className="pulse"` sürekli nabız animasyonu ima eder ancak CSS dosyada yok. Animasyon 5 sn'yi aşıp durdurulamıyorsa 2.2.2 ihlali olur.
- **Öneri:** Eğer `.pulse` sonsuz animasyonsa `animation-iteration-count` sınırla (≤ 5 sn) veya durdurma denetimi ekle; `@media (prefers-reduced-motion: reduce) { .pulse { animation: none } }`.

### A11 — Veri tablosunda `caption` ve `th scope` — **ihlal :21**
- **Sorun:** :21–26 tablo yalnız `td` içerir; `caption`, `thead`, `th scope="row|col"` yok. 2×2 olduğu için axe uyarı vermez; elle kontrolde ekran okuyucu "Matematik, 85" der, bunun ders ve not olduğunu söylemez.
- **Düzeltme:** `<caption>Sınav notları</caption><thead><tr><th scope="col">Ders</th><th scope="col">Not</th></tr></thead>` ve satır başı `<th scope="row">Matematik</th>`. Tablo formla ilişkisizse ayrı bölüme başlıkla taşı.

### A12 — `html lang` doğru; dil değişen parçalarda `lang` — **doğrulanamaz**
- **Durum:** `<html lang>` bileşen dışında (index.html / layout); dosyada yok. Bileşen içi tüm metin Türkçe; dil değişen parça yok, bu yüzden bileşen düzeyinde ek `lang` gerekmiyor.
- **Öneri:** Sayfa iskeletinde `<html lang="tr">` olduğunu doğrula.

### A13 — Canlı güncellemeler duyurulur — **ihlal :18**
- **Sorun:** :18 silme eylemi tüm alanları boşaltır; hiçbir `aria-live` / `role="status"` bölge yok. Ekran okuyucu kullanıcısı formun temizlendiğini fark etmez. Doğrulama mesajı da yok (:11), gelecekte eklenirse duyurulmayacak.
- **Düzeltme:** Form altına kalıcı `<div role="status" aria-live="polite" id="form-status"></div>`; temizleme / kayıt / hata sonuçlarını buraya yaz.

---

## Kontrol listesi dışında dikkat çekenler

- **:18 doğrudan DOM yazımı** (`document.querySelectorAll(...).value = ''`): React state'iyle senkron değil; kontrollü inputlara geçilince çalışmaz. Silme mantığını state'e taşı.
- **:5 sabit 320 px görsel**: dar ekranda (≤ 360 px) yatay kaydırma riski.
- **:19 `fontSize: 10`**: okunabilirlik; 1.4.4 (200 % büyütme) açısından da zayıf.
- **:9–16 `<form>` yok**: Enter ile gönderim, tarayıcı doğrulaması ve `autoComplete` çalışmaz.
- **:13 `disabled` placeholder option**: seçildikten sonra "Sınıf seçin"e geri dönülemez; etiket görevi göremez (bkz. U7).
- **Mobil klavye ipuçları:** `autoComplete="name"`, `autoComplete="email"`, `inputMode="numeric"` eksik; ilk kez dolduran veli için yazma yükünü azaltır.

## Düzeltme sırası (veli, mobil, ilk kez)

1. **Kaydet'i gerçek buton yap ve sonuç göster** (A7, U1, A13) — form çalışmıyor.
2. **Etiketleri ekle** (U7, A4) — veli hangi kutuya ne yazacağını göremiyor.
3. **Silme butonuna ad + onay** (A8, U5) — yanlışlıkla tüm form kaybı.
4. **TC Kimlik No alanını numerik yap, ipucu ve hata metni ekle** (U3, A5, U4).
5. **Kontrast, başlık, alt, odak** (A3, A1, A2, A6).
6. **Küçük hedef ve anlamsız link metinleri** (A9, U8, U6).
7. **Tablo başlıkları** (A11).
8. CSS geldiğinde A10 ve link altı çizgisini doğrula; sayfa iskeletinde `lang="tr"` ve skip link'i doğrula (A12, A1).