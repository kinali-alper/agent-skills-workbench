# Neden bu vaka?
Türkçe okul kayıt formu — otomatik araçların (axe, Lighthouse) kör noktalarını tek sayfada toplar:
placeholder-etiket, renk-tek-sinyal, div-buton, emoji-buton, küçük hedef, hareket, küçük tablo, belirsiz link;
ayrıca Nielsen heuristiklerine bağlı 6 kullanılabilirlik hatası (durum görünürlüğü, çıkış yolu, hata önleme, tutarlılık, onaysız silme, bağlamsız rozet).

Üç ikiz: React TSX · düz HTML · ASP.NET Razor — skill'lerin stack'ten bağımsız aynı bulguları vermesi için.

Test edilen skill'ler: ux-a11y-review (kendi), web-design-guidelines, wq-accessibility, heuristic-evaluation.

Çalıştırma:
```bash
cd playground && npm run test:a11y          # axe raporu → playground/reports/
cd playground && npm run lh -- broken       # Lighthouse (dev sunucu açık olmalı)
```
