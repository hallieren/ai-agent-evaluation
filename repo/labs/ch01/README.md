# Lab ch01: Pocket Eval

Following the Chapter 1 Lab steps:

1. Configure the model API (repo README: `MODEL_BASE_URL` / `MODEL_NAME` / `MODEL_API_KEY`).
2. `python labs/ch01/run.py`: Mini (Lv.0, read-only) runs `cases/seed-20` one case at a time,
   printing each case's final reply and a tool-call summary; traces go to `labs/ch01/traces.jsonl`.
3. Blind-label `annotation-sheet.md` (the four verdicts: pass / concern / unsafe / unclear), then compare with `reference.md`.
4. You will most likely hit the unauthorized refund commitment on case-014 and the fabricated order ID on case-009; if you didn't, run it again.
5. Fill in the decision sheet with `templates/ch01/pocket-eval-pack.md`.

Without a model API: `run.py` exits with an error (an eval has to test the real model). `MODEL_FAKE=1` is for
scripted tests only (see `mini/llm.py`), not a substitute for this chapter's Lab. No API yet? Read the
pre-generated traces in `traces/pregen-60.jsonl` first to get a feel for the shape, then come back once you have one.
