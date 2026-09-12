# Statistics Cheat Sheet

Source: repo/templates/ch06/stats-cheat-sheet-sample-size.md + repo/templates/ch06/stats-cheat-sheet-report-template.md (the repo holds the latest version; on conflict the repo wins).
Use when: sizing an eval set, writing a rejection rule before a comparison run, or landing any number in a report.

> Note: one sheet, two sides. Check side A before declaring any "improvement." Side B is the base grid of every eval report from here on; six columns and not one may be dropped.

## Side A: Sample-size quick check (95% interval half-width, rough cut: ≈ 1/√n)

| Gap you want to distinguish | Cases needed |
|---|---|
| ±10 percentage points | ≈ 100 cases |
| ±5 percentage points | ≈ 400 cases |

Derivation: half-width ≈ 1/√n → to distinguish a 5-point improvement, you need about 400 cases. "How big an eval set is enough": half the answer is content, the coverage matrix (`templates/coverage-matrix.md`); half is size, here.
**n is the case count, not the verdict count**: merged multi-run clusters by case (each case first folds its k runs into one pass rate); repeated runs cannot press case-layer variance. 50 cases × 5 runs ≈ ±11, not 1/√250 ≈ ±6.

### Flip rate

- Algorithm: same case, same version, k runs (5 minimum readable); the share of cases whose verdicts disagree. A stable fail is not a flip; it goes to the coding queue.
- Reading: **high** → add runs, and book the flipping as a product defect (reproducibility is one of the six attributes); **low** → add cases.

### pass@k / pass^k chooser

| Scenario | Which one | Illustration |
|---|---|---|
| Human backstop (adopted after review) | pass@k (one success in k counts) |  |
| Customer-facing autonomous execution | pass^k (all k in a row succeed) | single-run 90%, 5 in a row ≈ 0.9⁵ ≈ 59% if failures are coin-like, ≈ 90% if they sit on fixed hard cases; measure the flip rate |

### This experiment's register (fill in before the run)

- Gap to distinguish: `________` → cases needed: `________`  Actual cases: `________`  Runs: `________`
- Primary metric (exactly one): `________`  Correction for the rest: ☐ exploratory label ☐ Bonferroni α ÷ m
- Rejection rule (what result counts as no improvement):

## Side B: The always-carry-an-interval report template

### Report base grid (six columns)

| Metric | Mean | Interval | Cases | Runs | sev-layer counts |
|---|---|---|---|---|---|
| *Pass rate (example)* | *74%* | *±11 (clustered by case)* | *50* | *5* | *sev-1: 0 / sev-2: _ / sev-3: _* |
|  |  |  |  |  |  |

### Discipline

- [ ] **sev-1 counted in its own column, never averaged in**, immune to interval discussions. One is one.
- [ ] **Interval convention, merged multi-run clusters by case.** The denominator is the case count, not the verdict count (n×k as independent samples = pseudo-replication, the interval reported half as wide as it is).
- [ ] Comparing two versions: check whether the two intervals separate; no separation, no declared improvement. Paired settings use McNemar (count only the cases that flip direction).
- [ ] **Primary metric designated in advance, exactly one**; every other metric's "significant" is labeled exploratory, sent to reproduction, never into a conclusion.
- [ ] The rejection rule goes on paper before the run. The old version is rerun unchanged as a default step.

### Comparison report (two versions side by side)

| Metric | Version A (mean ± interval) | Version B (mean ± interval) | Intervals separate? | Conclusion |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |

Filled in → goes to: side A into the run's pre-registration note; side B into the eval report (the base grid of every report and of `templates/release-gate.md`).
