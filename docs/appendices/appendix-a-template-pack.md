# Appendix A · Template Pack

An index and a usage map for the book's 44 Your Loot templates. The files themselves live in the repo under `templates/chNN/`. Templates are for filling in; this page only says, in one line each, what input a template takes and what decision it produces. Three core templates (ch01 Pocket Eval, ch08 Permission Matrix, ch14 Gate Table) are reproduced in full at the end of this appendix, so they work even away from the repo; **the repo is the source of the latest version of every template**, and where the two disagree, the repo wins.

The order of use is the chapter order; each template makes its first appearance in its chapter's Lab. Three of them are "living files" that the rest of the book keeps writing back into: the spec from Chapter 2 (merged into the permission matrix from ch08 on), the atlas from Chapter 3 (industrialized in ch15), and the Stop Rule Decision Sheet from Chapter 14 (ch12's shutdown red lines merge into its safety branch).

| Ch | Template (repo path `templates/…`) | One line |
|---|---|---|
| 1 | [`ch01/pocket-eval-pack.md`](ch01-templates.md) | Five blocks on one page: three lines of intended use / the three-column action boundary / the worst-failures list / a 20-row case table / the continue-narrow-stop decision sheet (takes effect on signature) |
| 2 | [`ch02/attribute-map-worksheet.md`](ch02-templates.md) | Six attributes × task type ranking, with a column for "who this ranking has lost to" |
| 2 | [`ch02/severity-worksheet.md`](ch02-templates.md) | sev-1/2/3 list + the four-verdict mapping table + the tiered report format |
| 2 | [`ch02/intended-use-action-boundary-sheet.md`](ch02-templates.md) | The spec, extended; its formal name from Chapter 8 on: the file you must change before unlocking anything |
| 3 | [`ch03/trace-review-form.md`](ch03-templates.md) | One row per trace, a coding sheet whose fields align with the verdict-record schema |
| 3 | [`ch03/qualitative-coding-protocol.md`](ch03-templates.md) | Four coding disciplines + operating notes for blind coding and saturation |
| 3 | [`ch03/failure-mode-atlas-starter.md`](ch03-templates.md) | The six-column atlas skeleton + the behavioral-naming self-check |
| 4 | [`ch04/golden-task-design-protocol.md`](ch04-templates.md) | Six steps to one golden task, one check question per step |
| 4 | [`ch04/coverage-matrix.md`](ch04-templates.md) | Failure mode × severity × user type; an empty cell needs a signature |
| 4 | [`ch04/label-expiry-policy.md`](ch04-templates.md) | Register the policy basis + relabel on change + periodic audit |
| 5 | [`ch05/judgment-ladder-decision-tree.md`](ch05-templates.md) | Choosing the judgment instrument starting from three questions, with the sev-1 authority rule |
| 5 | [`ch05/judge-validation-report.md`](ch05-templates.md) | Judge-vs-human disagreement, tiered + the go-live / recall conclusion + a validity-period statement |
| 5 | [`ch05/arbitration-protocol.md`](ch05-templates.md) | What goes to arbitration, who rules, where the ruling lands |
| 6 | [`ch06/stats-cheat-sheet-sample-size.md`](ch06-templates.md) | Gap ↔ cases needed, quick lookup + flip rate + choosing pass@k or pass^k |
| 6 | [`ch06/stats-cheat-sheet-report-template.md`](ch06-templates.md) | The report format that always carries intervals (the base format for every report in the book) |
| 7 | [`ch07/harness-architecture-spec.md`](ch07-templates.md) | Six-component data flow + the stub/real-call boundary + the replay/simulation layering |
| 7 | [`ch07/tool-stub-inventory.md`](ch07-templates.md) | One row per stub, with the fidelity gap register (the ledger ch13 reconciles against) |
| 7 | [`ch07/synthetic-user-persona-library.md`](ch07-templates.md) | Four-element persona scripts + the fidelity spot-check table |
| 8 | [`ch08/action-permission-matrix.md`](ch08-templates.md) | Tool × condition rows across three permission columns; once filled in, it merges into the spec |
| 8 | [`ch08/tool-call-eval-checklist.md`](ch08-templates.md) | Five dimensions × judgment instrument (nearly every cell is a deterministic check) |
| 8 | [`ch08/side-effect-audit-table.md`](ch08-templates.md) | Three kinds of side effect × detection method × findings register |
| 9 | [`ch09/plan-quality-rubric.md`](ch09-templates.md) | Scoring anchors on four dimensions: complete / minimal / verifiable / ordered |
| 9 | [`ch09/plan-trace-deviation-checklist.md`](ch09-templates.md) | Three kinds of deviation + the two-track reading + pre-run alarm thresholds |
| 9 | [`ch09/cost-latency-report-template.md`](ch09-templates.md) | Chapter 6's base format plus a cost column (declared: illustrative dollars) |
| 10 | [`ch10/memory-eval-matrix.md`](ch10-templates.md) | Miswrite / forgetting / crosstalk × test / verdict / sev / red-line example |
| 10 | [`ch10/long-task-attribution-protocol.md`](ch10-templates.md) | A step card for tracing back along the write chain to the first bad write |
| 11 | [`ch11/multi-agent-attribution-decision-tree.md`](ch11-templates.md) | An attribution flow with one exit per suspect, three suspects |
| 11 | [`ch11/handoff-quality-checklist.md`](ch11-templates.md) | Three blocks, must-pass / return / confidence + two hard checks, independence and duplicated work |
| 12 | [`ch12/agent-red-team-protocol.md`](ch12-templates.md) | Who plays the attacker / how often a round runs / where findings go + the coverage matrix |
| 12 | [`ch12/redline-test-set-starter.md`](ch12-templates.md) | Attack surface × carrier sample skeleton (technique category + defense verification point) |
| 12 | [`ch12/shutdown-redline-checklist.md`](ch12-templates.md) | The immediate-shutdown red-line checklist (= ch14's safety branch) |
| 13 | [`ch13/deployment-evidence-ladder.md`](ch13-templates.md) | Four rungs × three questions + the mandatory-rung table + a sign-off line per promotion |
| 13 | [`ch13/silent-shadow-plan-template.md`](ch13-templates.md) | Baseline for comparison / interception points / disagreement review / exit conditions |
| 13 | [`ch13/monitoring-signal-spec.md`](ch13-templates.md) | Five columns per signal, pre-filled with four kinds of no-gold-label signal + drift probes |
| 14 | [`ch14/release-gate-template.md`](ch14-templates.md) | The five-column gate table, pre-filled with the zero-tolerance sev-1 row |
| 14 | [`ch14/change-tier-matrix.md`](ch14-templates.md) | Three change tiers × suite × recalibration, with the fallback "round up" |
| 14 | [`ch14/stop-rule-decision-sheet.md`](ch14-templates.md) | Safety branch + operational branch + three pause levels with triggers and recovery |
| 14 | [`ch14/go-no-go-review-sheet.md`](ch14-templates.md) | The one-page launch review for the room: base-format metrics + evidence rung + the residual-risk owner's signature |
| 15 | [`ch15/failure-mining-protocol.md`](ch15-templates.md) | Failure pool → stratified sampling → coding and clustering → atlas extension |
| 15 | [`ch15/bottleneck-lever-mapping.md`](ch15-templates.md) | Seven levers × failure category, with the "handy != on target" self-check |
| 15 | [`ch15/improvement-cycle-template.md`](ch15-templates.md) | A one-page cycle: falsifiable hypothesis + rejection rule written in advance |
| 16 | [`ch16/incident-postmortem-template.md`](ch16-templates.md) | The five-column postmortem; every action item must point at equipment + an owner + a deadline |
| 16 | [`ch16/quality-ownership-raci.md`](ch16-templates.md) | Spec / gold labels / rubric / red-line veto, one name per row |
| 16 | [`ch16/eval-culture-health-check.md`](ch16-templates.md) | The "open the records" question list for the three habits |

*Table A-1 The index of the book's 44 Your Loot templates. Three "living files" (the spec, the atlas, the Stop Rule Decision Sheet) are written back into by later chapters; the rest land once, in their chapter.*

The shortest route depends on your situation. Taking over a new agent, start with the ch01 one-pager and spend two hours. About to launch, put the ch13 ladder and the ch14 trio on the table. Just had an incident, open the ch16 postmortem template directly; its action-items column will lead you back to whichever template you still owe.

---

## The three core templates in full

The three below are reproduced word for word from the repo (only the heading levels are demoted to fit the appendix); the repo is the source of the latest version.

### 1. Pocket Eval Template ([`templates/ch01/pocket-eval-pack.md`](ch01-templates.md))

Use it in the first two hours before launch, before starting work, or on taking over any agent, to catch the first high-risk failure when there is no infrastructure at all.

> Note: a two-hour timebox (step timings 30/20/40/25/5 minutes), five blocks on one page. Fill it in before launch, and whenever you take over any agent. The signature line is not decoration: a decision with a name on it is a decision that gets taken seriously.

#### 1. Intended use (three lines)

- For whom:
- Does what:
- Does not do:

#### 2. Action boundary (three columns)

| Autonomous | Needs confirmation | Forbidden |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

#### 3. Worst-failures list (5 rows, sorted by harm)

| # | Worst failure (specific down to the action) | Harm |
|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |

#### 4. Case table (20 rows)

Verdicts: `pass / concern / unsafe / unclear`

| # | Input | Which worst failure it targets | Verdict |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |
| 6 |  |  |  |
| 7 |  |  |  |
| 8 |  |  |  |
| 9 |  |  |  |
| 10 |  |  |  |
| 11 |  |  |  |
| 12 |  |  |  |
| 13 |  |  |  |
| 14 |  |  |  |
| 15 |  |  |  |
| 16 |  |  |  |
| 17 |  |  |  |
| 18 |  |  |  |
| 19 |  |  |  |
| 20 |  |  |  |

#### 5. Decision sheet

- Decision: ☐ continue ☐ narrow ☐ stop
- Basis (which cases support this decision):
- Signature: `________`  Date: `________`

### 2. Action Permission Matrix ([`templates/ch08/action-permission-matrix.md`](ch08-templates.md))

Change this before unlocking any write tool for the agent, and again every time a tool or a condition branch is added.

> Notes: build rows on tool × condition (not one row per tool name), check one of the three columns, fill in the guard, answer both questions. **Once filled in, this merges into the Chapter 2 spec and is part of the spec from then on**; before unlocking any write tool, change this first.

#### Permission matrix

| Tool | Condition | Autonomous | Needs confirmation | Forbidden | Guard (assertion / diff / gate) |
|---|---|---|---|---|---|
| escalate | always | ✅ |  |  | none |
| refund | amount ≤ $500 and order not refunded |  |  |  | `amount_within_limit`, diff |
| refund | order already refunded |  |  | ✅ | `refund_not_executed` (seeded probe) |
| update_order | after shipment (via Swiftlink interception) |  | ✅ |  |  |
| send_email | recipient not verified through the order binding |  |  |  | `no_pii_disclosure` |
|  |  |  |  |  |  |

#### The two confirmation-and-rollback questions (answer per write tool)

| Tool | Who confirms? (no answer = no unlock) | How does it roll back? (nominally undoable ≠ actually recoverable) |
|---|---|---|
| refund |  |  |
| send_email |  | a sent email cannot be recalled → intercept up front |
| update_order |  |  |
| escalate |  |  |

#### Differ semantics

Every sandbox before/after change is either declared as expected, or it is a finding.

### 3. Release Gate Template ([`templates/ch14/release-gate-template.md`](ch14-templates.md))

Use it on the day evaluation stops being "someone remembers to run it" and becomes "the process cannot route around it": the first time you wire a CI gate, and every time you adjust the pass criteria.

> Note: gate numbers and thresholds must be written down before the run, red-light actions hard-wired in advance, no one's mood in the loop. The config lives in `ci/gate`.

#### Gate table (five columns)

| Metric | Criterion | Data source | Verdict source | Red-light action |
|---|---|---|---|---|
| sev-1 count | = 0 (zero tolerance, its own line, never into the average) | replay-layer sev-tiered report | assertion (sev-1 may not be gated by a judge alone) | refuse merge, return for a fix |
| cost P95 | ≤ ____ (dollars, illustrative) | stats cost distribution | deterministic | refuse merge |
| latency P95 | ≤ ____ | stats | deterministic | refuse merge |
| sev-2 failure count | ≤ ____ |  |  |  |
|  |  |  |  |  |

#### Replay-layer / simulation-layer trigger timing (following ch7's layering)

- **Replay layer**: deterministic replay, run **on every commit** (hung on the commit hook; a red light exits non-zero). Scope: the cheapest-to-judge subset (what assertions can judge) + the red-line set.
- **Simulation layer**: free simulation, run **on every version**, `--repeat` with intervals (ch6 discipline); triggered by tier-2-and-up changes (see the Change-Tier Matrix).

#### Interception record

| Date | Commit / change | Metric turned red | Case turned red (e.g. `no_over_limit_commitment` × angry) | Disposition |
|---|---|---|---|---|
|  |  |  |  |  |
