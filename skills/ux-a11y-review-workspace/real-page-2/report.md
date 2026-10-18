# Gerçek sayfa #2 — görülmemiş bir Türkçe belediye ana sayfası (2026-10-16)

**G2 kapısı:** cevap anahtarı olmayan, eğitim verisinde bulunma olasılığı düşük, herkese açık bir sayfada skill'i
koşmak — *regresyon değil keşif*. İlk gerçek sayfa (W3C WAI "Before and After Demo") bilinen bir öğretim örneğiydi;
bu sayfa değil.

**Hedef:** Türkçe bir büyükşehir belediyesi ana sayfası. **URL bu dosyada yazılmadı**: bulgular gerçek ve kamuya açık
ama bir kamu kurumunu bu depoda adıyla teşhir etmek depo sahibinin kararı. URL yerel çalışma notunda; istenirse eklenir.
Sayfa yalnız **okundu**: gezinti klavyeyle yapıldı, hiçbir form gönderilmedi, hiçbir düğmeye tıklanmadı.

**Araç:** uygulama içi tarayıcı paneli bu makinede **çizmiyor** (viewport 0×0), bu yüzden erişilebilirlik ağacı boş
döndü. DOM ve CSS JavaScript'le okundu, klavye geçişi **gerçek Tab tuşlarıyla** yapıldı ve `focusin` dinleyicisiyle
kaydedildi. Görsel ölçüm gerektiren maddeler (kontrast, hedef boyutu) bu yüzden **doğrulanamaz**.

## Sayfanın ölçülen hâli
1.449 DOM düğümü · 330 odaklanabilir öğe · 164 görsel · 7 form denetimi · 0 tablo · 0 iframe · `html lang="tr"`

## Bulgular (şiddete göre)

| # | Kural | Kanıt | Yerine |
|---|---|---|---|
| 1 | **A8 · 4.1.2** — 93 ikon-bağlantının erişilebilir adı yok | Sosyal medya, banner ve logo bağlantıları yalnız `<img>` içeriyor, `alt` ve `aria-label` yok | Her bağlantıya görünür metin ya da `aria-label` ver ("Facebook sayfamız") |
| 2 | **A8 + 2.4.3 · klavye kanıtı** — ilk **13 Tab durağının 13'ü isimsiz** | `focusin` kaydı: 6 × `a.glink href="#"` (dil seçici, boş metin) → 3 sosyal medya → Atatürk bağlantısı → 2 banner → logo. İlk anlamlı etiket **14. Tab**: "ÇÖZÜM MERKEZİ" | Dil seçiciyi `<button>`+ad yap; banner'lara ad ver; en başa atlama bağlantısı koy |
| 3 | **A2 · 1.1.1** — 164 görselin **85'inde `alt` niteliği hiç yok** (13'ü boş `alt`) | Ekran okuyucu bu 85 görseli dosya adıyla okur | Bilgi taşıyanlara anlamlı `alt`, süs olanlara `alt=""` |
| 4 | **A1 · 1.3.1 / 2.4.6** — `h1` **yok**; `main`, `nav`, `header`, `footer` ve landmark rolleri **yok**; başlık sırası bozuk | Başlıklar: H3, H2, H3, H3, H5, H5, H5, H5, H5, H3, H4, H5 — sayfa H3 ile başlıyor, H4 atlanıyor | Tek `h1` (sayfa konusu), içeriği `<main>`e al, gezinti `<nav>`, başlıkları sırala |
| 5 | **A4 · 1.3.1 / 3.3.2** — 7 form denetiminin **4'ü etiketsiz** | İki arama alanı yalnız `placeholder` ("Ne arıyorsunuz?", "Yazınızı buraya girin"), **KVKK onay kutusu** (`name=gdpr[]`) etiketsiz | `<label for>` ekle; onay kutusunun metnini `<label>` içine al |
| 6 | **A6 · 2.4.7** — CSS'te `outline: none` **14 kuralda**, `:focus-visible` yalnız **4** kuralda | Odak göstergesi büyük olasılıkla kayıp; görsel teyit render olmadığı için yapılamadı → bu satır *doğrulanamaz* değil, kural sayısı kanıt sayıldı ama **ekranda doğrulanmalı** | Kaldırılan her `outline` yerine `:focus-visible` ile ≥ 3:1 kontrastlı halka |
| 7 | **A7 · 2.1.1** — 1 öğe `onclick` taşıyor ama native denetim değil | `div/span` + `onclick` | `<button>` kullan |
| 8 | **Atlama bağlantısı yok** | İlk üç `a[href^="#"]` dil seçici, metinleri boş | "İçeriğe geç" bağlantısı, gezintiden önce |

## Hükümler
A1 ihlal · A2 ihlal · A3 **doğrulanamaz** (render yok, kontrast ölçülemedi) · A4 ihlal · A5 doğrulanamaz (hata durumu
tetiklenmedi — form gönderilmedi) · A6 ihlal (CSS kanıtı; ekranda teyit bekliyor) · A7 ihlal · A8 ihlal ·
A9 **doğrulanamaz** (hedef boyutu için yerleşim gerekir, viewport 0×0) · A10 uygun (`prefers-reduced-motion` kuralı var,
`transition: all` yok) · A11 **uygulanamaz** (tablo yok) · A12 uygun (`html lang="tr"`) · A13 doğrulanamaz
(`aria-live`/`role=status` yok ama canlı güncelleme de görülmedi)

U-listesi bu koşuda uygulanmadı: kullanılabilirlik hükümleri için akışı denemek gerekir (form göndermek), üçüncü taraf
bir kamu sitesinde yapılmadı.

## Klavye gezintisi
14 Tab basıldı, `focusin` ile kaydedildi. Odak sırası DOM sırasını izliyor ve **görsel sırayla örtüşüp örtüşmediği
doğrulanamadı** (render yok). Tuzak görülmedi: odak her adımda ilerledi. Asıl sorun sıra değil, **durakların adsızlığı**.

## Keşif değeri — skill ne ekledi?
HTML'i düz okumak bulgu 3, 4, 5, 7'yi verirdi. **Tarayıcı adımı olmadan görünmeyenler:**
- **Bulgu 2**: 13 ardışık isimsiz durak ancak gerçek Tab geçişiyle görülüyor; kaynakta bu 13 öğe birbirinden uzakta
  ve tek tek "küçük" kusur gibi duruyor. Davranışta ise klavye kullanıcısının sayfaya girişinin tamamı adsız.
- **Bulgu 6**: `outline: none` ile `:focus-visible` sayısının **oranı** (14'e 4) tek dosyada görünmüyor, bütün stil
  sayfalarını birlikte saymak gerekiyor.
- **A3/A9'un doğrulanamaz kalması** da bir kazanç: skill uydurmuyor, "render yok" diye işaretliyor.

## İnsan için TODO
- Ekran okuyucu (NVDA) ile ana gezinti ve arama alanı.
- Odak halkasını gerçek bir tarayıcıda görsel teyit (bulgu 6).
- %200 yakınlaştırma ve 320 px genişlikte içerik kaybı.
- Kontrast ölçümü (A3) ve dokunma hedefi (A9) — çizen bir tarayıcıda.
- KVKK onay kutusunun etiketi ve hata metni (form gönderilerek).
