"""Trace slicing tool (ch11 Lab step 3). Offline: reads trace JSONL, nothing else.

Renders: outer steps + nested subagent traces (indented) + spawn task description and
return (the two handoff ends) + the three multi-agent cost columns
(main agent / subagents / round trips; harness.trace.total_usage basis).

Usage: python labs/ch11/split.py <traces.jsonl> [...]
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from harness import trace as trace_mod  # noqa: E402


def clip(s, n=90):
    s = (s or "").replace("\n", " ")
    return s[:n] + ("…" if len(s) > n else "")


def show(tr):
    print(f"trace {tr['trace_id']}  case {tr['case_id']}")
    print("-" * 64)
    for depth, s in trace_mod.flat_steps(tr):
        pad = "    " * depth
        if s["type"] == "tool_call" and s["name"] == "spawn_subagent":
            print(f"{pad}{s['i']:>3}. [SPAWN] -> {s['args'].get('name', 'logistics')}")
            print(f"{pad}     task description (handoff outbound leg, verbatim): {s['args'].get('task', '')!r}")
        elif s["type"] == "subagent":
            print(f"{pad}{s['i']:>3}. [subagent:{s['name']}] nested trace "
                  f"{len(s['trace']['steps'])} steps ↓")
        elif s["type"] == "tool_call":
            print(f"{pad}{s['i']:>3}. [tool_call] {s['name']}"
                  f"({json.dumps(s.get('args', {}), ensure_ascii=False)})")
        elif s["type"] == "tool_result":
            print(f"{pad}{s['i']:>3}. [tool_result] {s['name']} -> {clip(s.get('content'))}")
        elif s["type"] == "inbound":
            print(f"{pad}{s['i']:>3}. [inbound:{s.get('source', '?')}] {clip(s.get('content'))}")
        else:
            print(f"{pad}{s['i']:>3}. [model] {clip(s.get('content'))}")
    for _, s in trace_mod.flat_steps(tr):
        if s["type"] == "subagent":
            print(f"     return (handoff return leg, verbatim): {s['trace']['final']!r}")
    print(f"final: {clip(tr['final'], 200)}")
    u = trace_mod.total_usage(tr)
    print("Three cost columns (ch11 basis: system cost = outer usage, all nested totals included):")
    print(f"  main agent   in {u['main']['tokens_in']:>6} / out {u['main']['tokens_out']:>5} tokens")
    print(f"  subagents    in {u['subagents']['tokens_in']:>6} / out {u['subagents']['tokens_out']:>5} tokens")
    print(f"  round trips  {u['handoffs']} (one full round trip per spawn)")
    print(f"  total        in {u['total']['tokens_in']} / out {u['total']['tokens_out']} tokens,"
          f" ${u['total']['cost_usd']} (illustrative)")


def main():
    files = sys.argv[1:]
    assert files, "Usage: python labs/ch11/split.py <traces.jsonl> [...]"
    for path in files:
        for tr in trace_mod.load(path):
            show(tr)
            print("=" * 64)


if __name__ == "__main__":
    main()
