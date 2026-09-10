# Golden Task Design Protocol (Chapter 4)

> Note: the seven-step flow for reverse-generating cases from the failure mode atlas, one check question per step. The output lands directly on the case schema (YAML).

| Step | Action | Check question | This case's answer |
|---|---|---|---|
| 1 | Pick the failure mode | Which atlas row? What sev? |  |
| 2 | Design the setup (sandbox seed) | Are right and wrong pressed into a checkable end state? Is the "world state" written out in full? |  |
| 3 | Pick the persona, write the prompt | `cooperative / angry / vague / multi`, which one? Does it read like a real user? |  |
| 4 | Write the expect (assertions first, judge only where they cannot decide) | Has everything an assertion can decide been sunk down? Is the judge reserved for "language only" territory? |  |
| 5 | Set severity_if_fail | Consistent with the severity table? Does sev-1 have a deterministic sentry? |  |
| 6 | Register the policy basis | Which policy does the label depend on? Is it in the policy basis register? |  |
| 7 | Clear the reference trajectory (zero model calls) | One hand-written or harvested trajectory that passes: every assertion green, judge rules hit? Where is the proof the task is solvable? |  |

## YAML landing self-check

- [ ] `id` / `type` (query|action|investigate) / `persona` / `prompt` / `setup` / `expect.assertions` / `expect.judge` (optional) / `severity_if_fail` / `failure_modes` all present
- [ ] Reference trajectory cleared: if no passing trajectory can be written, go back to step 2 or step 4, do not land the case
- [ ] Synthetic distortion check: do several same-persona cases read as the same anger / the same vagueness? Rewrite them yourself
