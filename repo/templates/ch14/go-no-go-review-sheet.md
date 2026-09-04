# Go/No-Go Review One-Pager (Chapter 14)

> Note: a one-page decision artifact for the VP / PM / legal, an audience that does not read traces, it reads this page. Every column references an existing artifact (gate table / ladder / register), no new numbers invented; a blank signature column means the page is not finished.

## Version and occasion

| Item | Value |
|---|---|
| Version / change |  |
| Change tier (Table 14-1) | tier 1 / tier 2 / tier 3 |
| Review date / attendees |  |

## 1. Metric row (Chapter 6 base grid, sev-tiered)

| Metric | Mean | Interval | Cases | Runs | sev-tiered count |
|---|---|---|---|---|---|
| Pass rate (offline full set) |  | ±____ (clustered by case) |  |  | sev-1: 0 / sev-2: _ / sev-3: _ |
| Cost P95 / latency P95 |  |  |  |  |  |

- [ ] sev-1 = 0. Nonzero, no meeting needed, zero tolerance does not enter the review, it simply does not release.

## 2. Evidence Ladder position (Chapter 13)

| Item | Value |
|---|---|
| Current rung | replay / shadow / canary / full traffic |
| What this rung newly verified |  |
| Promotion signal (the one written in advance) | met / not met: ____ |
| Rollback switch, last drill date |  |

## 3. Open reconciliation items

| Item | Status | Owner | Deadline |
|---|---|---|---|
| Unclosed rows in the fidelity register |  |  |  |
| Flaky quarantine list (count / share) |  |  |  |
| Other (judge calibration expired, label relabeling ...) |  |  |  |

## 4. Residual risk and its owner (the heart of this page)

| Residual risk (specific to a failure mode) | Worst outcome (sev) | Mitigation / monitoring | Risk-owner signature |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

- Rule: every row must be signed by a specific person. A row that can't be signed is the evidence it shouldn't ship yet.

## 5. Decision and signature

| Item | Value |
|---|---|
| Decision (one of three) | continue (promote as planned) / narrow (shrink traffic, turn off a capability, downgrade) / stop (roll back or don't ship) |
| Criterion pointed back to | gate-table row / ladder promotion signal / stop-rule item: ____ |
| Decision-maker signature / date |  |

> Room discipline: a deadline is not a criterion, criteria come from only three places, the gate table, the ladder promotion signal, and the stop rule. When a deadline overrides the evidence, section 4 turns "who carries the residual risk" into a signing act.
