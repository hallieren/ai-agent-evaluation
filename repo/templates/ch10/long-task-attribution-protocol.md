# Long-Task Attribution Protocol (Chapter 10)

> Note: for long-horizon failures (the step-40 error rooted at step 6), trace back along the write chain, looping the step card until the first bad write. Cloudrest 2 three-day investigation: first bad write = day one's note-writing step.

## Step card (loop, one card per round)

**Round `________`**

1. Wrong statement (which session/step, verbatim):
2. The memory entry it cites (`memory_write` content):
3. That entry's write point (session #/step #):
4. Did the information at the write point support this write?
   - ☐ Yes → another citation remains upstream; return to 1 and keep tracing
   - ☐ No → **first bad write found**: session `________` step `________`

## Attribution conclusion

- first bad write: session `________` step `________`
- Write content and contamination path (which later retrievals/conclusions it contaminated):
- Repair pointer (memory policy / write audit / isolation; maps to the ch15 lever "fix the memory policy"):

## Checkpoint-siting checklist

Where the long task sets checkpoints (reconciling written memory against world facts):

- [ ] Daily close / phase close: `________`
- [ ] After a high-risk write (when a conclusion-shaped statement goes into the notes)
- [ ] Before citing external/secondhand information as a premise (verify "the customer says they all leak" before treating it as fact)
- [ ] Session end: memory audit, every entry traceable
