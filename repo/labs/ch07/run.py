"""Chapter 7 Lab: one command, full run — sandbox self-check + synthetic-user sparring + layered report.

Step 1: world reset self-check (two reset snapshots must be identical); step 2: full run
(default cases/cases-50, the eval set built in Chapter 4; or pass --cases cases/seed-20
cases/redline): angry / vague / multi cases spar against synthetic users (--synth on by
default), actions land in the sandbox and the outbox; step 3: layered report.

Usage: python labs/ch07/run.py [--cases dir ...] [--repeat 1] [--no-synth]
Traces and verdicts go to labs/ch07/full-traces.jsonl / full-verdicts.jsonl. Needs a model API.
"""
import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
from harness import report, runner, trace  # noqa: E402
from world import world  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def need_model():
    if not os.environ.get("MODEL_BASE_URL"):
        sys.exit("No model API configured: export MODEL_BASE_URL / MODEL_NAME first (see the repo README).\n"
                 "Without a model API this script cannot run (MODEL_FAKE only fits pre-scripted teaching traces).")


def reset_check():
    world.reset()
    a = json.dumps(world.snapshot(), ensure_ascii=False, sort_keys=True)
    world.reset()
    b = json.dumps(world.snapshot(), ensure_ascii=False, sort_keys=True)
    assert a == b, "Two reset snapshots differ. The sandbox is not resettable, the eval foundation is cracked; fix before running"
    print("Step 1, sandbox self-check: two reset snapshots identical (this is what \"resettable\" means)\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", nargs="*",
                    default=[os.path.join(REPO, "cases", "cases-50")])
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--no-synth", action="store_true",
                    help="turn synthetic users off (every case runs single-turn)")
    a = ap.parse_args()
    need_model()
    reset_check()
    cases = []
    for d in a.cases:
        cases += runner.load_cases(d)
    print(f"Step 2, full run: {len(cases)} cases × {a.repeat} runs"
          f" (synthetic-user sparring: {'off' if a.no_synth else 'on, angry/vague/multi taken over by the three synth/ personas'})")
    traces, records = runner.run_suite(cases, {}, a.repeat, synth_users=not a.no_synth)
    trace.save(traces, os.path.join(HERE, "full-traces.jsonl"))
    trace.save(records, os.path.join(HERE, "full-verdicts.jsonl"))
    print(f"\nTraces and verdicts saved to labs/ch07/full-traces.jsonl / full-verdicts.jsonl")
    print("\nStep 3, the book's first complete report:")
    print(report.render(report.build(records, traces, a.repeat)))
    print("\nReading the report, skip the overall pass rate at first: first look at the sev-1 row, "
          "then at the verdict source (how many the assertions decided, how many the judge did)."
          "\nThen register at least one fidelity gap each for the refund stub and the send_email stub: "
          "templates/ch07/tool-stub-inventory.md.")


if __name__ == "__main__":
    main()
