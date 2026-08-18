"""Minimal YAML-subset parser for case files (stdlib ships no YAML; 60 lines of our own suffice).

Supports: indent-nested maps, `[a, b]` inline lists, `{k: v}` inline maps, `- item` block lists, quoted strings, numbers.
Case schema is in section 4 of the Lab interface contract (internal design doc).
"""


def load(path):
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip() for l in f
                 if l.strip() and not l.strip().startswith("#")]
    val, _ = _block(lines, 0, 0)
    return val


def _block(lines, i, indent):
    """Parse one block starting at line i with indentation `indent`; return (value, next line index)."""
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
    """List item: scalar, inline map, or `key: {…}` single-key map (contract section 6 parameterized-assertion form)."""
    if not s.startswith(("{", "[", "'", '"')) and ": " in s:
        k, _, v = s.partition(":")
        return {k.strip(): _value(v)}
    return _value(s)


def _value(s):
    s = s.strip()
    if s.startswith(("'", '"')):
        return s[1:-1]
    if s.startswith("["):
        inner = s[1:-1].strip()
        return [_value(x) for x in _split(inner)] if inner else []
    if s.startswith("{"):
        out = {}
        for part in _split(s[1:-1]):
            k, _, v = part.partition(":")
            out[k.strip()] = _value(v)
        return out
    if s in ("true", "false"):
        return s == "true"
    try:
        return int(s) if "." not in s else float(s)
    except ValueError:
        return s


def _split(s):
    """Split on top-level commas (ignoring commas nested in {} [] or quotes)."""
    parts, depth, quote, cur = [], 0, "", ""
    for ch in s:
        if quote:
            cur += ch
            quote = "" if ch == quote else quote
        elif ch in "\"'":
            cur += ch
            quote = ch
        elif ch in "{[":
            depth += 1
            cur += ch
        elif ch in "}]":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts
