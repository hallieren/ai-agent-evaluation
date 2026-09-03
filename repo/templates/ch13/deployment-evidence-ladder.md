# Deployment Evidence Ladder (Chapter 13)

> Note: a launch is not one flip, it is a climb: replay → silent/shadow → canary → full traffic. Each rung up trades for a new kind of evidence; promotion is a decision, and decisions carry names.

## Four rungs × three questions

| Rung | Newly verifies | Promotion signal | Rollback signal |
|---|---|---|---|
| Replay | Real input distribution; stub assumptions reconciled (ch7 register) | Layered rates clear the gate (zero sev-1); every register row concluded; new failures harvested, fixed, rerun | (offline, fix and rerun) |
| silent/shadow | Live real-system read path; same-question comparison vs humans | Disagreement postmortems acceptable; zero red-line hits on proposed actions | Proposed action hits sev-1 |
| Canary | Real consequences and the world's reaction; write-path stub assumptions closed | Zero red lines + signals no worse than baseline + inside SLO | Any sev-1; signal breaks the band |
| Full traffic | Nothing (only scale and the long tail) | None | Same as canary, plus drift alarms |

## Action type × mandatory rungs (the four-rung rule)

- Autonomous actions whose rollback column is empty (or nominally reversible, in practice unrecoverable) → **all four rungs, shadow not skippable**
- Purely read-only, or every write in the "needs confirmation" column → shadow may fold into the canary

| Action type (from the permission matrix) | Rollback column | Mandatory rungs |
|---|---|---|
|  |  |  |
|  |  |  |

## Promotion signature line per rung

| Promotion | Date | Evidence (report link / metrics) | Signature |
|---|---|---|---|
| Replay → shadow |  |  |  |
| Shadow → canary |  |  |  |
| Canary → full traffic |  |  |  |
