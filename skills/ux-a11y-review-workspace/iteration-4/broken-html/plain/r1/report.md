# UX ve Erişilebilirlik Denetimi — `broken.html`

**Dosya:** `project/broken.html` (39 satır, düz HTML; başka proje dosyası yok)
**Yöntem:** Statik kaynak incelemesi. Sayfa render edilmedi; hesaplanmış boyut, gerçek odak halkası ve görsel içeriği gibi yalnız tarayıcıda görülebilecek noktalar "doğrulanamaz" olarak işaretlendi. Kontrast oranları WCAG formülüyle kaynaktaki renk kodlarından hesaplandı.
**Bağlam:** Arayüz dili Türkçe. Kullanıcı kitlesi veliler — mobil cihazda, sayfayı ilk kez kullanıyor. Bu yüzden sayısal klavye, dokunma hedefi boyutu ve sade dil gibi noktalar ayrıca vurgulandı.
**Hüküm sözlüğü:** **ihlal :N** (N = birincil satır; diğer satırlar notta) / **uygun** / **uygulanamaz** / **doğrulanamaz**.

---

## Özet tablo

| Kod | Hüküm | Birincil kanıt |
|---|---|---|
| U1 | **ihlal :29** | Çöp kutusu butonu ve `#sil` linki hiçbir sonuç üretmiyor |
| U2 | **ihlal :28** | Formdan çıkış yolu (İptal / Geri) yok |
| U3 | **ihlal :22** | TC Kimlik No `type="text"`, `inputmode`/format ipucu/hata metni yok |
| U4 | **ihlal :19** | "Zorunlu = kırmızı" yönergesi gerçek durumla örtüşmüyor; zorunlu ve hata aynı sinyal |
| U5 | **ihlal :29** | Silme eylemleri onay/geri alma vermiyor |
| U6 | **ihlal :31** | "Yeni!" rozeti hiçbir içeriğe bağlı değil |
| U7 | **ihlal :20** | Tüm alanlarda placeholder etiket yerine kullanılmış |
| U8 | **ihlal :36** | "buraya tıklayın" hedefi söylemiyor |
| A1 | **ihlal :17** | `h1` yok (stil verilmiş `div`), `main` yok |
| A2 | **ihlal :18** | `img` üzerinde `alt` özniteliği hiç yok |
| A3 | **ihlal :19** | `#9a9a9a` / `#fff` ≈ 2,8:1 |
| A4 | **ihlal :20** | Hiçbir form denetimi programatik etikete bağlı değil |
| A5 | **ihlal :22** | Kırmızı kenarlık tek sinyal; `aria-invalid`/`aria-describedby`/metin yok |
| A6 | **ihlal :23** | `outline:none`, eşdeğer gösterge yok; sayfada `:focus-visible` tanımı yok |
| A7 | **ihlal :28** | `div` + `onclick` buton yerine kullanılmış |
| A8 | **ihlal :29** | Yalnız emoji taşıyan butonda erişilebilir ad yok |
| A9 | **ihlal :30** | 16×16 px hedef |
| A10 | **ihlal :12** | `animation … 1s infinite`, durdurma yok, `prefers-reduced-motion` yok |
| A11 | **ihlal :32** | 2×2 tabloda `caption` ve `th` yok (axe'ten kaçan küçük tablo) |
| A12 | **uygun** | `html lang="tr"` doğru; dil değişen parça yok |
| A13 | **uygulanamaz** | Sayfada odak almayan durum mesajı/toast/doğrulama yok; tek geri bildirim `alert()` (odak alır, 4.1.3 kapsamı dışı). U1 düzeltmesi eklenirken `role="status"` zorunlu |

**Sonuç:** 21 kontrolün 19'u ihlal, 1'i uygun, 1'i uygulanamaz.

---

## U — Kullanılabilirlik bulguları

### U1 — Eylemler görünür sonuç üretir mi? — **ihlal :29**
- `broken.html:29` — `<button class="icon-only">🗑</button>`: hiçbir `type`, `onclick` veya form bağlamı yok; tıklama hiçbir şey yapmaz.
- `broken.html:30` — `<a href="#sil">x</a>`: sayfada `id="sil"` bulunmuyor; tıklama yalnız URL'ye `#sil` ekler, kullanıcıya görünür bir sonuç yok.
- `broken.html:28` — `alert('kaydedildi')` teknik olarak görünür bir sonuçtur, bu yüzden bu satır U1'in birincil kanıtı değildir; ancak `role="status"` mesajı, yönlendirme veya bekleme göstergesi değildir ve mobilde engelleyici bir sistem diyaloğu açar (bkz. A13 ve ek bulgular).
- **Düzeltme:** Kaydet sonrası sayfa içinde `<p role="status">Kayıt alındı.</p>` göster ya da onay sayfasına yönlendir; Sil eylemlerine gerçek işlev + sonuç mesajı ekle.

### U2 — Her akıştan çıkış yolu var mı? — **ihlal :28**
- `broken.html:20-28` — Form alanlarının yanında yalnız "Kaydet" var; İptal / Geri yok. `<form>` öğesi bile yok (`broken.html:20`), dolayısıyla yarım veriyle ayrılmada uyarı mekanizması da yok.
- İlk kez gelen bir veli, yanlış sayfada olduğunu fark ettiğinde tarayıcı geri tuşuna mecbur kalır.
- **Düzeltme:** Kaydet'in yanına `<button type="button">İptal</button>` (nereye döndüğü belli olan bir hedefle); alanlar doluysa `beforeunload` benzeri kibar bir uyarı.

### U3 — Biçimli alanlar doğru tip/ipucu/hata metni taşır mı? — **ihlal :22**
- `broken.html:22` — `<input type="text" placeholder="TC Kimlik No">`: `inputmode="numeric"` yok (mobilde harf klavyesi açılır), `pattern="[0-9]{11}"` / `maxlength="11"` yok, format ipucu ve örnek yok, herhangi bir hata metni yok.
- `broken.html:21` — `type="email"` doğru; ancak format ipucu ve hata metni yine yok.
- Sayfada ne yanlış olduğunu ve nasıl düzeltileceğini söyleyen tek bir hata metni bulunmuyor.
- **Düzeltme:** `inputmode="numeric" pattern="[0-9]{11}" maxlength="11"`; alan altında `aria-describedby` ile bağlı "11 haneli, yalnız rakam. Örnek: 12345678901"; hata: "TC Kimlik No 11 haneli olmalı; siz 9 hane girdiniz."

### U4 — Zorunlu ve hata işareti ayrı mı; yönerge gerçek durumla örtüşüyor mu? — **ihlal :19**
- `broken.html:19` — "Lütfen **tüm** alanları doldurun. Zorunlu alanlar kırmızı ile işaretlidir." — İki cümle birbiriyle çelişir (hepsi zorunluysa neden yalnız biri işaretli?).
- `broken.html:22` — Yalnız TC Kimlik No alanında `border:2px solid red` var; e-posta ve ad soyad işaretsiz. Hiçbir alanda `required` özniteliği yok, yani yönerge gerçek durumla örtüşmez.
- Kırmızı kenarlık form geleneğinde **hata** sinyalidir; burada **zorunlu** anlamında kullanılmış. Kullanıcı henüz hiçbir şey yazmadan "hata var" algılar; gerçek hata geldiğinde ise ayrıştıramaz.
- **Düzeltme:** Zorunlu için etikette `*` + "(zorunlu)" metni ve `required`; hata için `aria-invalid="true"` + ikon + metin. Yönergeyi gerçek duruma göre yaz.

### U5 — Yıkıcı eylem onay ister mi? — **ihlal :29**
- `broken.html:29` — Çöp kutusu butonu: onay, geri alma, hatta işlev yok.
- `broken.html:30` — `href="#sil"` etiketli "x": silme niyeti taşıyan bir bağlantı, onaysız.
- **Düzeltme:** Sil eylemi öncesi `<dialog>` ile "X kaydını silmek istiyor musunuz? — Sil / Vazgeç" ya da 5-10 sn "Geri al" penceresi.

### U6 — Rozet/uyarı bir içeriğe bağlı mı? — **ihlal :31**
- `broken.html:31` — `<div class="pulse">Yeni!</div>`: hangi içeriğin yeni olduğu belirsiz; tabloya, forma ya da linke bağlı değil. Üstelik sürekli titreyerek (bkz. A10) dikkat çekiyor.
- **Düzeltme:** Ya kaldır ya da bağlamlı yap: "Yeni: Matematik notu güncellendi" biçiminde, ilgili öğenin yanında.

### U7 — Etiketler kalıcı mı? — **ihlal :20**
- `broken.html:20`, `:21`, `:22` — Üç `input` da yalnız `placeholder` taşıyor; kullanıcı yazmaya başlayınca etiket kaybolur, hangi alana ne yazdığını doğrulayamaz.
- `broken.html:24` — `<option value="" disabled selected>Sınıf seçin</option>`: devre dışı seçenek etiket yerine kullanılmış; seçim yapılınca "Sınıf" bilgisi ekrandan silinir.
- **Düzeltme:** Her denetim için görünür `<label for="…">`; placeholder yalnız örnek için ("Örn. Ayşe Yılmaz").

### U8 — Link/buton metni hedefi söyler mi? — **ihlal :36**
- `broken.html:36` — `<a href="#detay">buraya tıklayın</a>`: hedef yok, ekran okuyucu link listesinde anlamsız.
- `broken.html:30` — Link metni "x": ne yaptığını söylemez.
- `broken.html:29` — Yalnız emoji "🗑": erişilebilir ad yok (bkz. A8).
- `broken.html:28` — "Kaydet": tek uygun örnek; ancak neyi kaydettiği ("Kaydı gönder") daha açık olabilir.
- **Düzeltme:** "Kayıt detaylarını görüntüle", "Kaydı sil", "Formu temizle" gibi eylem + nesne metinleri.

---

## A — Erişilebilirlik bulguları (WCAG 2.2)

### A1 — Tek `h1`, hiyerarşik başlıklar, `main`, atlama linki — **ihlal :17**
- `broken.html:17` — `<div style="font-size:28px;font-weight:700">Öğrenci Kayıt</div>`: görsel olarak başlık, programatik olarak düz `div`. Sayfada hiç `h1`–`h6` yok.
- `broken.html:16-37` — `main` landmark yok; tüm içerik doğrudan `body` içinde.
- Atlama linki: Bu tam bir sayfa olduğundan "sayfa düzeyinde" kural uygulanır; ancak sayfada tekrarlayan blok (nav, header) bulunmadığı için 2.4.1 açısından atlama linki gerekli değil — bu alt madde ihlale dahil edilmedi.
- **Düzeltme:** `<h1>Öğrenci Kayıt</h1>`, içeriği `<main>` içine al, tablo ve form için `h2`.

### A2 — Görselde anlamlı `alt` / süs görselde `alt=""` — **ihlal :18**
- `broken.html:18` — `<img src="https://picsum.photos/seed/okul/320/120" width="320" height="120">`: `alt` özniteliği tamamen eksik; ekran okuyucu dosya yolunu okur.
- Görselin bilgi mi süs mü olduğu render edilmeden anlaşılamıyor (rastgele placeholder servisi). Her iki durumda da öznitelik zorunlu.
- **Düzeltme:** Okul logosu/bina fotoğrafıysa `alt="Atatürk İlkokulu ana bina"`; süs ise `alt=""`.

### A3 — Metin kontrastı ≥ 4,5:1 (büyük metin/UI ≥ 3:1) — **ihlal :19**
Hesaplanan oranlar (WCAG bağıl parlaklık formülü):

| Satır | Ön plan / Arka plan | Oran | Eşik | Sonuç |
|---|---|---|---|---|
| `:19` | `#9a9a9a` / `#fff` (yönerge metni, normal boy) | **≈ 2,8:1** | 4,5:1 | **İhlal** |
| `:12` / `:31` | `#fff` / `#e53e3e` ("Yeni!" rozeti, 16 px, normal kalınlık) | **≈ 4,1:1** | 4,5:1 | **İhlal** |
| `:10` / `:28` | `#fff` / `#2b6cb0` (Kaydet) | ≈ 5,4:1 | 4,5:1 | Uygun |
| `:22` | `red` kenarlık / `#fff` (UI bileşeni) | ≈ 4,0:1 | 3:1 | Uygun |
| `:8` | `#1a1a1a` / `#fff` (gövde) | ≈ 16,7:1 | 4,5:1 | Uygun |
| `:30` | Tarayıcı varsayılan link rengi / `#fff` | doğrulanamaz (varsayılan mavi ≈ 9:1 geçer; `font-size:10px` ayrıca okunabilirlik sorunu) | — | — |

- En kritik ihlal `:19`: zorunluluk yönergesini taşıyan tek cümle en düşük kontrastlı metin. Mobilde güneş ışığında neredeyse görünmez.
- **Düzeltme:** Yönerge için `#595959` veya daha koyu (≥ 4,5:1); rozet için `#c53030` (≈ 5,5:1) ya da metni kalın + 18,66 px yap.

### A4 — Her form denetimi programatik etikete bağlı — **ihlal :20**
- `broken.html:20`, `:21`, `:22` (`input`) ve `:23` (`select`): Hiçbirinde `id`, `<label for>`, `aria-label` veya `aria-labelledby` yok. Ekran okuyucu yalnız "düzenleme kutusu" / "açılır liste" der; placeholder erişilebilir ad olarak güvenilir değildir ve select'te hiç yoktur.
- **Düzeltme:** `<label for="ad">Ad Soyad</label><input id="ad" …>` — dört denetimin tümü için.

### A5 — Renk tek sinyal değil; link ayırt edici — **ihlal :22**
- `broken.html:22` — Kırmızı kenarlık zorunlu/hata bilgisini yalnız renkle taşır; `aria-invalid`, `aria-describedby`, ikon veya metin yok. Renk körü veya ekran okuyucu kullanan veli bu bilgiyi alamaz.
- `broken.html:19` — "kırmızı ile işaretlidir" yönergesi 1.4.1'in tam tarifi: bilgi yalnız renkle iletilmiş.
- Gövde içindeki linkler (`:30`, `:36`): Altı çizgiyi kaldıran CSS yok, tarayıcı varsayılanı korunur → bu alt madde **uygun**.
- **Düzeltme:** Zorunlu: etikette `*` + "(zorunlu)"; hata: `aria-invalid="true" aria-describedby="tc-hata"` + `<p id="tc-hata">⚠ TC Kimlik No 11 haneli olmalı.</p>`.

### A6 — Odak görünür ve kalır — **ihlal :23**
- `broken.html:23` — `<select style="outline:none">`: odak halkası kaldırılmış, yerine hiçbir eşdeğer gösterge (border/box-shadow değişimi) yok.
- `broken.html:7-14` — Stil bloğunda hiç `:focus` / `:focus-visible` kuralı yok; diğer öğeler tarayıcı varsayılanına kalıyor (kabul edilebilir ama garanti değil).
- `broken.html:28` — `div.fake-btn` zaten odak alamaz (bkz. A7), dolayısıyla odak göstergesi de yok.
- `onfocus=blur` gibi script ile odak düşürme yok → bu alt madde uygun.
- **Düzeltme:** `outline:none` sil; global `:focus-visible { outline: 3px solid #1a1a1a; outline-offset: 2px; }`.

### A7 — Etkileşimli öğe native mi? — **ihlal :28**
- `broken.html:28` — `<div class="fake-btn" onclick="…">Kaydet</div>`: Tab ile ulaşılamaz, Enter/Space çalışmaz, rol "button" değil. Sayfanın **ana eylemi** klavye ve ekran okuyucu kullanıcıları için tamamen erişilemez.
- `broken.html:30` — `<a href="#sil">`: Silme bir **eylem**dir, navigasyon değil; `button` olmalı.
- `broken.html:29` — `<button>` native, uygun (ama isim yok — A8).
- **Düzeltme:** `<button type="submit">Kaydet</button>` (bir `<form>` içinde); `<button type="button">Kaydı sil</button>`.

### A8 — Yalnız ikon/emoji taşıyan denetimde erişilebilir ad — **ihlal :29**
- `broken.html:29` — `<button class="icon-only">🗑</button>`: Ekran okuyucu "çöp kutusu" emojisini okur ya da hiçbir şey demez; eylemin ne olduğu ("Kaydı sil") belirsiz. `aria-label` veya gizli metin yok.
- `broken.html:30` — Metin "x": ikon gibi davranan tek harf, erişilebilir adı "x". Aynı sorun.
- **Düzeltme:** `<button type="button" aria-label="Kaydı sil">🗑</button>` ya da `<span class="visually-hidden">Kaydı sil</span>`.

### A9 — Tıklama hedefi ≥ 24×24 CSS px — **ihlal :30**
- `broken.html:30` — `width:16px;height:16px` açıkça 24×24 altında; `font-size:10px` ile mobilde parmakla vurulması neredeyse imkânsız.
- `broken.html:29` — `.icon-only` 18 px emoji + `border:0` + tarayıcı varsayılan padding: hesaplanan boyut render edilmeden bilinemez, **doğrulanamaz** (tahminen 24 px sınırında; açık `min-width/min-height:44px` önerilir).
- `broken.html:28` — `padding:8px 16px` + 16 px metin ≈ 35 px yükseklik, uygun.
- **Düzeltme:** Tüm dokunma hedeflerine `min-width:44px;min-height:44px` (mobil veli kitlesi için 24 px yasal alt sınır, 44 px iyi uygulama).

### A10 — Otomatik hareket durdurulabilir; flaş yok; reduced-motion — **ihlal :12**
- `broken.html:12-13` — `animation: pulse 1s infinite`: 5 sn'den uzun, kullanıcı tarafından durdurulamayan otomatik hareket (2.2.2 ihlali). `@media (prefers-reduced-motion: reduce)` kuralı yok.
- Flaş değerlendirmesi: `scale(1)→scale(1.15)` boyut değişimidir, parlaklık değişimi değil → 2.3.1 (flaş) **ihlal değil**.
- **Düzeltme:** Animasyonu kaldır ya da 3 döngüyle sınırla (`animation-iteration-count: 3`) + `@media (prefers-reduced-motion: reduce) { .pulse { animation: none } }`.

### A11 — Veri tablosunda `caption` ve `th scope` — **ihlal :32**
- `broken.html:32-35` — 2×2 tablo (ders adı / not): `caption` yok, `th` yok, `scope` yok. Ekran okuyucu "Matematik 85, Türkçe 92" der; bunun **not** olduğu, kimin notu olduğu anlaşılmaz.
- Bu tam olarak kontrol listesinin uyardığı durum: ≤3×3 küçük tablo, otomatik araçlardan (axe) kaçar, elle tespit edildi.
- **Düzeltme:** `<caption>Dönem notları</caption>` + `<tr><th scope="col">Ders</th><th scope="col">Not</th></tr>`; ders adları için `th scope="row"`.

### A12 — `html lang` doğru; dil değişen parçalarda `lang` — **uygun**
- `broken.html:2` — `<html lang="tr">` arayüz diliyle örtüşür.
- Sayfada Türkçe dışı bir metin parçası yok; parça düzeyinde `lang` gerekmiyor.

### A13 — Canlı güncellemeler `aria-live` / `role="status"` ile duyurulur — **uygulanamaz**
- Sayfada odak almayan bir durum mesajı, toast veya satır içi doğrulama bulunmuyor; 4.1.3 tam olarak bu tür (odak almayan) mesajları kapsar.
- Tek geri bildirim `broken.html:28` `alert('kaydedildi')`: native diyalog odak alır ve yardımcı teknoloji tarafından duyurulur — 4.1.3 kapsamı dışında. (UX açısından mobilde engelleyici ve kaba bir kalıp; U1 altında ele alındı.)
- **Uyarı:** U1 düzeltmesiyle sayfa içi durum mesajı eklenirken `role="status"` (veya `aria-live="polite"`) zorunlu; aksi hâlde bu madde ihlale döner.

---

## Kontrol listesi dışı ek bulgular

1. **`<form>` yok** (`broken.html:20-28`): Alanlar bir form içinde değil; Enter ile gönderme, native doğrulama (`required`, `pattern`), `autocomplete` davranışları çalışmaz.
2. **`autocomplete` yok** (`:20`, `:21`): `autocomplete="name"`, `autocomplete="email"` eksik — WCAG 1.3.5 (Girdi Amacını Tanımla, AA). Mobilde tarayıcı otomatik doldurmayı kaçırır.
3. **TC Kimlik No hassas veri** (`:22`): Neden istendiği, nasıl saklandığı hakkında tek satır açıklama yok. İlk kez gelen veli için güven sorunu; KVKK açısından da açıklama beklenir.
4. **Hotlink placeholder görsel** (`:18`): `picsum.photos` rastgele fotoğraf servisi; üretimde her yüklemede farklı görsel gelebilir, dış bağımlılık ve gizlilik (üçüncü taraf istek) sorunu.
5. **`alert()` kullanımı** (`:28`): Mobilde tüm sayfayı kilitler, stillenemez, bazı tarayıcılar art arda gelen alert'leri bastırır. Sayfa içi durum mesajına çevrilmeli.
6. **Sahte silme bağlantısı** (`:30` `href="#sil"`): Hedef `id` yok; tıklama URL'yi değiştirir, geri tuşu davranışını bozar.
7. **Olumlu:** `viewport` meta (`:5`) ve `charset` (`:4`) doğru; `max-width:640px` (`:8`) mobilde sorun çıkarmaz.

---

## Öncelik sırası (veli · mobil · ilk kez)

1. **Ana eylem erişilemez** — `:28` `div` → `button`, `<form>` içine al (A7, U2).
2. **Alanlar isimsiz** — `:20-23` görünür `label` ekle (A4, U7).
3. **TC Kimlik No mobilde harf klavyesi + ipucu yok** — `:22` `inputmode="numeric"`, format metni, hata metni (U3, A5).
4. **Yönerge okunmuyor ve yanlış** — `:19` kontrast 2,8:1 → koyult, "kırmızı" yerine metin işareti (A3, U4).
5. **Silme onaysız ve isimsiz** — `:29`, `:30` (U5, A8, A9).
6. **Yapı** — `h1`, `main`, tablo `caption`/`th` (A1, A11).
7. **Görsel gürültü** — `:12/:31` titreyen "Yeni!" rozetini kaldır ya da bağla (A10, U6, A3).

---

**Kısa özet:**
- 21 kontrolün 19'u ihlal; yalnız `lang` uygun, canlı bölge maddesi uygulanamaz.
- Sayfanın ana eylemi "Kaydet" bir `div`; klavye ve ekran okuyucuyla hiç çalışmıyor.
- Hiçbir form alanının etiketi yok; TC Kimlik No mobilde sayısal klavye açmıyor, ipucu ve hata metni yok.
- Zorunluluk yalnız kırmızı renkle anlatılıyor ve o metin bile 2,8:1 kontrastla okunmuyor.
- Silme eylemleri onaysız, isimsiz ve 16 px boyutunda; "Yeni!" rozeti bağlamsız ve sürekli titriyor.