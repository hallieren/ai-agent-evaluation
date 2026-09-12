# Judgment Ladder Decision Tree

Source: repo/templates/ch05/judgment-ladder-decision-tree.md (the repo holds the latest version; on conflict the repo wins).
Use when: assigning a judgment instrument to a failure mode, or reviewing a case whose `expect` block leans on a judge.

> Note: pick the judgment instrument for each failure mode. The cost ladder has four rungs: assertion < deterministic check < calibrated LLM judge < human. Everything that can be made deterministic, make deterministic; a judge appears only where language alone can judge.

## Decision tree (walk it once per failure mode)

The zeroth question comes first: **did the prompt actually say it?** If not, say it, then see whether the failure is still there; one that vanishes keeps only its case, for regression, and earns no judge.

Start with the three questions:

1. **Can the sandbox answer it?** (checkable end state: order status, refund records, outbox) → **assertion** (e.g. `refund_not_executed`, `order_state_equals`, `amount_within_limit`)
2. **Can it be checked against the policy ledger / structured data?** (parameters, formats, resolvable citations) → **deterministic check** (e.g. `citation_resolves`, `budget_steps_max`)
3. **Can a conservative scan catch it?** (a text scan that prefers false alarms to misses) → still a **deterministic check** (e.g. `no_pii_disclosure`, `no_over_limit_commitment`)

Only when all three come up empty do you climb:

- Single dimension, judgeable in language → **narrow judge** (e.g. `judge-tone-commitment`)
- Overall quality, multi-dimension rubric → **rubric judge** (e.g. `judge-report-rubric`, every dimension pointing at a failure in the atlas)
- Arbitration / spot checks / gold labels → **human**

## sev-1 authority rule

- [ ] Every case with `severity_if_fail: sev-1` has at least one assertion standing guard, or enters the human spot-check list.
- [ ] **The judge can only escalate, never release.** sev-1 is never gated by a judge alone.

## Conclusion table (goes into the case's expect block)

| Failure mode | Three-question result | Instrument (assertion name / judge name / human) | sev-1 guard |
|---|---|---|---|
| *e.g. over-limit commitment in the reply* | *scan clears outright violations; gray zone remains* | *`no_over_limit_commitment` + `judge-tone-commitment`* | *`amount_within_limit`* |
|  |  |  |  |
|  |  |  |  |

Filled in → goes to: each case's `expect` block (`assertions[]`, optional `judge`) and the failure mode atlas's "judged by" note.
