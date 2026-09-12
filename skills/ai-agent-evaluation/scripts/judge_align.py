#!/usr/bin/env python3
"""judge_align: judge-vs-human alignment report (book chapter 5, "judging").

Enforces: an LLM judge is trusted only against blind human labels on the same cases; disagreement is
layered by severity (a 10% miss on sev-3 and a 10% miss on sev-1 are different reports); per-class
recall exposes a judge that passes everything; the false-fail line exposes a judge the team will
learn to ignore; the report is void the moment the judge prompt or the base model changes.

align / align_recall / align_false_fail / render_align are lifted from the companion harness
(harness/judge.py); the layering key is parameterized. Stdlib only.

  python judge_align.py judge.jsonl human.jsonl [--by severity_if_fail] [--dims]
  python judge_align.py --selftest

Records are verdict-record JSONL: at least case_id and verdict; the human file carries the
layering key (default severity_if_fail, falling back to severity, then "sev-3").
"""
import argparse
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def _sev(h, by):
    return h.get(by) or h.get("severity") or "sev-3"


def align(judge_records, human_records, by="severity_if_fail"):
    """judge-vs-human alignment report: disagreement rate layered by severity (ch5).

    records: [{"case_id", "verdict", "severity"}]. Returns the layered disagreement table.
    """
    humans = {r["case_id"]: r for r in human_records}
    layers = {}
    for j in judge_records:
        h = humans.get(j["case_id"])
        if not h:
            continue
        sev = _sev(h, by)
        d = layers.setdefault(sev, {"n": 0, "disagree": 0, "cases": []})
        d["n"] += 1
        if j["verdict"] != h["verdict"]:
            d["disagree"] += 1
            d["cases"].append({"case_id": j["case_id"], "judge": j["verdict"],
                               "human": h["verdict"]})
    for d in layers.values():
        d["rate"] = round(d["disagree"] / d["n"], 3) if d["n"] else None
    return layers


def align_recall(judge_records, human_records):
    """Per-class recall (ch5 sidebar): of the cases humans labeled unsafe/concern, how many the judge catches back (labels non-pass).
    Layered disagreement rates can't expose a fake judge that labels everything pass; this line can. Returns (caught, should_catch)."""
    humans = {r["case_id"]: r for r in human_records}
    judged = {j["case_id"]: j for j in judge_records}
    flagged = [cid for cid, h in humans.items()
               if h["verdict"] in ("unsafe", "concern") and cid in judged]
    caught = sum(1 for cid in flagged if judged[cid]["verdict"] != "pass")
    return caught, len(flagged)


def align_false_fail(judge_records, human_records):
    """False fails (ch5): of the cases humans labeled pass, how many the judge rules non-pass.
    The other direction from per-class recall; a judge with many false fails is one the team learns to ignore. Returns (false_fails, human_passes)."""
    humans = {r["case_id"]: r for r in human_records}
    judged = {j["case_id"]: j for j in judge_records}
    passed = [cid for cid, h in humans.items()
              if h["verdict"] == "pass" and cid in judged]
    failed = sum(1 for cid in passed if judged[cid]["verdict"] != "pass")
    return failed, len(passed)


def dims_breakdown(judge_records, human_records):
    """Optional per-dimension view for rubric judges whose records carry dims: {name: value}.
    Per dimension: how the judge's values distribute, and (when the human record carries the same dimension) how often they differ."""
    humans = {r["case_id"]: r for r in human_records}
    dims = {}
    for j in judge_records:
        h = humans.get(j["case_id"])
        for name, val in (j.get("dims") or {}).items():
            d = dims.setdefault(name, {"values": {}, "compared": 0, "differ": 0})
            d["values"][str(val)] = d["values"].get(str(val), 0) + 1
            if h and name in (h.get("dims") or {}):
                d["compared"] += 1
                d["differ"] += str(h["dims"][name]) != str(val)
    return dims


def render_align(layers, recall, false_fail=None, dims=None):
    lines = ["judge-vs-human alignment report (disagreement rate layered by severity)", ""]
    for sev in sorted(layers):
        d = layers[sev]
        lines.append(f"  {sev}: {d['disagree']}/{d['n']} disagreement rate {d['rate']}")
        for c in d["cases"]:
            lines.append(f"    - {c['case_id']}: judge={c['judge']} human={c['human']}")
    caught, n = recall
    lines.append(f"  per-class recall: humans labeled {n} cases unsafe/concern, judge caught {caught}")
    if false_fail is not None:
        failed, n_pass = false_fail
        lines.append(f"  per-class false fails: humans labeled {n_pass} cases pass, judge failed {failed}")
    if dims is not None:
        lines.append("  per-dimension (judge value counts; differ = human dim value present and different):")
        for name in sorted(dims) or ["(no record carries dims)"]:
            d = dims.get(name)
            if d:
                vals = ", ".join(f"{k}: {v}" for k, v in sorted(d["values"].items()))
                lines.append(f"    - {name}: {vals}; differ {d['differ']}/{d['compared']}")
            else:
                lines.append(f"    - {name}")
    lines.append("")
    lines.append("Validity statement: the moment the judge prompt or the base model changes, this report is void (ch5/ch14 discipline).")
    return "\n".join(lines)


def run(judge_path, human_path, by, want_dims):
    judge_records, human_records = load(judge_path), load(human_path)
    layers = align(judge_records, human_records, by)
    if not layers:
        sys.exit("Zero matches: the two files share no case_id; check the inputs.")
    matched = sum(d["n"] for d in layers.values())
    print(f"{len(judge_records)} judge verdicts × {len(human_records)} human labels, "
          f"{matched} matched by case_id (layered by human '{by}', fallback 'severity')\n")
    print(render_align(layers, align_recall(judge_records, human_records),
                       align_false_fail(judge_records, human_records),
                       dims_breakdown(judge_records, human_records) if want_dims else None))


def selftest():
    j = [{"case_id": "c1", "verdict": "pass", "dims": {"evidence": "ok"}},
         {"case_id": "c2", "verdict": "pass"},
         {"case_id": "c3", "verdict": "concern"},
         {"case_id": "c9", "verdict": "unsafe"}]
    h = [{"case_id": "c1", "verdict": "pass", "severity_if_fail": "sev-3", "dims": {"evidence": "weak"}},
         {"case_id": "c2", "verdict": "unsafe", "severity": "sev-1"},
         {"case_id": "c3", "verdict": "concern", "severity_if_fail": "sev-2"}]
    layers = align(j, h)
    assert set(layers) == {"sev-1", "sev-2", "sev-3"} and layers["sev-1"]["rate"] == 1.0
    assert layers["sev-1"]["cases"][0] == {"case_id": "c2", "judge": "pass", "human": "unsafe"}
    assert align_recall(j, h) == (1, 2) and align_false_fail(j, h) == (0, 1)
    assert dims_breakdown(j, h) == {"evidence": {"values": {"ok": 1}, "compared": 1, "differ": 1}}
    out = render_align(layers, (1, 2), (0, 1), dims_breakdown(j, h))
    assert out.rstrip().endswith("this report is void (ch5/ch14 discipline).") and "differ 1/1" in out
    print("selftest ok")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("judge", nargs="?", help="judge verdict JSONL")
    ap.add_argument("human", nargs="?", help="blind human label JSONL")
    ap.add_argument("--by", default="severity_if_fail", help="layering key on the human record")
    ap.add_argument("--dims", action="store_true", help="per-dimension breakdown when records carry dims")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.judge and a.human):
        ap.error("need JUDGE.jsonl and HUMAN.jsonl")
    run(a.judge, a.human, a.by, a.dims)


if __name__ == "__main__":
    main()
