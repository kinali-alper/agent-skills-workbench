# Tetik ölçümü — `ux-a11y-review` description'ı

**Soru:** Skill'in `description` alanı, kullanıcı niyeti eşleştiğinde skill'i çağırtıyor mu; eşleşmediğinde (yakın komşu istekler) çağırtmıyor mu?
Yöntem skill-creator'ın "Description Optimization" akışından türetildi; yalnız **ölçüm** yapıldı, otomatik iyileştirme döngüsü (`run_loop.py`) çalıştırılmadı — description değişikliği kullanıcıya öneri olarak sunulur.

## Ön-kayıt (koşudan önce yazıldı — 2026-09-21)

- **Sorgu seti:** `trigger-eval.json` — 20 sorgu: 10 tetiklemeli (TR/EN; anahtar kelimeli 1, niyet ifadeli 9; yol veren 4, yol vermeyen 6), 10 tetiklememeli **yakın komşu** (düzenleme isteği → `wq-accessibility`, performans → `wq-performance`, SEO → `wq-seo`, görsel tasarım → tasarım skill'leri, bilgi sorusu, kullanıcı testi planı → `ux-designer`, araç yazımı, bug).
  Her tetiklememeli sorgunun `tag`'inde hangi skill'in kazanması gerektiği yazılı; kazanan rakip bulgunun parçasıdır.
- **Ortam:** `claude -p --model claude-opus-5 --max-turns 6 --disallowedTools Edit,Write,MultiEdit,NotebookEdit`; 5 dosyalık gerçekçi React+Vite iskeleti (README'de formun yolu), fixture = `evals/cases/broken-form/BrokenForm.tsx` → `src/pages/RegisterForm.tsx`; skill, skill-creator yöntemiyle `.claude/commands/<ad>-skill-<uid>.md` olarak sunulur; her worker ayrı proje kopyası (paralel koşular birbirinin komut dosyasını görmez). Kurulu gerçek `ux-a11y-review` ölçüm süresince kaldırıldı; diğer 27 skill (rakipler dahil) kurulu kaldı.
- **Metrikler (koşu başına):**
  - `first` — modelin **ilk** araç çağrısı skill (skill-creator'ın özgün metriği; "description ne kadar itici" teşhisi).
  - `any` — skill 6 tur içinde herhangi bir araç çağrısında çağrıldı.
  - `self_read` — model komut dosyasını kendisi okudu (`.claude/commands/…`) → o koşu **geçersiz örnek**; `any_clean = any / (n − self_read)`.
  - `ended` — `success` / `error_max_turns` (kesildi) / `timeout`.
- **Tekrar:** n = 3 koşu/sorgu; eşik 0.5 (≥ 2/3 → "tetikledi").
- **Kabul kuralı (any_clean):** tetiklemeli ≥ 8/10 **ve** tetiklememeli ≥ 8/10 → description olduğu gibi kalır. Altındaysa başarısızlar tek tek incelenir ve **öneri** yazılır; skill dosyası bu koşuda düzenlenmez.
- **Bilinen artefakt:** boş/ince projede model önce keşif yapar (`ls`, `find`, `Read`) → `first` düşük çıkar; `any_clean` asıl kapı.

## Dosyalar
- `trigger_eval.py` — koşucu (Windows uyumlu: `select()` yerine okuyucu iş parçacığı, `claude.cmd`, `PYTHONUTF8=1`; iki metrik; worker izolasyonu). Kanıt aracıdır, ürün değil (`scripts/` altında değil).
- `trigger-eval.json` — sorgu seti. `results.json` — ham sonuç (sorgu başına araç dizisi, çağrılan skill'ler, bitiş nedeni, maliyet).
  `skill_turns` = skill'in çağrıldığı **araç çağrısı sırası** (bir asistan mesajı birden çok araç çağırabilir), CLI turu değil — bu yüzden `max_turns: 6` yanında 8 veya 10 görülebilir.
- Koşucu, fixture'ı her koşuda yeniden kopyalamak için `--project-root` ile verilen özgün klasörü kullanır; worker kopyaları `<root>-w0..N` adıyla yanına açılır ve sonda silinir.

## Sonuç (koşu sonrası eklendi — 2026-09-21)

60 koşu, $22.3. Tablo ve yorum: [`../RESULTS.md` → "Trigger measurement"](../RESULTS.md). Kısa:
- Tetiklememeli 10/10 geçti — **30 koşuda 0 yanlış tetik**; rakipler etikette yazıldığı gibi kazandı.
- Yol veren tetiklemeliler 3/3 geçti. Yol vermeyenler için **hüküm yok**: 15/15 koşuda model `find` ile `.claude/commands/` dosyasını buldu, okudu, sonra skill'i çağırdı (`self_read` → geçersiz örnek). Yöntem artefaktı.
- `first` metriği 60 koşuda 0 — bu model/harness'te ilk eylem hep keşif; metrik bilgi taşımıyor.
- q6 (yalnız Nielsen/kullanılabilirlik isteği) `heuristic-evaluation`'a gitti — muhtemelen doğru yönlendirme, etiket tartışmalı.
- **Kabul kuralı yazıldığı gibi karşılanmadı** (3/10) ama 7 kayıptan 6'sı "örnek yok". Description **düzenlenmedi**; öneri: komut dosyasını proje dışına koyup yalnız yol vermeyen 6 sorguyu yeniden koş (~$8).

## G1 — yol vermeyen sorgular, komut dosyası proje DIŞINDA (16 Eki 2026)

İlk koşunun artefaktını kaldırmak için test komutu `~/.claude/commands` altına yazıldı (`--commands-dir`);
böylece model projeyi listeleyerek komut dosyasını bulamıyor. Sorgu seti: ilk turun **6 yol vermeyen tetiklemeli**
sorgusu (`g1-nopath.json`), aynı model (claude-opus-5), aynı eşik (0,5), 3 koşu, `--max-turns 6`, gerçek skill
yine kaldırıldı, rakipler kurulu.

| Etiket | first | any_clean | Skill'in çağrıldığı araç sırası | Bitiş |
|---|---|---|---|---|
| TR·intent·nopath | 0/3 | **3/3** | 6, 6, 7 | kesildi, kesildi, ok |
| TR·intent·nopath | 0/3 | **2/3** | —, 5, 5 | kesildi, kesildi, ok |
| TR·blindspot·nopath | 0/3 | **3/3** | 7, 5, 5 | kesildi ×3 |
| TR·nielsen·nopath | 0/3 | **2/3** | 5, —, 5 | kesildi ×3 |
| EN·intent·nopath | 0/3 | **3/3** | 6, 6, 7 | kesildi ×3 |
| EN·detail·nopath | 0/3 | **3/3** | 7, 7, 6 | ok ×3 |

**Sonuç: 6/6 geçti.** `self_read` **0/18** → artefakt tamamen kalktı; yani ilk turdaki "hüküm yok" durumu gerçekten
yöntemden geliyordu, description'dan değil. **Yol vermeyen istekler de skill'i tetikliyor.**
Ön-kayıtlı kabul kuralı artık karşılanıyor: tetiklemeli **9/10** (G1'in 6'sı + ilk turun yol veren 3'ü), tetiklememeli **10/10**. Kalan 1 sorgu q1
("Arayüzü denetle: <yol>" — çıplak anahtar kelime) **başarısız**: tek geçerli koşuda tetiklemedi, bir koşuda
`web-design-guidelines` kazandı. n = 1 olduğu için zayıf kanıt; istenirse G1 yöntemiyle tekrar ölçülür (~$3).

`first` metriği yine **0/18** — bu model/harness'te skill hiçbir zaman ilk araç çağrısı olmuyor; metrik ölü.

**Maliyet: $20,54** (18 koşu, koşu başına ~$1,14). İlk turun aynı sorgularındaki ölçüme göre tahmin ~$7'ydi;
**3 kat aştı**. Sebep ölçülebilir: komut dosyası projede bulunamadığı için model daha uzun keşif yaptı ve
**18 koşunun 13'ü `--max-turns 6` sınırına dayandı** (ilk turda bu oran 26/60'tı). Ders: artefaktı kaldırmak
maliyeti artırıyor; bir sonraki tetik ölçümünde tur bütçesi ve maliyet tahmini buna göre kurulmalı.

**G1 dosyaları:** `g1-nopath.json` (6 sorgu), `g1-results.json` (ham sonuç). Tek düzenleme: `commands_dir` alanındaki
makine yolu `~/.claude/commands` olarak normalleştirildi (`publish-check.sh` kuralı); ölçümü etkilemez.

