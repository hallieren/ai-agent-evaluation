"""Chapter 5 Lab: assign judges to traces and run the verdicts, judge-verdict JSONL out (the alignment tool's input).

Division of labor (the judgment ladder: whatever could sink has sunk to the assertion layer; the judge takes only what is left):
a case with an explicit expect.judge uses it; otherwise action → judge-tone-commitment,
investigate → judge-report-rubric, query gets none.
--judge forces one judge to blind-judge the whole batch (for calibration).

Usage: python labs/ch05/run.py --traces <traces.jsonl> [--cases cases/cases-50]
        [--judge judge-tone-commitment] [--out labs/ch05/judge-verdicts.jsonl]
Needs a model API. Alignment (offline): python labs/ch05/align.py labs/ch05/judge-verdicts.jsonl <human-labels.jsonl>
"""
import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
from harness import judge, runner, trace  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_JUDGE = {"action": "judge-tone-commitment", "investigate": "judge-report-rubric"}


def need_model():
    if not os.environ.get("MODEL_BASE_URL"):
        sys.exit("No model API configured: export MODEL_BASE_URL / MODEL_NAME first (see the repo README).\n"
                 "Without a model API: align.py is offline anyway.")


def pick_judge(case, forced):
    if forced:
        return forced
    if not case:
        return None
    return case.get("expect", {}).get("judge") or DEFAULT_JUDGE.get(case.get("type"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--traces", required=True)
    ap.add_argument("--cases", default=os.path.join(REPO, "cases", "cases-50"))
    ap.add_argument("--judge", default="", help="force one judge to blind-judge all traces (for calibration)")
    ap.add_argument("--out", default=os.path.join(HERE, "judge-verdicts.jsonl"))
    a = ap.parse_args()
    need_model()
    by_id = {c["id"]: c for c in runner.load_cases(a.cases)}
    records, skipped = [], 0
    for tr in trace.load(a.traces):
        case = by_id.get(tr["case_id"])
        jname = pick_judge(case, a.judge)
        if not jname:
            skipped += 1
            continue
        v = judge.judge(jname, tr, case or {"prompt": ""})
        rec = {"case_id": tr["case_id"], "run_id": "", "verdict": v["verdict"],
               "severity": (case or {}).get("severity_if_fail"), "failure_mode": None,
               "first_bad_step": None, "judged_by": jname, "notes": v.get("notes", "")}
        records.append(rec)
        print(f"  {tr['trace_id'] or tr['case_id']} [{jname}] -> {v['verdict']}"
              f"({v.get('notes', '')})")
    trace.save(records, a.out)
    n = len(records)
    counts = {v: sum(1 for r in records if r["verdict"] == v)
              for v in ("pass", "concern", "unsafe", "unclear")}
    print(f"\n{n} judge verdicts saved to {a.out}; skipped {skipped} (query, or no matching case).")
    print("Distribution: " + ", ".join(f"{k}: {v}" for k, v in counts.items()))
    print("Discipline: sev-1 is never released by the judge alone (the runner enforces this); the judge can only escalate."
          "\nNext: sample stratified by severity, blind-label by hand, run align.py for the calibration report.")


if __name__ == "__main__":
    main()
