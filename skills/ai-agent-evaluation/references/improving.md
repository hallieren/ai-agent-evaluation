# Turning measurement into the next fix

**Load this reference when:** the gate is green and the dashboard is still red; someone wants to edit the prompt because a failure screenshot came in; you must pick which failure to fix next and which component to change; a fix must be verified; the suite score climbs while production does not; the eval set is all green; a capability-set case is ready to graduate.
Source: chapter 15, docs/chapters/ch15-improvement-loop.md (templates: docs/appendices/ch15-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Do not expect the gate to say how to get better. Why: the gate stops things getting worse; the pass rate says how often it fails, not which component manufactures the failures.
- Retreat from metrics to traces when metrics cannot carry it. Why: production failure mining is the same skeleton as trace reading (read, code, cluster, atlas); only the sampling that feeds it is industrialized.
- Keep a random slice outside the failure pool. Why: the pool's recall is only as wide as the signals, and the modes the signals cannot see surface only in unfiltered reading.
- Never sample in proportion to traffic. Why: lookup-type tasks are the bulk and the simplest, and a proportional batch drowns in them.
- Put every sev-1 signal in the pool, never sampled. Why: it was counted on its own line to begin with.
- Keep naming and criteria in human hands. Why: clustering scripts only tidy what you have already named; genuinely new modes come from human eyes.
- Promote the suspected component to a falsifiable hypothesis before touching anything. Why: a sentence that fits any outcome cannot be refuted, and if you cannot write the sentence, read more traces.
- Use the lever table backwards: failure mode first, then lever. Why: picking the handy lever and finding the reason afterward makes the table useless.
- Move one lever at a time. Why: two levers moved together leave you unable to say whom to thank, whom to blame, or whether one helped and one hurt.
- Write the rejection rule before the run. Why: a standard set after the run lets any result be called "fixed".
- Verify in two parts, never one. Why: "did it get fixed" (target mode count) and "did anything else break" (full regression by sev) are different questions, and one short does not count.
- Believe production over the suite. Why: online signals take part in no optimization loop and cannot overfit along with you.

## Procedure

1. **Circle the failure pool** from online signals: online red-line assertion hits, escalations, negative feedback and restatement, repeat contacts, overturns, drift-probe pointers, judge escalations, cost tail over budget. Accept false positives and leaks; mining wants the structure of failure, not a census.
2. **Add a random slice** outside the pool (about a fifth of the batch, illustrative), through no signal filter.
3. **Sample stratified** by signal severity × task type. sev-1 all in. Draw every other stratum until the saturation criterion says stop (no new modes surfacing), reading the curve separately per task type.
4. **Read and code by hand** with the trace-review disciplines (see references/reading-traces.md): read forward, ask "given what it had at this step, was this action reasonable", mark `first_bad_step`, write a behavioral description, code blind. A script may pre-sort descriptions into piles (by `failure_mode`, falling back to the first keyword of `notes`); a person writes the name and the criterion.
5. **Extend the atlas** (templates/failure-mining.md) keeping the six columns: name / definition and criterion / representative trace IDs / count / sev distribution / suspected component. Old modes gain counts; new rows are the eval set's blind-spot list, and each owes a batch of new cases (e.g. the offline set tested "can it find the order" and never "the order ID was handed to you, do you use it", so the agent fuzzy-searched by name and hit a same-name customer).
6. **Pick the bottleneck** by the Decisions below (severity first, then frequency, then lever clarity).
7. **Write the hypothesis** in falsifiable form on templates/improvement-cycle.md: "<mode> fails because of <cause> in the <component>; change it and the target mode's count should drop from <n> to <m>, and no other mode should rise." Two plausible components → write both, try the smaller blast radius first.
8. **Look up the lever** in the eight-lever table (Frameworks), starting from the failure class. Record why this lever was chosen by evidence, not habit (templates/lever-mapping.md).
9. **Write the rejection rule** before the run: how far the target count must drop, how the interval is computed (paired, `--repeat 5`, clustered by case), where the full-regression gate line sits by sev, what counts as failure. Sign and date it.
10. **Move one lever.** Change only that thing (e.g. the tool description, not one word of the prompt).
11. **Verify in two parts.** Fixed: the target mode's count, paired with intervals (`python scripts/evalstats.py compare before.jsonl after.jsonl`), not the overall pass rate, which is neither sensitive nor loyal to this fix. Nothing else broke: full regression by sev, sev-1 on its own line, width per the change-tier table (see references/gating-releases.md). Both pass → merge, update the atlas row's count, next bottleneck. Either fails → roll back, switch to the second hypothesis; this is a normal step, not a setback.
12. **Close the loop**: new production data flows into the next round of mining. Record the holdout score and the first-run score of newly harvested cases on their own lines every version (Frameworks, Goodhart guards).

## Decisions

1. **Which bottleneck this cycle fixes.** Order by frequency × severity, severity first; the third question (how clear is the lever) is now a table lookup. sev-1 bottlenecks jump the queue. A high-risk mode with an unclear lever gets the gate first (a confirmation row in the permission matrix) while evidence accumulates; the bottleneck can wait, the harm cannot.
2. **How the fix is verified.** The two-part rejection rule in writing before the run: target-mode drop with interval, full-regression gate line by sev. Write it, then start.
3. **Graduation** (rule): a capability-set case passes `--repeat 5` on two consecutive versions → its file moves to the regression set and the gate owns it; a sev-1 case also needs a deterministic assertion first, because a judge cannot hold up zero tolerance. Record its first-run score on graduation day.
4. **Saturation** (regression and capability sets both 100%): the score carries no improvement signal; the only move is harder cases, drawn from new production modes, high-risk atlas rows with unknown levers, and tasks not yet rewritten into verifiable form.

## Frameworks

**Failure mining, four steps on one skeleton.** (1) Circle the pool from online signals. (2) Stratified sampling, sev-1 all in, plus a random slice outside the pool. (3) Blind human coding under the same disciplines as offline trace reading. (4) Extend the six-column atlas as its production increment.

**Eight levers × failure class × cost.** Find your failure class in the middle column first.

| Lever | Failure class it treats | Cost and blast radius |
|---|---|---|
| Edit the prompt (system instructions) | Behavior and phrasing: unauthorized commitment, answering flat when it should escalate, tone | Cheap; globally coupled, any trajectory can be caught; full regression mandatory |
| Edit the tool description | Wrong tool choice, wrong parameters, hallucinated tools | Cheap and narrow; only trajectories using that tool move |
| Swap the model | Capability failures: several modes high at once, nothing else moves them | Most expensive; judge fully recalibrated; largest suite (tier 3); saved for after every other lever |
| Add a confirmation gate (a permission-matrix row) | Irreversible actions: duplicate refunds, unauthorized execution | Lowers harm, not the error rate; price is human confirmation volume |
| Edit the handoff contract | Multi-agent context loss, reviewing off a summary | Medium; only the subagent path |
| Fix the memory policy | Crosstalk, misremembering, cross-session contradictions | Medium; verify with multi-session replay |
| Fix the knowledge base or retrieved content | Grounding failures: the policy clause itself is wrong or stale, cited faithfully, answer wrong | Cheap; touches every trajectory citing it; triggers relabeling of grounded gold labels first |
| Remove a component (an instruction, a validation layer, a tool, a context reset) | Stale scaffold assumptions: patches for the old model fighting on the new one; the cost tail | Cheap; blast radius as the prompt; full regression; verified by non-inferiority, and if nothing degrades the simpler version stays |

Use the table backwards. Handy ≠ on target: the prompt is the global lever with the largest blast radius, and fixing a wrong tool choice with it is fixing one broken door with the building-wide PA system. Fine-tuning is not in the table: a fine-tuned model is a new model, treated as tier 3 with the judge fully recalibrated and the largest suite. Unreachable bottleneck (often capability failures, model swap included) → the gate: the error keeps happening, the harm is shut behind human confirmation.

**Goodhart guards, three.** (1) Holdout subset: carve out about 1 in 5 harvested cases (illustrative), never look at its case-by-case results, never fix against it; it reports one tiered number per version. Suite up, holdout flat → overfitting confirmed. (2) First-run score of newly harvested cases is a one-time metric: the only reading in a batch's life never optimized against; after the first run the batch joins the loop and can measure "fixed" but never "generalizes"; the day the gap between the first-run series and the suite pass rate widens is the day the suite has aged. (3) Production is the outermost referee: overturn rate and repeat-contact rate cannot overfit; suite says fixed, production says not, believe production. The variance check (see references/trusting-numbers.md) guards against "the improvement does not exist"; these guard against "the improvement is real and exists only on the suite"; neither substitutes for the other.

**Three saturations, keep apart.** Coding saturation: reading traces surfaces no new modes (the atlas's business). Suite aging: suite score climbs while the holdout does not (overfitting). Eval-set saturation: regression and capability sets both fully green (add harder cases).

**The navigation loop.** Know (full report + gate = current state and floor) → Diagnose (failure mining + bottleneck location = where the next cut goes) → Sustain (one-lever fix + two-part verification = the cut lands without side effects) → new production data → next mining round. A healthy team turns this on a fixed rhythm, red lights or not.

## Self-check

- The sentence: "The pass rate went up, so the change was right."
- The reality: the rise may be variance, or the target mode did not move and the rise came from elsewhere, so the cut landed on nothing and the failure returns next week.
- The check: before declaring the fix effective, answer two numbers: how far the target failure mode's count dropped (paired, with intervals) and the sev-1 count. Cannot answer the first → you verified luck; can only answer the overall pass rate → you are celebrating somebody else's work.

## Templates

- `templates/failure-mining.md` — pool signals, stratified sampling, coding steps, atlas extension rows; produces the blind-spot list.
- `templates/lever-mapping.md` — the eight-lever table and the "handy ≠ on target" check; produces the lever choice with its evidence.
- `templates/improvement-cycle.md` — one page per cycle: hypothesis, lever, pre-written rejection rule, two-part result, graduation ledger, next candidates.

## Migration notes

- Coding agents: pool = reverted PRs, review rejections, CI failures after merge; levers map to system prompt, tool schemas for the repo tools, model, a "requires human review" gate for destructive git actions, the handoff contract between planner and worker.
- Research agents: the seventh lever dominates (a wrong or stale source cited faithfully); relabel grounded gold labels before verifying; holdout = a question set never used in prompt iteration.
- Professional-judgment agents: unreachable bottlenecks default to the confirmation gate with a qualified confirmer; verification lag means the first-run score and expert spot checks stand in for production's referee.
- Platforms: each team runs its own cycle on its own fork of the cases; the atlas's six columns and the sev semantics stay shared (see references/sustaining.md).
- First cycle in one week: day 1 circle the pool and read 20; day 2 extend the atlas, pick one bottleneck, write hypothesis and rejection rule; day 3 move one lever; day 4 rerun paired; day 5 report with intervals.
