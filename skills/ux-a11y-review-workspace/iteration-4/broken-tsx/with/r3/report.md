## BrokenForm.tsx  ·  Kullanıcılar: veliler — mobil, ilk kez kullanan, seyrek (kayıt döneminde ~1 kez)  ·  Dil: Türkçe  ·  **Statik denetim (render yok)**

Bağlam notu: Proje dosyası yalnız `BrokenForm.tsx`; kullanıcı grubu ve dil istekte verildi. Seyrek ve ilk kez kullanan mobil veli profili demek: H7 (uzman kısayolu) ikincil, H5/H9 (hata önleme ve kurtarma), kalıcı etiket ve ≥ 24 px (tercihen 44 px) dokunma hedefi birincil öncelik.

### Bulgular (şiddete göre)

BrokenForm.tsx:17 — A7 · WCAG 2.1.1 · 4.1.2 · şiddet 4 — "Kaydet" bir `div` + `onClick`; klavye ve ekran okuyucu için ulaşılamaz ve adsız; ayrıca hiçbir `<form>` yok, bu yüzden Enter / mobil klavyedeki "Git" tuşu da gönderemez → alanları `<form onSubmit={…}>` içine al, Kaydet'i `<button type="submit">Kaydı gönder</button>` yap (`.fake-btn` sınıfını butona taşı).

BrokenForm.tsx:17 — U1 · H1 · şiddet 4 — Kaydet'in `onClick={() => {}}` gövdesi boş: gönderim ne mesaj, ne yönlendirme, ne bekleme göstergesi üretir; veli kaydın alındığını bilemez → gönderim sırasında "Kaydediliyor…", sonra `role="status"` bölgesinde "Kayıt alındı. Onay e-postası gönderildi." ya da "Kayıt yapılamadı: kimlik numarası alanını düzeltin." göster.

BrokenForm.tsx:17 — A13 · WCAG 4.1.3 · şiddet 3 — Dosyada tek bir `aria-live` / `role="status"` bölgesi yok; Kaydet (:17) ve temizle (:18) durum değiştirir ama ekran okuyucuya hiçbir şey duyurulmaz → formun altına kalıcı `<p role="status" aria-live="polite">` ekle, gönderim ve temizleme sonuçlarını buraya yaz.

BrokenForm.tsx:9 — A4 · WCAG 1.3.1 · 3.3.2 · şiddet 3 — Dört form denetimi (:9 Ad Soyad, :10 E-posta, :11 TC Kimlik No, :12 Sınıf) programatik etikete bağlı değil; yalnız placeholder / devre dışı ilk seçenek var → her alana `id` ve kalıcı `<label htmlFor="adSoyad">Ad Soyad *</label>` ekle; select için `<label htmlFor="sinif">Sınıf</label>` (1.3.5 için ayrıca `autoComplete="name"` ve `autoComplete="email"` ver).

BrokenForm.tsx:9 — U7 · H6 · şiddet 3 — Placeholder etiket yerine kullanılmış (:9–:11); veli yazmaya başlayınca alan adı kaybolur, ilk kez dolduran bir veli için "hangi kutuya ne yazdım" sorusu doğar → etiketleri kalıcı yap (yukarıdaki A4 düzeltmesi), placeholder'ı yalnız örnek için kullan (`placeholder="örn. 12345678901"`).

BrokenForm.tsx:11 — U3 · H5 · H10 · şiddet 3 — TC Kimlik No `type="text"`; `inputMode`, `maxLength`, format ipucu ve hata metni yok; mobilde harf klavyesi açılır, 11 rakam kuralı hiçbir yerde söylenmiyor (3.3.3 hata önerisi de yok) → `inputMode="numeric" pattern="[0-9]{11}" maxLength={11}`, etiket altına "11 rakam, örn. 12345678901" ipucu; hata metni: "Kimlik numarası 11 rakam olmalı (örn. 12345678901)" ve `aria-describedby` ile alana bağla.

BrokenForm.tsx:11 — A5 · WCAG 1.4.1 · 3.3.1 · şiddet 3 — Zorunluluk (ve/veya hata) tek sinyalle, kırmızı kenarlıkla verilmiş; `aria-invalid`, ikon, metin yok; renk körü veya ekran okuyucu kullanan veli hiçbir şey algılamaz → zorunluluk için etikette `*` + `required`; hata için kırmızı kenarlık **+** ikon **+** alan altında metin, `aria-invalid="true" aria-describedby="tc-hata"`.

BrokenForm.tsx:7 — U4 · H4 · şiddet 3 — Yönerge kendi içinde çelişik: "tüm alanları doldurun" (hepsi zorunlu) ile "zorunlu alanlar kırmızı ile işaretlidir" (yalnız :11 kırmızı); üstelik kırmızı kenarlık web'de hata sinyalidir, zorunlu işareti değil (1.3.3: yönerge yalnız renge dayanıyor) → yönergeyi "* ile işaretli alanlar zorunludur" yap, zorunlu alanların etiketine `*` ekle, kırmızı kenarlığı yalnız gerçek hata durumunda göster.

BrokenForm.tsx:6 — A3 · WCAG 1.4.3 · şiddet 3 — Yönerge metni `#9a9a9a` / `#fff` ≈ 2.8:1; küçük metin için 4.5:1 gerekir, güneş altında telefon ekranında okunmaz → metin rengini en az `#767676` (4.5:1) yap; yönerge metni önemliyse `#595959` tercih et.

BrokenForm.tsx:12 — A6 · WCAG 2.4.7 · 2.4.11 · şiddet 3 — `select`'te `outline: 'none'` satır içi verilmiş, yerine eşdeğer gösterge yok; klavye kullanıcısı odağın nerede olduğunu görmez → inline outline kaldırmayı sil; `:focus-visible { outline: 3px solid <marka rengi>; outline-offset: 2px }` ile ≥ 3:1 gösterge ver.

BrokenForm.tsx:18 — A8 · WCAG 4.1.2 · 2.5.3 · şiddet 3 — Yalnız 🗑 emojisi taşıyan butonun Türkçe erişilebilir adı yok; ekran okuyucu "wastebasket" ya da hiçbir şey okur → `aria-label="Formu temizle"` ekle (ya da görünür metin "Formu temizle" + ikon).

BrokenForm.tsx:18 — U5 · H3 · şiddet 3 — 🗑 tıklanınca tüm alanlar onaysız ve geri alınamaz silinir (3.3.4); :19'daki `href="#sil"` linki de adıyla yıkıcı bir eylem ima ediyor ama ne yaptığı belirsiz → temizlemeden önce onay iste ("Girdiğiniz bilgiler silinsin mi?") ya da 5–10 sn "Geri al" penceresi ver; `#sil` linkinin eylemini adlandır veya kaldır.

BrokenForm.tsx:19 — A9 · WCAG 2.5.8 · şiddet 3 — "x" linki `display: inline-block`, 16×16 px, 10 px yazı; satır içi metin linki istisnası uygulanmaz; mobilde parmakla vurulamaz → en az 24×24 px (dokunma için 44×44 px öner) ve okunabilir yazı boyutu ver.

BrokenForm.tsx:27 — U8 · H2 · şiddet 2 — Link metni "buraya tıklayın" hedefi söylemez (2.4.4); :19'daki "x" de anlamsız ad → "Kayıt koşullarını görüntüle" / "Kayıt ayrıntılarını gör" gibi hedefi arayüz dilinde söyleyen metin; "x" için "Kapat" ya da eylemine göre "Kaydı sil".

BrokenForm.tsx:17 — U2 · H3 · şiddet 2 — Akıştan çıkış yolu yok: İptal / Geri butonu bulunmuyor; yarım veri varken sayfadan çıkışa uyarı da yok → Kaydet'in yanına ikincil "İptal" (önceki sayfaya) ekle; alanlar doluysa `beforeunload` ile "Girdiğiniz bilgiler kaybolacak" uyarısı ver.

BrokenForm.tsx:4 — A1 · WCAG 1.3.1 · 2.4.6 · şiddet 2 — Sayfa başlığı stil verilmiş `div`; `h1` yok, dolayısıyla başlık hiyerarşisi yok (`main` landmark ve atlama linki sayfa düzeyinde: doğrulanamaz) → `<h1>Öğrenci Kayıt</h1>` yap, stili CSS ile ver; bileşen bir `main` içine yerleştiğinden emin ol.

BrokenForm.tsx:20 — U6 · H8 · şiddet 2 — "Yeni!" rozeti hiçbir içeriğe bağlı değil; dikkati çeker ama neyi anlattığını söylemez; `aria-hidden="false"` etkisizdir (varsayılan) → rozeti bir içeriğe bağla ("Yeni: 2026 kayıt takvimi yayınlandı") ya da kaldır; `aria-hidden="false"` özniteliğini sil.

BrokenForm.tsx:21 — A11 · WCAG 1.3.1 · şiddet 2 — Not tablosunda `caption` ve `th` yok; 2×2 olduğu için axe yakalamaz, ekran okuyucu "Matematik 85" ilişkisini kuramaz → `<caption>Deneme sınavı notları</caption>`, ilk satır `<th scope="col">Ders</th><th scope="col">Puan</th>`, ders adları `<th scope="row">`.

BrokenForm.tsx:5 — A2 · WCAG 1.1.1 · şiddet 2 — `img` `alt` özniteliği taşımıyor; ekran okuyucu dosya URL'sini okur → görsel süs ise `alt=""`; okul fotoğrafı gibi bilgi taşıyorsa "X Okulu ana binası" gibi anlamlı `alt`.

### Kontrol listesi hükümleri
A1 ihlal :4 · A2 ihlal :5 · A3 ihlal :6 · A4 ihlal :9 · A5 ihlal :11 · A6 ihlal :12 · A7 ihlal :17 · A8 ihlal :18 · A9 ihlal :19 · A10 doğrulanamaz (`.pulse` animasyonu CSS'te) · A11 ihlal :21 · A12 doğrulanamaz (`html lang` bileşen dışında) · A13 ihlal :17
U1 ihlal :17 · U2 ihlal :17 · U3 ihlal :11 · U4 ihlal :7 · U5 ihlal :18 · U6 ihlal :20 · U7 ihlal :9 · U8 ihlal :27

WCAG 2.2 AA tarama (36 kriter) — dosyada ilgili olanlar bulgulara işlendi: 1.3.3 (:7 yönerge yalnız renge dayanır), 1.3.5 (:9–:10 `autocomplete` yok), 2.4.4 (:19, :27), 3.3.3 (hata önerisi yok), 3.3.4 (:18 onaysız veri silme). 1.4.4, 1.4.10, 2.4.2 render / sayfa düzeyi gerektirir → İnsan TODO.

### Klavye gezintisi
render yok — statik denetim. Kaynaktan öngörülen Tab sırası: :9 → :10 → :11 → :12 → :18 (🗑) → :19 (x) → :27; **:17 Kaydet Tab ile ulaşılamaz** (div). :12'de odak göstergesi görünmez (`outline: none`). Enter ile gönderim mümkün değil (`form` yok).

### İnsan için TODO
- Ekran okuyucu (NVDA / VoiceOver, Android TalkBack — veli mobilde): alan adları, hata duyuruları, tablo başlıkları okunuyor mu; düzeltmeler sonrası `role="status"` mesajı duyuruluyor mu.
- %200 yakınlaştırma ve 320 px genişlikte içerik/işlev kaybı, yatay kaydırma var mı (1.4.4, 1.4.10); `<title>` sayfayı ve siteyi tanımlıyor mu (2.4.2).
- Gerçek kullanıcıyla 1 görev: ilk kez kayıt yapan bir veli, telefonda, yardımsız formu doldurup gönderebiliyor ve sonucu anlıyor mu.
- A10 doğrulanamaz: `.pulse` sınıfının CSS'ini kontrol et — 5 sn'den uzun sürekli hareketse durdurulabilir olsun, flaş içermesin, `prefers-reduced-motion` ile kapansın.
- A12 doğrulanamaz: kök şablonda `<html lang="tr">` var mı.
- A1 sayfa düzeyi: bileşen `main` landmark içinde mi; tekrarlayan üst blok varsa atlama linki var mı.
- A9 CSS'e bağlı: `.fake-btn` (Kaydet) ve `.icon-only` (🗑) hedef boyutu ≥ 24×24 px (mobil için 44×44) mü.
- A3 CSS'e bağlı: yönerge dışındaki metinlerin ve `.fake-btn` / `.pulse` renklerinin kontrastı.
