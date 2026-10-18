---
name: visual-design-review
description: Görsel tasarımı denetle — bir arayüzün görsel zanaatını ölçer ve adlandırılmış bulgular verir (belirteç disiplini, hiyerarşi, "yapay zekâ işi" işaretleri, hareket, mikro metin). Use for a visual design review of UI source or a rendered page — signal counts and findings as file:line with a concrete fix. Güzellik puanı vermez; rapor üretir, dosya düzenlemez. Erişilebilirlik denetimi için değil (ux-a11y-review), tasarım üretmek için değil (frontend-design, design-taste-frontend, interface-design).
license: MIT
metadata:
  requires: "baseline-ui, interface-design, web-design-guidelines"
  status: "draft"
---

# Görsel tasarım denetimi

Bir arayüzün **görsel zanaatını** denetler: ölçek ve belirteç disiplini, hiyerarşi, yüzeyler, hareket, mikro tipografi
ve yaygın "yapay zekâ işi" işaretleri. Çıktı **sayılan işaretler + adlandırılmış bulgular**; 1–10 güzellik puanı
**verilmez** (bir ekran "işaretsiz" olup hâlâ sıkıcı olabilir — bunu rapor söyler, puan gizler).
Erişilebilirlik ayrı bir iştir: `ux-a11y-review`.

## Ne için kullanılmaz
- Erişilebilirlik/WCAG denetimi → `ux-a11y-review`.
- Tasarım **üretmek** ya da yön belirlemek → `frontend-design`, `design-taste-frontend`, `interface-design`.
- Yalnız hareket ayrıntısı → `motion-design`, `gsap-*`.
- Performans → `wq-performance`, `wq-core-web-vitals`.

## Gereksinimler
`scripts/visual-scan.py` için Python 3.9+ (yalnız standart kütüphane). Kurulu `baseline-ui` panel kuralları ve
`interface-design` zanaat ölçütleri için okunur; yoksa [references/isaretler.md](references/isaretler.md) tek başına yeter.
Render edilmiş sayfa gerekiyorsa başsız tarayıcı (adım 4) — **alt ajanların tarayıcısı yoktur**, o adım yalnız ana
oturumda çalışır.

## Hüküm sözlüğü
Her kontrol maddesi tam olarak **bir** durum alır:
- **ihlal :N** — kural çiğneniyor; N = dosya satırı. Bulgular bölümüne girer.
- **uygun** — kural karşılanıyor, kanıtı var.
- **uygulanamaz** — kuralın konusu bu arayüzde yok (ör. degrade yoksa G5).
- **doğrulanamaz** — kanıt statik kaynakta yok (hesaplanmış stil, utility sınıfı, render gerektiren ölçüm); İnsan TODO'ya.

## Adımlar

### 1. Bağlamı ve yüzey kipini yaz
Kip **üründen değil istenen yüzeyden** seçilir: **İkna** (tanıtım/giriş: cesur tipografi, tek anlamlı hareket) ·
**İşlet** (panel/form: sakin, yoğun, istenmedikçe animasyon yok) · **Oku** (içerik/belge: satır uzunluğu ve ritim) ·
**Deneyim** (anlatım/oyun: sahne ve geri bildirim). Eşikler kipe göre değişir; çatıştığında yüzeyin kipi kazanır.
✔ Kriter: rapor başlığında "Yüzey: … · Kip: …" satırı var.

### 2. Betiği koş
`python scripts/visual-scan.py <dosya|klasör>` → sayılabilir işaretler (ayrı font boyutu / yarıçap / gölge sayısı,
`transition: all`, 400 ms üstü geçiş, yerleşimi oynatan animasyon, `backdrop-filter`, saf gri nötr, boşluk ölçeğine
uyum, degrade interpolasyon uzayı, `font-display`/`size-adjust`, Türkçe `lang` + glif aralığı, odak halkası,
varsayılan yazı tipi ailesi, mor/indigo vurgu). Çıkış kodu 2 = işaret var. Raporun **provenans etiketlerini**
(`[kaynak]` / `[öneri]`) olduğu gibi aktar.
✔ Kriter: işaret sayısı + "betiğin göremediği" listesi rapora girdi.

### 3. Betiğin göremediğine hüküm ver
[references/isaretler.md](references/isaretler.md)'deki G-listesinin her satırına sözlükten bir durum yaz: hiyerarşi,
yerleşim ritmi, üslup birliği, görsel seçimi, mikro metin, bileşen teması, kip uyumu.
✔ Kriter: G1–G12'nin her biri için hüküm.

### 4. Render edilmiş sayfa (varsa)
Masaüstü **ve** mobil kareyi tek seferde al (başsız tarayıcı; bu makinede uygulama içi panel çizmiyorsa
`--headless=new --screenshot`). Kareye bakarak ölç: vurgu renginin alan payı, ilk ekranda ürünün kendisi görünüyor mu,
hiyerarşi kareden okunuyor mu, glif yedeklemesi var mı. **Bir** düzeltme turu, **en çok bir** yeniden kontrol.
Render edilemiyorsa bu adımı "render yok — statik denetim" diye işaretle.
✔ Kriter: iki kare + ölçüm satırı, ya da "render yok" notu.

### 5. İnsan için kalan işler
TODO bloğu: gerçek içerikle okunabilirlik, marka uyumu, bir kullanıcıya "bu ekran ne yapıyor" sorusu, yazı tipi
lisansı ve Türkçe glif testi, koyu/açık tema karşılaştırması.

## Çıktı biçimi

```
## <hedef>  ·  Yüzey: <…>  ·  Kip: <İkna|İşlet|Oku|Deneyim>

### İşaret sayısı
<betikten>: N işaret (0–1 temiz · 2–3 gözden geçir · 4+ yönü baştan düşün)

### Bulgular (şiddete göre)
<dosya>:<satır> — G3 · şiddet 3 — 14 ayrı font boyutu, ölçek yok → 6–8 basamaklı ölçek kur, `--step-*` belirteçleri
<dosya>:<satır> — G7 · şiddet 2 — üç eş kart + tek tip köşe → asimetrik ızgara, çapa kart 2×2

### Hükümler
G1 uygun · G2 ihlal :41 · G3 ihlal :12 · G4 doğrulanamaz (utility sınıfı) · … · G12 uygulanamaz

### Render
…

### İnsan için TODO
…
```

Düzeltmeyi **olumlu** yaz: yapılacak şeyi söyle ("nötrlere 0,01 krom ver, saf gri kullanma").

## Gotchas
- Betiğin "0 işaret" demesi tasarımın iyi olduğunu göstermez: utility sınıflı projede boyut/yarıçap sayımı
  "uygulanamaz" döner, alan payı ve glif yedeklemesi hiç ölçülmez. Adım 3 ve 4 atlanamaz.
- Yasağı alternatifsiz söylemek yeni klişe üretir: her **ihlal** satırı "yerine" ile birlikte yazılır.
- `[öneri]` etiketli eşikler bağımsız ölçülmedi; gerçek projede yanlış pozitif verirse eşiği tartış, bulguyu zorlama.
- Alt ajanın tarayıcısı yok; adım 4'ü alt ajana verme.
- Tek işaret zayıf kanıttır; hüküm **işaretlerin bir aradalığına** dayanır.

## Tamamlama kriteri
Adım 2'nin işaret sayısı yazıldı; G1–G12'nin **her biri** için sözlükteki dört durumdan biri var; her **ihlal**
`dosya:satır` + "yerine" taşıyor; her **doğrulanamaz** İnsan TODO'da; adım 4 ve 5 blokları mevcut.
Eksik hüküm = rapor bitmemiş.
