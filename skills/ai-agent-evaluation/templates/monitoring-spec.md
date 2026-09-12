# Monitoring Signal Spec

Source: repo/templates/ch13/monitoring-signal-spec.md (the repo holds the latest version; on conflict the repo wins).
Use when: gauges must be wired before canary traffic, or an online signal needs a baseline, a band, and a trigger action.

> Note: online has no gold labels, so monitor only "what can be judged without a reference answer." A signal without a baseline is just a number, and a signal without a trigger action is just decoration.

## Signal table (five columns)

Pre-filled with the four no-gold-label signal classes, in descending order of trustworthiness:

| Signal | Data source | Baseline | Band | Trigger action |
|---|---|---|---|---|
| Deterministic red-line assertions run online (`no_pii_disclosure` scans outbound, `amount_within_limit` scans refund arguments, `no_over_limit_commitment` scans reply text) | Production traces / outbound content | Zero hits | No band: a single instance trips | sev-1 single instance = rollback |
| Escalation rate (spike = new inputs; a dip is more suspicious = bluffed answers) | Human-handoff records |  |  |  |
| Customer repeat-contact rate (same customer, same matter, short window) | Session records (human-support era = ready-made baseline) |  |  |  |
| Overturn-type signals (appeal reversals; human rejection rate on "needs confirmation" actions; shadow disagreement postmortems) | Human ruling records |  |  |  |
| Prompt cache hit rate (the cost regression most easily shipped by accident) | API usage |  |  | Below the band = check the head of the prompt |
|  |  |  |  |  |

## Three-column cost basis

System cost = outer usage + the sum of every nested trace's usage.

| Main agent | Subagents | Round trips |
|---|---|---|
|  |  |  |

## Three drift probes (answering "is the world still the world in the eval set")

| Probe | Watches | Response (not rollback, harvesting) |
|---|---|---|
| Input distribution | Task-type mix, approximate persona distribution, topic words |  |
| Tool error rate | Real-system error codes (examines the "error recovery" dimension) |  |
| Escalation rate (on stage again) | Slow climb = input drift's earliest symptom |  |

Filled in → goes to: the monitoring configuration read by the canary and full-traffic rungs, and the rollback-signal list in templates/stop-rule.md.
