# Attributing failures in a multi-agent system

**Load this reference when:** the agent spawns subagents (or a second agent is about to be wired in); the end-to-end pass rate dropped after a split; a postmortem ends with "it wasn't me" from every module; you must cost a multi-agent run or choose a topology.
Source: chapter 11, docs/chapters/ch11-multi-agent.md (templates: docs/appendices/ch11-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Evaluate the system; no individual agent is the unit of evaluation once there are two. Why: the composition fallacy runs both directions, every agent right and the system wrong (a field dropped at the interface), and the system right while a subagent returned garbage the main agent happened not to use (passing by luck, with the subagent's actions and cost buried in the nested trace).
- End-to-end cases are the only evidence of system quality; single-agent verdicts are tools for attribution and regression. Why: which is criterion and which is tool must never flip, and the two-layer architecture exists to keep it from flipping.
- Always name three suspects: the main agent, the subagent, and the handoff itself. Why: the interface is natural language with no type checking and nothing errors when a field is dropped; "everyone debugs their own module" loses the third suspect every time.
- Write the handoff as a contract and check it deterministically. Why: a spawn missing required fields or a return missing confidence labels is caught without a judge.
- Never use "not found" as "does not exist", never use an inference as a fact. Why: the return's coverage and confidence labels exist so the main agent can tell them apart.
- A reviewer subagent must have an independent information source; an approval with zero tool calls in the nested trace is a violation. Why: input 100% from the party under review adds confidence and no information, and the error comes back plated "reviewed" (e.g. a custom-made item refunded on a summary that called it standard, sev-1).
- Cost the system as outer usage + the sum of every nested trace's usage. Why: counting only the outer usage underreports by the subagent share (10–24%, illustrative) and the finer the split the more leaks.
- Prefer an orchestrator over peers. Why: peer topology removes the attribution anchor and raises attribution cost by an order of magnitude, paid again on every failure.
- Race failures need repeated runs. Why: interleaving is probabilistic; one all-green run says only that this run's interleaving was safe.

## Procedure

1. Before wiring in a second agent, sign a handoff contract per interface (required fields, return fields, confidence labels), write at least 3 end-to-end cases only the system layer can judge, and give the subagent its own eval set with inputs constructed directly, never through the main agent. Missing any → not wired in (admission requirement).
2. Write the system-level case with its expected endpoint (e.g. order shipped under 24 hours ago, customer wants an address change, expected reply "the carrier can still intercept").
3. Flip `subagents` on and run the full set with `--repeat` (≥ 5 runs, rule). Nested traces sit inside `{"type": "subagent", "name": …, "trace": {…}}` steps.
4. For every system-level failure, walk the attribution procedure in fixed order:
   1. Locate at the system level: treat each nested trace as one step and find the outer `first_bad_step` (the loudest step is usually downstream; do not follow it).
   2. Boundary check: on the main agent's own model or tool_call step → Exit A, main agent. On a `subagent` step → drill down.
   3. Drill down and check the two ends: open the nested trace and repeat. A `first_bad_step` inside → Exit B, subagent. Every inside step clean → look at the spawn task description and how the return was used → Exit C, handoff. A grandchild agent inside → recurse; record the conclusion as a drill-down path (outer step → subagent step → grandchild step), not one number.
5. Record one attribution conclusion per failure: main / sub / handoff (combinations allowed), evidence steps, which layer's eval set it enters, what to fix (prompt / contract / architecture). Only Exit C fixes the contract instead of a prompt.
6. Run the two hard checks on every reviewer-type subagent: independence (count its own tool_calls in the nested trace; zero with an approval → violation) and duplicated work (what did it re-query that the main agent had already looked up and should have handed over as known facts).
7. For parallel spawns, flatten every nested trace's write `tool_call` steps onto one timeline. Same target object + two different initiators + written one after the other within one task → flag a race. Reproduce with `--repeat`; absent in one run ≠ absent.
8. Verify the fix: turn on the contract check and rerun the same case; a handoff failure should now be caught at the spawn step.
9. Cost the run in three columns, main agent / subagents / round trips, on the system basis, with mean ± interval and P95 (see references/plans-and-cost.md); add a "maximum nesting depth" column. Apply `budget_steps_max` / `budget_cost_max` on the system aggregate.
10. Do the real before/after of splitting: the same case, run with `subagents` off and on, two rows side by side, cost and capability together (turn the subagent off and its exclusive tool goes with it).
11. File each failure into the layer that owns it: handoff-class failures enter the system layer with the contract check updated in the same motion.

## Decisions

1. Write the attribution procedure into the institution: put outer `first_bad_step` → boundary check → drill down / check the two ends into the postmortem template (see templates/postmortem.md); ban "everyone debugs their own module"; every system-level failure states main / sub / handoff and the eval set it enters.
2. Two layers, two bars:

| Bar | Definition | Status |
|---|---|---|
| System bar | The spec's sev-tiered standard on end-to-end cases; sev-1 on its own line, never averaged | Sole release criterion |
| Single-agent bar | Each subagent's own eval-set pass standard + the handoff contract check | Admission requirement; no single-agent set + no signed contract → not wired in; passing every single-agent bar is no grounds for release |

## Frameworks

**Handoff contract**

| Part | Fields | Check |
|---|---|---|
| Required (at spawn) | Task goal including intent ("check shipment status" ≠ "the customer wants an address change"); constraints and time windows (e.g. the 24-hour post-shipment intercept window); known facts already looked up | Missing field → deterministic fail at the spawn step |
| Return | Conclusion; evidence (which tool call supports it); coverage (checked / not checked; "not found" ≠ "does not exist") | Missing field → deterministic fail at the return |
| Confidence labels | Every conclusion `verified / inferred / unknown` (is "arrives the day after tomorrow" the carrier system's words or the subagent's estimate?) | Missing label → deterministic fail |

**Attribution exits**

| Exit | Enters which eval set | What to fix |
|---|---|---|
| A main agent | The main agent's single-agent set | Its prompt / tool descriptions |
| B subagent | That subagent's single-agent set | Its prompt / its tools |
| C handoff | A system-level end-to-end case | The contract (required / return / confidence) or the architecture |

**Three topologies**

| Topology | New trouble | Patch |
|---|---|---|
| Parallel spawning | Races the before/after differ cannot see; a structural flip-rate source no prompt edit removes | Event-ordering check: same object, two initiators, written one after the other → flag; reproduce with `--repeat` |
| Peer collaboration | No mainline trace; attribution loses its anchor | Hunt the first bad message on a flattened timeline; make the message bus replayable first; use an orchestrator when you can |
| Recursive spawning | Drill-down deepens; each nesting layer adds two handoff ends | Write conclusions as drill-down paths; report a "maximum nesting depth" column next to the cost columns |

**Cost columns (illustrative shares from one measured run)**: main agent (in / out) / subagents (in / out) / round trips / total / cost. Subagent share 10% on a one-trip handoff case, 24% on a logistics query; round trips carry a slope (each returned conclusion is read back into context, so later rounds cost more). Never read three different cases as a controlled before/after of splitting; the only before/after is the same case with the flag off and on. Duplicated work (main agent and subagent both query the same order) is a line item the "known facts" field removes.

**MAST mapping (category level only; the atlas still grows from your own traces)**

| Concept | MAST category |
|---|---|
| Missing handoff required fields (intent and window never handed over) | Inter-agent misalignment |
| Cascade: one paraphrase from the main agent is the subagent's whole world | Inter-agent misalignment |
| Wrong-plan collusion: reviewer input 100% from the party under review | Task verification and termination |
| "Zero-tool-call approval is a violation" | Task verification and termination |
| Subagent wired in with no single-agent set and no signed contract | Specification and system design |
| Topology choice: parallel races, peers without an anchor | Specification and system design |

## Self-check

Sentence: "every agent passes its own tests, so the system is fine."
Reality: every part up to spec and the assembly never tested; interaction failures live in no agent's steps.
Check: count the end-to-end cases in the set (zero → the sentence cannot even be tested); then pull the last 10 system-level failures, check every agent's single-agent verdict on each, and count "system failures where every single agent was green".

## Templates

- `templates/handoff-checklist.md` — decides whether a spawn and its return are contract-complete, and whether a reviewer subagent is independent.
- `templates/attribution-tree.md` — decides main / sub / handoff for one system-level failure, which eval set it enters, and what to fix.

## Migration notes

- Before any second agent (even a wrapped retrieval chain): a filled contract, 3 end-to-end cases, and an independence check if the role is review.
- Coding agents: does the code-review subagent only read the diff summary, or can it run the tests itself? Zero tool calls behind an approval is the collusion case.
- Research agents: count how often the retrieval subagent's "not found" was used as "does not exist" in the main flow; that is where the first handoff failure lands.
- Professional-judgment agents: a reviewer that signs on the drafter's summary adds no independent evidence chain; require it to open the record itself.
- Platforms: report the subagent share and maximum nesting depth per tenant; a nested `invoke_agent` span tree is the trace equivalent of the `subagent` step.
- Injection propagates through the handoff: add "does the handed-over context carry unquarantined external content?" to the contract check (see references/adversarial.md).
