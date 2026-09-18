## home.before.html (W3C WAI "Before and After Demo" — CityLights, *inaccessible* sürüm)  ·  Kullanıcılar: şehir sakinleri ve ziyaretçiler — mobil + masaüstü, karışık deneyim, seyrek ziyaret (haber/etkinlik/bilet)  ·  Dil: İngilizce

Render: https://www.w3.org/WAI/demos/bad/before/home.html · Kaynak: 2026-09-18'de indirilen sayfa (W3C WAI BAD demo, 2012; W3C Document License), 389 satır, `#page` içi denetlendi (satır 168–363); W3C'nin demo çerçevesi (`#meta-header`, `#meta-footer`, Piwik) kapsam dışı.
Bağlam notu: projede CLAUDE.md/README yok; kullanıcı grubu sayfa içeriğinden çıkarıldı (portal, "visitors and residents"). Seyrek ziyaret → H7 ağırlıksız; karışık cihaz → hedef boyutu ve odak öncelikli.

### Bulgular (şiddete göre)

**Şiddet 4 — yayın engelleyici**

home.before.html:248,254,260,266,280-282,292-294,298,318,339 — A7 · A6 · WCAG 2.1.1 · 2.4.7 · şiddet 4 — Demo alanındaki **14 linkin hepsinde** `onfocus="blur();"`: klavye odağı linke gelir gelmez düşürülüyor. **Tarayıcıda doğrulandı (focusin/focusout günlüğü, 16 Tab):** Tab → logo → QUICKMENU → sonraki 14 Tab'ın her biri bir linke odak verir ve `blur()` anında düşürür (`focusout` ×14, kalıcı `focusin` yok; `activeElement` sürekli `<body>`). Odak görünmez ilerler; kullanıcı hiçbir şey görmez, Enter hiçbir şeyi açmaz. Klavye kullanıcısı ana navigasyona, haberlere, "Read More" ve "Click here" linklerine **hiç ulaşamaz** → `onfocus="blur();"` özniteliklerini kaldır; odağı görünür bırak.

home.before.html:248,254,260,266 — A2 · A8 · WCAG 1.1.1 · 4.1.2 · şiddet 4 — Sol navigasyonun 4 linki (Home, News, Tickets, Survey) yalnız `alt`'sız görsel taşıyor (`<img name="nav_home" src=…>` — `alt` yok); linkin erişilebilir adı boş → ekran okuyucu "link, nav_home.gif" der → her görsele `alt="Home"`, `alt="News"`… ver; tercihen metin link + CSS.

home.before.html:248,254,260,266 — A7 · WCAG 4.1.2 · şiddet 3 — Aynı linkler `href="javascript:location.href='home.html';"`: gerçek URL yok → orta tık / yeni sekme / JS kapalı çalışmaz; hover için `onMouseOver` görsel değişimi klavyede yok → `href="home.html"`; hover/focus stilini CSS `:hover, :focus-visible` ile ver.

home.before.html:187-204 — U1 · A4 · WCAG 3.2.2 · 3.3.2 · şiddet 4 — QUICKMENU `<select onchange="location.href=this.value">`: klavyede ok tuşuyla seçenek değiştirmek **anında** başka siteye yönlendirir (kullanıcı listeyi tarayamaz), onay/geri bildirim yok; etiket yok — `<option selected>QUICKMENU ----&gt;` placeholder olarak etiket yerine kullanılıyor → `<label for="quickmenu">Şehir hizmetleri</label>` ekle; yönlendirmeyi `onchange` yerine yanındaki "Git" düğmesine bağla.

**Şiddet 3 — önemli**

home.before.html:275,297 — A1 · WCAG 1.3.1 · 2.4.6 · şiddet 3 — "Welcome to CityLights" ve "Elsewhere on the Web" `<p class="headline">` / `<p class="subheadline">`; demo alanında hiç `h1–h6` yok; `main` landmark yok; tüm yerleşim iç içe `<TABLE>` (:170–362) → `<main>` + `<h1>Welcome to CityLights</h1>`, `<h2>` alt başlıklar; yerleşim tablolarını CSS grid/flex ile değiştir (geçiş döneminde `role="presentation"`).

home.before.html:286-288 — A2 · WCAG 1.1.1 · şiddet 3 — Üç haber görseli CSS `background: url(…)` ile `div`'de, `title="image"`; ekran okuyucu ve görsel-kapalı kullanıcı için içerik yok → `<img alt="Güneş şapkalı adam…">` gibi gerçek `img` + anlamlı `alt`; ya da haberle ilişkili süs ise `alt=""`.

home.before.html:184,312,333 — A2 · WCAG 1.1.1 · şiddet 3 — Hava durumu görseli (:184), "Free Penguins" ve "More City Parks" teaser görselleri (:312, :333) `alt`'sız; hava durumu **bilgi** taşır → `alt="Güneşli, 23°C"`; teaser görselleri bağlama göre `alt` ya da `alt=""`.

home.before.html:298 — A2 · WCAG 1.1.1 · şiddet 3 — Telefon numarası görsel olarak (`telefon_white_bg.gif`, `alt="1234 56789"`): `alt` var ama numara kopyalanamaz, büyütülemez, `tel:` linki olamaz → düz metin `<a href="tel:123456789">1234 56789</a>`.

home.before.html:292-294 — A8 · WCAG 4.1.2 · 2.4.4 · şiddet 3 — Üç "MORE" linkinin tek içeriği `alt=""` görsel → link adı **boş**; ekran okuyucu "link" der → `alt="Devamını oku: Heat wave…"` ya da görünür metin "Read more about the heat wave".

home.before.html:298,318,339 — U8 · H2 · WCAG 2.4.4 · şiddet 3 — "Click here" ×2, "Read More..." ×2: bağlam dışı okunduğunda hedef belirsiz; "Click here" ayrıca dokunmatikte anlamsız → "Killer bee safety guide (external)", "Read the full penguin story".

home.before.html:298 — U1 · WCAG 3.2.5 · şiddet 3 — İki dış link `target="_blank"` ile uyarısız yeni pencere açıyor; geri düğmesi çalışmaz, ekran okuyucu bağlam kaybeder → aynı pencerede aç ya da metne "(yeni sekmede açılır)" + ikon ekle.

home.before.html:309,330 — A3 · WCAG 1.4.3 · şiddet 3 — Teaser başlıkları `#41545D` / `#A9B8BF` = **3.88:1**; Verdana size=2 (~13 px) kalın → "büyük metin" değil, sınır 4.5:1 → arka planı `#8FA3AB`'ye açmak yerine metni `#2B3A41` yap (≥ 5.5:1).

home.before.html:1 — A12 · WCAG 3.1.1 · şiddet 3 — `<HTML>` üzerinde `lang` yok → ekran okuyucu telaffuz tablosunu seçemez → `<html lang="en">`.

**Şiddet 2 — küçük**

home.before.html:143 — U6 · H8 · şiddet 2 — `<NOSCRIPT><B><FONT COLOR=RED>This page uses scripts!!!</FONT></B></NOSCRIPT>` — neyin çalışmadığını, ne yapılacağını söylemeyen bağlamsız kırmızı uyarı → "Some features (weather, quick menu) need JavaScript. All content is available below." ya da JS gerektirmeyen alternatif.

home.before.html:215-227 — A13 · U1 · şiddet 2 — Tarih/hava `document.write` + `document.all` (IE'ye özgü) ile yazılıyor; modern tarayıcıda `document.all.WEATHER.setAttribute` hata verebilir ve blok boş kalır (render'da tarih göründü, `BGCOLOR` uygulanmadı) → sunucu tarafında ya da `textContent` ile yaz; canlı güncellenmiyorsa `aria-live` gerekmez.

home.before.html:292-294 — A9 · WCAG 2.5.8 · şiddet 2 — "MORE" görsel linkleri 48×16 px; metin içi link istisnası bu görsel-tek linklere uygulanmaz → en az 24×24 px hedef; metin linkle birleştir.

home.before.html:173-183,208,233,244-269,273,301,305-306,327 — A2 · WCAG 1.1.1 · şiddet 2 — ~25 süs/spacer görseli (`border_*.gif`, `marker2_*.gif`, `blank_5x5.gif`) `alt` yok → ekran okuyucu dosya adlarını okur → `alt=""`; daha iyisi CSS ile arka plan/kenarlık.

home.before.html:3 — U6 · H4 · şiddet 1 — `<TITLE>Welcome to CityLights! [Inaccessible Home Page]</TITLE>` demo etiketi kapsam dışı; gerçek sitede sayfa başlığı "CityLights — Home" biçiminde site adı + sayfa.

### Kontrol listesi hükümleri

A1 ihlal :275 · A2 ihlal :248 · A3 ihlal :309 · A4 ihlal :187 · A5 uygulanamaz (hata/durum bildirimi yok) · A6 ihlal :248 (CSS outline kaldırılmamış, :182'de varsayılan halka göründü; ama :248+ odak script ile düşürüldüğü için 14 linkte gösterge hiç oluşmuyor — WCAG 2.4.7) · A7 ihlal :248 · A8 ihlal :248 · A9 ihlal :292 · A10 uygulanamaz (yalnız hover ile tetiklenen görsel değişimi; otomatik hareket yok) · A11 uygulanamaz (veri tablosu yok; yerleşim tabloları A1 altında) · A12 ihlal :1 · A13 ihlal :215
U1 ihlal :187 · U2 uygun (navigasyon ve dış linkler var; klavye erişimsizliği A7 altında) · U3 uygulanamaz (biçimli alan yok) · U4 uygulanamaz (form yok) · U5 uygulanamaz (yıkıcı eylem yok) · U6 ihlal :143 · U7 ihlal :188 (QUICKMENU'de placeholder-seçenek etiket yerine) · U8 ihlal :298

### Klavye gezintisi (tarayıcı panelinde, gerçek Tab)

Sekme sırası (16 Tab, `focusin`/`focusout` günlüğü): **1** logo linki (:182, tarayıcı varsayılan halkası görünür) → **2** QUICKMENU `select` (:187; ok tuşu = anında yönlendirme riski, bilerek denenmedi) → **3–16** sol nav (4) + haber başlıkları (3) + MORE (3) + Click here (2) + Read More (2): her biri odak alır ve `onfocus="blur();"` ile **aynı anda düşürür** — 14 `focusout`, kalıcı `focusin` yok, `activeElement` boyunca `<body>`.
Sonuç: demo alanındaki 21 odaklanabilir öğeden klavyeyle **yalnız 2'si** (logo, select) odak tutuyor; 14 içerik/navigasyon linki görünmez geçiliyor, hiçbiri Enter ile açılamıyor; footer linkleri (:350) ancak 14 görünmez adımdan sonra. Odak sırası görsel sırayla örtüşüyor (sorun sıra değil, tuzak). Playwright/axe bu sayfa için çalıştırılmadı (harici site).

### İnsan için TODO
- [ ] Ekran okuyucu (NVDA/VoiceOver): sol nav linklerinin "nav_home.gif" diye okunduğunu, "MORE" linklerinin adsız kaldığını, QUICKMENU'nün etiketsiz duyurulduğunu doğrula.
- [ ] Klavyede QUICKMENU'de aşağı ok tuşuna basıp yönlendirmenin anında olup olmadığını doğrula (denetimde bilerek basılmadı — harici siteye yönlendirir).
- [ ] %200 yakınlaştırma ve 320 px genişlik: sabit 780 px tablo yerleşimi yatay kaydırma üretir mi (büyük olasılıkla evet — 1.4.10 reflow).
- [ ] Renk körlüğü simülasyonu: sol nav hover durumu yalnız görsel değişimiyle iletiliyor (:248 `switchImage`).
- [ ] Gerçek kullanıcı, 1 görev: yalnız klavyeyle "Free Penguins" haberinin devamını aç — beklenen sonuç: başaramaz.
- [ ] Karşılaştırma: W3C'nin kendi denetim raporu `before/reports/home.html` ile bulguları eşle (bu rapor yazıldıktan **sonra** açıldı).

---

### W3C cevap anahtarıyla karşılaştırma — *rapor tamamlandıktan sonra açıldı*

Kaynak: `before/reports/home.html` (W3C, 2012). AA düzeyinde 19 kriter (7 AAA kriteri kapsam dışı; 4.1.1 WCAG 2.2'de kaldırıldı).

| Sonuç | Sayı | Kriterler |
|---|---|---|
| Bulundu | **15** | 1.1.1 · 1.3.1 · 1.4.3 · 1.4.5 · 2.1.1 · 2.4.2 · 2.4.4 · 2.4.6 · 2.4.7 · 3.1.1 · 3.2.1 · 3.2.2 · 3.2.5 · 3.3.2 · 4.1.2 |
| Kısmi | 2 | 1.3.2 (yerleşim tablolarının okuma sırası — A1 altında değinildi, ayrı bulgu değil) · 3.2.4 ("MORE" / "Read More..." tutarsız adlandırma — yalnız ima) |
| Kaçtı | **2** | **1.4.1** — gövde linkleri yalnız renkle ayrılıyor (`#main a { text-decoration: none }`, :12-15) · **2.4.1** — demo alanında tekrarlayan blokları atlama linki yok |

İki kaçırma **kontrol listesi deliği**: A5 yalnız hata durumu için yazılmıştı (linkler değil); A1 atlama linkini istemiyordu. İkisi de bu kanıtla SKILL.md'de genişletildi (A5: gövde linki ayırt edici; A1: sayfa düzeyinde atlama linki; A6: "odak kalır").

Skill'in W3C listesinde **olmayan** bulguları: 2.5.8 hedef boyutu (2012'de kriter yoktu), bağlamsız `NOSCRIPT` uyarısı, `document.all` kırılganlığı, telefon numarasının görsel olması (1.4.5 altında sayılabilir).
