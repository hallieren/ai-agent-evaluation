# Failure Mode Atlas Starter

Source: repo/templates/ch03/failure-mode-atlas-starter.md (the repo holds the latest version; on conflict the repo wins).
Use when: clustering coded trace rows into named failure modes, and whenever a capability unlock or a production distribution change owes the atlas another round of coding.
Living file: later work writes back into this file (every capability unlock and distribution change adds incremental rows; failure mining on production data, templates/failure-mining.md, extends it; the eval set and judge calibration read from it).

> Note: the atlas is a living document, not a deliverable. One mode per row, all six columns filled; write a question mark where the suspected component is unclear, a question mark is honest and a blank is the dodge. The full reference taxonomy (references/failure-taxonomy.md): look after clustering, not before.

## Atlas table (row structure reused book-wide; failure mining extends this)

| Name (behavioral verb phrase) | Definition and criterion (what counts as a hit) | Representative trace IDs | Count | sev distribution | Suspected component |
|---|---|---|---|---|---|
| *e.g. hearsay taken as fact* | *a spoken claim written into the premise as verified fact; every later search hunts evidence for it* | *<trace-ids>* | *3* | *sev-1 × 3* | *prompt (premise does not distinguish claim / verified)?* |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

Near miss = the line was crossed but the consequence never landed; verdict `concern`, no sev tier; count it in the sev distribution column as "near miss × n".

## Behavioral-naming self-check

- [ ] Can this name make someone who has not read the traces imagine the failure? (good: "hearsay taken as fact," "fabricating an identifier"; bad: "understanding problem," "quality problem," the junk drawer)
- [ ] Is "definition and criterion" stated to the point of being decidable? When the next trace arrives you can clearly answer hit / no-hit; if not, split or merge.
- [ ] After reading a representative trace, can you say at a glance where the agent went wrong and why it counts as wrong? If not, suspect the criterion first; failures should seem fair.
- [ ] For every sev-1 mode, is at least one case in the red-line set?

## Ordering criterion

Frequency × severity, **severity first**, a low-frequency sev-1 ranks ahead of a high-frequency sev-3. Fix first the mode with high severity, high frequency, and a clear lever; a severe mode with an unclear lever goes onto a red-line case to watch and never leaves the atlas.

- Top-5 this cycle: 1. `____` 2. `____` 3. `____` 4. `____` 5. `____`
- This cycle fixes: `____` because `____`  Signature: `________`  Date: `________`

Filled in → goes to: reverse-generated cases in templates/golden-task.md and rows in templates/coverage-matrix.md; sev-1 rows into templates/redline-set.md; judge calibration focus (references/judging.md); the fix-first line into templates/improvement-cycle.md.
