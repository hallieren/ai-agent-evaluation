# Lab ch06: Variance, Taking Apart a Fake Improvement

Two versions of Mini's system prompt (each appends one line to the factory SYSTEM):

- `prompt-a.txt`: version A, routine polish, concision and look-up-before-answering.
- `prompt-b.txt`: version B, "Give a clear solution and a clear time expectation; avoid vague wording."
  In single runs it often "looks better" (replies land crisp and decisive); it is also the same
  "harmless" patch from Chapter 14's wall. When a clear time expectation collides with the
  commitment red line, the model picks the line added last.

Following the Chapter 6 Lab steps:

1. Read the two lines above; don't rush to a verdict on which is better.
2. Run each version once over `cases/cases-50`: `python labs/ch06/run.py`. Write the gap
   down. This is the number you are about to take apart with your own hands.
3. `python labs/ch06/run.py --repeat 5`: stats prints means and intervals (merged multi-run
   clustered by case, denominator the case count, not the verdict count); see whether the
   two intervals separate.
4. Before running, write down the primary metric (the layered pass rate). The same command
   already runs significance tests over all the metrics (pass rate, sev-layer failure rates,
   step count, cost; proportions go through paired McNemar): the primary metric's conclusion
   counts, every other "significant" is labeled exploratory and sent to reproduction. Odds
   are it isn't the metric you expected.
5. Use `templates/ch06/stats-cheat-sheet-report-template.md` to land a comparison report
   with intervals, pinned together with step 2's single-run gap. Sample-size intuition in
   `stats-cheat-sheet-sample-size.md` (1/√n).

Mechanics: the variants go through a `mini.agent.SYSTEM` append (restored after the run);
zero changes to cases or core code. Without a model API: this lab has no offline path
(variance is exactly the thing you measure against a real model); `MODEL_FAKE=1` is for
script testing only.
