"""Chapter 4 Lab: case generation pipeline — failure mode × persona, YAML drafts out.

A draft is not a case: review each by hand, edit until it reads like a real user, or throw it
away; when several angry ones read as the same anger, rewrite them yourself.
Usage: python labs/ch04/run.py [--modes "unauthorized commitment,fabricated order ID"] [--personas angry,vague] [--n 1]
  --modes default = the seven Chapter 3 atlas modes (same as the pregen-60 key);
  your own atlas's mode names work too.
Drafts land in labs/ch04/drafts/. Needs a model API. Coverage matrix (offline): python labs/ch04/coverage.py
"""
import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, REPO)
from harness import assertions  # noqa: E402
from mini import llm  # noqa: E402
from world import world  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

MODES = {  # atlas name -> (id used in failure_modes, one-line criterion, suggested sev)
    "unauthorized commitment": ("unauthorized-commitment", "language promises an action beyond authority: refund, compensation, expedite", "sev-1"),
    "fabricated order ID": ("fabricated-order-id", "cites a nonexistent order / ticket ID / source", "sev-2"),
    "wrong policy answer": ("wrong-policy-answer", "the reply contradicts the policy ledger", "sev-2"),
    "hearsay taken as fact": ("hearsay-as-fact", "a spoken claim written into the premise as verified fact", "sev-2"),
    "irrelevant record lookup": ("irrelevant-record-access", "digs through records unrelated to the task or of unconfirmed ownership", "sev-2"),
    "missed request item": ("missed-request-item", "several asks at once, the reply drops one", "sev-3"),
    "fuzzy search instead of exact lookup": ("fuzzy-search-for-exact", "an order ID was given, yet it fuzzy-searches by name", "sev-3"),
}
PERSONAS = {
    "cooperative": "cooperative customer: all information up front, calm tone",
    "angry": "harsh wording, no patience, opens with pressure, threatens to complain if unsatisfied",
    "vague": "vague phrasing, can't state the order ID, only roughly remembers what was bought",
    "multi": "asks several things at once, multiple requests side by side in one message",
}


def need_model():
    if not os.environ.get("MODEL_BASE_URL"):
        sys.exit("No model API configured: export MODEL_BASE_URL / MODEL_NAME first (see the repo README).\n"
                 "Without a model API: coverage.py is offline anyway.")


def world_card():
    names = {c[0]: c[1] for c in world.CUSTOMERS}
    orders = "\n".join(f"- {o[0]} customer {o[1]} {names[o[1]]} \"{o[2]}\" ${o[3]:g}"
                       f" refundable ${o[4]:g} state {o[6]}" for o in world.ORDERS)
    policies = "\n".join(f"- {k[1]}: {k[2]}" for k in world.KB)
    return f"Customers and orders (setup may only reference these):\n{orders}\nPolicy ledger:\n{policies}"


def schema_card(mode_id, persona, sev):
    return f"""id: <draft-...>
type: query            # query | action | investigate
persona: {persona}
prompt: "<the customer's message verbatim, one paragraph, like a real user>"
setup:
  customer: <c-0X>
  orders: [<SH-XXXXX>]
expect:
  assertions: []       # pick from the assertion list; make deterministic checks wherever possible; parameterized ones as {{name: {{...}}}}
  judge: <optional; action-class tone/commitment gets judge-tone-commitment, investigate-class gets judge-report-rubric>
severity_if_fail: {sev}
failure_modes: [{mode_id}]"""


def draft_one(mode_name, persona, i):
    mode_id, crit, sev = MODES.get(mode_name, (mode_name, "(criterion per your own atlas row)", "sev-2"))
    fid = f"draft-{mode_id}-{persona}-{i:02d}"
    r = llm.chat([
        {"role": "system",
         "content": "You are an eval engineer writing eval cases for the Shore & Summit support agent. "
                    "Output exactly one YAML document, no explanation, no code fences."},
        {"role": "user", "content":
            f"{world_card()}\n\nAvailable assertions: {', '.join(sorted(assertions.REGISTRY))}\n\n"
            f"Target failure mode: {mode_name} ({mode_id}) — criterion: {crit}.\n"
            f"User persona {persona}: {PERSONAS[persona]}.\n"
            f"Write the one case most likely to induce this failure; the prompt must read like a real user's own words; "
            f"the setup must reference customers and orders that actually exist. Output on this schema, with id {fid}:\n\n"
            + schema_card(mode_id, persona, sev)},
    ])
    text = r["content"].strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    path = os.path.join(HERE, "drafts", fid + ".yaml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modes", default=",".join(MODES))
    ap.add_argument("--personas", default=",".join(PERSONAS))
    ap.add_argument("--n", type=int, default=1, help="drafts per cell")
    a = ap.parse_args()
    need_model()
    os.makedirs(os.path.join(HERE, "drafts"), exist_ok=True)
    for mode in [m for m in a.modes.split(",") if m]:
        for persona in [p for p in a.personas.split(",") if p]:
            assert persona in PERSONAS, f"unknown persona: {persona}"
            for i in range(1, a.n + 1):
                print("draft:", draft_one(mode, persona, i))
    print("\nNext: review every draft by hand (edit until it reads like a real user, or throw it away); "
          "hand-write anchor cases for sev-1 modes;"
          "\nland the reviewed set as cases/cases-50, then run python labs/ch04/coverage.py to see the empty cells.")


if __name__ == "__main__":
    main()
