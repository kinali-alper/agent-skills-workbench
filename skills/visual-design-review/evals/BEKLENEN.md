# `visual-scan.py` fixture çifti ve beklenen sonuç

Betik değişince bu iki dosyada koş; sayılar bozulduysa betik bozulmuş demektir.

```bash
python ../scripts/visual-scan.py slop.html   # beklenen: ≥ 4 işaret, çıkış kodu 2
python ../scripts/visual-scan.py temiz.html  # beklenen: 0–1 işaret, çıkış kodu 0
```

| Fixture | Ne temsil ediyor | Ölçülen (2026-10-16) | Beklenen |
|---|---|---|---|
| `slop.html` | Aynı yönetim ekranı, "yapay zekâ işi" işaretleriyle: `lang` yok, Inter, sRGB mor→mavi degrade, 14 font boyutu, 8 yarıçap, 5 gölge, `transition: all`, 600 ms geçiş, `height` geçişi, 4 `backdrop-filter`, saf gri nötrler, ölçek dışı boşluk, `font-display`/`size-adjust` yok, `unicode-range` Türkçe'yi kapsamıyor, `uppercase` + `lang` yok, `outline: none` | **17 işaret**, kod **2** | ≥ 4 işaret, kod 2 |
| `temiz.html` | Aynı ekranın disiplinli hâli: `lang="tr"`, başlık + metin yüzü ayrı, OKLCH tonlanmış nötrler (krom 0,004→0,042), 6 font boyutu, 3 yarıçap, 2 gölge, 120–250 ms `transform`/`opacity` geçişi, tek `backdrop-filter` (yapışkan gezinti), 4 px tabanlı ölçekte %100 uyum, `font-display` + `size-adjust` + Latin Extended-A, `:focus-visible`, `tabular-nums`, `prefers-reduced-motion` | **0 işaret**, kod **0** | 0–1 işaret, kod 0 |

İkisi birlikte taranırsa değerler havuzlanır — bu normal: betik dosya değil **yüzey** ölçer, bir ekranın bütün CSS'i
tek havuzdur. Ayrı ayrı koş.

## Fixture'ın ölçmediği (bilerek)
- Hiyerarşi, yerleşim ve üslup birliği → skill'in 3. adımı (`references/isaretler.md` G-listesi).
- Vurgu renginin alan payı, gerçek glif yedeklemesi → 4. adım (render gerekir).
- Tailwind/utility sınıflı projeler: `slop.html` düz CSS yazar; utility sınıflı bir fixture henüz yok (betik bu
  durumda boyut/yarıçap satırını "uygulanamaz" diye işaretler).

## Eşiklerin provenansı
Rapordaki her satır etiketli: `[kaynak]` dış belgede doğrulanmış (MDN, web.dev, WCAG, Material, Lucide, Vercel
guidelines), `[öneri]` 2026 araştırma turunun önerisi — **bu depoda bağımsız ölçülmedi**. `[öneri]` eşikleri gerçek
projelerde yanlış pozitif verirse önce eşiği tartış; betiği değiştirmeden önce sayıyı yaz.

## Köken
Betik, özel bir birikim deposunda yazılmış bir tarayıcıdan taşındı (2026-10-16): `[zevk]` (kişisel beğeni) etiketli
eşikler bu sürümde `[kaynak]`/`[öneri]` olarak yeniden sınıflandırıldı, kişi/proje adına atıf yapan satırlar
çıkarıldı. Bu depodaki sürüm **proje bağımsızdır**.

## 2026-10-16 düzeltmesi
Mor/indigo tespiti yalnız sınıf adına (`indigo-500`, `from-purple`) bakıyordu; `slop.html`'deki hex yazımı
(`#7c3aed`, `#6366f1`) gözden kaçıyor ve betik "mor/indigo yok" diyordu. Artık doygun renklerin (krom ≥ 0,08)
OKLCH hue'suna da bakılıyor (255–330°). Bu yüzden `slop.html` 16 → **17 işaret**. `temiz.html` değişmedi (0).
