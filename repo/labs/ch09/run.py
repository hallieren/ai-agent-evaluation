"""ch9 Lab steps 2/4: planner on, full run (--repeat), budget assertions live, the first report with a cost distribution.

Usage: python labs/ch09/run.py [--cases cases/cases-50] [--repeat 5] [--no-planner]
Cases without budget_* get the suggested defaults from budgets.md overlaid (reference steps × 2).
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from harness import report, runner, stats, trace  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# budgets.md revised values: first real-model calibration median plus headroom (runner hard ceiling 40); cost anchored at historical P95 plus headroom
DEFAULT_BUDGETS = {"query": {"steps": 14, "cost": 0.05},
                   "action": {"steps": 24, "cost": 0.15},
                   "investigate": {"steps": 36, "cost": 0.90}}


def overlay_budgets(cases):
    """Overlay default budgets onto cases without budget_*. Returns the count added."""
    n = 0
    for c in cases:
        entries = c.setdefault("expect", {}).setdefault("assertions", [])
        names = [e if isinstance(e, str) else next(iter(e)) for e in entries]
        b = DEFAULT_BUDGETS.get(c.get("type", "query"), DEFAULT_BUDGETS["query"])
        if "budget_steps_max" not in names:
            entries.append({"budget_steps_max": {"max": b["steps"]}})
            n += 1
        if "budget_cost_max" not in names:
            entries.append({"budget_cost_max": {"max": b["cost"]}})
            n += 1
    return n


def by_type_table(cases, traces, records):
    """ch9 cost columns: cost/latency/step distributions per task type + within-budget counts."""
    types = {c["id"]: c.get("type", "query") for c in cases}
    rows = {}
    for tr, rec in zip(traces, records):
        r = rows.setdefault(types.get(rec["case_id"], "?"),
                            {"cost": [], "wall": [], "steps": [], "hit": 0, "n": 0})
        r["cost"].append(tr["usage"]["cost_usd"])
        r["wall"].append(tr["usage"]["wall_s"])
        r["steps"].append(len(tr["steps"]))
        r["n"] += 1
        if not (rec["notes"] or "").startswith("budget_"):
            r["hit"] += 1
    lines = ["task type      n  cost med  cost P95  cost max  latency P95(s)  steps P95  within budget"]
    for t in ("query", "action", "investigate"):
        if t not in rows:
            continue
        r = rows[t]
        lines.append(f"{t:<12} {r['n']:>3}   ${stats.percentile(r['cost'], 50):<8} "
                     f"${stats.percentile(r['cost'], 95):<7} ${max(r['cost']):<8} "
                     f"{stats.percentile(r['wall'], 95):<10} "
                     f"{stats.percentile(r['steps'], 95):<7} {r['hit']}/{r['n']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=os.path.join(ROOT, "cases", "cases-50"))
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--no-planner", action="store_true",
                    help="planner-off control configuration (for the cost-quality comparison points)")
    a = ap.parse_args()
    if not os.environ.get("MODEL_BASE_URL"):
        sys.exit("A model API is required: set MODEL_BASE_URL / MODEL_NAME (MODEL_API_KEY optional).\n"
                 "Without a model API this script cannot do the full run; for the offline part see align.py --demo and the README.")
    flags = {"write_tools": True, "planner": not a.no_planner}
    cases = runner.load_cases(a.cases)
    n = overlay_budgets(cases)
    print(f"[ch9] budget overlay: {n} default budget_* entries (cases with budgets already set are left alone); "
          f"flags = {[k for k, v in flags.items() if v]}")
    traces, records = runner.run_suite(cases, flags, a.repeat)
    os.makedirs(OUT, exist_ok=True)
    tag = "-noplanner" if a.no_planner else ""
    trace.save(traces, os.path.join(OUT, f"traces{tag}.jsonl"))
    trace.save(records, os.path.join(OUT, f"verdicts{tag}.jsonl"))
    print()
    print(report.render(report.build(records, traces, a.repeat)))
    print()
    print(by_type_table(cases, traces, records))
    print(f"\nTraces saved to labs/ch09/out/traces{tag}.jsonl; "
          f"next: python labs/ch09/align.py labs/ch09/out/traces{tag}.jsonl\n"
          "Report base grid: templates/ch09/cost-latency-report-template.md")


if __name__ == "__main__":
    main()
