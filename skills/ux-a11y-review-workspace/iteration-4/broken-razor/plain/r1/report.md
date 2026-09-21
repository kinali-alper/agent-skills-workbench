# UX ve Erişilebilirlik Denetimi — `BrokenForm.cshtml`

**Dosya:** `project/BrokenForm.cshtml` (Razor görünümü, 30 satır)
**Bağlam:** Öğrenci kayıt formu · Arayüz dili Türkçe · Kullanıcı: okul sekreteri, masaüstü, günde ~30 kez
**Yöntem:** Statik kaynak incelemesi. Sayfa render edilemedi; `_Layout.cshtml`, CSS (`.broken`, `.fake-btn`, `.icon-only`, `.pulse`, `.is-invalid`), ViewModel (`OgrenciKayitViewModel`) ve controller (`Kayit`, `Sil`, `Kosullar`) elde yok. Bu yüzden bazı hükümler **doğrulanamaz**; kalanlar dosya satırına bağlanmıştır.
**Hüküm kümesi:** ihlal :N / uygun / uygulanamaz / doğrulanamaz — her satıra tam bir hüküm.

---

## Özet tablo

| Kod | Hüküm | Satır | Kısa gerekçe |
|---|---|---|---|
| U1 | **ihlal** | :19 (ayrıca :18, :21) | Sıfırla, Kaydet ve Sil hiçbir görünür sonuç / `role="status"` üretmez |
| U2 | **ihlal** | :11 | Formda İptal/Geri yok; sıfırlama yarım veriyi uyarısız siler |
| U3 | **ihlal** | :14 (ayrıca :13) | TC Kimlik No'da `inputmode`/format ipucu/örnek yok; hata metni hiç yok |
| U4 | **ihlal** | :9 (ayrıca :14) | "Kırmızı = zorunlu" denir, işaret yok; kırmızı aynı anda hata rengi |
| U5 | **ihlal** | :21 (ayrıca :19) | Sil onaysız tek tık GET linki; sıfırla onaysız |
| U6 | **ihlal** | :22 | "Yeni!" rozeti hiçbir içeriğe bağlı değil |
| U7 | **ihlal** | :12 (12–14) | Etiket yok, placeholder etiket yerine kullanılmış |
| U8 | **ihlal** | :29 (ayrıca :21, :19) | "buraya tıklayın", "x", 🗑 hedefi söylemiyor |
| A1 | **ihlal** | :7 | Başlık `div`; `h1` yok. `main`/atlama linki: layout'ta, doğrulanamaz |
| A2 | **ihlal** | :8 | `img` üzerinde `alt` özniteliği yok |
| A3 | **ihlal** | :9 (ayrıca :21) | `#9a9a9a` beyaz üstünde ≈2,7:1 (< 4,5:1) |
| A4 | **ihlal** | :12 (12–15) | Hiçbir denetimin `label for`/`aria-labelledby` bağı yok |
| A5 | **ihlal** | :14 | Hata yalnız `is-invalid` rengiyle; `aria-invalid`/`aria-describedby`/metin yok |
| A6 | **ihlal** | :15 | `outline:none`, eşdeğer odak göstergesi yok |
| A7 | **ihlal** | :18 | `div` + `onclick` ile gönder düğmesi |
| A8 | **ihlal** | :19 (ayrıca :21) | Yalnız 🗑 emoji, erişilebilir ad yok |
| A9 | **ihlal** | :21 | Sil hedefi 16×16 px (< 24×24) |
| A10 | **doğrulanamaz** | :22 | `.pulse` animasyon ima eder; CSS yok, süre/`prefers-reduced-motion` görülemiyor |
| A11 | **ihlal** | :23 | Tabloda `caption`, `thead`, `th scope` yok |
| A12 | **doğrulanamaz** | — | `html lang` layout'ta; bu dosyada dil değişen parça yok |
| A13 | **ihlal** | :14 (ayrıca :11) | Hata/durum bildirimi için hiçbir `aria-live`/`role="status"` bölgesi yok |

**Sayım:** 19 ihlal · 0 uygun · 0 uygulanamaz · 2 doğrulanamaz.

---

## UX kontrol listesi — ayrıntılı hükümler

### U1 — Her eylem görünür sonuç üretir · **ihlal :19**
- `:19` `onclick="$('form')[0].reset()"` — form sessizce boşalır; mesaj, geri alma, odak yönetimi yok. Sekreter yanlışlıkla tıklarsa girdiği veriyi neden kaybettiğini anlamaz.
- `:18` `$('form').submit()` — gönderim sırasında bekleme göstergesi / devre dışı bırakma yok; çift tıklamada çift kayıt riski. Gönderim sonrası ne olduğu (`Kayit` action'ı) dosyada görülmüyor → o kısım doğrulanamaz.
- `:21` `Sil` linki — sonuç bildirimi yok (bkz. U5).
- Görünümde tek bir `role="status"` / `aria-live` / `asp-validation-summary` yok.

### U2 — Her akıştan çıkış yolu · **ihlal :11**
- `:11–20` form içinde İptal / Geri / Listeye dön yok. Tek "çıkış" `:19` sıfırla düğmesi; o da yarım veriyi uyarısız siler.
- Günde 30 kez kullanılan formda "vazgeç ve listeye dön" en sık ikinci eylemdir; eksik olması her seferinde tarayıcı geri tuşuna zorlar.

### U3 — Biçimli alanlar · **ihlal :14**
- `:14` `TcKimlikNo`: `inputmode="numeric"`, `maxlength="11"`, `pattern`, `autocomplete="off"` yok; "11 hane, örn. 12345678901" gibi format ipucu/örnek yok. Sadece `placeholder="TC Kimlik No"`.
- `:13` `Eposta`: `type="email"`/`autocomplete="email"` açıkça verilmemiş. (`asp-for`, ViewModel'de `[EmailAddress]`/`[DataType]` varsa `type="email"` üretebilir — ViewModel yok, bu kısım doğrulanamaz.)
- Hiçbir alanda `<span asp-validation-for>` yok → sunucu doğrulaması dönse bile **ne** yanlış ve **nasıl** düzelir metni gösterilecek yer yok. `:14`'teki `is-invalid` bir hata var der ama nedenini söylemez.

### U4 — Zorunlu ve hata işareti ayrı sinyaller · **ihlal :9**
- `:9` "Zorunlu alanlar kırmızı ile işaretlidir" — ama `:12–17` hiçbir alanda zorunlu işareti (`*`, "(zorunlu)", `required`, `aria-required`) yok. Yönerge gerçek durumla örtüşmüyor.
- Aynı cümle "Lütfen tüm alanları doldurun" der → hepsi zorunluysa "zorunlu alanlar" ayrımı anlamsız; iki cümle çelişir.
- `:14` `is-invalid` (Bootstrap'te kırmızı kenarlık) — kırmızı hem "zorunlu" hem "hatalı" anlamına gelecek; iki sinyal tek renkte birleşmiş.

### U5 — Yıkıcı eylem onay ister · **ihlal :21**
- `:21` `<a asp-action="Sil" asp-route-id="@Model.Id">x</a>` — kaydı silen eylem tek tıklık bir GET linki; onay diyaloğu, geri alma penceresi, hatta ne silineceğini söyleyen metin yok. Sil linki ayrıca kayıt formunun hemen yanında (`:20` kapanışından sonra) 16 px'lik bir "x" — yanlış tıklama olasılığı yüksek.
- `:19` `reset()` — tüm girdileri onaysız siler.
- Not (güvenlik/UX kesişimi): durum değiştiren `Sil`'in GET olması tarayıcı ön-yükleme ve CSRF açısından da sorunlu; `form method="post"` + anti-forgery ile yapılmalı.

### U6 — Rozet bağlama bağlı · **ihlal :22**
- `:22` `<span class="pulse">Yeni!</span>` — neyin yeni olduğu yok; hemen sonrasında not tablosu, öncesinde sil linki var. Bağlamsız, muhtemelen animasyonlu dikkat çekici (bkz. A10).

### U7 — Etiketler kalıcı · **ihlal :12**
- `:12`, `:13`, `:14` — yalnız `placeholder`; yazmaya başlanınca "hangi alandaydım" bilgisi kaybolur. Günde 30 kez doldurulan formda otomatik doldurma/yapıştırma sonrası alan adları görünmez olur.
- `:15–16` `select` için de görünür etiket yok; `disabled selected` "Sınıf seçin" seçeneği placeholder görevi görüyor.

### U8 — Link/buton metni hedefi söyler · **ihlal :29**
- `:29` `buraya tıklayın` → hedef "Kayıt koşulları". Bağlamdan koparılmış link listesinde (ekran okuyucu) anlamsız.
- `:21` `x` → "Kaydı sil" olması gerekir.
- `:19` `🗑` → "Formu temizle" (emoji çöp kutusu; sekreter "kaydı sil" sanabilir, U5 ile birleşince tehlikeli).

---

## Erişilebilirlik kontrol listesi — ayrıntılı hükümler

### A1 — Tek h1, hiyerarşi, main, atlama linki · **ihlal :7**
- `:7` `<div style="font-size:28px;font-weight:700">@ViewData["Title"]</div>` — görsel olarak başlık, programatik olarak değil. Görünümde hiç başlık öğesi yok (`h1` yok → hiyerarşi kurulamıyor).
- `main` landmark ve sayfa düzeyinde atlama linki `_Layout.cshtml`'de olur; dosyada yok → **bu alt madde doğrulanamaz**. Genel hüküm `h1` eksikliğinden dolayı ihlal.

### A2 — Görselde alt · **ihlal :8**
- `:8` `<img src="~/img/okul.jpg" width="320" height="120" asp-append-version="true" />` — `alt` özniteliği tamamen eksik. Ekran okuyucu dosya adını ("okul.jpg") okur. Logo/süs ise `alt=""`, bilgi taşıyorsa anlamlı metin gerekir.

### A3 — Kontrast · **ihlal :9**
- `:9` `style="color:#9a9a9a"` — sayfa arka planı CSS'te görülmüyor; standart beyaz (#fff) varsayımıyla kontrast ≈ **2,74:1**, gövde metni için 4,5:1 eşiğinin çok altında. Yalnızca çok koyu bir arka planda geçer, o da diğer varsayılan metni bozar. Üstelik bu cümle formun tek yönergesi (bkz. U4).
- `:21` `font-size:10px` "x" — rengi bilinmiyor (doğrulanamaz), ancak 10 px metin zaten okunabilirlik sınırının altında.
- `.is-invalid`, `.text-muted`, `.fake-btn` renkleri CSS'te → doğrulanamaz.

### A4 — Programatik etiket · **ihlal :12**
- `:12`, `:13`, `:14` `input` ve `:15` `select`: hiçbirinde `<label asp-for>`/`for`, `aria-label` ya da `aria-labelledby` yok. `asp-for` id/name üretir ama etiket bağı üretmez. Tarayıcıların placeholder'ı erişilebilir ad olarak kullanması bir yedek davranış, uyumluluk sayılmaz; `:15` select'in ise hiç adı yok ("Sınıf seçin" seçenek metni ad değildir).

### A5 — Renk tek sinyal değil · **ihlal :14**
- `:14` `class="... is-invalid"` — hata yalnızca kırmızı kenarlıkla; `aria-invalid="true"`, `aria-describedby` ile bağlı hata metni, ikon yok. `<span asp-validation-for="TcKimlikNo">` hiç yok.
- `:29` gövde metni içindeki link: altı çizili mi bilinmiyor (CSS yok) → alt madde doğrulanamaz; ana hüküm `:14`'ten ihlal.

### A6 — Odak görünür ve kalır · **ihlal :15**
- `:15` `style="outline:none"` — select üzerinde tarayıcı odak halkası kaldırılmış, dosyada `:focus-visible` eşdeğeri yok. Klavye ile formu dolduran sekreter hangi alanda olduğunu göremez.
- `:18` `div.fake-btn` odaklanamaz zaten (`tabindex` yok) → odak sırasından tümüyle düşer (A7 ile örtüşür).
- `onfocus=blur` benzeri odak düşürücü script yok (bu alt madde uygun).

### A7 — Etkileşimli öğe native · **ihlal :18**
- `:18` `<div class="fake-btn" onclick="$('form').submit()">Kaydet</div>` — `button` rolü yok, klavyeden erişilemez (tabindex yok), Enter/Space çalışmaz. Formda hiç `type="submit"` yok (tek buton `:19` `type="button"`), dolayısıyla alan içinde Enter da formu göndermeyebilir. Ayrıca `$('form').submit()` sayfadaki **tüm** formları gönderir ve jQuery unobtrusive validation'ı atlar.
- `:19` `button` native (uygun), `:21`/`:29` `a href` native (uygun).

### A8 — Yalnız ikon denetimde erişilebilir ad · **ihlal :19**
- `:19` `<button ... class="icon-only">🗑</button>` — `aria-label`/gizli metin yok; ekran okuyucu "çöp kutusu" gibi emoji adını okur, bunun "formu temizle" olduğu anlaşılmaz.
- `:21` `x` — tek harf, erişilebilir ad olarak anlamsız ("x" okunur).

### A9 — Tıklama hedefi ≥ 24×24 · **ihlal :21**
- `:21` `width:16px;height:16px` — 16×16 px, eşiğin altında; üstelik yıkıcı bir eylem (U5). Inline metin linki istisnası uygulanmaz (bloklaştırılmış, bağımsız hedef).
- `:19` `.icon-only` boyutu CSS'te → doğrulanamaz.

### A10 — Hareket durdurulabilir, flaş yok, reduced-motion · **doğrulanamaz**
- `:22` `class="pulse"` sürekli animasyon ima eder; ancak `@keyframes`, süre, tekrar ve `prefers-reduced-motion` sorgusu CSS'te, dosyada yok. Sınıf sonsuz döngü (`infinite`) tanımlıyorsa A10 ihlal olur; kesin hüküm CSS görülmeden verilemez. Denetim önerisi: CSS'te `.pulse` bloğunu kontrol et.

### A11 — Veri tablosunda caption ve th scope · **ihlal :23**
- `:23–28` `<table class="table">` — `caption` yok, `thead`/`th` yok; hücreler sadece `td`. Ders/Puan sütunlarının adı hiç yok (görsel olarak da). Tablo 2 sütun × N satır; N ≤ 3 ise axe'ten kaçar — **elle kontrol edildi, ihlal**.

### A12 — html lang · **doğrulanamaz**
- `<html lang>` `_Layout.cshtml`'de; bu dosyada yok. Görünüm içindeki tüm metin Türkçe; dil değişen parça (ör. İngilizce terim) yok → `lang` alt maddesi bu dosya için gerekmiyor.

### A13 — Canlı güncellemeler duyurulur · **ihlal :14**
- `:14` hata durumu (`is-invalid`) var ama onu duyuracak `aria-live`/`role="status"`/`role="alert"` bölgesi ya da `asp-validation-summary` görünümün hiçbir yerinde yok.
- `:11` form: `:18` gönder ve `:19` sıfırla sonrası oluşacak durum değişikliklerini bildirecek canlı bölge yok. Layout'ta jQuery unobtrusive validation yüklü olsa bile `asp-validation-for` kapsayıcıları olmadığı için istemci hataları da bir yere yazılamaz.

---

## Kontrol listesi dışı ama önemli gözlemler

1. `:18` `$('form').submit()` ve `:19` `$('form')[0].reset()` — jQuery'ye bağımlı inline script; CSP altında çalışmaz; sayfada ikinci bir form (ör. layout'taki çıkış formu) varsa `$('form').submit()` onu da gönderir.
2. `:21` Kayıt formunun yanında kaydı silen link: kayıt (oluşturma) ekranıyla silme eyleminin aynı görünümde olması bilgi mimarisi açısından şüpheli; `@Model.Id` yeni kayıtta 0/null olabilir.
3. `:7`, `:9`, `:15`, `:21` inline `style` — tema/yüksek kontrast modlarında geçersiz kılınamaz.
4. `:16` `disabled selected` placeholder seçeneği: kabul edilebilir, ancak `select`'e `required` de eklenmeli.
5. Formda `@Html.AntiForgeryToken()` görünmüyor; Form Tag Helper (`asp-action`) otomatik ekler, muhtemelen uygun — not olarak.

---

## Öncelik sırası (sekreterin günlük işine etkisi)

1. **A7/U1 `:18`** — Kaydet düğmesini `<button type="submit">` yap; klavye kullanıcısı için form şu an gönderilemez.
2. **A4/U7 `:12–15`** — Her alana görünür `<label asp-for>` ekle; placeholder'ı ipucuya indir.
3. **U5/A9/A8 `:21`** — Sil'i POST form + onay diyaloğu + "Kaydı sil" metni + ≥24 px hedefe çevir; `:19` sıfırlaya onay ve `aria-label="Formu temizle"`.
4. **U3/A5/A13 `:14`** — TC Kimlik No'ya `inputmode="numeric" maxlength="11"` + format ipucu; her alana `asp-validation-for` + `aria-describedby`; `asp-validation-summary` (`role="alert"`).
5. **U4/A3 `:9`** — Yönergeyi "Tüm alanlar zorunludur" olarak sadeleştir, rengi ≥4,5:1 yap, zorunlu işaretini metinle (`*` + açıklama) ver.
6. **A1 `:7`**, **A2 `:8`**, **A6 `:15`**, **A11 `:23`**, **U6/A10 `:22`**, **U8 `:29`**, **U2 `:11`** — h1, alt, odak halkası, caption/th, bağlamlı rozet, anlamlı link metni, İptal linki.

---

## Doğrulanamayan ve ek dosya isteyen noktalar

- `_Layout.cshtml`: `html lang`, `main`, atlama linki, jQuery/validation script'leri.
- CSS: `.broken`, `.fake-btn`, `.icon-only` (boyut/kontrast), `.pulse` (animasyon/reduced-motion), `.is-invalid`, link altı çizgisi, sayfa arka plan rengi.
- `OgrenciKayitViewModel`: `[Required]`, `[EmailAddress]`, `[Display]` öznitelikleri (asp-for'un ürettiği `type`/`required`/`data-val-*`).
- Controller `Kayit`/`Sil`: gönderim sonrası yönlendirme ve TempData mesajı var mı.

---

**Kısa özet:**
- 21 kontrolün 19'u ihlal, 2'si dosyadan doğrulanamıyor (animasyon CSS'i ve `html lang`); hiçbir satır temiz çıkmadı.
- En ağır sorunlar: Kaydet düğmesi gerçek buton değil (klavyeyle gönderilemez), alanların etiketi yok, Sil linki onaysız ve 16 px.
- Hata/zorunlu bilgisi yalnız renkle veriliyor, hata metni hiç yok; TC Kimlik No alanı biçim ipucu taşımıyor.
- Layout ve CSS dosyaları verilirse doğrulanamayan 2 madde ve birkaç alt madde kesinleşir.