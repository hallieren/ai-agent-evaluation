# Release Gate

Source: repo/templates/ch14/release-gate-template.md (the repo holds the latest version; on conflict the repo wins).
Use when: defining or auditing what blocks a merge, and recording every interception the gate makes.

> Note: gate numbers and thresholds must be written down before the run, red-light actions hard-wired in advance, no one's mood in the loop. The config lives in `ci/gate`.

## Gate table (five columns)

| Metric | Criterion | Data source | Verdict source | Red-light action |
|---|---|---|---|---|
| sev-1 count | = 0 (zero tolerance, its own line, never into the average) | replay-layer sev-tiered report | assertion (sev-1 may not be gated by a judge alone) | refuse merge, return for a fix |
| cost P95 | ≤ ____ (dollars, illustrative) | stats cost distribution | deterministic | refuse merge |
| latency P95 | ≤ ____ | stats | deterministic | refuse merge |
| sev-2 failure count | ≤ ____ and not significantly worse, paired | replay + simulation layer | assertion / calibrated judge / human | refuse merge |
| case text ↔ prompt / knowledge-base near duplicates | zero hits | replay layer (zero model calls) | deterministic | intercept, reword the case or mark it contaminated |
|  |  |  |  |  |

## Replay-layer / simulation-layer trigger timing

- **Replay layer**: deterministic replay, run **on every commit** (hung on the commit hook; a red light exits non-zero). Scope: the cheapest-to-judge subset (what assertions can judge) + the red-line set. suites lists the regression set only; the capability set (`cases/capability/`) runs on every version and reports on its own line, outside the gate.
- **Simulation layer**: free simulation, run **on every version**, `--repeat` with intervals; triggered by tier-2-and-up changes (see templates/change-tiers.md).

## Interception record

| Date | Commit / change | Metric turned red | Case turned red (e.g. `no_over_limit_commitment` × angry) | Disposition |
|---|---|---|---|---|
|  |  |  |  |  |

Filled in → goes to: `ci/gate.yaml` (suites, flags, repeat, thresholds) and the interception record kept alongside it; the record feeds templates/culture-health-check.md.
