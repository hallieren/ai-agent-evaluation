# labs/ch09: Planning and Cost

Following the chapter's Lab steps:

1. **Budgets first**: read `budgets.md`, write `budget_steps_max` / `budget_cost_max`
   into `cases/cases-50` (for cases without them, `run.py` overlays the suggested defaults);
   write down the deviation red lines: unplanned write operations, unplanned `get_customer`.
2. **Flip the switch**: `python labs/ch09/run.py --repeat 5` runs the full set with
   `planner` + `write_tools` on; the interval discipline gets no exemption for a new switch.
   Traces and verdicts land in `labs/ch09/out/`.
3. **Align**: `python labs/ch09/align.py labs/ch09/out/traces.jsonl` prints each trace's
   subgoal mapping, orphan-step count, and the deviation top-3.
4. **Report**: fill `templates/ch09/cost-latency-report-template.md` with the distribution
   numbers run.py prints; for the comparison configuration run
   `python labs/ch09/run.py --repeat 5 --no-planner` (the planner on/off cost-quality points).
5. **Decide**: answer the Decision section's three questions and write the budget
   revisions back into the cases.

**No model API?** `run.py` needs a real model (set `MODEL_BASE_URL` / `MODEL_NAME`).
`align.py` is fully offline and runs on any trace JSONL; `python labs/ch09/align.py --demo`
uses `MODEL_FAKE` to reproduce the canonical 11-step refund detour (including the
unplanned `get_customer`) and aligns it on the spot, zero API.
