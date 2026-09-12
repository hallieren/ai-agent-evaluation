# Silent/Shadow Plan

Source: repo/templates/ch13/silent-shadow-plan-template.md (the repo holds the latest version; on conflict the repo wins).
Use when: the agent is about to run on live traffic with output never sent, and the baseline, interception points, postmortem cadence, and exit condition must be written before it starts.

> Note: shadow = running online, producing no consequences. A shadow with no exit condition shadows forever; a shadow with no comparison is just a delayed launch.

## 1. Comparison baseline

- Compared against: ☐ human handling ☐ old version ☐ current process
- Same-question comparison method (how the entry-by-entry lineup works):

## 2. Interception point inventory (which layer stops each write)

| Write tool | Interception layer (where the action is caught) | Where the proposed action lands (log / outbox) | Red-line assertion scanned online? |
|---|---|---|---|
| *e.g. `refund`* | *stub layer, real gateway never called* | *proposed-action log* | *`refund_not_executed`, `amount_within_limit`* |
| send_email |  |  | `no_pii_disclosure` |
|  |  |  |  |

## 3. Disagreement postmortem process and cadence

- Cadence (daily / weekly): `________`  Read the top `________` disagreements each time
- Three-way call: ☐ the agent wrong ☐ human wrong (don't waste it, harvest) ☐ both right (different routes)
- Record table:

| Date | Entry | Three-way call | Disposition (harvest / fix / archive) |
|---|---|---|---|
|  |  |  |  |

## 4. Duration and exit conditions

- Planned duration: `________`  (the inference bill doubles for the whole of it)
- Exit (promotion) condition: disagreement rate stable below `________`, and the "the agent wrong" share of postmortems ≤ `________`; proposed actions hitting red-line assertions = 0
- Exit (abandon) condition: `________`
- Rollback signal: a proposed action hits a sev-1 red line (it caused nothing, but it tried)
- Honest-boundary memo: shadow cannot test the world's reaction to the agent (the customer's next line was spoken to a human); write-path stub assumptions wait for the canary to close.

Filled in → goes to: the Shadow → canary signature row of templates/evidence-ladder.md; harvested disagreements go to the eval set via templates/coverage-matrix.md.
