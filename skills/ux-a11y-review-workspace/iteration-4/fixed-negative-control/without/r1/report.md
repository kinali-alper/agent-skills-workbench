# UX ve Erişilebilirlik Denetimi — `FixedForm.tsx`

**Kapsam:** Yalnız kaynak dosya (`FixedForm.tsx`, 121 satır). CSS, router, sayfa iskeleti (`<html lang>`, `<title>`) yok; sayfa render edilemedi. Bulgular statik okuma ile sınırlıdır.
**Bağlam:** Türkçe arayüz, kullanıcılar veliler, mobil, ilk kez kullanan.
**Önem ölçeği:** Yüksek (görevi engeller / yanlış anlamaya yol açar) · Orta (belirgin sürtünme veya AT kullanıcılarına eksik bilgi) · Düşük (cila).

## Genel değerlendirme

Dosya, tipik form hatalarının çoğunu doğru çözmüş: her kontrolün `htmlFor` ile bağlı görünür etiketi var (65), hata/ipucu `aria-describedby` ile bağlı (62-69), `aria-invalid` durum bazlı (67), hata yalnız blur/gönderim sonrası görünür (31), gönderimde ilk hatalı alana odak (43), `role="status"` canlı bölge DOM'da baştan var (101), `noValidate` + `required` birlikte kullanılmış (66, 84), e-posta ve TC için doğru `type`/`inputMode` seçilmiş (86-87), tablo `caption` + `scope` ile işaretlenmiş (106-113), dekoratif görsel `alt=""` (78), uyarı simgesi `aria-hidden` (69), hata metinleri Türkçe ve "ne yanlış + nasıl düzelir" biçiminde (13-18). Aşağıdaki bulgular bu tabanın üzerine kalan boşluklardır; hiçbiri "erişilemez" seviyesinde değildir.

Toplam: **17 bulgu** (Yüksek 2, Orta 8, Düşük 7) + doğrulanamayan 1 grup.

---

## Yüksek

### 1. Başarı mesajı, kayıt koşullarıyla çelişiyor — `FixedForm.tsx:46`, `:117`
**Sorun:** Gönderim sonrası "Kayıt alındı. Onay e-postası gönderildi." deniyor; aynı sayfanın altında (117) "Kayıt, veli onayı ve okul yönetiminin kontenjan kontrolü sonrasında kesinleşir." yazıyor. İlk kez kayıt yapan veli, "Kayıt alındı" ifadesini "çocuğum kayıtlandı" diye okur; kontenjan reddi geldiğinde güven kaybı yaşar. Ayrıca mesaj, onayın hangi adrese gittiğini söylemiyor; regex'ten geçen ama yanlış yazılmış bir adresi (örn. `gmial.com`) fark etme şansı yok.
**Düzeltme:** `setStatus(`Başvurunuz alındı. Onay bağlantısı ${values.eposta} adresine gönderildi. Kayıt, kontenjan kontrolünden sonra kesinleşir.`)` gibi hem adresi yansıtan hem de durumu doğru adlandıran bir metin. Buna paralel olarak h1/submit etiketini de "Kayıt Başvurusu" / "Başvuruyu gönder" olarak hizalamak tutarlılığı sağlar.

### 2. Hata durumunda odak + canlı bölge çakışıyor; hata özeti yok — `FixedForm.tsx:39-44`, `:101`
**Sorun:** `onSubmit` içinde `setSubmitted(true)` ve `document.getElementById(first)?.focus()` aynı handler'da çağrılıyor. React 18 state güncellemesini handler bittikten sonra uygular; odak DOM güncellenmeden taşınır. Alan daha önce blur edilmemişse odak anında `aria-invalid="false"` ve `aria-describedby` yoktur; ekran okuyucu alanı **hatasız** okur, hata metni sonradan DOM'a gelir ve odak duyurusunun içine girmez. Üstüne, "Kayıt yapılamadı: işaretli alanları düzeltin." metni `aria-live="polite"` ile odak değişimiyle aynı anda tetiklenir; iOS VoiceOver ve NVDA'da odak duyurusu polite bölgeyi sıklıkla bastırır. Sonuç: kullanıcı yalnız "Öğrencinin adı soyadı, düzenleme alanı, gerekli" duyar; kaç alanda hata olduğunu ve neyin yanlış olduğunu duymaz. Görme dayalı kullanıcı için de mesaj butonların altında (101), odak ise sayfanın üstünde; mobilde mesaj ekran dışında kalır.
**Düzeltme:**
- Odaklamayı `useEffect` ile `submitted`/`focusTarget` state'ine bağlayın ya da `flushSync` içinde state'i uygulayıp sonra `focus()` çağırın; böylece alan, hatasıyla birlikte duyurulur.
- Hata sayısını yazın: `"3 alanda hata var. İlk hataya odaklandınız."` veya GOV.UK deseni: formun üstünde `<div role="alert" tabIndex={-1}>` içinde başlık + her hataya `href="#alanId"` bağlantı listesi, odağı bu kutuya taşıyın.
- Aynı metnin ikinci kez set edilmesi (`status` değişmezse) canlı bölgeyi tetiklemez; hata mesajına sayı veya zaman damgası eklemek bunu da çözer.

## Orta

### 3. TC Kimlik No doğrulaması yalnız "11 rakam" — `FixedForm.tsx:6`, `:17`
**Sorun:** `^\d{11}$` yazım hatasını yakalamaz; TC Kimlik No'nun ilk hanesi 0 olamaz ve 10. ile 11. hane kontrol hanesidir. Mobilde küçük klavyeyle yazılan tek rakamlık hata sunucuya kadar gider, veli formu ikinci kez doldurur.
**Düzeltme:** Regex'e ek olarak standart algoritmayı uygulayın: ilk hane ≠ 0; `(tek hanelerin toplamı×7 − çift hanelerin toplamı) mod 10 = 10. hane`; `(ilk 10 hanenin toplamı) mod 10 = 11. hane`. Hata metni: "TC Kimlik No geçersiz görünüyor. Rakamları kontrol edin."

### 4. TC alanında yapıştırma/boşluk sessizce kırpılıyor — `FixedForm.tsx:87`
**Sorun:** `maxLength={11}` bir metin girişinde 12. karakteri sessizce yutar; "123 456 789 01" gibi boşluklu yapıştırma 11 karaktere kırpılır ve içinde boşluk kaldığı için "11 rakamdan oluşmalıdır" hatası verir — kullanıcı 11 rakam yazdığını sanır. Ekran okuyucu kullanıcısı düşen karakteri hiç duymaz.
**Düzeltme:** `tc` için `onChange`'de `e.target.value.replace(/\D/g, '').slice(0, 11)` uygulayın; `maxLength`'i kaldırabilir ya da güvenlik ağı olarak bırakabilirsiniz. Hata göründüğünde ipucu (`'11 rakam, boşluksuz.'`) DOM'dan kaldırılıyor (68); `aria-describedby`'ye her iki id'yi de verip ipucunu görünür bırakmak, hatayı okuyan kullanıcının biçim bilgisini de almasını sağlar.

### 5. Hassas veri (TC) için neden/gizlilik açıklaması yok — `FixedForm.tsx:87`, `:80-82`
**Sorun:** İlk kez kayıt yapan veliden çocuğunun TC Kimlik No'su isteniyor; sayfada bu verinin neden gerekli olduğu, nerede saklanacağı veya KVKK aydınlatma metni bağlantısı yok. Mobilde, tanımadığı bir sayfaya TC girmek velilerin en çok tereddüt ettiği adımdır; terk oranını doğrudan etkiler.
**Düzeltme:** TC alanına ipucu ekleyin: "Öğrencinin kimliğini MEB kayıtlarıyla eşleştirmek için gerekli. Bilgileriniz yalnız kayıt işleminde kullanılır." ve giriş paragrafına (80-82) aydınlatma metni bağlantısı koyun.

### 6. "Formu temizle" (reset) düğmesi birincil eylemin yanında — `FixedForm.tsx:98`
**Sorun:** Reset düğmeleri formda nadiren ihtiyaç duyulan, yanlışlıkla basıldığında tüm girdiyi silen bir eylemdir (Nielsen, "Reset and Cancel Buttons"). Mobilde "Kaydet" ile yan yana; parmak kayması riskini `confirm()` (50) kısmen azaltır ama diyalog metni "Devam edilsin mi?" ve düğmeleri tarayıcının "Tamam / İptal"ı — "İptal"e basmak temizlemeyi mi, çıkmayı mı iptal ediyor, ilk kez kullanan veli için belirsiz. Form boşken de `confirm` çıkıyor (`dirty` kontrolü yalnız `onCancel`'da, 56).
**Düzeltme:** Düğmeyi kaldırın (4 alanlı formda gereksiz). Kalacaksa: görsel olarak ikincil/metin düğme yapın, birincil düğmeden ayırın, `if (!dirty) return` ekleyin ve `confirm` yerine iki net etiketli düğmesi olan (`"Evet, temizle"` / `"Vazgeç"`) bir `<dialog>` kullanın.

### 7. Emoji ekran okuyucuya okunuyor — `FixedForm.tsx:98`
**Sorun:** `🗑 Formu temizle` — emoji `aria-hidden` değil; TTS "çöp kutusu Formu temizle" der. 69. satırda `⚠` için doğru yapılan şey burada yapılmamış.
**Düzeltme:** `<span aria-hidden="true">🗑 </span>Formu temizle` ya da emoji yerine SVG ikon.

### 8. İçerik sıralaması: koşullar formun altında, ilgisiz not tablosu araya girmiş — `FixedForm.tsx:104-118`
**Sorun:** "Kayıt koşulları" (115-118) velinin formu doldurmadan önce bilmesi gereken bilgidir ama formun ve bir "Son sınav notları" tablosunun (106-113) altında. Henüz kaydı yapılmamış bir öğrencinin kayıt sayfasında sabit notlar (Matematik 85, Türkçe 92) hem bağlamsız hem de kime ait olduğu belirsiz — ilk kez gelen veli "bu kimin notu?" diye durur. Mobilde bu içeriğe ulaşmak için formu geçmek gerekir; çoğu veli görmeden gönderir.
**Düzeltme:** "Kayıt koşulları"nı giriş paragrafının hemen altına (formdan önce) taşıyın veya giriş paragrafına bağlantı koyun. Not tablosunu bu sayfadan kaldırın; kayıt sonrası panele ait bir bileşen.

### 9. "İptal" bir bağlantı, diğer eylemler düğme — `FixedForm.tsx:99`, `:55-57`
**Sorun:** `<a href="/" className="cancel">` düğme grubunun içinde; ekran okuyucu "bağlantı, İptal" der, kullanıcı gezinme mi eylem mi ayırt edemez. Klavyede Boşluk tuşu bağlantıyı tetiklemez (düğmeleri tetikler) — üç kontrolde iki farklı davranış. `dirty` durumunda `confirm` doğru; ama boş formda bile "/"ye dönüş ilk kez gelen veli için nereye gittiğini söylemiyor.
**Düzeltme:** Gerçekten sayfa değişimi ise bağlantı kalabilir ama etiketi hedefi söylesin: "Ana sayfaya dön". Eylem grubu içinde tutulacaksa `<button type="button">` + router `navigate('/')`.

### 10. Çift gönderim / bekleme durumu yok — `FixedForm.tsx:37-47`
**Sorun:** `onSubmit` senkron; gerçek bir istek eklendiğinde "Kaydet"e iki kez dokunan veli (mobilde yaygın) iki kayıt yaratır. Başarı sonrası form açık ve düzenlenebilir kalıyor; status metni butonların altında, kullanıcı tekrar "Kaydet"e basabilir.
**Düzeltme:** `pending` state ile düğmeyi `disabled` + `aria-busy="true"` yapın ve etiketi "Gönderiliyor…" yapın; başarı sonrası formu gizleyip yerine başarı kartı gösterin veya onay sayfasına yönlendirin.

## Düşük

### 11. Zorunlu yıldızı ve açıklaması gereksiz/çelişkili — `FixedForm.tsx:65`, `:81`
**Sorun:** Dört alanın dördü zorunlu; her etikette `*` var ve giriş metni hem "tüm alanları doldurun" hem "yıldızlı alanlar zorunlu" diyor. Yıldız `aria-hidden` olmadığı için her etikette TTS "yıldız" ekler; `required`/`aria-required` zaten bunu iletiyor.
**Düzeltme:** Tümü zorunluysa yıldızları kaldırıp tek cümle bırakın: "Tüm alanlar zorunludur." Yıldız kalacaksa `<span aria-hidden="true"> *</span>`.

### 12. Sınıf hatası ile yer tutucu aynı metin — `FixedForm.tsx:18`, `:90`
**Sorun:** Hata "Sınıf seçin." ve placeholder seçeneği "Sınıf seçin" — hata mesajı yeni bilgi vermez; ekran okuyucu aynı ifadeyi iki kez okur.
**Düzeltme:** Hata: "Öğrencinin sınıfını seçin (5. veya 6. Sınıf)."

### 13. E-posta ipucu yalnız hata durumunda ortaya çıkıyor — `FixedForm.tsx:14`, `:86`
**Sorun:** "Onay bu adrese gidecek" bilgisi hata metninde var ama alanı doğru dolduran veli bunu hiç görmez; hangi e-postayı vermesi gerektiğine (kendisinin mi, öğrencinin mi) karar vermesine yardımcı olmaz.
**Düzeltme:** `field('eposta', …, 'Onay bağlantısı bu adrese gönderilecek; düzenli kontrol ettiğiniz bir adres yazın.')` — 87'deki TC ipucuyla aynı mekanizma.

### 14. Sabit genişlikli, üçüncü taraf görsel — `FixedForm.tsx:78`
**Sorun:** `width={320}` küçük ekranlarda (320 px viewport + `main` iç boşluğu) yatay kaydırma yaratabilir. `picsum.photos` rastgele fotoğraf servisi: velinin cihazına üçüncü taraf istek gider, içerik sayfayla ilgisiz, çevrimdışı/yavaş ağda LCP'yi geciktirir. `alt=""` doğru.
**Düzeltme:** Yerel, okula ait bir görsel; `style={{ maxWidth: '100%', height: 'auto' }}` veya CSS ile sınırlandırın. Anlam taşımıyorsa tamamen kaldırmak en sadesi.

### 15. Sayfa içi bağlantı hedefi odak alamıyor — `FixedForm.tsx:104`, `:115`
**Sorun:** `<a href="#detay">` → `<section id="detay">`. SPA router hash'i yutabilir; ayrıca `section` odaklanabilir olmadığı için bazı tarayıcı/ekran okuyucu kombinasyonlarında odak bağlantıda kalır, kullanıcı hedefe gittiğini duymaz.
**Düzeltme:** `<section id="detay" tabIndex={-1} aria-labelledby="detay-h">` ve `<h2 id="detay-h">`; router varsa `onClick` ile `scrollIntoView` + `focus()`.

### 16. Satır içi sabit renk — `FixedForm.tsx:80`
**Sorun:** `color: '#4a4a4a', background: '#fff'` kontrastı yeterli (~9.7:1) ancak satır içi stil, koyu tema / yüksek kontrast modunda diğer içerikle uyumsuz bir beyaz kutu oluşturur.
**Düzeltme:** Sınıfa taşıyın (`.intro`), renkleri temanın değişkenlerinden alın.

### 17. Başlık dili — `FixedForm.tsx:76`
**Sorun:** "Öğrenci Kayıt" Türkçede tamlama eki eksik; resmi bir okul sayfasında güveni zedeleyen küçük bir pürüz.
**Düzeltme:** "Öğrenci Kaydı" (ya da 1. bulguyla birlikte "Öğrenci Kayıt Başvurusu").

---

## Doğrulanamayan (CSS/sayfa iskeleti yok)

- **Odak görünürlüğü** (`:focus-visible`), **dokunma hedefi boyutu** (WCAG 2.5.8, ≥24×24 px; mobil için 44×44 önerilir) — özellikle 96-100 arası üç eylemin yan yana dizilimi ve 104'teki `.badge`.
- **Renk kontrastı**: `.error`, `.hint`, `.badge`, `.cancel` sınıfları ve buton durumları.
- **Birincil / ikincil eylem ayrımı**: "Kaydet"in görsel olarak baskın olup olmadığı.
- **Hata ile sanal klavye**: hata `<p>` alanın altında (69); mobilde klavye açıkken görünürlüğü.
- **Sayfa düzeyi**: `<html lang="tr">`, `<title>`, tek `<main>` — bileşen bunları sağlayamaz; kabuk tarafında doğrulanmalı.

## Doğru yapılanlar (değiştirmeyin)

`htmlFor`/`id` eşleşmesi (65-66) · `aria-describedby` id'lerinin gerçekten var olan öğelere işaret etmesi (62, 68-69) · blur-sonrası doğrulama (31, 35) · `noValidate` ile tarayıcı balonu yerine kalıcı, Türkçe hata (84, 13-18) · hata örnekli ("örn. ayse@ornek.com") · `type="email"` + `autoComplete="email"` (86) · TC için `type="number"` yerine `inputMode="numeric"` (87) · disabled placeholder `<option value="">` (90) · `role="status"` canlı bölgenin baştan DOM'da olması (101) · tablo `caption`/`scope` (107-111) · `confirm` ile veri kaybı koruması (50, 56) · `aria-hidden` uyarı simgesi (69).

---

## Kısa özet
- 17 bulgu: 2 yüksek, 8 orta, 7 düşük; form tabanı sağlam, sorunlar mesaj/akış ve mobil ayrıntılarında.
- En önemlisi: "Kayıt alındı" mesajı, sayfanın kendi kayıt koşullarıyla çelişiyor ve e-posta adresini geri göstermiyor (46, 117).
- Hata gönderiminde odak ile canlı bölge çakışıyor; ekran okuyucu hata sayısını/mesajını kaçırabilir (39-44, 101).
- TC alanı: kontrol hanesi doğrulanmıyor, boşluklu yapıştırma sessizce kırpılıyor, neden istendiği açıklanmıyor (6, 17, 87).
- "Formu temizle" ve emoji, "İptal" bağlantısı, içerik sırası (koşullar en altta, ilgisiz not tablosu) mobil veli için sürtünme.