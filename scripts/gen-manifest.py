#!/usr/bin/env python3
"""vendor/*/REVIEW.md + SKILL.md + AUDIT-ALLOW + vendor/.audit-status'tan vendor/MANIFEST.md üretir.
Çalıştırma: bash scripts/gen-manifest.sh  (audit'i koşar, durum dosyasını yazar, sonra bu betiği çağırır). Elle düzenlenmez."""
import re, pathlib
V = pathlib.Path(__file__).resolve().parent.parent / 'vendor'
STATUS = {}
sf = V/'.audit-status'
if sf.exists():
    for l in sf.read_text(encoding='utf-8').splitlines():
        if ' ' in l: n, r = l.split(' ', 1); STATUS[n] = int(r) if r.strip().isdigit() else '?'
rows = []
for d in sorted(p for p in V.iterdir() if p.is_dir()):
    rev = (d/'REVIEW.md').read_text(encoding='utf-8')
    sk  = (d/'SKILL.md').read_text(encoding='utf-8')
    cell = lambda k: (re.search(rf'^\| {re.escape(k)} \| (.*?) \|\s*$', rev, re.M) or [None, '—'])[1]
    kaynak = cell('Kaynak')
    repo = (re.search(r'([\w.-]+/[\w.-]+)', kaynak) or [None,'—'])[1]
    pin  = (re.search(r'commit ([0-9a-f]{7})\*{0,2} \((\d{4}-\d{2}-\d{2})\)', kaynak) or re.search(r'commit ([0-9a-f]{7}) \((\d{4}-\d{2}(?:-\d{2})?)\)', kaynak))
    pin_s = f'`{pin.group(1)}` {pin.group(2)}' if pin else '—'
    lic = 'Apache-2.0' if 'Apache' in kaynak else ('MIT' if 'MIT' in kaynak else '—')
    katman = cell('Katman')
    m = re.search(r'^description:\s*(.*)$', sk, re.M)
    desc = (m.group(1).strip() if m else '')
    if desc in ('>', '|', '>-', '|-'):  # çok satırlı YAML: girintili devam satırlarını birleştir
        tail = sk[m.end():].splitlines()
        cont = []
        for l in tail:
            if l.startswith((' ', '	')) and l.strip(): cont.append(l.strip())
            elif l.strip() == '': continue
            else: break
        desc = ' '.join(cont)
    desc = desc.strip().strip('"')
    trig = re.findall(r'"([^"]{3,40})"', desc)[:4]
    trig_s = ', '.join(trig) if trig else (desc[:70] + '…' if len(desc) > 70 else desc)
    lines = sum(1 for _ in sk.splitlines())
    allow = d/'AUDIT-ALLOW'
    n_allow = sum(1 for l in allow.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')) if allow.exists() else 0
    rc = STATUS.get(d.name, '?')
    audit = 'TEMİZ' if rc == 0 else ('?' if rc == '?' else f'rc={rc}')
    audit += f' ({n_allow} istisna)' if n_allow else ''
    rows.append((d.name, katman, repo, pin_s, lic, audit, lines, trig_s))
out = ['# Vendor manifest', '', f'Üretildi: `scripts/gen-manifest.py` — elle düzenleme; kaynak `vendor/*/REVIEW.md`, `SKILL.md`, `AUDIT-ALLOW`.', '',
       'Katmanlar: **1** inceleme çekirdeği · **2** UX bilgi tabanı · **3** tasarım yönü (üretim) · **4** hareket · **5** web kalitesi · **6** süreç / skill yazımı. Katman, skill\'in bu depodaki rolünü söyler; hepsi `install.sh --only <ad>` ile tek tek kurulabilir.', '',
       '| Skill | Katman | Upstream | Pin | Lisans | Audit | SKILL.md satır | Tetik (description) |', '|---|---|---|---|---|---|---|---|']
for r in sorted(rows, key=lambda r: (r[1], r[0])):
    out.append('| ' + ' | '.join(str(x).replace('|', r'\|') for x in r) + ' |')
out += ['', f'Toplam {len(rows)} skill · pinli {sum(1 for r in rows if r[3] != "—")} · audit TEMİZ {sum(1 for r in rows if r[5].startswith("TEMİZ"))}.']
(V/'MANIFEST.md').write_text('\n'.join(out) + '\n', encoding='utf-8', newline='\n')
print(f'{len(rows)} satır → vendor/MANIFEST.md')
