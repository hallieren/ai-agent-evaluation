"""ch13 Lab: the three evidence ladder stages. Usage: python labs/ch13/run.py --stage replay|shadow|canary

replay -- "production traffic" pours into the ch7 harness, out comes the layered report (+ a fidelity register reconciliation reminder)
shadow -- Mini runs the inputs covered by the production-side record in parallel, actions intercepted, compared entry by entry against the human decisions, out comes the disagreement rate
canary -- a slice of traffic executes for real, monitor.py's signals go live, see which signal trips first
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import monitor  # noqa: E402
import traffic  # noqa: E402
from harness import report, runner, trace  # noqa: E402

FLAGS = {"write_tools": True, "external_content": True}


def frag_user_fn(fragments):
    q = list(fragments)
    return lambda history: q.pop(0) if q else None


def run_cases(cases, tag):
    traces, records = [], []
    for k, case in enumerate(cases):
        user_fn = frag_user_fn(case["fragments"]) if case.get("fragments") else None
        tr, rec = runner.run_case(case, FLAGS, user_fn, trace_id=f"t-{tag}-{k:03d}")
        traces.append(tr)
        records.append(rec)
        print(f"  {case['id']} <- {case['source']} [{case['origin']}] -> {rec['verdict']}"
              + (f" ({rec['notes']})" if rec["verdict"] != "pass" else ""))
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    trace.save(traces, os.path.join(out, f"{tag}-traces.jsonl"))
    trace.save(records, os.path.join(out, f"{tag}-verdicts.jsonl"))
    return traces, records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["replay", "shadow", "canary"])
    a = ap.parse_args()
    if not os.environ.get("MODEL_BASE_URL"):
        sys.exit("A model API is required: set MODEL_BASE_URL / MODEL_NAME.\n"
                 "Without a model API: traffic.py and monitor.py run offline on their own"
                 " (python labs/ch13/traffic.py; monitor.py over any existing output).")
    cases = traffic.stream()
    if a.stage == "replay":
        print(f"[replay] {len(cases)} units of real traffic pour into the ch7 harness")
        traces, records = run_cases(cases, "replay")
        print()
        print(report.render(report.build(records, traces)))
        print("\nReconcile: open ch7's tool stub fidelity gap register (templates/ch07/tool-stub-inventory.md)"
              " and go row by row against labs/ch13/production-log.jsonl, pick one of confirmed / refuted / no evidence.\n"
              "The `refund` stub row, whether the real gateway errors on a second refund or the stub quietly succeeds,"
              " gets its conclusion today; refuted rows, fix the stub, rerun.")
    elif a.stage == "shadow":
        log = traffic.load_production_log()
        seen, subset = set(), []
        for c in cases:
            if c["source"] in log and c["source"] not in seen:
                seen.add(c["source"])
                subset.append(c)
        print(f"[shadow] {len(subset)} inputs overlapping the production-side record (actions intercepted: sandboxed, nothing leaves)")
        traces, _ = run_cases(subset, "shadow")
        diffs = []
        for c, tr in zip(subset, traces):
            mine, theirs = traffic.decision(tr), log[c["source"]]["decision"]
            if mine != theirs:
                diffs.append((c, mine, theirs))
        print(f"\nDisagreement rate: {len(diffs)}/{len(subset)} = {len(diffs) / len(subset):.0%}")
        for c, mine, theirs in diffs:
            print(f"  {c['id']} <- {c['source']}: Mini={mine} vs human={theirs}"
                  f" ({log[c['source']]['summary']})")
        print("\nPostmortem every disagreement: Mini wrong, human wrong, or both right (different routes)?"
              " Don't waste the ones where the human was wrong, harvest them.")
    else:
        slice_ = [c for i, c in enumerate(cases) if i % 3 == 0 or c["origin"] == "new usage"]
        print(f"[canary] slicing {len(slice_)}/{len(cases)} units for real execution, monitoring signals live")
        traces, records = run_cases(slice_, "canary")
        print()
        print(monitor.render(monitor.signals(traces, records)))
        print("\nHarvest: pick 10 from the red-line hits, the disagreements, the tripped traces,"
              " write them into the eval set by the four steps, fill in the coverage matrix,"
              " rerun the offline full suite. Watch the 91% drop, and write the new number with its interval into the report.")


if __name__ == "__main__":
    main()
