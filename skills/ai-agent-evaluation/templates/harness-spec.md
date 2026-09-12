# Harness Architecture Spec

Source: repo/templates/ch07/harness-architecture-spec.md (the repo holds the latest version; on conflict the repo wins).
Use when: building or migrating the eval infrastructure, or before unlocking any tool that needs a stub.

> Notes: before building a harness, pin down three things in writing: the component data flow, the stub/real-call boundary, and the replay/simulation layering. The six components carry no world knowledge and migrate as a whole; only world and synth get swapped.

## 1. Six-component data flow

```
case(YAML)──> runner ──> trace(JSONL)──┬──> assertions ──┐
                │  │                   │                 ├──> stats ──> report
                │  │                   └──> judge ───────┘
                │  └── synthetic users
                └───── world(sandbox + stubs)
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
| *e.g. refund* | *stub* | *irreversible, real money* |
|  |  |  |
|  |  |  |

## 3. Replay/simulation layering strategy

A large volume of **deterministic replay** as the floor (runs on every commit = the enforcement layer of the release gate, `templates/release-gate.md`); a small volume of **free simulation** as the ceiling (runs on every version, with intervals, `templates/stats-cheat-sheet.md`). Deviation from the recorded track raises an alarm, never a forced verdict; the case escalates one fidelity level.

- Replay set scope: `________`  Trigger: every commit
- Free simulation scope: `________`  Trigger: every version, `--repeat` `____` runs

Filled in → goes to: the harness's own README or config (boundary table and layering), and the spec's action boundary (`templates/spec.md`) for which tools may only ever run against a stub.
