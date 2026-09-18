# Türkçe arayüz notları

Adım 1'de arayüz dili Türkçe tespit edildiğinde okunur. Kurallar SKILL.md'de; burada yalnız Türkçe örnekler.

## Link ve buton metni (U8 · H2)
| ❌ | ✅ |
|---|---|
| buraya tıklayın | Kayıt koşullarını görüntüle |
| devamı | Duyurunun tamamını oku |
| tıkla / bas | Ödevi gönder |
| Tamam / Devam | Kaydı onayla |
| 🗑 (adsız) | `aria-label="Formu temizle"` |

## Hata metni (U3 · H9)
| ❌ | ✅ |
|---|---|
| Geçersiz değer | Kimlik numarası 11 rakam olmalı (örn. 12345678901) |
| Hata oluştu | Kayıt gönderilemedi. Bağlantınızı kontrol edip yeniden deneyin |
| Zorunlu alan | E-posta adresi gerekli — onay bu adrese gidecek |

## Durum mesajı (U1 · H1)
"Kaydediliyor…" → "Kayıt alındı. Onay e-postası gönderildi." / "Kayıt yapılamadı: kimlik numarası alanını düzeltin."

## Zorunlu / hata ayrımı (U4)
Zorunlu: etiket sonunda `*` + form başında "* ile işaretli alanlar zorunludur".
Hata: kırmızı kenarlık **+** ikon **+** alan altında metin. İki sinyal aynı rengi paylaşıyorsa metinle ayrıl.

## Tipografi
Üç nokta `…` (tek karakter); ölçü birimleriyle bölünmez boşluk: `10&nbsp;MB`.
