# Cost/Latency Report Template (Chapter 9)

> Note: extension columns on the Chapter 6 report base grid. Your bill is decided by the tail; set the alarm at P95, not at the mean.
>
> **Declaration: costs are illustrative USD.**

## Cost and latency distribution (one row per task type)

| Task type | cases | runs | cost mean ± interval | cost P95 | cost max | latency mean ± interval | latency P95 |
|---|---|---|---|---|---|---|---|
| query |  |  |  |  |  |  |  |
| action |  |  |  |  |  |  |  |
| investigate |  |  |  |  |  |  |  |

## Step distribution and budgets met

Budget line anchor: `budget_steps_max` = reference steps × 2, or historical P95 plus headroom; over the line verdicts `concern` (sev-3).

| Task type | steps median | steps P95 | `budget_steps_max` met | `budget_cost_max` met |
|---|---|---|---|---|
| query |  |  |  |  |
| action |  |  |  |  |
| investigate |  |  |  |  |

## Tail list (top-3 dearest; read each trace)

| trace_id | cost | multiple of the median | where it got dear (detour / retrieval waste / re-query) |
|---|---|---|---|
|  |  |  |  |

## Configuration comparison (e.g. planner on / off)

| Configuration | Quality (pass rate ± interval) | cost median | cost P95 |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

- With multiple agents in play, the convention follows ch11: system cost = outer usage + the sum of every nested trace's usage.
