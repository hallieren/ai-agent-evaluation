# Bottleneck-to-Lever Mapping (Chapter 15)

> Note: the correct use is **backwards**, start from the failure mode, then look up which lever to move; not pick the handy lever first and then find the reason. One lever per cycle.

## Seven levers × failure classes

| Lever | Failure class it treats | Cost and blast radius (regression width) |
|---|---|---|
| Edit the prompt (system instructions) | Behavior and phrasing: unauthorized commitment, answering flat when it should escalate, tone | Cheap; but globally coupled, any trajectory can be caught in it, **full regression is mandatory** |
| Edit the tool description | Wrong tool choice, wrong parameters, hallucinated tools | Cheap and narrow: only trajectories that use that tool are touched |
| Swap the model | Capability failures: several modes running high at once, nothing else moves them | Most expensive: the judge is fully recalibrated (ch5 expiry discipline), and ch14 change tiers put you on the largest suite |
| Add a confirmation gate (a row in the permission matrix) | Irreversible actions: duplicate refunds, unauthorized execution | Doesn't lower the error rate, lowers the harm; the price is human confirmation volume |
| Edit the handoff contract | Multi-agent context loss, reviewing off a summary | Medium; only the subagent path is touched |
| Fix the memory policy | Crosstalk, misremembering, cross-session contradictions | Medium; must be verified with multi-session replay |
| Fix the knowledge base or retrieved content | Grounding failures: the policy document itself is wrong or stale, the agent cites it correctly and answers entirely wrong | Cheap; touches every trajectory citing that content, and triggers gold-label relabeling (ch4 expiry policy) |

Capability failures no lever reaches -> the gate: the harm is shut behind human confirmation, the bottleneck can wait, the harm cannot.

> Fine-tuning is not in the table: this book does not teach how to build agents (boundary declaration in the Decisions & Principles internal design doc); if you really do fine-tune, handle it as a ch14 tier-3 change, judge fully recalibrated + the largest suite.

## "Handy != on target" self-check

- [ ] Was this lever chosen by **evidence**, or by **habit**? (The handiest lever for any team is always editing the prompt, and using it to fix a wrong tool choice is like fixing one broken door with the building-wide PA system)
- [ ] Two suspected components and both plausible? -> Write both as falsifiable hypotheses, try the smaller blast radius first
- [ ] Did this cycle move only one lever?

## This cycle's selection record

- Failure mode: ____  Candidate levers: ____  Chosen: ____  Evidence: ____
