"""ch11 Lab step 2: unlock subagents, run the system-level end-to-end case set (Swiftlink handoff case included).

Usage: python labs/ch11/run.py [--repeat 3]
Under a real model the canonical handoff failure is probabilistic; deterministic reproduction: python labs/ch11/handoff-demo.py
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
    ap.add_argument("--cases", default=os.path.join(HERE, "cases"))
    ap.add_argument("--repeat", type=int, default=1)
    a = ap.parse_args()
    if not os.environ.get("MODEL_BASE_URL"):
        sys.exit("Model API required: set MODEL_BASE_URL / MODEL_NAME.\n"
                 "Without a model API: python labs/ch11/handoff-demo.py replays the canonical failure trace offline.")
    flags = {"write_tools": True, "subagents": True}
    cases = runner.load_cases(a.cases)
    print(f"[ch11] system-level cases × {len(cases)}, flags = {[k for k in flags]}")
    traces, records = runner.run_suite(cases, flags, a.repeat)
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    trace.save(traces, os.path.join(out, "traces.jsonl"))
    trace.save(records, os.path.join(out, "verdicts.jsonl"))
    print()
    print(report.render(report.build(records, traces, a.repeat)))
    print("\nNext: python labs/ch11/split.py labs/ch11/out/traces.jsonl (slice nested traces for attribution); "
          "attribution reference answer: labs/ch11/reference.md")


if __name__ == "__main__":
    main()
