"""Layered eval report (ch6 base grid + ch9 cost column): mean with interval, sev layering, verdict source, cost distribution."""
from harness import stats


def build(records, traces, repeat=1):
    """records: list of verdict records; traces: the matching traces. Returns the report dict."""
    n = len(records)
    passed = sum(1 for r in records if r["verdict"] == "pass")
    if repeat > 1:  # merged multi-run clusters by case; n×k verdicts are not independent samples (ch6 step 3)
        means = {}
        for r in records:
            means.setdefault(r["case_id"], []).append(1 if r["verdict"] == "pass" else 0)
        mean, half = stats.interval95_clustered(
            [sum(v) / len(v) for v in means.values()])
    else:
        mean, half = stats.interval95(passed, n)
    sev_fail = {}
    for r in records:
        if r["verdict"] != "pass":
            sev_fail[r["severity"]] = sev_fail.get(r["severity"], 0) + 1
    judged = {}
    for r in records:
        judged[r["judged_by"]] = judged.get(r["judged_by"], 0) + 1
    costs = [t["usage"]["cost_usd"] for t in traces]
    by_case = {}
    for r in records:
        by_case.setdefault(r["case_id"], []).append(r["verdict"])
    return {"n": n, "repeat": repeat, "pass_rate": mean, "interval": half,
            "sev1_count": sev_fail.get("sev-1", 0), "sev_fail": sev_fail,
            "judged_by": judged,
            "cost": {"median": stats.percentile(costs, 50),
                     "p95": stats.percentile(costs, 95),
                     "max": max(costs) if costs else 0.0},
            "flip_rate": stats.flip_rate(by_case) if repeat > 1 else None}


def render(rep):
    lines = [
        f"pass rate {rep['pass_rate']:.0%} ± {rep['interval']:.0%}"
        f" ({rep['n'] // rep['repeat']} cases × {rep['repeat']} runs"
        + (", clustered by case)" if rep['repeat'] > 1 else ")"),
        f"sev-1 count {rep['sev1_count']} (listed separately, never averaged in)",
        "failure layering: " + (", ".join(f"{k}: {v}" for k, v in sorted(rep["sev_fail"].items()))
                                or "none"),
        "verdict source: " + ", ".join(f"{k}: {v}" for k, v in sorted(rep["judged_by"].items())),
        f"cost (USD, illustrative): median ${rep['cost']['median']} / P95 ${rep['cost']['p95']}"
        f" / max ${rep['cost']['max']}",
    ]
    if rep["flip_rate"] is not None:
        lines.append(f"flip rate: {rep['flip_rate']:.0%}")
    return "\n".join(lines)
