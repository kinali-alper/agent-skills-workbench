#!/usr/bin/env python3
"""pin-sweep.py — vendor pin tazeliğini iki yönlü ölçer. Rapor üretir, hiçbir şeyi değiştirmez.

Her vendor için iki soru, ikisi de blob hash'iyle (okumayla değil):
  A) yerel `SKILL.md` blob'u == **pinlenen** commit'teki blob mu?  → kopyamız sadık mı
  B) pinlenen blob == upstream **HEAD** blob mu?                   → upstream pinin ötesine geçmiş mi
İkisini ayırmak önemli: (A)'daki fark *bizim* değişikliğimizdir ve REVIEW.md'de yazılı olmalı; (B)'deki fark
upstream'ın ilerlediğini söyler — pinlemenin amacı tam budur, inceleme tetikleyicisidir, hata değil.

Kullanım:
    python scripts/pin-sweep.py                 # tablo
    python scripts/pin-sweep.py --json          # makine okur
    GITHUB_TOKEN=... python scripts/pin-sweep.py   # kimliksiz API ~60 çağrı/saat verir, vendor başına 2 çağrı
                                                   # gerekir; 29 vendor için token olmadan son satırlar 403 alır

Kaynak satırı `vendor/<ad>/REVIEW.md` içindeki `| Kaynak | <repo> · [<yol> ·] commit <sha> … |` biçiminden okunur.
Çıkış kodu: 0 = belgesiz sapma yok · 2 = belgesiz sapma var · 1 = kullanım/okuma hatası.
"""
from __future__ import annotations

import argparse
import base64
import difflib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KAYNAK = re.compile(r"^\|\s*Kaynak\s*\|\s*([^\s|·]+)\s*·\s*(.*?)\*{0,2}commit\s*\*{0,2}\s*([0-9a-f]{7,40})", re.M)
# REVIEW.md'de belgelenmiş uyarlamayı arayan ifadeler (biri geçiyorsa fark "belgeli" sayılır)
DOC = re.compile(r"Uyarlama|`name`\s*alanı|name:\s*alanı|description.{0,20}(kısalt|trim)|öneki ile kuruldu", re.I)


def api(url: str, token: str | None):
    headers = {"User-Agent": "pin-sweep", "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=25) as h:
        return json.load(h)


def blob(repo: str, path: str, token: str | None, ref: str | None = None):
    url = f"https://api.github.com/repos/{repo}/contents/{path}" + (f"?ref={ref}" if ref else "")
    try:
        d = api(url, token)
        return d.get("sha"), base64.b64decode(d.get("content", "")).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return f"HTTP{e.code}", ""
    except Exception as e:  # ağ yok, DNS, zaman aşımı
        return type(e).__name__, ""


def diff_lines(a: str, b: str) -> list[str]:
    return [l for l in difflib.unified_diff(a.splitlines(), b.splitlines(), n=0, lineterm="")
            if l[:1] in "+-" and l[:3] not in ("+++", "---")]


def sweep(token: str | None) -> list[dict]:
    out = []
    for d in sorted(p for p in (ROOT / "vendor").iterdir() if p.is_dir()):
        rec = {"vendor": d.name}
        rev, sk = d / "REVIEW.md", d / "SKILL.md"
        if not (rev.exists() and sk.exists()):
            rec["durum"] = "REVIEW/SKILL eksik"
            out.append(rec)
            continue
        t = rev.read_text(encoding="utf-8")
        m = KAYNAK.search(t)
        if not m:
            rec["durum"] = "Kaynak satırı okunamadı"
            out.append(rec)
            continue
        repo, mid, pin = m.group(1), m.group(2).strip(" ·*"), m.group(3)
        path = (mid + "/SKILL.md") if mid else "SKILL.md"
        local_sha = subprocess.run(["git", "hash-object", str(sk)], capture_output=True, text=True,
                                   cwd=ROOT).stdout.strip()
        pin_sha, pin_txt = blob(repo, path, token, pin)
        head_sha, _ = blob(repo, path, token)
        rec.update(repo=repo, path=path, pin=pin, local=local_sha, pin_blob=pin_sha, head_blob=head_sha)

        if pin_sha == local_sha:
            rec["kopya"] = "sadık"
        elif isinstance(pin_sha, str) and not re.fullmatch(r"[0-9a-f]{40}", pin_sha or ""):
            rec["kopya"] = f"okunamadı ({pin_sha})"
        else:
            dl = diff_lines(pin_txt, sk.read_text(encoding="utf-8"))
            meta_only = bool(dl) and all(re.match(r"[+-](name|description|license):", x) for x in dl)
            rec["kopya"] = f"farklı ({len(dl)} satır{', yalnız name/description' if meta_only else ''})"
            rec["belgeli"] = bool(DOC.search(t))
        if head_sha == pin_sha:
            rec["upstream"] = "pin ile aynı"
        elif isinstance(head_sha, str) and not re.fullmatch(r"[0-9a-f]{40}", head_sha or ""):
            rec["upstream"] = f"okunamadı ({head_sha})"
        else:
            rec["upstream"] = "pinin ötesine geçti"
        out.append(rec)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="vendor pin tazeliği (rapor-only)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    rows = sweep(token)

    undocumented = [r["vendor"] for r in rows if r.get("kopya", "").startswith("farklı") and not r.get("belgeli")]
    if a.json:
        print(json.dumps({"satırlar": rows, "belgesiz_sapma": undocumented}, ensure_ascii=False, indent=2))
    else:
        w = max(len(r["vendor"]) for r in rows)
        print(f"{'vendor':<{w}}  {'pin':<9}{'kopya':<40}upstream")
        for r in rows:
            print(f"{r['vendor']:<{w}}  {r.get('pin', '-'):<9}{r.get('kopya', r.get('durum', '?')):<40}{r.get('upstream', '-')}")
        faithful = sum(1 for r in rows if r.get("kopya") == "sadık")
        diff_doc = sum(1 for r in rows if r.get("kopya", "").startswith("farklı") and r.get("belgeli"))
        unread = [r["vendor"] for r in rows if "okunam" in str(r.get("kopya", r.get("durum", "")))]
        moved = [r["vendor"] for r in rows if r.get("upstream") == "pinin ötesine geçti"]
        print()
        print(f"{len(rows)} vendor · sadık {faithful} · belgeli uyarlama {diff_doc} · belgesiz sapma {len(undocumented)} {undocumented or ''}")
        print(f"upstream pinin ötesine geçti: {len(moved)} {moved or ''} · okunamadı {len(unread)} {unread or ''}")
        if unread and not token:
            print("not: GITHUB_TOKEN verilirse kimliksiz ~60 çağrı/saat sınırı kalkar (vendor başına 2 çağrı gerekir).")
    return 2 if undocumented else 0


if __name__ == "__main__":
    sys.exit(main())
