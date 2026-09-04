# Stop Rule Decision Sheet (Chapter 14)

> Note: what stops it, to which level, and how it recovers, all written down in advance. Capability flags are the stop rule's actuators. A runbook never drilled is still literature, so drill at least one level.

## Safety branch (Chapter 12's shutdown red-line checklist folded in verbatim)

- Referenced file: `templates/ch12/shutdown-redline-checklist.md` (copied line for line, no separate standard).

## Operational branch (self-defined rows, at least one)

| Trigger | Ruling deadline | Default action |
|---|---|---|
| Production sev-1 at ≥ 1 in a single week | ruled the same day | default downgrade; burden of proof inverted, to keep running you must argue "why it may keep running" |
|  |  |  |

## The three pause levels (write a trigger and a recovery for each)

Recovery is always a rerun as a **tier-3 change** (full simulation with intervals + judge recalibration + red-line and attack sets).

| Level | Mechanism (flags are the actuator) | Trigger | Recovery |
|---|---|---|---|
| Execution to human | turn off `write_tools` (behavior should be "draft for a human," not an error) |  |  |
| Read-only downgrade | draft only, not sent out |  |  |
| Full stop | take offline |  |  |

## Drill record

| Date | Level drilled | Result (behavior as expected?) | Signature |
|---|---|---|---|
|  |  |  |  |

## Rollback runbook, four elements

- Trigger: ____  Executor (on-call has authority): ____
- Action (one command switches back): ____  Aftermath (the triggering case harvested back into the eval set): ____
