# Shutdown Red-Line Checklist

Source: repo/templates/ch12/shutdown-redline-checklist.md (the repo holds the latest version; on conflict the repo wins).
Use when: deciding in advance which security failures stop the agent immediately; revisit after every red-team round and every breach.

> Note: which security failures = shut down immediately, ticked and written down in advance. This checklist is the **security branch** of the Stop Rule decision sheet (templates/stop-rule.md), folded into it as is, not a second document.

## Immediate-shutdown red lines (tick the ones in force; add rows)

- [ ] Any red-line action that breaches every layer (an over-<limit> refund goes through, order details leak out)
- [ ] Any cross-session harm caused by contaminated memory
- [ ] Any instruction injected into the main agent that a subagent executes
- [ ] (candidate) The same class of attack recurs after a fix
- [ ] (candidate) The agent bypasses human confirmation on a red-line action
- [ ] (your own) `________`

## Register per red line

| Red line | Detection (online assertion / monitoring signal) | Pause level (see the three pause levels in templates/stop-rule.md) | Owner |
|---|---|---|---|
| *example: over-<limit> refund executed after breaching every layer* | *`refund_not_executed` online + side-effect audit* | *full stop* | *`________`* |
|  |  |  |  |

## Discipline

- A breaching attack sample goes straight onto this checklist + into `cases/attacks`.
- Shutdown is not the end: recovery reruns per a tier-3 change (full simulation with intervals + judge recalibration + red-line and attack sets rerun; see templates/change-tiers.md).

Filled in → goes to: the stop rule decision sheet (its security branch) and the monitoring signal spec for each detection line.
