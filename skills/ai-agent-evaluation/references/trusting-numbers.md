# Reading a number as one draw, and deciding when an improvement is real

**Load this reference when:** reporting any pass rate or proportion; comparing two versions; someone says "79% > 74%"; sizing an eval set; choosing between more runs and more cases; reading flip rates, pass@k, or pass^k; deciding whether a judge is stable enough to grade stability.
Source: chapter 6, docs/chapters/ch06-variance.md (templates: docs/appendices/ch06-templates.md)

- [Rules](#rules)
- [Procedure](#procedure): report a level · compare two versions · size the set · split the budget · split the judge's bill
- [Decisions](#decisions)
- [Frameworks](#frameworks): worked 50 × 5 example · cluster by case · tests · pass@k vs pass^k · flip rate · budget
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- A single run's number is one lottery draw, not a measurement; run the same version ≥ 5 times (rule) and never report a single-run point value. Why: non-determinism compounds along the trace; the same case flipping between `pass` and `unsafe` across runs is the normal condition.
- Randomness has two layers: the case layer (the eval set samples reality) and the run layer (each run samples the agent's behavior distribution). Why: repeated runs press only the run layer; only more cases press the case layer.
- Interval half-width ≈ 1/√n, n = case count (rule): 100 cases → ±10, 400 → ±5. Why: worst-case at 50%, an engineer's rough cut needs no package.
- Merged multi-run intervals cluster by case; the denominator is the case count, never n × k verdicts. Why: counting 250 verdicts as independent is pseudo-replication; report the interval half as wide and you will declare improvements twice as often. 250 appears in the cost ledger, never in the interval.
- Every metric enters a report as mean + interval + cases + runs + sev-layer counts. Why: the interval is the written admission of how much the number moves on its own.
- Compare versions paired on the same set, and write the rejection rule before the run. Why: pairing cancels the case layer; a threshold picked after the run can make anything "significant".
- One primary metric, or Bonferroni (α ÷ m), chosen before the run. Why: look at 10 metrics and one crosses the line on luck alone.
- sev-1 sits outside statistics: its own column, never averaged, immune to every interval discussion. Why: one wrongful refund is one incident, not "a 2% failure rate".
- A proportion with no denominator gets its denominator asked for first. Why: below three digits the reading carries ±10-plus points of built-in wobble (alignment rates, flip rates, any layered statistic).
- The judge samples too; an evaluator that cannot judge steadily has no standing to grade anyone's stability. Why: `--repeat` repeats the whole pipeline, and the judge's flips get booked to the agent.

## Procedure

### 1. Report a level

1. Run the version ≥ 5 times on the same cases: `python scripts/evalstats.py report verdicts.jsonl --repeat 5`.
2. Fold each case's k runs into one pass rate (all pass = 1.0; three of five = 0.6).
3. Take the standard deviation over the case means, divide by √(case count), multiply by 1.96: that is the clustered 95% half-width (the harness's `interval95_clustered`, ten lines).
4. Write the line: `pass rate 74% ± 11 (50 cases × 5 runs, clustered by case); sev-1 count 0 (listed separately, never averaged in)` (numbers illustrative).
5. Compute the flip rate over the same runs and read it (Frameworks). Stable failures go to the coding queue, not into the flip rate.

### 2. Compare two versions

1. Before the run, write down: the primary metric (usually the layered pass rate), the rejection rule (what result counts as no improvement), and the interval convention. Every other metric is labeled exploratory; anything "significant" there goes to reproduction, never into a conclusion.
2. Rerun the old version unchanged as a default step; set old-rerun, old-original, and new side by side.
3. Run both versions paired on the same cases, ≥ 5 runs each: `python scripts/evalstats.py compare old.jsonl new.jsonl --repeat 5`.
4. Declare improvement only if intervals separate or the paired test passes (McNemar on the flip counts). Otherwise the result is "an observation awaiting reproduction".
5. Feed the z test the case count, never the merged verdict count.

### 3. Size the eval set

1. Name the gap you need to distinguish. ±5 → about 400 cases; ±10 → about 100; a 50-case set resolves only gaps on the order of 20 points (rule): `python scripts/evalstats.py size --gap 5`.
2. Cannot afford 400: pair the comparison and add runs to press the distinguishable gap, or write down that the set answers only coarse questions until volume arrives.

### 4. Split the budget (cases × runs × cost per run)

| Observation | Where the variance is | Spend on |
|---|---|---|
| high flip rate on the same cases | run layer | runs; and book poor reproducibility as a product defect, not only a measurement problem |
| low flip rate, but the set is not trusted to represent reality | case layer | cases |
| goal is comparing two versions | | pairing plus added runs |
| goal is estimating the true level | | cases |

Illustrative account of 250 runs: 250 cases × 1 run gives a clean ±6 and no flip rate at all; 50 cases × 5 runs floats between ±6 and ±12 and lands at ±11. Repeated runs buy two things cases cannot: the flip-rate number, and evidence of the reproducibility defect. Add cases before runs; spend added runs on the subset most suspected of flipping (judge-judged cases, investigation cases, historical flippers).

### 5. Split the judge's bill

1. Freeze a batch of traces and have the judge judge them repeatedly; the traces cannot move, so every flip is the judge's.
2. Or rerun the alignment set against the same human labels at intervals; a disagreement rate that moves on its own is judge variance, not agent regression.
3. High judge flip on a property → go back to triage (rubric still vague) or sink the property to a deterministic check (`refund_not_executed` answers the same ten thousand times). See references/judging.md.

## Decisions

1. **What interval every metric reports.** Mean + interval (merged multi-run, clustered by case) + case count + run count, with sev-layer counts in their own column. Only a line like `pass rate 74% ± 11 (50 cases × 5 runs, clustered by case), sev-1 count 0` enters a report.
2. **How big an improvement earns belief.** Paired comparison, 5 runs, and separated intervals (or a passing test), all three, with the rejection rule on paper before the run. Missing any one → "an observation awaiting reproduction", not an improvement.

## Frameworks

**Worked example, 50 cases × 5 runs** (all numbers illustrative)

| Run | Passes | Pass rate |
|---|---|---|
| 1 | 37/50 | 74% |
| 2 | 35/50 | 70% |
| 3 | 38/50 | 76% |
| 4 | 36/50 | 72% |
| 5 | 39/50 | 78% |

1. Run layer: mean 74%; deviations 0, −4, +2, −2, +4; sum of squares 40; ÷ (n − 1 = 4); root ≈ 3.2 points. That is the measured "change nothing and the number moves". Fresh cases every run would predict √(0.74 × 0.26 ÷ 50) ≈ 6.2; the same cases held case difficulty fixed, hence half.
2. Case layer: single-run half-width 1/√50 ≈ ±14 rough, 1.96 × √(0.74 × 0.26 ÷ 50) ≈ ±12 proper. Even a fully deterministic agent carries this ±12 when extrapolating to the task class.
3. Merge: 185/250 = 74%; 1/√250 ≈ ±6 tempts, and assumes the same case's five runs are independent. Cluster by case instead: run-layer variance = 0.032² × 50 ≈ 0.05; total ≈ 0.74 × 0.26 ≈ 0.19; case layer ≈ 0.14, about three times the run layer; clustered standard error ≈ 5.5 points; 95% interval ≈ ±11. Five runs pressed ±12 only to ±11; the bulk of the variance is in the case layer.
4. Report line: `Pass rate 74% ± 11 (50 cases × 5 runs, clustered by case); sev-1 count 0 (listed separately, never averaged in).`

**Cluster by case, verbatim:** Each case first folds its 5 runs into one pass rate (all five pass = 1.0, three pass and two fail = 0.6); then take the standard deviation over these 50 case means and divide by √50.

**The two tests** (α = 0.05)

| Test | Use | Counts | Reading | Bias to know |
|---|---|---|---|---|
| two-proportion z | unpaired | case counts per version | \|z\| > 1.96 significant | unpaired → no pairing dividend, misses real differences (conservative); merged verdicts as denominator → underestimated SE, noise reads as difference (anti-conservative); only convention polices the denominator |
| McNemar | paired, same set | only cases that flip (A pass B fail; A fail B pass); both-pass and both-fail carry nothing | continuity-corrected χ² > 3.841 | none beyond needing pairing |

Paired bootstrap on the difference is equally legitimate; McNemar is used because it can be worked by hand. Overlapping intervals ≠ not significant: non-overlap is sufficient, not necessary; "intervals must separate" is a conservative simplification that declares fewer victories; run the test when you need the precise conclusion. Bonferroni with 10 metrics: a single metric needs p < 0.005.

**pass@k vs pass^k.** `@` = at least once (one success in k is enough); `^` = every time (like a product). pass@k fits a human backstop (candidates, retries, cheap failure); a customer-facing agent gets one draw per customer, so watch pass^k. Single-run 90% (illustrative) gives pass^5 ≈ 0.9⁵ ≈ 59% if failures behave like a coin (independent across runs) and ≈ 90% if failures sit on a fixed 10% of hard cases; the same 90% spans both, and only measurement (the flip rate) tells you which shape you have: `python scripts/evalstats.py passk verdicts.jsonl --k 5`.

**Flip rate.** Same case, same version, k runs; the share of cases whose verdicts disagree (rule: 5 runs is the minimum readable; two runs cannot separate "flips occasionally" from "flips every time", and 1 in 5 vs 4 in 5 are different diseases).

| Per-run verdicts (illustrative) | Flip? | Disposition |
|---|---|---|
| pass pass pass pass pass | no | stable |
| unsafe unsafe unsafe unsafe unsafe | no; stable fail, a hard case | not a flip; goes to the coding queue (see references/reading-traces.md) after the reference trajectory clears it |
| pass unsafe pass pass concern | yes; more than one verdict | counts toward the flip rate (e.g. 9 of 50 → 18%) |

High flip rate → failures like a coin, any mean is a report on luck. Low flip rate with fixed failers → stable mean, and every hard case is a defect to code, not noise. A frontier model failing all N runs points first at a broken task (ambiguous spec, misconfigured grader, unreachable setup) and only second at capability; check the reference trajectory first (see references/building-eval-sets.md).

**Sample size for a proportion** (rule: half-width ≈ 1/√n, n = case count)

| Gap to distinguish | Cases needed |
|---|---|
| ±10 points | ≈ 100 |
| ±5 points | ≈ 400 |
| a 50-case set | resolves gaps on the order of 20 points only |

**Report base grid** (six columns, none dropped): Metric | Mean | Interval | Cases | Runs | sev-layer counts.

## Self-check

Sentence: "79% > 74%, so the new version is better."
Reality: a version whose number moves between 73% and 79% with nothing changed has not been beaten by 79%.
Check: rerun the old version unchanged, set the three numbers side by side, and require the "improvement" to clear the old version's own swing; make the rerun a default step of every release comparison, not a matter of self-discipline.

## Templates

- `templates/stats-cheat-sheet.md`: side A fixes the gap, the case count, and the rejection rule before the run; side B is the six-column report grid and the two-version comparison table.

## Migration notes

- Coding agents: the test suite is deterministic, the agent is not; run the same task ≥ 5 times and read the flip rate before believing a pass rate; "all N runs fail" → suspect the task setup before the model.
- Research agents: citation-resolution rates and rubric-dimension rates are proportions and obey the same 1/√n; ask for the denominator.
- Professional-judgment agents: sev-1 counts stay outside every interval; expert-disagreement residue is read case by case, never averaged.
- Platforms: "experiment" defaults to a single pass; carry `--repeat` and clustered intervals over as a habit, and check what denominator the platform's interval uses.
- Alignment-layer disagreement rates (see references/judging.md) and derail rates (see references/gating-releases.md) are proportions under this same ruler.
