# Lab ch02: Defining "Good", Spec Before Unlock

This chapter's Lab needs no new scripts; the viewer, t-0007, and the templates are already in the repo. Following the Chapter 2 Lab steps:

1. `python viewer/trace_viewer.py traces/examples/t-0007.jsonl`: the trace schema makes its formal entrance.
   Spend five minutes learning the fields: `steps[].type` (model / tool_call / tool_result) and `usage` (tokens, cost, elapsed time).
   The schema definition is §3 of the Lab interface contract (internal design doc).
2. In t-0007, find the step where the endpoint stayed right and the process went risky: which step called `get_customer`,
   who did it look up, and why shouldn't it have. Write down the number of the first bad step;
   Chapter 3 turns this move into a discipline (`first_bad_step`).
3. Use `templates/ch02/` to write Mini's spec, three pieces:
   - `attribute-map-worksheet.md`: the attribute ranking (start from safety > correctness > cost > latency; disagree and change it, but write down why)
   - `severity-worksheet.md`: the severity table (which sev is case-014's unauthorized commitment?)
   - `intended-use-action-boundary-sheet.md`: the action boundary
4. Go back to Chapter 1's 20 labeled cases (`labs/ch01/annotation-sheet.md`) and re-review them through the sev lens:
   any case labeled `pass` then that you want to move to `concern` now? If yes, the spec has started working.

Fully offline, no model API needed.
