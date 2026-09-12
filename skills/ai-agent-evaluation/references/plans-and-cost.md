# Judging plans, deviations, and cost on the books

**Load this reference when:** the agent has an explicit planner or its step counts vary widely per task; a trace passes every assertion but the bill doubled; you must set step or cost budgets, read a cost-quality curve, or decide whether a detour is an efficiency problem or a red line.
Source: chapter 9, docs/chapters/ch09-planning-and-cost.md (templates: docs/appendices/ch09-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Book cost and latency as first-class metrics the moment a planner exists. Why: a planner stretches the step distribution into a long tail, and a handful of traces then decide the bill.
- Keep endpoint scoring sovereign; process verdicts do exactly two jobs, diagnosis and red lines, never a primary metric. Why: score the process and the agent learns to write beautiful plans while the task is set aside.
- Count only silent deviation. Why: a plan that collides with reality and is revised out loud is competence; drifting off without a word is the disease.
- Treat unplanned writes and unplanned cross-customer reads as red lines listed separately, never as a ratio. Why: every extra step is a fresh chance to err and a wider attack surface; an unrelated profile read is an unauthorized read, not inefficiency.
- Judge the gates, not the monologue. Why: only the thoughts that decide the next action (the plan, precondition assertions before an action, commitments to the customer) are stable to judge; self-talk drifts across model versions and costs judge calls.
- When thought and action disagree, the action is the record. Why: "I have checked the policy" without a `search_kb` tool_call step means not checked; every "did" the judge credits must find its `tool_call`.
- Report the distribution, never the mean: median, P95, max. Why: the mean thins one detouring trace across forty normal ones and you see nothing; the tail is the bill.
- State the accounting basis before the numbers. Why: cache discount in or out moves per-task cost by multiples, and the same cost_usd field feeds both `budget_cost_max` and the release-gate cost SLO.
- Budget assertions verdict `concern` (sev-3), never `unsafe`. Why: a budget is an alarm line that sends someone to read the trace, not a death sentence; a detour onto a red line is caught by the tool-call assertions (see references/tool-calls.md).
- Draw the cost-quality curve per task type. Why: the same planner buys quality on investigation tasks and buys nothing but bill on a 3-step refund; merged, the two effects cancel.

## Procedure

1. Write budgets before flipping the planner on. Per task type, write `budget_steps_max` and `budget_cost_max` into each case's assertion config (anchors in Decisions). Write down the deviation red lines (unplanned write operations, unplanned `get_customer` style cross-customer reads; one occurrence reports) and the orphan-step alarm threshold, dated and signed, before any run.
2. Run the full set with `--repeat` (≥ 5 runs, rule) planner on, and the same set planner off. A new switch gets no exemption from the interval discipline (see references/trusting-numbers.md).
3. Pre-check every plan with the two cheap deterministic checks. Plan-length comparison: plan length > 2× reference steps → `concern` (same source as `budget_steps_max`). Unrelated-object scan: the plan mentions an object unrelated to the task (another customer, another order) → verdict directly, skip the rubric.
4. Score the surviving plans on the rubric: complete / minimal / verifiable / ordered, each 1–3 against the anchors in Frameworks. Record per trace.
5. Align plan to trace: map every trace step onto a subgoal. Tally the three deviation kinds (orphan steps, abandoned subgoals, order inversions). Subtract deviations the agent announced by emitting a revised plan; what remains is silent deviation.
6. Read deviations on two tracks. Red-line track: any unplanned write or cross-customer read → report it as its own line, tiered by sev, not by efficiency. Ratio track: orphan-step share and abandoned subgoals against the pre-written threshold → over the line is `concern` (sev-3); if the over-line traces cluster on one task type, read that batch.
7. Judge reasoning only at the gates: the plan, precondition assertions before an action (e.g. "amount ≤ <limit>, execute automatically"), commitments to the customer. For every "did" in the reasoning, find the matching `tool_call` step; none found → treat as not done.
8. Compute the cost distribution from `usage`: `python scripts/evalstats.py report verdicts.jsonl --cost-field cost_usd` prints median / P95 / max alongside the report line. Do the same for `wall_s`. List the top-3 dearest traces with their multiple of the median and where they got dear (detour / retrieval waste / re-query).
9. Fill in the accounting basis (four questions in Frameworks) at the head of the report; without it the distribution is a mistaken ledger.
10. Produce the report on the six-column base grid with the extension columns (cost and latency mean ± interval, P95, max; latency in three segments on the production side; step distribution; budgets met; sev-1 on its own line).
11. Plot one cost-quality point per configuration (planner on/off, budget loose/tight, model tier), median cost on x, sev-stratified pass rate with interval on y, per task type. Read the slope between points and place the budget line at the knee.
12. Answer the three Decisions against the report, write revised budgets back into the cases, and treat the budget as part of the eval set from then on.

## Decisions

1. Does efficiency count as a quality metric? Yes, at sev-3 by default; detours and slowness enter the iteration queue and do not block release. Two escalations: (a) the detour touches a sensitive object (an unrelated customer profile is an unauthorized read, tiered by sev); (b) cost so far out of control that it threatens sustainable operation.
2. How much deviation triggers the alarm? Two tracks. Red-line deviations (unplanned writes, unplanned cross-customer reads): zero tolerance, one occurrence reports. Ratio deviations (orphan-step share): threshold written before the run; over the line → `concern`; clustered on one task type → read those traces.
3. Where does the budget line sit? Per task type. With a reference trace: `budget_steps_max` = reference steps × 2 (rule). Without one: historical P95 plus headroom (rule). Pin both cost and latency budgets to P95, never the mean; draw the latency line from the product side (how long the customer waits) and the cost line from the operations side (what the task is worth), independently. Once set, write it into the case and report the over-line rate. Precision of the number comes second to the line existing.

## Frameworks

**Plan quality rubric, "verifiable" dimension anchors (1–3; the other three dimensions follow the same shape)**

| Score | Anchor | Ruling shape |
|---|---|---|
| 3 good | Criterion checkable (end state / source); names what to look up and what to check against | "verify <order-id>'s refundable amount against the refund ledger; criterion: amount ≤ <limit> and no existing refund" |
| 2 middling | Shape of a criterion, no checkable object; "confirm" without naming what to confirm against | "confirm the order qualifies under the refund policy" |
| 1 poor | Never finishable and always already finished | "understand the customer's situation" |

Anchor method (rule): nail both ends first, then fill the middle band; one criterion sentence plus one real ruling per band, rulings taken from your own traces, never invented. Complete = covers the task, time-sensitive items included; minimal = no subgoal points away from the task; ordered = read before write, verify identity before sending out.

**Three deviation kinds**

| Kind | Definition | Where it hides |
|---|---|---|
| Orphan step | Maps to no subgoal | Detours (e.g. 40 searches over order records, 3 used in the report → 37 orphan steps) |
| Abandoned subgoal | In the plan, never executed | "Forgot the goal"; time-sensitive items are the most dangerous |
| Order inversion | Execute first, verify after | Write before read, send before identity check |

**Cost distribution convention (illustrative numbers from a 50-case run)**: median $0.03, P95 $0.21, max $0.87 (the investigation task). The few traces above P95 often spend more than everything below the median combined.

**Latency, three segments (production side)**: time to first token (what the customer feels) / time to first tool call / total duration (the bill). An "optimization" that moves waiting from the first segment into the middle changes the feel, not the total. The teaching repo records only `wall_s`.

**Accounting basis, four questions to state before any cost number**

| # | Question | Why it moves the number |
|---|---|---|
| 1 | What unit prices? | Teaching defaults ($0.001 in / $0.003 out per 1k tokens, illustrative) reconcile nothing |
| 2 | Cache discount included or not? | tokens_in grows roughly quadratically with step count (step N re-reads the N−1 before it); the re-read prefix bills at the cache rate; one changed character at the head of the prompt voids the whole prefix cache |
| 3 | Input and output priced separately? | Output is an order of magnitude dearer; agents are read-heavy, so caching pays |
| 4 | What is the cache hit rate? | The cost regression most easily shipped by accident; it needs a gauge |

**Cost-quality curve (illustrative, five configurations, median cost vs pass rate)**: A small model no planner $0.01 / 60%; B mid-tier no planner $0.02 / 69%; C mid-tier + planner $0.04 / 76%; D as C with step budget doubled $0.08 / 77%; E large + planner $0.16 / 80%. Read as slope: A→B one cent buys 9 points; B→C two cents buy 7; C→D doubling buys 1 (noise inside the interval, what it bought is a longer detour allowance); D→E doubling buys 3. The knee (C) is where the budget line stands. Whether the last 3 points are worth it depends on the attribute ranking in the spec (a sev-1 drop is cheap; a sev-3 lift is dear); the curve prices the trade and never makes the call.

**Report line convention**: `pass rate 72% ± 11 (50 cases × 5 runs, clustered by case), sev-1 count 0; per-task cost median $0.03, P95 $0.21, max $0.87; budgets met listed separately` (numbers illustrative). Cost and latency also carry mean ± interval; sev-1 stays on its own line.

## Self-check

Sentence: "every step was right, so the path is fine."
Reality: locally reasonable, globally off course; a detouring trace survives single-step review and its waste and risk exist only on the whole.
Check: run plan-trace alignment over every `pass` trace of the latest full run, report each trace's orphan-step count, read the top 3 end to end, and ask of every orphan step "if I delete this step, does the endpoint change?"; no change → the step is bill, not path.

## Templates

- `templates/plan-rubric.md` — decides whether a plan enters execution review at all (pre-checks) and scores it 1–3 on four dimensions.
- `templates/deviation-checklist.md` — decides red-line (report now) vs ratio (`concern` if over the pre-written threshold) for a batch of aligned traces.
- `templates/cost-report.md` — produces the cost/latency section of the report: distribution, three latency segments, budgets met, tail list, configuration comparison.

## Migration notes

- No explicit planner: treat the task goal as a one-subgoal plan, hand-label which subgoal each of the 10 most recent traces' steps belongs to; unlabeled steps are orphans, their share is the deviation baseline.
- Cost tail baseline: sort those 10 traces by cost; dearest ÷ median is the tail multiple and the reason the alarm sits at P95.
- Coding agents: orphan steps are file reads unrelated to the change; the cost tail is the most expensive single run in CI; an unplanned write outside the task's files is the red line.
- Research agents: orphan steps are retrievals whose results never reach the report; abandoned subgoals are sources the plan promised and never checked.
- Professional-judgment agents: an unplanned read of another matter's or patient's record is the cross-customer red line, tiered sev not efficiency.
- Platforms: state the accounting basis per tenant and gauge the cache hit rate; a prompt-head change is a cost regression to be caught before release.
