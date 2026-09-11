# Appendix E · Glossary

The book's terms, grouped by theme. Entry format: **term**: a one-line definition. (chapter of first appearance)

## 1. Objects and basic units

- **trace (trajectory)**: the complete record of one agent run, the sequence of steps alternating between model turns, tool calls, and tool results, plus the final output; the basic unit of evaluation. (ch2)
- **case (task / test case)**: one test, a world state (setup) plus a request (prompt) plus the expected trace properties (expect); the evals literature calls it a task or a test case. (first used in ch1, schema fixed in ch4)
- **inbound (external content ingestion event)**: one of the trace step types, the moment external content such as a fetched web page or an incoming email body enters the context; attack-surface inventories and injection attribution both start from it. (ch12)
- **eval (evaluation)**: the systematic evaluation of an agent, the sum of cases, verdicts, and reports; this book's position is that the eval is the agent's spec. (ch1)
- **eval-as-spec**: attribute priorities + the severity table + the action boundary form a spec that can exist before the code; extend the eval before extending capability; at the case level, this means the eval set itself precedes the code, and a new requirement first becomes a new case. (ch2, ch4)
- **the three axes**: the self-check coordinates of a task: is the endpoint verifiable / is the action reversible / is there a gold answer; they decide the judgment instrument and the attribute priorities. (ch2)
- **Pocket Eval**: the two-hour minimum eval: a one-page boundary + worst failures + handwritten high-risk cases + the four verdicts + a continue / narrow / stop decision. (ch1)

## 2. Verdicts

- **the four verdicts (pass / concern / unsafe / unclear)**: the four levels of a per-case human verdict, unchanged throughout the book. The fourth verdict depends on who labels: an engineer judging evidence from traces uses unclear; when real users react to outputs, the fourth becomes useless (a value signal). (ch1)
- **sev-1 / sev-2 / sev-3 (severity)**: failure tiers: irreversible harm or unauthorized action / recoverable user loss / experience and efficiency; metrics are reported tiered by sev, with sev-1 counted on its own line and never averaged in. (ch2)
- **assertion**: an expectation written for a single case that one line of code can answer, such as `refund_not_executed`. (first seen in the case schema in ch4, formally defined in ch5)
- **judge (LLM-as-judge)**: using a model to judge attributes that only language can judge; its qualification to serve is calibration (judge-vs-human alignment), and on sev-1 it may only escalate, never release; the calibration set and the examples in the prompt must not overlap. (ch5)
- **false-pass rate / false-fail rate**: the judge's two directional error rates against gold; a human `unsafe`/`concern` that the judge rules `pass` is a false pass, a human `pass` that the judge rules non-pass is a false fail; per-class recall is the complement of the false-pass rate. Kappa is for human-vs-human only. (ch5)
- **verdict sinking**: pushing verdicts as far down the ladder as possible: whatever an assertion can judge never reaches the judge, whatever the judge can judge never takes a human; in domains where the data is imprisoned it does more than save money, it is the precondition for an evaluation system existing at all (Appendix C). (ch5)
- **the judgment ladder**: the cost ladder of judgment instruments, assertion < deterministic check < calibrated judge < human; every verdict uses the lowest rung it can. (ch5)
- **first_bad_step**: the first step that went wrong (not the worst output); the discipline of coding the cause rather than the symptom, a fixed field of the verdict record. (ch3)
- **the failure mode atlas**: the living document of failure clusters, six columns per row: name / definition and criterion / representative traces / count / sev distribution / suspected component. (ch3)

## 3. Eval sets and infrastructure

- **golden task**: a pre-designed evaluation task with an endpoint made as verifiable as possible; the basic unit of an eval set. (ch4)
- **coverage matrix**: the tiered coverage table of failure mode × severity × user type; an empty cell is a testing blind spot. (ch4)
- **regression set**: the part of the eval set the gate reads, expected to pass at close to 100%, where a red light means a regression; in the repo it is the directories listed under suites in `ci/gate.yaml`. (ch4, ch14)
- **capability set**: cases written eval-first that the agent cannot pass yet, living in `cases/capability/`; expected to fail, run on every version, reported on their own line, never blocking a release. (ch4)
- **graduation**: a capability-set case moves into the regression set after passing `--repeat 5` on two consecutive versions, and a sev-1 case also needs a deterministic assertion first; its first-run score on graduation day is the one reading in its life that was never optimized against. (ch15)
- **reference trajectory**: the one known-passing trajectory attached to every case, hand-written or harvested from a passing trace, run through the assertions and judge rules with zero model calls to prove the task is solvable and the verdict configuration is right. (ch4)
- **harness**: the self-built eval infrastructure, runner, trace, assertions, judge, stats, report; the repo's real asset. (ch7)
- **agent harness (scaffold)**: the layer that turns around the model, the loop, tool orchestration, prompt assembly; Mini = model + scaffold, and the thing under test is the two together. In this book the word harness on its own always means the eval infrastructure. (ch7)
- **tool stub**: a fake implementation that catches calls in place of the real tool (a refund stub, an outbox stub), making dangerous actions testable; the stub's fidelity must itself be evaluated. (ch7)
- **synthetic user**: the counterparty played by an LLM, three personas, angry / vague / multi; the four script elements and the three distortions are in ch7. (ch7)
- **seeded-error probe**: a deliberately planted error, to see whether the process catches it; manually adding sev-1 scenarios to the alignment set follows the same idea. (ch8)

## 4. Trustworthy numbers

- **pass@k / pass^k**: at least one success in k attempts / all k consecutive attempts succeed; an agent should watch the latter. (ch6)
- **flip rate**: the share of a case's verdicts that disagree across repeated runs; a high flip rate is itself a reproducibility defect, not only a measurement problem. A different concept from ch13's "overturn rate," never confuse them. (ch6)
- **trial**: one attempt at one case. This book's "run" is one pass over the whole eval set, which gives every case one trial; the k in pass@k / pass^k counts trials. (ch6)
- **paired comparison**: old and new versions run the same cases, compared case by case; the evals literature's pairwise comparison, a judge comparing two candidate outputs, is a different thing. (ch6)
- **saturation (of the eval set)**: the regression set and the capability set both pass in full, and the score stops carrying any improvement signal; the move is to add harder cases. Three different concepts from ch3's saturation of coding (reading traces no longer surfaces new failure modes) and ch15's suite aging (overfitting), never confuse them. (ch15)

## 5. Agent-specific battlegrounds

- **Action Permission Matrix**: the autonomous / needs-confirmation / forbidden boundary and rollback strategy for every write operation; a hard boundary unrelated to the agent's judgment. (ch8)
- **before/after diff**: diffing the sandbox state before and after; the semantics: every change is either declared as expected, or it is a finding. (ch8)
- **plan-trace alignment**: mapping execution steps one by one back onto plan subgoals, to quantify deviation. (ch9)
- **orphan step**: a step that maps to no subgoal; one of the three deviation classes (the other two are abandoned subgoal and order inversion). (ch9)
- **first bad write**: the first wrong write found by tracing back along the memory write chain; the anchor for long-horizon attribution. (ch10)
- **handoff contract**: the checklist of context a main-agent-to-subagent handoff must carry; dropping intent or a deadline is a breach. (ch11)

## 6. Shipping and sustaining

- **evidence ladder**: the ladder of evidence from offline to online, replay → silent/shadow → canary → full traffic. (ch13)
- **silent/shadow**: the agent produces output on real traffic without it taking effect, compared against the human result; a mandatory rung in high-stakes domains. (ch13)
- **overturn rate**: the share of conclusions and actions later overturned by a human: a human reversal after a customer appeal, a human rejection of a "needs confirmation" action. A different concept from ch6's "flip rate" (the same case disagreeing across runs). (ch13)
- **harvesting from production**: the fixed action of turning production traces into new eval-set cases; four entry points: an online red-line hit, an overturned item, a repeat visit, a new shape pointed at by a drift probe. (ch13)
- **drift**: signals such as the input distribution, tool error rate, or escalation rate leaving their baseline band; the response is harvesting and adding coverage, not a direct rollback. (ch13)
- **derail rate**: the share of replays in which the agent's behavior leaves the recorded track; each change type has an expected order of magnitude, and exceeding it means the change was tiered too low. (ch14)
- **quarantine**: the isolation lane for unstable cases, flag → isolate → rule by a deadline (fix the case / fix the agent / downgrade to non-gating monitoring); isolation with an alarm clock, not an exemption. (ch14)
- **canary**: a small share of real traffic goes first; an anomalous metric means rollback. (ch13)
- **change tiers**: setting the regression scale by change type: which kinds run the full suite, which run a sample, which tier a vendor model swap belongs to. (ch14)
- **stop rule**: the pre-written stopping condition, the situations in which the agent must be paused, no discussion, no iteration. (ch14)
- **failure mining**: clustering production failures and mapping them to attributes / steps / components; the failure mode atlas industrialized on production data. (ch15)
- **bottleneck-to-lever mapping**: which improvement lever each failure class corresponds to: edit the prompt, swap the model, change the tool, add a confirmation, remove a component. (ch15)
- **blameless postmortem**: the agent version of the incident postmortem, where the trace is the chain of evidence; the output points at equipment, not at people. (ch16)
