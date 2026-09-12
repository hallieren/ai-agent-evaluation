# Deployment Evidence Ladder

Source: repo/templates/ch13/deployment-evidence-ladder.md (the repo holds the latest version; on conflict the repo wins).
Use when: a launch or a routine release must decide which rungs to walk, what promotes it at each rung, and who signs.

> Note: a launch is not one flip, it is a climb: replay → silent/shadow → canary → full traffic. Each rung up trades for a new kind of evidence; promotion is a decision, and decisions carry names.

## Four rungs × three questions

| Rung | Newly verifies | Promotion signal | Rollback signal |
|---|---|---|---|
| Replay | Real input distribution; stub assumptions reconciled (fidelity gap register, see templates/stub-inventory.md) | Layered rates clear the gate (zero sev-1); every register row concluded; new failures harvested, fixed, rerun | (offline, fix and rerun) |
| silent/shadow | Live real-system read path; same-question comparison vs humans | Disagreement postmortems acceptable; zero red-line hits on proposed actions | Proposed action hits sev-1 |
| Canary | Real consequences and the world's reaction; write-path stub assumptions closed | Zero red lines + signals no worse than baseline + inside SLO | Any sev-1; signal breaks the band |
| Full traffic | Nothing (only scale and the long tail) | None | Same as canary, plus drift alarms |

## Action type × mandatory rungs (the four-rung rule)

- Autonomous actions whose rollback column is empty (or nominally reversible, in practice unrecoverable) → **all four rungs, shadow not skippable**
- Purely read-only, or every write in the "needs confirmation" column → shadow may fold into the canary

| Action type (from the permission matrix) | Rollback column | Mandatory rungs |
|---|---|---|
| *e.g. `refund` (autonomous under `<limit>`)* | *empty (a paid-out refund cannot be recalled)* | *all four, shadow not skippable* |
|  |  |  |
|  |  |  |

## Promotion signature line per rung

| Promotion | Date | Evidence (report link / metrics) | Signature |
|---|---|---|---|
| Replay → shadow |  |  |  |
| Shadow → canary |  |  |  |
| Canary → full traffic |  |  |  |

Filled in → goes to: the Go/No-Go review sheet (templates/go-no-go.md, section 2) and the release record for this version.
