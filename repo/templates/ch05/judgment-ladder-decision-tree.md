# Judgment Ladder Decision Tree (Chapter 5)

> Note: pick the judgment instrument for each failure mode. The cost ladder has four rungs: assertion < deterministic check < calibrated LLM judge < human. Everything that can be made deterministic, make deterministic; a judge appears only where language alone can judge.

## Decision tree (walk it once per failure mode)

Start with the three questions:

1. **Can the sandbox answer it?** (checkable end state: order status, refund records, outbox) → **assertion** (e.g. `refund_not_executed`, `order_state_equals`, `amount_within_limit`)
2. **Can it be checked against the policy ledger / structured data?** (parameters, formats, resolvable citations) → **deterministic check** (e.g. `citation_resolves`, `budget_steps_max`)
3. **Can a conservative scan catch it?** (a text scan that prefers false alarms to misses) → still a deterministic check (e.g. `no_pii_disclosure`, `no_over_limit_commitment`)

Only when all three come up empty do you climb:

- Single dimension, judgeable in language → **narrow judge** (`judge-tone-commitment`)
- Overall quality, multi-dimension rubric → **rubric judge** (`judge-report-rubric`, every dimension pointing at a failure in the atlas)
- Arbitration / spot checks / gold labels → **human**

## sev-1 authority rule

- [ ] Every case with `severity_if_fail: sev-1` has at least one assertion standing guard, or enters the human spot-check list.
- [ ] **The judge can only escalate, never release.** sev-1 is never gated by a judge alone.

## Conclusion table (goes into the case's expect block)

| Failure mode | Three-question result | Instrument (assertion name / judge name / human) | sev-1 guard |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |
