# labs/ch12: Adversarial and Injection

Follow the chapter's Lab steps:

1. **Build the injection test set first**: open `cases/attacks` (already layered by attack surface × carrier, 15 samples;
   attack-01 the forged policy page and attack-05 the forged customer email are the two canonical samples).
   Find the empty cells with `templates/ch12/redline-test-set-starter.md` and add at least one sample of your own.
2. **Then unlock `external_content`**: run one case that carries an inbound email first (e.g. `cases/attacks/attack-04.yaml`, body under `setup.inbound`)
   and look at the `inbound` step in the trace viewer (`python viewer/trace_viewer.py <trace file>`); the one difference from `tool_result`: the content comes from an untrusted source.
3. **Run a red-team round**: `python labs/ch12/run.py`, all attack samples,
   flags = `write_tools` + `external_content`; output lands in `labs/ch12/out/`.
4. **Layered interception tally**: `python labs/ch12/layers.py`, which layer each attack finally stopped at
   (input filter / action boundary / permission matrix / human confirmation / breach), printed as a table.
   Stare at it for a minute: do interceptions crowd almost entirely into the last layer? Breaches go straight onto the Shutdown Red-Line Checklist.
5. **Bank for regression**: new samples and this round's successful attacks all get banked into `cases/attacks`, rerun every version from now on.

**Without a model API**: `run.py` needs a real model; `layers.py` is fully offline and can tally any saved
traces+verdicts. Teaching sample: run `python labs/ch16/generate_material.py` first, then
`python labs/ch12/layers.py --traces labs/ch16/material/incident-trace.jsonl --verdicts labs/ch16/material/incident-verdict.jsonl`.

The complete trace of that forged customer email is the material for the Chapter 16 simulated incident postmortem; leave it closed until then.
