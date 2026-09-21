## broken.html  ·  Kullanıcılar: veliler — mobil, ilk kez, tek seferlik (kayıt yılda bir)  ·  Dil: Türkçe  ·  **Statik denetim — sayfa render edilemedi, yalnız kaynak incelendi**

Kaynak: `project/broken.html` (39 satır, tüm CSS/JS satır içi; harici dosya yok — bu yüzden "doğrulanamaz" hüküm gerekmedi).
Bağlam gerekçesi: kullanıcı grubu ve dil görevde verildi; `html lang="tr"` ve tüm metinler Türkçe bunu doğruluyor. Tekrar sıklığı çıkarım: öğrenci kaydı yılda bir yapılır → H7 (uzman kısayolu) düşük öncelik, **ilk kez + mobil** → etiket kalıcılığı, hedef boyutu, hata metni ve geri dönüş yolu yüksek öncelik.

### Bulgular (şiddete göre)

broken.html:28 — A7 · WCAG 2.1.1 · 4.1.2 · şiddet 4 — Ana eylem "Kaydet" bir `div` + `onclick`; klavye odağı almaz, ekran okuyucuya "buton" olarak bildirilmez, Enter/Space ile tetiklenmez. Ayrıca sayfada `<form>` ve `name` öznitelikleri yok: alanlar hiçbir yere gönderilemez, Enter tuşu formu göndermez → Alanları `<form>` içine al, her alana `name` ver, Kaydet'i `<button type="submit" class="fake-btn">Kaydet</button>` yap.

broken.html:28 — U1 · H1 · şiddet 4 — Kaydet'in tek sonucu `alert('kaydedildi')`: veri hiçbir yere gitmeden "kaydedildi" denir (yanlış onay), mesaj bağlamsız ve küçük harf, mobilde engelleyici modal → Gerçek gönderim sonrası sayfaya `role="status"` alanı ile "Kayıt alındı. Onay e-postası gönderildi." yaz ya da onay sayfasına yönlendir; gönderim sırasında "Kaydediliyor…" göster.

broken.html:20 — A4 · WCAG 1.3.1 · 3.3.2 · şiddet 3 — 20–23. satırlardaki dört form denetiminin (Ad Soyad, E-posta, TC Kimlik No, Sınıf) hiçbirinde programatik etiket yok; ekran okuyucu alanları "düzenleme kutusu" diye okur → Her alana kalıcı `<label for="ad">Ad Soyad</label>` + `id` ver; select için `<label for="sinif">Sınıf</label>`.

broken.html:20 — U7 · H6 · şiddet 3 — Etiket yerine placeholder kullanılmış (20–22); veli yazmaya başlayınca "TC Kimlik No" kaybolur, hangi alanda olduğunu hatırlamak zorunda kalır → Kalıcı etiket ekle; placeholder'ı yalnız örnek biçim için kullan ("örn. 12345678901").

broken.html:22 — U3 · H5 · H10 · şiddet 3 — TC Kimlik No alanı `type="text"`, `inputmode`/`maxlength`/`pattern` ve biçim ipucu yok; mobilde harf klavyesi açılır; hiçbir alanda hata metni mekanizması yok → `inputmode="numeric" maxlength="11" pattern="[0-9]{11}" autocomplete="off"` ver, etiket altına "11 rakam, örn. 12345678901" ipucu ekle; hata metnini "Kimlik numarası 11 rakam olmalı (örn. 12345678901)" biçiminde alan altına yaz.

broken.html:19 — U4 · H4 · şiddet 3 — Yönerge "tüm alanları doldurun" derken "zorunlu alanlar kırmızı ile işaretlidir" diyor (çelişki: hepsi zorunluysa neden biri işaretli?); kırmızı kenarlık (satır 22) evrensel olarak **hata** sinyalidir, burada **zorunlu** anlamında kullanılmış → Zorunlu için etiket sonuna `*` + form başına "* ile işaretli alanlar zorunludur"; kırmızı kenarlığı yalnız hata için, ikon + metinle birlikte kullan; yönergeyi gerçek durumla eşle.

broken.html:22 — A5 · WCAG 1.4.1 · 3.3.1 · şiddet 3 — Zorunlu/hata bilgisi yalnız renkle (`border:2px solid red`) taşınıyor; `aria-invalid`, `aria-describedby`, `required` yok; renk körü ya da ekran okuyucu kullanan veli bilgiyi almaz → `required` + `aria-required` ekle; hata durumunda `aria-invalid="true"` + `aria-describedby="tc-hata"` ile alan altında metin + ikon göster.

broken.html:19 — A3 · WCAG 1.4.3 · şiddet 3 — Yönerge metni `#9a9a9a` / `#fff` = **2,81:1** (gereken 4,5:1); satır 31 "Yeni!" rozeti `#fff` / `#e53e3e` = **4,13:1**, 16 px normal metin, ayrıca hareketli → Yönerge rengini en az `#767676` (4,54:1) ya da gövde rengi `#1a1a1a` yap; rozet arka planını `#c53030` (5,6:1) gibi koyulaştır.

broken.html:23 — A6 · WCAG 2.4.7 · şiddet 3 — `select` üzerinde `outline:none`, yerine eşdeğer gösterge yok; klavye kullanıcısı odağın nerede olduğunu görmez → `outline:none` kaldır ya da `select:focus-visible { outline: 3px solid #1a1a1a; outline-offset: 2px }` ekle (≥ 3:1).

broken.html:29 — A8 · WCAG 4.1.2 · 2.5.3 · şiddet 3 — Yalnız 🗑 emojisi taşıyan butonun erişilebilir adı yok; ekran okuyucu "çöp kutusu" ya da hiçbir şey okur; gerçek işlevi kaynaktan anlaşılmıyor → Butona gerçek işlevini söyleyen `aria-label` ver (ör. formu temizliyorsa "Formu temizle"); `type="button"` ekle.

broken.html:29 — U5 · H3 · şiddet 3 — 🗑 butonu ve satır 30'daki `#sil` bağlantısı yıkıcı görünüyor; ikisi de onay istemiyor, geri alma yok; ilk kez kullanan veli formu yanlışlıkla silebilir → Yıkıcı eylemden önce onay iletişim kutusu ("Girdiğiniz bilgiler silinsin mi?") ya da 5–10 sn "Geri al" penceresi ver.

broken.html:30 — A9 · WCAG 2.5.8 · şiddet 3 — `#sil` bağlantısı **16×16 px**, 10 px yazı; mobil velinin parmağıyla isabet ettiremeyeceği kadar küçük ve 🗑 ile Kaydet'e komşu → En az 24×24 (dokunma için 44×44 öner): `min-width:44px; min-height:44px; display:inline-flex; align-items:center; justify-content:center`.

broken.html:36 — U8 · H2 · WCAG 2.4.4 · şiddet 3 — "buraya tıklayın" hedefi söylemez; satır 30'daki "x" eylemi söylemez; her iki bağlantı (`#detay`, `#sil`) sayfada olmayan id'lere gider (hedef yok) → Metinleri hedefe göre yaz: "Kayıt koşullarını görüntüle" / "Girilenleri sil"; bağlantıları var olan hedeflere bağla ya da eylem ise `button` yap.

broken.html:17 — A1 · WCAG 1.3.1 · 2.4.6 · şiddet 3 — Sayfa başlığı stilli `div`; `h1` ve `main` landmark yok; ekran okuyucu başlık listesi boş → `<h1>Öğrenci Kayıt</h1>` yap (28 px/700 stilini koru), içeriği `<main>` içine al. Atlama linki: sayfada tekrarlayan gezinme bloğu olmadığı için bu dosyada gerekli değil.

broken.html:18 — WCAG 1.4.10 (tarama) · şiddet 3 — `img width=320` + gövde `padding:24px` iki yanda = 368 px; 320 px genişlikte yatay kaydırma oluşur (mobil veliler için birincil cihaz) → `img { max-width:100%; height:auto }`.

broken.html:18 — A2 · WCAG 1.1.1 · şiddet 2 — Görselde `alt` yok; ekran okuyucu URL'yi ("picsum.photos/seed/okul…") okur → Süs görseliyse `alt=""`; okul logosu/afiş gibi bilgi taşıyorsa anlamlı `alt` ("Okul binası").

broken.html:12 — A10 · WCAG 2.2.2 · şiddet 2 — `.pulse` animasyonu `infinite`, 5 sn'den uzun sürer, durdurma yolu yok, `prefers-reduced-motion` yok (flaş yok, 2.3.1 uygun) → Animasyonu 5 sn içinde bitir (`animation: pulse 1s 3`) ya da tamamen kaldır; `@media (prefers-reduced-motion: reduce) { .pulse { animation:none } }`.

broken.html:31 — U6 · H8 · şiddet 2 — "Yeni!" rozeti hiçbir içeriğe bağlı değil; ne yeni belli değil, sürekli titreşerek dikkat çeker → Rozeti bir içeriğe bağla ("Yeni: 2026–27 kayıt takvimi yayınlandı") ya da kaldır.

broken.html:32 — A11 · WCAG 1.3.1 · şiddet 2 — 2×2 not tablosunda `caption` ve `th scope` yok; ekran okuyucu "Matematik 85"i başlıksız okur; küçük tablo axe'ten kaçar → `<caption>Ara sınav notları</caption>`, `<tr><th scope="col">Ders</th><th scope="col">Not</th></tr>`, ders adlarını `th scope="row"` yap.

broken.html:28 — A13 · WCAG 4.1.3 · şiddet 2 — Sayfada hiçbir canlı bölge yok; doğrulama/sonuç için `role="status"`/`aria-live` alanı bulunmuyor; tek geri bildirim engelleyici `alert()` (ekran okuyucu duyurur ama odağı çalar ve mobilde akışı keser) → Formun üstüne boş `<p role="status" id="durum"></p>` koy; gönderim sonucu ve hata özetini buraya yaz.

broken.html:28 — U2 · H3 · şiddet 2 — Kayıt akışında İptal/Geri yolu yok; yarım veri varken çıkışta uyarı yok → Kaydet'in yanına "Vazgeç" (ikincil buton, kayıt listesine döner) ekle; alanlar doluysa `beforeunload` uyarısı ver.

broken.html:20 — WCAG 1.3.5 (tarama) · şiddet 2 — Ad Soyad ve E-posta alanlarında `autocomplete` yok; mobil velinin tarayıcı otomatik doldurması çalışmaz → `autocomplete="name"` (satır 20), `autocomplete="email"` (satır 21).

broken.html:29 — WCAG 3.2.4 (tarama) · şiddet 2 — Aynı yıkıcı eylem iki farklı biçimde görünüyor: 🗑 butonu (29) ve "x" bağlantısı `#sil` (30) → Tek bir denetim bırak, adı ve görünümü tutarlı olsun.

broken.html:6 — WCAG 2.4.2 (tarama) · şiddet 1 — `<title>` geliştirici notu taşıyor ("(hatalı, düz HTML)") ve site adı yok → "Öğrenci Kayıt — <Okul/Kurum adı>".

### Kontrol listesi hükümleri
A1 ihlal :17 · A2 ihlal :18 · A3 ihlal :19 · A4 ihlal :20 · A5 ihlal :22 · A6 ihlal :23 · A7 ihlal :28 · A8 ihlal :29 · A9 ihlal :30 · A10 ihlal :12 · A11 ihlal :32 · A12 uygun (`html lang="tr"`, tüm içerik Türkçe, dil değişen parça yok) · A13 ihlal :28 · U1 ihlal :28 · U2 ihlal :28 · U3 ihlal :22 · U4 ihlal :19 · U5 ihlal :29 · U6 ihlal :31 · U7 ihlal :20 · U8 ihlal :36

WCAG 2.2 tarama (36 kriter) — dosyada ilgili bulunanlar: 1.4.10 (:18), 1.3.5 (:20), 3.2.4 (:29), 2.4.2 (:6) yukarıda Bulgular'da. Geçilenler: 1.2.x ses/video yok; 1.3.4 yön kilidi yok; 2.1.4 kısayol yok; 2.2.1 zaman sınırı yok; 2.5.2 eylem `click`'te; 3.2.1/3.2.2 odak-girdi bağlam değişimi yok; 3.3.7/3.3.8 tek adım, kimlik doğrulama yok; 2.4.5/3.2.3/3.2.6 site düzeyi — tek dosyada değerlendirilemez.

### Klavye gezintisi
render yok — statik denetim. Kaynaktan türetilen beklenen Tab sırası (tarayıcıda doğrulanmadı): Ad Soyad (20) → E-posta (21) → TC Kimlik No (22) → Sınıf (23, odak görünmez) → 🗑 (29) → x (30) → buraya tıklayın (36). **Kaydet (28) hiç odak almaz** — ana görev klavyeyle tamamlanamaz. Odak sırası görsel sırayla örtüşüyor ancak 28 atlanır; 23'te odak görsel olarak kaybolur.

### İnsan için TODO
- Ekran okuyucu (NVDA/VoiceOver, mobilde TalkBack): alanların adsız okunduğunu, 🗑'in ne duyurulduğunu, `alert()` sonrası odağın nereye döndüğünü, tablonun başlıksız okunduğunu doğrula.
- %200 yakınlaştırma ve 320 px genişlik: satır 18 görselinin yatay kaydırma yaratıp yaratmadığını, 640 px `max-width` gövdenin daralmasını ve 28 px başlığın kırılmasını kontrol et.
- Hedef boyutu ölçümü: satır 29 🗑 butonunun render boyutu tarayıcı varsayılan padding/line-height'ına bağlı (kaynaktan ölçülemedi); 24×24 altındaysa A9'a ekle.
- Gerçek kullanıcıyla 1 görev: ilk kez kullanan bir veli, telefonda yardımsız "çocuğunu 5. sınıfa kaydet" görevini tamamlayabiliyor mu? Özellikle TC Kimlik alanında klavye tipi, kırmızı kenarlığın "hata" olarak yorumlanması ve Kaydet sonrası "kaydedildi" mesajına güven gözlemlenmeli.