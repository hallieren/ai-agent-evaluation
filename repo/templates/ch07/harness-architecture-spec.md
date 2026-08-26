# Harness Architecture Spec (Chapter 7)

> Notes: before building a harness, pin down three things in writing: the component data flow, the stub/real-call boundary, and the replay/simulation layering. The six components carry no world knowledge and migrate as a whole; only world and synth get swapped.

## 1. Six-component data flow

```
cases ──> runner ──> trace(JSONL, contract §3)
              │            │
   world(sandbox+stubs)  assertions ──┐
   synth(synthetic users) judge ──────┼──> stats ──> report
                                        ┘
```

| Component | Job | My counterpart |
|---|---|---|
| runner | start the agent, feed cases, manage repeat |  |
| trace | write trajectories to disk (schema per the interface contract) |  |
| assertions | deterministic verdicts |  |
| judge | calibrated LLM verdicts |  |
| stats | intervals / significance / flip rate |  |
| report | layered by sev, verdict sources visible, intervals attached |  |

## 2. Stub/real-call boundary table

Default stance: all writes stubbed, reads go to sandbox data, the model API is always called for real. Two criteria: irreversibility, real counterparty.

| Tool | Stub / real call | Reason (irreversible? real counterparty?) |
|---|---|---|
| refund | stub | irreversible, real money |
| send_email | stub (outbox, one-way in) | real counterparty |
|  |  |  |

## 3. Replay/simulation layering strategy

A large volume of **deterministic replay** as the floor (runs on every commit = the enforcement layer of the ch14 gate); a small volume of **free simulation** as the ceiling (runs on every version, with ch6 intervals).

- Replay set scope: `________`  Trigger: every commit
- Free simulation scope: `________`  Trigger: every version, `--repeat` `____` runs
