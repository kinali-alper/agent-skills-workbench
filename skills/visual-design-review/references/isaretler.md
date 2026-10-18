# G-listesi — betiğin göremediği işaretler, kaynaklarıyla

Adım 3'te okunur. Her satır **tek** hüküm alır (ihlal :N / uygun / uygulanamaz / doğrulanamaz) ve her ihlal
"yerine ne" ile yazılır. Kaynak sütunu: iddianın geldiği **herkese açık** belge. Kaynağı olmayan eşik `[öneri]`
diye işaretlidir ve bu depoda bağımsız olarak ölçülmemiştir — tartışmaya açıktır.

| G | Kontrol (ne aranıyor) | Yerine ne | Kaynak |
|---|---|---|---|
| G1 | **Hiyerarşi kareden okunuyor**: ekranda bir birincil eylem ve bir birincil mesaj var; göz nereye gideceğini bulur | Başlık–gövde arasını belirgin aç, ikincil eylemleri sadeleştir, tek birincil düğme | Anthropic frontend-design: "Use extremes: 100/200 weight vs 800/900, not 400 vs 600. Size jumps of 3x+, not 1.5x." (claude.com/blog/improving-frontend-design-through-skills) |
| G2 | **Yazı ölçeği basamaklı**: boyutlar bir ölçekten geliyor, keyfî değil; ekranda az sayıda boyut | 6–8 basamaklı ölçek kur, belirteçle (`--step-*`) kullan; ekranda ~3 boyutu geçme | NN/g görsel hiyerarşi (en çok 3 yazı boyutu önerisi); Utopia ölçek üreticisi `[öneri]` eşik |
| G3 | **Tipografi bilinçli seçilmiş**: başlık ve metin yüzü ürüne uygun, varsayılan değil; Türkçe glifleri taşıyor | Bir karakterli başlık + bir metin yüzü, ikisi de ğ ş ı İ taşıyor; varsayılanı bilinçli seçiyorsan gerekçesini yaz | Anthropic frontend-design: "Never use: Inter, Roboto, Open Sans, Lato, default system fonts" |
| G4 | **Tek vurgu rengi, küçük alan**: vurgu bir iş yapıyor (eylem), dekorasyon değil | Vurguyu yalnız birincil eyleme ve duruma ayır; nötrlerle kur | Vercel Web Interface Guidelines (vercel.com/design/guidelines) · alan payı %5–10 `[öneri]` |
| G5 | **Degrade ve cam ölçülü**: varsa bir yerde, bir nedenle; metin altında bulanıklık yok | Degradeyi tek yerde kullan, algısal uzayda interpole et; camı yalnız üst üste binen yüzeyde | Adam Wathan (2026-08-07, x.com/adamwathan): "leading to every AI generated UI on earth also being indigo." · `avoid-ai-design` README (ikinci kuşak: krem + serif + terrakota) |
| G6 | **Yüzey çeşitliliği sınırlı**: köşe yarıçapı ve gölge birkaç değerden; kart kromu her yerde aynı değil | En çok 3 yarıçap (girdi/kart/hap), en çok 3 gölge; gölgeyi iki katman kur (ortam + yön) | Vercel guidelines: "Child radius ≤ parent radius & concentric so curves align." · sayı eşiği `[öneri]` |
| G7 | **Yerleşim içerikten geliyor**: üç eş kart / bento duvarı / tam ortalanmış simetri varsayılan değil | Asimetrik ızgara (12 kolon, metin 2/9, görsel 9/13); bento'da çapa döşeme ve boyut hiyerarşisi | `avoid-ai-design` README · bento boyut hiyerarşisi `[öneri]` |
| G8 | **İlk ekranda ürünün kendisi**: ekran görüntüsü, gerçek veri, gerçek çıktı — yalnız slogan değil | Kahraman alanına ürünün gerçek bir ekranını/çıktısını koy | Vercel guidelines (durum tasarımı ilkesi) · `[öneri]` |
| G9 | **Üslup birliği**: fotoğraf + düz vektör + çizgisel SVG aynı ekranda karışmıyor; görseller tek palet/ışık/kadraj | Tek üslup seç; görselleri tek renk derecelendirmesi ve tek kadraj oranıyla üret | `[öneri]` (bu depoda ölçülmedi) |
| G10 | **İkon disiplini**: tek set, tek çizgi kalınlığı, boyuta göre ayarlı; "AI için parıltı" ikonu yok | Tek set (ör. 24 px tuval, 2 px çizgi, yuvarlak uç); 16 px'te çizgiyi kalınlaştır, ≥ 32 px'te incelt | Lucide ikon spesifikasyonu (lucide.dev/contribute/icons/specification): "Strokes **must** be 2 pixels wide." |
| G11 | **Mikro metin ürünü anlatıyor**: başlık ne yaptığını söylüyor; "Keşfet / Güçlendir / Harika!" yok; hata metni ne yanlış + nasıl düzelir diyor | Somut Türkçe başlık; eylem adı eylemi söylüyor; hata metni çözüm veriyor | Vercel guidelines: "Don't just state what went wrong—tell the user how to fix it." |
| G12 | **Kip uyumu**: panelde dekoratif hareket/görsel yok; tanıtımda tek anlamlı hareket var; okuma yüzeyinde satır uzunluğu ve ritim korunuyor | Kipi adım 1'de yaz, eşikleri ona göre uygula | `baseline-ui` (kurulu): "NEVER add animation unless it is explicitly requested" (panel) · Impeccable'ın yüzey kipi fikri (yalnız fikir ödünç alındı, kurulmadı) |

## Notlar
- **Tek işaret zayıftır.** Hüküm işaretlerin bir aradalığına dayanır; hedef 0–1 işaret.
- Bu liste **proje bağımsızdır**: belirli bir ürünün ya da kişinin zevkini içermez. Bir kural yalnız bir ekibin
  beğenisinden geliyorsa buraya değil, o projenin kendi belgesine yazılır.
- `[öneri]` eşikleri 2026 web tasarımı araştırmasının cevaplarından gelir; o cevapların ölçülmüş etkisi tek model
  ailesinden geldiği için bu depoda **kanıt** sayılmaz. Gerçek projede yanlış pozitif verirlerse eşik tartışılır.
