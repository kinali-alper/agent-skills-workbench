# FixedForm.tsx — UX ve Erişilebilirlik Denetimi

**Kapsam:** Yalnız kaynak dosya (`FixedForm.tsx`, 121 satır). Sayfa render edilemedi; CSS yok. Bu yüzden renk kontrastı, dokunma hedefi boyutu, odak görünürlüğü gibi görsel ölçümler yapılamadı (bkz. son bölüm).
**Bağlam:** Arayüz Türkçe; kullanıcılar mobilde, formu ilk kez dolduran veliler.

## Genel değerlendirme

Dosya temel erişilebilirlik desenlerini doğru kuruyor: her kontrolün `htmlFor` ile bağlı `<label>`'ı var; hata/ipucu `aria-describedby` ile kontrole bağlı; `aria-invalid` durumu hata ile birlikte değişiyor; hata yalnız alan terk edildikten ya da gönderim denendikten sonra görünüyor ve yazarken canlı güncelleniyor; başarısız gönderimde odak ilk hatalı alana taşınıyor; durum mesajı için sayfa yüklenirken zaten var olan bir `role="status"` bölgesi kullanılıyor; tablo `caption` ve `scope` ile işaretlenmiş; süsleme görselinde `alt=""` var; e-posta alanında `type="email"` + `autoComplete="email"`, TC alanında `inputMode="numeric"` kullanılıyor. Aşağıdaki bulgular bu iyi tabanın üzerinde kalan eksikler.

Toplam **11 bulgu**: 1 Yüksek, 5 Orta, 5 Düşük.

---

## Bulgular

### 1. Hata özeti "aşağıda" diyor, ama durum bölgesi alanların altında — `FixedForm.tsx:42`, `FixedForm.tsx:101`
**Önem:** Orta
**Sorun:** Gönderim başarısız olunca `setStatus('Kayıt yapılamadı: aşağıda işaretli alanları düzeltin.')` yazılıyor (satır 42), fakat bu metni gösteren `<p role="status">` formun en altında, düğmelerin altında render ediliyor (satır 101). Hatalı alanlar mesajın **üstünde**. Yön kelimesi yanlış; ilk kez form dolduran bir veli "aşağıda" bir şey aramaya çalışabilir. Ayrıca odak ilk hatalı alana (yukarıya) gidince mobilde mesaj ekran dışında kalabilir.
**Öneri:** Ya durum bölgesini formun üstüne (başlık ile ilk alan arasına) taşıyın ve metni "aşağıda işaretli alanları" olarak bırakın, ya da metni "işaretli alanları düzeltin" / "yukarıdaki alanları" biçiminde yön bilgisi doğru olacak şekilde değiştirin. Hata sayısını eklemek de yardımcı olur: "2 alanda hata var".

### 2. Gönderim sırasında bekleme durumu yok; başarıdan sonra form yeniden gönderilebilir — `FixedForm.tsx:37-47`, `FixedForm.tsx:97`
**Önem:** Yüksek
**Sorun:** `onSubmit` senkron çalışıyor, hiçbir ağ isteği/bekleme yok ve "Kayıt alındı. Onay e-postası gönderildi." mesajı doğrudan yazılıyor (satır 46). "Kaydet" düğmesi hiç devre dışı kalmıyor; form dolu ve düzenlenebilir kalıyor. Mobilde çift dokunma ya da "acaba gitti mi?" refleksiyle ikinci dokunuş aynı kaydı tekrar gönderir. Gerçek gönderim eklendiğinde bu iskelet aynen kalırsa, kullanıcı hiçbir geri bildirim almadan bekler.
**Öneri:** `pending` durumu ekleyin: gönderim sırasında `<button type="submit" disabled={pending} aria-busy={pending}>Kaydediliyor…</button>`; başarıda formu bir onay görünümüyle değiştirin (veya alanları temizleyip `submitted`'ı sıfırlayın) ve odağı onay başlığına taşıyın. Başarı mesajında bir sonraki adımı söyleyin ("E-postanızı kontrol edin; onay bağlantısı 10 dk içinde gelir").

### 3. Aynı hata metni ikinci kez duyurulmaz — `FixedForm.tsx:40-44`, `FixedForm.tsx:101`
**Önem:** Düşük
**Sorun:** Kullanıcı hatayı düzeltmeden tekrar "Kaydet"e basarsa `setStatus` aynı string'i yazar; DOM içeriği değişmediği için `aria-live` bölgesi yeniden duyurmaz. Ekran okuyucu kullanıcısı gönderimin işlenmediğini sanabilir (odak yine ilk hatalı alana gidiyor, bu kısmen telafi ediyor).
**Öneri:** Her gönderimde önce `setStatus('')` sonra bir sonraki tick'te mesajı yazın, ya da mesaja değişen bir bilgi ekleyin (hata sayısı: "3 alanda hata var").

### 4. Yıkıcı "Formu temizle" düğmesi ana eylemin hemen yanında — `FixedForm.tsx:96-100`
**Önem:** Orta
**Sorun:** Üç eylem yan yana: **Kaydet** — **Formu temizle** — **İptal**. Yıkıcı eylem ortada, ana eylemin bitişiğinde. Mobilde başparmakla yanlış dokunma olasılığı yüksek; `confirm()` koruması var ama ilk kez kullanan bir veli için ekstra bir engel ve stres kaynağı. Formda yalnız 4 alan var; "temizle" düğmesinin sağladığı fayda düşük.
**Öneri:** Reset düğmesini kaldırın (4 alan için gerekli değil). Kalması gerekiyorsa görsel olarak ikincil/metin düğmesi yapın ve ana eylemden ayırın (örn. en sona, ayrı satıra).

### 5. Düğme metninde emoji ekran okuyucuya okunuyor — `FixedForm.tsx:98`
**Önem:** Düşük
**Sorun:** `🗑 Formu temizle` — emoji, etiketin bir parçası olarak "çöp kutusu" (ya da İngilizce "wastebasket") diye seslendirilir; düğme adı gürültülü olur.
**Öneri:** `<span aria-hidden="true">🗑 </span>Formu temizle` ya da emojiyi tamamen kaldırın. (Satır 69'daki `⚠` için bu zaten doğru yapılmış.)

### 6. Yıldız işareti seslendiriliyor ve tüm alanlar zorunluyken açıklama fazlalık — `FixedForm.tsx:65`, `FixedForm.tsx:81`
**Önem:** Düşük
**Sorun:** `{label} *` (satır 65) — yıldız düz metin olduğu için ekran okuyucu her etikette "yıldız" der; kontrol zaten `required` + `aria-required` taşıyor, yani "zorunlu" bilgisi iki kez aktarılıyor. Ayrıca formdaki **tüm** alanlar zorunlu; "Yıldızla (*) işaretli alanlar zorunludur." (satır 81) cümlesi ayrım yapmayan bir kural anlatıyor.
**Öneri:** Yıldızı `<span aria-hidden="true"> *</span>` içine alın; açıklamayı "Tüm alanlar zorunludur." olarak sadeleştirin (yıldızları da kaldırabilirsiniz).

### 7. TC alanında `maxLength` sessizce kesiyor; boşluklu yapıştırma yanıltıcı hata veriyor — `FixedForm.tsx:87`, `FixedForm.tsx:17`
**Önem:** Orta
**Sorun:** `maxLength={11}` fazla karakteri sessizce atar. Veli TC'yi "123 456 789 01" biçiminde (11 rakam + boşluk) yapıştırırsa 11 karakter kalır, bazıları boşluk; hata "TC Kimlik No 11 rakamdan oluşmalıdır" der — oysa kullanıcı 11 rakam girmiştir. İpucu "boşluksuz" diyor ama sorunu önlemiyor. Ayrıca doğrulama yalnız uzunluğa bakıyor; TC Kimlik No'nun kontrol basamağı algoritması var, yazım hatası ancak sunucuda yakalanır.
**Öneri:** `onChange` içinde rakam dışını süzün: `value.replace(/\D/g, '').slice(0, 11)`; `maxLength`'i kaldırın ya da yalnız güvenlik ağı olarak bırakın. İyileştirme olarak TC kontrol basamağı doğrulamasını ekleyin ("TC Kimlik No geçersiz görünüyor, lütfen kontrol edin").

### 8. Ad alanında `autoComplete="off"` — `FixedForm.tsx:85`
**Önem:** Düşük
**Sorun:** Tarayıcılar `autocomplete="off"`'u çoğunlukla yok sayar; ayrıca öğrencinin adı için otomatik tamamlama veri kaynağı zaten yok. Mobilde daha faydalı olan `autoCapitalize` ayarı yok — klavye ilk harfi büyük yapmayabilir ("ayşe yılmaz").
**Öneri:** `autoComplete="off"` yerine `autoCapitalize="words"` ekleyin. (Bu, kullanıcının kendi bilgisi olmadığı için WCAG 1.3.5 kapsamına girmez; UX iyileştirmesi.)

### 9. Seçim alanı için `disabled` placeholder seçeneği kontrol edilen değeri taşıyor — `FixedForm.tsx:89-93`
**Önem:** Düşük
**Sorun:** `<option value="" disabled>Sınıf seçin</option>` — kontrol edilen `value=""` bir `disabled` seçeneğe denk geliyor. Güncel tarayıcılarda başlangıçta görünür, ama kullanıcı bir sınıf seçtikten sonra listede placeholder'a geri dönemez (istenen davranış olabilir) ve bazı mobil seçici (picker) uygulamalarında devre dışı seçenek beklenmedik görünebilir.
**Öneri:** Daha dayanıklı çözüm: placeholder'ı `disabled` yapmayıp `hidden` ile birleştirmek, veya seçim listesini ikiden fazla seçenek yoksa radyo düğmelerine çevirmek (5. / 6. sınıf — iki radyo, mobilde tek dokunuşla seçilir, picker açılmaz).

### 10. Sayfa akışı: sınav notları tablosu bu sayfaya ait değil; kayıt koşulları formdan sonra ve onaysız — `FixedForm.tsx:104-118`
**Önem:** Orta
**Sorun:** (a) "Son sınav notları" tablosu (satır 106-113) ilk kez kayıt yapan veli için anlamsız — henüz öğrenci yok, "kimin notu?" sorusu doğar; formun ilk kez kullanan kişi için tek odak olması gerekir. (b) "Kayıt koşulları" (satır 115-118) formun **altında**; kullanıcı koşulları görmeden "Kaydet"e basabilir. Formda koşulları okuduğunu/kabul ettiğini belirten bir kontrol yok. (c) Reşit olmayan bir çocuğun TC Kimlik No'su toplanıyor; sayfada neden istendiğine ve nasıl korunacağına dair tek satır yok (KVKK aydınlatma bağlantısı). Bu ilk kez gelen velide güven sorunu yaratır. (Bu madde içerik/hukuki UX; WCAG maddesi değil.)
**Öneri:** Notlar tablosunu bu sayfadan kaldırın. Koşulları formun üstüne taşıyın ya da formun içine "Kayıt koşullarını okudum ve kabul ediyorum" onay kutusu + bağlantı ekleyin. TC alanının yanına kısa bir amaç açıklaması ve KVKK aydınlatma metni bağlantısı koyun.

### 11. İptal bağlantısı düğme grubunda — klavye davranışı farklı — `FixedForm.tsx:99`
**Önem:** Düşük
**Sorun:** `<a href="/">İptal</a>` iki `<button>` arasında/yanında. Gezinme yaptığı için bağlantı olması doğru, ama klavyede Space ile tetiklenmez ve ekran okuyucu "bağlantı" der; düğme gibi stillendiyse kullanıcı beklentisi karışır. Ayrıca `dirty` boşken hiç uyarı vermeden ana sayfaya gider (bu doğru).
**Öneri:** Bağlantı olarak kalsın ama görsel olarak metin bağlantısı gibi görünsün (düğme taklidi yapmasın); ya da düğme yapılıp `navigate('/')` ile yönlendirilsin. Yıkıcı reset kaldırılırsa (bulgu 4) iki eylem kalır ve karışıklık azalır.

---

## Kaynaktan doğrulanamayan noktalar (CSS/render gerekir)

Bunlar bulgu değil; render edildiğinde kontrol edilmesi gereken maddeler:

- **Renk kontrastı:** `.hint`, `.error`, `.badge`, `.status`, `.cancel` sınıflarının renkleri bilinmiyor. Satır 80'deki inline `#4a4a4a` / `#fff` çifti ~9:1 ile yeterli. Hata rengi + `⚠` simgesi birlikte olduğu için hata yalnız renge bağlı değil (iyi).
- **Dokunma hedefi boyutu:** Üç eylem yan yana (satır 96-100); mobilde her birinin en az 24×24 CSS px (WCAG 2.5.8), tercihen 44×44 olması ve aralarında boşluk bulunması gerekir.
- **Odak görünürlüğü:** `:focus-visible` stilleri bilinmiyor; özellikle satır 43'te programatik odak sonrası hatalı alanın belirgin olması gerekir.
- **Görsel taşması:** Satır 78'deki görsel sabit `width={320}`; 320-360 px genişlikteki telefonlarda kenar boşluklarıyla birlikte yatay kaydırmaya yol açabilir. CSS'te `max-width:100%; height:auto` olduğundan emin olun.
- **Alan yerleşimi:** `field()` fragment döndürüyor (satır 64-70); label/kontrol/hata'nın dikey yığılması ve aralıkları CSS'e bağlı.
- **Yerel `confirm()` diyalogları** (satır 50, 56): Erişilebilir ve odak yönetimi tarayıcıya ait, ancak düğme etiketleri cihaz diline göre gelir ("OK/Cancel"); markalı bir diyalog isteniyorsa özel modal gerekir. Tek başına kusur değil.

## Doğru yapılan ve kusur olarak işaretlenmeyen noktalar

- Odağın ilk hatalı alana taşınması + `aria-describedby` ile hatanın okunması (satır 43, 66-69).
- Hata görünürken ipucunun gizlenmesi (satır 68) — hata metni format bilgisini içeriyor.
- `aria-invalid="false"` render edilmesi zararsız.
- `required` + `aria-required` tekrarı zararsız.
- `React.ChangeEvent` tip konumunda `import` olmadan kullanılması TS'te geçerlidir (UMD tip erişimi).

---

**Kısa özet:**
- 11 bulgu: 1 yüksek, 5 orta, 5 düşük. Temel erişilebilirlik altyapısı sağlam.
- En önemli: gönderimde bekleme/çift gönderim koruması yok (satır 37-47).
- Hata özeti "aşağıda" diyor ama alanlar mesajın üstünde (satır 42/101).
- Yıkıcı "Formu temizle" düğmesi ana eylemin dibinde; emoji seslendiriliyor (satır 98).
- Sayfa akışı: alakasız notlar tablosu, koşullar formdan sonra, TC için KVKK/amaç açıklaması yok (satır 104-118).