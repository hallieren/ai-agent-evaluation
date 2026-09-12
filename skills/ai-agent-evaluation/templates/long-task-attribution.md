# Long-Task Attribution Protocol

Source: repo/templates/ch10/long-task-attribution-protocol.md (the repo holds the latest version; on conflict the repo wins).
Use when: a failure cites a state produced earlier (another session, another day); find the first bad write and site checkpoints.

> Note: for long-horizon failures (the step-40 error rooted at step 6), trace back along the write chain, looping the step card until the first bad write (e.g. a three-day investigation whose first bad write is day one's note recording a customer's "they all leak" as fact).

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
- Repair pointer (memory policy / write audit / isolation; maps to the lever "fix the memory policy" in templates/lever-mapping.md):

## Checkpoint-siting checklist

Where the long task sets checkpoints (reconciling written memory against world facts):

- [ ] Daily close / phase close: `________`
- [ ] After a high-risk write (when a conclusion-shaped statement goes into the notes)
- [ ] Before citing external/secondhand information as a premise (verify "the customer says they all leak" before treating it as fact)
- [ ] Before an irreversible action: is the memory this action relies on still fresh?
- [ ] Session end: memory audit, every entry traceable

Filled in → goes to: the verdict record's `first_bad_step` (session + step) and the failure mode atlas; checkpoint sites go into the harness config.
