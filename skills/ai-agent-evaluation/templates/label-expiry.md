# Label Expiry Policy

Source: repo/templates/ch04/label-expiry-policy.md (the repo holds the latest version; on conflict the repo wins).
Use when: landing any case (register its basis), whenever a policy or rules line changes (relabel before the change counts as done), and on a periodic audit schedule.

> Note: labels depend on policy, policy changes, labels rot. Three pieces: basis registration, change-triggered relabeling, periodic audits. Expiry is silent: the eval still runs and the report still prints, only the gold is wrong, the same way on every case.

## 1. Policy basis register

| case_id | Policy line depended on (location in the policy ledger) | gold label / assertions | Registered on |
|---|---|---|---|
| *<case-id>* | *refund authority line: single refund ≤ <limit> auto, above needs human approval* | *`no_over_limit_commitment`, sev-1* | *<date>* |
|  |  |  |  |

## 2. Change-triggered relabeling flow

When a policy change happens (including external changes such as a supplier or vendor update; see templates/change-tiers.md):

1. Run the policy diff against the basis register, list the affected cases:
2. Relabel case by case (update expect / severity_if_fail / gold label), record the edits:
3. Re-run all affected cases, mark the report "post-relabel":
4. Signature: `________`  Date: `________`

The change does not count as complete until step 4 is signed.

## 3. Periodic audit checklist (quarterly suggested)

- [ ] Sample N cases, verify case by case that the policy each depends on is still current
- [ ] Deliberately include cases that have never failed (a strong agent, or a case that died long ago?) and cases that have never passed (a weak agent, or an unsolvable task? clear the reference trajectory before concluding)
- [ ] Any case missing from the basis register (step 6 of templates/golden-task.md skipped when a new case landed)?
- [ ] Has the input distribution drifted out of the coverage matrix (cross-check the drift probes in references/going-live.md; this policy covers "policy changed, labels rotted", drift probes cover "inputs changed, coverage leaks")

Filled in → goes to: the basis register (kept beside the eval set); the affected-case list and the post-relabel report into the release record (templates/release-gate.md).
