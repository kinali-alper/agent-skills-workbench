# UX + Erişilebilirlik Denetimi — FixedForm.tsx

**Denetlenen dosya:** `FixedForm.tsx` (proje yalnız bu dosyadan oluşuyor)
**Bağlam:** Türkçe arayüz, veli kullanıcılar, mobil, ilk kez kullanım. Sayfa render edilemedi; yalnız kaynak kod incelendi.

**Yöntem notu:** Dosya `className="hint" / "error" / "badge" / "status" / "cancel" / "actions" / "fixed"` sınıflarına başvuruyor ama projede bir stil dosyası yok. Bu yüzden tek kural uygulandı: hüküm dosyadaki kod kanıtıyla verilebiliyorsa **uygun/ihlal**; hüküm tamamen dosyada bulunmayan bir CSS değerine bağlıysa **doğrulanamaz**. Stil yokken tarayıcı varsayılanları geçerlidir (linkler altı çizili, varsayılan odak halkası, siyah/beyaz metin).

## Özet

| Hüküm | Sayı |
|---|---|
| ihlal | 0 |
| uygun | 15 |
| uygulanamaz | 2 |
| doğrulanamaz | 4 |

---

## U — Kullanılabilirlik

| U | Hüküm | Kanıt / Gerekçe |
|---|---|---|
| U1 | **uygun** | Gönder → `setStatus` :42 (hata) / :46 (başarı); Temizle → `setStatus('Form temizlendi.')` :52; İptal → `href="/"` yönlendirme :99. Durum mesajı `role="status" aria-live="polite"` içinde :101 ve ilk render'dan itibaren DOM'da. |
| U2 | **uygun** | Çıkış yolu: `İptal` linki :99. Yarım veri (`dirty` :29) varken çıkışta `confirm('Girdiğiniz bilgiler kaybolacak. Çıkılsın mı?')` :56. |
| U3 | **uygun** | TC: `inputMode="numeric" maxLength={11}` :87 (type belirtilmemiş → text; kimlik no için doğru kalıp, sayısal klavye açılır), kalıcı ipucu `'11 rakam, boşluksuz.'` :87, hata metni ne yanlış + nasıl düzelir + örnek :17. E-posta: `type="email" autoComplete="email"` :86, hata metni örnekli :15. Telefon/tarih alanı yok. İyileştirme (ihlal değil): e-posta için hata öncesi kısa bir biçim ipucu eklenebilir. |
| U4 | **uygun** | Zorunlu işareti: etikette `*` :65 + açıklama `'Yıldızla (*) işaretli alanlar zorunludur.'` :81. Hata işareti ayrı sinyal: `aria-invalid` :67 + `⚠` ikonu ve metin :69. Yönerge gerçekle örtüşür: dört alanın dördü de `required` :66 ve dördü de yıldızlı. |
| U5 | **uygun** | Formu temizle → `confirm('Formdaki tüm bilgiler silinecek. Devam edilsin mi?')`, hayır ise `preventDefault` :50. Kirli formdan çıkış → onay :56. Gönderim yıkıcı değil (kayıt; onay e-postası ile teyit :46). |
| U6 | **uygun** | `Yeni` rozeti bir içeriğe bağlı: `'Sınıf listesi 2026-27 dönemine güncellendi.'` :104. Bağlamsız dikkat çekici yok. |
| U7 | **uygun** | Her alanda kalıcı `<label htmlFor>` :65. `placeholder` özniteliği hiç kullanılmıyor. Select'teki `'Sınıf seçin'` seçeneği :90 etiket değil, ilk seçenek; `Sınıf` etiketi :88 kalıcı. |
| U8 | **uygun** | `Kaydet` :97, `Formu temizle` :98, `İptal` :99, `Kayıt koşullarını görüntüle` :104 — hepsi Türkçe, eylemi/hedefi söylüyor. |

## A — Erişilebilirlik

| A | Hüküm | Kanıt / Gerekçe |
|---|---|---|
| A1 | **doğrulanamaz** | Dosya içinde kontrol edilebilenler geçiyor: tek `h1` :76, `h2` :116 (hiyerarşik), `<main>` landmark :75. Atlama linki sayfa düzeyinde bir öğedir; bileşen dosyasında doğrulanamaz (kontrol listesinin kendi notu). |
| A2 | **uygun** | Tek görsel :78 — picsum yer tutucu banner, bilgi taşımıyor; `alt=""` doğru. `width/height` verildiği için düzen kayması da yok. |
| A3 | **doğrulanamaz** | Dosyadaki tek renk çifti `#4a4a4a` / `#fff` :80 → yaklaşık 8.9:1, geçer. `.error`, `.hint`, `.badge`, `.status`, `.cancel` renkleri stil dosyasında; dosya projede yok. Stil yoksa tarayıcı varsayılanı (siyah/beyaz) geçer. |
| A4 | **uygun** | Ortak `field()` sarmalayıcısı her kontrole `<label htmlFor={f}>` :65 ve `id: f` :66 veriyor; dört alan da bu sarmalayıcıdan geçiyor :85–94. `select` dahil. |
| A5 | **uygun** | Hata renk dışı iki sinyalle: metin + `⚠` ikonu :69 (ikon `aria-hidden`, metin okunur), programatik olarak `aria-invalid` + `aria-describedby` :67 (hata varken `${f}-err`, yokken `${f}-hint` :62). Gövde metnindeki link :104 için dosyada altı çizgiyi kaldıran stil yok; tarayıcı varsayılanı (altı çizili) geçerli. |
| A6 | **uygun** | Dosyada `outline` kaldıran stil ya da `onFocus={blur}` benzeri odak düşüren script yok. Gönderimde odak ilk hatalı alana **taşınıyor** :43 (düşürülmüyor). Stil yokken tarayıcı varsayılan `:focus-visible` halkası geçerli. Not: dış CSS eklenirse ≥ 3:1 gösterge yeniden kontrol edilmeli. |
| A7 | **uygun** | Tüm etkileşimli öğeler native: `input` :85–87, `select` :89, `button type="submit"` :97, `button type="reset"` :98, `a href` :99, :104. `div/span + onClick` yok. |
| A8 | **uygulanamaz** | Yalnız ikon/emoji taşıyan denetim yok. `🗑 Formu temizle` :98 görünür metin taşıyor; `⚠` :69 `aria-hidden` ve yanında metin var. Öneri (ihlal değil): `🗑` de `aria-hidden` ile sarılırsa ekran okuyucu "çöp kutusu" okumaz. |
| A9 | **doğrulanamaz** | Boyutlar CSS'te. `button`, `input`, `select` tarayıcı varsayılan boyutunda → 2.5.8 "kullanıcı ajanı" istisnası. `İptal` linki :99 buton satırında (`.actions`), gövde metni içinde değil; inline istisnası uygulanmaz, boyutu `.cancel` stiline bağlı — dosyada yok. |
| A10 | **uygulanamaz** | Animasyon, otomatik hareket, otomatik oynatma, flaş yok. |
| A11 | **uygun** | `<caption>` :107, sütun başlıkları `th scope="col"` :108, satır başlıkları `th scope="row"` :110–111. Tablo 3×2 (küçük); elle kontrol edildi. |
| A12 | **doğrulanamaz** | `<html lang>` sayfa düzeyinde; bileşen dosyasında `html` öğesi yok. Dil değişen parça yok — tüm metin Türkçe; `lang` gereken alt parça bulunmuyor. |
| A13 | **uygun** | Canlı bölge `role="status" aria-live="polite"` :101 ilk render'dan itibaren DOM'da (sonradan eklenmiyor → duyuru güvenilir). Gönderim özeti :42/:46 ve temizleme :52 bu bölgeden duyurulur. Alan başı hata metinleri :69 canlı bölgede değil; `aria-describedby` :67 ile alana bağlı, gönderimde odak ilk hataya taşındığında :43 okunur — kabul gören kalıp. |

---

## Not edilen küçük iyileştirmeler (ihlal sayılmadı)

- :98 `🗑` emojisi `aria-hidden` ile gizlenebilir; erişilebilir ad zaten metinden geliyor.
- :86 e-posta alanına hata öncesi kısa biçim ipucu (`örn. ayse@ornek.com`) eklenebilir; TC alanındaki kalıp ile tutarlı olur.
- :65 etiketteki `*` ekran okuyucuda "yıldız" olarak okunur; :81'deki açıklama bunu karşılıyor, alternatif olarak `<span aria-hidden>*</span>` + `required` yeterli olur.

## Kısa özet

- İhlal yok: form etiketleme, hata sinyali, onay akışları, durum duyurusu ve tablo yapısı doğru kurulmuş.
- Dört madde (A1 atlama linki, A3 renkler, A9 hedef boyutu, A12 `html lang`) yalnız kaynak dosyadan doğrulanamıyor; sayfa düzeyi ya da CSS gerekiyor.
- İki madde (A8 ikon-only kontrol, A10 hareket) bu bileşende uygulanamaz.