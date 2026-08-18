"""Trace viewer (terminal-first, minimal): python viewer/trace_viewer.py traces/examples/t-0007.jsonl"""
import json
import sys


def show(tr):
    print(f"trace {tr['trace_id']}  case {tr['case_id']}")
    on = [k for k, v in tr["flags"].items() if v]
    print(f"flags: {', '.join(on) if on else '(Lv.0 read-only)'}")
    if tr.get("plan"):
        print(f"plan:\n  " + tr["plan"].replace("\n", "\n  "))
    print("-" * 60)
    _steps(tr["steps"], 0)
    print("-" * 60)
    print(f"final: {tr['final']}")
    u = tr["usage"]
    print(f"usage: in {u['tokens_in']} / out {u['tokens_out']} tokens,"
          f" ${u['cost_usd']} (illustrative), {u['wall_s']}s")


def _steps(steps, depth):
    pad = "    " * depth
    for s in steps:
        if s["type"] == "model":
            print(f"{pad}{s['i']:>3}. [model] {_clip(s.get('content', ''))}")
        elif s["type"] == "tool_call":
            print(f"{pad}{s['i']:>3}. [tool_call] {s['name']}({json.dumps(s['args'], ensure_ascii=False)})")
        elif s["type"] == "tool_result":
            print(f"{pad}{s['i']:>3}. [tool_result] {s['name']} -> {_clip(s['content'])}")
        elif s["type"] == "inbound":
            print(f"{pad}{s['i']:>3}. [inbound:{s.get('source', '?')}] ⚠ external content {_clip(s['content'])}")
        elif s["type"] == "subagent":
            print(f"{pad}{s['i']:>3}. [subagent:{s['name']}] ↓ nested trace")
            _steps(s["trace"]["steps"], depth + 1)


def _clip(s, n=100):
    s = (s or "").replace("\n", " ")
    return s[:n] + ("…" if len(s) > n else "")


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        for line in f:
            if line.strip():
                show(json.loads(line))
                print("=" * 60)
