# Tool Stub Inventory

Source: repo/templates/ch07/tool-stub-inventory.md (the repo holds the latest version; on conflict the repo wins).
Use when: a stub is built or changed, after every full sandbox run, and before reading any sandbox pass rate as a promise about production.

> Notes: a stub is an assumption about the real system's behavior, and assumptions go wrong. One row per stub, fidelity gaps registered one by one. Registering a gap does not remove it, it just keeps it from hiding behind "it's probably close enough". This table gets reconciled row by row at the replay rung of the evidence ladder (confirmed / refuted / no evidence; see `templates/evidence-ladder.md`).

## Stub behavior + fidelity gap register

| Tool | Stub behavior | Real-system behavior (known/assumed) | Gap | Which verdicts it affects | Replay-rung reconciliation |
|---|---|---|---|---|---|
| *e.g. refund* | *edits the sandbox order DB; a duplicate refund quietly succeeds* | *the real gateway returns an error code on a second refund* | *stub more lenient* | *idempotency assertions (`refund_not_executed`), diffs* | *☐ confirmed ☐ refuted ☐ no evidence* |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

Direction of the gap matters: a stub stricter than the real system produces false alarms (harmless); a stub more lenient than the real system is the fatal kind.

## Self-check

- [ ] Is the "gap" column's registered count zero? Zero does not mean fidelity, it means nobody looked. Every place a stub is more lenient than the real system is a crack where offline goes all-green and production flips over.
- [ ] Every write stub has at least one registered gap with the class of verdicts it affects written down.
- [ ] Each seeded-error probe runs in both configurations: the stub returns the real system's error code, and the stub silently succeeds (`templates/side-effect-audit.md`).

Filled in → goes to: the harness spec's boundary table (`templates/harness-spec.md`) and the shadow plan's list of assumptions to reconcile against real traffic (`templates/shadow-plan.md`).
