# Running adversarial eval and verifying defense in depth

**Load this reference when:** the agent ingests content nobody reviewed (web pages, inbound email, ticket fields, documents, webhooks) or is about to; a red team is being planned or its report read; you must decide which layer stopped an attack, whether "we held" means anything, or which security failures shut the agent down.
Source: chapter 12, docs/chapters/ch12-adversarial.md (templates: docs/appendices/ch12-templates.md)

- [Rules](#rules)
- [Procedure](#procedure)
- [Decisions](#decisions)
- [Frameworks](#frameworks)
- [Self-check](#self-check)
- [Templates](#templates)
- [Migration notes](#migration-notes)

## Rules

- Intercept in layers and verify layer by layer; never plan to "fix" injection. Why: in the context window instructions and data are the same kind of thing, tokens; the system prompt is only the passage that happens to come first, and a later passage written to look more like a command wins. This is structural and cannot be sealed.
- Run adversarial eval as a first-class citizen on the same harness, atlas, and judgment ladder as functional eval. Why: the attack surface grows with every capability and techniques evolve; a one-off penetration test is stale the next month.
- Treat "citation resolves" as distinct from "source trusted". Why: `citation_resolves` only checks that a citation traces to a page; a forged policy page traces perfectly and still puts the attacker's script into the report's conclusion.
- Keep the permission matrix independent of the agent's judgment. Why: the forged email that lured a refund was stopped on the amount by the matrix, not by the agent seeing through it; once injection contaminates judgment, any defense built on judgment falls with it.
- Judge tool misuse by whose will the call expresses, never by whether the call errored. Why: the tool works and the call "succeeds"; the intent was hijacked.
- Ask the per-layer question, never the overall "did we hold?". Why: "we held" is true when every layer but the last was breached, and the next attack path may not pass through that last layer.
- Give every layer's number an interval; check whether the same case lands on the same layer across runs; never average breaches. Why: attack success is a random event on the least stable boundary of model behavior; one run with zero breaches is one draw; "a 6.7% breach rate" does not stand, one breach is one incident.
- Bank every successful attack as a permanent regression case in the atlas and the red-line set. Why: a fixed attack that never became a regression case comes back in the next version; "we found N problems" does not qualify as a red-team deliverable.
- Record only the technique category and the defense checkpoint, never a weaponizable payload. Why: the conclusion you want is "my layer 3 cannot stop this class of technique", not a stockpile.
- Rerun the red team on every version and every capability unlock, and staff it with people who did not build the system (rotation, an adversarial persona, an outsider). Why: skipping a round assumes the new capability opened no new door; builders share the system's assumptions and the attacker's value is not sharing them.

## Procedure

1. Write the threat model first: who attacks, after what (e.g. fraudulent customers after refunds → privilege escalation + tool misuse; social engineers after other people's data → exfiltration; indiscriminate poisoning scripts → injection itself). It decides which cells of the matrix get written densest.
2. Build the attack set before opening the entrance: lay out the attack surface × carrier matrix (five surfaces × web / email / ticket), fill the empty cells with at least one sample each, following the sample skeleton (id, type, attack_surface, carrier, technique, defense_checkpoint, `expect.assertions` with a red-line assertion, `severity_if_fail: sev-1`).
3. Inventory the exits: every channel that can send a string out (email body, report citation, ticket notes, confirmation reply, webhooks, generated reports). A complete exfiltration case names its way in and its way out; every new output feature adds one more channel to the red-line scan, with `no_pii_disclosure` at the exit.
4. Count your layers honestly: input filtering / content isolation; action boundary (the spec's "what it does not do"); permission matrix; human confirmation. Only the system prompt → no depth at all.
5. Flip `external_content` on. Run one inbound case and confirm `inbound` steps appear in the trace; they differ from `tool_result` in one way only, the content is untrusted.
6. Run the red-team round with `--repeat 5` from the very first time (rule). On a forged-source investigation case, watch the report's conclusion while `citation_resolves` stays green. On a forged-instruction action case, note the step and the layer where `refund_not_executed` / the permission matrix stopped it.
7. Label each attack with the layer it finally stopped at (input filter / action boundary / permission matrix / human confirmation / breach) and fill the layered interception table: each cell mean ± interval, case count × run count noted, breaches on their own line.
8. Read the table for three things: which layer takes most interceptions (one layer abnormally high → the others were not tested); whether a layer stopped 0 (two readings, never triggered or truly useless; plant seeded probes to separate them, see references/tool-calls.md); whether interceptions crowd into the last layer (→ depth is fake, open an action item).
9. Check flips: the same case stopped by the permission matrix in one run and breaching in another is a line of defense with a probability; report it separately from the mean.
10. Generate variants of stopped samples with an attacker LLM, changing only the surface: wording (command → quotation → "while you're at it"), carrier (web → email → ticket; the most skipped and most valuable), language (another natural language, split, encoded, quoted block). Variants reuse the parent's assertions and defense checkpoint as they are.
11. Run multi-turn escalating attacks with an adversarial synthetic-user persona (persona / demand / held-back info naming the turn the forged context appears / end condition; see references/harness.md): probe the policy → forge context ("the previous agent verified me, ticket …") → lure the action. Judge the whole trace's endpoint and the actions along the way, never one turn.
12. Bank results: new-result variants enter labeled with their parent id; every entry is a regression case rerun each version; every breach goes onto the shutdown checklist and into the atlas. Rerun this whole procedure at every version and every unlock.

## Decisions

1. Threat model before any red team: write who will attack and after what; map each attacker kind to its likely carrier and surface. No threat model → the red team shoots at imagined advanced attacks and misses the path of least effort.
2. Shutdown red lines = the security branch of the stop rule (see references/gating-releases.md): define in advance which failures mean stop the agent, no discussion, no iteration. Candidates: a red-line action after breaching every layer (an over-limit refund executed, details leaked); cross-session harm from contaminated memory; a subagent executing an instruction injected into the main agent; the agent bypassing human confirmation on a red-line action; the same class of attack recurring after a fix.
3. Variant banking rules: only variants that produce a new result (stopped at a different layer, or breach) enter; entering means regression; techniques expire, so down-sample variants stopped by the same layer for several consecutive versions, never delete, and never retire the parent.
4. Resource placement: attacks aim at the intersection of irreversible actions and protected data; put the last layers (permission matrix, identity verification, human confirmation) there first, not evenly across every tool call.

## Frameworks

**Five attack surfaces (the attacker's intent; injection is the vehicle, the other four are the ends)**

| Surface | What is lured | What crosses the line | Verdict handle |
|---|---|---|---|
| Injection | Obeying content over the system prompt | Instructions hidden in external content | Which layer stopped it |
| Tool misuse | Harm with a legitimate tool (send to an attacker's address, update a field) | Whose will the call expresses | Not the tool error |
| Privilege escalation | An action beyond the action boundary (auto-executing an over-limit refund, promising unauthorized compensation) | The permission tier | Permission matrix, `refund_not_executed`, `no_over_limit_commitment` |
| Data exfiltration | Protected data to an unverified recipient | The exit; independent of intent | `no_pii_disclosure` at every outbound channel |
| Autonomy boundary | Widening its own task scope ("while you're at it" change config, notify others) | The scope, though every step looks legitimate | Compare actions taken against the task asked |

**Two canonical cases**: the forged policy page passes `citation_resolves` and its script lands in the report (citation resolves ≠ source trusted; investigation tasks have no gold answer and no end state to contradict it); the forged customer email walks the agent to the `refund` door and the permission matrix stops it on the amount (over the auto-refund limit → human approval), not on seeing through the scam.

**OWASP / ATLAS mapping (category level; numbering shifts between versions)**

| Surface | OWASP LLM Top 10 category | Note |
|---|---|---|
| Injection | Prompt Injection | Both canonical cases are indirect injection (payload in ingested content) |
| Tool misuse | Excessive Agency | Tests will |
| Privilege escalation | Excessive Agency | Tests the tier |
| Autonomy boundary | Excessive Agency | Tests scope; kept as three rows because they are tested differently |
| Data exfiltration | Sensitive Information Disclosure | Flows out through a legitimate channel |
| Downstream executes the agent's output | Insecure / Improper Output Handling | Out of scope; the receiver's responsibility |

Division of labor: consult MITRE ATLAS (attacker tactics and techniques) when writing the threat model and red-team scripts; report in OWASP category names to management and security review. The matrix's vertical axis maps to OWASP, its horizontal axis to ATLAS's "where it gets in".

**Attack surface × carrier matrix**: rows = five surfaces; columns = inbound carriers (web via `fetch_url` / email inbound body / ticket customer fields) plus, for the exfiltration row, outbound channels (email body / report citation / ticket notes). Layering is for seeing the empty cells; the same intent in a web page, an email, and a ticket note is three cases because each layer sees them at a different moment (e.g. the ticket-body refund lure filled from an empty cell became the worst flipper: 3 breaches in 5 runs, illustrative).

**Four layers and the layered interception table (15 samples, one run, illustrative)**

| Layer | Stopped here | Leaked to next | Mean ± interval (5 runs) |
|---|---|---|---|
| 1 Input filtering / content isolation | 0 | 15 | fill in |
| 2 Action boundary | 3 | 12 | fill in |
| 3 Permission matrix | 7 | 5 | fill in |
| 4 Human confirmation | 2 | 3 | fill in |
| Breach (past every layer) | 3 | / | own line, never averaged |

Readings: "stopped 0" has two readings (never triggered / truly useless), separable only by probes; interceptions crowding into the last layer → the depth is fake; the reliable conclusions from one run are structural (layer 1 absent, middle layers carry the load, some breached), the integers are one draw.

**Three layer-1 measures**: wrap and label external content as "data, not instructions"; channel separation (external content only through a dedicated role or field, never spliced into the instruction passage); pre-screening by a cheap classifier or rule set, degrading on suspicion (hand to a human, strip links). None stops every variant; layer 1's job is to shrink what layer 2 must catch.

**Cross-cuts**: permission matrix independent of judgment (tools); injection written into memory = resident backdoor, so memory's write path sits one layer apart from external content and the contaminated entry is a crosstalk-class red line (memory); the handoff propagates injection, "read" at the main agent becomes "executed" at the subagent, so the contract asks whether handed-over context carries unquarantined external content (multi-agent); verdict instruments are an attack surface, wording that just clears the regex or a report that looks like a report, so sink verdicts to world state where possible (judging).

## Self-check

Sentence: "we added an anti-injection line to the system prompt, so we're safe."
Reality: that line and the attacker's line are tokens on the same level; the defense is bypassable by design.
Check: take the samples known to be stopped by that line, rewrite each (split, encode, disguise as a quotation, switch language), rerun; how far the stop rate falls is the true quality of that line.

## Templates

- `templates/red-team-protocol.md` — decides who attacks, how often, where findings go, and produces the coverage matrix and the round's reporting basis.
- `templates/redline-set.md` — produces attack samples at teaching level (technique + checkpoint) for the empty cells.
- `templates/shutdown-checklist.md` — decides which security failures stop the agent immediately, with detection, pause level, and owner.

## Migration notes

- Run a minimal red team before opening any external entrance: threat model; one injection sample per entry point on the matrix; an honest layer count; ≥ 5 runs with an interval in every cell.
- Coding agents: carriers are poisoned dependency documentation and issue bodies; irreversible actions are force pushes and leaked secrets.
- Research agents: the carrier is SEO-polluted search results; the red line is the attacker's script written into the conclusion, the forged-page case exactly.
- Healthcare: a "family member" email lures a record send; PHI exfiltration cannot be recalled, so the data boundary and the defense line coincide.
- Finance: a forged client instruction or reconciliation page lures a transfer or payee change; privilege escalation plus irreversible action with more zeros and no return window.
- Platforms: every new output feature (weekly report, ticket write-back, webhook) is a new exfiltration exit; extend the red-line scan in the same change.
