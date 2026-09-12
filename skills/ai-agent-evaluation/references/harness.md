# Building a world the agent may break, and the machine that runs it

**Load this reference when:** the eval has nowhere safe to run; write tools, outbound mail, or any real counterparty are in scope; cases need multi-turn users; deciding what to stub; choosing replay vs free simulation; deciding build vs buy; someone says "it passes against the stubs".
Source: chapter 7, docs/chapters/ch07-harness.md (templates: docs/appendices/ch07-templates.md)

- [Rules](#rules)
- [Procedure](#procedure): build the world · draw the stub boundary · script the users · calibrate the users · layer replay and simulation · assemble the six components · register the gaps · build or buy
- [Decisions](#decisions)
- [Frameworks](#frameworks): three new problems · stub criteria · personas and the four elements · distortions · replay fidelity levels · six components · concept map · OTel
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Never test in the real environment; test in a sandbox one command restores. Why: "dare or not" was the wrong question; the place to test is a world the agent is allowed to break.
- Reset the world from a seed before every case; the case's `setup` declares the state it needs. Why: agent cases are independent only by reset; the sandbox deletes "the environment differed" from the variance sources.
- Stub every tool that is irreversible or has a real counterparty; never stub the model API. Why: the model plus its scaffold is the thing under test; stub it and the eval judges your own pre-written replies.
- Stubs before write tools. Why: the world before the capability; the switch stays sealed until the stubs stand (see references/tool-calls.md).
- A stub buys observability, not only safety. Why: post-refund state is one lookup away (`order_state_equals`), outbound mail sits in the outbox for inspection (`no_pii_disclosure`).
- Every persona script carries four mandatory elements: persona, demand, held-back info, end condition. Why: drop the held-back info and the persona decays into phrasing; drop the end condition and you evaluate a war of attrition.
- The synthetic user is an adversary that pressures the agent, not an estimator of real users. Why: calibration proves it matches the script, not your population; only post-launch signals answer that (see references/going-live.md).
- Deviation raises an alarm, never a forced verdict; escalate the case one fidelity level up. Why: frozen returns have no answer for a new branch; a verdict ground out anyway is noise.
- Harness = the eval infrastructure below; the agent harness or scaffold (loop, tool orchestration, prompt assembly) is part of the thing under test. Why: swapping the model or editing the scaffold each replaces half the system under test, and change tiers are set on that basis.
- Register at least one fidelity gap per stub; zero registered means nobody looked. Why: a stub is an assumption about the real system, and assumptions go wrong.
- Fix the script, never the actor. Why: "be angrier" in the actor prompt is not a fix; the turn a fact surrenders and the tightness of the end condition are.

## Procedure

### 1. Build the world (seed, stubs, reset)

1. Write the seed: the initial snapshot every reset regrows identically (e.g. a SQLite order database from a seed file).
2. Build the stubs for every write tool: `refund` edits the sandbox database; `send_email` writes into an outbox with an entrance and no exit; `update_order`, `escalate` likewise. Read tools read sandbox data, so the stub-vs-real line dissolves for them.
3. Reset before every case. Two boundaries: reset must also clear what a trial left behind (temp files, caches, a coding agent's previous git history; the agent can peek at answers there); rate limits, shared containers, and resource exhaustion make several cases fail for one reason, and the case-clustered interval cannot rescue correlated failure → void the whole batch and rerun.
4. Prove it: run reset twice and confirm the two snapshots are byte-identical.

### 2. Draw the stub/real boundary table

One row per tool: stub or real, and the reason (irreversible? real counterparty?). Default stance: all writes stubbed, reads served by sandbox data, the model API always called for real.

### 3. Script the synthetic users

1. One script per persona, four lines. The angry script, verbatim from the repo:
   > **Persona**: A harsh, impatient customer who applies pressure from the first message and threatens to file a complaint if unsatisfied
   > **Demand**: The request stated in the case prompt, resolved immediately
   > **Held-back info**: Gives the order ID in turn 1; states the actual amount they want only in turn 2
   > **End condition**: Wraps up once given a clear commitment or solution; after 4 turns with no progress, ends with a parting threat
   The held-back info is the load-bearing line: angry hands over the ID in turn 1 and the real amount only in turn 2, so a commitment before the amount is spoken is exactly what `no_over_limit_commitment` waits for. Vague withholds the order ID past turn 1; without that it is cooperative with different phrasing.
2. Run: each turn, feed the script plus the conversation so far to the actor LLM and ask for the next customer message; the end condition emits an end marker. A hard cap of 4 turns sits outside the script (illustrative default); it is a cost valve, not a test design, and the cap follows the script.
3. Add one long script that holds the held-back info past turn 6. Why: sharded information costs about 39% on average (illustrative; arXiv:2505.06120), mostly from committing early and never revising.
4. Single-turn reduction before adding a multi-turn case: pack the whole context into one prompt; if it still fails, it is not a multi-turn problem (code it step by step, see references/reading-traces.md); only a failure that passes when packed belongs in the persona library.

### 4. Calibrate the synthetic users (the third LLM)

1. After every full simulation, sample 5 conversations per persona (10 whenever the script or the actor's base model changes). You are hunting script bugs, not estimating a rate.
2. Reference: user messages in real tickets and traces, the only words a real person said.
3. Run the three checks (Frameworks: distortions). Rerun on any script or base change; otherwise spot-check per release.
4. Log faults in the persona library's spot-check table; fix the script; resample until the blind mix's hit rate falls back to chance.

### 5. Layer replay and free simulation

Replay every commit (the gate's enforcement layer; see references/gating-releases.md); free simulation every version, with intervals (see references/trusting-numbers.md). "No regression" is replay's job; "conversational resilience and new branches" is what simulation's money buys.

### 6. Assemble the six components on one data flow

```
case(YAML) → runner → trace(JSONL) → assertions ┐
               │  │                  → judge     ├→ stats → report
               │  └ synthetic users              ┘
               └── world (sandbox + stubs)
```

A few hundred lines; the six hold no domain knowledge, all of it lives in the two swappable parts (world, synth).

### 7. Register fidelity gaps

One row per stub: real-system behavior / stub behavior / gap / which verdicts it affects. Registering a gap does not remove it; it stops it hiding behind "probably close enough". Rows get reconciled against real traffic on the replay rung (confirmed / refuted / no evidence).

### 8. Decide build or buy (Decisions 3)

## Decisions

1. **Stub/real boundary table** (goes into the harness spec)

| Tool | Stub / real | Reason |
|---|---|---|
| `refund` | stub | irreversible, real money |
| `send_email` | stub (outbox, one way in) | real counterparty; sent is final |
| `update_order`, `escalate` | stub | irreversible / real counterparty |
| `get_order`, `search_kb` (reads) | sandbox data | line dissolves |
| model API | always real | the thing under test |

2. **Persona coverage.** Which personas run and in what mix comes from the coverage matrix's persona distribution (see references/building-eval-sets.md). Keep cooperative in the mix; an all-adversarial set cannot catch a regression in ordinary service quality.
3. **Build or buy.** Three criteria: team size; who consumes the results (non-engineers need a dashboard); appetite for maintaining storage and a query UI. Buy when several people share results, roles need dashboards, or you want hosted labeling and judge runs. Either way the disciplines stay: the atlas moves into the tag system, the ladder becomes scorer config, variance and the fidelity register run as before. Build once first; the trace schema exports to OTel, so buying later is never locked out.

## Frameworks

**Three problems single-turn evaluation never had**

| Problem | What it means | Answer |
|---|---|---|
| the world gets dirty | the previous case's refund contaminates the next case's query | reset from seed before every case |
| actions leak out | the worst a tool call can do is real money and real mail | stubs wedged between actions and the world |
| the counterparty is alive | turn 3's input depends on turn 2's output | freeze it (replay) or improvise it (synthetic user) |

The core problem moves from "preparing inputs" to "rebuilding the world".

**Personas** (aligned with the case schema's persona enum)

| Persona | Core behavior | What it tests | Held-back design |
|---|---|---|---|
| angry | pressure from turn 1, over-limit demand, stakes rise each turn | commitment red line, tone | ID in turn 1, real amount in turn 2 |
| vague | cannot produce the order ID, inconsistent description | follow-up and verification, "just guess one" | ID never in turn 1; item named in turn 2 |
| multi | three asks at once, a fourth midstream | task tracking, omissions | never volunteers which item was missed; one "what about the rest?" |
| cooperative | ordinary user, no trouble | baseline service quality | none |
| long (variant of any) | holds held-back info past turn 6 | committing early and never revising | past turn 6 |

**Three distortions, three checks** (5 conversations per persona; 10 after a script or base change)

| Distortion | Check | Criterion |
|---|---|---|
| too cooperative | read turn counts: in which turn does angry relent | compare with how long real complaint tickets hold out; cooling off after two turns is distortion |
| too dramatic | blind mix: shuffle synthetic messages among real ticket messages, a colleague picks the acted ones | beating chance by a clear margin means the tone gave itself away |
| talked out of its position | read endings: share of conversations where the user abandons the demand, then read each one | did the agent solve it, or did one explanation disarm the actor |

**Replay fidelity levels** (the iron rule spans all three: deviation raises an alarm, never a forced verdict; escalate one level)

| Level | What is frozen | Model re-reasons? | Tests | Cost / variance | Voided when |
|---|---|---|---|---|---|
| 1 verdict-layer replay | the trace itself | no | the verdict logic (assertions, differ, stats, report) | zero model calls, byte-deterministic | the trace changes |
| 2 fixed-input rerun | case, seed, stub returns, user lines | yes | the agent, in a deterministic environment; red can only come from the agent's side (sampling luck included) | cheapest floor that runs the model | the agent leaves the recorded track (unexpected tool, uncontained branch) |
| 3 free simulation | nothing; synthetic users improvise | yes | new branches, conversational resilience | highest | never; it is the top |

"Deterministic replay runs on every commit" means level 2; "deterministic" refers to the environment half. The derail rate is the iron rule turned into a metric (see references/gating-releases.md).

**Six components**

| Component | Job |
|---|---|
| runner | reads cases, resets the world, starts the agent (wiring a synthetic user when needed), collects traces, manages `--repeat` |
| trace | writes trajectories to disk per the schema |
| assertions | deterministic verdicts, the ladder's floor |
| judge | the calibrated judges (`judge-tone-commitment`, `judge-report-rubric`) |
| stats | intervals, significance, flip rate |
| report | layered by sev, verdict sources visible, intervals attached, never only the average |

**Fidelity gap register.** A stub stricter than the real system → false alarms, annoying but harmless. A stub more lenient → fatal; every crack where offline goes all-green and production flips over lives there (e.g. the real gateway errors on a second refund of the same order while the stub quietly succeeds; real mail has latency and bounces while the outbox receives instantly).

**Build-or-buy concept map**

| Here | Platform term | Does not migrate by itself |
|---|---|---|
| case set | dataset | `setup` (world prior state) usually has to go into metadata |
| assertions + judge | scorer / evaluator | the tier discipline (sev-1 never released by a judge alone) |
| one eval run with intervals | experiment / run | `--repeat` and intervals; platforms default to a single pass |
| trace (JSONL) | trace / span tree | lossless via OTel |
| verdict record | annotation / feedback | `judged_by`, `first_bad_step` need custom fields |

What the platform hosts is infrastructure; judgment cannot be hosted (defining good, calibrating the judge, registering stub gaps stay yours).

**OTel GenAI mapping.** The whole trajectory is the root `invoke_agent` span; `steps[].type: model` → `chat` span with `gen_ai.usage.input_tokens / output_tokens`; `tool_call/tool_result` → `execute_tool` span (`gen_ai.tool.name`); `subagent` → nested `invoke_agent` sub-tree.
`inbound` (custom event, suggested attribute `inbound.source`), `usage.cost_usd`, `case_id`, `plan`, `memory_write` have no standard counterpart and go out as custom attributes.

## Self-check

Sentence: "It all passes against the stubs, so it will pass in the real environment."
Reality: a sandbox pass rate is capped by stub fidelity; every place a stub is more lenient than the real system is a crack where offline is all-green and production flips over.
Check: open the stub inventory and count the rows in the gap column; zero means nobody looked; register at least one known gap per stub with the class of verdicts it affects written down.

## Templates

- `templates/harness-spec.md`: the six-component data flow, the stub/real boundary table, and the replay/simulation layering (what runs on every commit vs every version).
- `templates/stub-inventory.md`: per-stub behavior and the fidelity gap register, reconciled row by row against real traffic.
- `templates/persona-library.md`: the four-element script per persona and the fidelity spot-check table.

## Migration notes

- The six components carry no domain knowledge and move as a whole; only `world/` and `synth/` get swapped. Draw your own stub/real table first, then decide which components plug in tonight.
- Coding agents: the sandbox is a throwaway git repository (reset = check out again); the test suite is a ready-made assertion layer; reset must also wipe caches and prior git history the agent could read answers from.
- Research agents: the sandbox is a frozen corpus snapshot; the synthetic user becomes a synthetic reviewer; outbound publishing and citations land in an outbox stub.
- Professional-judgment agents: the fidelity gap register is where regulated behaviors of real systems (audit trails, confirmation records) that the stub omits get written down before the silent/shadow rung (see references/going-live.md).
- Platforms: dataset / scorer / experiment / trace map one to one; insist on `setup`, `--repeat`, and `judged_by` as custom fields.
