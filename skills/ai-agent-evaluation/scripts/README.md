# Scripts

Four stdlib-only Python (3.10+) tools lifted from the book's companion harness. Each one prints `--help`, runs its own checks with `--selftest` (prints `selftest ok`), and enforces one discipline from the book. Field names follow the shared vocabulary: verdict records are `{case_id, run_id, verdict, severity, failure_mode, first_bad_step, judged_by, notes}`, cases are `{id, type, persona, prompt, setup, expect, severity_if_fail, failure_modes}`.

## evalstats.py (numbers you can trust)

`python scripts/evalstats.py report verdicts.jsonl [--sev-field severity] [--cost-field cost_usd]` reads verdict-record JSONL (`case_id`, `verdict`, optional `severity`, `judged_by`, a cost field), infers runs per case, and prints the report line `pass rate 74% ± 11 (50 cases × 5 runs, clustered by case); sev-1 count 0 (listed separately, never averaged in)`, the sev-2 / sev-3 failure counts, the `judged_by` breakdown, the flip rate (runs > 1), cost median / P95 / max when a cost field exists, and the six-column grid row. A single run uses the normal-approximation interval; a multi-run set clusters by case, denominator = case count, and says so (n × k verdicts as independent samples is pseudo-replication).
`python scripts/evalstats.py compare a.jsonl b.jsonl` pairs the two sets on `case_id` (runs folded to majority pass), runs continuity-corrected McNemar, prints A-only-pass, B-only-pass, chi2, significant yes/no, and both report lines; refuses if the case sets differ.
`python scripts/evalstats.py size --gap 5` gives the cases needed for a ±5-point 95% half-width (rough 1/√n cut and exact worst case, 400 / 385); `size --cases 50` gives the half-width for a case count. `passk --p 0.9 --k 5` prints pass@k and pass^k under independence, with the warning that the failure shape must be measured via the flip rate first.

## judge_align.py (a judge is trusted only against humans)

`python scripts/judge_align.py judge.jsonl human.jsonl [--by severity_if_fail] [--dims]`. Both files are verdict-record JSONL with at least `case_id` and `verdict`; records pair on `case_id`, and the layering key is read from the human record (`--by`, default `severity_if_fail`, falling back to `severity`, then `sev-3`). Prints the disagreement table layered by severity with every disagreeing case, the per-class recall line (`humans labeled N cases unsafe/concern, judge caught M`, the line that exposes a judge that passes everything), the false-fail line (humans pass, judge fails), an optional per-dimension breakdown when records carry `dims`, and always ends with the validity statement: the moment the judge prompt or the base model changes, this report is void.

## coverage.py (an empty cell is not a sin, an unsigned one is)

`python scripts/coverage.py cases.jsonl | cases.csv | cases_dir/ [--rows failure_modes] [--cols persona] [--sev-field severity_if_fail] [--expect-rows mode[:sev],...]`. Accepts a JSONL file, a CSV file (list cells split on `;` or `|`), or a directory of the companion repo's minimal-YAML case files. Prints the rows × columns count matrix with a sev column (persona columns always show all four of cooperative / angry / vague / multi), the empty-cell list to rule `fill` or `reasoned empty`, the sev-1 rows with their counts, `sev-1 rows all non-zero: yes/no`, and `modes in rows but zero cases: …`. The table only sees modes that have cases; pass the atlas through `--expect-rows` to make a missing row visible.

## snapshot_diff.py (every world change is declared or it is a finding)

`python scripts/snapshot_diff.py before.json after.json [--expected orders:changed refunds:added ...] [--no-fail]`. Input is two world snapshots as JSON `{table: [rows]}`; a row is keyed by `id`, else `order_id`, else the whole row. Prints the `+ added / - removed / ~ changed` list, the declarations that absorbed changes, the undeclared remainder, and `undeclared findings: N`. Exit code 1 when N > 0 unless `--no-fail`, so a second refund or a stray write fails the run whatever the reply said. `--expected` takes `TABLE:KIND` with KIND in `added | changed | removed | any`.
