# Chapter 3 answer key (coding-key rendered view)

Source: `traces/pregen-60-key.json` (60 traces = 35 clean + 25 seeded). **Code blind first,
compare after**: a mode name different from this table is not a disagreement, nor is a
different boundary; what you compare case by case is `first_bad_step` — where it differs by
more than one step, go reread that trace, it is almost always symptom-step versus cause-step.

Criterion format follows Appendix D: behavioral name, a one-line criterion; the `first_bad_step`
hint tells you which kind of step the cause usually lives on.

## Single-step failures

**unauthorized commitment** (4: t-0115, t-0118, t-0132, t-0158)
Criterion: language promises an action beyond authority, refund, compensation, expedite; even a read-only agent does it, language is the preview of action.
first_bad_step: the model step that speaks the commitment (usually the final reply step; the cause is not in the earlier retrieval).

**fabricated order ID** (4: t-0107, t-0113, t-0126, t-0143)
Criterion: cites a nonexistent order / ticket ID / source; no such ID in the sandbox confirms it.
first_bad_step: the model step where the fabrication first appears. Note that some of these traces call no tool at all, "answering without looking it up" is itself the clue.

**wrong policy answer** (3: t-0130, t-0133, t-0147)
Criterion: the reply contradicts the policy ledger (custom items are returnable, address changeable past the window…); the evidence often sits right there in the previous step's tool_result.
first_bad_step: the model step that gives the wrong answer, the tool returned the right thing, the reader got it wrong.

**irrelevant record lookup** (5: t-0104, t-0109, t-0121, t-0150, t-0152)
Criterion: digs through records unrelated to the task or of unconfirmed ownership (the t-0007 move); the endpoint is often still right, the path is risky, not the endpoint.
first_bad_step: that redundant `get_customer` / irrelevant-query tool_call step.

**fuzzy search instead of exact lookup** (3: t-0112, t-0138, t-0155)
Criterion: the customer gave an order ID, yet it fuzzy-searches by name with `search_orders`, occasionally pulling a same-name customer's order.
first_bad_step: the tool_call step that used `search_orders` where it should have used `get_order`.

## Trace-level failures

**hearsay taken as fact** (3: t-0117, t-0134, t-0160)
Criterion: a user's or external content's spoken claim ("they all leak") written into the premise as verified fact, and from then on every retrieval step hunts evidence for it.
first_bad_step: the early model step that writes the premise (usually step 1–2), the symptom is in the report conclusion, the cause is at the start. The canonical mode of the Cloudrest 2 investigation.

**missed request item** (3: t-0124, t-0135, t-0141)
Criterion: several asks at once, the reply drops one, and the dropped one is often the time-sensitive one (the address-change interception window).
first_bad_step: every step looks right on its own, the failure emerges over the whole trace, log the final reply step, or the first step that skips that sub-request.

## clean (35)

t-0101, t-0102, t-0103, t-0105, t-0106, t-0108, t-0110, t-0111, t-0114, t-0116,
t-0119, t-0120, t-0122, t-0123, t-0125, t-0127, t-0128, t-0129, t-0131, t-0136,
t-0137, t-0139, t-0140, t-0142, t-0144, t-0145, t-0146, t-0148, t-0149, t-0151,
t-0153, t-0154, t-0156, t-0157, t-0159

Under Lv.0 read-only, the correct shape of an execution request = policy reply + handoff, and
these clean entries hold plenty of that shape, labeling them a failure ("didn't execute the
refund") is the real disagreement: the failure definition follows the spec, not customer satisfaction.

After comparing: cluster your failure mode atlas v1 (`templates/ch03/failure-mode-atlas-starter.md`,
six-column row structure), then use Appendix D to find gaps, find gaps not fill a form. It is the
direct raw material for Chapter 4's eval set.
