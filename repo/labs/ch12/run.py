"""ch12 Lab step 3: unlock external_content and run one red-team round over all of cases/attacks.

Usage: python labs/ch12/run.py [--repeat 1]
Output: labs/ch12/out/{traces,verdicts}.jsonl; layered interception table: python labs/ch12/layers.py
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from harness import report, runner, trace  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=os.path.join(ROOT, "cases", "attacks"))
    ap.add_argument("--repeat", type=int, default=1)
    a = ap.parse_args()
    if not os.environ.get("MODEL_BASE_URL"):
        sys.exit("A model API is required: set MODEL_BASE_URL / MODEL_NAME.\n"
                 "Without one: layers.py can tally any saved traces+verdicts offline; "
                 "the teaching sample is under labs/ch16/material/ (the canonical forged-customer-email trace).")
    flags = {"write_tools": True, "external_content": True}
    cases = runner.load_cases(a.cases)
    print(f"[ch12] red team: {len(cases)} attack samples (layered by attack surface × carrier), "
          f"flags = {[k for k in flags]}")
    traces, records = runner.run_suite(cases, flags, a.repeat)
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    trace.save(traces, os.path.join(out, "traces.jsonl"))
    trace.save(records, os.path.join(out, "verdicts.jsonl"))
    print()
    print(report.render(report.build(records, traces, a.repeat)))
    print("\nNext: python labs/ch12/layers.py (the layered interception table, this chapter's core Lab output)")


if __name__ == "__main__":
    main()
