# Building eval sets that represent reality

**Load this reference when:** the hand-written cases all pass and nobody trusts it; a failure mode atlas exists and no case hunts its rows; someone counts test cases as evidence ("we have 1,000"); a new requirement or capability is about to be built; a policy changed and nobody relabeled; cases are being synthesized by a model; a case's low score might be the grading; you need to decide which cells of coverage may stay empty.
Source: chapter 4, docs/chapters/ch04-eval-sets.md (templates: docs/appendices/ch04-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

1. A case is world state + request + expected trajectory properties, never an input-output pair. Why: right and wrong live in the relation between the reply and the world state (the same "refund this order" is correct to execute at ≤ the ceiling and correct to escalate above it).
2. Design the endpoint verifiable first. Why: an assertion is written once, runs ten thousand times for free, and never drifts; a judge costs a call per run, needs calibration, and drifts.
3. Every case clears a reference trajectory with zero model calls before landing. Why: the first suspect behind a low score is often the grading, not the agent (illustrative: a model went 42% → 95% on a public benchmark after grading bugs were fixed; another benchmark graded "reach" as "exceed" and penalized agents that obeyed).
4. Budget follows severity, not traffic. Why: sampling by traffic can leave sev-1 scenarios with zero cases, and they are the reason the eval exists.
5. Persona is a first-class dimension, and cooperative stays in. Why: vague forces guessing, angry forces rushed soothing, multi-request forces drops; cooperative tests "should not trigger" so you do not breed an agent that escalates everything.
6. Synthesis produces drafts only; every stratum keeps a non-synthetic anchor. Why: synthetic input is too clean and shrinks to the model's prior; the matrix looks spread out while the mechanisms crowd one cell.
7. Fixes target the failure mode, never the case's text. Why: a case whose phrasing sits in the system prompt tests recitation.
8. Register the policy basis of every label. Why: a gold label is a verdict under world state + policy; when the policy changes the label expires silently and punishes correct behavior the same way on every run.
9. New requirements become new cases first. Why: three cases with `setup`, `expect`, and `severity_if_fail` are more precise than three paragraphs of PRD and write the risk consensus down in advance.
10. Start at 50 cases; structural completeness before volume (illustrative count, rule on the order). Why: with the structure right, volume fills cells; with it wrong, volume reskins one case.
11. Every sev-1 mode gets a deterministic sentry. Why: sev-1 is never released on a judge's word alone.

## Procedure

1. Input: the failure mode atlas (references/reading-traces.md) and the policy or rules ledger.
2. Reverse-generate from every atlas row: one reproduction (setup restores the world as it was, prompt restores the request) plus several variants (same mode, different world state, persona, phrasing). Tag each with `failure_modes`.
3. Forward-generate the skeleton: one case per policy line (return window, refund ceiling, address-change window, identity verification, commitment red line). This is the red lines' positive checklist.
4. For each case run the seven-step golden task protocol (Frameworks); land it on the YAML schema only after step seven passes.
5. Hand-write at least one anchor per sev-1 mode, assertion-decidable, with its reference trajectory; land both together.
6. Draft volume by "failure mode × persona × policy line"; a human edits every draft until it reads real or throws it away. When several same-persona drafts read as the same anger or the same vagueness, rewrite them yourself.
7. Build the coverage matrix (`python scripts/coverage.py <cases-dir>`), rule every empty cell (Decisions), sign the annotation bar. Cross-check the atlas for modes missing as an entire row.
8. Split the set: capability set (cases the agent cannot pass yet, own report line, never blocking) versus regression set (expected ≈ 100%, gate reads only this). See references/gating-releases.md.
9. Hold out a small slice from daily regression; run it only at release evals.
10. Break at least one self-correlation link (case author, agent, judge); if none can be broken, mark the pass rate as an upper bound.
11. Register every case's policy basis; wire the change-triggered relabel flow; schedule the periodic audit (Frameworks).
12. Drill one expiry once: pick a plausible policy change (the refund ceiling rises), pull the affected-case list from the basis register, walk the diff → relabel → rerun path.

## Decisions

**Decision 1, the coverage matrix.** Axes: failure mode × severity × user type (in the artifact severity rides in a column beside the mode, so the table is mode × persona). Read it for two things: are all sev-1 rows non-zero, and which cells are empty.

| Cell state | Ruling | Requirement |
|---|---|---|
| any sev-1 row with a zero total | must fill | no exceptions; every high-risk mode needs a sentry standing |
| top atlas modes missing a persona | must fill | full-persona coverage of the atlas's top modes |
| empty cell where the failure mechanism and the persona interact (e.g. unverified-recipient disclosure × cooperative: calm "send me a copy of my order details" wording induces exfiltration as well as an angry one, and reads more like a real attacker) | fill | signed |
| empty cell with no interaction (e.g. missed request item × cooperative: dropping needs concurrent asks, a single-request persona has nothing to drop) | reasoned empty | written reason + signature by the spec owner |
| empty cell with no reason | hole | not a decision; the review does not pass |
| an atlas mode absent from the matrix as an entire row | louder than any empty cell | add the row, then rule its cells |

An empty cell with a reason is a decision; without one it is a hole. Changing the eval set means changing the matrix. (Illustrative live matrix: 50 cases, 14 modes × 4 personas = 56 cells, 19 non-empty, 37 ruled.)

**Decision 2, how big is big enough.** Structural half: every must-be-non-zero cell non-zero, every cell with variants and an anchor. Statistical half (cases per cell before the interval supports version comparison): see references/trusting-numbers.md (~400 cases for ±5 points, rule). Until then: 50 cases to start.

**Decision 3, where a failing case lives.**

| Case | Directory | Reported | Blocks release |
|---|---|---|---|
| written eval-first, agent cannot pass yet | capability set | own line | never |
| expected to pass | regression set (base cases, red-line, attacks) | pass rate ± interval, sev-1 count separately | a red light = regression |

Graduation (rule): a capability-set case passes `--repeat 5` on two consecutive versions → moves to the regression set. A sev-1 case also needs a deterministic assertion in place before it graduates. The set is never finished: cases graduate, requirements add, policy relabels, production failures flow back (references/going-live.md). An eval set unchanged for a year has lost contact with reality.

**Decision 4, self-correlation.** Same model writes the cases, runs the agent, and judges → the pass rate measures how high one model scores itself, stably and reproducibly. Break one link: human-rewritten cases (case side), judge-vs-human alignment with sev-1 never released by a judge alone (judge side, references/judging.md). If the team has exactly one usable model and no link breaks → downgrade the pass rate to an upper-bound reading ("at least not worse than this"), never "how good is it".

## Frameworks

**Case schema (YAML) and field meanings.**

```yaml
id: <case-id>
type: action              # query | action | investigate  (the three task families)
persona: cooperative      # cooperative | angry | vague | multi
prompt: "<the request, written the way this persona writes>"
setup:                    # sandbox seed: the world state before the case runs
  orders: [<order-id>]    # which records exist, each in what state
expect:
  assertions: [refund_not_executed, no_over_limit_commitment]   # end-state / trajectory checks
  judge: judge-tone-commitment                                  # optional; purely deterministic cases carry none
severity_if_fail: sev-1   # from the severity table (references/defining-good.md)
failure_modes: [unauthorized-commitment]                        # atlas rows this case hunts
```

Three consequences: writing a case includes building a world (designing `setup` is half the work); coverage gains dimensions (world states and personas must be spread, not only inputs); gold is not eternal (a label hangs on setup + policy).

**Two roads to the same golden task.** Testing unauthorized commitment: road A hands the reply to a judge (a call per run, drift, calibration). Road B seeds an over-ceiling order in `setup` and hangs `refund_not_executed` + `no_over_limit_commitment` on `expect` (written once, free forever, no drift). Take road B wherever it goes; the verifiability inventory's third column (rewrite won't go) is all that earns a judge.

**Assertion by target.**

| Target | Deterministic check | Judge only if |
|---|---|---|
| unauthorized commitment | `refund_not_executed`, `no_over_limit_commitment` on an over-ceiling setup | residual tone / commitment wording → `judge-tone-commitment` |
| misread status, doubling down | seed a tricky order state; `order_state_equals` | never |
| investigation citations | `citation_resolves` | report quality → `judge-report-rubric` |
| data disclosure | `no_pii_disclosure` on a setup with an unverified recipient | never |
| runaway cost | `budget_steps_max`, `budget_cost_max` | never |

**Seven-step golden task protocol.**

| Step | Action | Check question |
|---|---|---|
| 1 | pick the failure mode | which atlas row, what sev? |
| 2 | design the setup | are right and wrong pressed into a checkable end state? is the world state written out in full? |
| 3 | pick the persona, write the prompt | which of cooperative / angry / vague / multi? does it read like a real user? |
| 4 | write the expect, assertions first | has everything an assertion can decide been sunk down? is the judge reserved for language-only territory? |
| 5 | set `severity_if_fail` | consistent with the severity table? does sev-1 have a deterministic sentry? |
| 6 | register the policy basis | which policy line does the label depend on? is it in the basis register? |
| 7 | clear the reference trajectory, zero model calls | one hand-written or harvested passing trajectory: every assertion green, judge rules hit? |

Step 7 proves the task is solvable and the verdict configuration is right. No passing trajectory can be written → the task is unsolvable or `expect` locks a freedom it should not; go back to step 2 or 4, do not land the case.

**Three leakage paths.**

| Path | Mechanism | Plug |
|---|---|---|
| fix-time seepage | a case's phrasing pasted into the prompt or knowledge base as an example; the case now tests recitation | fix the mode, not the text; reword any case whose scene appears in prompt or KB, or mark it contaminated (the gate scans for this, references/gating-releases.md) |
| self-correlation | generator writes what it finds natural (comfort-zone distribution); a same-model judge shares language priors (kinship leniency); the number is stable and pretty | break one link (Decisions); otherwise upper-bound reading |
| overfitting the daily set | tuning prompts against the same 50 until the target becomes the cases | holdout slice run only at release; the day holdout pulls away from daily is the diagnosis |

**Label expiry, three countermeasures.** Register the basis (every case → the policy line it depends on). Change-triggered relabeling (a policy diff → affected-case list first; the change is not complete until relabeling is; rerun affected cases, mark the report "post-relabel", sign). Periodic audit (sample cases, ask "does the basis still hold"; deliberately sample never-failed cases, which may mean a strong agent or a case that died long ago, and never-passed cases, which may mean a weak agent or an unsolvable task; clear the reference trajectory before concluding either). Second expiry path: the policy stays and the agent outgrows the gold (triage in references/judging.md).

**Synthetic distortion, two sides.** Too clean (model anger is grammatical, coherent, on topic; real anger has typos, answers sideways, curses the carrier first). Shrinks to the prior (dozens of angry drafts from one prompt are one anger in rotated wording). Countermeasure is discipline, not technique: drafts only, human-edited or discarded, one non-synthetic anchor per stratum. Synthesis supplies volume; anchors supply truth.

**Living requirements doc.** New capability (e.g. address change) → write the cases before code: execute before shipment; within 24 h after shipment initiate a carrier intercept; past that refuse and explain. Requirements review reviews the cases (`setup` = scenario, `expect` = acceptance criteria, `severity_if_fail` = risk consensus). They fail on day one and live in the capability set.

## Self-check

Self-consolation: "we have 1,000 test cases."
Reality: count is the easiest metric to counterfeit; one scenario renamed, re-priced, and reworded a thousand times crowds one cell, and the bigger the number the sturdier the illusion.
Check: sort the cases into the coverage matrix and count two numbers, non-empty cells and cases in the sev-1 rows; a thousand cases in a handful of cells with sev-1 rows near blank is one case echoed a thousand times.

## Templates

- `templates/golden-task.md`: the seven-step protocol with the YAML landing self-check; produces one landed case with a cleared reference trajectory.
- `templates/coverage-matrix.md`: mode × sev × persona counts plus the annotation bar; produces the fill / reasoned-empty rulings with signatures.
- `templates/label-expiry.md`: basis register, change-triggered relabel flow, periodic audit; produces the affected-case list and the post-relabel report.

## Migration notes

- Coding agent: red line "no deleting tests to make the suite pass", with a doomed-to-fail test seeded in `setup`; world state = repo state; dimensions become repo size × change type × test coverage state.
- Professional-judgment agent (contract review): red line "liability cap below contract value → must escalate"; dimensions become contract type × jurisdiction × counterparty leverage.
- Research agent: `setup` = the corpus available; `citation_resolves` is the sentry; the judge takes only synthesis quality.
- No failure list yet: reverse from the policy or rules document, at least one "induce a violation" input per rule.
- Any domain: the matrix structure travels as is; the persona axis is the support world's stratification and gets redesigned around your failure mechanisms. Copy the case schema wholesale; the `setup` field forces the question most teams never ask, what is this agent's world state.
