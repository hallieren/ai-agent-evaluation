"""Chapter 6 Lab: compare two system prompt versions — reproduce the single-run gap first, then take it apart with intervals and significance.

Two versions = one line each appended to the factory SYSTEM: prompt-a.txt (version A) /
prompt-b.txt (version B, the patch that "looks better" — give a clear solution and a clear
time expectation, avoid vague wording; same patch as ch14's wall).
The append goes through mini.agent.SYSTEM (restored after the run); no case changes, no core-code changes.

Usage: python labs/ch06/run.py [--cases cases/cases-50] [--repeat 1]
  Step 2 runs each version once (--repeat 1); step 3 uses --repeat 5 for the intervals. Needs a model API.
"""
import argparse
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
from harness import report, runner, stats  # noqa: E402
from mini import agent  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def need_model():
    if not (os.environ.get("MODEL_BASE_URL") or os.environ.get("MODEL_FAKE")):
        sys.exit("No model API configured: export MODEL_BASE_URL / MODEL_NAME first (see the repo README).\n"
                 "Without a model API: MODEL_FAKE=1 walks a scripted queue (test-only, not an eval).")


def run_variant(name, cases, repeat):
    with open(os.path.join(HERE, f"prompt-{name}.txt"), encoding="utf-8") as f:
        extra = f.read().strip()
    base = agent.SYSTEM
    agent.SYSTEM = base + "\n" + extra
    try:
        print(f"== Variant {name.upper()} (appended: {extra})")
        traces, records = runner.run_suite(cases, {}, repeat, verbose=False)
    finally:
        agent.SYSTEM = base
    return traces, records


def per_case(records, pred):
    """Cluster by case: each case folds its k runs into one proportion (ch6 step 3, never treat n×k as independent samples)."""
    by = {}
    for r in records:
        by.setdefault(r["case_id"], []).append(1 if pred(r) else 0)
    return {cid: sum(v) / len(v) for cid, v in by.items()}


def mean_z(xs, ys):
    """Two-mean z test (large-sample approximation); the stats module handles proportions, continuous quantities get covered here."""
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    vx = sum((x - mx) ** 2 for x in xs) / max(len(xs) - 1, 1)
    vy = sum((y - my) ** 2 for y in ys) / max(len(ys) - 1, 1)
    se = math.sqrt(vx / len(xs) + vy / len(ys))
    z = (mx - my) / se if se else 0.0
    return mx, my, abs(z) > 1.96, round(z, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=os.path.join(REPO, "cases", "cases-50"))
    ap.add_argument("--repeat", type=int, default=1)
    a = ap.parse_args()
    need_model()
    cases = runner.load_cases(a.cases)
    out = {}
    for name in ("a", "b"):
        traces, records = run_variant(name, cases, a.repeat)
        print(report.render(report.build(records, traces, a.repeat)))
        print()
        out[name] = (traces, records)
    (ta, ra), (tb, rb) = out["a"], out["b"]

    print("== Significance (proportions: paired McNemar, majority verdict per case; α = 0.05; sev-1 listed separately, never averaged in)")
    checks = [("pass rate", lambda r: r["verdict"] == "pass")] + [
        (f"{sev} failure rate", lambda r, s=sev: r["verdict"] != "pass" and r["severity"] == s)
        for sev in ("sev-1", "sev-2", "sev-3")]
    for label, pred in checks:
        ca, cb = per_case(ra, pred), per_case(rb, pred)
        p1 = sum(ca.values()) / len(ca) if ca else 0.0
        p2 = sum(cb.values()) / len(cb) if cb else 0.0
        a_only = sum(1 for cid in ca if ca[cid] > 0.5 >= cb.get(cid, 0.0))
        b_only = sum(1 for cid in ca if cb.get(cid, 0.0) > 0.5 >= ca[cid])
        sig, chi2 = stats.mcnemar(a_only, b_only)
        print(f"  {label}: A {p1:.1%} vs B {p2:.1%}, direction flips {a_only}+{b_only} -> "
              f"{'significant' if sig else 'not significant'} (chi2={chi2})")
    for label, key in (("step count", lambda t: len(t["steps"])),
                       ("cost ($)", lambda t: t["usage"]["cost_usd"])):
        ma, mb, sig, z = mean_z([key(t) for t in ta], [key(t) for t in tb])
        print(f"  {label} mean: A {ma:.3g} vs B {mb:.3g} -> "
              f"{'significant' if sig else 'not significant'} (z={z})")
    if a.repeat == 1:
        print("\nGot the single-run gap written down? Now rerun with --repeat 5 — see whether the intervals separate before concluding.")
    else:
        print("\nSet this against the single-run gap from step 2 and use templates/ch06/stats-cheat-sheet-report-template.md"
              "\nto land a comparison report with intervals — the two numbers pinned together are your private exhibit that a single-run number cannot be trusted.")


if __name__ == "__main__":
    main()
