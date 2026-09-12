# Reading traces and clustering failures into an atlas

**Load this reference when:** failures are piling up and every meeting opens with "I saw it once do…"; nobody can answer "which kinds of failure, in what proportions, which hurts most"; a pass rate is reported and nobody has read a trace; you are about to build metrics, an eval set, or a judge and have no failure mode atlas yet; two people disagree on where a trace went wrong.
Source: chapter 3, docs/chapters/ch03-error-analysis.md (templates: docs/appendices/ch03-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

1. Read first, then count; the order cannot be reversed. Why: a metric says how often it fails, a trace says what the failure is; every automation built before reading measures the wrong question precisely.
2. Mark only `first_bad_step`, even when the worst output comes later. Why: a failure planted at step 3 detonates at step 9; the blast is where the compounding comes due, the plant point is what you fix.
3. Where you code decides what you cluster. Why: code the blast and you cluster symptoms ("wrong reply", "wrong conclusion"); code the first bad step and you cluster causes ("misread a tool result", "hearsay taken as fact"). Symptom clusters produce a report; cause clusters produce a repair list.
4. Downstream steps that double down are not new failures. Why: log the echoes and one bad trace impersonates five in the statistics.
5. Read forward from step 1, never backward from the blast. Why: knowing the ending explains every step by the ending; reading forward judges from the information position the agent stood in.
6. Write behavior, not speculation; anchor every description to a step. Why: "step 2 wrote hearsay into the premise as fact" clusters and gets fixed; "the model can't understand" does neither.
7. Do not start from a taxonomy; compare after clustering. Why: a borrowed taxonomy makes you see the failures you expected and miss the ones you did not, and the latter are the point.
8. Every sev-1 mode puts at least one case into the red-line set. Why: a high-risk mode lying in the atlas has to become a sentry standing in the eval set.
9. Order by frequency × severity, severity first; raw frequency never counts alone. Why: a top-5 by raw frequency is average-thinking wearing a new face.
10. A question mark in "suspected component" is honest; a blank is the dodge. Why: the column is the hinge between atlas and improvement, and an unknown lever must stay visible.

## Procedure

1. Pick the batch. At least 5 traces, 3 failing and 2 passing (rule; enough to hit one symptom-step versus cause-step dispute). Target 20 across every task family, not the short ones. Budget several minutes per trace; 20 traces plus clustering ≈ 3–4 hours (illustrative). Do not run it in gaps between meetings.
2. For one trace: read the case and `final` first. Fix the endpoint verdict in mind: right or wrong, and wrong in what way.
3. Go back to step 1 and read forward, asking every step: "given the information available at this step, is this action reasonable?" Use the per-step-type question in Frameworks.
4. The first "no" is the `first_bad_step` candidate. Keep reading: note where the evidence contradicts the premise and is not re-examined, but log nothing new for steps that merely run on the poisoned premise. Log a genuinely independent second error (e.g. an identifier fabricated at step 7 after a premise error at step 2) as secondary, never as an equal split.
5. Write one coding row: `trace_id`, verdict (`pass / concern / unsafe / unclear`), `first_bad_step`, one-line behavioral step-anchored description, severity (by consequence, not by the artifact type: a wrong report that would trigger a recall is sev-1), suspected component (prompt / tool description / retrieval / knowledge base / model reading a result / `?`).
6. Code blind. Look at another coder's rows or an answer key only after your own are done. When comparing, compare `first_bad_step` case by case; a gap of more than one step sends you back to reread that trace.
7. Log batch pacing: per batch, the count, the task types covered, and how many new modes appeared. Keep the count per task type, not only overall.
8. Cluster. Spread the rows out (a whiteboard beats a spreadsheet), pile similar descriptions, name each pile with a behavioral verb phrase. Write a definition and criterion decidable on the next trace (hit / no-hit); a mode you cannot state that far has not formed, split or merge it.
9. Fill the atlas: name / definition and criterion / representative trace IDs / count / sev distribution / suspected component. Near misses count under `concern` with no sev tier.
10. Only now open references/failure-taxonomy.md and compare, to find gaps in your atlas, not to fill a form.
11. Judge saturation per task type (Decisions). Top up whichever family is still producing new modes.
12. Write the decision: the top-5 table, which mode this cycle fixes, and the criterion beside it. Add one red-line case per sev-1 mode (see references/building-eval-sets.md). A spoken priority does not survive the next meeting.

## Decisions

**Ordering and fix-first.** Score each mode on three questions.

| Question | Reads from | Weight |
|---|---|---|
| How severe? | sev distribution column | first; a low-frequency sev-1 ranks ahead of a high-frequency sev-3 even at 10× the count |
| How common? | count column | second |
| Is the lever clear? | suspected component column | a definite hypothesis is targeted surgery; a `?` is a blind box |

Rulings:

- High severity + high frequency + clear lever → fix first this cycle.
- High severity + unclear lever (`?`) → put a red-line case on it, watch it, accumulate evidence; it never vanishes from the atlas because "we don't know how to fix it". A sev-1 you cannot see does not become a sev-3.
- High frequency + sev-3 + clear lever → schedule; never ahead of a sev-1 row.
- Output: the top-5 table plus one line "this cycle fixes <mode> because <criterion>", signed.

**Symptom-step versus cause-step disagreement.** Two coders mark `first_bad_step` two steps apart (one at step 9 where the wrong reply was spoken, one at step 5 where the order status was misread). The cause-step coder is right by discipline. Argue it through once; the split deepens the shared definition of "what counts as wrong" and feeds judge calibration later (references/judging.md).

**Saturation (when reading is enough).**

- The last several traces in a row produced no new mode → near saturation for this batch and this task family.
- Judge it per task type. Lookup traces are short with a narrow failure surface and saturate first; investigation and synthesis traces are long and saturate last. An overall curve that flattens is usually the lookup family dragging the mixed curve flat while investigation keeps producing modes (the overall-saturation illusion). Plot per family; top up the unsaturated one.
- Saturation is a snapshot against current capability + current input distribution, not an endpoint. Every capability unlock (write tools, memory, subagents) and every distribution change (production traffic) owes the atlas another round of incremental coding.

## Frameworks

**Plant and blast.** A trace is a dozen-plus alternating steps (model, tool_call, tool_result) with state passed along. Once step 5 misreads the state, every later step runs "reasonably" on a poisoned premise, and the error cashes out in `final`. The loudest error is at the blast; the cause is at the plant point. (E.g. an investigation whose step 2 wrote one customer's spoken "they all leak" into the premise as an order fact, after which every search hunted evidence for it and the real pattern, complaints clustered on one supplier batch, was never seen; and a refund reply wrong at step 9 whose only error was a misread order status at step 5.)

**Forward-reading question by step type.**

| Step type | Ask |
|---|---|
| model | do the assertions in this turn have a source in earlier steps? is a claim being written as a verified fact? |
| tool_call | where did the arguments come from? were they available and confirmed? |
| tool_result | did the next step read it correctly? does it contradict the premise, and was the premise re-examined? |
| subagent / inbound | same question at the handoff: what did the receiver know, and was that enough (see references/multi-agent.md)? |

**Three products of one forward read.** `first_bad_step`; a behavioral description ("step 1 wrote the customer's spoken claim into the premise as verified fact"); one suspected-component hypothesis (prompt, tool description, retrieval, knowledge base, or the model reading a result). Working backward from the blast produces none of these reliably: knowing the ending, the premise step reads like "reasonable task understanding".

**Coding row (five columns after `trace_id`; aligned to the verdict record so it logs straight in).**

| trace_id | verdict | first_bad_step | one-line failure description (behavioral, step-anchored) | severity | suspected component |
|---|---|---|---|---|---|
| <trace-id> | `unsafe` | 2 | step 2 wrote the customer's spoken paraphrase "they all leak" into the investigation premise as verified fact; every later search hunted evidence for it | sev-1 (the conclusion would trigger a recall) | prompt (premise never required distinguishing claim / verified)? |

The cause step drifts between traces (step 1 in one, step 2 in another); the criterion does not.

**Four coding disciplines.**

| Discipline | Do | Not |
|---|---|---|
| Behavior, not speculation | "step 2 wrote hearsay into the premise as fact" | "the model can't understand" |
| Anchor to a step | every description carries a step number | "policy understanding is off" |
| One trace, one primary failure | primary = the error at `first_bad_step`; independent second error → secondary | two failures splitting the billing evenly; echoes logged as errors |
| No taxonomy first | let categories grow, compare against references/failure-taxonomy.md after clustering | jamming traces into ready-made slots |

**Behavioral naming.** Good: "hearsay taken as fact", "doubling down after misreading a tool result", "fabricating an identifier", "answering hard instead of handing off". Bad: "understanding problem", "quality problem" (anything fits in, nothing comes back out). Test: can someone who has not read the traces imagine the failure from the name alone?

**Atlas (six columns, fixed book-wide; example v1 from 60 traces, 35 clean and 25 failing, illustrative).**

| Name | Definition and criterion | Representative trace IDs | Count | sev distribution | Suspected component |
|---|---|---|---|---|---|
| unauthorized commitment | language promises an action beyond authority (refund / compensation / expedite); a read-only agent does it too | <ids> | 4 | sev-1 × 4 | prompt (commitment constraint bypassed by new inducement phrasing) |
| fabricated identifier | cites a nonexistent order / ticket ID; absence from the sandbox confirms it | <ids> | 4 | sev-2 × 4 | prompt (no hard "no evidence, no answer" instruction)? |
| wrong policy answer | reply contradicts the policy ledger; evidence often sits in the previous tool_result | <ids> | 3 | sev-2 × 3 | model reading the result (tool returned the right thing) |
| irrelevant record lookup | digs through records unrelated to the task or of unconfirmed ownership; endpoint often still right | <ids> | 5 | near miss × 5 (all `concern`) | tool description (`get_customer` has no ownership constraint)? |
| fuzzy search instead of exact lookup | customer gave an ID, agent fuzzy-searches by name | <ids> | 3 | near miss × 3 (pulling a same-name customer's order makes it sev-2) | tool-description boundary (`get_order` vs `search_orders`) |
| hearsay taken as fact | a spoken claim written into the premise as verified fact; later searches hunt evidence for it | <ids> | 3 | sev-1 × 3 | prompt (premise does not distinguish claim / verified)? |
| missed request item | several asks at once, one dropped; often the time-sensitive one | <ids> | 3 | sev-3 × 3 (time-sensitive item escalates by consequence) | ? |

25 failures → 7 modes; the compression ratio is information (failures concentrate). Severity first: the fix-first list is the two sev-1 rows, not the most frequent row (irrelevant record lookup, 5). Read the atlas on a first pass by three columns only: name, sev distribution, suspected component.

**Three downstreams of the atlas.** Reverse-generate a stratified eval set from it (references/building-eval-sets.md); assign judge calibration focus by it (references/judging.md); industrialize it as failure mining on production data (references/improving.md). The atlas is a living document.

**Reading cost.** Reading is the most expensive path-level check and spends human time by the minute. It buys the structure of the failures, which every later instrument uses. It is not the long-term judgment instrument; automation goes to the judgment ladder, and the ladder is built on the atlas, the atlas on reading, in that order.

## Self-check

Self-consolation: "we ran 500 cases, 82% pass."
Reality: both numbers are real and empty; nobody knows which modes are in the 18% or whether a sev-1 is, so 82% averages ignorance into a respectable decimal.
Check: when anyone (you included) reports a pass rate, pull one failure at random on the spot and ask for its `first_bad_step`; if they can point at it, an atlas stands behind the number; if not, the number was never unsealed, read first and report after.

## Templates

- `templates/trace-review.md`: the coding sheet (one trace per row) plus the coding protocol (four disciplines, blind coding, batch pacing, saturation); produces rows that log straight into the verdict record.
- `templates/failure-mode-atlas.md`: the six-column atlas skeleton with the behavioral-naming self-check and the ordering rule; produces the top-5 and the fix-first decision.

## Migration notes

- Existing agent, no harness: export recent failure records (logs or session history), use the same coding sheet, mark "the first link that went wrong" even if the trace has no clean step structure.
- Coding agent: a failure trace is one CI session that broke or one PR that got reverted; `first_bad_step` usually lands on "misread the error message" or "edited a file it shouldn't have"; the final crash is only the settlement.
- Professional-judgment agent (contract review, finance, medical documentation): `first_bad_step` is usually "hearsay taken as fact" or the retrieval layer grabbing the wrong basis.
- LangSmith / Braintrust: every span and tool call is a step; mark `first_bad_step` on the earliest span that went wrong and copy the coding sheet over; no re-export needed.
- No agent yet: run the same coding on a human process (ticket handling and escalation records contain hearsay taken as fact too), or on a competitor fed the same inputs.
