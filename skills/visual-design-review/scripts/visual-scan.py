#!/usr/bin/env python3
"""visual-scan.py — bir arayüzün kaynağından sayılabilir "yapay zekâ işi" işaretlerini sayar. Rapor üretir, dosya düzenlemez.

Kullanım:
    python visual-scan.py <dosya|klasör> [...]        # insan okur
    python visual-scan.py --json <yol>                # makine okur
Çıkış kodu: 0 = temiz (0–1 işaret) · 2 = işaret bulundu (≥ 2) · 1 = kullanım hatası.

Yalnız standart kütüphane; ağ çağrısı, alt süreç ve dosya yazma yok.

Statik tarama. **Göremediği şeyler** (raporun sonunda da yazılır):
  - Tailwind/utility sınıfları: `text-3xl`, `rounded-xl` gibi sınıflar `font-size:` bildirimi üretmez → boyut/yarıçap
    sayımı bu projelerde eksik kalır. Sınıf adlarından tahmin YAPILMAZ (yanlış sayımdan iyidir).
  - Hesaplanmış stiller, kalıtım, cascade sonucu: yalnız yazılan bildirim görülür.
  - Vurgu renginin alan payı ve gerçek glif yedeklemesi: ekran görüntüsü/render gerekir.
  - Hiyerarşi, yerleşim, üslup birliği, mikro metin: bunlar skill'in insan/model adımlarında değerlendirilir.

Eşiklerin yanında kaynağı yazar:
  [kaynak] = dış belgede doğrulanmış (MDN, web.dev, WCAG, Material, Lucide, Vercel guidelines)
  [öneri]  = 2026 web tasarımı araştırmasının önerisi; bağımsız olarak ölçülmedi, eşik tartışmaya açık
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

EXT = {".css", ".scss", ".html", ".htm", ".cshtml", ".razor", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte"}
SKIP_DIR = {"node_modules", ".git", "dist", "build", ".next", "venv", ".venv", "__pycache__"}

# ---------------------------------------------------------------- renk yardımcıları


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_oklch(hx: str) -> tuple[float, float, float] | None:
    """#rgb / #rrggbb → (L, C, H). Oklab dönüşümü: Björn Ottosson'un yayımladığı matrisler.

    Doğrulama (Tailwind v4 slate, yayımlanmış oklch değerleriyle): #f8fafc → 0.9842 0.0034 247.9 (yayımlanan
    .984 .003 247.858) · #64748b → 0.5544 0.0407 257.4 (.554 .046 257.4) · #0f172a → 0.2077 0.0398 265.8
    (.208 .042 265.8). L ve H birebir; **krom ~%10 düşük çıkıyor** çünkü hex sRGB'ye kırpılmış bir geri dönüş.
    Bu yüzden krom eşiği sert kapı değil, gösterge sayılır; saf gri tespiti (C = 0) etkilenmiyor.
    """
    h = hx.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6 or re.search(r"[^0-9a-fA-F]", h):
        return None
    r, g, b = (_srgb_to_linear(int(h[i : i + 2], 16) / 255) for i in (0, 2, 4))
    l_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m_ = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    C = math.hypot(a, bb)
    H = math.degrees(math.atan2(bb, a)) % 360
    return round(L, 4), round(C, 4), round(H, 1)


# ---------------------------------------------------------------- desenler

RX = {
    "font_size": re.compile(r"font-size\s*:\s*([0-9.]+)(px|rem|em|pt)", re.I),
    "radius": re.compile(r"border-radius\s*:\s*([^;}\n]+)", re.I),
    "shadow": re.compile(r"box-shadow\s*:\s*([^;}\n]+)", re.I),
    "transition_all": re.compile(r"transition\s*:\s*all\b", re.I),
    "duration": re.compile(r"(?:transition|animation)(?:-duration)?\s*:[^;}\n]*?([0-9.]+)(ms|s)\b", re.I),
    "layout_anim": re.compile(
        r"transition(?:-property)?\s*:[^;}\n]*\b(width|height|top|left|right|bottom|margin|padding)\b", re.I
    ),
    "backdrop": re.compile(r"backdrop-filter\s*:", re.I),
    "will_change": re.compile(r"will-change\s*:|translateZ\(\s*0", re.I),
    "gradient": re.compile(r"(linear|radial|conic)-gradient\(", re.I),
    "gradient_space": re.compile(r"(linear|radial|conic)-gradient\(\s*in\s+(oklab|oklch|lab|lch)", re.I),
    "fontface": re.compile(r"@font-face\s*\{([^}]*)\}", re.I | re.S),
    "hex": re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b"),
    "oklch": re.compile(r"oklch\(\s*([0-9.]+%?)\s+([0-9.]+)\s+([0-9.]+)", re.I),
    "spacing": re.compile(r"(?:margin|padding|gap|row-gap|column-gap)[a-z-]*\s*:\s*([^;}\n]+)", re.I),
    "lang": re.compile(r"<html[^>]*\blang\s*=\s*[\"']([a-zA-Z-]+)", re.I),
    "lang_attr_any": re.compile(r"\blang\s*=\s*[\"']([a-zA-Z-]+)", re.I),
    "uppercase": re.compile(r"text-transform\s*:\s*uppercase", re.I),
    "focus_remove": re.compile(r"outline\s*:\s*(?:none|0)\b", re.I),
    "focus_visible": re.compile(r":focus-visible", re.I),
    "generic_font": re.compile(r"font-family\s*:[^;}\n]*\b(Inter|Roboto|Open Sans|Lato|Poppins|Space Grotesk)\b", re.I),
    "ai_purple": re.compile(r"\b(indigo|violet|purple|fuchsia)-[2-9]00\b|from-(purple|indigo|violet)", re.I),
    "px_len": re.compile(r"(-?[0-9.]+)px"),
    "tr_glyphs": re.compile(r"[ĞğİıŞşÇçÖöÜü]"),
    "unicode_range": re.compile(r"unicode-range\s*:\s*([^;}\n]+)", re.I),
    "utility_size": re.compile(r"\b(text-(xs|sm|base|lg|xl|[2-9]xl)|rounded-(sm|md|lg|xl|[2-9]xl|full))\b"),
}

TR_RANGES = ("011e", "011f", "0130", "0131", "015e", "015f")


def gather(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if p.is_file():
            out.append(p)
        else:
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix.lower() in EXT and not any(d in f.parts for d in SKIP_DIR):
                    out.append(f)
    return out


def scan(files: list[Path]) -> dict:
    t = {}
    text = {}
    for f in files:
        try:
            text[f] = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
    blob = "\n".join(text.values())

    # 1. tipografi disiplini
    sizes = {f"{float(v)}{u.lower()}" for v, u in RX["font_size"].findall(blob)}
    t["font_size_count"] = len(sizes)
    t["font_sizes"] = sorted(sizes)
    t["utility_classes"] = len(RX["utility_size"].findall(blob))

    # 2. yüzey çeşitliliği
    t["radius_count"] = len({v.strip().lower() for v in RX["radius"].findall(blob)})
    t["shadow_count"] = len({v.strip().lower() for v in RX["shadow"].findall(blob) if v.strip().lower() != "none"})

    # 3. hareket
    t["transition_all"] = len(RX["transition_all"].findall(blob))
    slow = []
    for v, unit in RX["duration"].findall(blob):
        ms = float(v) * (1000 if unit.lower() == "s" else 1)
        if ms > 400:
            slow.append(int(ms))
    t["slow_transitions"] = sorted(slow, reverse=True)
    t["layout_anim"] = len(RX["layout_anim"].findall(blob))
    t["will_change"] = len(RX["will_change"].findall(blob))
    t["backdrop_filter"] = len(RX["backdrop"].findall(blob))

    # 4. renk
    grads = len(RX["gradient"].findall(blob))
    t["gradients"] = grads
    t["gradients_in_perceptual"] = len(RX["gradient_space"].findall(blob))
    hexes = set(RX["hex"].findall(blob))
    t["hex_count"] = len(hexes)
    t["oklch_count"] = len(RX["oklch"].findall(blob))
    chroma = []
    for hx in hexes:
        conv = hex_to_oklch(hx)
        if conv and conv[1] < 0.05:  # nötr aday
            chroma.append(conv[1])
    for _l, c, _h in RX["oklch"].findall(blob):
        cv = float(c)
        if cv < 0.05:
            chroma.append(cv)
    t["neutral_count"] = len(chroma)
    t["neutral_chroma_median"] = round(sorted(chroma)[len(chroma) // 2], 4) if chroma else None
    t["pure_gray_count"] = sum(1 for c in chroma if c < 0.002)

    # 5. boşluk ölçeği
    vals = []
    for decl in RX["spacing"].findall(blob):
        for m in RX["px_len"].findall(decl):
            v = abs(float(m))
            if v:
                vals.append(v)
    t["spacing_values"] = len(vals)
    if vals:
        base = 4 if sum(1 for v in vals if v % 4 == 0) >= sum(1 for v in vals if v % 8 == 0) else 8
        on = sum(1 for v in vals if v % base == 0)
        t["spacing_base"] = base
        t["spacing_conformity"] = round(100 * on / len(vals))
    else:
        t["spacing_base"] = None
        t["spacing_conformity"] = None

    # 6. yazı tipi yükleme
    all_faces = RX["fontface"].findall(blob)
    # yalnız `src: local(...)` olan yüz, metrik eşleme için yazılmış yedektir; font-display beklenmez
    faces = [b for b in all_faces if re.search(r"url\(", b, re.I)]
    t["fontface_count"] = len(faces)
    t["fallback_faces"] = len(all_faces) - len(faces)
    t["fontface_with_display"] = sum(1 for b in faces if re.search(r"font-display", b, re.I))
    t["fontface_with_size_adjust"] = sum(1 for b in all_faces if re.search(r"size-adjust", b, re.I))
    ur = " ".join(RX["unicode_range"].findall(blob)).lower()
    t["unicode_range_covers_tr"] = (not ur) or all(r in ur for r in TR_RANGES) or "u+0100-017f" in ur.replace(" ", "")

    # 7. Türkçe
    langs = RX["lang"].findall(blob)
    t["html_lang"] = langs[0].lower() if langs else None
    t["uppercase_rules"] = len(RX["uppercase"].findall(blob))
    t["has_tr_text"] = bool(RX["tr_glyphs"].search(blob))
    t["lang_en_islands"] = sum(1 for l in RX["lang_attr_any"].findall(blob) if l.lower().startswith("en"))

    # 8. odak + klişe
    t["outline_none"] = len(RX["focus_remove"].findall(blob))
    t["focus_visible"] = len(RX["focus_visible"].findall(blob))
    t["generic_font"] = len(RX["generic_font"].findall(blob))
    # Mor/indigo aile: sınıf adı (indigo-500, from-purple) VE doygun hex/oklch renklerin hue'su (255–330°).
    # Sınıf adı tek başına yetmiyordu: hex yazımı (#7c3aed) gözden kaçıyordu.
    purple_hues = []
    for hx in hexes:
        conv = hex_to_oklch(hx)
        if conv and conv[1] >= 0.08 and 255 <= conv[2] <= 330:
            purple_hues.append(hx)
    for _l, c, h in RX["oklch"].findall(blob):
        if float(c) >= 0.08 and 255 <= float(h) <= 330:
            purple_hues.append(f"oklch(… {h})")
    t["ai_purple"] = len(RX["ai_purple"].findall(blob))
    t["purple_colors"] = sorted(set(purple_hues))
    t["files"] = len(text)
    return t


# her hüküm: (durum, mesaj, provenans). Mesaj duruma göre ayrı yazılır — geçen satır kendi olumlu hâlini söyler.
def verdicts(t: dict) -> list[tuple[str, str, str]]:
    v: list[tuple[str, str, str]] = []

    def judge(flag: bool, fail: str, ok: str, prov: str, soft: bool = False):
        if flag:
            v.append(("isaret" if not soft else "bilgi", fail, prov))
        else:
            v.append(("uygun", ok, prov))

    # tipografi disiplini
    if t["font_size_count"] == 0:
        v.append(("uygulanamaz", f"Ayrı `font-size` bildirimi yok (utility sınıfı: {t['utility_classes']}) — boyut disiplini statik ölçülemedi", "[öneri]"))
    else:
        n = t["font_size_count"]
        judge(n > 12, f"Ayrı font boyutu {n} — keyfî ölçek (≤ 8 disiplinli)", f"Ayrı font boyutu {n} — ölçek disiplinli (≤ 8 hedef, > 12 keyfî)", "[öneri]")
    judge(t["radius_count"] > 3, f"Ayrı `border-radius` değeri {t['radius_count']} — en çok 3 olmalı (ör. 4 px girdi, 8 px kart, 999 px hap)", f"Ayrı `border-radius` değeri {t['radius_count']} (≤ 3)", "[öneri]")
    judge(t["shadow_count"] > 3, f"Ayrı `box-shadow` değeri {t['shadow_count']} — en çok 3 olmalı", f"Ayrı `box-shadow` değeri {t['shadow_count']} (≤ 3)", "[öneri]")

    # hareket
    judge(t["transition_all"] > 0, f"`transition: all` {t['transition_all']} yerde — yalnız değişen özelliği yaz", "`transition: all` yok", "[kaynak]")
    judge(bool(t["slow_transitions"]), f"400 ms üstü geçiş {len(t['slow_transitions'])} adet ({t['slow_transitions'][:5]} ms) — günlük arayüzde 120–250 ms", "400 ms üstü geçiş yok", "[kaynak]")
    judge(t["layout_anim"] > 0, f"Yerleşimi oynatan geçiş {t['layout_anim']} adet (width/height/top/left/margin/padding) — yalnız `transform`/`opacity` animasyonla", "Geçişler yalnız yerleşimi oynatmayan özelliklerde", "[kaynak]")
    judge(t["will_change"] > 0, f"CSS'te kalıcı `will-change`/`translateZ(0)` {t['will_change']} adet — animasyon süresince aç, sonra kaldır", "Kalıcı `will-change` yok", "[kaynak]", soft=t["will_change"] <= 2)
    judge(t["backdrop_filter"] > 2, f"`backdrop-filter` {t['backdrop_filter']} yerde — varsayılan buzlu cam işareti; yalnız üst üste binen yüzeyde kullan", f"`backdrop-filter` {t['backdrop_filter']} yerde (ölçülü)", "[öneri]")

    # renk
    if t["gradients"]:
        judge(t["gradients_in_perceptual"] == 0, f"{t['gradients']} degradenin hiçbiri `in oklab/oklch` ile interpolasyonlu değil — sRGB'de orta ton griye düşer", f"Degradelerin {t['gradients_in_perceptual']}/{t['gradients']} tanesi algısal uzayda interpolasyonlu", "[kaynak]")
    if t["neutral_count"]:
        judge(t["pure_gray_count"] > 0, f"Saf gri nötr {t['pure_gray_count']}/{t['neutral_count']} (krom < 0,002) — nötrleri hafif tonla (0,003–0,046)", f"Nötrler tonlanmış: {t['neutral_count']} nötr, medyan krom {t['neutral_chroma_median']}", "[öneri]")

    # boşluk
    if t["spacing_conformity"] is not None:
        judge(t["spacing_conformity"] < 90, f"Boşluk ölçeğine uyum %{t['spacing_conformity']} ({t['spacing_base']} px tabanı, {t['spacing_values']} değer) — ≥ %90 hedef", f"Boşluk ölçeğine uyum %{t['spacing_conformity']} ({t['spacing_base']} px tabanı)", "[öneri]")

    # yazı tipi yükleme
    if t["fontface_count"]:
        eksik = t["fontface_count"] - t["fontface_with_display"]
        judge(eksik > 0, f"`font-display` yazılmayan `@font-face` {eksik}/{t['fontface_count']} — gövdede `optional`, başlıkta `swap`", f"Her `@font-face` (`{t['fontface_count']}`) `font-display` taşıyor", "[kaynak]")
        judge(t["fontface_with_size_adjust"] == 0, f"Yedek yazı tipinde `size-adjust` yok ({t['fontface_count']} web yüzü) — yazı tipi gelince metin sıçrar", f"Yedek yüzde `size-adjust` var ({t['fontface_with_size_adjust']})", "[kaynak]", soft=True)
        judge(not t["unicode_range_covers_tr"], "`unicode-range` Türkçe gliflerini (U+011E/011F, 0130/0131, 015E/015F) kapsamıyor — Latin Extended-A ekle", "`unicode-range` Türkçe gliflerini kapsıyor", "[kaynak]")

    # Türkçe
    if t["has_tr_text"] or t["uppercase_rules"]:
        lang = t["html_lang"]
        tr_ok = bool(lang and lang.startswith("tr"))
        judge(lang is None, "`<html lang>` yok — Türkçe sayfada `lang=\"tr\"` şart", f"`<html lang>` = {lang!r}", "[kaynak]")
        if t["uppercase_rules"]:
            judge(not tr_ok, f"`text-transform: uppercase` {t['uppercase_rules']} yerde ama `lang` = {lang!r} — 'iletişim' ILETISIM olur (doğrusu İLETİŞİM)", f"`text-transform: uppercase` {t['uppercase_rules']} yerde ve `lang=tr` doğru — büyük harf Türkçe kurala göre", "[kaynak]")

    # odak + klişe
    judge(t["outline_none"] > t["focus_visible"], f"`outline: none` {t['outline_none']} yerde, `:focus-visible` {t['focus_visible']} yerde — odak halkası kayboluyor", f"Odak halkası korunuyor (`:focus-visible` {t['focus_visible']}, `outline: none` {t['outline_none']})", "[kaynak]")
    judge(t["generic_font"] > 0, f"Varsayılan yazı tipi ailesi bildirimi {t['generic_font']} (Inter/Roboto/Poppins/Space Grotesk…) — bilinçli seçim değilse değiştir", "Varsayılan yazı tipi ailesi bildirimi yok", "[kaynak]")
    pc = t.get("purple_colors", [])
    judge(t["ai_purple"] > 0 or len(pc) > 0,
          f"Mor/indigo ailesinde renk: sınıf {t['ai_purple']}, doygun değer {len(pc)} ({', '.join(pc[:4])}) — markanın bilinçli kararı değilse paleti markadan türet",
          "Mor/indigo varsayılan vurgu yok", "[kaynak]")
    return v


NOTES = """Statik taramanın göremediği (elle ya da render ile bakılacak):
  - Tailwind/utility sınıfları boyut ve radius sayımına girmez (bu koşuda {util} utility sınıfı görüldü).
  - Vurgu renginin alan payı (%5–10 hedefi) → ekran görüntüsünde piksel ölçümü gerekir.
  - Gerçek glif yedeklemesi: `İSTANBUL ılık şğüöç` dizgesini 16 px ve 64 px'te render edip yedek yazı tipine
    düşen karakter var mı diye bak.
  - Hiyerarşi, yerleşim, üslup birliği, mikro metin: skill'in 3. ve 4. adımında değerlendirilir."""


def main() -> int:
    ap = argparse.ArgumentParser(description="Tasarım işaretlerini kaynak dosyalardan sayar (rapor-only).")
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true", help="Ham ölçümleri JSON yaz")
    a = ap.parse_args()

    files = gather([p for p in a.paths])
    if not files:
        print("Taranacak dosya bulunamadı.", file=sys.stderr)
        return 1
    t = scan(files)
    v = verdicts(t)
    flags = [x for x in v if x[0] == "isaret"]

    if a.json:
        print(json.dumps({"olcumler": t, "hukumler": [{"durum": d, "mesaj": m, "kaynak": k} for d, m, k in v],
                          "isaret_sayisi": len(flags)}, ensure_ascii=False, indent=2))
    else:
        print(f"tasarim_tara · {t['files']} dosya")
        print()
        for durum, msg, prov in v:
            mark = {"isaret": "[İŞARET]", "uygun": "[uygun] ", "bilgi": "[bilgi]  ", "uygulanamaz": "[yok]   "}[durum]
            print(f"  {mark} {msg}  {prov}")
        print()
        print(f"İşaret sayısı: {len(flags)} → " + ("temiz (0–1)" if len(flags) <= 1 else
              "gözden geçir (2–3)" if len(flags) <= 3 else "4+ işaret: yönü baştan düşün"))
        print()
        print(NOTES.format(util=t["utility_classes"]))
    return 0 if len(flags) <= 1 else 2


if __name__ == "__main__":
    sys.exit(main())
