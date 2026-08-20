# Failure Mode Atlas Starter (Chapter 3)

> Note: the atlas is a living document, not a deliverable. One mode per row, all six columns filled; write a question mark where the suspected component is unclear, a question mark is honest and a blank is the dodge. Appendix D's full taxonomy, look after clustering, not before.

## Atlas table (row structure reused book-wide; Chapter 15 failure mining extends this)

| Name (behavioral verb phrase) | Definition and criterion (what counts as a hit) | Representative trace IDs | Count | sev distribution | Suspected component |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## Behavioral-naming self-check

- [ ] Can this name make someone who has not read the traces imagine the failure? (good: "hearsay taken as fact," "fabricating an identifier"; bad: "understanding problem," "quality problem," the junk drawer)
- [ ] Is "definition and criterion" stated to the point of being decidable? When the next trace arrives you can clearly answer hit / no-hit; if not, split or merge.
- [ ] For every sev-1 mode, is at least one case in the red-line set?

## Ordering criterion

Frequency × severity, **severity first**, a low-frequency sev-1 ranks ahead of a high-frequency sev-3.
