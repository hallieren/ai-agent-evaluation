# Quality Ownership RACI

Source: repo/templates/ch16/quality-ownership-raci.md (the repo holds the latest version; on conflict the repo wins).
Use when: the team has grown past a handful of people and each quality asset needs one name, or a compliance domain requires formal governance.

> Note: fill the ownership table with **real names** and put it on the repo's front page. Four rows to start; at 3 people it keeps "common property" from turning into "nobody's property", at 15 people it is the foundation of governance.

## Ownership table (four rows to start)

R = responsible for doing it, A = accountable for the final call (exactly one A per row, a person, never a department), C = must be consulted, I = must be informed

| Asset | R | A (a real name, one) | C | I |
|---|---|---|---|---|
| The spec (Intended Use & Action Boundary Sheet, including the permission matrix) |  |  |  |  |
| Gold labels (the eval set and relabeling) |  |  |  |  |
| The judge rubric (including the calibration report's expiry) |  |  |  |  |
| The red-line veto (sev-1 assertions and the shutdown red lines, one person can veto a release; no meeting, no vote) |  |  |  |  |
| *e.g. the harness and verdict implementations (engineering)* |  |  |  |  |
|  |  |  |  |  |

## Guidance for promoting this into formal governance

Once the team passes ____ people or enters a strict compliance domain:

- [ ] Changes go through approval: a tier-3 change needs the A's signature, and the record is kept
- [ ] Decisions are auditable: arbitration records, escalation signature columns, and gate interception records are archived periodically
- [ ] Guard against two systems: a paper RACI to satisfy the audit while the real habits go their own way is the most common failure; the way to check is to go through the records (see templates/culture-health-check.md), not to ask how it feels
- [ ] Owner departure / rotation process: the handover pack = this table + every template and record for that row's asset
- [ ] In a credentialed domain, the A for gold labels holds the domain credential

Filled in → goes to: the repo's front page (README), and the approval signature on every tier-3 change record.
