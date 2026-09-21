## FixedForm.tsx  ·  Kullanıcılar: veliler — mobil, ilk kez kullanan, seyrek (yılda bir kayıt)  ·  Dil: Türkçe  ·  **Statik denetim (render yok)**

Bağlam kullanıcı tarafından verildi; dosya içi metinler (h1 "Öğrenci Kayıt", "Veli e-postası", onay e-postası) bunu doğruluyor. Seyrek kullanım → H7 kısayol beklentisi yok; mobil → hedef boyutu ve `inputMode` kritik.

### Bulgular (şiddete göre)

**Kontrol listesi ihlali: yok.** A1–A13 ve U1–U8'de dosya kanıtıyla çiğnenen kural bulunmadı.

Aşağıdakiler hüküm etkilemeyen, düşük şiddetli iyileştirme notlarıdır (ihlal sayılmaz):

FixedForm.tsx:98 — A8 çevresi · WCAG 4.1.2 · şiddet 1 — "🗑 Formu temizle" butonunda emoji erişilebilir ada giriyor (ekran okuyucu "çöp kutusu Formu temizle" der); görünür metin zaten var → emojiyi `<span aria-hidden="true">🗑 </span>` içine al, 69. satırdaki ⚠ deseniyle aynı.
FixedForm.tsx:46 — H5 · şiddet 1 — Başarılı gönderimden sonra form dolu ve Kaydet etkin kalıyor; ikinci dokunuş aynı kaydı yeniden tetikleyebilir → başarıda Kaydet'i devre dışı bırak ya da onay görünümüne geç (durum mesajı korunarak).
FixedForm.tsx:42 — U1 çevresi · H1 · şiddet 1 — Hata durumu mesajı genel ("işaretli alanları düzeltin"); odak ilk hatalı alana gidiyor, bu yeterli → isteğe bağlı: hatalı alan sayısını ve ilk alanın adını söyle ("2 alan hatalı: TC Kimlik No…").

### Kontrol listesi hükümleri

**Erişilebilirlik (A)**
A1 doğrulanamaz (atlama linki sayfa düzeyi; dosyada tek `h1` :76, `h2` :116 hiyerarşik, `main` :75 uygun) · A2 uygun (:78 süs görsel `alt=""`; picsum yer tutucu, bilgi taşımıyor) · A3 doğrulanamaz (CSS; tek satır içi kanıt :80 `#4a4a4a`/`#fff` = 8,9:1 uygun; `.error`, `.hint`, `.badge`, buton renkleri CSS'te) · A4 uygun (:65–66 her denetim `label htmlFor` ↔ `id`, select dahil) · A5 uygun (hata: :69 ⚠ ikon + metin + :67 `aria-invalid` + `aria-describedby`; :104 gövde linki tarayıcı varsayılan alt çizgisine dayanıyor, CSS kaldırıyorsa TODO) · A6 doğrulanamaz (`:focus-visible` CSS'te; kaynakta odak düşüren script yok, :43 odak ilk hatalı alana taşınıyor — uygun) · A7 uygun (:85–99 `input`, `select`, `button`, `a href`; div/span onClick yok) · A8 uygun (yalnız ikonlu denetim yok; :98 emoji + görünür metin, bkz. not) · A9 doğrulanamaz (hedef boyutu CSS'te; :99 `İptal` inline `a`, mobil için ≥ 24 px teyit gerek) · A10 uygulanamaz (hareket/animasyon/otomatik güncelleme yok) · A11 uygun (:107 `caption`, :108 `th scope="col"`, :110–111 `th scope="row"`; 2×2 tablo elle kontrol edildi) · A12 doğrulanamaz (`html lang` sayfa düzeyi; dosyada dil değişen parça yok) · A13 uygun (:101 `role="status" aria-live="polite"` DOM'da önceden var, :42/:46/:52 mesajlar buraya yazılıyor)

**Kullanılabilirlik (U)**
U1 uygun (:46 "Kayıt alındı. Onay e-postası gönderildi.", :42 hata durumu, :52 "Form temizlendi." → :101 status) · U2 uygun (:99 İptal linki, :56 kirli formda çıkış onayı; :98 temizle) · U3 uygun (:86 `type="email" autoComplete="email"`, :87 `inputMode="numeric" maxLength=11` + ipucu "11 rakam, boşluksuz."; :15/:17 hata metinleri ne yanlış + örnek) · U4 uygun (zorunlu: :65 `*` + :81 açıklama; hata: ikon + metin + aria-invalid; :81 yönerge tüm alanların zorunlu olduğu gerçekle örtüşüyor) · U5 uygun (:50 temizleme onay istiyor; gönderim öncesi doğrulama 3.3.4 "kontrol edilebilir" koşulunu sağlıyor) · U6 uygun (:104 "Yeni" rozeti "Sınıf listesi 2026-27 dönemine güncellendi" içeriğine bağlı) · U7 uygun (:65 kalıcı `label`; :90 "Sınıf seçin" seçeneği etiketin yerine geçmiyor) · U8 uygun (:97 "Kaydet", :98 "Formu temizle", :99 "İptal", :104 "Kayıt koşullarını görüntüle" — hedef/eylem Türkçe)

**WCAG 2.2 AA tarama (kalan 36 kriter, dosyada ilgili olanlar)**
1.3.5 uygun — :86 veli e-postası `autocomplete="email"`; :85 öğrenci adı ve :87 öğrenci TC'si kullanıcının kendi bilgisi değil, `autocomplete` zorunlu değil · 1.3.3 uygun — :81 yönerge yıldız karakterini metinle de veriyor · 2.5.2 uygun — eylemler `click`/`submit`/`reset`te · 3.2.2 uygun — :89 select onChange yalnız state · 3.3.3 uygun — :15/:17 düzeltme önerisi · 3.3.4 uygun — gönderim öncesi doğrulama + temizlemede onay · 3.3.8 uygun — yapıştırma engeli yok · 2.4.2 / 2.4.5 / 3.2.3 / 3.2.6 sayfa/site düzeyi, dosyada uygulanamaz · 1.2.x / 1.4.2 / 2.1.4 / 2.2.1 / 2.5.1 / 2.5.4 / 2.5.7 uygulanamaz (medya, kısayol, zaman sınırı, hareket yok).

### Klavye gezintisi
Render yok — statik denetim. Kaynaktan öngörü: DOM sırası = ad → e-posta → TC → sınıf → Kaydet → Formu temizle → İptal → (durum) → Kayıt koşulları linki; CSS `order`/`float` kullanılmıyorsa görsel sırayla örtüşür. Tüm eylemler native öğe, Tab ile ulaşılabilir; gönderimde odak ilk hatalı alana taşınıyor (:43). Tuzak oluşturacak bileşen yok.

### İnsan için TODO
- **A1** — Sayfa şablonunda atlama linki ("İçeriğe geç") ve `main`'in tek olduğunu doğrula (bileşen zaten `main` render ediyor; şablonda ikinci bir `main` varsa birini `div`e çevir).
- **A3** — CSS'te `.error`, `.hint`, `.badge`, buton ve `.cancel` link renklerini ölç: metin ≥ 4,5:1, UI kenarlığı ≥ 3:1. Satır içi `#4a4a4a`/`#fff` (8,9:1) tamam.
- **A5** — `.cancel` ve gövde linkinde `text-decoration: none` varsa alt çizgi ya da renk dışı ayırt edici ekle.
- **A6** — `:focus-visible` göstergesi ≥ 3:1 ve `outline: none` ile silinmemiş olsun; Tab ile baştan sona gez, odak kaybolan yer var mı bak.
- **A9** — Mobilde `İptal` (`a.cancel`) ve `🗑 Formu temizle` hedefleri ≥ 24×24 CSS px (tercihen 44); butonlar arası boşluk yanlış dokunmayı önlesin.
- **A12** — `<html lang="tr">` sayfa şablonunda.
- **Ekran okuyucu (NVDA/VoiceOver)** — etiketler "Öğrencinin adı soyadı yıldız" şeklinde okunuyor mu, blur sonrası `aria-describedby` hata metni okunuyor mu, gönderimde status mesajı ve odak taşınması birlikte duyuruluyor mu, tablo başlıkları (Ders/Not, satır başlığı) okunuyor mu.
- **%200 yakınlaştırma ve 320 px** — `.actions` satırındaki üç eylem taşmadan sarıyor mu, tablo yatay kaydırma yaratıyor mu.
- **Gerçek kullanıcı, 1 görev** — ilk kez kullanan bir veli, telefonda, yardımsız: öğrenciyi kaydedip "Kayıt alındı" mesajını görüyor mu; TC alanına boşluklu yapıştırma (maxLength kesmesi) hata döngüsü yaratıyor mu.