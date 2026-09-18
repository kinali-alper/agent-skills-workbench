---
name: ux-a11y-review
description: Arayüzü denetle — tam UX + erişilebilirlik denetimi (kullanılabilirlik incelemesi ve erişilebilirlik kontrolü tek raporda). Use for a full UX + accessibility review of UI source (TSX, HTML, Razor, Vue, Svelte, Framer) — findings as file:line with WCAG 2.2 / Nielsen H# and a concrete fix. Report-only; does not edit files.
---

# UX + erişilebilirlik denetimi

Bir arayüz dosyasını (veya render edilmiş sayfayı) **kullanılabilirlik** (Nielsen H1–H10) ve **erişilebilirlik** (WCAG 2.2 AA) açısından denetler. Çıktı rapordur; dosya düzenlenmez. Otomatik araçların (axe, Lighthouse) kör noktalarına odaklanır: davranış, anlam, etiket kalıcılığı, odak, hedef boyutu, tablo yapısı.

## Adımlar

### 1. Bağlamı tespit et
Hedef kullanıcıları ve arayüz dilini projeden çıkar: CLAUDE.md, README, rota/bileşen adları, mevcut metinler. Bulamazsan **devam etmeden kullanıcıya sor**.
Kullanıcı grubu için üç şeyi yaz: cihaz (mobil/masaüstü), deneyim düzeyi, tekrar sıklığı (günde bir / günde otuz). Bunlar H7 (verimlilik) ve hedef boyutu kararlarını yönlendirir.
✔ Kriter: rapor başlığında "Kullanıcılar: … · Dil: …" satırı var, ya da "bilinmiyor — soruldu".

Arayüz dili Türkçe ise [references/locale-tr.md](references/locale-tr.md) oku. Dosya Razor (.cshtml) ise [references/stack-razor.md](references/stack-razor.md) oku.

### 2. Kullanılabilirlik geçişi
`heuristic-evaluation` skill'ini çağır ve sürecini uygula: yeni kullanıcı gözüyle, deneyimli kullanıcı gözüyle, her görev akışı için. Her bulguya H# ve şiddet (0–4).
Aşağıdaki U-listesinin her satırına hüküm ver:

| U | Kontrol | Heuristik |
|---|---|---|
| U1 | Her eylem (gönder, sil, kaydet) görünür sonuç üretir: durum mesajı (`role="status"`), yönlendirme veya bekleme göstergesi | H1 |
| U2 | Her akıştan çıkış yolu var: İptal / Geri; yarım veri varsa çıkışta uyarı | H3 |
| U3 | Biçimli alanlar (kimlik no, telefon, tarih) doğru `type`/`inputmode`, format ipucu ve örnek taşır; hata metni **ne** yanlış ve **nasıl** düzelir söyler | H5 · H10 |
| U4 | Zorunlu işareti ve hata işareti iki ayrı sinyaldir; yönerge metni gerçek durumla örtüşür | H4 |
| U5 | Yıkıcı eylem (sil, sıfırla, geri alınamaz gönderim) onay ister ya da geri alma penceresi verir | H3 |
| U6 | Rozet/etiket/uyarı bir içeriğe bağlıdır ("Yeni: X güncellendi"); bağlamsız dikkat çekici yok | H8 |
| U7 | Etiketler kalıcıdır; placeholder etiket yerine geçmez | H6 |
| U8 | Link ve buton metni hedefi/eylemi arayüz dilinde söyler ("Kayıt koşullarını görüntüle", "Formu temizle") | H2 |

✔ Kriter: U1–U8'in her biri için hüküm: **bulundu (dosya:satır)** / **yok** / **uygulanamaz**.

### 3. Erişilebilirlik geçişi
Aşağıdaki A-listesinin her satırına hüküm ver. Kural metni ve kod reçetesi gerektiğinde `~/.claude/skills/wq-accessibility/SKILL.md` ilgili bölümünü oku (skill'i çağırma; 460 satır). Form-UX ayrıntıları (autocomplete, inputmode, placeholder biçimi) için `web-design-guidelines`.

| A | Kontrol | WCAG |
|---|---|---|
| A1 | Sayfada tek `h1`, başlıklar hiyerarşik, `main` landmark | 1.3.1 · 2.4.6 |
| A2 | Bilgi taşıyan görselde anlamlı `alt`; süs görselde `alt=""` | 1.1.1 |
| A3 | Metin kontrastı ≥ 4.5:1 (büyük metin / UI ≥ 3:1) | 1.4.3 · 1.4.11 |
| A4 | Her form denetimi programatik etikete bağlı (`label for`, `aria-labelledby`) | 1.3.1 · 3.3.2 |
| A5 | Hata ve durum rengin yanında metin/ikonla iletilir; `aria-invalid` + `aria-describedby` | 1.4.1 · 3.3.1 |
| A6 | Odak görünür: `:focus-visible` ile ≥ 3:1 kontrastlı gösterge; kaldırılan outline yerine eşdeğer var | 2.4.7 · 2.4.11 |
| A7 | Etkileşimli öğe **native** (`button`, `a href`, form denetimi); `div/span` + onClick yerine | 2.1.1 · 4.1.2 |
| A8 | Yalnız ikon/emoji taşıyan denetimde erişilebilir ad (`aria-label` / gizli metin) | 4.1.2 · 2.5.3 |
| A9 | Tıklama hedefi ≥ 24×24 CSS px (inline metin linki hariç) | 2.5.8 |
| A10 | Hareket `prefers-reduced-motion` altında durur; 5 sn'den uzun otomatik hareket durdurulabilir | 2.3.3 · 2.2.2 |
| A11 | Veri tablosunda `caption` ve `th scope`; **küçük tablolar (≤3×3) axe'ten kaçar, elle kontrol** | 1.3.1 |
| A12 | `html lang` doğru; dil değişen parçalarda `lang` | 3.1.1 · 3.1.2 |
| A13 | Canlı güncellemeler (doğrulama, toast) `aria-live` / `role="status"` ile duyurulur | 4.1.3 |

✔ Kriter: A1–A13'ün her biri için hüküm: **bulundu (dosya:satır)** / **yok** / **uygulanamaz**.

### 4. Etkileşimli doğrulama (sayfa render edilebiliyorsa)
Tarayıcı panelinde sayfayı aç; **Tab** ile baştan sona gez. Rapora yaz: odak sırası görsel sırayla örtüşüyor mu, ulaşılamayan eylem var mı, odak kaybolan yer var mı. Playwright + axe varsa çalıştır ve ihlal id'lerini A-listesiyle eşle.
Sayfa render edilemiyorsa bu adımı "render yok — statik denetim" diye işaretle.
✔ Kriter: "Klavye gezintisi: …" satırı ya da "render yok" notu.

### 5. İnsan için kalan işler
Ajanın yapamadığı kontrolleri **TODO bloğu** olarak rapora ekle:
- Ekran okuyucu (NVDA/VoiceOver): form etiketleri, hata duyuruları, tablo başlıkları okunuyor mu
- %200 yakınlaştırma ve 320 px genişlikte içerik kaybı var mı
- Gerçek kullanıcıyla 1 görev: [adım 1'deki kullanıcı grubu] akışı yardımsız tamamlayabiliyor mu

## Çıktı biçimi

```
## <dosya>  ·  Kullanıcılar: <…>  ·  Dil: <…>

### Bulgular (şiddete göre)
<dosya>:<satır> — A4 · WCAG 3.3.2 · şiddet 3 — input yalnız placeholder ile adlandırılmış → kalıcı <label for="ad">Ad Soyad</label> ekle
<dosya>:<satır> — U1 · H1 · şiddet 4 — Kaydet görünür sonuç üretmiyor → gönderim sonrası role="status" mesajı veya onay sayfası

### Kontrol listesi hükümleri
A1 bulundu :5 · A2 bulundu :6 · A3 yok · … · U8 bulundu :28

### Klavye gezintisi
…

### İnsan için TODO
…
```

Düzeltmeyi **olumlu** yaz: yapılacak şeyi söyle ("`:focus-visible` ile 3 px outline ver").

## Tamamlama kriteri
A1–A13 ve U1–U8'in **her biri** için hüküm yazıldı; her "bulundu" hükmü `dosya:satır` taşıyor; adım 4 ve 5 blokları mevcut. Eksik hüküm = rapor bitmemiş.
