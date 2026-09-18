## FixedForm.tsx  ·  Kullanıcılar: veliler — mobil, ilk kez kullanan, tek seferlik (kayıt dönemi başına bir)  ·  Dil: Türkçe

Kapsam: tek bileşen dosyası (`FixedForm.tsx`, 121 satır). Öğrenci kayıt formu (ad, veli e-postası, TC kimlik no, sınıf) + Kaydet / Formu temizle / İptal eylemleri, durum mesajı, "Yeni" rozeti, küçük not tablosu, kayıt koşulları bölümü. Sayfa render edilemedi; CSS, host HTML ve rota dosyaları mevcut değil.

Yöntem: adım 1 bağlam (kullanıcıdan verildi), adım 2 `heuristic-evaluation` süreci (yeni kullanıcı gözü → deneyimli kullanıcı gözü → görev akışları: kayıt gönderme, formu temizleme, vazgeçme, hata düzeltme), adım 3 A1–A13 statik denetim, `references/locale-tr.md` Türkçe örnekleriyle karşılaştırıldı.

### Bulgular (şiddete göre)

**İhlal bulunmadı.** Dosyadaki hiçbir satır U1–U8 veya A1–A13 kural metnini çiğnemiyor. Kanıtı dosya dışında (CSS / host HTML) olan 6 madde aşağıda "doğrulanamaz" olarak işlendi ve İnsan için TODO'ya taşındı.

#### Notlar (ihlal değil — şiddet 1, isteğe bağlı iyileştirme)

- FixedForm.tsx:98 — A8/U8 kapsamında **uygun** (buton görünür metin taşıyor). Ancak `🗑` emojisi `aria-hidden` değil; ekran okuyucu erişilebilir adı "çöp kutusu Formu temizle" olarak okur. Aynı dosyada :69'daki `⚠` ikonu `aria-hidden="true"` ile gizlenmiş — tutarlılık için emojiyi de `<span aria-hidden="true">🗑 </span>` içine al.
- FixedForm.tsx:65 — Zorunlu işareti `*` etiket metninin içinde ve `aria-required` ile birlikte veriliyor; ekran okuyucu "yıldız" + "zorunlu" diye iki kez duyurur. Kozmetik; istenirse `<span aria-hidden="true"> *</span>` ile yalnız görsel bırak. U4 hükmü değişmez (iki ayrı sinyal mevcut, yönerge :81 gerçek durumla örtüşüyor).
- FixedForm.tsx:31, :35 — Alan terk edilince (blur) çıkan satır içi hata canlı bölgede değil; yalnız `aria-describedby` ile alana bağlı (:67). Ekran okuyucu kullanıcısı bir sonraki alana geçtiği için o anda duymaz; gönderimde :42 durum mesajı + :43 odak taşıma ile telafi ediliyor. 4.1.3 ihlali değil; NVDA ile doğrulanacak (TODO).

### Kontrol listesi hükümleri

**Erişilebilirlik (A1–A13)**

- A1 **doğrulanamaz** — atlama linki sayfa düzeyinde, bileşen dosyasında karar verilemez (skill kuralı). Dosyada kanıtlı kısımlar uygun: tek `h1` :76, `h2` :116 hiyerarşik, `main` landmark :75.
- A2 **uygun** — :78 görsel süs (rastgele picsum banner), `alt=""` doğru; bilgi taşıyan görsel yok.
- A3 **doğrulanamaz** — dosyadaki tek renk çifti :80 `#4a4a4a` / `#fff` ≈ 8.9:1 (geçer). `.hint`, `.error`, `.badge`, `.status`, `.cancel`, buton renkleri CSS'te.
- A4 **uygun** — :65 `<label htmlFor={f}>` ↔ :66 `id: f`; dört alan da (`ad`, `eposta`, `tc`, `sinif`) aynı sarmalayıcıdan geçiyor (:85–:94).
- A5 **doğrulanamaz** — hata sinyali dosyada tam kanıtlı ve uygun: :67 `aria-invalid` + `aria-describedby`, :69 ikon + metin (renk tek sinyal değil). Gövde metni içindeki link (:104) altı çizgisi CSS'e bağlı; tarayıcı varsayılanı çizili, `text-decoration: none` olmadığı doğrulanmalı.
- A6 **doğrulanamaz** — `:focus-visible` göstergesi CSS'te. Dosyada odak düşüren script yok; tersine :43 hatalı ilk alana programatik odak veriyor (olumlu).
- A7 **uygun** — tüm etkileşimli öğeler native: `input` :85–87, `select` :89, `button` :97–98, `a href` :99 ve :104. `div/span + onClick` yok.
- A8 **uygun** — yalnız ikon taşıyan denetim yok; :98 butonu görünür metin taşıyor ("Formu temizle"), :69 `⚠` ikonu `aria-hidden` (bkz. Notlar).
- A9 **doğrulanamaz** — buton/link boyutları CSS'te (`.actions`, `.cancel`). Mobil veli için 44×44 hedeflenmeli (TODO).
- A10 **uygulanamaz** — dosyada animasyon, geçiş veya otomatik hareket yok.
- A11 **uygun** — :107 `caption`, :108 `th scope="col"` ×2, :110–111 `th scope="row"`. Tablo 2×2 gövde (axe'ten kaçan boyut) — elle kontrol edildi.
- A12 **doğrulanamaz** — `html lang` host belgede. Dosya içinde dil değişen parça yok (örnek e-posta `ayse@ornek.com` :15 Türkçe bağlamda okunur).
- A13 **uygun** — :101 `<p role="status" aria-live="polite">`; :42/:46/:52 gönderim, hata ve temizleme sonuçları buraya yazılıyor.

**Kullanılabilirlik (U1–U8)**

- U1 **uygun** (H1) — Kaydet → :46 "Kayıt alındı. Onay e-postası gönderildi." / :42 "Kayıt yapılamadı: aşağıda işaretli alanları düzeltin." + :43 ilk hatalı alana odak; Formu temizle → :52 "Form temizlendi."; İptal → :99 ana sayfaya yönlendirme. Hepsi :101 `role="status"` üzerinden duyurulur. Dosyada ağ isteği yok, bu yüzden bekleme göstergesi gerekmiyor.
- U2 **uygun** (H3) — :99 İptal linki her an mevcut; :56 yarım veri (`dirty` :29) varsa çıkışta onay soruyor.
- U3 **uygun** (H5·H10) — TC: :87 `inputMode="numeric"` + `maxLength={11}` + kalıcı ipucu "11 rakam, boşluksuz."; hata :17 ne yanlış + örnek. E-posta: :86 `type="email"` + `autoComplete="email"`; hata :15 örnekli. `type="number"` kullanılmamış (kimlik numarası için doğru). Ad alanındaki `autoComplete="off"` (:85) velinin kendi verisi olmadığı için sorun değil.
- U4 **uygun** (H4) — Zorunlu: :65 etikette `*` + :81 form başı yönerge "Yıldızla (*) işaretli alanlar zorunludur" — dört alan da zorunlu, yönerge gerçek durumla örtüşüyor. Hata: :67 `aria-invalid` + :69 ikon + metin — zorunlu işaretinden ayrı sinyal.
- U5 **uygun** (H3) — :50 Formu temizle onay istiyor; :56 dolu formdan çıkış onay istiyor. Geri alınamaz başka eylem yok.
- U6 **uygun** (H8) — :104 "Yeni" rozeti somut içeriğe bağlı: "Sınıf listesi 2026-27 dönemine güncellendi." Bağlamsız dikkat çekici yok.
- U7 **uygun** (H6) — :65 kalıcı `<label>`; hiçbir alan placeholder'ı etiket yerine kullanmıyor. :90 "Sınıf seçin" seçeneği etiketin yanında ek ipucu, etiket değil.
- U8 **uygun** (H2) — :97 "Kaydet", :98 "Formu temizle", :99 "İptal", :104 "Kayıt koşullarını görüntüle" — eylem/hedef Türkçe ve somut; "tıkla / devamı" tipi metin yok.

**Özet satırı:** A1 doğrulanamaz · A2 uygun · A3 doğrulanamaz (CSS) · A4 uygun · A5 doğrulanamaz (link CSS; hata sinyali uygun) · A6 doğrulanamaz (CSS) · A7 uygun · A8 uygun · A9 doğrulanamaz (CSS) · A10 uygulanamaz · A11 uygun · A12 doğrulanamaz (html) · A13 uygun · U1 uygun · U2 uygun · U3 uygun · U4 uygun · U5 uygun · U6 uygun · U7 uygun · U8 uygun

**Sayım:** ihlal 0 · uygun 14 · uygulanamaz 1 · doğrulanamaz 6 (toplam 21/21)

### Klavye gezintisi

**render yok — statik denetim.** DOM sırasından çıkarılan Tab yolu: `ad` (:85) → `eposta` (:86) → `tc` (:87) → `sinif` (:89) → Kaydet (:97) → Formu temizle (:98) → İptal (:99) → "Kayıt koşullarını görüntüle" (:104). Görsel sıra DOM sırasıyla aynı (özel `tabIndex` yok). Tüm eylemler native öğe, klavyeyle ulaşılabilir. Odak kaybı yaratan script yok; gönderimde hata varsa odak :43 ile ilk hatalı alana taşınır ve `aria-describedby` hata metnini okutur. `confirm()` diyalogları (:50, :56) tarayıcı native, klavyeyle Enter/Esc ile yönetilir. Odak göstergesinin görünürlüğü CSS'e bağlı (A6).

### İnsan için TODO

Doğrulanamaz maddeler (kanıt CSS / host HTML'de):

- [ ] **A1** — Sayfa şablonunda tekrarlayan blok (üst menü) varsa `main`'e atlama linki var mı? (`<a href="#main">İçeriğe geç</a>`, ilk odaklanabilir öğe.)
- [ ] **A3** — CSS'te `.hint`, `.error`, `.badge`, `.status`, `.cancel` ve buton metin/arka plan renklerini ölç: metin ≥ 4.5:1, UI bileşeni ≥ 3:1. Özellikle kırmızı hata metni ve "Yeni" rozeti.
- [ ] **A5** — `.cancel` ve gövde içi link (:104) için CSS'te `text-decoration: none` yoksa tamam; varsa altı çizgi veya renk dışı ayırt edici geri ver.
- [ ] **A6** — `:focus-visible` ile ≥ 3:1 kontrastlı, ≥ 2–3 px outline var mı? `outline: none` kullanılmışsa eşdeğer gösterge ekle.
- [ ] **A9** — `.actions` içindeki butonlar ve İptal linki ≥ 24×24 CSS px (mobil veli için 44×44 hedefle); İptal linkine `padding` ver, butonlar arasında ≥ 8 px boşluk.
- [ ] **A12** — Host belgede `<html lang="tr">`.

Skill'in zorunlu insan kontrolleri:

- [ ] **Ekran okuyucu (NVDA / VoiceOver):** dört etiket alan adıyla okunuyor mu; blur sonrası çıkan hata bir sonraki alana geçildiğinde duyuluyor mu (duyulmuyorsa hata `<p>` öğesine `role="alert"` düşün); gönderim sonrası :101 durum mesajı ve ilk hatalı alana odak taşıması çalışıyor mu; tablo hücrelerinde "Ders / Not" başlıkları okunuyor mu; :98 butonunda "çöp kutusu" ön eki rahatsız ediyor mu.
- [ ] **%200 yakınlaştırma ve 320 px genişlik:** `.actions` satırındaki üç eylem taşıyor mu, hata metinleri ve tablo kesiliyor mu, :78 görsel (320 px sabit) yatay kaydırma yaratıyor mu.
- [ ] **Gerçek kullanıcıyla 1 görev:** ilk kez kullanan bir veli, telefonda yardımsız "çocuğunu 5. sınıfa kaydet" akışını tamamlayıp onay mesajını görüyor mu? Özellikle TC alanında sayısal klavyenin açıldığını ve yanlış e-posta girişinde hata metnini anladığını gözle.