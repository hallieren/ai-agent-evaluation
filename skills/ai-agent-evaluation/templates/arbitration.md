# Arbitration Protocol

Source: repo/templates/ch05/arbitration-protocol.md (the repo holds the latest version; on conflict the repo wins).
Use when: an assertion and a judge disagree, a verdict came back `unclear`, or a spot check found a judge-human disagreement.

> Note: the human is the scarce resource at the top of the ladder, doing only arbitration, spot checks, and gold labels. This sheet fixes what enters arbitration, who rules, and where the ruling lands.

## What enters arbitration

- [ ] Cases where an assertion and a judge conflict
- [ ] Cases with verdict `unclear`
- [ ] Judge-human disagreements found in spot checks

## Who rules

- Arbiter = **spec owner** (the real name on the "spec" row of the RACI table, see `templates/ownership-raci.md`): `________`
- Escalation path for disputes (when the owner cannot decide either): `________`

## Where the ruling lands (three exits, pick at least one)

| Exit | Action |
|---|---|
| gold label wrong | Fix the gold label, register it in the label expiry policy's relabeling flow (`templates/label-expiry.md`) |
| rubric / assertion ambiguous | Fix the rubric or the assertion criterion, written back as an operational definition; the judge calibration report is void, rerun it |
| the verdict itself overturned | Rewrite the verdict record, `judged_by: human` |

## Arbitration log

| Date | case_id | Conflict (who vs who) | Ruling | Exit | Signature |
|---|---|---|---|---|---|
| *e.g. 2026-09-11* | *<case-id>* | *`judge-tone-commitment` pass vs human concern* | *"a completed tense counts as a commitment"* | *rubric ambiguous* | *<owner>* |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

Filled in → goes to: the gold label (exit 1), the rubric or assertion criterion plus a rerun of `templates/judge-validation-report.md` (exit 2), or the verdict record (exit 3).
