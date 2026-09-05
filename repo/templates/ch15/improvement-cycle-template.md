# Improvement Cycle Template (Chapter 15)

> Note: one page per cycle. The rejection rule is written before the run; set the standard after the run and any result can be called "fixed".

## Cycle #____ (dates ____ to ____)

### Target mode

- Atlas row: ____ (count ____, sev ____)

### Experimental hypothesis (falsifiable form)

- "____ fails because of ____ in the ____ component; change it and the target mode's count should drop from ____ to ____."

### Lever moved (only one allowed)

- ☐ edit the prompt ☐ edit the tool description ☐ swap the model ☐ add a confirmation gate ☐ edit the handoff contract ☐ fix the memory policy
- The change itself:

### Pre-written rejection rule (signed before the run)

- The target mode's count has to drop to: ____ (paired, `--repeat` 5 passes, with intervals, how the interval is computed: ____)
- Full-regression gate line (by sev tier): ____
- What result counts as failure: ____
- Signature: ____  Date: ____

### Two-part verification result (one part short doesn't count)

1. **Did it get fixed?** Target mode's count (paired ± interval, not the overall pass rate):
2. **Did it break anything else?** Full regression by sev tier:

- Conclusion: ☐ keep it, in effect ☐ roll back and try the next hypothesis (a normal step in the cycle, not a setback)

### Next cycle's candidates

- Mode: ____  Basis (failure-pool signal): ____
