# Judge Validation Report

Source: repo/templates/ch05/judge-validation-report.md (the repo holds the latest version; on conflict the repo wins).
Use when: putting a judge on duty for the first time, or after any judge-prompt edit or base-model swap (the previous report is void).

> Note: the calibration report a judge needs before going on duty, one per judge. Validity is not permanent: the moment the prompt or the base model changes, the report is void, rerun it.

- Judge name: `judge-________`  Version / base model: `________`  Report date: `________`

## 1. Alignment set composition (stratified by severity and failure mode)

The alignment set enriches sev-1 by hand, at a density far above the natural distribution (the same idea as seeded-error probes, see `templates/side-effect-audit.md`). State the estimand: an enriched-layer rate is a capability reading on a constructed distribution, not a production miss rate.

| Layer | Failure mode | Count |
|---|---|---|
| sev-1 |  |  |
| sev-2 |  |  |
| sev-3 |  |  |

Alignment-set split: tuning half `____` cases / reporting half `____` cases; example case_ids that entered the prompt: `____` (removed from both halves).

## 2. Judge-human disagreement rate, layered

| severity layer | Count | Disagreements | Disagreement rate | human-human anchor |
|---|---|---|---|---|
| sev-1 |  |  |  |  |
| sev-2 |  |  |  |  |
| sev-3 |  |  |  |  |

Reading precision ≈ ±1/√(count); a single-digit layer is read case by case, not as a rate.

False passes (the fixed line, the complement of per-class recall): humans labeled `________` cases unsafe/concern, the judge caught `________`.

False fails (the fixed line): humans labeled `________` cases pass, the judge failed `________`.

Investigation judges (e.g. `judge-report-rubric`) also layer by rubric dimension:

| rubric dimension | Disagreement rate |
|---|---|
|  |  |

## 3. Disagreement triage log

| case_id | Judge verdict | Human verdict | Cause (judge wrong / gold wrong / rubric ambiguous / gold stale) | Disposition |
|---|---|---|---|---|
|  |  |  |  |  |

## 4. On-duty / recall conclusion

- Bar (anchored to human-human agreement, false passes and false fails read separately): sev-3 goes on duty when it nears the ceiling; sev-2 goes on duty only after every disagreement sample is triaged; sev-1 has no threshold, only the authority rule (the judge can only ever escalate).
- Conclusion: ☐ on duty ☐ recalled  Signature: `________`

## 5. Validity statement

This report is valid only for judge prompt version `____` and base model `____`; a change to either voids it, rerun (change tiers: a model swap triggers judge recalibration, see `templates/change-tiers.md`).

Filled in → goes to: the judge's calibration record next to its prompt version; the on-duty conclusion gates whether `judged_by: judge-<name>` verdicts may enter a report.
