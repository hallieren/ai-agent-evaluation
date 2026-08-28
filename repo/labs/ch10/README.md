# labs/ch10: Memory

Follow the chapter's Lab steps:

1. **Eval first**: add assertions to `cases/redline/redline-11.yaml` (Jamie Carter SH-90312) and
   `redline-12.yaml` (Jaime Carter SH-90321); the blank expect is deliberate (hint: `no_pii_disclosure` is waiting).
   Three-session consistency check: use `--sessions` to line up your own case sequence (query → execute → follow up) and define which statements get reconciled together.
2. **Baseline**: `python labs/ch10/replay.py --pair --memory false`. Without memory, Mini honestly
   queries the database every time and crosstalk cannot be examined out; write down this "all pass".
3. **Flip the switch**: `python labs/ch10/replay.py --pair --memory true`. Jamie Carter's session runs
   first (writes memory), then Jaime Carter's (examines retrieval); watch whose order sneaks into the second session's reply.
4. **The long task**: `python labs/ch10/replay.py --yunqi2 --memory true` runs the Cloudrest 2 three-day
   script (the script lives in `script-yunqi2.py`). Execute the Long-Task Attribution Protocol on the wrong conclusion
   (`templates/ch10/long-task-attribution-protocol.md`), tracing the write chain to the first bad write;
   reference answer: `attribution.md` (verify it lands on day one).
5. **Produce**: the Memory Eval Matrix results (`templates/ch10/memory-eval-matrix.md`), miswrite / forgetting / crosstalk / missed recall in separate rows, never merged.

Replayer mechanics: at the end of each session, the trace's `memory_write` is appended into the next
session's `memory_notes` (mini/agent.py's memory channel); `--memory false` carries nothing.

**No model API?** Under `MODEL_FAKE=1`, `--pair` and `--yunqi2` run fully offline (built-in scripts feed the lines,
one script set for memory on and one for off); `--sessions` with an arbitrary sequence needs a real model (`MODEL_BASE_URL` / `MODEL_NAME`).

**Real-model behavior is probabilistic, and that is itself one of this chapter's lessons**: whether memory
contamination (crosstalk, hearsay taken as fact) happens depends on your model's judgment on the day. In real runs,
flash sometimes prudently questioned the "they all leak" hearsay and nothing got contaminated; sometimes it did.
So the offline `MODEL_FAKE --yunqi2` uses a fixed script to **guarantee** the canonical contamination reproduces
(for teaching and regression), while a real-model run answers "will your agent actually do this". One clean run does
not mean safe; memory errors are low-frequency, high-risk, and it takes repeated runs (Chapter 6) to force them out.
That is exactly why `--pair`/`--yunqi2` deserve repeated runs with the stats stratified by severity.
