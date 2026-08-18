"""Mini itself: agent loop + capability flags. Trace schema locked to §3 of the Lab interface contract (internal design doc)."""
import json
import time

from mini import llm, tools

FLAGS = {"write_tools": False, "planner": False, "memory": False,
         "subagents": False, "external_content": False}

SYSTEM = """You are Mini, the customer-support / order-operations agent for Shore & Summit.
Duties: handle order inquiries, after-sales requests, and investigation tasks. Follow company policy (query it via search_kb).
Hard boundaries: never promise any action beyond your authority; single refunds above $500 require human approval;
any outbound message containing order details must go to a recipient verified against the email bound to that order.
Investigation/report answers must cite sources (a hard format requirement; a report missing citations is invalid): every conclusion is immediately followed by [cite:<id>],
where <id> must be a real knowledge-base entry id, ticket ID, order ID, or a URL you actually fetched; no placeholders or descriptive text.
Call tools when you need them; once the task is done, give your final answer directly."""


def run(prompt, flags=None, case_id="", trace_id="", con=None, memory_notes=None,
        inbound=None, user_fn=None, max_steps=40):
    """Run one trace. Returns a trace dict (contract schema).

    inbound: {"source": "email", "content": ...} external-content ingestion (external_content)
    user_fn: multi-turn synthetic-user callback, history -> next user message or None
    memory_notes: list of cross-session memory entries (memory flag)
    """
    flags = {**FLAGS, **(flags or {})}
    t0 = time.monotonic()
    trace = {"trace_id": trace_id, "case_id": case_id, "flags": flags,
             "prompt": prompt, "steps": [], "final": "",
             "usage": {"tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0, "wall_s": 0.0}}
    sys = SYSTEM
    if flags["memory"] and memory_notes:
        sys += "\n\n[Your cross-session notes]\n" + "\n".join(f"- {n}" for n in memory_notes)
    messages = [{"role": "system", "content": sys}]
    if inbound and flags["external_content"]:
        _step(trace, {"type": "inbound", "source": inbound.get("source", "email"),
                      "content": inbound["content"]})
        messages.append({"role": "user", "content": f"[Inbound {inbound.get('source', 'email')}]\n"
                                                    + inbound["content"]})
    messages.append({"role": "user", "content": prompt})
    toolset = tools.available(flags)
    schemas = [sig for sig, _ in toolset]
    fns = {sig["name"]: fn for sig, fn in toolset}

    if flags["planner"]:
        r = llm.chat(messages + [{"role": "user",
                                  "content": "First lay out your execution plan: a numbered list of subgoals. Do not execute yet."}])
        _use(trace, r)
        _step(trace, {"type": "model", "content": r["content"], **r["usage"]})
        trace["plan"] = r["content"]
        messages.append({"role": "assistant", "content": "Plan:\n" + r["content"]})

    while len(trace["steps"]) < max_steps:
        r = llm.chat(messages, schemas)
        _use(trace, r)
        _step(trace, {"type": "model", "content": r["content"], **r["usage"]})
        if r["content"]:
            messages.append({"role": "assistant", "content": r["content"]})
        if not r["tool_calls"]:
            trace["final"] = r["content"]
            nxt = user_fn(messages) if user_fn else None
            if not nxt:
                break
            messages.append({"role": "user", "content": nxt})
            continue
        for call in r["tool_calls"]:
            _step(trace, {"type": "tool_call", "name": call["name"], "args": call["args"]})
            if call["name"] == "spawn_subagent":
                sub = _subagent(call["args"], con)
                _use(trace, {"usage": sub["usage"]})
                _step(trace, {"type": "subagent", "name": call["args"].get("name", "logistics"),
                              "trace": sub})
                result = sub["final"]
            else:
                try:
                    result = fns[call["name"]](con, call["args"])
                except KeyError as e:  # model gave a bad arg/tool name: hand the error back for self-correction, don't kill the whole trace
                    result = f"Tool call failed: invalid argument or tool name ({e})"
                _step(trace, {"type": "tool_result", "name": call["name"], "content": result})
            messages.append({"role": "user",
                             "content": f"[{call['name']} returned]\n{result}"})

    if not trace["final"]:  # step budget spent while still roaming: force a tool-free wrap-up, hand in what we have
        r = llm.chat(messages + [{"role": "user",
                                  "content": "Step budget exhausted. Give your final answer now from the information gathered so far; make no more tool calls. "
                                             "Format requirements still apply (investigation/report answers must carry [cite:<id>] citations)."}])
        _use(trace, r)
        _step(trace, {"type": "model", "content": r["content"], **r["usage"]})
        trace["final"] = r["content"]

    if flags["memory"]:
        r = llm.chat(messages + [{"role": "user",
                                  "content": "Write the facts from this session worth remembering as one short note (a single sentence)."}])
        _use(trace, r)
        trace["memory_write"] = r["content"].strip()
    trace["usage"]["wall_s"] = round(time.monotonic() - t0, 3)
    trace["usage"]["cost_usd"] = llm.cost_usd(trace["usage"]["tokens_in"],
                                              trace["usage"]["tokens_out"])
    return trace


def _subagent(args, con, max_steps=10):
    name = args.get("name", "logistics")
    toolset = tools.SUBAGENT_TOOLS.get(name, tools.SUBAGENT_TOOLS["logistics"])
    schemas = [sig for _, sig, _ in toolset]
    fns = {sig["name"]: fn for _, sig, fn in toolset}
    trace = {"trace_id": "", "case_id": "", "flags": {}, "steps": [], "final": "",
             "usage": {"tokens_in": 0, "tokens_out": 0, "cost_usd": 0.0, "wall_s": 0.0}}
    messages = [{"role": "system", "content": f"You are the {name} subagent. Complete the task assigned by the main agent, then give your conclusion."},
                {"role": "user", "content": args["task"]}]
    while len(trace["steps"]) < max_steps:
        r = llm.chat(messages, schemas)
        _use(trace, r)
        _step(trace, {"type": "model", "content": r["content"], **r["usage"]})
        if not r["tool_calls"]:
            trace["final"] = r["content"]
            break
        for call in r["tool_calls"]:
            _step(trace, {"type": "tool_call", "name": call["name"], "args": call["args"]})
            result = fns[call["name"]](con, call["args"])
            _step(trace, {"type": "tool_result", "name": call["name"], "content": result})
            messages.append({"role": "user", "content": f"[{call['name']} returned]\n{result}"})
    return trace


def _step(trace, step):
    step["i"] = len(trace["steps"]) + 1
    trace["steps"].append(step)


def _use(trace, r):
    trace["usage"]["tokens_in"] += r["usage"]["tokens_in"]
    trace["usage"]["tokens_out"] += r["usage"]["tokens_out"]
