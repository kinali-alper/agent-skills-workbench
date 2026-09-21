# UX ve Erişilebilirlik Denetimi — BrokenForm.cshtml

**Denetlenen dosya:** `project/BrokenForm.cshtml` (Razor görünümü, ASP.NET Core)
**Bağlam:** Arayüz dili Türkçe; kullanıcılar okul sekreterleri; masaüstü; günde ~30 kez kullanılan form.
**Yöntem:** Yalnız kaynak dosya incelendi (statik okuma). Sayfa render edilmedi; CSS, layout (`_Layout.cshtml`), ViewModel ve JavaScript dosyaları mevcut değil. Bu nedenle bazı bulgular "doğrulanamadı" notuyla verilmiştir.
**Ölçüt:** WCAG 2.2 AA + form UX pratikleri (klavye, hata bildirimi, tekrarlı kullanım verimliliği).

**Önem derecesi:** Kritik (görevi engelliyor / veri kaybı) · Yüksek (WCAG A/AA ihlali, ciddi kullanım sorunu) · Orta (WCAG AA / belirgin UX sorunu) · Düşük (iyileştirme).

---

## Özet tablo

| # | Satır | Önem | Konu |
|---|-------|------|------|
| 1 | 18 | Kritik | "Kaydet" bir `div`; klavyeyle çalışmıyor, Enter ile gönderim yok |
| 2 | 21 | Kritik | Silme işlemi GET link; 16×16 px hedef; "x" metni; onay yok |
| 3 | 12–14 | Yüksek | Alanların `<label>`'ı yok; yalnız placeholder; hata mesajı alanı yok |
| 4 | 14 | Yüksek | `is-invalid` sınıfı sabit kodlanmış; alan her zaman kırmızı, mesaj yok |
| 5 | 11 | Yüksek | Doğrulama özeti yok; `Id` gizli alanı eksik olabilir |
| 6 | 15 | Yüksek | `outline:none` odak göstergesini kaldırıyor; etiket yok |
| 7 | 19 | Yüksek | Emoji-only sıfırlama düğmesi; erişilebilir adı yok; onaysız veri silme; birincil düğmenin yanında |
| 8 | 9 | Orta | Kontrast ≈ 2,8:1; "kırmızı ile işaretlidir" yalnız renge dayanıyor ve gerçekte işaret yok |
| 9 | 7 | Orta | Başlık `div`; semantik `<h1>` yok |
| 10 | 8 | Orta | `<img>` `alt` özniteliği yok |
| 11 | 22 | Orta | `.pulse` "Yeni!" — muhtemelen sürekli animasyon, bağlamsız |
| 12 | 23–28 | Orta | Tabloda başlık satırı, `caption`, boş durum yok |
| 13 | 29 | Orta | "buraya tıklayın" bağlam dışı link metni |
| 14 | 12–14 | Düşük | `autocomplete`, `inputmode`, `autofocus` eksik (tekrarlı kullanım verimliliği) |

---

## Bulgular

### 1. Kritik — `BrokenForm.cshtml:18` — Gönder düğmesi bir `div`, klavye ile kullanılamıyor

```razor
<div class="fake-btn" onclick="$('form').submit()">Kaydet</div>
```

**Sorun**
- `div` odaklanabilir değil (Tab ile ulaşılamaz), `role="button"` yok, Enter/Space ile tetiklenmez. Yalnız fareyle çalışır. (WCAG 2.1.1 Klavye, 4.1.2 Ad/Rol/Değer)
- Ekran okuyucu bunu düğme olarak duyurmaz; "Kaydet" salt metin gibi görünür.
- Formda gerçek bir submit düğmesi olmadığı ve birden fazla metin alanı bulunduğu için, HTML'in örtük gönderim kuralı gereği **bir alandayken Enter'a basmak formu göndermez**. Günde 30 kez veri giren bir sekreter için bu, her kayıtta fareye uzanma zorunluluğu demektir — en büyük verimlilik kaybı.
- jQuery'ye (`$`) bağımlı; jQuery yüklenmemişse "Kaydet" hiç çalışmaz. `$('form')` sayfadaki tüm formları seçer; layout'ta başka form (örn. çıkış formu) varsa yanlış form gönderilebilir.
- İstemci tarafı doğrulama (`jquery.validate.unobtrusive`) programatik `submit()` çağrısıyla atlanabilir.

**Düzeltme**
```razor
<button type="submit" class="btn btn-primary">Kaydet</button>
```
Bu tek değişiklik Tab odaklanmayı, Enter/Space ile tetiklemeyi, alanlardan Enter ile gönderimi ve doğrulamanın çalışmasını aynı anda sağlar. `.fake-btn` CSS'i `.btn` üzerine taşınabilir.

---

### 2. Kritik — `BrokenForm.cshtml:21` — Silme işlemi GET link, 16×16 px, "x" metni, onay yok

```razor
<a asp-action="Sil" asp-route-id="@Model.Id" style="display:inline-block;width:16px;height:16px;font-size:10px;line-height:16px">x</a>
```

**Sorun**
- **Yıkıcı işlem GET ile yapılıyor.** Tarayıcı ön-yükleme (prefetch), link tarayıcı botlar veya yanlışlıkla tıklama kaydı geri dönüşsüz silebilir. CSRF'e de açıktır (antiforgery token yok).
- Onay adımı yok. Kayıt formunun hemen altında, 16 px'lik bir "x". Günde 30 kez bu sayfayı kullanan biri için yanlış tıklama olasılığı yüksek.
- Hedef boyutu 16×16 px; WCAG 2.5.8 (min 24×24) ihlali; fare kullanıcıları için de zor.
- Link metni "x": ekran okuyucu "x, link" der; ne silineceği belli değil (2.4.4 Link Amacı). 10 px yazı tipi okunaksız.
- Görsel olarak "kapat" (×) ile karışır — kullanıcı pencereyi kapatmak isterken öğrenciyi siler.

**Düzeltme**
```razor
<form asp-action="Sil" asp-route-id="@Model.Id" method="post" class="d-inline"
      onsubmit="return confirm('@Model.AdSoyad adlı öğrenci kaydı silinecek. Emin misiniz?');">
    <button type="submit" class="btn btn-outline-danger">Öğrenciyi sil</button>
</form>
```
- POST + antiforgery (form tag helper otomatik ekler), açık metin, onay adımı, ≥ 24 px (tercihen ≥ 44 px) hedef.
- Birincil işlem (Kaydet) ile görsel olarak ayrılmış bir konuma (sayfa altı, "Tehlikeli işlemler" bölümü) taşıyın.
- Daha iyisi: `confirm()` yerine erişilebilir bir modal/`<dialog>`, ya da silmeyi ayrı bir onay sayfasına alın. (Örnekteki `@Model.AdSoyad` JS dizesine gömülü; adı `data-ad` özniteliğine koyup JS'te okumak tırnak sorununu önler.)

---

### 3. Yüksek — `BrokenForm.cshtml:12–14` — Alanların etiketi yok; yalnız placeholder; hata mesajı alanı yok

```razor
<input asp-for="AdSoyad" placeholder="Ad Soyad" class="form-control" />
<input asp-for="Eposta" placeholder="E-posta" class="form-control" />
<input asp-for="TcKimlikNo" placeholder="TC Kimlik No" class="form-control is-invalid" />
```

**Sorun**
- Hiçbir alanda `<label>` yok. Placeholder etiketin yerini tutmaz: kullanıcı yazmaya başlayınca kaybolur, kontrastı düşüktür, tarayıcı otomatik doldurmasında görünmez, bazı ekran okuyucular okumaz. (WCAG 1.3.1, 3.3.2 Etiket veya Talimat, 4.1.2)
- Üç alan doldurulduktan sonra sekreter hangi kutuya ne yazdığını göremez; "E-posta" ile "TC Kimlik No" alanları yer değiştirmiş olsa fark edilmez.
- Hiçbir alanın yanında `<span asp-validation-for="...">` yok. Sunucu tarafı doğrulama hatası döndüğünde kullanıcı **hangi alanın neden reddedildiğini göremez**. (WCAG 3.3.1 Hata Tanımlama, 3.3.3 Hata Önerisi)
- Zorunlu alan işareti yok (bkz. Bulgu 8).

**Düzeltme** (her alan için aynı yapı)
```razor
<div class="mb-3">
    <label asp-for="AdSoyad" class="form-label">Ad Soyad <span aria-hidden="true">*</span></label>
    <input asp-for="AdSoyad" class="form-control" autocomplete="name" required aria-required="true" autofocus />
    <span asp-validation-for="AdSoyad" class="invalid-feedback d-block" role="alert"></span>
</div>
```
- `<label asp-for>` otomatik `for`/`id` eşleşmesi üretir; ViewModel'de `[Display(Name="Ad Soyad")]` varsa metin oradan gelir.
- Placeholder'ı kaldırın ya da yalnız örnek biçim için kullanın (`placeholder="ornek@ornek.com"`).
- Sayfa altına `@section Scripts { <partial name="_ValidationScriptsPartial" /> }` ekleyin ki hatalar gönderimden önce gösterilsin.

---

### 4. Yüksek — `BrokenForm.cshtml:14` — `is-invalid` sınıfı sabit kodlanmış

**Sorun**
- `class="form-control is-invalid"` her render'da alanı kırmızı çerçeveli gösterir; kullanıcı henüz hiçbir şey yazmamışken "hata var" sinyali alır ama neyin yanlış olduğu söylenmez. Yanlış hata sinyali güveni zedeler; gerçek hata çıktığında ayırt edilemez.
- Yalnız renk değişimi (kırmızı çerçeve) hata bilgisini taşıyor; metin yok. (WCAG 1.4.1 Renk Kullanımı, 3.3.1)

**Düzeltme**
- `is-invalid` sınıfını kaldırın. ASP.NET Core doğrulama alt yapısı `input-validation-error` sınıfını otomatik ekler; Bootstrap ile eşlemek için `site.css`'e `.input-validation-error` için `.is-invalid` ile aynı kural ya da küçük bir JS köprüsü yeterlidir.
- Hata metni için `<span asp-validation-for="TcKimlikNo">` ekleyin.
- TC Kimlik No için: `inputmode="numeric" maxlength="11" pattern="[0-9]{11}" autocomplete="off"` ve ViewModel'de biçim doğrulaması; hata mesajı "TC Kimlik No 11 haneli olmalıdır" gibi somut olsun.

---

### 5. Yüksek — `BrokenForm.cshtml:11` — Doğrulama özeti yok; `Id` gizli alanı eksik olabilir

```razor
<form asp-action="Kayit" method="post">
```

**Sorun**
- `<div asp-validation-summary="ModelOnly">` yok. Alana bağlı olmayan sunucu hataları (örn. "Bu TC Kimlik No ile kayıt zaten var", veritabanı hatası) kullanıcıya **hiç gösterilmez**; sayfa sessizce geri gelir. Sekreter kaydı yaptığını sanır. (WCAG 3.3.1)
- Satır 21'de `Model.Id` kullanılıyor ve satır 24'te mevcut notlar listeleniyor; yani sayfa mevcut bir öğrenciyi düzenliyor gibi görünüyor. Ancak formda `<input type="hidden" asp-for="Id" />` yok — POST'ta `Id` gitmez, sunucu güncelleme yerine yeni kayıt açabilir ya da hata verebilir. *(Controller görülemediği için "olası" işlevsel risk olarak not edildi.)*
- Başarılı gönderim sonrası durum mesajı (TempData / "Kayıt başarıyla kaydedildi") için bir yer yok. (WCAG 4.1.3 Durum Mesajları)

**Düzeltme**
```razor
<form asp-action="Kayit" method="post" novalidate>
    <input type="hidden" asp-for="Id" />
    <div asp-validation-summary="ModelOnly" class="alert alert-danger" role="alert"></div>
    @if (TempData["Mesaj"] is string mesaj)
    {
        <div class="alert alert-success" role="status">@mesaj</div>
    }
    ...
```
- `novalidate` tarayıcının yerel balonunu kapatır; hatalar tutarlı biçimde ASP.NET Core doğrulamasıyla gösterilir (isteğe bağlı).

---

### 6. Yüksek — `BrokenForm.cshtml:15–17` — `outline:none`, etiket yok

```razor
<select asp-for="SinifId" asp-items="Model.Siniflar" class="form-select" style="outline:none">
    <option value="" disabled selected>Sınıf seçin</option>
</select>
```

**Sorun**
- `style="outline:none"` klavye odak göstergesini kaldırır. Tab ile gelen kullanıcı hangi alanda olduğunu göremez. (WCAG 2.4.7 Odak Görünür)
- `<label>` yok (Bulgu 3 ile aynı).
- `disabled selected` yer tutucu seçenek kabul edilebilir bir desen; ancak `required` olmadan kullanıcı hiçbir şey seçmeden gönderebilir ve sunucu "0" ya da null alır.
- `Model.Siniflar` null gelirse çalışma zamanı hatası verir (null güvenliği controller'da sağlanmalı).

**Düzeltme**
```razor
<div class="mb-3">
    <label asp-for="SinifId" class="form-label">Sınıf <span aria-hidden="true">*</span></label>
    <select asp-for="SinifId" asp-items="Model.Siniflar" class="form-select" required aria-required="true">
        <option value="">Sınıf seçin</option>
    </select>
    <span asp-validation-for="SinifId" class="invalid-feedback d-block"></span>
</div>
```
- `outline:none` kaldırın; özel odak stili isteniyorsa `:focus-visible { outline: 2px solid ...; outline-offset: 2px }` ile **değiştirin**, silmeyin.

---

### 7. Yüksek — `BrokenForm.cshtml:19` — Emoji-only sıfırlama düğmesi; ad yok; onaysız veri silme

```razor
<button type="button" class="icon-only" onclick="$('form')[0].reset()">🗑</button>
```

**Sorun**
- Erişilebilir adı yok; ekran okuyucu "çöp kutusu, düğme" ya da yalnız "düğme" der. Ne yaptığı anlaşılmaz. (WCAG 4.1.2)
- İşlev "formu temizle" ama simge "sil/çöp": kullanıcı öğrencinin silineceğini düşünebilir (satır 21'deki gerçek silme ile karışır).
- **Kaydet'in hemen yanında**, onaysız, geri alınamaz: doldurulmuş üç alan + sınıf seçimi tek yanlış tıklamayla gider. Günde 30 kullanımda bu kaçınılmaz olarak yaşanır.
- `$('form')[0]` sayfadaki **ilk** formu sıfırlar; layout'ta başka bir form varsa yanlış formu hedefler. jQuery bağımlılığı.
- `.icon-only` CSS görülemedi; hedef boyutu 24×24 px'in altında olabilir (2.5.8).

**Düzeltme**
- En iyisi: düğmeyi **kaldırın**. Kısa bir formda "temizle" değer katmaz; kullanıcı alanları elle düzeltir.
- Kalacaksa:
```razor
<button type="reset" class="btn btn-link ms-3" aria-label="Form alanlarını temizle"
        onclick="return confirm('Girdiğiniz bilgiler silinecek. Devam edilsin mi?');">
    <span aria-hidden="true">🗑</span> Temizle
</button>
```
`type="reset"` jQuery'siz çalışır ve yalnız kendi formunu sıfırlar. Kaydet'ten uzağa (satırın karşı ucuna) koyun, ikincil görünüm verin.

---

### 8. Orta — `BrokenForm.cshtml:9` — Kontrast yetersiz; zorunlu alan bilgisi yalnız renkle ve gerçekte işaret yok

```razor
<p class="text-muted" style="color:#9a9a9a">Lütfen tüm alanları doldurun. Zorunlu alanlar kırmızı ile işaretlidir.</p>
```

**Sorun**
- `#9a9a9a` beyaz üzerinde ≈ **2,8:1**; WCAG 1.4.3 için normal metinde 4,5:1 gerekir. Inline stil, temanın `text-muted` değerini de ezer (koyu tema, kurumsal renk değişikliği uygulanmaz).
- "Zorunlu alanlar kırmızı ile işaretlidir": bilgi yalnız renkle veriliyor (1.4.1). Renk körlüğü olan kullanıcı ayırt edemez.
- Daha kötüsü: formda **hiçbir alanda zorunluluk işareti yok** (asterisk, `required`, `aria-required` hiçbiri). Cümle gerçekle uyuşmuyor; tek kırmızı öğe satır 14'teki sabit `is-invalid` hatası. Kullanıcı yanlış yönlendirilir.
- "Lütfen tüm alanları doldurun" ile "zorunlu alanlar işaretlidir" birbirine ters: ya hepsi zorunlu, ya bazıları.

**Düzeltme**
- Inline rengi kaldırın; `text-secondary` ya da en az `#6c757d` (≈ 4,7:1) kullanın.
- Metni gerçeğe uydurun: `<p id="form-aciklama">Yıldız (*) ile işaretli alanlar zorunludur.</p>` ve form'a `aria-describedby="form-aciklama"`.
- Her zorunlu alanın etiketine `*` (ve/veya "(zorunlu)") ekleyin; `required aria-required="true"` kullanın.

---

### 9. Orta — `BrokenForm.cshtml:7` — Sayfa başlığı semantik değil

```razor
<div style="font-size:28px;font-weight:700">@ViewData["Title"]</div>
```

**Sorun**
- Görsel olarak başlık, yapısal olarak düz `div`. Ekran okuyucu kullanıcıları başlıklar arasında gezinemez (H tuşu); sayfanın ana başlığı yok. (WCAG 1.3.1, 2.4.6)
- Inline `px` boyut, tema/tipografi ölçeğinden kopuk.

**Düzeltme**
```razor
<h1 class="h3">@ViewData["Title"]</h1>
```
(Layout'ta zaten bir `<h1>` varsa `<h2>` kullanın; sayfa başına tek `<h1>`.)

---

### 10. Orta — `BrokenForm.cshtml:8` — Görselde `alt` yok

```razor
<img src="~/img/okul.jpg" width="320" height="120" asp-append-version="true" />
```

**Sorun**
- `alt` özniteliği hiç yok; ekran okuyucu dosya adını ("okul.jpg") okur. (WCAG 1.1.1)
- `width`/`height` verilmiş olması iyidir (yerleşim kayması önlenir).

**Düzeltme**
- Dekoratif ise: `alt=""` (okuyucu atlar).
- Bilgi taşıyorsa (okul logosu/adı): `alt="… İlkokulu logosu"` gibi kısa, anlamlı metin.
- Formun üstünde 320×120 px görsel her açılışta alanları aşağı iter; günde 30 kez kullanılan bir formda görseli küçültmek ya da kenara almak alanların ekranın üst kısmında kalmasını sağlar.

---

### 11. Orta — `BrokenForm.cshtml:22` — "Yeni!" rozeti: sürekli animasyon, bağlamsız

```razor
<span class="pulse">Yeni!</span>
```

**Sorun**
- `.pulse` adı sürekli (infinite) bir CSS animasyonunu düşündürür. *(CSS görülemedi; doğrulanamadı.)* Sürekli hareket dikkat dağıtır, bazı kullanıcılarda rahatsızlık yaratır; 5 saniyeden uzun otomatik hareket durdurulabilir olmalı (WCAG 2.2.2) ve `prefers-reduced-motion` saygı görmeli (2.3.3).
- Rozet hangi öğenin "yeni" olduğunu söylemiyor; silme linkinin hemen yanında duruyor ve dikkati yıkıcı işleme çekiyor.
- Günde 30 kez gören biri için "Yeni!" birinci günden sonra gürültüdür; kalıcı "yeni" etiketi anlamını yitirir.

**Düzeltme**
- Kaldırın ya da neyin yeni olduğunu söyleyen, belirli bir öğeye bağlı bir rozet yapın: `<span class="badge bg-info">Yeni özellik: toplu not girişi</span>`.
- Kalacaksa CSS'e:
```css
@media (prefers-reduced-motion: reduce) { .pulse { animation: none; } }
```
ve animasyonu sınırlı sayıda (örn. `animation-iteration-count: 3`) çalıştırın.

---

### 12. Orta — `BrokenForm.cshtml:23–28` — Tablo başlıksız, `caption` yok, boş durum yok

```razor
<table class="table">
    @foreach (var not in Model.Notlar)
    {
        <tr><td>@not.Ders</td><td>@not.Puan</td></tr>
    }
</table>
```

**Sorun**
- `<thead>`/`<th scope="col">` yok: ekran okuyucu hücreleri sütun adıyla ilişkilendiremez; gören kullanıcı da "85" değerinin puan mı, yüzde mi olduğunu bilmez. (WCAG 1.3.1)
- `<caption>` yok; tablonun ne listelediği (öğrencinin notları) belirtilmiyor. Tabloyla formun ilişkisi de açıklanmıyor.
- `Model.Notlar` boşsa boş bir `<table>` render edilir — kullanıcı "not yok mu, yüklenmedi mi?" ayırt edemez. `Model.Notlar` null ise çalışma zamanı hatası.
- Sayısal sütun (Puan) sola dayalı olur; sayılar sağa dayalı okunur.

**Düzeltme**
```razor
@if (Model.Notlar?.Any() == true)
{
    <table class="table">
        <caption>Öğrencinin ders notları</caption>
        <thead>
            <tr><th scope="col">Ders</th><th scope="col" class="text-end">Puan</th></tr>
        </thead>
        <tbody>
        @foreach (var not in Model.Notlar)
        {
            <tr><td>@not.Ders</td><td class="text-end">@not.Puan</td></tr>
        }
        </tbody>
    </table>
}
else
{
    <p class="text-secondary">Bu öğrenciye ait not kaydı bulunmuyor.</p>
}
```

---

### 13. Orta — `BrokenForm.cshtml:29` — "buraya tıklayın" bağlam dışı link metni

```razor
<a asp-action="Kosullar">buraya tıklayın</a>
```

**Sorun**
- Link metni tek başına anlam taşımıyor; ekran okuyucu link listesinde "buraya tıklayın" olarak çıkar. (WCAG 2.4.4)
- Link, çevresinde açıklayıcı cümle olmadan tek başına duruyor; gören kullanıcı da nereye gideceğini bilmez.
- "Tıklayın" klavye kullanıcıları için yanlış eylem fiili.

**Düzeltme**
```razor
<a asp-action="Kosullar">Kayıt koşullarını okuyun</a>
```
Kayıt formuyla ilgiliyse formun **üstünde** ya da Kaydet düğmesinin yakınında, "Kaydet'e basarak <a>kayıt koşullarını</a> kabul edersiniz." gibi bir cümle içinde olmalı.

---

### 14. Düşük — `BrokenForm.cshtml:12–14` — Tekrarlı kullanım için giriş yardımcıları eksik

**Sorun**
- `autocomplete` yok: tarayıcı `name`/`email` alanlarını öneremez.
- `inputmode`/`type` açık değil: `asp-for`, ViewModel'de `[EmailAddress]`/`[DataType]` varsa `type="email"` üretir, ama ViewModel görülemedi. TC Kimlik No için `inputmode="numeric"` klavye/doğrulama ipucu verir.
- İlk alanda `autofocus` yok; sekreter her açılışta fareyle ilk kutuya tıklar (30×/gün).
- Alanlar arasında `mb-3` gibi boşluk sınıfı yok; `form-control` öğeleri üst üste yapışık render olur (Bootstrap varsayılanı).

**Düzeltme**
- `AdSoyad`: `autocomplete="name" autofocus`
- `Eposta`: `type="email" autocomplete="email" inputmode="email" spellcheck="false"`
- `TcKimlikNo`: `inputmode="numeric" maxlength="11" autocomplete="off"`
- Her alan grubu `<div class="mb-3">` içine.

---

## Kapsam dışı / doğrulanamayan noktalar

Aşağıdakiler yalnız bu dosyadan belirlenemez; layout, CSS ve controller ile birlikte kontrol edilmelidir:

1. **`<html lang="tr">`** — Layout'ta olmalı (WCAG 3.1.1). Yoksa ekran okuyucu Türkçe metni İngilizce sesletir.
2. **`<main>` landmark'ı ve sayfa `<title>`** — `ViewData["Title"]` set ediliyor (satır 3); layout'un bunu `<title>` içinde kullandığı varsayıldı.
3. **`.broken`, `.fake-btn`, `.icon-only`, `.pulse` CSS'i** — hedef boyutları, odak stilleri, animasyon süresi doğrulanamadı.
4. **jQuery ve `_ValidationScriptsPartial`** — yüklü olduğu varsayılamaz; satır 18–19 bunlara bağımlı.
5. **ViewModel data annotations** — `[Required]`, `[Display]`, `[EmailAddress]` varlığı bilinmiyor; etiket metinleri ve otomatik `type` üretimi buna bağlı.
6. **Controller `Kayit`/`Sil` eylemleri** — `Sil` GET ile silme yapıyorsa Bulgu 2 kritikliğini korur; `[HttpPost]` + `ValidateAntiForgeryToken` ile sınırlıysa link zaten çalışmıyor demektir (yine düzeltilmeli).
7. **Başarı geri bildirimi** — Kayıt sonrası nereye yönlendirildiği ve mesaj gösterildiği bilinmiyor (WCAG 4.1.3).
8. **Null güvenliği** — `Model.Siniflar`, `Model.Notlar`, `Model.Id` null gelirse görünüm çöker; controller'da garanti edilmeli.

---

## Öncelikli düzeltme sırası

1. Satır 18: `div` → `<button type="submit">` (klavye + Enter ile gönderim).
2. Satır 21: Silme → POST form + onay + okunur metin + ≥ 24 px hedef; Kaydet'ten uzağa.
3. Satır 12–17: Her alana `<label asp-for>` + `<span asp-validation-for>`; `is-invalid` ve `outline:none` kaldır; `required`/`*` işaretleri; satır 11'e `asp-validation-summary` ve gizli `Id`.
4. Satır 19: Sıfırlama düğmesini kaldır ya da etiketle + onay + uzaklaştır.
5. Satır 7–9: `<h1>`, `alt`, kontrast ve doğru zorunluluk cümlesi.
6. Satır 22–29: Rozeti kaldır/sınırla; tabloya `caption` + `thead` + boş durum; link metnini düzelt.
7. Satır 12–14: `autocomplete`/`inputmode`/`autofocus` (verimlilik).

İlk üç madde sayfayı klavyeyle **kullanılabilir** ve ekran okuyucuyla **anlaşılır** kılar; kalanlar günlük 30 kullanımda hata ve zaman kaybını azaltır.
