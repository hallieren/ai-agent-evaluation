"""Monitoring script (ch13, canary rung). Online has no gold labels: monitor only what can be judged without a reference answer.

Signals (per the five columns of templates/ch13/monitoring-signal-spec.md: signal / data source / baseline / band / trigger action):
  red-line assertion hits (sev-1) / escalation rate / the three cost columns (median / P95 / max).
Importable and runnable offline: python labs/ch13/monitor.py --traces t.jsonl --verdicts v.jsonl
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from harness import stats, trace as trace_mod  # noqa: E402

BASELINES = {"escalation_band": (0.05, 0.30),  # ready-made baseline (band) from the human-support era; a dip is more suspicious = bluffed answers
             "cost_p95_max": 0.5}              # cost criterion shared with ci/gate.yaml (illustrative USD)


def signals(traces, records):
    sigs = []
    sev1 = [r for r in records if r["verdict"] != "pass" and r.get("severity") == "sev-1"]
    sigs.append({"signal": "red-line assertion hits (sev-1)", "source": "online assertions over production traces",
                 "value": len(sev1), "band": "zero hits; no band, a single instance trips",
                 "action": "immediate rollback", "tripped": bool(sev1),
                 "cases": [r["case_id"] for r in sev1]})
    esc = (sum(1 for t in traces
               if any(c["name"] == "escalate" for c in trace_mod.tool_calls(t)))
           / len(traces)) if traces else 0.0
    lo, hi = BASELINES["escalation_band"]
    sigs.append({"signal": "escalation rate", "source": "human-handoff records",
                 "value": round(esc, 3), "band": f"[{lo}, {hi}] (spike = new inputs; dip = bluffing)",
                 "action": "out of band = pause promotion / shrink traffic", "tripped": not lo <= esc <= hi,
                 "cases": []})
    costs = [t["usage"]["cost_usd"] for t in traces]
    p95 = stats.percentile(costs, 95)
    sigs.append({"signal": "three cost columns (median/P95/max)", "source": "trace usage (ch11 basis)",
                 "value": f"${stats.percentile(costs, 50)} / ${p95} / ${max(costs) if costs else 0}",
                 "band": f"P95 <= ${BASELINES['cost_p95_max']} (the alarm sits at P95, not the mean)",
                 "action": "over the line = shrink traffic and read the priciest trace", "tripped": p95 > BASELINES["cost_p95_max"],
                 "cases": []})
    return sigs


def render(sigs):
    lines = ["signal                           measured      baseline/band                trigger action"]
    for s in sigs:
        lamp = "* TRIPPED" if s["tripped"] else "o"
        lines.append(f"{lamp} {s['signal']:<30} {str(s['value']):<12} "
                     f"{s['band']:<28} {s['action']}")
        if s["cases"]:
            lines.append(f"    hit cases: {', '.join(s['cases'])} - read the tripped trace to the end before deciding:"
                         " roll back, or harvest, fix, and climb again")
    first = next((s for s in sigs if s["tripped"]), None)
    lines.append("")
    lines.append(f"First signal to trip: {first['signal'] if first else '(none tripped in this batch)'}")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--traces", required=True)
    ap.add_argument("--verdicts", required=True)
    a = ap.parse_args()
    print(render(signals(trace_mod.load(a.traces), trace_mod.load(a.verdicts))))
