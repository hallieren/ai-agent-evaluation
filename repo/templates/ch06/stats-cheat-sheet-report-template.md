# Statistics Cheat Sheet · Side B: The Always-Carry-an-Interval Report Template (Chapter 6)

> Note: side B of a one-sheet, two-sided card. From this chapter on, this is the base grid of every eval report in the book. Six columns and not one may be dropped.

## Report base grid (six columns)

| Metric | Mean | Interval | Cases | Runs | sev-layer counts |
|---|---|---|---|---|---|
| Pass rate (example) | 74% | ±11 (clustered by case) | 50 | 5 | sev-1: 0 / sev-2: _ / sev-3: _ |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## Discipline

- [ ] **sev-1 counted in its own column, never averaged in**, immune to interval discussions. One is one.
- [ ] **Interval convention, merged multi-run clusters by case.** The denominator is the case count, not the verdict count (n×k as independent samples = pseudo-replication, the interval reported half as wide as it is).
- [ ] Comparing two versions: check whether the two intervals separate; no separation, no declared improvement. Paired settings use McNemar (count only the cases that flip direction).
- [ ] **Primary metric designated in advance, exactly one**; every other metric's "significant" is labeled exploratory, sent to reproduction, never into a conclusion.
- [ ] The rejection rule goes on paper before the run.

## Comparison report (two versions side by side)

| Metric | Version A (mean ± interval) | Version B (mean ± interval) | Intervals separate? | Conclusion |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
