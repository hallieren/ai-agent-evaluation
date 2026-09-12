# Deforming the method for high-stakes domains

**Load this reference when:** the agent acts in healthcare, finance, or legal work; experts disagree about what "correct" is; an action cannot be undone by anyone; a regulator, auditor, committee, or opposing counsel will read the evidence; traces cannot leave a data boundary; a judge model's compliance status is unclear.
Source: appendix C, docs/appendices/appendix-c-high-stakes.md

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Keep the same method; deform it only where three general assumptions fail. Why: the assumptions are that ground truth is trustworthy, that harm is containable, and that evidence is written for yourself, and each failing assumption changes a specific part of the practice, not the whole.
- Measure human–human agreement before any eval set goes to production. Why: it is at once the ceiling for judge calibration and the confidence statement for the gold labels, and low agreement is a property of the domain, not a failed process.
- Let regulation and scope of practice draw the forbidden / needs-confirmation columns. Why: the team no longer decides them, and the confirmer must be qualified with the confirmation itself archived.
- Promote seeded-error probes to primary evidence. Why: a sandbox can manufacture neither patients nor markets.
- Make silent/shadow mandatory for any action whose rollback cell is empty. Why: a dispensed prescription or a wrong transfer has no undo.
- Stop on a single sev-1. Why: the operational trigger "≥ 1 per week" is for recoverable domains only.
- Shape the evidence for its audience from the start. Why: translating after the fact loses the trail, and the audience decides the shape.
- Send the judge in; never send the data out. Why: only the verdict record crosses the boundary, and verdict sinking is what allows an evaluation system to exist at all.
- Decide judge eligibility by compliance agreement, not capability. Why: a model not covered by the agreement judges only de-identified data or does not judge.
- Treat de-identification as re-identification risk management. Why: masking names leaves rare-feature combinations, and a multi-step trace accumulates quasi-identifiers in tool arguments, retrieval results, and reasoning.

## Procedure

1. **Establish ground truth confidence.** Have two or more domain experts blind-label the same batch; compute human–human agreement (kappa; physicians on a diagnosis often land at 0.4–0.7, illustrative of the domain). Record it as the judge-calibration ceiling.
2. **Handle low agreement three ways**: move gold labels from single-annotator to multi-expert plus an arbitration record (templates/arbitration.md); enter contested cases into the set together with the point of contention; add a "ground truth confidence" layer to the report, with low-confidence dimensions marked reference-only and kept out of the gate.
3. **Rebuild the permission matrix under regulation** (templates/permission-matrix.md): forbidden and needs-confirmation columns from regulation and scope of practice; confirmer named with credentials; each confirmation archived.
4. **Build the seeded-error library** as the core asset: drug interactions, dose limits, transfer limits, changed payee accounts, privileged recipients. Run it as primary evidence, not a supplement.
5. **Mark every empty rollback cell** and promote those actions: shadow mandatory on the evidence ladder (templates/evidence-ladder.md), and the stop rule's safety branch tightened to a single sev-1 (templates/stop-rule.md).
6. **Version and archive** the eval set, the judge validation report, the gate records, and `judged_by` on every verdict, reproducible on rerun; this is the audit trail.
7. **Write the prospective validation plan** for the clinical or risk committee directly from the ladder and gate outputs: which rungs, which signals per rung, what stops the climb.
8. **Write every record to the standard "opposing counsel will read every line"**; connect the blameless postmortem (templates/postmortem.md) with legal review, because the trace is also an exhibit.
9. **Deploy the judge inside the boundary**; export only `{verdict, severity, failure_mode}`; run assertions and deterministic checks inside by default; push every verdict as far down the ladder as it goes.
10. **Pre-check any vendor model swap for compliance** (BAA-type agreement in healthcare, residency and confidentiality clauses in finance, privilege review in legal) before the tier-3 recalibration starts (see references/gating-releases.md).
11. **Staff annotation from in-boundary experts** with access; plan for scarcity one order of magnitude worse than usual.
12. **Substitute for verification lag** with expert spot checks, assertion-type leading indicators, and longer rung dwell times (see references/going-live.md).

## Decisions

1. **Which deformation applies** to a given design question: contested truth → agreement, arbitration, confidence layer; irreversible harm → regulated matrix, seeded probes primary, mandatory shadow, single-sev-1 stop; external audience → audit trail, prospective plan, exhibit-grade records.
2. **Whether a judge may see the data**: covered by the compliance agreement → judge inside the boundary on raw traces; not covered → de-identified data only, or no judging role.
3. **Whether a verdict may leave the boundary**: assertion or deterministic verdict → the record leaves; judge verdict → the record leaves, the text does not; human label → stays with the in-boundary expert, only the label leaves.

## Frameworks

**Three failing assumptions.**

| Assumption | Where it fails (healthcare / finance / legal) | What changes in the method |
|---|---|---|
| Ground truth is trustworthy | Physician agreement on a diagnosis often 0.4–0.7 kappa; compliance shifts with regulatory interpretation; legal conclusions have an adversary by nature | Agreement before everything; multi-expert labels with arbitration; contested cases kept with their contention; a ground-truth-confidence layer, low-confidence dimensions out of the gate |
| Harm is containable | A wrong drug goes into the patient; a wrong transfer is money gone plus penalties; a privileged email to the wrong recipient waives privilege | Matrix columns drawn by regulation with a qualified, archived confirmer; seeded-error probes as primary evidence; shadow mandatory where rollback is empty; single sev-1 stops the agent |
| Evidence is written for yourself | Regulators and auditors want an audit trail; clinical committees want a prospective validation plan; opposing counsel reads discovery | `judged_by` becomes a compliance asset; eval set, judge report, gate records versioned and reproducible; interval discipline as defense material; ladder and gate outputs serve the committee unchanged; postmortems joined to legal review |

**Imprisoned-data architecture.** Judge inside the boundary; only the verdict record crosses (verdict, severity, failure_mode), no raw text. BAA-aware judge: eligibility is a compliance question, and a vendor model swap gains a compliance pre-check before recalibration. De-identification widens what may leave; it never replaces the in-boundary judge. Annotators inside too: expert annotation is the only compliant option, not the best-quality one. A self-built harness deployable inside the boundary rises in value; the data boundary is also an attack target, so the defense line and the compliance boundary coincide.

**Three domains at a glance.**

| Domain | Data constraint | Who confirms an irreversible action | Core seeded-error probes | Evidence audience |
|---|---|---|---|---|
| Healthcare | PHI stays inside; BAA-type agreement decides the judge | A licensed clinician, confirmation archived | Drug interactions, dose limits, wrong-patient lookups | Regulator, clinical committee (prospective validation plan), ethics review for canary assignment |
| Finance | Data residency and confidentiality clauses; the judge passes the same border review | A compliance officer with signing authority | Transfer limits, changed payee accounts, duplicate transfers | Auditor and regulator (the trail is the defense) |
| Legal | Privileged material never leaves; the eval process survives privilege review | Counsel of record | Privileged recipient, overreach of authority, a citation that does not resolve | Opposing counsel in discovery (records as exhibits) |

**Verdict flow across the boundary.**

| Verdict source | Runs where | What crosses |
|---|---|---|
| Assertion / deterministic check | Inside, by nature | The verdict record |
| Calibrated judge | Inside (compliant environment) | `verdict, severity, failure_mode`; no raw text |
| Human expert | Inside, credentialed, with access | The label and the arbitration record |

**Regulatory alignment (directional, not legal advice).** Logging-retention and post-market monitoring obligations for high-risk systems line up with trace archiving, the evidence ladder, and online monitoring; predetermined change-control plans in medical software regulation are isomorphic to change tiers. A practitioner with this practice faces those requirements missing only a mapping table.

## Self-check

- The sentence: "We de-identified it, so the traces can go out for judging."
- The reality: de-identification is re-identification risk management, and a multi-step trace leaks quasi-identifiers from arguments, retrievals, and reasoning.
- The check: name the environment the judge runs in and list every field that crosses the boundary; anything beyond verdict, severity, and failure_mode needs the compliance agreement's signature.

## Templates

- `templates/permission-matrix.md` — the regulated forbidden / needs-confirmation columns with a credentialed confirmer.
- `templates/arbitration.md` — the multi-expert arbitration record behind contested gold labels.
- `templates/evidence-ladder.md` — shadow marked mandatory for every empty rollback cell.
- `templates/stop-rule.md` — the safety branch tightened to a single sev-1.
- `templates/ownership-raci.md` — the formal RACI with a credentialed Accountable for gold labels.

## Migration notes

- Healthcare: PHI stays inside; BAA decides the judge; the confirmer is a licensed clinician; canary assignment is an ethics-review decision; every rung's evidence archived for the regulator.
- Finance: data residency and confidentiality clauses gate the judge; the audit trail is the defense; a single wrong transfer is sev-1 with penalties following; changed-payee and transfer-limit probes are core.
- Legal: privileged material never leaves; the eval process must survive privilege review; records are written as exhibits; gold labels are established through argument, not annotation alone.
- General teams: apply the same order for any action whose rollback column is empty (silent first, canary second, evidence written at every rung), and treat `judged_by` as an asset today so it is a compliance asset later.
