# Change-Tier Matrix (Chapter 14)

> Note: three change tiers, tier 1 (local) / tier 2 (behavioral) / tier 3 (foundational). A vendor upgrade email is a change too. Fallback discipline: **when unsure, tier up**.

## Tier matrix

| Tier | Change type | Suite that must run | Recalibration triggered |
|---|---|---|---|
| Tier 1 (local) |  | replay-layer subset + affected cases | none |
| Tier 2 (behavioral) |  | full simulation with intervals + red-line set | as needed (if the rubric moved, recalibrate the related judge) |
| Tier 3 (foundational) | **vendor model swap** (incl. vendor upgrade email) | full simulation with intervals + red-line and attack sets rerun, **no sampling** | all judges recalibrated (rerun judge-vs-human alignment, ch5 validity discipline) |
| Tier 3 (foundational) | **policy change** | affected cases relabeled, then full rerun (ch4 label-expiry process) | recalibrate if the change touches a rubric |
| Fallback | any change you are unsure of | **tier up** | tier up |

## Pending-tier register

| Date | Change description | Tier | Basis | Suite run? | Signature |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## Reminders

- Recovery after a stop = rerun as a tier-3 change (see the Stop Rule Decision Sheet).
- "A one-line prompt patch" is not demoted for being small; the harmless-patch relapse dies before merge because the replay layer keeps running.
