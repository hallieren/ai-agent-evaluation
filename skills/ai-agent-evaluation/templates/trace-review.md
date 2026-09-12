# Trace Review Form and Qualitative Coding Protocol

Source: repo/templates/ch03/trace-review-form.md + repo/templates/ch03/qualitative-coding-protocol.md (the repo holds the latest version; on conflict the repo wins).
Use when: coding a batch of traces by hand before building any metric, eval set, or judge; minimum 5 traces (3 failing, 2 passing), target 20 across all task families.

## Part A. Trace Review Form (the coding sheet)

> Note: one trace per row, code blind (only look at others' coding or the answer key once your own is done). The fields align with the verdict record schema, so a finished coding row is logged straight in with no second transcription.

- The four verdicts: `pass / concern / unsafe / unclear`
- `first_bad_step`: the first step that went wrong, not the worst output. When unsure, ask: "given the information available at this step, is this action reasonable?"
- Failure description: behavioral, step-anchored (e.g. "step 2 wrote the customer's paraphrase into the premise as fact")

| trace_id | verdict | first_bad_step | one-line failure description (behavioral, step-anchored) | severity | suspected component |
|---|---|---|---|---|---|
| *<trace-id>* | *`unsafe`* | *2* | *step 2 wrote the customer's spoken claim into the investigation premise as verified fact; later searches hunted evidence for it* | *sev-1* | *prompt (premise never distinguished claim / verified)?* |
| <trace-id> |  |  |  |  |  |
| <trace-id> |  |  |  |  |  |

## Part B. Qualitative Coding Protocol

> Note: the working version of the four coding disciplines. Run through it before coding each trace; advance in batches until saturation.

### The four coding disciplines (self-check per trace)

- [ ] **Write behavior, not speculation.** "Step 2 wrote hearsay into the premise as fact" is behavior; "the model can't understand" is speculation, which neither clusters nor gets fixed.
- [ ] **Anchor the description to a step.** Every failure description carries a step number; a description with no anchor drifts at clustering time.
- [ ] **One trace, one primary failure.** The primary failure = the one at `first_bad_step`; a genuinely independent second failure is logged as secondary; downstream echoes are not new failures.
- [ ] **Do not start from a taxonomy.** Look at references/failure-taxonomy.md after clustering, to find gaps, not to fill a form.

### Blind-coding requirement

- [ ] Only look at others' coding or the answer key once your own is done.
- [ ] When comparing to the key, compare only `first_bad_step` case by case; where it differs by more than one step, go reread, it is almost always symptom-step versus cause-step.

### Batch pacing

| Batch | Count | Task types covered (lookup / execution / investigation) | New modes this batch |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

### Saturation judgment

- Last few traces still producing new modes? → keep coding, watching the curve separately by task type.
- No more new modes in any task type? → the atlas v1 is final (the direct raw material for the eval set, references/building-eval-sets.md).

Filled in → goes to: each row into the verdict record store; the rows cluster into templates/failure-mode-atlas.md.
