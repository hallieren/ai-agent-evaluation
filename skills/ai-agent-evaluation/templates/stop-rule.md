# Stop Rule Decision Sheet

Source: repo/templates/ch14/stop-rule-decision-sheet.md (the repo holds the latest version; on conflict the repo wins).
Use when: writing down in advance what pauses the agent, to which level, who executes rollback, and how it recovers.

> Note: what stops it, to which level, and how it recovers, all written down in advance. Capability flags are the stop rule's actuators. A runbook never drilled is still literature, so drill at least one level.

Living file: later work writes back into this file (new shutdown red lines from breaching attack samples, new operational rows from production sev-1s, every drill and every rollback).

## Safety branch (the shutdown red-line checklist folded in verbatim)

- Referenced file: `templates/shutdown-checklist.md` (copied line for line, no separate standard). Any single red line on it → stop, no discussion, no iteration.

## Operational branch (self-defined rows, at least one)

| Trigger | Ruling deadline | Default action |
|---|---|---|
| Production sev-1 at ≥ 1 in a single week (illustrative) | ruled the same day | default downgrade; burden of proof inverted, to keep running you must argue "why it may keep running" |
| *e.g. escalation rate or tool error rate crossing its band for `<n>` consecutive days* | *same day* | *pause promotion, shrink traffic, harvest* |
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

Filled in → goes to: the on-call runbook; triggering cases go to the eval set; drills and rollbacks are written back into this file.
