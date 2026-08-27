# Action Permission Matrix (Chapter 8)

> Notes: build rows on tool × condition (not one row per tool name), check one of the three columns, fill in the guard, answer both questions. **Once filled in, this merges into the Chapter 2 spec and is part of the spec from then on**; before unlocking any write tool, change this first.

## Permission matrix

| Tool | Condition | Autonomous | Needs confirmation | Forbidden | Guard (assertion / diff / gate) |
|---|---|---|---|---|---|
| escalate | always | ✅ |  |  | none |
| refund | amount ≤ $500 and order not refunded |  |  |  | `amount_within_limit`, diff |
| refund | order already refunded |  |  | ✅ | `refund_not_executed` (seeded probe) |
| update_order | after shipment (via Swiftlink interception) |  | ✅ |  |  |
| send_email | recipient not verified through the order binding |  |  |  | `no_pii_disclosure` |
|  |  |  |  |  |  |

## The two confirmation-and-rollback questions (answer per write tool)

| Tool | Who confirms? (no answer = no unlock) | How does it roll back? (nominally undoable ≠ actually recoverable) |
|---|---|---|
| refund |  |  |
| send_email |  | a sent email cannot be recalled → intercept up front |
| update_order |  |  |
| escalate |  |  |

## Differ semantics

Every sandbox before/after change is either declared as expected, or it is a finding.
