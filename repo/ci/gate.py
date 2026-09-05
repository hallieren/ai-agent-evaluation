"""Release gate (ch14): a red light exits non-zero, no one's mood in the loop.

Usage: python ci/gate.py [config path]   (default ci/gate.yaml)
Hang it on the commit hook: one line in .git/hooks/pre-commit, `python ci/gate.py || exit 1`
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from harness import caseyaml, report, runner  # noqa: E402


def main(cfg_path):
    if not os.environ.get("MODEL_BASE_URL"):
        raise SystemExit("No model API configured. First export MODEL_BASE_URL / MODEL_NAME"
                         " (MODEL_API_KEY optional), see the repo README.")
    cfg = caseyaml.load(cfg_path)
    flags = {f: True for f in cfg.get("flags", [])}
    th = cfg["thresholds"]
    all_records, all_traces = [], []
    for suite in cfg["suites"]:
        print(f"[gate] replay {suite}")
        cases = runner.load_cases(os.path.join(os.path.dirname(cfg_path), "..", suite))
        traces, records = runner.run_suite(cases, flags, cfg.get("repeat", 1),
                                           verbose=False)
        all_records += records
        all_traces += traces
    rep = report.build(all_records, all_traces, cfg.get("repeat", 1))
    print()
    print(report.render(rep))
    print()
    sev2 = rep["sev_fail"].get("sev-2", 0)
    cost_p95 = rep["cost"]["p95"]
    lines = [
        ("sev-1 count", rep["sev1_count"], th["sev1_max"]),
        ("sev-2 count", sev2, th["sev2_max"]),
        ("cost P95 ($)", cost_p95, th["cost_p95_max"]),
    ]
    red = False
    for name, got, limit in lines:
        ok = got <= limit
        red = red or not ok
        print(f"[gate] {'green' if ok else 'red'}  {name}: {got} (criterion <= {limit})")
    if red:
        print("[gate] red light, refuse merge. Red-light action, see the Release Gate Template.")
        sys.exit(1)
    print("[gate] all green, release.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         os.path.join(os.path.dirname(__file__), "gate.yaml"))
