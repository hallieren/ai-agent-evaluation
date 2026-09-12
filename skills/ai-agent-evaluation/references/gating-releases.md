# Gating every release so change stays safe

**Load this reference when:** a prompt or tool change is about to merge; someone says "it's just a prompt change"; the team is afraid to release or batching changes; a case goes red then green; a vendor announces a model upgrade; you need a CI gate, a change-tier table, a rollback runbook, or a stop rule; the first month has no thresholds.
Source: chapter 14, docs/chapters/ch14-release-engineering.md (templates: docs/appendices/ch14-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Read fear of releasing as the diagnosis of a failing eval practice. Why: the practice exists to make change safe, and fear means nobody believes anything will tell them before a regression reaches the user.
- Turn "run the eval" into a gate the process cannot route around. Why: a one-line prompt patch ("give a clear time expectation") punched straight through a commitment red line that a wording constraint had fixed, and nothing stopped it before the customer.
- Run replay before anything enters the main branch. Why: replay is the fastest, cheapest, lowest-variance layer, and it answers the one question every commit must ask, "did anything regress".
- Itemize replay's variance honestly: environment zero, model not. Why: recorded tool returns and wording never change, but the model re-reasons each time, and a team that expects zero variance concludes the gate is untrustworthy after the first red-then-green.
- Gate by severity, never by a total threshold. Why: "≥ 90% to ship" is average-score thinking, and the average is the best hiding place a high-risk failure could ask for.
- Never let a judge alone gate a sev-1 row. Why: a judge that misses is not easy to notice; judge-gated zero tolerance becomes zero observation.
- Compare paired, with intervals, threshold written before the run, in both directions. Why: 79% > 74% is not a reason to merge, and a red light that has not cleared the interval test blocks on variance and costs the gate everyone's trust.
- Never quarantine a sev-1 case. Why: a red line that flips is an intermittent hit, handled with pass^k, not noise.
- Pin dated model versions for the system under test and the judge. Why: an alias turns a vendor swap into a notice; a version number turns it back into a tier-3 change you schedule, and pinning both keeps the ruler from drifting with the thing measured.
- Relabel before gating on a policy change. Why: a gate run on rotten labels is itself lying.
- When unsure of the tier, tier up. Why: tiering saves the money that is certainly safe, not the money that is uncertain.
- Decide rollback and stop conditions in calm time. Why: at the incident there must be no decision to make, only a runbook to execute.
- Apply sev-1 zero tolerance from the first commit, no cold start. Why: it needs no distribution; one is one.

## Procedure

1. **Write the gate table** (templates/release-gate.md), five columns per row: metric / criterion / data source (replay or simulation layer) / verdict source (assertion, judge, human) / red-light action. Required rows: sev-1 count = 0 (rule) with verdict source assertion or human; sev-2 count ≤ budget and not significantly worse paired; cost P95 and latency P95 ≤ the budget line; near-duplicate scan of case text vs prompt / examples / knowledge base = zero hits (zero model calls). Capability-set results get their own line and never turn the gate red.
2. **Put it in CI, not the wiki.** Config under `ci/`, script exits non-zero on red, hung on the commit hook (`python ci/gate.py || exit 1` in `.git/hooks/pre-commit`). Example shape of the config:

   ```yaml
   # ci/gate.yaml — written before the run; a threshold change = tier 2, keep a record
   suites: [cases/redline]        # regression set only; cases/capability stays out
   flags: [write_tools]
   repeat: 1                      # sev-1 row: run 3 and take the majority
   thresholds:
     sev1_max: 0
     sev2_max: 2                  # illustrative
     cost_p95_max: 0.5            # dollars, illustrative
   ```

3. **Set the three cadences.** Every commit: the assertion subset + `cases/redline` + `cases/attacks`. Every PR merge: full replay. Nightly: the simulation layer with `--repeat` and intervals. Full replay retreats from every commit to every merge; the frequency retreats, the promise does not.
4. **Counter replay's model-side variance.** Write assertions at the semantic layer (lock "no unauthorized commitment", not its phrasing); run the sev-1 row 3 times and take the majority (rule); apply flaky quarantine to the replay layer too.
5. **Read the derail rate** on every replay run (share of cases where the new version leaves the recorded track). Derailed cases are auto-escalated to the simulation layer for a fresh verdict. Compare the rate against the band for the declared change tier; a mismatch re-tiers the change (Frameworks).
6. **Quarantine flaky cases** (three steps): flag by flip rate over a preset threshold from the `--repeat` record; move to a separate daily lane (results recorded, trend watched, no longer blocking); attach a deadline (two weeks, illustrative) and an owner, and rule at the deadline: fix the case (the `expect` locked a degree of freedom it should not have, e.g. exact wording instead of the commitment's meaning), fix the agent (the behavior is unstable; a high flip rate is a reproducibility defect in the system under test), or demote to non-gating monitoring.
7. **Classify every change by tier** before running anything (templates/change-tiers.md), by blast radius, never diff size. Run the tier's mandatory suite. Log the tier ruling in the pending-tier register with a signature.
8. **Run the gate.** `python scripts/evalstats.py compare old.jsonl new.jsonl` for the paired, intervaled comparison; `python scripts/evalstats.py report new.jsonl` for the sev-tiered lines. Red light → the red-light action in the table, no discussion.
9. **Canary as the default last gate** for every routine release: small slice, the online signals from references/going-live.md, promotion criteria written in advance; past it comes full traffic.
10. **Execute the rollback runbook on trigger** (four elements: trigger, executor, action, aftermath). Harvest the triggering case into the eval set; it waits in the next version's gate.
11. **Apply the stop rule** (templates/stop-rule.md) for situations no rollback fixes (attacks in batches, a broken upstream, harm landed with cause unknown). Pause to the lowest sufficient level; recovery reruns as a tier-3 change.
12. **Cold-start thresholds in the first month** (Frameworks); recalibrate quarterly, and run each recalibration through the tier table.

## Decisions

1. **Release gate definition.** Five columns per row, in `ci/` config; a gate not enforced in CI is only a wish. The sev-1 row's verdict source is never a judge alone; the sev-2 row carries a written budget number; the cost / latency row carries the P95 budget line. Example sev-1 row: unauthorized commitment count / = 0 / replay + simulation layer / assertion / block immediately.
2. **Change-tier table calibrated against your own history.** Page through last month's merges, ask of each what tier it ran at and what tier the table says; the gap is your current risk exposure. Keep the fallback row (tier up); a vendor's upgrade email goes through the table too.
3. **Gate by severity.**

| Tier | Regime | Criterion | Verdict source |
|---|---|---|---|
| sev-1 | Zero tolerance, its own line | Count = 0 (rule); never averaged; immune to interval talk | Assertion or human; judge may only escalate |
| sev-2 | Budgeted | Count ≤ ceiling written in advance (from the severity table's tolerance negotiation) AND not significantly worse in the paired comparison | Assertion, calibrated judge, or human |
| sev-3 | Trend | Never blocks one release; recorded across versions; worsening trend files a ticket | Any rung |

Non-inferiority criterion: the gate asks only "is the new version no worse", i.e. degradation no larger than the pre-written amount; improvement is none of its business. Both-direction interval rule: a green light needs the paired interval to exclude the written degradation, and a red light must clear the interval test before it blocks.

4. **Stop rule, two branches, three pause levels** (Frameworks); recovery after any stop = tier-3 change.

## Frameworks

**Cost arithmetic (illustrative).** cases × mean steps × tokens per step × unit price × commits per day. 50 cases × 12 steps × ~3K tokens × $3 per million tokens ≈ $5 per pass; 30 commits a day ≈ $150 a day, four figures a month; 200 cases → ×4. The $5 looks too small to justify skipping; the account only counts once multiplied to the end of the month, which is why full replay runs per merge, not per commit.

**Derail-rate bands (illustrative; calibrate against your own history).**

| Change type | Expected derail rate | Reading |
|---|---|---|
| Prompt | 30–60% | Only 5% is suspicious: the change did not take |
| Tool description | < 10% | Only trajectories using that tool should move |
| Report wording | ~0 | |
| Declared tier 1, observed 40% | — | Tiered too low → tier up per the fallback row |

**Quarantine disciplines, three.** No silent renewal: a deadline passed without a ruling defaults to "fix the agent", burden of proof on whoever wants to revoke it. sev-1 never quarantined: flipping red lines are intermittent hits, judged pass^k (`python scripts/evalstats.py passk --p <rate> --k 5`). List length is a gate-health metric: quarantine list > 5% of the eval set (illustrative) is a system problem (simulation-layer fidelity or agent stability), not a case-by-case fix.

**SLOs in the gate.** `budget_steps_max` and `budget_cost_max` graduate from case assertions to release-level SLOs on the same accounting basis. Watch P95, not the mean; the tail is the bill. Gate row: per-task cost and latency P95 do not cross the budget line, and the budget-assertion hit rate is no higher than the previous version (paired). With subagents: system cost = outer usage + every nested trace's usage, three columns (main agent / subagents / round trips); leave the nested account out and the SLO is decoration.

**Change tiers.**

| Tier | Change type | Must run | Recalibration |
|---|---|---|---|
| Tier 1 (local) | A single tool description, an individual case fix, report wording | Full replay (auto on commit) + simulation of the affected case subset | None |
| Tier 2 (behavioral) | System prompt, planning / memory policy, adding or removing a tool, persona script, a gate threshold change | Full replay + full simulation (paired, with intervals) + red-line and attack sets | If a rubric moved, recalibrate the related judge |
| Tier 3 (foundational) | Vendor model swap or base upgrade (including a vendor upgrade notice), a change to the judge's prompt or base, policy change, verdict-logic change, recovery after a stop, a fine-tuned model | All of tier 2, no sampling + matching recalibration + mandatory canary | Model swap: rerun judge-vs-human alignment before any gate number (`python scripts/judge_align.py judge.jsonl human.jsonl`); policy change: relabel affected cases first, then gate |
| Fallback | Any change you are unsure of | Tier up | Tier up |

Vendor model swap notes: it is the tier-3 change most easily mistaken for tier 0 (no diff, no PR); a swap replaces half the system under test and voids the judge's calibration because the alignment set no longer represents what the judge will face; after a swap, try deleting the most prescriptive prompt instructions and keep the simpler version if nothing degrades (see references/improving.md, eighth lever). A mandatory canary because stubs have a fidelity limit and foundational risk cannot be fully tested offline.

**Rollback runbook, four elements.** Trigger (which gate reds and online signals count; a production sev-1 is on the list). Executor (on-call has authority, no meeting). Action (previous version stays available; one command switches back). Aftermath (the triggering case is harvested into the eval set).

**Stop rule.**

| Branch | Trigger | Ruling |
|---|---|---|
| Safety | The shutdown red lines, verbatim from templates/shutdown-checklist.md: any red-line action succeeding past every defense layer (an over-limit refund goes through, details leak), any cross-session harm from poisoned memory, a subagent executing an instruction injected into the main agent | Stop on occurrence, no discussion, no iteration |
| Operational (you define it) | Production sev-1 ≥ 1 in a single week (illustrative); monitoring metrics (escalation rate, tool error rate) repeatedly crossing the line | Ruled the same day; default action is a downgrade; burden of proof inverted, the side that wants to keep running must argue |

Three pause levels, capability flags as actuators (unlocked one layer at a time, so locked back one layer at a time): (1) execution to human, turn off `write_tools`, every write becomes a suggestion, the agent still looks up, answers, drafts; (2) read-only downgrade, the reply itself is a draft sent after human review; (3) full stop, traffic back to pure human. Drill at least one level; recovery = tier 3.

**Threshold cold start, four steps.** (1) Weeks 1–2: hang every gate, run on every commit, produce reports, red does not block; this buys the distribution of pass rate, derail rate, cost, latency. (2) Set initial values: P95 budget line = observed P95 + margin; sev-2 budget from the high end of actual weekly counts via the tolerance negotiation; derail bands = observed values bucketed by change type. (3) Judge-gated rows: pull a batch of judge verdicts for human review; the human overturn rate is the initial band, because the judge cannot vouch for itself. (4) First version rough, written down, recalibrated quarterly through the tier table. Exception: sev-1 = 0 takes effect from the first commit.

## Self-check

- The sentence: "It's just a prompt change, no need to rerun."
- The reality: the prompt is the single largest point on the behavior surface, and one line of wording instruction punched through a commitment red line.
- The check: page back through the last 10 merges, count the eval skips, find who decided "no need to run" in which line of which chat; then hang the replay layer on the commit hook so "don't rerun" stops being an option.

## Templates

- `templates/release-gate.md` — the five-column gate table and the interception record; decides what blocks merge.
- `templates/change-tiers.md` — which suite a change must run and what it recalibrates; decides the tier before anything runs.
- `templates/stop-rule.md` — safety and operational branches, three pause levels, rollback runbook; decides when the agent pauses and how it recovers.
- `templates/go-no-go.md` — the one-page room decision with a risk-owner signature column; decides continue / narrow / stop.

## Migration notes

- Coding agents: replay = the recorded issue set rerun on commit; canary = low-risk repos first; a base-model or IDE-vendor upgrade is tier 3; "execution to human" = PRs opened but never auto-merged.
- Research agents: the derail band for a prompt change is wide by nature; gate on citation assertions (`citation_resolves`) and overreach red lines; a knowledge-base or retrieval-source change relabels grounded gold labels before the gate.
- Professional-judgment agents: the operational branch tightens to "a single sev-1 stops the agent", no weekly count; the change-tier table is the predetermined change-control plan a regulator expects; a model swap clears compliance (see references/high-stakes.md) before recalibration is even discussed.
- Platforms: the sev table and gate semantics are one copy organization-wide, changed as tier 3 (see references/sustaining.md); a gate slower than ~10 minutes (illustrative) teaches teams to route around it.
- First gate tonight: assertion-judged subset as the replay layer on commit; three rows (sev-1 = 0, sev-2 ≤ budget, cost P95 ≤ line) from historical distribution; a two-row tier table ("prompt and model = full, everything else = subset"); rerun your last "no need to rerun" change paired as the first piece of evidence.
