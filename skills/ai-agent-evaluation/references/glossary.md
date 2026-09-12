# Using the practice's terms and record schemas exactly

**Load this reference when:** a term is ambiguous in conversation (flip vs overturn, paired vs pairwise, harness vs agent harness, the three saturations); you are writing or parsing a verdict record, case, trace, or report line; you need the canonical field names for a script or a template.
Source: appendix E, docs/appendices/appendix-e-glossary.md

- [Rules](#rules)
- [Objects and basic units](#objects-and-basic-units)
- [Verdicts](#verdicts)
- [Eval sets and infrastructure](#eval-sets-and-infrastructure)
- [Trustworthy numbers](#trustworthy-numbers)
- [Agent-specific battlegrounds](#agent-specific-battlegrounds)
- [Shipping and sustaining](#shipping-and-sustaining)
- [Record schemas](#record-schemas)
- [Self-check](#self-check)

## Rules

- Use the four verdicts and three severities by their exact names. Why: scripts, templates, and gate config key on them.
- Never confuse flip rate with overturn rate. Why: flip rate is the same case disagreeing across repeated runs; overturn rate is a human reversing the agent's conclusion or action in production.
- Never confuse paired comparison with pairwise comparison. Why: paired is old and new versions on the same cases, case by case; pairwise is a judge comparing two candidate outputs.
- Keep the three saturations apart. Why: coding saturation (no new failure modes from reading), suite aging (suite up, holdout flat, overfitting), and eval-set saturation (everything green, add harder cases) have three different prescriptions.
- Let "harness" alone mean the eval infrastructure. Why: the agent harness (scaffold) is the layer around the model and is part of the thing under test.

## Objects and basic units

- **trace (trajectory)**: the complete record of one agent run, steps alternating model turns, tool calls, and tool results, plus the final output; the basic unit of evaluation.
- **case (task / test case)**: one test, a world state (`setup`) plus a request (`prompt`) plus the expected trace properties (`expect`).
- **inbound**: the trace step type where external content (a fetched page, an incoming email body) enters the context; attack-surface inventories and injection attribution start here.
- **eval**: the systematic evaluation of an agent, the sum of cases, verdicts, and reports; the eval is the agent's spec.
- **eval-as-spec**: attribute priorities + the severity table + the action boundary form a spec that exists before the code; a new requirement first becomes a new case.
- **the three axes**: is the endpoint verifiable / is the action reversible / is there a gold answer; they decide the judgment instrument and the attribute priorities.
- **Pocket Eval**: the two-hour minimum eval: one-page boundary + worst failures + handwritten high-risk cases + the four verdicts + a continue / narrow / stop decision.

## Verdicts

- **the four verdicts (pass / concern / unsafe / unclear)**: the per-case human verdict levels; `pass` = endpoint right and path clean; `concern` = attempt, near miss, low harm; `unsafe` = red line hit; `unclear` = cannot judge (a signal the criterion is not verifiable). When real users label outputs, the fourth becomes `useless`.
- **sev-1 / sev-2 / sev-3**: irreversible harm or unauthorized action (zero tolerance, its own line, never averaged, never released by a judge alone, always guarded by an assertion or a human) / recoverable loss from wrong information (budgeted) / experience and efficiency (trend). Arbitration: can it be undone? if not, who absorbs it? no name → sev-1.
- **assertion**: an expectation for a single case that one line of code answers (e.g. `refund_not_executed`, `amount_within_limit`).
- **judge (LLM-as-judge)**: a model judging attributes only language can judge; qualified by calibration (judge-vs-human alignment); on sev-1 it may only escalate; calibration set and prompt examples must not overlap.
- **false-pass rate / false-fail rate**: the judge's two directional error rates against gold; human `unsafe`/`concern` ruled `pass` = false pass; human `pass` ruled non-pass = false fail; per-class recall = 1 − false-pass rate. Kappa is for human-vs-human only.
- **verdict sinking**: push every verdict as far down the ladder as possible; in imprisoned-data domains it is the precondition for an eval system existing.
- **the judgment ladder**: assertion < deterministic check < calibrated LLM judge < human; every verdict uses the lowest rung it can.
- **first_bad_step**: the first step that went wrong, not the worst output; a fixed field of the verdict record.
- **the failure mode atlas**: the living document of failure clusters, six columns: name / definition and criterion / representative trace IDs / count / sev distribution / suspected component.
- **near miss**: the agent headed for a red line and was stopped or stopped itself; verdict `concern`, and the attempt gets a postmortem.

## Eval sets and infrastructure

- **golden task**: a pre-designed task with an endpoint made as verifiable as possible; the basic unit of an eval set.
- **coverage matrix**: failure mode × severity × user type; an empty cell is a testing blind spot.
- **regression set**: the part of the eval set the gate reads, expected near 100%; a red light means a regression; the suites listed in `ci/gate.yaml`.
- **capability set**: cases written eval-first that the agent cannot pass yet (`cases/capability/`); run every version, reported on its own line, never blocking.
- **graduation**: a capability case moves to the regression set after passing `--repeat 5` on two consecutive versions (rule); a sev-1 case also needs a deterministic assertion first; its first-run score is recorded on graduation day.
- **reference trajectory**: the one known-passing trajectory attached to every case, run through assertions and judge rules with zero model calls to prove the task is solvable and the verdict configuration right.
- **harness**: the self-built eval infrastructure: runner, trace, assertions, judge, stats, report.
- **agent harness (scaffold)**: the loop, tool orchestration, and prompt assembly around the model; the thing under test is model + scaffold together.
- **tool stub**: a fake implementation catching calls in place of the real tool; its fidelity must itself be evaluated (fidelity gap register).
- **synthetic user**: the LLM-played counterparty; personas angry / vague / multi.
- **seeded-error probe**: a deliberately planted error to see whether the process catches it.

## Trustworthy numbers

- **pass@k / pass^k**: at least one success in k attempts / all k attempts succeed; an agent watches the latter.
- **flip rate**: the share of a case's verdicts that disagree across repeated runs; a high flip rate is a reproducibility defect of the system under test. Not the overturn rate.
- **trial**: one attempt at one case; a run is one pass over the whole set; k counts trials.
- **paired comparison**: old and new versions on the same cases, case by case (McNemar). Not pairwise comparison.
- **clustered by case**: the interval's denominator is the case count, never n × k verdicts.
- **saturation (of the eval set)**: regression and capability sets both fully pass; add harder cases. Distinct from coding saturation and suite aging.

## Agent-specific battlegrounds

- **Action Permission Matrix**: autonomous / needs-confirmation / forbidden boundary and rollback strategy per write operation; a hard boundary unrelated to the agent's judgment.
- **before/after diff**: sandbox state diffed around a run; every change is either declared as expected or it is a finding.
- **plan-trace alignment**: execution steps mapped back onto plan subgoals to quantify deviation.
- **orphan step**: a step mapping to no subgoal; the other two deviation classes are abandoned subgoal and order inversion.
- **first bad write**: the first wrong write found along the memory write chain; the anchor for long-horizon attribution.
- **handoff contract**: the context a main-agent-to-subagent handoff must carry; dropping intent or a deadline is a breach.

## Shipping and sustaining

- **evidence ladder**: replay → silent/shadow → canary → full traffic; each rung answers newly verifies / promotion signal / rollback signal.
- **silent/shadow**: output on real traffic that never takes effect, compared against the human result; mandatory in high-stakes domains.
- **overturn rate**: the share of conclusions and actions later overturned by a human (appeal reversal, rejection of a needs-confirmation action). Not the flip rate.
- **harvesting from production**: turning production traces into cases; intakes: online red-line hit, overturned item, repeat contact, drift-probe pointer.
- **drift**: input distribution, tool error rate, or escalation rate leaving its band; the response is harvesting, not rollback.
- **derail rate**: the share of replays where behavior leaves the recorded track; exceeding the change type's band means the change was tiered too low.
- **quarantine**: the isolation lane for unstable cases: flag → isolate → rule by deadline (fix the case / fix the agent / downgrade to monitoring); an alarm clock, not an exemption.
- **canary**: a small, sticky, customer-bucketed share of real traffic; an anomalous signal means rollback.
- **change tiers**: tier 1 local / tier 2 behavioral / tier 3 foundational; the tier sets the suite; a vendor model swap is tier 3.
- **stop rule**: the pre-written condition under which the agent is paused, no discussion, no iteration; safety branch = shutdown red lines, operational branch = self-defined; three pause levels.
- **failure mining**: clustering production failures into the atlas; the offline error analysis industrialized.
- **bottleneck-to-lever mapping**: eight levers (prompt, tool description, model swap, confirmation gate, handoff contract, memory policy, knowledge base, remove a component), read backwards from the failure class.
- **blameless postmortem**: the trace is the chain of evidence; the output points at equipment, not people.

## Record schemas

**Verdict record**: `{case_id, run_id, verdict, severity, failure_mode, first_bad_step, judged_by (assertion | judge-<name> | human), notes}`. In imprisoned-data domains only `verdict, severity, failure_mode` cross the boundary.

**Case**: `id, type (query | action | investigate), persona (cooperative | angry | vague | multi), prompt, setup (world state), expect {assertions[], judge?}, severity_if_fail, failure_modes[]`. A harvested case without `setup` is the most common reject.

**Trace**: `{trace_id, case_id, steps[{i, type: model | tool_call | tool_result | subagent | inbound, …}], final, usage{tokens_in, tokens_out, cost_usd, wall_s}, plan?, memory_write?}`. With subagents, system cost = outer usage + the sum of every nested trace's usage, reported as main agent / subagents / round trips.

**Report line**: `pass rate 74% ± 11 (50 cases × 5 runs, clustered by case); sev-1 count 0 (listed separately, never averaged in)` (numbers illustrative). Base grid: Metric | Mean | Interval | Cases | Runs | sev-layer counts. Produce it with `python scripts/evalstats.py report verdicts.jsonl`.

**Gate config** (`ci/gate.yaml`): `suites` (regression set only), `flags`, `repeat`, `thresholds {sev1_max: 0, sev2_max, cost_p95_max}`.

## Self-check

- The sentence: "Everyone knows what we mean by pass rate."
- The reality: without the case count, the run count, the clustering, and the sev-1 line, the same phrase means five different numbers.
- The check: every reported number carries the report line's shape, and every verdict record carries `judged_by`.
