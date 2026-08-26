# Lab ch07 — The Full Harness: One Command, Full Run

What this Lab produces is the battleground for every chapter that follows. Following the Chapter 7 Lab steps:

1. **Meet the world.** `world/` is the Shore & Summit sandbox — the SQLite order database seed,
   the outbox stub, reset. Run `python world/world.py` twice in a row and confirm "resettable":
   the two snapshots are identical (`labs/ch07/run.py` self-checks this again before it starts).
2. **Meet the synthetic users.** Chat one round with the angry persona by hand, playing Mini yourself;
   then open `synth/synth.py` and read the four script elements (persona / demand / held-back info /
   end condition). Do one fidelity spot-check while you are at it: does it sound like the real
   voices in the Chapter 3 traces? If not, log it in the spot-check table in
   `templates/ch07/synthetic-user-persona-library.md`
   (three known distortions: too cooperative, too dramatic, talked out of its own position).
3. **One command, full run.** `python labs/ch07/run.py` — after the reset self-check it runs the
   full set (default `cases/cases-50`, the eval set built in Chapter 4; for the red-line pack or
   the seed pack use `--cases cases/redline cases/seed-20`): angry / vague / multi cases spar
   against synthetic users, actions land in the sandbox and the outbox. The output is the book's
   first complete report: layered by sev, verdict sources visible, intervals attached.
4. **Read the report.** Skip the overall pass rate at first: first eye on the sev-1 row, second on
   the verdict-source column. Then register at least one fidelity gap each for the refund stub and
   the send_email stub: `templates/ch07/tool-stub-inventory.md`
   (this table gets reconciled row by row in ch13; registering a gap does not remove it,
   it just keeps it from hiding).
   Harness structure cross-reference: `templates/ch07/harness-architecture-spec.md`.
5. From here on, "run the eval" equals one command. When Chapter 8 unlocks `write_tools`,
   this machine is already waiting for it.

Without a model API: steps 1, 2 (reading the script), and 4 (reading the templates) work as is;
the full run needs a model (`MODEL_FAKE=1` is test-only, not an eval).
