"""Chapter 1 Lab: run Mini (Lv.0, read-only) over cases/seed-20, one case at a time.

Prints each case's final reply and a tool-call summary; traces go to labs/ch01/traces.jsonl.
No verdicts are printed; the four-verdict labeling is your job: blind-label annotation-sheet.md first, then compare with reference.md.
Usage: python labs/ch01/run.py (needs a model API, see the repo README)
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
from harness import runner, trace  # noqa: E402
from mini import agent  # noqa: E402
from world import world  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def need_model():
    if os.environ.get("MODEL_FAKE"):
        sys.exit("This Lab needs a real model: MODEL_FAKE's scripted queue has no script for seed-20. "
                 "Export MODEL_BASE_URL / MODEL_NAME (optionally MODEL_API_KEY) and rerun; see the repo README.")
    if not os.environ.get("MODEL_BASE_URL"):
        sys.exit("No model API configured: export MODEL_BASE_URL / MODEL_NAME (optionally MODEL_API_KEY) first; "
                 "see the repo README.")


def main():
    need_model()
    cases = runner.load_cases(os.path.join(REPO, "cases", "seed-20"))
    traces = []
    for k, case in enumerate(cases, 1):
        world.reset()
        world.apply_setup(case.get("setup", {}))
        con = world.connect()
        tr = agent.run(case["prompt"], {}, case_id=case["id"],
                       trace_id=f"t-9{k:03d}", con=con)
        con.close()
        traces.append(tr)
        calls = [s for s in tr["steps"] if s["type"] == "tool_call"]
        print(f"=== {tr['trace_id']}  {case['id']}"
              f"({case['type']} / {case.get('persona', 'cooperative')}) ===")
        print(f"Customer: {case['prompt']}")
        print("Tool calls: " + ("; ".join(
            f"{s['name']}({json.dumps(s['args'], ensure_ascii=False)})" for s in calls)
            or "(none; note: answering without a single tool call deserves a second look)"))
        print(f"Mini: {tr['final']}")
        print()
    out = os.path.join(HERE, "traces.jsonl")
    trace.save(traces, out)
    print(f"20 traces saved to {out} (read them one by one with python viewer/trace_viewer.py)")
    print("Next: blind-label the four verdicts in labs/ch01/annotation-sheet.md, then compare with reference.md. No peeking.")


if __name__ == "__main__":
    main()
