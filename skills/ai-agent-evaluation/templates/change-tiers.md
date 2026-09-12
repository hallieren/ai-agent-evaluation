# Change-Tier Matrix

Source: repo/templates/ch14/change-tier-matrix.md (the repo holds the latest version; on conflict the repo wins).
Use when: any change is about to run the gate and its tier, mandatory suite, and recalibration must be decided first.

> Note: three change tiers, tier 1 (local) / tier 2 (behavioral) / tier 3 (foundational). A vendor upgrade email is a change too. Fallback discipline: **when unsure, tier up**.

## Tier matrix

| Tier | Change type | Suite that must run | Recalibration triggered |
|---|---|---|---|
| Tier 1 (local) | *e.g. a single tool description, an individual case fix, report wording* | replay-layer subset + affected cases | none |
| Tier 2 (behavioral) | *e.g. system prompt, planning / memory policy, adding or removing a tool, persona script, a gate threshold* | full simulation with intervals + red-line set | as needed (if the rubric moved, recalibrate the related judge) |
| Tier 3 (foundational) | **vendor model swap** (incl. vendor upgrade email; pin the version first, an alias counts as unpinned) | full simulation with intervals + red-line and attack sets rerun, **no sampling** + mandatory canary | all judges recalibrated (rerun judge-vs-human alignment) |
| Tier 3 (foundational) | **policy change** | affected cases relabeled, then full rerun (label-expiry process) | recalibrate if the change touches a rubric |
| Fallback | any change you are unsure of | **tier up** | tier up |

## Pending-tier register

| Date | Change description | Tier | Basis | Suite run? | Signature |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## Reminders

- Recovery after a stop = rerun as a tier-3 change (see templates/stop-rule.md).
- "A one-line prompt patch" is not demoted for being small; the harmless-patch relapse dies before merge because the replay layer keeps running.
- Calibrate this table against last month's merges: tier run vs tier the table says; the gap is your risk exposure.

Filled in → goes to: the pending-tier register kept with `ci/`, and the "Change tier" row of templates/go-no-go.md.
