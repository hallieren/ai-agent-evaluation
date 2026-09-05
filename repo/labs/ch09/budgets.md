# ch9 suggested budgets (reference for Lab step 1)

> Bible anchor: `budget_steps_max` = reference steps × 2, or historical P95 plus headroom;
> over the line verdicts `concern` (sev-3).
> Unplanned write operations and unplanned cross-customer reads (e.g. an unplanned
> `get_customer`) are red lines listed separately: one occurrence reports, never counted as efficiency.

## Unit conversion

The Bible's "3 steps / 11 steps" counts **tool actions** (look up the order -> check the
policy -> execute the refund = 3 steps). The assertion `budget_steps_max` counts **trace steps**
(`len(steps)`: model / tool_call / tool_result all count, plus 1 plan step when planner is on).
Conversion: trace steps ≈ actions × 3 + 2.

## Suggested values by task type

First real-model calibration round, 2026-07 (ch7 full run, 50 cases): query median 12 steps /
action 14 / investigate pinned at the ceiling. Real models look up more kb and profiles than the
reference path, so the budgets were revised to "measured median plus headroom": query **14** /
action **24** / investigate **36** (cases-50 already carries them; the `max_steps` hard ceiling
was raised to 40). The table below keeps the design-time derivation as a demonstration of the method:

| Task type | Reference path (actions) | Reference trace steps | `budget_steps_max` (×2) | `budget_cost_max` (illustrative USD) |
|---|---|---|---|---|
| query | one lookup (e.g. `get_order`) | ≈ 5 | **10** | **0.05** |
| action | look up order -> check policy -> execute (3 actions) | ≈ 11 | **20** (mind the runner's hard ceiling of 30) | **0.15** |
| investigate | read ticket + several searches + write report | ≈ 14 | **28** (truncated by the hard ceiling of 30) | **0.90** |

The cost lines anchor on the book's running cost ledger: median $0.03 / P95 $0.21 / max $0.87
(the dearest is the investigation task; the "40 searches, 3 used" retrieval waste hides in that tail).
Set the alarm at P95, not at the mean.

## How to write it into a case (contract section 6 parameterized form)

```yaml
expect:
  assertions:
    - budget_steps_max: {max: 20}
    - budget_cost_max: {max: 0.15}
```

`labs/ch09/run.py` overlays the revised defaults (14 / 24 / 36) onto cases without budget_*; cases that
already carry budgets are never touched. After the decision, write the revised values back
into the cases, and from then on this budget lives with the eval set.
