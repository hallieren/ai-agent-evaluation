# Plan Quality Rubric

Source: repo/templates/ch09/plan-quality-rubric.md (the repo holds the latest version; on conflict the repo wins).
Use when: the agent emits an explicit plan (subgoal list) before executing; score the plan itself before reading the trace.

> Note: with the planner on, judge the plan itself. Four dimensions, each with anchors;
> run the two cheap pre-checks first, and only what passes enters the rubric.

## Cheap pre-checks (deterministic, run first)

- [ ] **Plan-length comparison**: plan steps vs reference steps (over ×2 goes straight to `concern`; same source as `budget_steps_max`)
- [ ] **Unrelated-object scan**: the plan mentions an object unrelated to the task (unrelated customer, unrelated order, unrelated file) -> verdict directly, skip the rubric

## Four dimensions (1 poor / 2 middling / 3 good)

| Dimension | Definition | Anchor 3 (good) | Anchor 1 (poor) | Score |
|---|---|---|---|---|
| complete | The subgoals together cover the task, nothing dropped | Full coverage, time-sensitive items included | Drops a time-sensitive subgoal |  |
| minimal | No superfluous subgoals | Every step points at the task | Contains a "verify an unrelated customer" style step |  |
| verifiable | Every subgoal has a completion criterion | Criterion checkable (end state / source), e.g. "amount ≤ <limit> and no existing refund in the ledger" | "Understand the situation" style, never finishable and always already finished |  |
| ordered | The dependencies are right | Read before write, verify identity before sending out | Order inverted |  |

Anchor 2 (middling) for each dimension: has the shape of the criterion but no checkable object (e.g. "confirm the order qualifies" without naming what to confirm against). Fill the two ends first, then the middle, with rulings from your own traces.

## Record

| trace_id | Pre-checks | complete | minimal | verifiable | ordered | Notes |
|---|---|---|---|---|---|---|
| *example: a 3-step refund plan* | *pass* | *3* | *3* | *2* | *3* | *subgoal 2 says "confirm eligibility" without naming the ledger* |
|  |  |  |  |  |  |  |

Filled in → goes to: the verdict record's `notes` and the failure mode atlas (plan-stage rows); pre-check failures land as `concern` verdicts.
