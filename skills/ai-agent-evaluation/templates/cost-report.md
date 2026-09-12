# Cost/Latency Report Template

Source: repo/templates/ch09/cost-latency-report-template.md (the repo holds the latest version; on conflict the repo wins).
Use when: producing the cost and latency section of an eval report, or comparing configurations (planner on/off, model tier, budget).

> Note: extension columns on the six-column report base grid (see templates/stats-cheat-sheet.md). Your bill is decided by the tail; set the alarm at P95, not at the mean.
>
> **Declaration: costs are illustrative USD.** In your own system, replace this line with the accounting basis: unit prices / cache discount included? / input and output priced separately? / cache hit rate.

## Cost and latency distribution (one row per task type)

| Task type | cases | runs | cost mean ± interval | cost P95 | cost max | cache hit rate | latency mean ± interval | latency P95 |
|---|---|---|---|---|---|---|---|---|
| query |  |  |  |  |  |  |  |  |
| action |  |  |  |  |  |  |  |  |
| investigate |  |  |  |  |  |  |  |  |

## Latency in three segments (production side; the teaching repo records only wall_s)

| Task type | first token P95 | first tool call P95 | total duration P95 |
|---|---|---|---|
| query |  |  |  |
| action |  |  |  |
| investigate |  |  |  |

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
| *example: an investigation trace* | *$0.87* | *29×* | *retrieval waste, 40 searches with 3 used* |
|  |  |  |  |

## Configuration comparison (e.g. planner on / off)

| Configuration | Quality (pass rate ± interval) | cost median | cost P95 |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

- With multiple agents in play, the convention follows references/multi-agent.md: system cost = outer usage + the sum of every nested trace's usage.
- Percentiles: `python scripts/evalstats.py report verdicts.jsonl --cost-field cost_usd`.

Filled in → goes to: the eval report (cost section) and the release gate's cost / latency SLO lines (see templates/release-gate.md).
