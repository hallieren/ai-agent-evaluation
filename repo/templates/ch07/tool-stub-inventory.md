# Tool Stub Inventory (Chapter 7)

> Notes: a stub is an assumption about the real system's behavior, and assumptions go wrong. One row per stub, fidelity gaps registered one by one. Registering a gap does not remove it, it just keeps it from hiding behind "it's probably close enough". This table gets reconciled row by row at ch13's replay rung (confirmed / refuted / no evidence).

## Stub behavior + fidelity gap register

| Tool | Stub behavior | Real-system behavior (known/assumed) | Gap | Which verdicts it affects | ch13 reconciliation |
|---|---|---|---|---|---|
| refund | edits the sandbox order DB; a duplicate refund quietly succeeds? | does the real gateway return an error code on a second refund? |  | idempotency assertions, diffs |  |
| send_email | writes to the outbox, always succeeds | real email systems have latency and bounces |  | `no_pii_disclosure`, timeliness checks |  |
| update_order |  |  |  |  |  |
| escalate |  |  |  |  |  |

## Self-check

- [ ] Is the "gap" column's registered count zero? Zero does not mean fidelity, it means nobody looked. Every place a stub is more lenient than the real system is a crack where offline goes all-green and production flips over.
