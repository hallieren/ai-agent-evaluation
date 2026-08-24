# Lab ch05 — The Judgment Ladder: Sink, Assign Judges, Align

Input: the `cases/cases-50` landed in Chapter 4 + the repo assertion library
(`harness/assertions.py`) + the judge harness (`harness/judge.py`) + the alignment
tool in this directory. Following the Chapter 5 Lab steps:

1. **Sink first.** Fill in the verdict configuration (`expect.assertions`) for all 50
   cases; everything that can be made deterministic, make deterministic. Investigation
   cases get mandatory citations plus `citation_resolves`. Run once and watch the ratio:
   `python -m harness.runner --cases cases/cases-50 --traces-out labs/ch05/traces.jsonl --verdicts-out labs/ch05/verdicts.jsonl`
   In the verdict records, `judged_by: assertion` marks what the bottom of the ladder caught.
2. **Assign judges.** Remaining action-case properties get `judge-tone-commitment`;
   investigation cases get `judge-report-rubric` (draft the rubric from the template in
   `templates/ch05/`). Run the judges over the existing traces:
   `python labs/ch05/run.py --traces labs/ch05/traces.jsonl`
   For calibration, have each judge blind-judge the same batch: add
   `--judge judge-tone-commitment` / `--judge judge-report-rubric`.
3. **Align.** Sample stratified by severity, blind-label by hand into a verdict-record
   JSONL (copy the format of `human-labels-sample.jsonl`, `judged_by: human`), then:
   `python labs/ch05/align.py labs/ch05/judge-verdicts.jsonl <your-human-labels.jsonl>`
   Disagreement rates come out layered by severity, one calibration report per judge
   (report template in `templates/ch05/judge-validation-report.md`).
4. **Read the disagreements.** Read each disagreeing case and look for the patterns where
   the judge deceives you: long, polite unauthorized commitments, and reports whose
   citations are complete but twist their sources.
5. **Look at the data.** The verdict records' `judged_by` now takes three values:
   `assertion` / `judge-<name>` / `human`. The judgment ladder is visible in the data.

Without a model API: `run.py` needs a model (a judge is a model call; `MODEL_FAKE=1` is
test-only); `align.py` is fully offline. Walking the format and output once with
`human-labels-sample.jsonl` works fine too.
