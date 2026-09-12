# Failure mining protocol

Source: repo/templates/ch15/failure-mining-protocol.md (the repo holds the latest version; on conflict the repo wins).
Use when: production traces must be pooled, sampled, coded, and folded into the failure mode atlas.

> Note: the industrialized version of offline error analysis on production data. The goal is the structure of failure, not a census of failure, so a pool with false positives and leaks is fine.

## 1. Failure-pool signal list (production "suspected failure" is defined by online signals)

- [ ] escalation (handoff to a human)
- [ ] negative user feedback and restatement
- [ ] assertion hits (online red line)
- [ ] judge escalation
- [ ] the cost tail over budget
- [ ] (your own) ____

## 2. Stratified sampling rules

- [ ] **Never sample in proportion to traffic** (lookup-type tasks drown the batch)
- [ ] Stratify by signal severity and task type
- [ ] **sev-1 signals all enter the pool**, never sampled
- [ ] Read the saturation curve separately per task type, stop at saturation
- [ ] Keep a random slice of ____% outside the pool (no signal filter at all; the modes the signals cannot see surface only here; about a fifth, illustrative)

| Stratum (signal × task type) | In pool | Sampled |
|---|---|---|
| *e.g. overturn × action-type* | *__* | *__* |
|  |  |  |

## 3. Coding and clustering steps

1. Read every trace by hand, code it with the Trace Review Form (templates/trace-review.md: verdict / `first_bad_step` / behavioral description / severity / suspected component)
2. Code blind, all four coding disciplines still apply (dirty data gets no exemption)
3. Cluster, name behaviorally (a script may pre-sort piles; a person writes the name and the criterion)

## 4. Atlas extension format (six-column row structure)

| Name (behavioral verb phrase) | Definition and criterion | Representative trace IDs | Count | sev distribution | Suspected component |
|---|---|---|---|---|---|
| *e.g. fuzzy-searches by name with the order ID in hand* | *order ID present in the prompt and a `search_orders` call in the trace* |  |  |  |  |
|  |  |  |  |  |  |

Once extended: a new sev-1 mode -> a red-line case; the suspected component -> look up templates/lever-mapping.md, write the falsifiable hypothesis.

Filled in → goes to: templates/failure-mode-atlas.md (new rows and updated counts) and the target-mode field of templates/improvement-cycle.md.
