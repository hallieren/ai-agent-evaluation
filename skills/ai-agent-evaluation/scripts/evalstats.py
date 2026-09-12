#!/usr/bin/env python3
"""evalstats: the numbers discipline for agent eval reports (book chapter 6, "trusting numbers").

Enforces: never a bare pass rate, always mean + 95% interval; multi-run sets cluster by case (denominator =
case count, never n x k verdicts); sev-1 sits on its own line, never averaged in; versions are compared
paired on case_id with McNemar; sample size from the 1/sqrt(n) rough cut and the exact worst case; pass@k
and pass^k mean nothing until the flip rate is measured. Math lifted verbatim from harness/stats.py.

  python evalstats.py report verdicts.jsonl [--sev-field severity] [--cost-field cost_usd]
  python evalstats.py compare a.jsonl b.jsonl | size --gap 5 | size --cases 50 | passk --p 0.9 --k 5 | --selftest
"""
import argparse
import json
import math
import sys


# ---- lifted verbatim from harness/stats.py -------------------------------------------------
def interval95(passed, n):
    """95% interval for a pass rate (normal approximation). Returns (mean, half-width). For single runs; merged multi-run goes through interval95_clustered."""
    if n == 0:
        return 0.0, 0.0
    p = passed / n
    half = 1.96 * math.sqrt(p * (1 - p) / n)
    return round(p, 4), round(half, 4)


def interval95_clustered(case_means):
    """Pass-rate interval for merged multi-run: clustered by case (ch6 step 3).
    case_means: one entry per case, its k runs folded into a single pass rate. The denominator is the case count;
    treating n×k verdicts as independent samples is pseudo-replication and reports the interval about half as wide as it is. Returns (mean, half-width)."""
    n = len(case_means)
    if n == 0:
        return 0.0, 0.0
    m = sum(case_means) / n
    var = sum((x - m) ** 2 for x in case_means) / (n - 1) if n > 1 else 0.0
    half = 1.96 * math.sqrt(var / n)
    return round(m, 4), round(half, 4)


def mcnemar(a_only_pass, b_only_pass):
    """McNemar paired test (continuity-corrected, α = 0.05): two versions run the same eval set; count only the cases that flip direction.
    a_only_pass: cases A passes and B fails; b_only_pass: cases A fails and B passes.
    Cases that pass both or fail both carry no information. Returns (significant, chi2)."""
    b, c = a_only_pass, b_only_pass
    if b + c == 0:
        return False, 0.0
    chi2 = (abs(b - c) - 1) ** 2 / (b + c)
    return chi2 > 3.841, round(chi2, 3)


def significant(p1, n1, p2, n2):
    """Two-proportion z test, α = 0.05. Returns (significant, z)."""
    if n1 == 0 or n2 == 0:
        return False, 0.0
    p = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se if se else 0.0
    return abs(z) > 1.96, round(z, 3)


def flip_rate(runs_by_case):
    """Flip rate: fraction of cases whose repeated runs disagree. runs_by_case: {case_id: [verdict, ...]}"""
    flips = sum(1 for vs in runs_by_case.values() if len(set(vs)) > 1)
    n = len(runs_by_case)
    return round(flips / n, 4) if n else 0.0


def percentile(values, q):
    """P50/P95 etc. q ∈ [0, 100]."""
    if not values:
        return 0.0
    xs = sorted(values)
    i = min(len(xs) - 1, max(0, math.ceil(q / 100 * len(xs)) - 1))
    return xs[i]


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def by_case(records):
    out = {}
    for r in records:
        out.setdefault(r["case_id"], []).append(r)
    return out


def build(records, sev_field="severity", cost_field="cost_usd"):
    cases = by_case(records)
    runs = max(len(v) for v in cases.values())
    verdicts = {c: [r["verdict"] for r in rs] for c, rs in cases.items()}
    if runs > 1:
        mean, half = interval95_clustered(
            [sum(v == "pass" for v in vs) / len(vs) for vs in verdicts.values()])
    else:
        mean, half = interval95(sum(r["verdict"] == "pass" for r in records), len(records))
    sev_fail, judged = {}, {}
    for r in records:
        if r["verdict"] != "pass":
            sev = r.get(sev_field) or "unlabeled"
            sev_fail[sev] = sev_fail.get(sev, 0) + 1
        if r.get("judged_by"):
            judged[r["judged_by"]] = judged.get(r["judged_by"], 0) + 1
    costs = [r[cost_field] for r in records if isinstance(r.get(cost_field), (int, float))]
    return {"n_cases": len(cases), "runs": runs, "n": len(records), "pass_rate": mean,
            "interval": half, "uneven": any(len(v) != runs for v in cases.values()),
            "sev_fail": sev_fail, "judged_by": judged,
            "flip_rate": flip_rate(verdicts) if runs > 1 else None,
            "cost": {"median": percentile(costs, 50), "p95": percentile(costs, 95),
                     "max": max(costs)} if costs else None}


def render(rep):
    sev1, cl = rep["sev_fail"].get("sev-1", 0), (", clustered by case" if rep["runs"] > 1 else "")
    layer = ", ".join(f"{k}: {v}" for k, v in sorted(rep["sev_fail"].items()))
    lines = [f"pass rate {rep['pass_rate']:.0%} ± {rep['interval'] * 100:.0f} "
             f"({rep['n_cases']} cases × {rep['runs']} runs{cl}); "
             f"sev-1 count {sev1} (listed separately, never averaged in)",
             "failure layering (non-pass verdicts by severity): " + (layer or "none")]
    if rep["judged_by"]:
        lines.append("verdict source: " + ", ".join(f"{k}: {v}" for k, v in sorted(rep["judged_by"].items())))
    if rep["flip_rate"] is not None:
        lines.append(f"flip rate: {rep['flip_rate']:.0%} (cases whose runs disagree; measure it, never assume it)")
        lines.append(f"note: interval denominator is the case count ({rep['n_cases']}); treating the "
                     f"{rep['n']} verdicts as independent samples would be pseudo-replication"
                     + (" (uneven runs per case: max used)" if rep["uneven"] else ""))
    else:
        lines.append("note: single run, normal-approximation interval; run ≥ 5 times before trusting the number")
    if rep["cost"]:
        lines.append("cost (USD, as recorded): median ${median} / P95 ${p95} / max ${max}".format(**rep["cost"]))
    lines.append("grid: Metric | Mean | Interval | Cases | Runs | sev-layer counts\n"
                 f"grid: pass rate | {rep['pass_rate']:.0%} | ±{rep['interval'] * 100:.0f} | "
                 f"{rep['n_cases']} | {rep['runs']} | {layer or 'none'}")
    return "\n".join(lines)


def majority(records):
    """Fold a case's runs into one boolean: strict majority of runs passed."""
    folded = {}
    for cid, rs in by_case(records).items():
        folded[cid] = sum(r["verdict"] == "pass" for r in rs) * 2 > len(rs)
    return folded


def cmd_compare(a, b, sev_field, cost_field):
    ra, rb = load(a), load(b)
    fa, fb = majority(ra), majority(rb)
    if set(fa) != set(fb):
        only_a, only_b = sorted(set(fa) - set(fb)), sorted(set(fb) - set(fa))
        sys.exit(f"refused: case_id sets differ (only in A: {len(only_a)} {only_a[:5]}; "
                 f"only in B: {len(only_b)} {only_b[:5]}). A paired comparison needs the same cases.")
    a_only, b_only = sum(fa[c] and not fb[c] for c in fa), sum(fb[c] and not fa[c] for c in fa)
    sig, chi2 = mcnemar(a_only, b_only)
    print(f"A: {a}\n{render(build(ra, sev_field, cost_field))}\n")
    print(f"B: {b}\n{render(build(rb, sev_field, cost_field))}\n")
    print(f"paired on {len(fa)} cases (runs folded to majority pass): A-only-pass {a_only}, B-only-pass {b_only}")
    print(f"McNemar (continuity-corrected, α = 0.05): chi2 {chi2}, significant: {'yes' if sig else 'no'}"
          + ("" if sig else " (cannot be told apart on this set; report the difference as noise)"))


def cmd_size(gap, cases, p):
    if gap:
        rough, exact = math.ceil((100 / gap) ** 2), math.ceil((1.96 * 100 / gap) ** 2 * p * (1 - p))
        print(f"for a ±{gap:g}-point 95% half-width: rough cut 1/√n → {rough} cases; "
              f"exact at p={p} (1.96·√(p(1-p)/n)) → {exact} cases")
    if cases:
        rough, exact = 100 / math.sqrt(cases), 1.96 * math.sqrt(p * (1 - p) / cases) * 100
        print(f"{cases} cases: rough cut 1/√n → ±{rough:.1f} points; exact at p={p} → ±{exact:.1f} points")
    if not gap and not cases:
        sys.exit("give --gap POINTS or --cases N")


def cmd_passk(p, k):
    print(f"p = {p}, k = {k}: pass@k (at least one of {k} runs passes) {1 - (1 - p) ** k:.4f}; "
          f"pass^k (all {k} runs pass) {p ** k:.4f}")
    print("warning: both assume independent runs; whether failures are coin flips or hard cases that always "
          "fail is a property of the data, measure it via the flip rate (report on a ≥ 5-run set) before quoting either")


def selftest():
    m, h = interval95_clustered([1.0] * 25 + [0.0] * 25)
    assert interval95(37, 50) == (0.74, 0.1216) and m == 0.5 and 0.13 < h < 0.15
    assert mcnemar(10, 2) == (True, 4.083) and mcnemar(0, 0) == (False, 0.0)
    assert flip_rate({"a": ["pass", "pass"], "b": ["pass", "concern"]}) == 0.5
    assert percentile([1, 2, 3, 4, 5], 50) == 3 and percentile([], 95) == 0.0
    recs = [{"case_id": "c1", "verdict": "pass"}, {"case_id": "c1", "verdict": "unsafe", "severity": "sev-1"},
            {"case_id": "c2", "verdict": "pass"}, {"case_id": "c2", "verdict": "pass"}]
    rep = build(recs)
    assert rep["runs"] == 2 and rep["sev_fail"] == {"sev-1": 1} and rep["flip_rate"] == 0.5
    assert "clustered by case" in render(rep) and majority(recs) == {"c1": False, "c2": True}
    print("selftest ok")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("report", help="report line + layers for one verdict JSONL")
    r.add_argument("verdicts")
    c = sub.add_parser("compare", help="paired McNemar between two verdict JSONLs")
    c.add_argument("a"), c.add_argument("b")
    for p in (r, c):
        p.add_argument("--sev-field", default="severity"), p.add_argument("--cost-field", default="cost_usd")
    s = sub.add_parser("size", help="cases needed for a half-width, or half-width for a case count")
    s.add_argument("--gap", type=float, default=0), s.add_argument("--cases", type=int, default=0)
    s.add_argument("--p", type=float, default=0.5, help="assumed pass rate (0.5 = worst case)")
    k = sub.add_parser("passk", help="pass@k and pass^k under independence")
    k.add_argument("--p", type=float, required=True), k.add_argument("--k", type=int, required=True)
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    run = {"report": lambda: print(render(build(load(a.verdicts), a.sev_field, a.cost_field))),
           "compare": lambda: cmd_compare(a.a, a.b, a.sev_field, a.cost_field),
           "size": lambda: cmd_size(a.gap, a.cases, a.p), "passk": lambda: cmd_passk(a.p, a.k)}
    run.get(a.cmd, ap.print_help)()


if __name__ == "__main__":
    main()
