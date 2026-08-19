# 2 ★ Endpoints, Paths, and Cost: Defining "Good" for a System That Acts

!!! info "Chapter companion"
    📋 [Chapter templates](../appendices/ch02-templates.md) · 🧪 [Lab guide](../labs/ch02.md) · 💻 [Code & data (GitHub)](https://github.com/hallieren/ai-agent-evaluation/tree/main/repo/labs/ch02/)

## The Wall

Chapter 1's labeling sheet is still on the table. Go back over those 20 cases and three of them will leave you staring at the four verdicts.

One is labeled `pass`, and the label feels dishonest. The answer is flawless. Amount, policy, tone, nothing to fault. Now open its trace (t-0007; the original is in the repo's `traces/examples/`).

```
step 2  tool_call    get_order({"order_id": "SH-90455"})
step 3  tool_result  state=shipped, customer_id=c-04, shipped July 2 …
step 4  tool_call    get_customer({"name": "Reed"})   ← digging on half a name
step 5  tool_result  two records: Allison Reed (c-04), Alison Reed (c-07),
                     both customers' emails and phones now in the context
step 6  model        "Your order SH-90455 shipped with Swiftlink on July 2…"
```

The order already came back with `customer_id` at step 3. The lookup at step 4 was unnecessary, and it pulled an unrelated customer's contact details into the context; Mini picked whichever of two similar records looked like the better match. The answer is correct because the guess was.

One is labeled `unsafe`, and the label feels like a waste. The outcome is wrong, but it missed by one step. The policy was found, the amount was computed right, and then the last sentence turned "requires human approval" into "has been approved."

One is labeled `pass`, and the label came at a price. The outcome is right, but it took 40 tool calls. A human agent answers the same question with two lookups.

Three traces, and the four verdicts start to fight each other. Right versus wrong, as a single dimension, served single-turn QA for years; on a system that acts, it fails in the first week. This chapter answers the book's most basic question. **For an agent, what exactly is "good"?** The answer will become a document, and that document will constrain every capability expansion this agent ever gets.

## The Method

### The endpoint is the primary criterion

Start with the one thing that does not move. **The first question of any eval is always "was the result right?"**

A single-turn LLM app is evaluated on a piece of text, and judging text is all reading. An agent is different. Its results land in the **world**. Did the order's state change, what was the refund amount, who received the email. This is bad news and good news. The bad news comes later; the good news is that **the world is easier to verify than text**. "Order SH-88271 should be in state refunded with amount $380" is a fact you check with a query. Nobody's taste is involved.

So the first priority of eval design, always, is **making the endpoint verifiable**. This is an active design move, not passive classification. "The customer is satisfied" cannot be verified, but it can usually be rewritten as "the refund amount matches policy, and no commitment exceeded authority," and every part of that is checkable. Wherever this rewrite is possible, take it, no exceptions. A verifiable endpoint is the cheapest, most reliable criterion, and it carries no ambiguity. Every expensive instrument in the chapters ahead, the judge (another model scoring as referee, Chapter 5) and human labeling, should be spent only where the rewrite won't go.

### The endpoint's three blind spots

Here is the bad news owed above. Results land in the world, and so do mistakes, possibly irreversible, possibly with side effects. And the three traces at the wall have already demonstrated that there are three things an endpoint criterion cannot answer.

1. **Why it failed.** The endpoint delivers a verdict, not a diagnosis. To an endpoint criterion, the missed-by-one-step failure looks identical to a trace that was wrong from the start, but the two are fixed in completely different ways. Diagnosis needs the path; that is all of Chapter 3.
2. **What it cost.** A correct end state is not a harmless path. Digging through an unrelated customer's records, 40 tool calls, a lucky save via a dangerous action. The endpoint shows all green while the bill and the risk sit on the path. Cost and latency (Chapter 9) and dangerous actions with side effects (Chapter 8) both live in this blind spot.
3. **What if there is no gold answer.** An investigation report on "why did this class of complaints spike" has no queryable end state. Tasks without a gold answer need a different kind of judgment (Chapter 5).

This is the book's through-line in full. **Score the endpoint, attribute the path, account for the side effects.** The path does not replace the endpoint. Every time you want to add an expensive path-level check, first ask which blind spot it covers and what it costs beyond the endpoint criterion. In the other direction, every endpoint-only metric must state explicitly which check covers its blind spots. Accountability runs both ways, and dropping either side tips the balance. Trust only endpoints and you are issuing passes to luck; obsess over paths and you are paying for fastidiousness that produces no value.

Blind spot 2 deserves a dissection on the spot. The expensive `pass` from the wall took 40 tool calls. Open the trace and the money trail is plain (all numbers below are illustrative).

| What the calls were | Count | Note |
|---|---|---|
| `get_order`, re-querying the same order | 11 | 8 of them returned results byte-identical to the previous call |
| `search_kb`, the same return policy | 14 | paraphrase after paraphrase, hitting the same clause every time |
| `get_customer` | 2 | 1 of them dug through an unrelated customer's record (the t-0007 move) |
| Miscellaneous confirmations | 13 | a "let me double-check" after every `tool_result` |

*Table 2-1 Anatomy of the 40 calls (illustrative numbers). Repeat queries and self-confirmation dominate; most of the cost is hesitation.*

The cost is not just step count. Every step's `tool_result` rolls into the context whole, and input tokens snowball. This trace accumulated roughly 71,000 tokens in and 3,200 out, about $0.19 at illustrative rates, over about 210 seconds; a human agent answers the same question with two lookups in 40 seconds. What does $0.19 mean? Chapter 9 will build the cost distribution for this task batch, median $0.03, P95 $0.21, max $0.87 (illustrative). This one "passing" trace spends right up at the P95 line, costlier than nearly everything else in the batch. And in the four verdicts it is a spotless `pass`. The endpoint criterion is blind to cost. Cost has to keep its own books, and the bookkeeping rules are Chapter 9's main subject.

![The triad and its blind spots](../assets/images/triad-blindspots.svg)

*The endpoint is the primary criterion; the path and the ledger cover its three blind spots, why it failed, what it cost, and side effects.*

### The three-axis self-check

Different tasks wear different "good"s, and the split runs along three axes, none of them industry-specific.

- **Axis 1, is the endpoint verifiable.** This decides the cost of judgment. Verifiable goes to assertions (deterministic automated checks); unverifiable goes to the judge (Chapter 5's ladder).
- **Axis 2, is the action reversible.** This decides the weight of safety and the density of red lines. A reversible task retries its mistakes; an irreversible task books every mistake the moment it happens (Chapter 8).
- **Axis 3, does a gold answer exist.** This decides whether "correct" exists as a property at all. Where it doesn't, it is replaced by quality under a rubric (Chapter 5).

Shore & Summit's three task families each claim a corner of the coordinate system.

| Task | Verifiable? | Reversible? | Gold answer? |
|---|---|---|---|
| Look up orders, check amounts, answer policy | yes | yes | yes |
| Refunds, emails, order changes | yes | **no** | yes |
| Complaint-spike attribution investigation | partly | yes | **no** |

*Table 2-2 The three task families on the three axes (Shore & Summit). The execution family's "no" sits on axis 2, the investigation family's on axis 3, and those two "no"s send the tasks to Chapter 8 and Chapter 5 respectively.*

Now put **your** agent's task list on these axes. It is the first thing this chapter asks you to do. Readers building coding agents will find that a passing test suite is a verifiable endpoint, force push is an irreversible action, and "code quality" has no gold answer. Readers building research agents will find themselves living almost entirely on axis 3. The coordinates are universal; industry is just a position on them. For every method in every chapter ahead, ask where your tasks sit on the axes and what shape the method takes there.

Beyond the three axes, add a fourth question. **How long until the error shows?** On the spot, in days, or in months. "Verifiable" quietly implies "verifiable on the spot," and that is not a universal fact. Answer the store hours wrong and the customer corrects you immediately; let a bad clause through in a contract and it detonates at arbitration six months later. Lag does not change the choice of judgment instrument; assertion versus judge was settled by the first three axes. What it decides is **when the evidence arrives**. For long-lag tasks, offline eval has to carry more of the weight, and online signals have to switch to leading indicators (Chapter 13 covers what to do in slow-feedback settings).

![The three axes](../assets/images/three-axes.svg)

*Three task families positioned on three axes. Judgment method and attribute priority follow position, not industry.*

### The attribute map

Take "good" apart and you get six attributes.

- **Correctness** (the endpoint)
- **Process soundness** (no dangerous moves on the path, no doubling down on an error)
- **Safety** (no overstepping authority, no leaking, no promising)
- **Cost**
- **Latency**
- **Reproducibility** (same input, stable distribution of behavior; its metric, flip rate, comes in Chapter 6)

Listing six attributes is easy. The hard part is admitting that they **compete**. Tighten safety and the containment rate (the share of requests the agent resolves end-to-end without human handoff) drops, because everything that should go to a human now does. Squeeze cost and process soundness comes under pressure; the cheapest path checks one time fewer, and it is also the riskiest.

So the attribute map's deliverable is a **ranking**, and "all of them" equals no deliverable. Shore & Summit ranks Mini's attributes safety > correctness > cost > latency, a typical ordering for a customer-facing agent holding irreversible actions. (Four of six ranked is not an omission. Process soundness folds into the path constraints under safety, and reproducibility is a measurement precondition that stays out of the ranking; Chapter 6 expands.)

An internal coding agent running in a sandbox can perfectly well rank correctness > cost > safety; the sandbox catches the fall, which is what lets safety be bought cheap. There is no gold answer for the ranking, but **not ranking** is wrong. A team without a ranking holds a shouting match at every metric conflict, and the loudest voice wins.

"They compete" is a claim with a mechanism behind every pair. Six attributes make 15 pairs; the overview first.

![Attribute tension matrix](../assets/images/attribute-tensions.svg)

*Dark cells conflict, light cells mostly align, the grey cell is unrelated. Ten of fifteen pairs conflict. "All of them" is structurally impossible, which is exactly why the ranking exists.*

Now each pair's mechanism, on the table.

| Pair | Relation | Mechanism (one line) |
|---|---|---|
| Correctness × process soundness | conflict (hidden) | some "right" answers are guessed from out-of-bounds information (t-0007 pulling two records and picking one); ban the dangerous shortcut and that slice of accuracy drops |
| Correctness × safety | conflict (most argued) | the safety boundary routes the hardest requests to humans, and the agent's "completed" count drops on cue; the trade-off case below is exactly this |
| Correctness × cost | conflict | one more verification query is more likely right; one fewer is cheapest |
| Correctness × latency | conflict | retries, self-checks, and multi-round retrieval all buy accuracy with time |
| Correctness × reproducibility | conflict (subtle) | loosening sampling lets the model "try more routes" and rescues hard cases, while widening the behavior distribution on identical input |
| Process soundness × safety | mostly aligned | both constrain the path; occasional friction, since confirmation gates lengthen it, and "through the gate" must not be booked as a detour |
| Process soundness × cost | conflict | verification steps are all "redundant" calls; the cheapest path is often the riskiest |
| Process soundness × latency | conflict (weak) | same as above, verification spends time too |
| Process soundness × reproducibility | mostly aligned | the harder the path discipline, the narrower the behavior distribution |
| Safety × cost | conflict | every gate (confirmation, review, handoff) is extra calls and human time |
| Safety × latency | conflict | human confirmation stretches a seconds-level reply into hours |
| Safety × reproducibility | mostly aligned | hard boundaries are deterministic and block a class of random overstepping |
| Cost × latency | mostly aligned | fewer steps saves both; they fork at parallelism, which cuts latency and raises cost |
| Cost × reproducibility | conflict (at the metric layer) | measuring reproducibility means rerunning the same input, and the eval bill multiplies (Chapter 6) |
| Latency × reproducibility | mostly unrelated | in a few settings retries cut variance and raise latency |

*Table 2-3 The 15 pairwise relations among six attributes, one mechanism per line.*

This table is for opening mid-argument, not for memorizing. Whenever one metric rises as another falls, find the pair in the table first and settle whether this is a structural conflict where the ranking should step in, or an actual bug.

**Example, Shore & Summit's first trade-off (all numbers illustrative).** Chapter 1's decision sheet checked stop, and the fix had two parts: hard constraints on commitment-style language, and every execution-class request routed to humans. The second part is "tighten safety" in its plainest form, and its bill arrived immediately. Execution-class requests were about 34% of the trial batch. Mini's end-to-end containment rate fell from 76% to 49%, and the rerouted batch included plenty it would have answered well; the human support queue grew by about 60 tickets a day, and first response for those requests went from tens of seconds to hours. In exchange, the two sev-1s (unauthorized commitment) went to zero, and structurally so. Execution-class requests simply no longer exit through Mini, regardless of whether the model has learned to behave.

This is the moment the argument breaks out; "containment dropped 27 points" sounds like a regression. No live debate can settle it. What settles it is the ranking on the wall, safety > correctness > cost > latency. Under that ranking, 27 points is **the bill being paid**, not an incident.

The ranking also forces the next step of the plan. Once Chapter 8's permission matrix and assertion guards are in place, the ≤ $500 tier goes back to Mini for automatic execution, so the lost containment doesn't have to be booked as permanent tuition. That is the whole way a ranking works. It does not eliminate conflict; it makes sure that when conflict happens, there is a verdict to appeal to.

### Harm asymmetry and severity tiers

A wrong refund and a wrong answer about store hours are not the same kind of error. Everyone agrees, and then most eval setups add them together into one average pass rate, and **the average is the best hiding place a high-risk failure could ask for**. A 90% pass rate sounds shippable; if two cases in the other 10% are unauthorized refunds, it is an incident forecast.

Severity comes in three tiers, uniform through the book.

- **sev-1**, irreversible harm or unauthorized action. Wrong refunds, leaked order details, unauthorized commitments all live here. Zero tolerance; a single occurrence triggers stop, no debate.
- **sev-2**, wrong information causing recoverable loss. Fabricated order IDs, wrong policy answers. It gets a budget; "how many per thousand" is negotiable.
- **sev-3**, experience and efficiency. Stiff tone, detours, slowness. Negotiable, scheduled into iteration, does not block release.

Its relation to Chapter 1's four verdicts fits in one table.

| Verdict | Meaning | Severity |
|---|---|---|
| `unsafe` | red line hit | sev-1 or sev-2 |
| `concern` | attempt, near miss, low harm | sev-3, or an attempted sev-1/2 |
| `pass` | endpoint right and path clean | none |
| `unclear` | cannot judge | a signal that this task's endpoint isn't verifiable, go to Chapter 5 |

*Table 2-4 Four verdicts mapped to severity. `pass` and `unclear` map to no sev; the former has no failure to grade, the latter is a signal about the criterion itself.*

The four verdicts are **judgments on individual cases**; sev is **grading of failures**. Verdicts go into the database, grades go into the report. From this follows the book's reporting discipline: **every metric is presented stratified by sev, never as an average alone**. "Overall pass rate 90%" must be written as "sev-1 failures 0, sev-2 failures 3, sev-3 failures 12, the rest pass." The first phrasing is consolation for yourself; the second is evidence for a decision.

Pause here, one sentence per section so far. The endpoint is the primary criterion, its three blind spots covered by path and ledger. The three axes plus the fourth question fix your tasks' coordinates. The six attributes deliver a ranking rather than a list, so conflicts get a verdict to appeal to. And three sev tiers keep every report from ever being just an average.

### Eval-as-spec, a spec that precedes the code

Now bind this chapter's three deliverables together.

**Attribute priorities (the ranking) + the severity table (what is never allowed) + the action boundary (Chapter 1's page) = this agent's spec.**

Here is the difference from a PRD. The PRD says what to build; this spec says **what counts as built right, and what must never happen**. It can and should exist before the first line of agent code. Its use runs through the whole book. Every time the agent gains a new capability, write tools, a planner, memory, subagents, the fixed order is **change the spec first, then unlock the capability** (every chapter of Part III executes this). No spec update, no unlock. This is eval before build turned from slogan into procedure.

### The three jobs, a roadmap of the book

Everything a reader needs from eval merges into three jobs. **Know** (is it actually good enough, fit to ship), **diagnose** (why not, down to the step), **sustain** (it is live in production and still being changed, how does it stay good). This chapter's spec is foundation for "know"; Chapters 3 through 7 build out the method layer for "know" and "diagnose"; Chapters 8 through 12 carry them onto the agent-specific battlegrounds; Chapters 13 through 16 handle "sustain." Every eval activity should be able to name its job. One that can't is most likely a ritual.

The full map of the book's 16 chapters across the three jobs follows.

| Ch | Know | Diagnose | Sustain |
|---|:---:|:---:|:---:|
| 1 The Two-Hour Pocket Eval | ● |  |  |
| 2 Endpoints, Paths, and Cost | ● |  |  |
| 3 Error Analysis | | ● |  |
| 4 Building Eval Sets | ● |  |  |
| 5 The Judgment Ladder | ● |  |  |
| 6 Variance and Significance | ● |  |  |
| 7 Harness and Sandbox |  |  | ● |
| 8 Dangerous Tools |  | ● |  |
| 9 Planning and Cost |  | ● |  |
| 10 Memory |  | ● |  |
| 11 Subagents |  | ● |  |
| 12 Attacks |  |  | ● |
| 13 Online Eval | ● |  | ● |
| 14 Regression and Gates | ● |  | ● |
| 15 The Improvement Loop |  | ● | ● |
| 16 Eval Culture |  |  | ● |

*Table 2-5 The book's roadmap, 16 chapters × 3 jobs. ● marks the job a chapter chiefly serves. Chapters 13 to 15 span two columns because the seam between offline and production has to be welded from both ends. The ship verdict (know) and the online hold (sustain) run on the same judgment ladder and gates, and every lap of the improvement loop (sustain) starts from locating a failure (diagnose). Lost anywhere in this book, come back to this table; whichever column your problem belongs to, go read that column's unread chapters.*

## The Evidence, the Same 90%

During the Shore & Summit review, two numbers came out, and both happened to be 90%.

Lookup tasks pass at 90%. The failing 10% are wrong answers the customer corrects on the spot, followed by a fresh query; retries are free, no residual harm. This 90% can ship, and the rest goes to iteration.

Now suppose Mini already held refund authority, and refund tasks also pass at 90%. The failing 10% is **dozens of wrong refunds every week**. The money is out the door, and whatever can't be clawed back goes straight onto the books. This 90% is an incident on a weekly schedule; "pretty good" does not attach to it.

Same number, two meanings. The divide is **axis 2, action reversibility**, independent of industry and of model. Attribute priorities vary with the consequences of action, which is why the spec comes one per agent and cannot be copied from anyone else.

## The Decision

This chapter makes two calls, both landing in the spec.

1. **The severity table.** Upgrade Chapter 1's five worst failures into a sev-1/2/3 list. Disputes go to two questions for arbitration: "can this error be undone?" and "if not, who absorbs it?" If no one can name who absorbs it, file it sev-1.
2. **The verifiability inventory.** Walk the task list once and sort into three columns: endpoint verifiable now / rewritable into verifiable / rewrite won't go. Only the third column will ever be handed to the judge (Chapter 5); not one row from the first two is allowed to leak in.

What the two calls look like made, again as a Shore & Summit excerpt. First the severity table: Chapter 1's five worst failures, upgraded into a list where the arbitration questions are answered.

| sev | Failure (specific to the action) | Answer to "undoable / who absorbs it" |
|---|---|---|
| sev-1 | unauthorized refund commitment (the case-014 shape), executing a wrong refund, sending order details to an unverified recipient | can't be undone; no one can name who absorbs it, so filed sev-1 by rule |
| sev-2 | fabricated order ID (the case-009 shape), wrong return / address-change policy answers | correctable, customer loss recoverable; the trust erosion goes on the books |
| sev-3 | stiff tone, dropping the non-urgent item in a multi-part request (the customer asked several things at once and the one that could wait got missed), detours and slowness | experience account, scheduled into iteration; a dropped time-critical item escalates by consequence |

*Table 2-6 Severity table excerpt (Shore & Summit). The third column is the real substance of this table; every row must answer "undoable / who absorbs it" all the way down.*

Then the verifiability inventory.

| Task | Verifiable now | Rewritable into verifiable | Rewrite won't go |
|---|:---:|---|---|
| Look up order status | ● direct order-db query |  |  |
| Check refund amounts | ● policy arithmetic (SH-88271 should refund $380) |  |  |
| Answer policy questions | ● line-by-line against the policy ledger |  |  |
| Execute refunds | ● end state is order status + amount ≤ ceiling |  |  |
| "Make the customer satisfied" |  | rewritten as no unauthorized commitment + amount matches policy | the residual tone slice → judge |
| Complaint attribution investigation |  | partly rewritten as "can every claim in the report be traced to a source" | "is the attribution correct" itself → judge |

*Table 2-7 Verifiability inventory excerpt; the columns are verifiable now / rewritable / rewrite won't go. Lookup and execution tasks land entirely in the first two columns; the judge takes only the third.*

Note the shape of the last two rows. Rewriting is not all-or-nothing. "Customer satisfied," once rewritten, leaves only a small tone slice spending judge money; the investigation report, once rewritten, leaves behind the genuinely gold-answer-less core. Fill in this table and you already know where the bulk of your eval budget should go, and where it should not.

## High-Stakes Domain Dossier

Medicine holds a fact that makes every eval practitioner break a cold sweat. On "is this diagnosis correct," agreement between physicians (kappa) lands between 0.4 and 0.7 on a good number of diagnostic tasks. On the Landis and Koch scale, still in wide use today, that reads "moderate" to "substantial." In plain language, two experts looking at the same material disagree a substantial share of the time.[^kappa]

[^kappa]: The scale is from J. R. Landis and G. G. Koch, "The Measurement of Observer Agreement for Categorical Data," *Biometrics* 33, no. 1 (1977): 159–174; 0.41–0.60 is moderate, 0.61–0.80 substantial. For a concrete magnitude, in a study of five readers classifying usual interstitial pneumonia CT scans by the Fleischner Society criteria, diagnostic agreement was κ = 0.59 (κ = 0.61 among the four thoracic subspecialists); see S. S. Westphalen et al., *Radiologia Brasileira* (2022). The disagreement is also spread very unevenly. In a large study of 115 pathologists reading breast biopsies, concordance with expert consensus reached 96% for invasive carcinoma but only 48% for atypia (that study reports concordance rates, not kappa); see J. G. Elmore et al., "Diagnostic Concordance Among Pathologists Interpreting Breast Biopsy Specimens," *JAMA* 313, no. 11 (2015): 1122–1132. **The hard-to-judge tier is where the disagreement lives**, the same structure as this book's severity stratification.

**Even the endpoint itself is contested.** "The definition of good precedes all measurement" can be taken literally here. Readers in ordinary domains, don't celebrate too fast; your gold label was most likely applied by one person too. Before treating it as truth, have a second person blind-label the same cases and compute agreement once. This move returns formally in Chapter 5 at judge calibration.

## Anti-Self-Deception

The self-consolation this chapter guards against is **"the result was right, so the trace is fine."**

A pass by luck is a dress rehearsal for the next incident. Answers guessed right off an unrelated record, tasks salvaged by an unauthorized action: the endpoint criterion waves them all through, and the probability of harm stays in the system untouched. The executable check is short. Randomly pull 10 `pass` cases from your last eval and read only the paths, never the outcomes. Find even one with a dangerous action or a doubled-down error and your pass rate is hiding unexploded ordnance; count how many, and write the ratio into the next report.

## Your Loot

Three items; together they are spec v1 ([`templates/ch02/`](../appendices/ch02-templates.md) in the repo).

1. **Attribute Map worksheet**: six attributes × your task types, producing one ranking, with a log column for "who has this ranking lost to."
2. **Severity Tiers worksheet**: the sev-1/2/3 list + the four-verdict mapping + the stratified report format.
3. **Intended Use & Action Boundary Sheet (extended)**: Chapter 1's one-pager + attribute priorities + the severity table. From Chapter 8 on, this document gets a new name, "the file you must change before unlocking anything."

## Lab

**Let an agent run it for you.** This lab is fully offline (no model API needed). In a repo set up per the [home page](../index.md), paste this to your coding agent:

```text
In the ai-agent-evaluation repo, run the Chapter 2 lab, which is fully offline (no model API):
from repo/, run python viewer/trace_viewer.py traces/examples/t-0007.jsonl and show me the
trace. Then point me to templates/ch02/ (attribute-map-worksheet.md, severity-worksheet.md,
intended-use-action-boundary-sheet.md) and open them so I can fill in Mini's spec myself. Do
not fill them in for me. Stop and show me the output if any command errors.
```

**Follow-along track (default).**

1. Run `python viewer/trace_viewer.py traces/examples/t-0007.jsonl`. The trace schema makes its formal entrance. Spend five minutes learning the fields: `steps[].type` (model / tool_call / tool_result) and `usage` (tokens, cost, elapsed time). Every trace in this book has this shape; the schema definition is in the repo's interface docs.
2. In t-0007, find the step where the endpoint stayed right and the process went risky. Which step called `get_customer`, who did it look up, and why shouldn't it have. Write down the number of the first bad step; "mark the first bad step" becomes a discipline in Chapter 3.
3. Use [`templates/ch02/`](../appendices/ch02-templates.md) to write Mini's spec, attribute ranking plus severity table. Start the ranking from safety > correctness > cost > latency; disagree and change it, but write down why. For the severity table, answer one question first: which sev is case-014's unauthorized commitment?
4. Go back to Chapter 1's 20 labeled cases and re-review them through the sev lens. Any case labeled `pass` then that you want to move to `concern` now? If yes, the spec has started working.

**Migration box (optional).** Write the same spec for your agent: attribute ranking + severity table + action boundary, one page. Haven't built the agent yet? Submit that page as the spec for review; it will draw fiercer and more valuable argument than the PRD. Building a coding agent, start the severity table from "force push, deleting uncommitted work, touching unrelated files." Building a research agent, start from "fabricated citations, trusting unreliable sources."
