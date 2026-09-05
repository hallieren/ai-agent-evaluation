"""Coverage matrix tool (Chapter 4, offline): failure mode × severity × persona.

Usage: python labs/ch04/coverage.py [cases dir, default cases/cases-50]
An empty cell is not a sin, an unsigned one is — copy the empty-cell list into the
annotation bar of templates/ch04/coverage-matrix.md and rule each "fill" or "reasoned empty".
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
from harness import runner  # noqa: E402

PERSONAS = ["cooperative", "angry", "vague", "multi"]


def matrix(path):
    cases = runner.load_cases(path)
    rows = {}
    for c in cases:
        p = c.get("persona", "cooperative")
        for m in c.get("failure_modes") or ["(no failure mode tagged)"]:
            r = rows.setdefault(m, {"sev": set(), "n": {q: 0 for q in PERSONAS}})
            r["sev"].add(c.get("severity_if_fail", "sev-3"))
            r["n"][p] += 1
    return rows, len(cases)


def main(path):
    rows, ncase = matrix(path)
    print(f"Coverage matrix: {path} ({ncase} cases; one case can carry several modes, counts go by mode row)\n")
    w = max(len(m) for m in rows) + 2
    print("  " + "failure mode".ljust(w) + "sev".ljust(14)
          + "".join(p.ljust(13) for p in PERSONAS) + "total")
    for m in sorted(rows, key=lambda m: (min(rows[m]["sev"]), m)):
        r = rows[m]
        total = sum(r["n"].values())
        print("  " + m.ljust(w) + "/".join(sorted(r["sev"])).ljust(14)
              + "".join(str(r["n"][p]).ljust(13) for p in PERSONAS) + str(total))
    empties = [(m, p) for m in sorted(rows) for p in PERSONAS if rows[m]["n"][p] == 0]
    print(f"\nEmpty-cell list ({len(empties)} cells; rule each \"fill\" or \"reasoned empty\", log in the annotation bar):")
    for m, p in empties:
        print(f"  - {m} × {p}")
    sev1 = [m for m in rows if "sev-1" in rows[m]["sev"]]
    print("\nsev-1 check: " + (", ".join(f"{m}({sum(rows[m]['n'].values())} cases)"
                                         for m in sorted(sev1)) or "no sev-1 row in this directory!"))
    print("Reminder: this table only sees modes with existing cases — a mode in your atlas that never "
          "appears here is an entire missing row; check against the atlas and add it. "
          "sev-1 rows must be non-zero: every high-risk mode needs a sentry standing.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "cases", "cases-50"))
