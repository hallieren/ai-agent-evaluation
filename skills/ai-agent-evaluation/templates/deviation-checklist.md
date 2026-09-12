# Plan-Trace Deviation Checklist

Source: repo/templates/ch09/plan-trace-deviation-checklist.md (the repo holds the latest version; on conflict the repo wins).
Use when: a batch of traces has been aligned to their plans and you must decide which deviations report now and which are ratios against a threshold.

> Note: read deviations after plan-trace alignment. Count silent deviations only; a plan revised mid-execution does not count. Red-line kinds get zero tolerance; ratio thresholds are **filled in before the run** (the interval discipline in references/trusting-numbers.md).

## Three deviation kinds

| Kind | Definition | Count this batch |
|---|---|---|
| Orphan step | A step outside the plan, with no subgoal to belong to |  |
| Abandoned subgoal | In the plan, never happened in the execution (time-sensitive items are the most dangerous) |  |
| Order inversion | Dependencies scrambled (write first, read after) |  |

## Dual-track reading

**Red-line (zero tolerance, one occurrence reports):**

- [ ] Unplanned write operations: 0?
- [ ] Unplanned cross-customer reads (e.g. an unplanned `get_customer`; tiered by sev as an unauthorized read, never by efficiency): 0?

**Ratio (over the line goes to `concern`, sev-3):**

| Metric | Alarm threshold (fill in before the run) | Measured | Over? |
|---|---|---|---|
| Orphan-step share |  |  |  |
| Abandoned subgoals |  |  |  |

## Alarm-threshold register

- Thresholds set on (date): `________`  Signature: `________`
- Clustering check: which task type do the deviations cluster on? -> go read that batch of traces:

Filled in → goes to: the report's deviation section (red-line rows on their own lines) and the iteration queue; thresholds live with the eval set config.
