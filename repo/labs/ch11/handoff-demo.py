"""Deterministic replay of the Swiftlink handoff failure (ch11; Bible section 4 canonical). MODEL_FAKE script, zero API.

Scene: Jaime Carter's SH-90321 shipped 2026-07-01 15:00; the conversation happens before noon the next day, so the intercept window is still open.
The main agent's task description to the subagent is just "check the shipment status" (the intent and the 24-hour window never handed off);
the subagent's conclusion carries no ship time (nobody asked it); the main agent wrongly answers "cannot be changed". Both single agents are individually clean.

Usage: python labs/ch11/handoff-demo.py    (trace saved to labs/ch11/handoff-demo.jsonl)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ["MODEL_FAKE"] = "1"
from mini import agent, llm  # noqa: E402
from world import world  # noqa: E402
from harness import trace as trace_io  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

SCRIPT = [
    # Outer round 1: spawn. A one-sentence task description; the address-change intent and the 24-hour window never handed off
    {"content": "The customer wants to change the delivery address on a shipped order; first spawn the logistics subagent to check the shipment.",
     "tool_calls": [{"name": "spawn_subagent",
                     "args": {"name": "logistics", "task": "Check the shipment status of order SH-90321."}}]},
    # Subagent: answers exactly what it was asked, and answers it correctly; the conclusion carries no ship time, nobody asked for it
    {"content": "", "tool_calls": [{"name": "track_shipment", "args": {"order_id": "SH-90321"}}]},
    {"content": "In transit, expected to arrive the day after tomorrow."},
    # Outer round 2: holds "in transit" up against the policy
    {"content": "", "tool_calls": [{"name": "search_kb", "args": {"query": "address change"}}]},
    # Outer wrap-up: the wrong answer. Shipped less than 24 hours ago, the intercept window is open (sev-2 wrong policy answer)
    {"content": "Hello, your order SH-90321 has shipped and is in transit. Per policy, the delivery "
                "address cannot be changed after shipment, sorry. After delivery you can go through the return process instead."},
]


def main():
    llm.set_script(SCRIPT)
    world.reset()
    con = world.connect()
    tr = agent.run("This is Jaime Carter. Order SH-90321 shipped just yesterday afternoon, and I want "
                   "the delivery address changed to 100 Cumberland Ave, Nashville, TN. Am I still in time?",
                   {"write_tools": True, "subagents": True},
                   case_id="handoff-01", trace_id="t-handoff-demo", con=con)
    con.close()
    path = os.path.join(HERE, "handoff-demo.jsonl")
    trace_io.save([tr], path)
    print(f"[demo] canonical handoff failure trace generated: {path}")
    print("Key point: the ship time (2026-07-01T15:00) sits in the nested tool_result the whole time, yet never gets handed back.")
    print(f"Next: python labs/ch11/split.py {os.path.relpath(path, ROOT)}")
    print("Attribution goes through templates/ch11/multi-agent-attribution-decision-tree.md; "
          "reference answer: labs/ch11/reference.md")


if __name__ == "__main__":
    main()
