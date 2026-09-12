---
name: ai-agent-evaluation
description: >
  Use when designing, running, reading, or reviewing an evaluation of an AI agent or LLM
  system: deciding whether an agent can ship, defining what "good" means for a system that
  acts, error analysis on traces, building an eval set, choosing between assertions, LLM
  judges and human labels, calibrating a judge, reporting pass rates and comparing versions,
  sandboxes and synthetic users, tool calls and irreversible actions, planner cost, memory,
  subagents, prompt injection and red teaming, shadow and canary launches, CI release gates,
  regression, stop rules, improvement loops, and incident postmortems. Also use whenever the
  user says "eval", "eval set", "LLM-as-judge", "pass rate", "is it better", "can we ship",
  "golden set", "benchmark our agent", "regression suite", "red team", "canary", or asks to
  review an eval report, plan, judge prompt, or release gate. Not for public leaderboards,
  retriever metrics (recall@k, NDCG), prompt engineering as such, or building the agent.
---

# Evaluating AI agents

**Score the endpoint, attribute the path, account for the side effects. Eval before you build.**

An agent's results land in the world (order state, files, money, mail), not in a piece of text. That makes the endpoint easier to verify than prose and makes three things invisible to an endpoint check: why it failed, what the path cost or risked, and what to do when no gold answer exists. A failure planted at step 3 detonates at step 9. Every step samples, so a single run's number is one lottery draw. Everything below follows from those facts.

Load one primary reference per situation (see the router); add only an overlay the router names (high-stakes for a regulated domain, the matching reference in review mode). Templates are fill-in artifacts; copy them into the user's project. Scripts are stdlib Python; run them instead of re-deriving statistics.

## Route by situation

| The user says | Job | Load | First move |
|---|---|---|---|
| "Demo works, boss asks can we ship, we have nothing" | know | `references/defining-good.md` (Pocket Eval section) | Two hours: one-page boundary → five worst failures → 10–20 boundary-crossing cases (≥ 3 two-turn) → four verdicts → signed continue / narrow / stop |
| "What should we measure, what counts as good" | know | `references/defining-good.md` | Place each task on the three axes, rank the six attributes, write the severity table with "undoable? who absorbs it?" |
| "Pile of failures, no idea which matter" | diagnose | `references/reading-traces.md` | Read 20 traces forward, mark `first_bad_step`, code blind, cluster into the six-column atlas |
| "Need test cases" / "our cases don't look like production" | know | `references/building-eval-sets.md` | Reverse-generate from the atlas; every case gets `setup` + `expect`; fill the coverage matrix; clear the reference trajectory with zero model calls |
| "Should we use an LLM judge" / "does our judge work" | know | `references/judging.md` | Walk the ladder from the zeroth question; sink everything deterministic; judge-vs-human alignment with per-class recall |
| "74% → 79%, is that real" / "how many cases do we need" | know | `references/trusting-numbers.md` | Rerun the old version; paired, ≥ 5 runs, cluster by case; `python scripts/evalstats.py compare` |
| "We can't test refunds / emails / pushes for real" | sustain | `references/harness.md` | Sandbox + stubs + reset; four-element persona scripts; replay under simulation |
| "We're giving it write tools" | diagnose | `references/tool-calls.md` | Permission matrix rows as tool × condition, each with a guard; seeded-error probe; diff list first, reply second |
| "We're adding a planner" / "the bill doubled" | diagnose | `references/plans-and-cost.md` | Plan rubric + deviation checklist; report cost as median / P95 / max per task type |
| "We're adding memory" | diagnose | `references/memory.md` | Four mechanisms, each its own row; the crosstalk pair; a three-session check |
| "We split it into subagents and it got worse" | diagnose | `references/multi-agent.md` | Three suspects; attribution procedure in fixed order; handoff contract |
| "It reads web pages / inbound email" / "red team" | sustain | `references/adversarial.md` | Threat model first; surface × carrier matrix; tally interceptions per layer |
| "Offline is 91%, launching Monday" | know + sustain | `references/going-live.md` | Read the permission matrix's rollback column → mandatory rungs; wire signals before traffic |
| "Fixed A, B regressed" / "people fear merging" | sustain | `references/gating-releases.md` | Gate by sev in CI config; change tiers; flaky quarantine with a deadline; stop rule |
| "We have data, don't know what to change" | diagnose + sustain | `references/improving.md` | Mine failures → falsifiable hypothesis → one lever → two-part verification; holdout untouched |
| "Postmortem became a blame game" / "nobody owns the evals" | sustain | `references/sustaining.md` | Trace on the table, `first_bad_step`, layered interception, action items → equipment + owner + deadline |
| "Review my eval report / plan / judge / gate / cases" | any | this file, **Review mode** + the matching reference | Tagged one-line findings, then the closing line |

Regulated or high-harm domain (health, finance, legal): also load `references/high-stakes.md`. Unsure which word means what: `references/glossary.md`. Naming failure modes after clustering: `references/failure-taxonomy.md` (never before).

## Invariants

Apply these everywhere. Each carries its reason so you can defend it.

1. **The endpoint is the primary criterion; make it verifiable before spending judge or human money.** The world is easier to verify than text; rewrite "customer satisfied" into checkable facts.
2. **sev-1 is counted on its own line, never averaged, never released by a judge alone, always guarded by an assertion or a human.** One is one; the average is the best hiding place a high-risk failure could ask for.
3. **Every verdict sits on the lowest ladder rung that can carry it** (assertion < deterministic check < calibrated judge < human). Higher rungs cost more and widen ambiguity.
4. **Mark only the first bad step; downstream echoes are not new failures.** Cause clusters produce a repair list; symptom clusters produce a report.
5. **Read traces before building metrics; read forward, never backward from the blast.** Working backward explains every step by the ending you already know.
6. **A single run is one draw. Every number carries an interval whose denominator is the case count.** n × k verdicts treated as independent is pseudo-replication and halves the interval.
7. **Thresholds, rejection rules, and primary metrics are written and signed before the run.** Pick the standard after the run and any number becomes significant.
8. **Change the spec before unlocking any capability. No spec update, no unlock.** Write tools, planner, memory, subagents, external content: each gets its cases first.
9. **Every sandbox change is either declared as expected, or it is a finding.** Assertions catch what you thought of; the diff exposes what you did not.
10. **Deviation raises an alarm, never a forced verdict.** A derailed replay changes examination halls; grinding out a verdict on frozen returns is noise.
11. **The defense and the ruler that measures it are two different things.** Guards stop; online assertions ask whether the guards stopped it.
12. **One lever at a time, chosen backwards from the failure mode.** Two levers moved together leave nobody to thank or blame.
13. **Findings become permanent regression cases, never a report in a drawer.** An attack fixed but never banked returns next version.
14. **An unsigned decision is not a decision; an empty cell with a written reason is a decision, without one it is a hole.**
15. **Report the distribution and the tail, never only the mean.** Cost and latency pin to P95; the tail is the bill.

## Vocabulary

- **Four verdicts** on a case: `pass` (endpoint right, path clean) · `concern` (attempt, near miss, low harm) · `unsafe` (red line hit) · `unclear` (cannot judge; a signal that the criterion is not verifiable yet). Never a 0–10 score: a score is fake precision and gets averaged. Real users labeling outputs replace `unclear` with `useless`.
- **Severity** grades failures, not cases. **sev-1** irreversible harm or unauthorized action, zero tolerance. **sev-2** wrong information causing recoverable loss, budgeted. **sev-3** experience and efficiency, trend. A **near miss** crossed the line with no consequence: verdict `concern`, no tier.
- **Trace**: one run, steps of type `model | tool_call | tool_result | subagent | inbound`, then `final`. **Case**: world state (`setup`) + request + expected trajectory properties (`expect`). **Verdict record**: the row a judgment produces, with `first_bad_step` and `judged_by`.
- **Three jobs**: **know** (is it good enough to ship), **diagnose** (why not, down to the step), **sustain** (it is live and still changing). An eval activity that cannot name its job is a ritual.

## Decision procedures

**Position the task, then pick the instrument**
1. Is the endpoint verifiable? Yes → assertion. Partly → rewrite until only a small residue is left. No → step 3.
2. Is the action reversible? No → dense red lines, assertion sentries mandatory, failures default sev-1.
3. Does a gold answer exist? No → citation audit first, then a dimensional rubric judge (binary dimensions, explicit aggregation).
4. How long until the error shows? Long lag → offline carries the weight; online uses leading indicators and expert spot checks.
5. Write the row into the verifiability inventory: verifiable now / rewritable / rewrite won't go. Only the third column ever reaches a judge.

**Judgment ladder, before writing any judge prompt**
0. Did the prompt ever say it? Say it. A failure that vanishes keeps its case for regression and earns no judge.
1. Queryable from the sandbox or world state? → assertion.
2. Checkable against the policy ledger? → deterministic check.
3. Does a conservative scan clear the outright violations? → scan first; only the gray zone goes up.
4. Language-only residue → a narrow judge (one property) or a rubric judge (dimensions), calibrated against humans before duty.
5. Humans do three jobs only: arbitration, spot checks, ground truth. On sev-1 the judge may escalate, never release.

**Severity arbitration**
1. Can this error be undone? No → sev-1 candidate.
2. If not, who absorbs it? No name → sev-1, by rule.
3. Undoable, the user loses and recovers → sev-2 with a budget.
4. Experience or efficiency only → sev-3, scheduled.
5. Consequence upgrades a tier (a dropped time-critical item escalates); mechanism never downgrades one.

**Capability unlock gate** (write tools, planner, memory, subagents, external content)
1. Does the spec hold permission rows written as tool × condition?
2. Does every sev-1 red line have an assertion guard? A judge does not count.
3. Has it run in a sandbox with a before/after diff?
4. Is there at least one seeded-error probe aimed at the defenses?
5. "Who confirms? How does it roll back?" answered per write tool. No answer to "who confirms" → do not unlock.
6. The capability's cases are filed before the flag flips.

**Launch rungs** (replay → silent/shadow → canary → full traffic)
1. Read the permission matrix's rollback column per action type.
2. Empty, or nominally reversible but unrecoverable in practice → all four rungs; shadow is not skippable.
3. Read-only, or every write needs confirmation → shadow may fold into the canary.
4. Each rung answers three questions: what it newly verifies, the promotion signal, the rollback signal. Sign each promotion.
5. Canary: slice by task type (reversible first), bucket by customer and keep it sticky, criterion "no worse than the human baseline", gauges wired before traffic.
6. Any sev-1 online → roll back on one instance. Drift → harvest cases, never roll back.

**Change tiers** (must-run grows, never shrinks)
1. Tier 1, local (one tool description, a case fix, wording) → full replay + simulation of the affected subset.
2. Tier 2, behavioral (system prompt, planner or memory policy, tool added or removed, persona script) → + full simulation paired with intervals + red-line and attack sets.
3. Tier 3, foundational (model swap including a vendor upgrade notice, judge prompt or base, policy change, verdict logic) → + recalibration or relabeling + a mandatory canary.
4. Pin dated model versions for the agent and the judge; an alias is unpinned and turns a tier-3 change into a notice.
5. Derail rate outside the declared tier's band → tier up. Unsure → tier up. Recovery after a stop → tier 3.

**Lever selection** (improvement loop)
1. Start from the atlas row and its suspected component.
2. Write the falsifiable sentence: "X fails because of Y in component Z; change Z and the count on X drops from A to B, and no other mode rises."
3. Look up the lever backwards from the failure class: prompt · tool description · model · confirmation gate · handoff contract · memory policy · knowledge base · remove a component.
4. Two plausible levers → smaller blast radius first. Move exactly one.
5. High severity with an unclear lever → the gate first; keep the case as a sentry.
6. Write the rejection rule, then verify two ways: target-mode count down (paired, with interval) and nothing else worse, by sev.

## Output contracts

Produce these in exactly this shape. Numbers in the examples are illustrative.

**Report line** (every metric, every report):
`pass rate 74% ± 11 (50 cases × 5 runs, clustered by case); sev-1 count 0 (listed separately, never averaged in); sev-2 failures 3; sev-3 failures 12`
Base grid: `Metric | Mean | Interval (clustered by case) | Cases | Runs | sev-1 / sev-2 / sev-3`. Compute the half-width with `python scripts/evalstats.py size --cases N` (exact at the observed rate, or run `report` on the verdict file); quote ±1/√n only as the worst-case rough cut and label it so. Cost and latency: `median / P95 / max`, with the accounting basis stated (unit prices, cache discount, in/out priced separately).

**Case** (YAML):
```yaml
id: <unique-id>
type: query | action | investigate
persona: cooperative | angry | vague | multi
prompt: "the user's opening message"
setup: { world state before the run }
expect: { assertions: [...], judge: optional-judge-name }
severity_if_fail: sev-1 | sev-2 | sev-3
failure_modes: [atlas-mode-name]
```

**Verdict record**: `{case_id, run_id, verdict, severity, failure_mode, first_bad_step, judged_by: assertion | judge-<name> | human, notes}`.

**Spec** (one living file, revision log): intended use in three lines (for whom / does what / does not do) + action boundary as tool × condition rows in three columns (autonomous / needs confirmation / forbidden) with a guard per row + attribute ranking with its reason and a "who this ranking lost to" log + severity table with "undoable? who absorbs it?" per row + verifiability inventory.

**Gate row** (five columns, first row fixed): `Metric | Criterion | Data source (replay / simulation) | Verdict source (assertion / judge / human) | Red-light action` → `sev-1 count | = 0 | replay sev-tiered report | assertion | refuse merge`.

**Atlas row** (six columns): `Name (behavioral verb phrase) | Definition and criterion (decidable hit / no-hit) | Representative trace IDs | Count | sev distribution | Suspected component (? allowed, blank not)`.

## Claim → evidence

| Claim | Requires | Not sufficient |
|---|---|---|
| "The new version is better" | Paired run on the same cases, ≥ 5 runs each, intervals clustered by case separated or McNemar passing, rejection rule written first, old version rerun | A single-run delta; n × k as the denominator; a metric chosen after the run |
| "It's safe to ship" | sev-1 = 0 from assertions or humans, sev-tiered report, every rollback-empty action walked through shadow and canary, signals with baseline + band + trigger, signed go / no-go | An overall pass rate above a threshold; judge-only sev-1 verdicts; a good demo |
| "Our judge works" | Judge-vs-human alignment on a sev-stratified set, false-pass and false-fail per layer, per-class recall line, human-human anchor, report dated after the last prompt or base change | Overall agreement rate; a stronger base model; a longer prompt |
| "Coverage is good" | Coverage matrix with every sev-1 row non-zero, every empty cell signed with a reason, a non-synthetic anchor per stratum, every atlas mode present as a row | Case count; traffic-proportional sampling; synthetic volume |
| "The fix worked" | Target failure mode count down (paired, interval), full regression by sev with sev-1 on its own line, one lever moved, holdout flat or up | Overall pass rate up; two levers at once; suite up while the holdout is flat |
| "Sandbox pass means production pass" | Fidelity gap register reconciled row by row (confirmed / refuted / no evidence), then shadow and canary evidence | Zero registered gaps; "the stubs are close enough" |
| "Each agent passes, so the system is fine" | End-to-end cases passing; attribution naming main / sub / handoff for recent failures; handoff contract checks | Single-agent bars green; reviewer approvals with zero tool calls |
| "We held the attack" | Layered interception table with intervals, breaches on their own line, interceptions not crowded in the last layer, variants across carriers banked as regression cases | No breach in one run; a "breach rate"; interceptions all at human confirmation |
| "We have an eval culture" | Commit history with most of the team adding cases, non-engineers among them; weekly trace-reading output; a case ID per incident; RACI with real names | Dashboards; a values poster; a platform team |
| "It's just a prompt change" | Tier 2: full replay + full simulation paired with intervals + red-line and attack sets; derail rate inside the prompt band | Diff size; "only one line"; a green subset run |

## Review mode

When asked to review an eval plan, eval set, judge, report, gate, or postmortem: load the matching reference, then emit findings only. Flag what would change a decision; wording preferences are not findings.

| Tag | Criterion | Required replacement |
|---|---|---|
| `avg-hides-sev` | A rate reported without sev stratification | `sev-1 N, sev-2 N, sev-3 N, rest pass` |
| `no-interval` | A number without interval, case count, and run count | The report line |
| `pseudo-rep` | Interval denominator is verdicts (n × k), not cases | Cluster by case |
| `no-denominator` | A proportion with no n, or n < 10 read as a scale | Attach n; single digits → read the cases, do not report the ratio |
| `single-run` | A verdict or comparison from one pass | ≥ 5 runs, paired, rejection rule first |
| `judge-gates-sev1` | A sev-1 verdict source is a judge alone | Assertion guard or human spot-check list |
| `uncalibrated-judge` | No alignment report, or one older than the last prompt or base change | Run alignment; add the validity statement |
| `symptom-coded` | Failure logged at the blast, not the first bad step | Re-mark `first_bad_step`; rename the mode behaviorally |
| `no-setup` | A case with an input but no world state or expectation | Add `setup` + `expect`; sink assertions first |
| `unsigned-empty` | An empty coverage cell or missing threshold with no reason and no name | Fill it, or write the reason and sign |
| `wording-assertion` | An assertion locked on phrasing instead of meaning or world state | Assert the semantic property or the end state |
| `no-guard` | A permission row, write tool, or gate row with no assertion or precondition | Add the guard, or demote to needs-confirmation |
| `judgment-as-defense` | A defense that depends on the agent's judgment, or a guard used as its own ruler | Hard boundary independent of judgment; a separate online assertion |
| `alias-model` | Agent or judge referenced by a vendor alias | Pin dated versions; treat a swap as tier 3 |
| `no-regression-case` | An incident, red-team finding, or overturn with no case ID | Harvest it: rebuild `setup`, fix `expect`, file it in the matrix |

Finding format, one line each: `<where>: <tag> <what is wrong>. <replacement in one clause>.` Every finding carries exactly one tag from the table; one line means one line, no second sentence, no sub-bullets. When the user asks for brevity, keep only the findings that would change the decision, sev-1 exposure first, at most six.
Example: `Report §2: avg-hides-sev "pass rate 91%" carries no tiers. Rewrite as sev-1 0 / sev-2 3 / sev-3 12, rest pass.`
Close every review with: `sev-1 exposure: <none found | N findings that could let a sev-1 through>. Fix first: <one tag>.`
Nothing to flag: `Holds. Nothing to overturn.`

## Self-deception table

Each sentence is the consolation a team tells itself. Answer it with the check, not with an argument.

| The sentence | Reality | Executable check |
|---|---|---|
| "Eval is too heavy; we can't start yet." | Shipping without evidence is a decision, not a resourcing problem. | Find two hours today; run the Pocket Eval. |
| "The result was right, so the trace is fine." | A pass by luck is a dress rehearsal for the next incident. | Pull 10 random `pass` cases, read only the paths; count dangerous actions and doubled-down errors, write the ratio into the report. |
| "We ran 500 cases, 82% pass." | Two real numbers, both empty, until someone has read a failure. | Pull one failure at random; ask the reporter for its `first_bad_step`. |
| "We have 1,000 test cases." | Count is the easiest metric to counterfeit. | Sort into the coverage matrix; count non-empty cells and cases in sev-1 rows. |
| "The LLM judge says pass, so it passes." | An evaluator nobody has evaluated has no standing. | Blind-label a sev-stratified sample of its passes; compare the alignment report's date with the last prompt or base change. |
| "79% > 74%, so the new version is better." | First ask how much each number moves on its own. | Rerun the old version unchanged; the improvement must clear that swing. |
| "It all passes against the stubs, so it will pass in production." | Sandbox pass rate is capped by stub fidelity. | Count registered rows in the fidelity gap register; zero means nobody looked. |
| "The reply was graceful, so this round was fine." | After write tools, the reply is the least informative part of the trace. | Cover the reply on 10 endpoint-pass write traces; re-verdict from `tool_call` args and the diff list; count overturns. |
| "Every step was right, so the path is fine." | Each step can be right and the total a detour. | For the top-3 orphan-step traces ask per step: "delete it, does the endpoint change?" |
| "All single-session cases pass, so multi-session is fine." | A stateless eval set is issuing a pass to a stateful system. | Count cases whose verdict needs two or more sessions; zero with memory on is failing to examine. |
| "Every agent passes its own tests, so the system is fine." | Every part up to spec does not mean the airplane flies. | Count end-to-end cases; among the last 10 system failures count those where every agent was green. |
| "We added an anti-injection line to the prompt, so we're safe." | One sentence is one layer, and a wording-level one. | Rephrase the samples it stops (split, encode, quote, switch language); rerun; the drop is that line's true quality. |
| "91% offline, time for full traffic." | Offline measures the world you could think of; the wreck is in the part you couldn't. | Answer: red-line hits on production in the last 24 h? last reconciliation of production inputs against the eval set? date of the last harvested case? |
| "It's just a prompt change, no need to rerun." | The prompt is the largest point on the behavior surface. | Count eval skips in the last 10 merges and who decided; hang the replay layer on the commit hook. |
| "The pass rate went up, so the change was right." | The overall rate is neither sensitive nor loyal to your fix. | Report the drop on the target failure mode (paired, interval) and the sev-1 count. |
| "We have eval infrastructure, so we have an eval culture." | Infrastructure without habits is a few people's overtime. | Count who added a case last month (under half the team is a danger sign; any non-engineers?); ask a colleague which case matches the last incident. |

## Never produce

- A threshold presented as a default. The book's numbers are teaching numbers; label them `(illustrative)` and cold-start real ones from two weeks of run-but-don't-block data. The one exception needs no history: sev-1 = 0.
- A ratio on a single-digit denominator. Read the cases instead.
- A "breach rate", an averaged sev-1, or any high-risk count folded into a mean.
- An "improvement" without the old version rerun under the same conditions.
- A severity tier with no answer to "undoable? who absorbs it?".
- A judge verdict on sev-1 with no assertion or human beside it.

## Supporting files

References (`references/`): `defining-good` · `reading-traces` · `building-eval-sets` · `judging` · `trusting-numbers` · `harness` · `tool-calls` · `plans-and-cost` · `memory` · `multi-agent` · `adversarial` · `going-live` · `gating-releases` · `improving` · `sustaining` · `failure-taxonomy` · `high-stakes` · `glossary`. Each opens with "Load this reference when" and, except the glossary lookup index, lists its templates.

Scripts (`scripts/`, stdlib only, `--help` and `--selftest` on each):
- `evalstats.py report verdicts.jsonl` → the report line with intervals clustered by case, sev counts, flip rate, cost P95. `compare a.jsonl b.jsonl` → paired McNemar. `size --gap 5` → cases needed. `passk --p 0.9 --k 5`.
- `judge_align.py judge.jsonl human.jsonl` → layered disagreement, per-class recall, false-fail line, validity statement.
- `coverage.py cases/` → coverage matrix, empty cells, sev-1-row check.
- `snapshot_diff.py before.json after.json --expected table:kind` → `+ - ~` list and undeclared findings.

Templates (`templates/`): 40 fill-in files, each named in its reference. Start points by situation: taking over an agent → `pocket-eval.md`; about to launch → `evidence-ladder.md`, `release-gate.md`, `change-tiers.md`, `stop-rule.md`; just had an incident → `postmortem.md`.

Source of truth: the book *AI Agent Evaluation* (`docs/chapters/`, `docs/appendices/`) and its templates (`repo/templates/`). Where this skill and the book disagree, the book wins.
