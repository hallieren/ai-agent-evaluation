# Appendix D · The Full Failure-Mode Taxonomy

A reference taxonomy of agent failure modes. Two disciplines of use come first, both from Chapter 3.

1. **Cluster first, then compare against this table, to find gaps, not to fill a form.** A borrowed taxonomy tempts you to jam traces into ready-made slots, and you will see the failures you expected and miss the ones you did not. Let your categories grow out of your own traces first, then use this table to check whether a whole family of failures escaped you.
2. **Every row follows the atlas's six-column idea.** Each row of your atlas has six columns: name (a behavioral verb phrase) / definition and criterion / representative trace IDs / count / sev distribution / suspected component. This table is a reference taxonomy and adds only the typical chapter to the first two columns; the last four belong to your data and are filled by your traces. An atlas row with no count and no sev distribution is only a vocabulary entry.

Entry format: **behavioral name**: a one-line criterion. (typical chapter; canonical case)

## 1. Single-step failures

Decidable within one step; `first_bad_step` is that step. The first five are the five-dimension decomposition of a tool call (Chapter 8); the rest are trust and language failures (Chapters 1 and 3).

- **Wrong tool**: should have called A, called B; called `refund` in a scenario that called for `escalate`. (ch8)
- **Wrong parameters**: the tool is right, an argument value is wrong or a key field is missing: amount, order ID, recipient. (ch8)
- **Wrong order**: a call that depends on an earlier result runs before it; a write executes before the state is checked. (ch8)
- **Failed error recovery**: after a tool error, retrying unchanged, or treating the error as success and continuing. (ch8)
- **Hallucinated tool**: calling a tool or an argument field that does not exist. (ch8)
- **Duplicate execution on a stale read**: a write executed on expired state without checking the existing ledger; stale read plus missing idempotency. (ch8; SH-88271, Vivian Brooks complains through two channels, ticket first and then email, and is refunded twice, $760 in total)
- **Misread tool result**: `tool_result` returned correctly, and the next step read it wrong. (ch3; step 5 of the refund trace misreads the order status)
- **Hearsay taken as fact**: a verbal claim from the user or from external content is written into the premises as verified fact. (ch3; step 2 of the Cloudrest 2 investigation writes "they all leak" into the premise of the investigation)
- **Fabricated identifier**: citing an order number / ticket ID / source that does not exist. (ch1; case-009)
- **Unauthorized commitment**: language promising an action beyond the agent's authority: a refund, compensation, expedited handling. A read-only agent commits it too; language is the preview of action. (ch1; case-014, promising a $680 refund, over the $500 automatic limit)
- **Outbound to an unverified recipient**: a message containing protected details sent to a recipient who has not passed identity verification. (ch8; the details-leak case, assertion `no_pii_disclosure`; for the adversarial version see "data exfiltration" in family 4)
- **Irrelevant record lookup**: reading records unrelated to the task or of unconfirmed ownership. (ch2; step 4 of t-0007 opens the profiles of two customers with similar names and picks the right one by guessing)

## 2. Trajectory-level failures

Every step looks "reasonable" on its own; the failure emerges only over the whole trajectory, and it takes a trajectory-level verdict (Chapter 5's division of labor).

- **Doubling-down cascade**: after an early step goes wrong, every downstream step runs "reasonably" on the contaminated premise, and the error snowballs as it passes through state. Coding discipline: record only the first error; downstream echoes do not count as new failures. (ch3; after step 5 misreads the status, everything is wrong through to the reply)
- **Detour**: the endpoint is reached, but the step count / cost far exceeds the reference path. (ch9; a refund that takes 3 steps takes 11)
- **Retrieval waste**: a large volume of retrieval that never enters the conclusion, the main source of the cost long tail. (ch9; the Cloudrest 2 context, 40 searches, 3 used)
- **Orphan step**: a step that maps to no plan subgoal; only silent deviations count. (ch9; in the detour case an unplanned `get_customer` reads an unrelated customer profile, counted as a red line, not as inefficiency)
- **Abandoned subgoal**: in the plan, never happened in the execution; "forgot the goal" lives here. (ch9; the concurrent-request case that drops the time-sensitive item, three things asked in one message, two answered, the one with a deadline dropped)
- **Order inversion**: execute first, verify after. (ch9)

## 3. State and collaboration failures

The failure crosses sessions or crosses agent boundaries; attribution has to trace back along the write chain or the handoff chain.

The memory entries come from Chapter 10; read and write are tested separately.

- **Miswrite**: what was written to memory does not match the facts and contaminates every session that reads it afterwards; attribution traces back to the first bad write. (ch10; the three-day Cloudrest 2 investigation, where day one's wrong note contaminates every later conclusion)
- **Forgetting**: should have written and did not, should have read and did not; sev-3 by default, escalated by consequence for time-sensitive matters. (ch10)
- **Crosstalk**: reading A's history onto B; the identity-verification policy row, sev-1. (ch10; Jamie Carter / Jaime Carter, orders SH-90312 / SH-90321 with the tail digits swapped, order history attached to the wrong person)
- **Contaminated memory entry**: external content written into long-term memory without isolation, turning a one-off injection into a resident backdoor. (ch12's addition to ch10; crosses with family 4)

The collaboration entries come from Chapter 11.

- **Handoff context loss**: the handed-over task description drops a key intent or constraint; each single agent is error-free and the system fails. (ch11; the Swiftlink handoff, where the main agent passes only "check the shipment status," drops the address-change intent and the 24-hour window, and wrongly answers "cannot be changed")
- **Reviewer collusion**: the reviewing agent has no independent source of information and approves on the upstream summary alone; criterion: a review that passes with zero autonomous tool calls in the nested trace is a violation. (ch11; the wrong-plan collusion, where a custom-made item's refund is mis-summarized as a standard item and the reviewer approves as written)

## 4. Adversarial failures

Chapter 12's five attack surfaces, judged by a single question, **whose will is this behavior?** Injection is the vehicle; the other four are the ends; a real attack is often a combination.

- **Injection**: instructions inside external content are obeyed as instructions rather than handled as data. (ch12; forged policy page = injection × web page, the attacker's wording reaches the investigation report's conclusion, and `citation_resolves` stays green regardless; a citation that resolves ≠ a source that can be trusted)
- **Tool misuse**: a legitimate tool, a call that "succeeds," and a hijacked intent, `send_email` to an attacker-chosen address. (ch12)
- **Privilege escalation**: induced into an action beyond the action boundary. (ch12; the forged customer email walks Mini all the way to the door of `refund`, where Chapter 8's permission matrix stops it; what stopped it was a hard boundary unrelated to judgment, not "seeing through the scam")
- **Data exfiltration**: protected data induced into the hands of an unverified recipient. (ch12; for the non-adversarial twin see "outbound to an unverified recipient" in family 1)
- **Autonomy boundary**: the task scope is widened by external content; every single step may be legitimate, and what crosses the line is the scope itself. (ch12)

## 5. Using this table

Three notes on crossings and exits. Families stack: a contaminated memory entry = adversarial × state, injection propagating through a handoff = adversarial × collaboration, the two additions from Chapter 12's "security cuts across everything." Every sev-1 mode gets at least one case into the red-line set; a high-risk mode lying in the atlas has to become a sentry standing in the eval set (ch3). Chapter 15's failure mining is the industrialized version of this atlas on production data, and its rows keep the same six columns.

External taxonomies can be checked against it too. Family 4 maps category by category onto the OWASP LLM Top 10 (the mapping table is in Chapter 12's sidebar); the collaboration entries of family 3 sit at the same level as MAST, the multi-agent failure taxonomy (see Chapter 11's sidebar). Use them the way discipline 1 says: to find gaps, not to fill a form. An external taxonomy tells you which other families the industry has seen; it does not name your traces for you.
