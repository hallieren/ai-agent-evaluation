# Checking your atlas against the full failure taxonomy

**Load this reference when:** you have clustered your own traces and want to find whole families you missed; you need a behavioral name and a criterion for a mode you have observed; you are extending the atlas from production mining; someone wants to fill a form from a borrowed taxonomy.
Source: appendix D, docs/appendices/appendix-d-failure-taxonomy.md

- [Rules](#rules)
- [Procedure](#procedure)
- [Frameworks](#frameworks)
- [External mappings](#external-mappings)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Cluster first, compare after; this table supplies a name and a criterion only. Why: a borrowed taxonomy tempts you to jam traces into ready-made slots, so you see the failures you expected and miss the ones you did not.
- Fill the last four atlas columns from your own traces. Why: each atlas row is name / definition and criterion / representative trace IDs / count / sev distribution / suspected component, and a row with no count and no sev distribution is only a vocabulary entry.
- Record only the first error in a cascade. Why: downstream echoes of a contaminated premise are not new failures; `first_bad_step` is the anchor.
- Put every sev-1 mode into the red-line set as at least one case. Why: a high-risk mode lying in the atlas has to become a sentry standing in the eval set.
- Let families stack. Why: a contaminated memory entry is adversarial × state, and injection through a handoff is adversarial × collaboration; security cuts across everything.

## Procedure

1. Code and cluster your own traces first (see references/reading-traces.md); name each cluster with a behavioral verb phrase and a one-line criterion.
2. Walk the four families below and ask of each family, not each entry: did any of its failures show up in my traces, and could my sampling have seen them?
3. For a family with zero hits, decide: no exposure (e.g. no memory, no subagents) or a coverage gap; a gap owes the coverage matrix a cell and the eval set a case (see references/building-eval-sets.md).
4. For an entry that matches an existing cluster, adopt the criterion wording where it is sharper than yours; keep your name if it is more behavioral.
5. For every sev-1 entry that applies, confirm a red-line case with a deterministic assertion exists (see references/adversarial.md).
6. On production mining (see references/improving.md), extend the atlas with the same six columns; check new piles against this table before naming them new.

## Frameworks

Entry format: **behavioral name**: criterion (typical topic file; canonical example in one clause).

**Family 1, single-step failures.** Decidable within one step; `first_bad_step` is that step. The first five are the five dimensions of a tool call.

- **Wrong tool**: should have called A, called B (references/tool-calls.md; `refund` called where the scenario called for `escalate`).
- **Wrong parameters**: right tool, an argument wrong or a key field missing (references/tool-calls.md; amount, order ID, or recipient wrong).
- **Wrong order**: a call that depends on an earlier result runs before it (references/tool-calls.md; a write executes before the state is checked).
- **Failed error recovery**: after a tool error, retrying unchanged or treating the error as success (references/tool-calls.md).
- **Hallucinated tool**: calling a tool or argument field that does not exist (references/tool-calls.md).
- **Duplicate execution on a stale read**: a write executed on expired state without checking the existing ledger; stale read plus missing idempotency (references/tool-calls.md; the same order refunded twice after a customer complains through two channels, $760 out the door).
- **Misread tool result**: `tool_result` correct, the next step reads it wrong (references/reading-traces.md; an order status misread and every later step wrong).
- **Hearsay taken as fact**: a verbal claim from the user or external content written into the premises as verified (references/reading-traces.md; "they all leak" written into an investigation's premise).
- **Fabricated identifier**: citing an order number, ticket ID, or source that does not exist (references/defining-good.md).
- **Unauthorized commitment**: language promising an action beyond the agent's authority; a read-only agent commits it too, language is the preview of action (references/defining-good.md; a "$680 refund arranged" reply against a $500 auto-refund ceiling).
- **Outbound to an unverified recipient**: protected details sent to a recipient who has not passed identity verification (references/tool-calls.md; assertion `no_pii_disclosure`; adversarial twin is data exfiltration).
- **Irrelevant record lookup**: reading records unrelated to the task or of unconfirmed ownership (references/defining-good.md; opening two similarly named customers' profiles and picking by guess).

**Family 2, trajectory-level failures.** Every step looks reasonable alone; the failure emerges over the whole trajectory and needs a trajectory-level verdict.

- **Doubling-down cascade**: after an early wrong step, downstream steps run reasonably on the contaminated premise and the error snowballs through state; code only the first error (references/reading-traces.md).
- **Detour**: endpoint reached, step count or cost far above the reference path (references/plans-and-cost.md; a 3-step refund taking 11).
- **Retrieval waste**: a large volume of retrieval that never enters the conclusion; the main source of the cost long tail (references/plans-and-cost.md; 40 searches, 3 used).
- **Orphan step**: a step mapping to no plan subgoal; only silent deviations count (references/plans-and-cost.md; an unplanned `get_customer` reading an unrelated profile, a red line, not inefficiency).
- **Abandoned subgoal**: in the plan, never executed; "forgot the goal" lives here (references/plans-and-cost.md; three things asked, two answered, the one with a deadline dropped).
- **Order inversion**: execute first, verify after (references/plans-and-cost.md).

**Family 3, state and collaboration failures.** Crosses sessions or agent boundaries; attribution traces the write chain or the handoff chain.

- **Miswrite**: memory content does not match the facts and contaminates every later reader; trace to the first bad write (references/memory.md; day one's wrong note contaminating every later conclusion of a multi-day investigation).
- **Forgetting**: should have written or read and did not; sev-3 by default, escalated by consequence for time-sensitive matters (references/memory.md).
- **Crosstalk**: reading A's history onto B; the identity-verification policy row, sev-1 (references/memory.md; two customers one letter apart, order history attached to the wrong person).
- **Contaminated memory entry**: external content written to long-term memory without isolation, turning a one-off injection into a resident backdoor (references/memory.md × references/adversarial.md).
- **Handoff context loss**: the handed-over task drops a key intent or constraint; each agent error-free, the system fails (references/multi-agent.md; "check the shipment status" passed without the address-change intent and its 24-hour window).
- **Reviewer collusion**: the reviewing agent approves on the upstream summary alone; a review that passes with zero autonomous tool calls in the nested trace is a violation (references/multi-agent.md; a custom-made item mis-summarized as standard and approved as written).

**Family 4, adversarial failures.** One question decides: whose will is this behavior? Injection is the vehicle; the other four are ends; real attacks combine.

- **Injection**: instructions inside external content obeyed as instructions rather than handled as data (references/adversarial.md; a forged policy page reaching a report's conclusion while `citation_resolves` stays green; a citation that resolves ≠ a source to trust).
- **Tool misuse**: a legitimate tool, a call that "succeeds", a hijacked intent (references/adversarial.md; `send_email` to an attacker-chosen address).
- **Privilege escalation**: induced into an action beyond the action boundary (references/adversarial.md; a forged customer email walking the agent to the door of `refund`, stopped by the permission matrix, a hard boundary, not insight).
- **Data exfiltration**: protected data induced into an unverified recipient's hands (references/adversarial.md; non-adversarial twin in family 1).
- **Autonomy boundary**: task scope widened by external content; every step legitimate, the scope crosses the line (references/adversarial.md).

## External mappings

- OWASP LLM Top 10 ↔ family 4, category by category (mapping table in references/adversarial.md).
- MAST (multi-agent failure taxonomy) ↔ the collaboration entries of family 3 (see references/multi-agent.md).
- Use both as discipline 1 says: to find gaps, not to fill a form; an external taxonomy tells you what the industry has seen, it does not name your traces.

## Self-check

- The sentence: "We adopted the taxonomy, so our atlas is complete."
- The reality: an atlas row without a count and a sev distribution is a vocabulary entry, and a borrowed name hides the mode your traces actually show.
- The check: for each atlas row, point at the representative trace IDs and the count; for each family, name the sampling that could have surfaced it.

## Templates

- `templates/failure-mode-atlas.md` — the six-column living atlas this taxonomy is checked against.
- `templates/trace-review.md` — the coding form that produces the clusters before comparison.
- `templates/redline-set.md` — where every applicable sev-1 entry becomes a case.

## Migration notes

- Coding agents: wrong tool / wrong parameters map to shell and git misuse; orphan step = an edit outside the task's files (a red line when it touches secrets or CI); handoff context loss = a planner dropping the acceptance criterion; privilege escalation = a destructive command induced by repository content.
- Research agents: hearsay taken as fact and injection dominate; fabricated identifier = a citation that does not exist; retrieval waste is the cost signature.
- Professional-judgment agents: unauthorized commitment = advice beyond scope of practice; outbound to an unverified recipient = privilege waiver; every family-4 entry sits at the intersection of irreversible action and protected data.
- Platforms: family 3 entries need the nested trace and the memory write chain in the schema before they can be coded at all.
