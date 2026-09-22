#!/usr/bin/env python3
"""Trigger measurement for a skill description — Windows-safe variant of skill-creator's run_eval.py.

Differences from upstream (documented in RESULTS.md):
- thread reader instead of select() (Windows pipes)
- claude.cmd resolved for CreateProcess; PYTHONUTF8 expected
- runs each query for up to --max-turns and records BOTH metrics:
    first  = skill invoked as the model's very first tool call (upstream metric)
    any    = skill invoked at any turn within --max-turns
  plus first_tool, turn index of the Skill call, and whether the model Read the
  command file itself (self-discovery → 'any' is contaminated for that run).
Output JSON keeps upstream keys (results[].trigger_rate/pass, summary) using the 'first' metric.
"""
import argparse, json, os, shutil, subprocess, sys, threading, time, uuid, queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import date


def parse_skill_md(skill_path: Path):
    text = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    fm = text.split("---", 2)[1]
    name = desc = None
    for line in fm.splitlines():
        if line.startswith("name:"): name = line.split(":", 1)[1].strip()
        if line.startswith("description:"): desc = line.split(":", 1)[1].strip()
    return name, desc


ORIGINAL_ROOT = None  # set in main(): the --project-root passed on the CLI (fixture source for per-run re-copy)


def run_once(query, skill_name, description, roots: "queue.Queue", model, timeout, max_turns):
    project_root = roots.get()
    try:
        return _run_once(query, skill_name, description, project_root, model, timeout, max_turns)
    finally:
        roots.put(project_root)


def _run_once(query, skill_name, description, project_root: Path, model, timeout, max_turns):
    uid = uuid.uuid4().hex[:8]
    clean = f"{skill_name}-skill-{uid}"
    cmd_dir = project_root / ".claude" / "commands"; cmd_dir.mkdir(parents=True, exist_ok=True)
    cmd_file = cmd_dir / f"{clean}.md"
    indented = "\n  ".join(description.split("\n"))
    cmd_file.write_text(f"---\ndescription: |\n  {indented}\n---\n\n# {skill_name}\n\nThis skill handles: {description}\n", encoding="utf-8", newline="\n")
    claude_bin = shutil.which("claude.cmd") or shutil.which("claude") or "claude"
    cmd = [claude_bin, "-p", query, "--output-format", "stream-json", "--verbose", "--max-turns", str(max_turns),
           "--disallowedTools", "Edit,Write,MultiEdit,NotebookEdit"]
    fx = project_root / "src" / "pages" / "RegisterForm.tsx"; fx_src = ORIGINAL_ROOT / "src" / "pages" / "RegisterForm.tsx" if ORIGINAL_ROOT else None
    if fx_src and fx_src.exists(): shutil.copyfile(fx_src, fx)  # negatives may not mutate the fixture (defence in depth)
    if model: cmd += ["--model", model]
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    r = {"first_tool": None, "skill_turn": None, "self_read": False, "tools": [], "skills_called": [], "cost": None, "timeout": False, "ended": None}
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=str(project_root), env=env)
        q = queue.Queue()
        def reader():
            try:
                for raw in p.stdout: q.put(raw)
            finally: q.put(None)
        threading.Thread(target=reader, daemon=True).start()
        t0 = time.time(); turn = 0
        while time.time() - t0 < timeout:
            try: raw = q.get(timeout=1.0)
            except queue.Empty: continue
            if raw is None: break
            try: e = json.loads(raw.decode("utf-8", errors="replace"))
            except json.JSONDecodeError: continue
            if e.get("type") == "assistant":
                for c in e.get("message", {}).get("content", []):
                    if c.get("type") != "tool_use": continue
                    turn += 1; name = c.get("name", ""); inp = c.get("input", {})
                    r["tools"].append(name)
                    if r["first_tool"] is None: r["first_tool"] = name
                    if name == "Read" and ".claude/commands" in str(inp.get("file_path", "")).replace("\\", "/"): r["self_read"] = True
                    if name == "Skill":
                        r["skills_called"].append(str(inp.get("skill", "")).replace(clean, "<TEST-SKILL>"))
                        if f"{skill_name}-skill-" in str(inp.get("skill", "")) and r["skill_turn"] is None: r["skill_turn"] = turn
            elif e.get("type") == "result":
                r["cost"] = e.get("total_cost_usd"); r["ended"] = e.get("subtype"); break
        else:
            r["timeout"] = True; r["ended"] = "timeout"
    finally:
        if p.poll() is None: p.kill(); p.wait()
        if cmd_file.exists(): cmd_file.unlink()
    r["first"] = r["skill_turn"] == 1
    r["any"] = r["skill_turn"] is not None
    r["any_clean"] = r["any"] and not r["self_read"]
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-set", required=True); ap.add_argument("--skill-path", required=True)
    ap.add_argument("--project-root", required=True); ap.add_argument("--model", default=None)
    ap.add_argument("--runs-per-query", type=int, default=3); ap.add_argument("--num-workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=180); ap.add_argument("--max-turns", type=int, default=6)
    ap.add_argument("--threshold", type=float, default=0.5); ap.add_argument("--out", required=True)
    ap.add_argument("--description", default=None, help="override description under test")
    a = ap.parse_args()
    evals = json.loads(Path(a.eval_set).read_text(encoding="utf-8"))
    name, desc = parse_skill_md(Path(a.skill_path))
    if a.description: desc = a.description
    root = Path(a.project_root)
    global ORIGINAL_ROOT; ORIGINAL_ROOT = root
    roots = queue.Queue()
    for w in range(a.num_workers):  # isolated copy of the project per worker
        wr = root.parent / f"{root.name}-w{w}"
        if wr.exists(): shutil.rmtree(wr)
        shutil.copytree(root, wr, ignore=shutil.ignore_patterns(".claude"))
        (wr / ".claude" / "commands").mkdir(parents=True)
        roots.put(wr)
    jobs = [(i, k) for i, _ in enumerate(evals) for k in range(a.runs_per_query)]
    runs = {i: [] for i in range(len(evals))}
    with ThreadPoolExecutor(max_workers=a.num_workers) as ex:
        futs = {ex.submit(run_once, evals[i]["query"], name, desc, roots, a.model, a.timeout, a.max_turns): (i, k) for i, k in jobs}
        for f in as_completed(futs):
            i, k = futs[f]; runs[i].append(f.result())
            e = evals[i]; rr = runs[i][-1]
            print(f"  q{i+1:02d} run{k+1} first={rr['first']} any={rr['any']} turn={rr['skill_turn']} tools={rr['tools']} skills={rr['skills_called']}", file=sys.stderr, flush=True)
    results = []; passed = 0
    for i, e in enumerate(evals):
        rs = runs[i]; n = len(rs)
        first_rate = sum(r["first"] for r in rs) / n
        valid = [r for r in rs if not r["self_read"]]
        any_rate = (sum(r["any"] for r in valid) / len(valid)) if valid else 0.0
        any_raw = sum(r["any"] for r in rs) / n
        trig = first_rate >= a.threshold
        ok = trig == e["should_trigger"]; passed += ok
        results.append({"query": e["query"], "tag": e.get("tag"), "should_trigger": e["should_trigger"],
                        "trigger_rate": first_rate, "triggers": sum(r["first"] for r in rs), "runs": n, "pass": ok,
                        "any_clean_rate": any_rate, "any_raw_rate": any_raw, "valid_runs": len(valid), "pass_any": (any_rate >= a.threshold) == e["should_trigger"],
                        "ended": [r["ended"] for r in rs],
                        "first_tools": [r["first_tool"] for r in rs], "skill_turns": [r["skill_turn"] for r in rs], "skills_called": [r["skills_called"] for r in rs], "tools": [r["tools"] for r in rs],
                        "self_read": sum(r["self_read"] for r in rs), "timeouts": sum(r["timeout"] for r in rs),
                        "cost_usd": round(sum(r["cost"] or 0 for r in rs), 4)})
    out = {"skill_name": name, "description": desc, "model": a.model, "date": date.today().isoformat(),
           "max_turns": a.max_turns, "runs_per_query": a.runs_per_query, "threshold": a.threshold,
           "results": results,
           "summary": {"total": len(evals), "passed": passed, "failed": len(evals) - passed,
                       "passed_any": sum(r["pass_any"] for r in results),
                       "truncated_runs": sum(r["ended"].count("error_max_turns") for r in results),
                       "self_read_runs": sum(r["self_read"] for r in results),
                       "cost_usd": round(sum(r["cost_usd"] for r in results), 3)}}
    for w in range(a.num_workers):
        for _ in range(2):
            shutil.rmtree(root.parent / f"{root.name}-w{w}", ignore_errors=True); time.sleep(0.5)
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps(out["summary"], ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    main()
