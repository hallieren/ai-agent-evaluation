# Taking an agent live without going blind

**Load this reference when:** offline is all green and someone says "ship it"; a launch is being planned or is already at replay / shadow / canary; production has no gold labels and you need signals; the dashboard drifted and someone wants to roll back; you need to harvest production traces into cases.
Source: chapter 13, docs/chapters/ch13-online-eval.md (templates: docs/appendices/ch13-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Treat launch as a climb, never a switch. Why: a launch has two blindnesses, **distribution blindness** (the eval set does not represent production) and **verdict blindness** (production has no gold labels), and flipping a switch leaves the eval on the offline side of both.
- Assume traffic changes because you launched. Why: people behave differently at an agent that answers in seconds than at a mailbox that answers in a day (e.g. one matter split into a string of fragments over hours), and replaying history can never test that.
- Earn every rung by answering three questions: what it newly verifies, what signal permits promotion, what signal triggers rollback. Why: a rung you cannot answer for is a rung you have not earned.
- Make real-traffic replay the minimum release gate. Why: a version that has not run on real inputs has no standing to discuss launch (see references/gating-releases.md for wiring it into CI).
- Reconcile the fidelity gap register row by row at the replay rung. Why: replay carries the real systems' behavior logs, so every stub assumption can be closed as confirmed / refuted / no evidence instead of "probably close enough".
- Write shadow's exit condition before it starts. Why: shadow doubles the inference bill before any customer value exists, and "more running can't hurt" burns money by the day.
- Never read shadow disagreement as error. Why: postmortems regularly find the human was wrong, and those entries go straight to harvesting.
- Slice the canary by customer and keep the bucket sticky. Why: slicing by message or session bounces one customer between human and agent, no overturn or repeat contact can be attributed, and every online signal is contaminated.
- Wire the gauges before the traffic. Why: a canary without gauges is streaking at a smaller scale.
- Keep the defense and the ruler separate. Why: guards inside the agent do the stopping, online assertions in monitoring ask whether the guards stopped it, and a single component doing both breaks silently.
- Treat any sev-1 online as rollback on one instance. Why: sev-1 stays singled out and never enters an average, online as well as offline.
- Respond to drift with harvesting, never rollback. Why: drift means the world changed and the agent did not, so an old version does nothing against a new world.
- Rebuild the world state when harvesting. Why: the most common harvesting reject copied the input and dropped the world state that made it fail.

## Procedure

1. **Fill the Deployment Evidence Ladder** (templates/evidence-ladder.md). For every action type in the permission matrix, read its rollback column and assign mandatory rungs per the Decisions below. Name a signer per promotion.
2. **Rung 1, replay.** Feed real inputs (historical tickets, real inbound mail, records from the period when writes were routed to humans) into the offline harness. World resets, writes hit stubs, verdicts walk the ladder. Where a human handled the same item, line the agent's proposal against the human's handling, entry by entry (the offline overturn signal).
3. **Reconcile the fidelity gap register.** For each row, open the real system's logs and rule: confirmed (close the row), refuted (fix the stub, rerun everything), no evidence (flag it, carry it to shadow and canary for focused observation). (e.g. does the real refund gateway error on a second refund of the same order while the stub quietly succeeds?)
4. **Promote from replay** only when: layered pass rate clears the gate with sev-1 = 0 (rule); every register row has a conclusion; every new failure mode replay exposed has been harvested, fixed, and rerun. Replay has no rollback; failures here are gains.
5. **Rung 2, silent/shadow.** Run the agent on live traffic with output never sent and actions intercepted before real systems (templates/shadow-plan.md: comparison baseline, interception point per write tool, disagreement postmortem cadence, planned duration, exit conditions). Compute the disagreement rate against humans; postmortem the largest disagreements as agent wrong / human wrong (harvest it) / both right by different routes. Observe the register rows flagged "no evidence" on the read path.
6. **Promote from shadow** when the disagreement rate is stable, the "agent wrong" share of postmortems is at or under the pre-written ceiling, and zero proposed actions hit a red-line assertion. Roll back on a proposed action that hits a sev-1 red line: it caused nothing, but it tried, and what it tried in shadow it will do in canary.
7. **Rung 3, canary.** Before any traffic: hash customer IDs into buckets; drill the rollback switch (minutes, one motion); wire the monitoring spec (templates/monitoring-spec.md). Let query-type and reversible-action traffic in first, irreversible actions last. Hold the criterion "no worse than the human baseline".
8. **Promote from canary** when zero online red-line hits, overturn and repeat-contact signals no worse than the human baseline, and cost and latency inside the SLO. Roll back on any single sev-1 (no statistical defense) or on the overturn or repeat-contact rate breaking its band.
9. **Rung 4, full traffic.** Expect no new evidence, only scale and the long tail. Move the eval from pre-release checkpoint to permanent instrument panel: canary signals stay on, drift probes are added.
10. **Run the three drift probes** on a schedule (input distribution, tool error rate, escalation rate). On an alarm, go to step 11, never to the rollback switch.
11. **Harvest** (four steps). Select from the four intakes by priority: online red-line hits (every one), overturned entries, traces behind repeat contacts, new input shapes the drift probes point at. Write each into a case: scrub it, rewrite into your eval world, rebuild the world state of that moment in `setup`. Fix the `expect` from the postmortem (a human states the ending it should have had; make deterministic whatever can be, see references/judging.md). File it in the coverage matrix and see which cell it lands in; expect it to land in cells once marked "can't think of a case".
12. **Rerun the offline full suite** after the first harvest round. Expect the pass rate to drop (e.g. a 91% falling after 10 harvested cases, illustrative). Do not mourn it; those points were a loan from distribution blindness. Record the new number with its interval: `python scripts/evalstats.py report verdicts.jsonl`.

## Decisions

1. **Which rungs are mandatory before launch.** The criterion is the permission matrix's rollback column, not courage.

| Action type (from the permission matrix) | Mandatory rungs |
|---|---|
| Any autonomous action whose rollback column is empty, or nominally reversible but in practice unrecoverable (e.g. `refund`, `send_email`) | All four rungs; shadow not skippable |
| Purely read-only agent, or every write in the needs-confirmation column | Shadow may fold into the canary (human confirmation is itself a layer of shadow) |
| New product with no historical traffic | Replay stands in with the hand-written eval set; shadow becomes less skippable, not more |

2. **Which online signals trigger rollback.** Two tiers, each signal with a data source and a response deadline; drill the rollback switch on a schedule.

| Tier | Members | Response |
|---|---|---|
| Immediate rollback | Any sev-1 red-line assertion hit online (exactly one member) | Single instance → roll back; no statistical defense |
| Pause promotion / shrink traffic | Overturn rate, repeat-contact rate, escalation rate, or cost P95 (the 95th of 100 traces by cost) breaking the baseline band | Hold the rung, shrink the slice, read the traces |
| (not rollback) | Drift-probe alarms | Harvest and add coverage, never the rollback switch |

3. **Canary versus A/B.** Run the canary as controlled exposure with gauges and the criterion "no worse than the human baseline"; do not run it as an A/B. Three structural reasons: you cannot afford the sample size (telling a 5-point gap apart takes ~400 cases (rule), sev-1 events count by the week, and the canary must rule quickly); the risk is asymmetric (a new system that might commit a sev-1 versus humans is not two equivalent arms, so a one-sided question gets a one-sided criterion); traffic feeds back on itself (the treatment changes the input distribution, so the identical-distribution premise fails). Once full traffic is steady with volume and a baseline, an A/B of version against version, both arms agents, earns its turn.

## Frameworks

**Evidence ladder, four rungs × three questions.**

| Rung | Newly verifies | Promotion signal | Rollback signal |
|---|---|---|---|
| Replay | Real input distribution; stub assumptions reconciled (fidelity gap register) | Layered rates clear the gate (sev-1 = 0); every register row concluded; new failures harvested, fixed, rerun | (offline: fix and rerun) |
| Silent/shadow | Live real-system read path (stale reads become testable); same-question comparison vs humans | Disagreement postmortems acceptable; zero red-line hits on proposed actions | Proposed action hits sev-1 |
| Canary | Real consequences and the world's reaction; write-path stub assumptions closed | Zero red lines + signals no worse than baseline + inside SLO | Any sev-1; a signal breaks the band |
| Full traffic | Nothing (only scale and the long tail) | None | Same as canary, plus drift alarms |

Shadow's honest boundary: it cannot test the world's reaction to the agent (the customer's next line was spoken to a human), it cannot close write-path stub assumptions, and it cannot see behaviors that only appear in front of an agent.

**Canary controls, three.** (1) Slice by task type, not percentage: query-type first, action-type later; reversible actions first, irreversible last. (2) Rollback switch one motion away, minutes, drilled on a schedule; an undrilled plan is no plan. (3) Monitoring wired before traffic. Bucketing: hash the customer ID, whole person stays in the bucket, no mid-session handoff, still there next visit. One one-way exception: the agent bucket may be cut back to humans, whole bucket, any time; moving human-bucket customers to the agent mid-stream is never allowed.

**Four signal classes that need no gold label, descending trustworthiness.**

| Class | Signal | Data source | Reading |
|---|---|---|---|
| 1 | Deterministic red-line assertions run online (`no_pii_disclosure` on every outbound message, `amount_within_limit` on every `refund` argument, `no_over_limit_commitment` on every reply) | Production traces / outbound content | Zero hits; a single instance trips; no band |
| 2 | Escalation rate | Human-handoff records | No correct value, only baseline and band; a spike = new inputs it cannot handle; a dip is more suspicious (the world did not get simpler, it started bluffing) |
| 3 | Customer repeat-contact rate (same customer, same matter, short window) | Session records; the human-support era is the ready-made baseline | The customer is labeling for you; the label is "dissatisfied" |
| 4 | Overturn-type signals: human reversal after appeal; human rejection rate on needs-confirmation actions (the permission matrix produces it for free); shadow disagreement postmortems | Human ruling records | The closest thing production has to a gold label |

Judge online: sample only; its calibration was done on the offline distribution and expires under drift (recalibration discipline in references/gating-releases.md). Correct its reported pass rate before reading it (Rogan–Gladen): true pass rate ≈ (observed pass rate + TNR − 1) ÷ (TPR + TNR − 1), TPR = 1 − false-fail rate, TNR = 1 − false-pass rate, clipped to [0, 1]. A lenient judge reports high, a strict one low; the correction cannot narrow the interval, and the worse the judge, the wider it gets.

**Monitoring signal spec, five columns.** Signal / data source / baseline / band / trigger action. A signal without a baseline is a number; a signal without a trigger action is decoration. Cost and latency stay first-class; add a row for the prompt cache hit rate (data source: API usage; below the band → inspect the head of the prompt; the cost regression most easily shipped by accident). Cost basis with subagents: system cost = outer usage + the sum of every nested trace's usage, reported in three columns, main agent / subagents / round trips.

**Drift probes, three.** Input distribution (task-type mix, approximate persona mix, topic words; a new product category, policy, or campaign shoves inputs off the eval set). Tool error rate (real error codes, first seen here; when it climbs, the error-recovery dimension is under test and your recovery cases are still written to the stubs' script). Escalation rate (a slow climb is input drift's earliest symptom; new inputs become pleas for help first, failures second). Drift does not trigger rollback; it triggers harvesting.

**Verification lag substitutes** (when errors surface late, e.g. a waved-through contract clause exploding months later): periodic expert spot checks as proxy labels; assertion-type leading indicators computable on the spot (citation resolves, conclusion does not overreach authority); stretch each rung's dwell time to match the lag and swap promotion signals from outcome metrics to leading indicators + spot checks.

## Self-check

- The sentence: "91% offline, time for full traffic."
- The reality: offline pass rate measures the world you could think of; the wreck happens in the part you could not.
- The check (five minutes, three questions): ① red-line assertion hits on production traffic in the last 24 hours (no answer = no online eval, only offline memories); ② date of the last reconciliation of the production input distribution against the offline set; ③ date the most recent harvested case entered the eval set (no answer = the eval set is expiring, and the score was its score when fresh).

## Templates

- `templates/evidence-ladder.md` — which rungs this launch must walk, and who signs each promotion.
- `templates/shadow-plan.md` — shadow's baseline, interception points, postmortem cadence, and exit condition.
- `templates/monitoring-spec.md` — every online signal's baseline, band, and trigger action, plus cost basis and drift probes.

## Migration notes

- Coding agents: replay = rerun on real issue history; shadow = the agent's PRs get reviewed but never merged, compared against the human fix; canary = low-risk repositories first; overturn signal = review rejection rate and revert rate.
- Research agents: shadow = the report runs alongside the human conclusion and never ships; repeat contact becomes "corrected after publication".
- Professional-judgment agents (clinical, legal, finance): the rollback column is empty top to bottom, so shadow is mandatory and often regulator-required; canary slicing is an ethics decision ("which patients get the algorithm") and each rung's evidence is archived for the regulator; verification lag is the norm, so use the three substitutes above.
- Platforms: shadow's comparison baseline may be the old version rather than humans; the bucketing unit is whatever the counterparty is (customer, repo, account), never the message.
- Any agent: the assertions that depend on no single case's expectation move into production as is; they are your first online gauge.
