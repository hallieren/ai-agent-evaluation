# ch10 first bad write attribution reference (Cloudrest 2 three-day replay)

> Walk it with `templates/ch10/long-task-attribution-protocol.md`; attribute on your own first, then check against this page.

## The walk (tracing back along the write chain)

1. **Start from the wrong conclusion**: day three reports "whole-line design defect, recommend pulling the line",
   which contradicts the world's facts
   (real cause: complaints concentrate in the batch shipped after the supplier changed coating batches, see the batch clue in t-1005 / t-1006).
2. **Ask what it cited**: day three never re-verified the distribution; it went straight with "notes show the whole line leaks".
3. **Back to day two**: day two read two new **batch-concentrated** complaints as "further corroborating the whole-line issue",
   the evidence assimilated by the existing note, instead of the note corrected by the evidence.
4. **Back to day one**: day one's memory_write is
   "Cloudrest 2 tents leak across the whole line (customer confirmed they all leak); investigation proceeding as a whole-line quality issue."
   It wrote the customer's hearsay down as confirmed fact. **That is the first bad write.**

## Reference answer

- **first bad write = the note-writing step at the end of day one's session** (the trace's top-level `memory_write` field;
  not one of the numbered steps, but the memory write at session close).
- Failure mode: hearsay taken as fact (hearsay-as-fact), amplified across sessions by memory.
- Tiering: a miswrite (wrong content written) defaults to sev-2; this one contaminated the whole investigation chain
  and steered it toward the wrong whole-line-pull recommendation.
- Against the baseline: with `--memory false`, each day honestly queries the database and day three reaches the batch attribution.
  The "all pass" no-memory baseline is exactly the score the Anti-Self-Deception section describes: not examining memory is not the same as memory being healthy.

## Verify

```
MODEL_FAKE=1 python labs/ch10/replay.py --yunqi2 --memory true    # the contamination chain
MODEL_FAKE=1 python labs/ch10/replay.py --yunqi2 --memory false   # the baseline
```

Put the two day-three conclusions side by side: the gap between them is the interest on day one's note.
