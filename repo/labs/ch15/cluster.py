"""Failure mining clustering script (ch15 Lab steps 1-2). Offline: reads verdict JSONL + trace JSONL, never touches a model.

Circle the pool: failing verdicts (verdict != pass) plus behavior patterns mined out of the traces
(such as "fuzzy search by name even with the order ID given", which the offline atlas does not have).
Pre-sort into piles by failure_mode / notes keyword affinity; then check the piles against the offline
mode list in traces/pregen-60-key.json and flag the ones missing from the atlas = new mode candidates.
After stratified sampling, read and code every trace by hand, the Chapter 3 muscle, this time on dirty data.

Usage: python labs/ch15/cluster.py [--verdicts v.jsonl ...] [--traces t.jsonl ...]
       (by default it pools everything produced under labs/ch13/out/)
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from harness import trace as trace_mod  # noqa: E402

# failure_mode (case vocabulary) -> offline atlas mode name (pregen-60-key vocabulary)
MODE_ALIAS = {"unauthorized-commitment": "unauthorized commitment", "hearsay-as-fact": "hearsay taken as fact",
              "missed-request-item": "missed request item", "irrelevant-record-access": "irrelevant record lookup",
              "fabricated-order-id": "fabricated order ID", "fabricated-identifier": "fabricated order ID",
              "wrong-policy-answer": "wrong policy answer", "wrong-tool-selection": "fuzzy search instead of exact lookup",
              "fuzzy-search-for-exact": "fuzzy search instead of exact lookup", "dropped-subgoal": "missed request item",
              "retrieval-waste": "irrelevant record lookup"}
ORDER_ID = re.compile(r"SH-\d{5}")


def known_modes():
    with open(os.path.join(ROOT, "traces", "pregen-60-key.json"), encoding="utf-8") as f:
        return set(json.load(f).values()) - {"clean"}


def cluster_key(rec):
    """Pre-sort key: failure_mode first, falling back to the assertion name / first keyword of notes."""
    if rec.get("failure_mode"):
        return rec["failure_mode"]
    head = (rec.get("notes") or "").split(":")[0].strip()
    return head or "(unclassified)"


def mine_traces(traces):
    """Behavior pattern mining: fuzzy search by name even with the order ID given (prompt carried SH-xxxxx, yet search_orders was called)."""
    hits = []
    for tr in traces:
        prompt_ids = set()
        for s in tr["steps"]:
            if s["type"] == "inbound":
                prompt_ids |= set(ORDER_ID.findall(s.get("content") or ""))
        if any(c["name"] == "search_orders" for c in trace_mod.tool_calls(tr)):
            # the trace does not store the raw prompt; look back through final+model steps for an order ID (a cheap approximation)
            text = " ".join([tr.get("final") or ""]
                            + [s.get("content") or "" for s in tr["steps"]])
            if ORDER_ID.findall(text) or prompt_ids:
                hits.append(tr)
    return hits


def main():
    ap = argparse.ArgumentParser()
    default_dir = os.path.join(ROOT, "labs", "ch13", "out")
    ap.add_argument("--verdicts", nargs="*",
                    default=sorted(glob.glob(os.path.join(default_dir, "*-verdicts.jsonl"))))
    ap.add_argument("--traces", nargs="*",
                    default=sorted(glob.glob(os.path.join(default_dir, "*-traces.jsonl"))))
    a = ap.parse_args()
    assert a.verdicts, "no verdict file to pool: run labs/ch13/run.py first, or point --verdicts at a path"
    records = [r for p in a.verdicts for r in trace_mod.load(p)]
    traces = [t for p in a.traces for t in trace_mod.load(p)]
    fails = [r for r in records if r["verdict"] != "pass"]
    clusters = {}
    for r in fails:
        clusters.setdefault(cluster_key(r), []).append(r)
    print(f"pool: {len(records)} verdicts ({len(fails)} failing) + {len(traces)} traces\n")
    known = known_modes()
    print("piles (six-column row structure per the Chapter 3 atlas: name/criterion/representative trace/count/sev distribution/suspected component, the last three filled in after human reading)")
    print("name (failure_mode)           cnt  sev distribution   sample cases   in offline atlas?")
    for key, rs in sorted(clusters.items(), key=lambda kv: -len(kv[1])):
        sev = {}
        for r in rs:
            sev[r.get("severity")] = sev.get(r.get("severity"), 0) + 1
        offline = MODE_ALIAS.get(key, key) in known
        print(f"{key:<28} {len(rs):>4}  {str(sev):<18} "
              f"{', '.join(r['case_id'] for r in rs[:3]):<14} "
              f"{'yes' if offline else 'no -> new mode candidate'}")
    mined = mine_traces(traces)
    if mined:
        print(f"\nbehavior pattern mining: \"fuzzy search by name even with the order ID given\", {len(mined)} traces"
              f" (samples: {', '.join(t['trace_id'] for t in mined[:3])})")
        print("  the offline atlas has no such row (pregen only tests 'can it find it', not 'it was handed to you, do you use it')."
              " New mode candidate, goes into the atlas extension.")
        print("  Two bottleneck candidates, both plausible: does the system prompt fail to require"
              " 'with an order ID present, exact lookup is mandatory', or is the description boundary between"
              " get_order and search_orders vague? Write both as falsifiable hypotheses and pick the one with the"
              " smaller blast radius first, the tool description. Walkthrough in cycle-demo.md.")
    else:
        print("\nbehavior pattern mining: no \"fuzzy search by name even with the order ID given\" in this pool; try another pool or more traffic.")
    print("\nNext: stratified sampling, then read and code every trace by hand; extend the atlas reusing the six-column row structure"
          " (templates/ch15/failure-mining-protocol.md).")


if __name__ == "__main__":
    main()
