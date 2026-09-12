# Side-Effect Audit Table

Source: repo/templates/ch08/side-effect-audit-table.md (the repo holds the latest version; on conflict the repo wins).
Use when: designing detection for write tools, and after every run that touched a write tool (read the diff list first, the reply second).

> Notes: the three typical side effects of write tools × three detection methods. Once the verdict methods are in place, register every finding from every run in the last column. Every "change not declared as expected" on a diff list lands here.

## Side effect × detection method

| Side effect | Definition | Assertion | Diff | Probe |
|---|---|---|---|---|
| partial write | a multi-step write breaks off halfway; the world rests in an intermediate state |  | before/after diff against the declared expectations |  |
| duplicate submission | the same action executed twice (idempotency missing, e.g. a second refund on an order already refunded) | `order_state_equals`, `refund_not_executed` | one extra row in the refund ledger | setup seeds "already refunded" |
| stale read | acting on expired state (e.g. refunding again without checking the refund ledger) |  |  | two-channel timing case (ticket + next-day email) |

Division of labor: the diff catches the first occurrence you never thought of; the assertion makes sure the same mistake always has someone waiting for it.

## Register of confirmed findings

| Date | case_id / trace_id | Side-effect type | Caught by which layer (assertion / diff / probe) | severity | Disposition |
|---|---|---|---|---|---|
| *e.g. 2026-09-11* | *<case-id> / <trace-id>* | *duplicate submission* | *diff (`+ refunds` row undeclared)* | *sev-1* | *new assertion `refund_not_executed` + seeded probe added to the redline set* |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

Filled in → goes to: the failure mode atlas (`templates/failure-mode-atlas.md`, one row per confirmed side-effect type) and the redline set (`templates/redline-set.md`) for every finding that earns a standing probe.
