# Keeping the practice alive as the team grows

**Load this reference when:** the team has grown and habits are slipping; an incident or attempted attack needs a postmortem; a postmortem turned into a hearing; nobody owns the labels, the spec, or the red lines; several teams share one harness; someone says "we have eval infrastructure" as if that settled it; governance or an audit is coming.
Source: chapter 16, docs/chapters/ch16-eval-culture.md (templates: docs/appendices/ch16-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Write ownership down once the team passes a handful of people. Why: at 15 people, ownership that is not written down does not exist; "we'll handle it" no longer names anyone.
- Put the trace on the table before any postmortem discussion. Why: where facts are absent, positions fill in; the trace turns "whose fault" into one causal chain running through several owners' territory.
- Ask "which defense layer should have caught this and did not", never "who". Why: a postmortem examines the system, and people are not a defense layer.
- Give attempts a postmortem too. Why: an attack that got stopped may show that only one layer of the defense depth still works, and that is itself the incident.
- Point every action item at a piece of equipment, an owner, and a deadline. Why: "be more careful next time" clears nothing.
- Name one person per asset; a department name does not count. Why: "everyone is responsible together" translates inside an organization to "nobody is".
- Give the red-line veto to one name, no meeting, no vote. Why: on a sev-1 change, a decision that needs a meeting arrives after the harm.
- Let eval sets fork; never let sev semantics fork. Why: two teams with different meanings of sev-2 feed one dashboard, and every cross-team comparison and gate loses its meaning.
- Trade attendance for output in the trace-reading meeting. Why: a decaying meeting is not cured by a pep talk; no output counts as absent.
- Treat a postmortem that produced no case as no postmortem. Why: an incident that never enters the eval set is free to recur.
- Hold a feature out of review until it has a case. Why: the case before the code is the line that runs through the whole practice.
- Keep governance and habits joined. Why: governance without habits is a signing ceremony by people who never read a trace; habits without governance leave nothing to show the regulator.

## Procedure

1. **Fill the ownership table with real names** (templates/ownership-raci.md), four rows to start: spec (intended use, action boundary, severity table; a PM or tech lead), gold labels (the domain expert who knows the policy), judge rubric (content to the domain expert, calibration to engineering), red-line veto (one name). Engineering owns the harness and verdict implementations. Put the table on the repo's front page.
2. **Schedule the three habits** on the calendar and in the templates: which day the trace-reading meeting sits on, who is on the rotation, which review template carries "case first" as a required field.
3. **Read traces weekly.** Rotation covers everyone, PMs and new hires included. Every batch holds a random slice, not only what the signals circled. Each meeting commits at least one atlas addition or one new case to the repo; no output counts as absent. Two consecutive weeks of zero output means the meeting is dead and has not stopped yet.
4. **Run a postmortem for every incident and every attempt** (templates/postmortem.md). Prepare the trace first; the meeting opens with it on the projector and one question, "which step is the first one that went wrong". Fill the five columns (Frameworks). Close with the two checks: the incident is in the atlas, and the case it produced is in the eval set.
5. **Convert every action item** into action → equipment it points at → owner → deadline. An item that points at no equipment is either a genuinely new wall (rare) or "be more careful" in disguise; delete and rewrite.
6. **Enforce case-before-code**: a feature without a case does not enter review. Check review records against case commit times.
7. **If several teams share one harness**, apply the commons rules and platform matters (Frameworks). Register any sev-definition change as a tier-3 change with the red-line veto holder signing.
8. **Run the culture health check** (templates/culture-health-check.md) by going through records, never by asking how it feels; count danger signs, fix the first one, name its owner.
9. **When governance is required** (regulated domain or a team past a set size), promote the ownership table into a formal RACI (Accountable for gold labels must hold the domain credential), archive tier-3 approvals, arbitration records, and gate interception records, and use the postmortem template's output directly as the audit record.

## Decisions

1. **Ownership table filled with real names**, one name per row: spec / gold labels / judge rubric / red-line veto, on the repo's front page.
2. **Three habits landed in calendars and templates**: the trace-reading day and rotation; incident → case as a closing check; "case first" as a required review field. Culture exists as calendars and templates; a values poster does not count.
3. **Sev-definition dispute** → arbitration at the organizational level (the arbitration protocol raised one level, see references/judging.md), with the red-line veto holder signing; a forked sev definition is a platform incident.

## Frameworks

**Postmortem, five columns.** The trace is the chain of evidence; the material basis of blameless is sufficient evidence.

| Column | Content | Source equipment |
|---|---|---|
| Timeline | The trace itself, step by step, no retelling | Trace schema (see references/reading-traces.md) |
| `first_bad_step` | The first step that went wrong, not the worst output and not the step that got stopped (e.g. taking a forged sender at face value, not the `refund` call the permission matrix blocked) | Trace-reading discipline |
| Diff list | Before/after sandbox changes; each one "declared in advance" or "a discovery"; empty = an attempt | Side-effect audit (see references/tool-calls.md) |
| Defense performance | Per layer (input filter / action boundary / permission matrix / human confirmation): stopped, zero interceptions, or never triggered | Layered interception tally (see references/adversarial.md) |
| Action items | action → equipment → owner → deadline | Every template in this skill |

Question the room answers: which defense layer should have caught this and did not. Zero interceptions at every layer but one means one layer of depth is still working, and that is the incident.

**Ownership, four names.**

| Asset | Owner (one name) | Why this person |
|---|---|---|
| Spec (intended use, action boundary, severity table) | PM or tech lead | A product promise, not test configuration |
| Gold labels (eval set, relabeling) | Domain expert who knows the policy | Labels wrong, everything the ladder judges above them is wrong |
| Judge rubric | Content: domain expert; calibration: engineering | The judging division of labor landed on heads |
| Red-line veto | One name | On any sev-1 change, no is no; no meeting, no vote |

**Shared platform, three commons rules.** Consumption tied to contribution (whoever ships a capability files its cases first). Incidents belong to their owner (the team whose incident it is turns it into a case). The platform tends tools, not judgment (harness to the platform; cases and labels to the business teams).

**Shared platform, three matters.** (1) Eval sets may fork, sev semantics may not: forked cases stay with their owners; a forked sev definition is a platform incident. (2) The sev table is a platform asset, one copy organization-wide, changed as a tier-3 change (announced, reviewed, every affected team's gates rerun); teams keep the right to hang their own failure modes on it ("deleting a user upload is sev-1 for us"), not to edit what a tier means; the content of sev-1 is the domain expert's, the dictionary is the platform's. (3) The platform carries an SLA or the gate gets routed around: replay results within 10 minutes of submission (illustrative); a broken stub (a carrier changed its interface, the policy store changed structure) is the platform's highest priority, fixed by the on-call that day, because one broken stub turns every gate falsely red; the fidelity gap register is maintained and reconciled by the platform. Broken cases and labels are the business team's; broken stubs and harness are the platform's.

**Three habits.**

| Habit | Floor | Evidence it is alive |
|---|---|---|
| Read traces every week | Rotation incl. PMs; always a random slice; ≥ 1 atlas addition or case committed per meeting | Meeting records and commits for each of the last four weeks |
| Every incident enters the eval set | Postmortem closing check | Case commit linked to the most recent incident |
| Every feature has a case before code | "No case, no review" | Case commit time precedes review time for the last three features |

**Governance versus habits.** Governance without habits: the committee reviews slides. Habits without governance: you read traces weekly and cannot prove it. Habits supply governance with content; governance leaves habits their evidence; short either one you have paper compliance.

## Self-check

- The sentence: "We have eval infrastructure, therefore we have an eval culture."
- The reality: infrastructure is an asset, culture is a habit; assets stay in the repo, habits break quietly when headcount multiplies by five.
- The check: count the people who added a case in the last month (fewer than half the team = a few people's overtime) and how many of them are not engineers (zero = the product–model interface is not connected); then ask a random colleague which case corresponds to the last incident (no case ID = you own infrastructure).

## Templates

- `templates/postmortem.md` — five columns from trace to action items; produces equipment-pointed items with owners and the case that enters the eval set.
- `templates/ownership-raci.md` — one name per asset and the path to formal governance; produces the front-page ownership table.
- `templates/culture-health-check.md` — record-backed questions per habit; produces the danger-sign count and the first fix.

## Migration notes

- Coding agents: the trace-reading meeting reads agent PR sessions; the "incident" is a reverted or harmful merge; the red-line veto covers destructive repo actions.
- Research agents: gold labels are owned by the subject-matter expert, not the prompt author; incident = a published claim later corrected.
- Professional-judgment agents: governance is mandatory; the Accountable for gold labels must hold clinical or legal credentials; the postmortem record is the audit record; the trace is an exhibit, so write it as if opposing counsel will read every line.
- Platforms: the three commons rules and the SLA above; the sev table is the one shared asset; each team owns its fork of cases and its own incidents.
- No trace, only recollection, at your first postmortem: the first action item has generated itself, get the system producing traces that can be reviewed.
