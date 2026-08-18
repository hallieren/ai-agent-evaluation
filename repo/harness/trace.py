"""Trace persistence and loading (JSONL, one trace per line). Schema is in contract section 3."""
import json


def save(traces, path):
    with open(path, "w", encoding="utf-8") as f:
        for t in traces:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def flat_steps(tr):
    """Flatten the steps; nested subagent steps come out as (depth, step). Chapter 11's attribution slices on this."""
    out = []

    def walk(steps, depth):
        for s in steps:
            out.append((depth, s))
            if s["type"] == "subagent":
                walk(s["trace"]["steps"], depth + 1)
    walk(tr["steps"], 0)
    return out


def tool_calls(tr, name=None, nested=True):
    """All tool_call steps (nested included by default)."""
    steps = [s for _, s in flat_steps(tr)] if nested else tr["steps"]
    return [s for s in steps
            if s["type"] == "tool_call" and (name is None or s["name"] == name)]


def total_usage(tr):
    """Multi-agent cost accounting (ch11): the outer usage already includes the nested totals; here it is broken out into three columns."""
    sub = [s["trace"]["usage"] for _, s in flat_steps(tr) if s["type"] == "subagent"]
    sub_in = sum(u["tokens_in"] for u in sub)
    sub_out = sum(u["tokens_out"] for u in sub)
    return {"total": tr["usage"],
            "main": {"tokens_in": tr["usage"]["tokens_in"] - sub_in,
                     "tokens_out": tr["usage"]["tokens_out"] - sub_out},
            "subagents": {"tokens_in": sub_in, "tokens_out": sub_out},
            "handoffs": len(sub)}
