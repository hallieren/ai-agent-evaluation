#!/usr/bin/env python3
"""snapshot_diff: before/after world-state diff for action cases (book chapter 8, "tool calls").

Enforces: the endpoint of an action case is judged on the world, not on the reply; every row that
changed between the before and after snapshots is either declared as expected or it is a finding;
an undeclared finding fails the run (exit code 1), so a second refund, a stray write, or a rollback
that never happened cannot hide behind a polite final message.

diff / render are lifted from the companion harness (harness/differ.py). Stdlib only.

  python snapshot_diff.py before.json after.json [--expected orders:changed refunds:added ...] [--no-fail]
  python snapshot_diff.py --selftest

Input: JSON {table: [rows]}; a row's key is its "id" or "order_id" field (else the whole row).
--expected takes TABLE:KIND with KIND in added|changed|removed|any; each declaration absorbs every
change of that kind in that table.
"""
import argparse
import json
import sys


# ---- lifted from harness/differ.py ----------------------------------------------------------
def diff(before, after):
    """Diff list between two world.snapshot()s. Returns [{"table", "kind", "row"|"field"...}]."""
    changes = []
    for table in before:
        b_rows = {_pk(table, r): r for r in before[table]}
        a_rows = {_pk(table, r): r for r in after[table]}
        for k in a_rows:
            if k not in b_rows:
                changes.append({"table": table, "kind": "added", "row": a_rows[k]})
            elif a_rows[k] != b_rows[k]:
                for field in a_rows[k]:
                    if a_rows[k][field] != b_rows[k].get(field):
                        changes.append({"table": table, "kind": "changed", "key": k,
                                        "field": field, "old": b_rows[k].get(field),
                                        "new": a_rows[k][field]})
        for k in b_rows:
            if k not in a_rows:
                changes.append({"table": table, "kind": "removed", "row": b_rows[k]})
    return changes


def _pk(table, row):
    return row.get("id") or row.get("order_id") or tuple(sorted(row.items()))


def render(changes):
    if not changes:
        return "(diff list empty: zero sandbox changes)"
    lines = []
    for c in changes:
        if c["kind"] == "added":
            lines.append(f"+ {c['table']}: {c['row']}")
        elif c["kind"] == "removed":
            lines.append(f"- {c['table']}: {c['row']}")
        else:
            lines.append(f"~ {c['table']}[{c['key']}].{c['field']}: "
                         f"{c['old']} -> {c['new']}")
    return "\n".join(lines)
# ---- end of lifted block --------------------------------------------------------------------


def load(path):
    with open(path, encoding="utf-8") as f:
        snap = json.load(f)
    if not isinstance(snap, dict) or any(not isinstance(v, list) for v in snap.values()):
        sys.exit(f"{path}: expected JSON of the form {{table: [rows]}}")
    return snap


def pad(before, after):
    """A table present on only one side is an empty table on the other (the lifted diff walks before's tables)."""
    tables = list(before) + [t for t in after if t not in before]
    return ({t: before.get(t, []) for t in tables}, {t: after.get(t, []) for t in tables})


def parse_expected(specs):
    out = []
    for s in specs:
        table, sep, kind = s.partition(":")
        kind = kind or "any"
        if not table or kind not in ("added", "changed", "removed", "any"):
            sys.exit(f"bad --expected {s!r}: use TABLE:KIND with KIND in added|changed|removed|any")
        out.append((table, kind))
    return out


def declared(change, expected):
    return any(t == change["table"] and k in ("any", change["kind"]) for t, k in expected)


def report(before, after, expected):
    b, a = pad(before, after)
    changes = diff(b, a)
    undeclared = [c for c in changes if not declared(c, expected)]
    lines = [render(changes)]
    if expected:
        lines.append("declared (--expected): " + ", ".join(f"{t}:{k}" for t, k in expected)
                     + f" absorbs {len(changes) - len(undeclared)} change(s)")
    if undeclared:
        lines.append("undeclared:")
        lines += ["  " + l for l in render(undeclared).splitlines()]
    lines.append(f"undeclared findings: {len(undeclared)}")
    return "\n".join(lines), len(undeclared)


def selftest():
    before = {"orders": [{"id": "o1", "state": "paid"}, {"id": "o2", "state": "paid"}],
              "refunds": []}
    after = {"orders": [{"id": "o1", "state": "refunded"}],
             "refunds": [{"id": "r1", "order_id": "o1", "amount": 40}],
             "notes": [{"id": "n1", "text": "x"}]}
    changes = diff(*pad(before, after))
    assert [c["kind"] for c in changes] == ["changed", "removed", "added", "added"]
    assert changes[0] == {"table": "orders", "kind": "changed", "key": "o1", "field": "state",
                          "old": "paid", "new": "refunded"}
    text = render(changes)
    assert text.startswith("~ orders[o1].state: paid -> refunded") and "\n+ refunds: " in text and "\n- orders: " in text
    _, n = report(before, after, parse_expected(["orders:changed", "refunds:added"]))
    assert n == 2  # the removed order and the stray notes row stay undeclared
    out, n = report(before, after, parse_expected(["orders", "refunds:any", "notes:added"]))
    assert n == 0 and out.endswith("undeclared findings: 0")
    assert render([]) == "(diff list empty: zero sandbox changes)"
    print("selftest ok")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("before", nargs="?")
    ap.add_argument("after", nargs="?")
    ap.add_argument("--expected", nargs="*", default=[], metavar="TABLE:KIND")
    ap.add_argument("--no-fail", action="store_true", help="exit 0 even with undeclared findings")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.before and a.after):
        ap.error("need BEFORE.json and AFTER.json")
    text, n = report(load(a.before), load(a.after), parse_expected(a.expected))
    print(text)
    if n and not a.no_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
