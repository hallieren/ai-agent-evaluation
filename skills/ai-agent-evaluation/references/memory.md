# Evaluating memory across sessions

**Load this reference when:** the agent reads or writes cross-session memory (or is about to); a failure cites a state produced in an earlier session; you need to tell forgetting from missed recall, place checkpoints on a long task, or decide whether "all single-session cases pass" means anything.
Source: chapter 10, docs/chapters/ch10-memory.md (templates: docs/appendices/ch10-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Change the unit of evaluation from one trace to a stretch of history the moment memory is on. Why: the harness resets before every case, so single-session eval is structurally blind to anything that happens between sessions.
- Test the write path and the read path separately, four mechanisms, four rows, never one blended pass rate. Why: four mechanisms map to four repairs (what to write / when to write / retrieval keys / recall count); blended, repair fires blind.
- Never merge the two read failures. Why: crosstalk is a safety event (someone else's information reached this person, sev-1); missed recall is a capability event (this person's own information went unused, sev-3); one point inside the same pass rate spans two severity tiers.
- After any failure you are about to file as "forgetting", query the memory store once; the entry is there → it is missed recall. Why: forgetting is fixed on the write side, missed recall on the retrieval side; the repairs point in opposite directions.
- Guard crosstalk with an assertion (`no_pii_disclosure`, fail-if-present), never a judge alone. Why: sev-1 is never released by a judge alone (see references/judging.md).
- Attribute long-task failures along the write chain to the first bad write, across traces. Why: the step-40 failure has its root at step 6 of a trace three days ago, and every step in between faithfully cited a bad state; `first_bad_step` numbering now crosses traces.
- Split consistency checking in half before any judge sees it: same fact field reconciled across sessions → assertion; semantic contradiction → judge. Why: field reconciliation covers the most valuable contradiction class in one line of code, and semantic contradiction is the judge's error-prone zone.
- Tier memory errors by consequence, not by mechanism; the report still keeps separate rows. Why: forgetting and missed recall share a tier and do not share a repair entrance.
- Treat a contaminated memory entry (external content injected into memory) as a red line of the crosstalk kind. Why: an injection written to memory is a resident backdoor that flares up in later sessions and other customers' sessions (see references/adversarial.md).

## Procedure

1. Before flipping `memory` on, put four things in place: a crosstalk case pair, a missed-recall case, at least one cross-session consistency check, a session-end write audit, plus a memory expiry policy (who changes memory when the world changes). Missing any → the switch stays off.
2. Build the crosstalk red-line pair: two deliberately near-identical entities (e.g. two customers one letter apart, order ids with swapped tail digits) in `setup`. Run A first (writes memory), then B (examines retrieval). `expect`: `no_pii_disclosure`, fail-if-present, `severity_if_fail: sev-1`.
3. Build the missed-recall case with the same shape reversed: session one plants a fact (e.g. the customer confirms a delivery-address change), session two sends a request that ought to trigger recall ("is my address updated?"). Assert the fact shows up in this turn, fail-if-absent. Deterministic either way: a visible memory-read event in the trace, or the reply's field reconciles with the planted entry.
4. Build the forgetting case: session one plants a fact the future needs, session two examines it by fact-field reconciliation (assertion). Note that auditing the store cannot show an absence; only the next session can.
5. Add the miswrite check at session end: for every new `memory_write`, ask whether it traces to a fact in this session's trace. Order numbers, amounts, statuses, addresses → deterministic reconciliation against the sandbox; summary-style notes → judge spot check.
6. Run the baseline with `memory: false` on the crosstalk pair; record the "all pass". It is failing to examine, not health; keep it only as the contrast row.
7. Flip `memory: true`, run the pair with the multi-session replayer (A then B), then the missed-recall and forgetting sequences, with `--repeat` (≥ 5 runs, rule).
8. Run the three-session consistency check: the same customer visits three times (query → execute → follow up). Verdict each session, then line up the three final replies. Extract fact fields (refund status, amount, order status, delivery address) and assert equality across sessions. Send only the remaining semantic contradictions (opposite stances with no shared field) to the judge; put those samples into the judge alignment set and read the disagreement rate for this class separately.
9. For every failure verdicted "forgetting", query the memory store for the entry; present → reclassify as missed recall.
10. For any wrong statement in a long task, run the write-chain trace: which memory entry does it cite → that entry's write point → did the information at the write point support the write? Yes → go up one more citation; no → first bad write found. Fill `first_bad_step` with session and step.
11. Site checkpoints: at every session boundary audit the day's writes before closing; before every irreversible action add the confirmation-gate item "is the memory this action relies on still fresh?". Add denser sites only where the task is long and the actions irreversible.
12. Report four rows separately (miswrite / forgetting / crosstalk / missed recall) with sev distribution per row, plus the consistency check as its own standalone row. Write the severity tiers into the spec (see references/defining-good.md).

## Decisions

1. Severity tiers for memory errors, by consequence, not mechanism:

| Mechanism | Default tier | Escalation |
|---|---|---|
| Crosstalk | sev-1, zero tolerance | Same policy line as emailing order details to an unverified contact (identity-verification line) |
| Miswrite | sev-2 | Wrong information, recoverable |
| Forgetting | sev-3 | Re-tier by the consequence it triggers (e.g. a forgotten 24-hour post-shipment intercept window) |
| Missed recall | sev-3 | Same consequence shape as forgetting; re-tier likewise |

   Tiers are tiers; the report keeps separate rows.
2. Where the checkpoints go: two default sites (session boundary audit; freshness check before an irreversible action). Anything denser is a cost question: a checkpoint prepays after-the-fact attribution as a running cost; the longer the task and the less reversible the actions, the better the deal.

## Frameworks

**Two roads to a stale copy**

| Road | Signature | Example |
|---|---|---|
| Drift | Every entry was right when written; time made it wrong | Problem resolved, memory still shows it open → superfluous apology; policy changed, memory holds the old version |
| Rot | Wrong at write time, cited as fact, written on top of | A customer's secondhand "they all leak" noted on day one; days two and three hunt for evidence that the whole line leaks |

Shared trait: the error is produced in another session and the current session merely cites it; read the failing trace alone and you see an agent faithfully using what it was handed.

**Memory eval matrix (four mechanisms)**

| Path | Mechanism | Test | Verdict means | Default sev | Direction |
|---|---|---|---|---|---|
| Write | Miswrite | Session-end audit: every write traceable to an in-session fact | Deterministic reconciliation against the sandbox + judge spot check on summaries | sev-2 | — |
| Write | Forgetting | Session one plants a fact, session two examines it | Assertion (fact-field reconciliation) | sev-3, upgraded by consequence | fail-if-absent (next session only) |
| Read | Crosstalk | Near-identical entity pair: run A (write), then B (retrieval) | `no_pii_disclosure` | sev-1 | fail-if-present |
| Read | Missed recall | Plant a known entry, construct a request that ought to trigger recall | Assertion; memory-read event visible, or reply field reconciles with the entry | sev-3, upgraded by consequence | fail-if-absent |

Disambiguation (rule): after the failure, query the store once; entry there → missed recall, not forgetting. Additional red line: the contaminated memory entry (external-content injection written into memory).

**Four mechanisms → four repairs**: miswrite → what to write; forgetting → when to write; crosstalk → how to design the retrieval keys; missed recall → how many entries to recall (and ranking).

**Three-session consistency check**: query → execute → follow up; verdict object is the relation between traces. Fact-field half (assertion): refund status, amount, order status, delivery address, unequal → fail (e.g. session three "your refund has arrived" against session one "does not qualify under the refund policy" is caught by the single field "refund status"). Semantic half (judge): opposite stances with no shared field (e.g. "we usually make an exception" vs "policy allows no exceptions"). The judge's two opposite errors: different wording read as contradiction (false alarm), same stance with swapped subject read as agreement (miss). Samples enter the judge alignment set; a sev-1 consistency failure (another customer's facts spoken aloud) → the judge only escalates, release needs an assertion or the human spot-check list.

**Write-chain attribution loop**: wrong statement → the memory entry it cites → that entry's write point → supported by the information at the write point? yes → loop; no → first bad write. Conclusion records session and step, the contamination path, and the repair pointer (memory policy / write audit / isolation).

## Self-check

Sentence: "all single-session cases pass, so multi-session is fine too."
Reality: drift, rot, the four mechanisms, and cross-session inconsistency all happen between sessions, where a reset-per-case eval never looks; the score was never tested, however high.
Check: count the cases in the eval set whose verdict needs two or more sessions; zero while the agent has memory → a stateless set is issuing a pass permit to a stateful system. Running the crosstalk pair with memory off and getting "all pass" is failing to examine.

## Templates

- `templates/memory-matrix.md` — decides test, verdict means, and sev per mechanism, and produces the four separate result rows plus the standalone consistency row.
- `templates/long-task-attribution.md` — decides where the first bad write sits and where checkpoints go.

## Migration notes

- Before any agent gets memory, four items or no switch: a crosstalk pair of similar entities, a missed-recall case, one cross-session consistency check, a session-end write audit; plus a memory expiry policy.
- Coding agents: the "similar-name customers" are files or branches with similar names; a stale note about a module's behavior after a refactor is drift.
- Research agents: the similar entities are two sources with similar titles; a secondhand claim noted as fact and cited on later days is rot, and the write-chain trace ends at the note that first recorded it.
- Professional-judgment agents: crosstalk between two clients or patients is the identity-verification red line; every irreversible action gets the "is this memory still fresh?" gate.
- Platforms: memory writes from external content sit one layer apart from the agent's own conclusions; the contaminated-entry red line runs in every tenant's set.
