## FixedForm.tsx  ·  Kullanıcılar: veliler — mobil, ilk kez kullanan, tekrar sıklığı tek sefer/nadir  ·  Dil: Türkçe  ·  **Statik denetim (render yok)**

Kapsam: yalnız `FixedForm.tsx` (proje dosyası olarak tek dosya). CSS, `<html lang>`, `<title>` ve sayfa iskeleti bu dosyada değil; bunlara bağlı maddeler **doğrulanamaz** olarak işaretlendi ve İnsan TODO'ya taşındı. Bağlam kullanıcı tarafından verildi (veliler, mobil, ilk kez); dosyadaki metinler (Öğrenci Kayıt, Veli e-postası, TC Kimlik No) bunu doğruluyor. `references/locale-tr.md` ve `references/wcag22-aa-sweep.md` okundu; `heuristic-evaluation` çağrıldı; `wq-accessibility` SKILL.md'nin 2.5.8 / 3.3.2 / 3.3.1 / 4.1.2 / 4.1.3 bölümleri okundu.

### Bulgular (şiddete göre)
**İhlal bulunmadı.** A1–A13 ve U1–U8'in dosyada kanıtlanabilen her maddesi karşılanıyor; kalanlar başka dosyaya bağlı (aşağıda doğrulanamaz).

### Öneriler (ihlal değil — Bulgular sayımına girmez)
- FixedForm.tsx:43 — H1 · 4.1.3 · şiddet 2 (statik olarak kanıtlanamaz, TODO'da) — `document.getElementById(first)?.focus()` aynı handler içinde `setSubmitted(true)`'dan **önce**, re-render'dan önce çalışıyor; odak alana gittiği anda DOM'da `aria-invalid="false"` ve `aria-describedby` hâlâ ipucu (ya da yok). Ekran okuyucu alanı hatasız okuyabilir; hata `<p>` sonra belirir ve kendi canlı bölgesi yok → odak vermeyi `submitted`'a bağlı bir `useEffect`'e taşı (ya da `flushSync` ile state'i önce yaz), alternatif olarak hata `<p>`'sine `role="alert"` ver.
- FixedForm.tsx:69 — 4.1.3 · şiddet 1 — Blur'da beliren alan hatası canlı bölgede değil; odak zaten sonraki alana geçtiği için duyurulmaz (gönderimde :101 status bunu telafi ediyor) → yukarıdaki `role="alert"` önerisiyle birlikte değerlendir.
- FixedForm.tsx:65 — 4.1.2 · şiddet 1 — Etiketteki `*` ekran okuyucuda "yıldız" okunur; `aria-required` zaten zorunluluğu bildiriyor → `<span aria-hidden="true">*</span>` ile sar.
- FixedForm.tsx:98 — 4.1.2 · şiddet 1 — `🗑` emoji `aria-hidden` değil; "çöp kutusu Formu temizle" okunur → `<span aria-hidden="true">🗑 </span>Formu temizle`.

### Kontrol listesi hükümleri
A1 doğrulanamaz (atlama linki sayfa düzeyi; dosyada tek `h1` :76, `h2` :116, `main` :75 uygun) · A2 uygun (:78 süs görsel `alt=""`) · A3 doğrulanamaz (CSS; tek inline renk :80 `#4a4a4a`/`#fff` ≈ 8,9:1 uygun; `.hint` `.error` `.badge` `.status` buton renkleri CSS'te) · A4 uygun (:65–66 `htmlFor`/`id` dört alanda) · A5 doğrulanamaz (gövde linki :104 altı çizgisi CSS; hata sinyali :67–69 `aria-invalid` + `aria-describedby` + ikon + metin uygun) · A6 doğrulanamaz (`:focus-visible` CSS; dosyada odak düşüren script yok, :43 odak ilk hatalı alana taşınıyor) · A7 uygun (:85–99 `input` `select` `button` `a href`; `div`+onClick yok) · A8 uygun (:98 emoji yanında görünür metin var; yalnız-ikon denetim yok) · A9 doğrulanamaz (buton/`.cancel` link boyutu CSS) · A10 uygulanamaz (hareket/animasyon/otomatik oynatma yok) · A11 uygun (:107 `caption`, :108 `th scope="col"`, :110–111 `th scope="row"`; 2×3 küçük tablo elle kontrol edildi) · A12 doğrulanamaz (`html lang` sayfa düzeyi; dosyada dil değişen parça yok) · A13 uygun (:101 `role="status" aria-live="polite"` ilk render'da var; :42 :46 :52 durum mesajları buraya yazılıyor)

U1 uygun (:42 hata, :46 başarı, :52 temizleme mesajı → :101 status; İptal :99 yönlendirme) · U2 uygun (:99 İptal linki, :56 kirli formda onay; :98 Temizle) · U3 uygun (:86 `type="email"` `autoComplete="email"`; :87 `inputMode="numeric"` `maxLength=11` + ipucu "11 rakam, boşluksuz."; :15 :17 hata metni ne yanlış + örnek) · U4 uygun (:65 `*` + :81 açıklama = zorunlu sinyali; :67–69 `aria-invalid` + ⚠ + metin = hata sinyali; :81 yönerge gerçek durumla örtüşüyor, dört alan da zorunlu) · U5 uygun (:50 Temizle onayı, :56 İptal kirli formda onay; gönderim :40–44 doğrulamayla kontrol ediliyor, 3.3.4 "checked") · U6 uygun (:104 "Yeni" rozeti "Sınıf listesi 2026-27 dönemine güncellendi" içeriğine bağlı) · U7 uygun (:65 kalıcı `label`; :90 seçim yer tutucusu etiket yerine geçmiyor) · U8 uygun (:97 Kaydet, :98 Formu temizle, :99 İptal, :104 Kayıt koşullarını görüntüle)

**Toplam 21 hüküm:** ihlal 0 · uygun 14 (A2 A4 A7 A8 A11 A13 + U1–U8) · uygulanamaz 1 (A10) · doğrulanamaz 6 (A1 A3 A5 A6 A9 A12)

#### WCAG 2.2 AA sweep (kalan 36 kriter — dosyada ilgili olanlar)
- 1.3.5 Girdi amacı: :86 `autoComplete="email"` veli e-postası için uygun; :85 `autoComplete="off"` öğrenci adı içindir (kullanıcının kendisi değil), savunulabilir.
- 1.3.3 Duyusal özellikler: :81 yönerge sembole (`*`) dayanıyor, konum/renk değil — uygun.
- 2.4.4 Link amacı: :104 "Kayıt koşullarını görüntüle" → `#detay` hedefi :115'te mevcut — uygun.
- 3.2.2 Girdide bağlam: :89 `select` `onChange` yalnız state yazıyor, yönlendirme yok — uygun.
- 3.2.4 Tutarlı tanımlama: "Kayıt/Kaydet" terimleri başlık, buton ve durum mesajlarında tutarlı — uygun.
- 3.3.3 Hata önerisi: :15 :17 örnekli öneri — uygun. 3.3.4 Hata önleme: :50 onay, :40 doğrulama — uygun. 3.3.7 Tekrarlı giriş: tek adımlı form — uygulanamaz.
- 2.5.2 İşaretçi iptali: eylemler `onClick`/`onSubmit`/`onReset`, `mousedown` yok — uygun.
- 2.4.2 Sayfa başlığı `<title>`, 1.4.4 %200, 1.4.10 reflow, 1.4.12 metin aralığı: dosyada/render yok → İnsan TODO.
- 1.2.x, 1.4.2, 2.1.4, 2.2.1, 2.5.1, 2.5.4, 2.5.7, 3.3.8: ilgili öğe yok — uygulanamaz.

### Klavye gezintisi
render yok — statik denetim. DOM'dan beklenen odak sırası (doğrulanmadı): Öğrencinin adı soyadı → Veli e-postası → Öğrencinin TC Kimlik No → Sınıf → Kaydet → Formu temizle → İptal → Kayıt koşullarını görüntüle. Gönderimde odak ilk hatalı alana taşınıyor (:43). Odak tuzağı oluşturacak modal/iframe/widget yok; `confirm()` diyalogları native.

### İnsan için TODO
- **A1** — Sayfa iskeletinde tekrarlayan blok (nav/header) varsa `main`'e atlama linki var mı; sayfada başka `h1` yok mu.
- **A3** — CSS'te `.hint`, `.error`, `.badge`, `.status`, buton ve `.cancel` link renkleri: metin ≥ 4,5:1, UI kenarlık/ikon ≥ 3:1 (ölçüm: DevTools ya da Colour Contrast Analyser).
- **A5** — `.cancel` ve :104 gövde linki: alt çizgi ya da renk dışı ayırt edici CSS'te korunuyor mu; `.error` yalnız renkle değil (ikon+metin var, kenarlık ek).
- **A6** — `:focus-visible` göstergesi tüm denetimlerde görünür ve ≥ 3:1 mi; `outline: none` varsa eşdeğeri var mı; odak yapışkan öğelerle örtülmüyor mu (2.4.11).
- **A9** — Kaydet / Formu temizle / İptal hedefleri ≥ 24×24 CSS px (mobil veli için 44×44 önerilir); `.actions` içinde hedefler arası boşluk.
- **A12** — Sayfa kökünde `<html lang="tr">` var mı; `<title>` (2.4.2) sayfayı tanımlıyor mu ("Öğrenci Kayıt — okul adı").
- **Ekran okuyucu (NVDA/VoiceOver, TalkBack mobil)** — Kaydet'e boş formla basınca: odak ilk hatalı alana gidiyor **ve hata metni okunuyor mu** (:43 zamanlama riski, bkz. Öneriler); alanı terk edip hata belirince duyuru var mı; dört etiket + `*` + ipucu/hata okunuyor mu; tablo başlıkları (Ders/Not, satır başlıkları) okunuyor mu; :101 durum mesajları duyuruluyor mu.
- **%200 yakınlaştırma ve 320 px genişlik** — form, `.actions` düğme grubu ve tablo yatay kaydırma/içerik kaybı üretmiyor mu (1.4.4, 1.4.10); metin aralığı artırılınca kırılma (1.4.12).
- **Gerçek kullanıcıyla 1 görev** — İlk kez giren bir veli, mobilde, yardımsız: öğrenci adı + kendi e-postası + öğrencinin TC no + sınıf girip "Kayıt alındı" mesajını görüyor mu; hatalı TC girince mesajı anlayıp düzeltebiliyor mu; `confirm()` metinlerini anlıyor mu.
