# Coverage Matrix Template

Source: repo/templates/ch04/coverage-matrix.md (the repo holds the latest version; on conflict the repo wins).
Use when: reviewing an eval set's structure (before trusting any count of cases), and every time the eval set changes; generate the counts with `python scripts/coverage.py <cases-dir>`.

> Note: three-dimensional coverage, failure mode × severity × user type. An empty cell is not a sin, an unsigned one is. Rule every empty cell "fill" or "reasoned empty" and log it in the annotation bar.

## Matrix (one row per failure mode, counts spread by persona)

persona: `cooperative / angry / vague / multi` (the support world's axis; redesign the persona axis around your own failure mechanisms, e.g. contract type × jurisdiction × leverage, or repo size × change type × coverage state)

| Failure mode | sev | cooperative | angry | vague | multi | Total |
|---|---|---|---|---|---|---|
| *e.g. unauthorized-commitment* | *sev-1* | *6* | *5* | *1* | *0* | *12* |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

## Coverage self-check

- [ ] All sev-1 rows non-zero (every high-risk mode needs a sentry standing)
- [ ] Every cell either holds a case or appears in the annotation bar below
- [ ] Every atlas mode appears as a row (a mode missing as an entire row is louder than any empty cell; check against templates/failure-mode-atlas.md)
- [ ] Every non-empty stratum holds at least one non-synthetic anchor

## Allowed empties and reasons (annotation bar; empty cells require signatures)

| Empty cell (mode × persona) | Ruling (fill / reasoned empty) | Reason | Signature |
|---|---|---|---|
| *e.g. missed-request-item × cooperative* | *reasoned empty* | *the dropping mechanism needs concurrent multi-requests; a single-request persona has nothing to drop* | *spec owner* |
|  |  |  |  |

Filled in → goes to: the eval set review record; "fill" rulings become new cases via templates/golden-task.md; the two counts (non-empty cells, cases in sev-1 rows) into the eval report.
