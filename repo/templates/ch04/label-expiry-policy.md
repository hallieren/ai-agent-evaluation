# Label Expiry Policy (Chapter 4)

> Note: labels depend on policy, policy changes, labels rot. Three pieces: basis registration, change-triggered relabeling, periodic audits.

## 1. Policy basis register

| case_id | Policy line depended on (location in the policy ledger) | gold label / assertions | Registered on |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

## 2. Change-triggered relabeling flow

When a policy change happens (including external changes like a "supplier upgrade email", see ch14 change tiers):

1. Run the policy diff against the basis register, list the affected cases:
2. Relabel case by case (update expect / severity_if_fail / gold label), record the edits:
3. Re-run all affected cases, mark the report "post-relabel":
4. Signature: `________`  Date: `________`

## 3. Periodic audit checklist (quarterly suggested)

- [ ] Sample N cases, verify case by case that the policy each depends on is still current
- [ ] Any case missing from the basis register (step 6 skipped when a new case landed)?
- [ ] Has the input distribution drifted out of the coverage matrix (cross-check ch13 drift probes — the expiry policy covers "policy changed, labels rotted"; input drift covers "inputs changed, coverage leaks")
