# WCAG 2.2 A+AA — kompakt listenin dışında kalan 36 kriter

Adım 3'te A1–A13 bittikten sonra okunur. Kompakt liste (A1–A13) = otomatik araçların kör noktaları + sık ihlaller (19 kriter);
WCAG 2.2 A+AA toplamı 55 (4.1.1 kaldırıldı). Buradaki 36 için **hüküm zorunlu değil**; ilgili olanı bulguya yaz, ilgisizi geç.
Etiket: **kaynak** = koddan görülür · **render** = tarayıcıda görülür · **insan** = ajan doğrulayamaz, İnsan TODO'ya.

Bir kriter fixture ya da gerçek sayfa kanıtıyla sık ihlal çıkarsa A-listesine terfi eder (RESULTS.md'de gerekçeyle).

## Algılanabilir
| Kriter | Seviye | Ne | Nasıl bakılır |
|---|---|---|---|
| 1.2.1–1.2.5 | A/AA | Ses/video: alt yazı, sesli betimleme, canlı alt yazı | **kaynak**: `<video>`/`<audio>` varsa `<track kind="captions">`, transkript linki; yoksa uygulanamaz |
| 1.3.2 Anlamlı sıra | A | DOM sırası okuma sırasıyla örtüşür (yerleşim tabloları, CSS `order`, `float`) | **kaynak+render**: CSS ile yer değiştirmiş içerik |
| 1.3.3 Duyusal özellikler | A | Yönerge yalnız şekil/konum/sese dayanmaz ("sağdaki yeşil düğme") | **kaynak**: yönerge metinleri |
| 1.3.4 Yön | AA | İçerik dikey/yatay kilitli değil | **kaynak**: `orientation` media query ile kilitleme |
| 1.3.5 Girdi amacı | AA | Kişisel alanlarda doğru `autocomplete` (`name`, `email`, `tel`, `bday`…) | **kaynak**: form alanları |
| 1.4.2 Ses kontrolü | A | 3 sn'den uzun otomatik ses durdurulabilir | **kaynak**: `autoplay` |
| 1.4.4 Metin büyütme | AA | %200'de içerik/işlev kaybı yok | **render**: zoom 200 %; **insan** doğrular |
| 1.4.5 Metin görseli | AA | Metin görsel olarak değil metin olarak | **kaynak**: `alt` ile yazı taşıyan `img` |
| 1.4.10 Reflow | AA | 320 px genişlikte yatay kaydırma yok | **render**: 320 px viewport |
| 1.4.12 Metin aralığı | AA | Satır/harf/kelime aralığı artırılınca kırılma yok | **render**: aralık CSS enjekte edip bak; **insan** |
| 1.4.13 Hover/odakla beliren içerik | AA | Tooltip/menü: fareyi çekmeden kapatılabilir, üzerine gidilebilir, kalıcı | **render**: hover/odak öğeleri |

## Çalıştırılabilir
| Kriter | Seviye | Ne | Nasıl bakılır |
|---|---|---|---|
| 2.1.2 Klavye tuzağı | A | Odak her bileşene girip **çıkabilir** (modal, iframe, widget) | **render**: adım 4 Tab gezintisinde çıkışı da dene |
| 2.1.4 Tek tuş kısayolları | A | Harf kısayolu varsa kapatılabilir/değiştirilebilir | **kaynak**: `keydown` tek karakter |
| 2.2.1 Zaman sınırı | A | Oturum/zaman sınırı uzatılabilir | **kaynak**: timeout, otomatik çıkış |
| 2.3.1 Üç flaş | A | Saniyede 3'ten fazla yanıp sönme yok | **render**: animasyonlar |
| 2.4.2 Sayfa başlığı | A | `<title>` sayfayı ve siteyi tanımlar | **kaynak** |
| 2.4.3 Odak sırası | A | Tab sırası anlamlı | **render**: adım 4 |
| 2.4.4 Link amacı | A | Link metni + bağlam hedefi söyler | **kaynak** (U8 ile örtüşür; U8 arayüz dili, bu kriter bağlam) |
| 2.4.5 Birden çok yol | AA | Sayfaya ulaşmanın ≥2 yolu (menü, arama, site haritası) | **kaynak**: site düzeyi; bileşen dosyasında uygulanamaz |
| 2.5.1 İşaretçi hareketleri | A | Çoklu nokta/yol hareketine tek nokta alternatifi | **kaynak**: pinch, swipe |
| 2.5.2 İşaretçi iptali | A | Eylem `mousedown`'da değil `click`/`mouseup`'ta | **kaynak** |
| 2.5.4 Hareketle tetikleme | A | Cihaz sallama/eğme ile eyleme alternatif | **kaynak**: `devicemotion` |
| 2.5.7 Sürükleme | AA | Sürükle-bırak'a tek nokta alternatifi | **kaynak**: drag handlers |

## Anlaşılabilir
| Kriter | Seviye | Ne | Nasıl bakılır |
|---|---|---|---|
| 3.2.1 Odakta bağlam | A | Odak almak sayfayı/pencereyi değiştirmez | **kaynak**: `onfocus` içinde yönlendirme/submit |
| 3.2.2 Girdide bağlam | A | Seçim değişimi uyarısız yönlendirmez (`select onchange=location`) | **kaynak** |
| 3.2.3 Tutarlı gezinme | AA | Menü sırası sayfalar arası aynı | **kaynak**: site düzeyi |
| 3.2.4 Tutarlı tanımlama | AA | Aynı işlev aynı adla ("Kaydet" her yerde "Kaydet") | **kaynak**: buton/link metinleri |
| 3.2.6 Tutarlı yardım | A | Yardım linki/iletişim her sayfada aynı yerde | **kaynak**: site düzeyi |
| 3.3.3 Hata önerisi | AA | Hata biliniyorsa düzeltme önerisi | **kaynak** (U3 ile örtüşür) |
| 3.3.4 Hata önleme (yasal/finans/veri) | AA | Geri alınabilir / kontrol edilebilir / onaylanabilir | **kaynak** (U5 ile örtüşür) |
| 3.3.7 Tekrarlı giriş | A | Aynı bilgi aynı süreçte ikinci kez istenmez | **kaynak**: çok adımlı form |
| 3.3.8 Erişilebilir kimlik doğrulama | AA | Giriş bilişsel test istemez; yapıştırma serbest, parola yöneticisi çalışır | **kaynak**: `onpaste` engeli, CAPTCHA |

## Notlar
- **2.3.3 Etkileşimden doğan animasyon AAA'dır**; A10 bunu iyi uygulama olarak ister (`prefers-reduced-motion`), AA gereği değil. AA gereği 2.2.2 (durdurulabilir hareket) ve 2.3.1 (flaş).
- **3.2.5 Talep üzerine değişim AAA**; W3C BAD karşılaştırmasında sayıldı ama AA kapsamında değil.
