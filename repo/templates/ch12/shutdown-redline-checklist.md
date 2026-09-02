# Shutdown Red-Line Checklist (Chapter 12)

> Note: which security failures = shut down immediately, ticked and written down in advance. This checklist is the **security branch** of the Chapter 14 Stop Rule decision sheet, folded into it as is, not a second document.

## Immediate-shutdown red lines (tick the ones in force; add rows)

- [ ] Any red-line action that breaches every layer (an over-limit refund goes through, order details leak out)
- [ ] Any cross-session harm caused by contaminated memory
- [ ] Any instruction injected into the main agent that a subagent executes
- [ ] (candidate) The same class of attack recurs after a fix
- [ ] (candidate) The agent bypasses human confirmation on a red-line action
- [ ] (your own) `________`

## Register per red line

| Red line | Detection (online assertion / monitoring signal) | Pause level (see the ch14 three pause levels) | Owner |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

## Discipline

- A breaching attack sample goes straight onto this checklist + into `cases/attacks`.
- Shutdown is not the end: recovery reruns per the ch14 tier-3 change (full simulation with intervals + judge recalibration + red-line and attack sets rerun).
