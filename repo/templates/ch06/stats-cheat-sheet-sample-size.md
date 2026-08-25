# Statistics Cheat Sheet · Side A: Sample-Size Quick Check (Chapter 6)

> Note: side A of a one-sheet, two-sided card. Check this side before declaring any "improvement."

## Sample-size quick check (95% interval half-width, rough cut: ≈ 1/√n)

| Gap you want to distinguish | Cases needed |
|---|---|
| ±10 percentage points | ≈ 100 cases |
| ±5 percentage points | ≈ 400 cases |

Derivation: half-width ≈ 1/√n → to distinguish a 5-point improvement, you need about 400 cases. "How big an eval set is enough": half the answer is content, the coverage matrix (ch4); half is size, here.
**n is the case count, not the verdict count**: merged multi-run clusters by case (each case first folds its k runs into one pass rate); repeated runs cannot press case-layer variance — 50 cases × 5 runs ≈ ±11, not 1/√250 ≈ ±6.

## Flip rate

- Algorithm: same case, same version, k runs; the share of cases whose verdicts disagree.
- Reading: **high** → add runs, and book the flipping as a product defect (reproducibility is one of the six attributes); **low** → add cases.

## pass@k / pass^k chooser

| Scenario | Which one | Illustration |
|---|---|---|
| Human backstop (adopted after review) | pass@k (one success in k counts) |  |
| Customer-facing autonomous execution | pass^k (all k in a row succeed) | single-run 90%, 5 in a row ≈ 0.9⁵ ≈ 59% |

## This experiment's register (fill in before the run)

- Gap to distinguish: `________` → cases needed: `________`  Actual cases: `________`  Runs: `________`
- Rejection rule (what result counts as no improvement):
