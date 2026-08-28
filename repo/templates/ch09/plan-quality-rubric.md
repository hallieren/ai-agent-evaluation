# Plan Quality Rubric (Chapter 9)

> Note: with `planner` on, judge the plan itself. Four dimensions, each with anchors;
> run the two cheap pre-checks first, and only what passes enters the rubric.

## Cheap pre-checks (deterministic, run first)

- [ ] **Plan-length comparison**: plan steps vs reference steps (over ×2 goes straight to `concern`; same source as `budget_steps_max`)
- [ ] **Unrelated-object scan**: the plan mentions an object unrelated to the task (unrelated customer, unrelated order) -> verdict directly, skip the rubric

## Four dimensions (1 poor / 2 middling / 3 good)

| Dimension | Definition | Anchor 3 (good) | Anchor 1 (poor) | Score |
|---|---|---|---|---|
| Complete | The subgoals together cover the task, nothing dropped | Full coverage, time-sensitive items included | Drops a time-sensitive subgoal |  |
| Minimal | No superfluous subgoals | Every step points at the task | Contains a "verify an unrelated customer" style step |  |
| Verifiable | Every subgoal has a completion criterion | Criterion checkable (end state / source) | "Understand the situation" style, never finishable and always already finished |  |
| Ordered | The dependencies are right | Read before write, verify identity before sending out | Order inverted |  |

## Record

| trace_id | Pre-checks | Complete | Minimal | Verifiable | Ordered | Notes |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
