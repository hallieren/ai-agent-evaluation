# Silent/Shadow Plan Template (Chapter 13)

> Note: shadow = running online, producing no consequences. A shadow with no exit condition shadows forever; a shadow with no comparison is just a delayed launch.

## 1. Comparison baseline

- Compared against: ☐ human handling ☐ old version ☐ current process
- Same-question comparison method (how the entry-by-entry lineup works):

## 2. Interception point inventory (which layer stops each write)

| Write tool | Interception layer (where the action is caught) | Where the proposed action lands (log / outbox) | Red-line assertion scanned online? |
|---|---|---|---|
| refund |  |  | `refund_not_executed` etc. |
| send_email |  |  | `no_pii_disclosure` |
|  |  |  |  |

## 3. Disagreement postmortem process and cadence

- Cadence (daily / weekly): `________`  Read the top `________` disagreements each time
- Three-way call: ☐ Mini wrong ☐ human wrong (don't waste it, harvest) ☐ both right (different routes)
- Record table:

| Date | Entry | Three-way call | Disposition (harvest / fix / archive) |
|---|---|---|---|
|  |  |  |  |

## 4. Duration and exit conditions

- Planned duration: `________`
- Exit (promotion) condition: disagreement rate stable below `________`, and the "Mini wrong" share of postmortems ≤ `________`; proposed actions hitting red-line assertions = 0
- Exit (abandon) condition: `________`
- Honest-boundary memo: shadow cannot test the world's reaction to the agent (the customer's next line was spoken to a human); write-path stub assumptions wait for the canary to close.
