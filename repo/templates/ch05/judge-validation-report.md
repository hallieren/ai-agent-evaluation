# Judge Validation Report Template (Chapter 5)

> Note: the calibration report a judge needs before going on duty, one per judge. Validity is not permanent: the moment the prompt or the base model changes, the report is void, rerun it.

- Judge name: `judge-________`  Version / base model: `________`  Report date: `________`

## 1. Alignment set composition (stratified by severity and failure mode)

The alignment set enriches sev-1 by hand, at a density far above the natural distribution (the same idea as the ch8 seeded-error probes).

| Layer | Failure mode | Count |
|---|---|---|
| sev-1 |  |  |
| sev-2 |  |  |
| sev-3 |  |  |

## 2. Judge-human disagreement rate, layered

| severity layer | Count | Disagreements | Disagreement rate | human-human anchor |
|---|---|---|---|---|
| sev-1 |  |  |  |  |
| sev-2 |  |  |  |  |
| sev-3 |  |  |  |  |

Per-class recall (the fixed line): humans labeled `________` cases unsafe/concern, the judge caught `________`.

Investigation judges (`judge-report-rubric`) also layer by rubric dimension:

| rubric dimension | Disagreement rate |
|---|---|
|  |  |

## 3. Disagreement triage log

| case_id | Judge verdict | Human verdict | Cause (judge wrong / gold wrong / rubric ambiguous) | Disposition |
|---|---|---|---|---|
|  |  |  |  |  |

## 4. On-duty / recall conclusion

- Bar (anchored to human-human agreement): sev-3 goes on duty when it nears the ceiling; sev-2 goes on duty only after every disagreement sample is triaged; sev-1 has no threshold, only the authority rule (the judge can only ever escalate).
- Conclusion: ☐ on duty ☐ recalled  Signature: `________`

## 5. Validity statement

This report is valid only for judge prompt version `____` and base model `____`; a change to either voids it, rerun (ch14 change tiers: a model swap triggers judge recalibration).
