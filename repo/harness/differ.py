"""before/after differ (ch8). Semantics: every change is either declared as expected, or it is a finding."""


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
