# Side-Effect Audit Table (Chapter 8)

> Notes: the three typical side effects of write tools × three detection methods. Once the verdict methods are in place, register every finding from every run in the last column — every "change not declared as expected" on a diff list lands here.

## Side effect × detection method

| Side effect | Definition | Assertion | Diff | Probe |
|---|---|---|---|---|
| partial write | a multi-step write breaks off halfway; the world rests in an intermediate state |  | before/after diff against the declared expectations |  |
| duplicate submission | the same action executed twice (idempotency missing, e.g. the second SH-88271 refund) | `order_state_equals`, `refund_not_executed` | one extra row in the refund ledger | setup seeds "already refunded" |
| stale read | acting on expired state (e.g. refunding again without checking the refund ledger) |  |  | two-channel timing case (ticket + next-day email) |

## Register of confirmed findings

| Date | case_id / trace_id | Side-effect type | Caught by which layer (assertion / diff / probe) | severity | Disposition |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
|  |  |  |  |  |  |
