"""results.json → Markdown tablo (RESULTS.md için)."""
import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
def pct(x): return f"{round(x*3)}/3"
rows = ["| # | Etiket | Beklenen | first | any_clean | geçerli n | Bitiş | İlk araç / rakip skill |", "|---|---|---|---|---|---|---|---|"]
for i, r in enumerate(d['results'], 1):
    exp = "tetikle" if r['should_trigger'] else "tetikleme"
    ended = ",".join({"success":"ok","error_max_turns":"kesildi","timeout":"zaman"}.get(e or "?", str(e)) for e in r['ended'])
    comp = sorted({s for run in r['skills_called'] for s in run if s != "<TEST-SKILL>"})
    ft = "/".join(str(t) for t in r['first_tools'])
    extra = f"{ft}" + (f" · rakip: {', '.join(comp)}" if comp else "")
    mark = "✓" if r['pass_any'] else "✗"
    rows.append(f"| {i} | {r['tag']} | {exp} | {pct(r['trigger_rate'])} | {round(r['any_clean_rate']*r['valid_runs']) if r['valid_runs'] else 0}/{r['valid_runs']} {mark} | {r['valid_runs']} | {ended} | {extra} |")
s = d['summary']
pos = [r for r in d['results'] if r['should_trigger']]; neg = [r for r in d['results'] if not r['should_trigger']]
print("\n".join(rows))
print()
print(f"Tetiklemeli geçen (any_clean): {sum(r['pass_any'] for r in pos)}/{len(pos)} · Tetiklememeli geçen: {sum(r['pass_any'] for r in neg)}/{len(neg)} · first metriğiyle geçen: {s['passed']}/{s['total']}")
print(f"Kesilen koşu: {s['truncated_runs']}/60 · self-read (geçersiz) koşu: {s['self_read_runs']}/60 · maliyet ${s['cost_usd']} · model {d['model']} · {d['date']} · max-turns {d['max_turns']}")
