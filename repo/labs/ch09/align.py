"""plan-trace alignment tool (ch9 Lab step 3). Offline: reads trace JSONL only, never touches the model.

For each trace with a `plan` field, maps tool_call steps onto the plan's subgoals
(cheap heuristics: tool name / keyword / argument-value matching), and prints
orphan-step counts plus the deviation top-3.
Three deviation kinds (silent deviations only): orphan steps / abandoned subgoals /
order inversions (this tool reports the first two).

Usage: python labs/ch09/align.py [traces.jsonl ...]
       python labs/ch09/align.py --demo    # offline demo: MODEL_FAKE reproduces the 11-step refund detour
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from harness import trace as trace_io  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

TOOL_KEYS = {
    "get_order": ["get_order", "look up order", "look up the order", "check the order", "order status", "verify the order"],
    "search_orders": ["search_orders", "search order", "search for order", "find the order"],
    "get_customer": ["get_customer", "customer profile", "customer record", "verify the customer"],
    "read_ticket": ["read_ticket", "ticket"],
    "search_kb": ["search_kb", "policy", "knowledge"],
    "refund": ["execute the refund", "issue the refund", "process the refund", "refund"],
    "send_email": ["send_email", "email", "reply to the customer"],
    "update_order": ["update_order", "update the order", "modify the order", "change the address"],
    "escalate": ["escalate", "hand off to a human", "human agent"],
    "spawn_subagent": ["spawn_subagent", "subagent", "logistics"],
    "fetch_url": ["fetch_url", "web page", "fetch"],
}


def parse_plan(plan):
    goals = [m.group(1).strip() for line in plan.splitlines()
             if (m := re.match(r"\s*(?:\d+\s*[.):]|[-*])\s*(.+)", line))]
    return goals or ([plan.strip()] if plan.strip() else [])


def owner(step, goals):
    """Keys ordered by specificity, tried one by one against the subgoals; first hit owns the step (cheap case-insensitive heuristic, good enough). Argument values count only when they are a specific phrase (two words or more)."""
    keys = TOOL_KEYS.get(step["name"], [step["name"]])
    vals = [str(v) for v in step.get("args", {}).values() if len(str(v).split()) >= 2]
    for k in keys + vals:
        for gi, g in enumerate(goals):
            if k.lower() in g.lower():
                return gi
    return None


def align_one(tr):
    goals = parse_plan(tr.get("plan", ""))
    calls = [s for s in tr["steps"] if s["type"] == "tool_call"]
    orphan, hit, seen, dup = [], set(), set(), 0
    for s in calls:
        gi = owner(s, goals)
        orphan.append(s) if gi is None else hit.add(gi)
        key = (s["name"], json.dumps(s.get("args", {}), sort_keys=True))
        dup += key in seen
        seen.add(key)
    return {"trace_id": tr["trace_id"], "case_id": tr["case_id"], "goals": goals,
            "calls": len(calls), "orphan": orphan, "dup": dup,
            "abandoned": [g for i, g in enumerate(goals) if i not in hit]}


def render(rows, top):
    print("trace         case        goals  tool steps  orphan(share)  dup calls  abandoned")
    for r in rows:
        ratio = len(r["orphan"]) / r["calls"] if r["calls"] else 0.0
        print(f"{r['trace_id']:<13} {r['case_id']:<11} {len(r['goals']):>4}  {r['calls']:>5}"
              f"  {len(r['orphan']):>3} ({ratio:.0%})   {r['dup']:>6}  {len(r['abandoned']):>4}")
    worst = sorted(rows, key=lambda r: (len(r["orphan"]), r["dup"]), reverse=True)[:top]
    print(f"\n== Deviation top-{top} (read each end to end: every step looks \"reasonable\" alone) ==")
    for r in worst:
        print(f"\n{r['trace_id']} / {r['case_id']}  plan:")
        for i, g in enumerate(r["goals"], 1):
            print(f"    {i}. {g}")
        for s in r["orphan"]:
            print(f"  orphan step i={s['i']}: {s['name']}({json.dumps(s.get('args', {}), ensure_ascii=False)})"
                  + ("  <- unplanned cross-customer read, red line, listed separately" if s["name"] == "get_customer" else ""))
        for g in r["abandoned"]:
            print(f"  abandoned subgoal: {g} (time-sensitive items are the most dangerous)")
    print("\nReading sheet: templates/ch09/plan-trace-deviation-checklist.md (thresholds filled in before the run)")


def demo():
    """MODEL_FAKE reproduces the canonical "11 steps vs 3 steps" refund detour (Bible section 5), then aligns it."""
    os.environ["MODEL_FAKE"] = "1"
    from mini import agent, llm
    from world import world
    go = {"name": "get_order", "args": {"order_id": "SH-90699"}}
    kb = {"name": "search_kb", "args": {"query": "refund"}}
    llm.set_script([
        {"content": "1. Use get_order to look up order SH-90699\n2. Use search_kb to check the refund policy\n3. Execute the refund of $199"},
        {"content": "", "tool_calls": [go]}, {"content": "", "tool_calls": [go]},
        {"content": "", "tool_calls": [kb]}, {"content": "", "tool_calls": [kb]},
        {"content": "", "tool_calls": [kb]},
        {"content": "", "tool_calls": [{"name": "get_customer", "args": {"name": "Reed"}}]},
        {"content": "", "tool_calls": [go]},
        {"content": "", "tool_calls": [{"name": "refund", "args": {"order_id": "SH-90699", "amount": "199"}}]},
        {"content": "Refund executed: SH-90699 $199, going back to your original payment method."}])
    world.reset()
    con = world.connect()
    tr = agent.run("This is Allison Reed. The aroma diffuser humidifier SH-90699 is leaking. Refund me.",
                   {"write_tools": True, "planner": True},
                   case_id="demo-refund-detour", trace_id="t-demo-09", con=con)
    con.close()
    tr["usage"]["wall_s"] = 0.0  # wall clock is meaningless in fake mode; zero it so regeneration is byte-identical
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "demo-plan-trace.jsonl")
    trace_io.save([tr], path)
    print(f"[demo] plan trace written to {path} (reference path 3 steps, the run detours; includes an unplanned get_customer)\n")
    return [path]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    files = demo() if a.demo else (a.files or [os.path.join(OUT, "traces.jsonl")])
    rows, skipped = [], 0
    for path in files:
        for tr in trace_io.load(path):
            rows.append(align_one(tr)) if tr.get("plan") else None
            skipped += 0 if tr.get("plan") else 1
    if skipped:
        print(f"(skipped {skipped} traces without a plan field; for planner-off traces see the migration box)\n")
    assert rows, "no traces with a plan field to align: run labs/ch09/run.py first (planner on)"
    render(rows, 3)


if __name__ == "__main__":
    main()
