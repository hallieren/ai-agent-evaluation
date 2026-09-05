# Failure Mining Protocol (Chapter 15)

> Note: the industrialized version of ch3's error analysis on production data. Mining wants the structure of failure, not a census of failure, so a pool with false positives and leaks is fine.

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

| Stratum (signal × task type) | In pool | Sampled |
|---|---|---|
|  |  |  |

## 3. Coding and clustering steps (following ch3)

1. Read every trace by hand, code it with the Trace Review Form (verdict / `first_bad_step` / behavioral description / severity / suspected component)
2. Code blind, all four coding disciplines still apply (dirty data gets no exemption)
3. Cluster, name behaviorally

## 4. Atlas extension format (six-column row structure, following Chapter 3)

| Name (behavioral verb phrase) | Definition and criterion | Representative trace IDs | Count | sev distribution | Suspected component |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Once extended: a new sev-1 mode -> a red-line case; the suspected component -> look up the bottleneck-to-lever mapping, write the falsifiable hypothesis.
