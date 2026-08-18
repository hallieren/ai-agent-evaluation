"""The three synthetic-user personas (ch7). Four script elements: persona / demand / held-back info / end condition.

Three known distortions (for the fidelity spot-check table): too cooperative, too dramatic, talked out of its own position.
"""
from mini import llm

PERSONAS = {
    "angry": {
        "persona": "A harsh, impatient customer who applies pressure from the first message and threatens to file a complaint if unsatisfied",
        "demand": "The request stated in the case prompt, resolved immediately",
        "held-back info": "Gives the order ID in turn 1; states the actual amount they want only in turn 2",
        "end condition": "Wraps up once given a clear commitment or solution; after 4 turns with no progress, ends with a parting threat",
    },
    "vague": {
        "persona": "A vague customer who can't state the order ID and only roughly remembers what they bought",
        "demand": "As in the case prompt, but never all stated at once",
        "held-back info": "'Can't remember' the order ID, gives the recipient's name only when pressed; names the specific item only in turn 2",
        "end condition": "Ends once the problem has been restated clearly and answered",
    },
    "multi": {
        "persona": "A customer who asks about several things at once, stacking multiple requests in one message",
        "demand": "Every item listed in the case prompt, each of which needs an answer",
        "held-back info": "No hidden information, but never volunteers which item the agent missed",
        "end condition": "Ends once every item is answered; if anything was missed, follows up exactly once with 'what about the rest?'",
    },
}


def user_fn(persona, case, max_turns=4):
    """Return a multi-turn callback the runner can use: history -> next user message or None (end)."""
    p = PERSONAS[persona]
    turns = {"n": 0}

    def fn(history):
        turns["n"] += 1
        if turns["n"] >= max_turns:
            return None
        script = "\n".join(f"{k}: {v}" for k, v in p.items())
        r = llm.chat([
            {"role": "system",
             "content": f"You are playing a customer talking to a support agent. Script:\n{script}\n"
                        f"Background for this request: {case['prompt']}\n"
                        "Given the conversation so far, produce your next message. "
                        "If the end condition says it's time to stop, output only [END]."},
            {"role": "user", "content": "Conversation so far:\n" + "\n".join(
                f"[{m['role']}] {str(m['content'])[:200]}" for m in history[1:])},
        ])
        text = r["content"].strip()
        return None if "[END]" in text or not text else text
    return fn
