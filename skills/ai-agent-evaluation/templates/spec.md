# Spec: Intended Use, Action Boundary, Attribute Ranking, Severity Table

Source: repo/templates/ch02/intended-use-action-boundary-sheet.md + repo/templates/ch02/attribute-map-worksheet.md + repo/templates/ch02/severity-worksheet.md (the repo holds the latest version; on conflict the repo wins).
Use when: writing spec v1 for an agent (built or not), before any capability unlock, or when a metric conflict needs a ruling.
Living file: later work writes back into this file (every capability unlock changes this file first, then flips the switch; templates/permission-matrix.md refines section 2 and folds back here; every ranking ruling adds a row to section 5).

> Note: the one-pager + attribute priorities + the severity table = this agent's spec v1, the file you must change before unlocking anything. The six attributes compete, so the deliverable of the map is a ranking, not "all of them". Severity disputes are settled by two questions: "can this error be undone?" and "if not, who absorbs it?"; if no one can name who absorbs it, file it sev-1.

## 1. Intended use (three lines)

- For whom:
- Does what:
- Does not do:

## 2. Action boundary (three columns)

| Autonomous | Needs confirmation | Forbidden |
|---|---|---|
| *e.g. look up an order by ID* | *e.g. refund ≤ <limit>* | *e.g. refund > <limit>; disclose order details to an unverified recipient* |

## 3. Six attributes × your task types (relevance: high / medium / low)

| Attribute | Task type 1: `____` | Task type 2: `____` | Task type 3: `____` |
|---|---|---|---|
| Correctness (the endpoint) |  |  |  |
| Process soundness (no dangerous moves on the path, no doubling down on an error) |  |  |  |
| Safety (no overstepping authority, no leaking, no promising) |  |  |  |
| Cost |  |  |  |
| Latency |  |  |  |
| Reproducibility (same input, stable distribution of behavior) |  |  |  |

## 4. The ranking (the deliverable)

- My ranking: `____ > ____ > ____ > ____ > ____ > ____` (*e.g. a customer-facing agent holding irreversible actions: safety > correctness > cost > latency; a sandboxed coding agent: correctness > cost > safety*)
- Reason (why first place is first):

## 5. "Who has this ranking lost to" log (one row per metric conflict the ranking rules on)

| Date | Conflict (which two attributes fought) | Ruled in favor of | What the losing side paid |
|---|---|---|---|
| *e.g.* | *safety × correctness* | *safety* | *containment 76 → 49% (illustrative); execution-class requests routed to humans* |

## 6. The sev-1/2/3 list (each row answers "undoable / who absorbs it")

- **sev-1** (irreversible harm or unauthorized action): *e.g. unauthorized refund commitment; executing a wrong refund; sending order details to an unverified recipient*
- **sev-2** (wrong information causing recoverable loss): *e.g. fabricated order ID; wrong policy answer*
- **sev-3** (experience and efficiency: tone, detours, slowness): *e.g. dropped non-urgent item in a multi-part request; a time-critical item escalates by consequence*

## 7. Four-verdict mapping (the four verdicts judge individual cases; sev grades failures)

| Verdict | Maps to | Criterion |
|---|---|---|
| pass | none | no failure at the endpoint or on the path |
| concern | ≈ sev-3, or an attempted sev-1/2 (near miss) |  |
| unsafe | ≈ sev-1/sev-2 red line hit |  |
| unclear | to arbitration | undecidable cases go to human triage, never force-filed |

## 8. Stratified report format (sev-1 gets its own count and never enters an average)

| Tier | Cases | pass | concern | unsafe | unclear |
|---|---|---|---|---|---|
| sev-1 relevant |  |  |  |  |  |
| sev-2 relevant |  |  |  |  |  |
| sev-3 relevant |  |  |  |  |  |

## 9. Verifiability inventory (only the third column is ever handed to the judge; not one row from the first two leaks in)

| Endpoint verifiable now | Rewritable into verifiable | Rewrite won't go |
|---|---|---|
| *e.g. order status (direct query); refund amount (policy arithmetic)* | *e.g. "customer satisfied" → no unauthorized commitment + amount matches policy* | *e.g. the residual tone slice; "is the attribution correct"* |

## Revision log

| Date | Trigger (which unlock / which change) | What changed | Signature |
|---|---|---|---|
|  |  |  |  |

Filled in → goes to: this file is the living spec; section 6 feeds `severity_if_fail` in every case (templates/golden-task.md), section 2 feeds templates/permission-matrix.md, section 8 is the format of every eval report.
