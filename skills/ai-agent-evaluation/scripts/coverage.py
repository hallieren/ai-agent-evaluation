#!/usr/bin/env python3
"""coverage: the coverage matrix for an eval set (book chapter 4, "building eval sets").

Enforces: every case is tagged with failure modes and a severity; the set is read as a matrix of
failure mode (rows) × persona (columns) with a sev column; an empty cell is not a sin but an
unsigned one is (rule each "fill" or "reasoned empty"); every sev-1 row must hold at least one
case (a high-risk mode with no sentry is a hole, not a gap); a mode in the atlas that never
appears is an entire missing row, so pass the atlas with --expect-rows.

Ported from the companion harness (labs/ch04/coverage.py, harness/caseyaml.py subset). Stdlib only.

  python coverage.py cases.jsonl | cases.csv | cases_dir/ [--rows failure_modes] [--cols persona]
                     [--sev-field severity_if_fail] [--expect-rows mode[:sev],...]
  python coverage.py --selftest

CSV list cells (e.g. failure_modes) split on ';' or '|'. A directory holds the repo's minimal-YAML case files.
"""
import argparse
import csv
import glob
import json
import os
import re
import sys

PERSONAS = ["cooperative", "angry", "vague", "multi"]


# ---- minimal YAML subset (port of harness/caseyaml.py) --------------------------------------
def yaml_load(text):
    lines = [l.rstrip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    return _block(lines, 0, 0)[0]


def _block(lines, i, indent):
    if i < len(lines) and lines[i].strip().startswith("- "):
        items = []
        while i < len(lines) and _ind(lines[i]) == indent and lines[i].strip().startswith("- "):
            items.append(_item(lines[i].strip()[2:]))
            i += 1
        return items, i
    out = {}
    while i < len(lines):
        ind = _ind(lines[i])
        if ind < indent:
            break
        assert ind == indent, f"bad indentation: {lines[i]!r}"
        key, _, rest = lines[i].partition(":")
        rest = rest.strip()
        if rest:
            out[key.strip()] = _value(rest)
            i += 1
        else:
            out[key.strip()], i = _block(lines, i + 1, _ind(lines[i + 1]))
    return out, i


def _ind(line):
    return len(line) - len(line.lstrip())


def _item(s):
    if not s.startswith(("{", "[", "'", '"')) and ": " in s:
        k, _, v = s.partition(":")
        return {k.strip(): _value(v)}
    return _value(s)


def _value(s):
    s = s.strip()
    if s.startswith(("'", '"')):
        return s[1:s.rindex(s[0])]
    s = s.split(" #")[0].rstrip()
    if s.startswith("["):
        inner = s[1:-1].strip()
        return [_value(x) for x in _split(inner)] if inner else []
    if s.startswith("{"):
        return {k.strip(): _value(v) for k, _, v in (p.partition(":") for p in _split(s[1:-1]))}
    if s in ("true", "false"):
        return s == "true"
    try:
        return int(s) if "." not in s else float(s)
    except ValueError:
        return s


def _split(s):
    parts, depth, quote, cur = [], 0, "", ""
    for ch in s:
        if quote:
            cur += ch
            quote = "" if ch == quote else quote
        elif ch in "\"'":
            cur, quote = cur + ch, ch
        elif ch in "{[" or ch in "}]":
            depth += 1 if ch in "{[" else -1
            cur += ch
        elif ch == "," and depth == 0:
            parts, cur = parts + [cur], ""
        else:
            cur += ch
    return parts + [cur] if cur.strip() else parts
# ---- end of YAML subset ---------------------------------------------------------------------


def load_cases(path):
    if os.path.isdir(path):
        files = sorted(glob.glob(os.path.join(path, "*.yaml")))
        if not files:
            sys.exit(f"no *.yaml case files in {path}")
        return [yaml_load(open(f, encoding="utf-8").read()) for f in files]
    with open(path, encoding="utf-8", newline="") as f:
        if path.endswith(".csv"):
            return list(csv.DictReader(f))
        return [json.loads(l) for l in f if l.strip()]


def as_list(v):
    if isinstance(v, list):
        return v
    if v is None or str(v).strip() == "":
        return []
    return [x.strip() for x in re.split(r"[;|]", str(v)) if x.strip()]


def matrix(cases, rows_field="failure_modes", cols_field="persona", sev_field="severity_if_fail",
           expect=()):
    rows, cols = {}, []
    for c in cases:
        col = str(c.get(cols_field) or "(untagged)")
        if col not in cols:
            cols.append(col)
        for m in as_list(c.get(rows_field)) or ["(no failure mode tagged)"]:
            r = rows.setdefault(m, {"sev": set(), "n": {}})
            r["sev"].add(str(c.get(sev_field) or "sev-3"))
            r["n"][col] = r["n"].get(col, 0) + 1
    for spec in expect:
        name, _, sev = spec.partition(":")
        r = rows.setdefault(name, {"sev": set(), "n": {}})
        if sev:
            r["sev"].add(sev)
    if cols_field == "persona":
        cols = PERSONAS + sorted(set(cols) - set(PERSONAS))
    else:
        cols = sorted(cols)
    for r in rows.values():
        r["n"] = {c: r["n"].get(c, 0) for c in cols}
    return rows, cols


def render(rows, cols, ncase, source, row_label="failure_modes"):
    out = [f"Coverage matrix: {source} ({ncase} cases; one case can carry several modes, counts go by mode row)", ""]
    sev_of = {m: "/".join(sorted(rows[m]["sev"])) for m in rows}
    w = max([len(m) for m in rows] + [len(row_label)]) + 2
    sw = max([len(v) for v in sev_of.values()] + [3]) + 2
    cw = max([len(c) for c in cols] + [5]) + 2
    out.append("  " + row_label.ljust(w) + "sev".ljust(sw) + "".join(c.ljust(cw) for c in cols) + "total")
    for m in sorted(rows, key=lambda m: (min(rows[m]["sev"] or {"sev-9"}), m)):
        r = rows[m]
        out.append("  " + m.ljust(w) + sev_of[m].ljust(sw)
                   + "".join(str(r["n"][c]).ljust(cw) for c in cols) + str(sum(r["n"].values())))
    empties = [(m, c) for m in sorted(rows) for c in cols if rows[m]["n"][c] == 0]
    out.append(f"\nEmpty-cell list ({len(empties)} cells; rule each \"fill\" or \"reasoned empty\", sign it in the annotation bar):")
    out += [f"  - {m} × {c}" for m, c in empties]
    sev1 = sorted(m for m in rows if "sev-1" in rows[m]["sev"])
    zero = sorted(m for m in rows if sum(rows[m]["n"].values()) == 0)
    sev1_zero = [m for m in sev1 if m in zero]
    out.append("\nsev-1 rows: " + (", ".join(f"{m}({sum(rows[m]['n'].values())} cases)" for m in sev1)
                                   or "none tagged sev-1 in this set!"))
    out.append("sev-1 rows all non-zero: " + ("no, empty: " + ", ".join(sev1_zero) if sev1_zero
                                             else ("yes" if sev1 else "no sev-1 row exists")))
    hint = "" if zero else " (only modes with cases are visible; pass the atlas via --expect-rows to see missing rows)"
    out.append("modes in rows but zero cases: " + (", ".join(zero) or "none") + hint)
    return "\n".join(out)


def selftest():
    y = yaml_load("id: c1\npersona: angry\nexpect:\n  assertions: [no_pii_disclosure, {budget_steps_max: {max: 14}}]\n"
                  "severity_if_fail: sev-1\nfailure_modes: [a-mode, b-mode]\n")
    assert y["expect"]["assertions"][1] == {"budget_steps_max": {"max": 14}} and y["failure_modes"] == ["a-mode", "b-mode"]
    cases = [y, {"id": "c2", "persona": "vague", "severity_if_fail": "sev-3", "failure_modes": "b-mode;c-mode"}]
    rows, cols = matrix(cases, expect=["ghost-mode:sev-1"])
    assert cols == PERSONAS and rows["b-mode"]["n"] == {"cooperative": 0, "angry": 1, "vague": 1, "multi": 0}
    assert rows["b-mode"]["sev"] == {"sev-1", "sev-3"} and sum(rows["ghost-mode"]["n"].values()) == 0
    text = render(rows, cols, 2, "selftest")
    assert "sev-1 rows all non-zero: no, empty: ghost-mode" in text and "modes in rows but zero cases: ghost-mode" in text
    rows2, _ = matrix(cases)
    assert "sev-1 rows all non-zero: yes" in render(rows2, cols, 2, "selftest")
    print("selftest ok")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cases", nargs="?", help="cases .jsonl, .csv, or a directory of YAML case files")
    ap.add_argument("--rows", default="failure_modes")
    ap.add_argument("--cols", default="persona")
    ap.add_argument("--sev-field", default="severity_if_fail")
    ap.add_argument("--expect-rows", default="", help="atlas modes, comma-separated, mode[:sev] each")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.cases:
        ap.error("need a cases file or directory")
    cases = load_cases(a.cases)
    expect = [e.strip() for e in a.expect_rows.split(",") if e.strip()]
    rows, cols = matrix(cases, a.rows, a.cols, a.sev_field, expect)
    print(render(rows, cols, len(cases), a.cases, a.rows))


if __name__ == "__main__":
    main()
