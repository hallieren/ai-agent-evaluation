# Appendix B · Mini Repo Map and Migration Guide

This appendix pays off three IOUs and adds a repo map. The IOUs are the platform concept isomorphism table from Chapter 7's sidebar, the module-by-module migration guide from Chapter 7's migration box, and the OTel field mapping from the interface contract.

## 1. The repo map

```
repo/
  mini/        the agent itself. llm.py is the only file in the whole repo that touches a model API
               (configured by environment variables, any OpenAI-compatible endpoint works); agent.py is
               the main loop and the five capability flags; tools.py is the registry of 13 tools.
  world/       the Shore & Summit sandbox: seeded SQLite DB + outbox stub + reset. world.py alone is the
               whole world; web/ is the "internet" behind fetch_url.
  harness/     the six components of the eval machine: runner / trace / assertions / judge / stats / report,
               plus differ (before/after diff) and caseyaml (a 60-line parser).
  cases/       seed-20 (Chapter 1), cases-50 (Chapter 4), redline (red lines), attacks (attack samples).
  traces/      t-0007 and pregen-60 (regenerated deterministically by generate.py, an offline script
               driving the real loop).
  synth/       the three synthetic-user personas (four-element scripts).
  viewer/      the terminal trace viewer.
  templates/   the 44 Your Loot templates (Appendix A is the index).
  labs/        chNN/: each chapter's Lab scripts, thin orchestration, all of it reusing harness, none of it
               bringing its own machine.
  ci/          gate.py + gate.yaml: three criteria rows, a red light exits non-zero.
```

*Figure B-1 The repo directory map. The eval machine lives in `harness/`; world knowledge lives only in `world/` and `synth/`, and those two are exactly what a migration rewrites.*

Pure stdlib throughout (about 3,100 lines of Python), no file over 200 lines, no framework. The machine is small enough to read in an afternoon. That is deliberate; it is itself the course.

## 2. The module-by-module migration guide (paying off Chapter 7's migration box)

The six components contain no Shore & Summit knowledge. Move them in dependency order.

| Component | Depends on | Migration action |
|---|---|---|
| trace | nothing | Move as is. Your agent only has to write JSONL to the contract schema; you need not change the agent's code, write a log adapter |
| assertions | trace + your world | Move the framework, rewrite the assertion bodies: replace `refund_not_executed` with your own "irreversible action not executed" |
| stats | nothing | Move as is, not one line changes |
| judge | llm | Swap the prompt for your attributes; keep `align()` and the alignment report format untouched |
| report | stats | Move as is; adjust the column names to your sev tiers |
| runner | all of the above + world | Move the skeleton, swap two points: `world.reset/apply_setup` (your sandbox) and case loading |
| **Only two things get rewritten**: `world/` (your sandbox: for a coding agent a throwaway git repository, where reset = check out again; for a research agent a frozen corpus snapshot) and `synth/` (your counterparty personas) | | |

*Table B-1 Migration order and actions for the six harness components. The fewer the dependencies, the earlier it moves; `trace` and `stats` move with zero changes.*

## 3. The build-it-yourself ↔ commercial platform isomorphism table (paying off Chapter 7's sidebar)

Eval platforms such as Braintrust, Arize, and LangSmith map one to one onto this book's harness concepts. Build first, buy later, and neither the data nor the method goes to waste.

| This book | Platform term | Watch out for when migrating |
|---|---|---|
| case set (cases/) | dataset | A case's `setup` (the world's prior state) is a first-class concept that platform datasets commonly lack; it usually has to be stuffed into metadata |
| assertions + judge | scorer / evaluator | The tiering discipline (a sev-1 is never released by a judge alone) is your process; the platform will not enforce it for you |
| one eval run with intervals | experiment / run | Platforms default to a single pass; `--repeat` and intervals are a habit you have to insist on carrying over |
| trace (JSONL) | trace / span tree | See the OTel mapping in the next section, essentially lossless |
| verdict record (`judged_by` visible) | annotation / feedback | The `judged_by` ladder and `first_bad_step` usually need custom fields |

*Table B-2 The build-it-yourself ↔ commercial platform isomorphism table. Concepts correspond one to one; the third column reminds you that disciplines and first-class concepts (such as `setup`) do not migrate on their own.*

## 4. Trace schema ↔ OTel GenAI semantic conventions

Field names follow the interface contract; when exporting to any OTel-compatible backend, use the table below.

| Contract field | OTel GenAI counterpart |
|---|---|
| `trace_id` | trace id |
| the whole trajectory | root span (`gen_ai.operation.name: invoke_agent`) |
| `steps[].type: model` | `chat` span; `tokens_in/out` → `gen_ai.usage.input_tokens / output_tokens` |
| `steps[].type: tool_call/tool_result` | `execute_tool` span (`gen_ai.tool.name` = the tool name) |
| `steps[].type: subagent` (nested trace) | a nested `invoke_agent` sub-span tree |
| `steps[].type: inbound` | no standard counterpart, a custom event; suggested attribute `inbound.source` (this is the one first-class concept this book adds beyond the standard convention: external content ingestion must be visible in the trace) |
| `usage.cost_usd` | no standard field, a custom attribute (remember the "illustrative / actual" annotation) |
| `case_id`, `plan`, `memory_write` | custom attributes |

*Table B-3 Trace schema ↔ OTel GenAI semantic conventions mapping. `inbound` and `cost_usd` have no standard counterpart and go out as custom attributes.*

The value of this mapping table is **no lock-in**. Chapter 7 promised "build first, and buying later is not locked out"; this is how the promise is kept.
