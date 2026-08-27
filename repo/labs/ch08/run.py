"""Chapter 8 Lab: flip the switch — unlock write_tools, red lines + all of cases-50, diff list on every write.

The order is Part III's template: change the spec → write the cases → differ smoke test →
flip the switch → question it layer by layer. This script does the last three: first a smoke
test on one read-only case (the diff list must be empty), then unlocks write_tools and runs
cases/redline + cases/cases-50, printing a verdict per case; every case whose trace touched a
write tool gets a before/after diff list (harness.differ) — every change is either declared
as expected, or it is a finding.

Usage: python labs/ch08/run.py [--cases dir ...] [--repeat 1]; needs a model API.
Traces and verdicts go to labs/ch08/full-traces.jsonl / full-verdicts.jsonl.
"""
import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
from harness import caseyaml, differ, report, runner, trace  # noqa: E402
from mini import agent  # noqa: E402
from world import world  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WRITE = ("refund", "send_email", "update_order", "escalate")


def need_model():
    if not (os.environ.get("MODEL_BASE_URL") or os.environ.get("MODEL_FAKE")):
        sys.exit("No model API configured: export MODEL_BASE_URL / MODEL_NAME first (see the repo README).\n"
                 "Without a model API: MODEL_FAKE=1 walks a scripted queue (test-only, not an eval).")


def run_one(case, flags, trace_id=""):
    """Run one case; returns (trace, verdict record, diff list)."""
    world.reset()
    world.apply_setup(case.get("setup", {}))
    before = world.snapshot()
    con = world.connect()
    tr = agent.run(case["prompt"], flags, case_id=case["id"], trace_id=trace_id, con=con)
    con.close()
    after = world.snapshot()
    return tr, runner.evaluate(tr, before, after, case), differ.diff(before, after)


def touched_write(tr):
    return any(s["name"] in WRITE for s in trace.tool_calls(tr))


def smoke():
    case = caseyaml.load(os.path.join(REPO, "cases", "seed-20", "case-001.yaml"))
    _, _, changes = run_one(case, {}, "t-8000")
    print("Step 1, differ smoke test (read-only case-001, write_tools off):")
    print("  " + differ.render(changes).replace("\n", "\n  "))
    assert not changes, "Non-empty diff on a read-only case — smoke test failed; fix the sandbox before flipping the switch"
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", nargs="*",
                    default=[os.path.join(REPO, "cases", "redline"),
                             os.path.join(REPO, "cases", "cases-50")])
    ap.add_argument("--repeat", type=int, default=1)
    a = ap.parse_args()
    need_model()
    smoke()
    cases = []
    for d in a.cases:
        cases += runner.load_cases(d)
    flags = {"write_tools": True}
    print(f"Step 2, flip the switch: write_tools unlocked, {len(cases)} cases × {a.repeat} runs\n")
    traces, records = [], []
    for rep in range(1, a.repeat + 1):
        for k, case in enumerate(cases, 1):
            tr, rec, changes = run_one(case, flags, trace_id=f"t-8{rep:01d}{k:02d}")
            rec["run_id"] = f"r-{rep:02d}"
            traces.append(tr)
            records.append(rec)
            print(f"{case['id']} [{rec['judged_by']}] -> {rec['verdict']}"
                  + (f"({rec['notes']})" if rec["verdict"] != "pass" else ""))
            if touched_write(tr) or changes:
                print("  diff list:")
                print("    " + differ.render(changes).replace("\n", "\n    "))
    trace.save(traces, os.path.join(HERE, "full-traces.jsonl"))
    trace.save(records, os.path.join(HERE, "full-verdicts.jsonl"))
    print("\nStep 3, the layered report:")
    print(report.render(report.build(records, traces, a.repeat)))
    print("\nQuestion it layer by layer (step 5): find the duplicate-refund case (redline-02) — "
          "what does the judge say, what does order_state_equals say, what does the diff list say? "
          "Three layers, three different answers: that is the whole point of layering."
          "\nThen the over-limit case (redline-01): at which step's tool_call does amount_within_limit "
          "light red (the verdict record's first_bad_step)."
          "\nTwo deliverables: the Action Permission Matrix merged into the spec "
          "(templates/ch08/action-permission-matrix.md) + your first diff report.")


if __name__ == "__main__":
    main()
