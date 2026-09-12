# Tool-Call Eval Checklist

Source: repo/templates/ch08/tool-call-eval-checklist.md (the repo holds the latest version; on conflict the repo wins).
Use when: reviewing the eval configuration for any tool-using agent, before a write tool is unlocked.

> Notes: walk your tool-call eval configuration through the five dimensions. You will find nearly every cell says "deterministic check." Tool calls have structured arguments; the judge does not get a turn.

| Dimension | Question | Recommended verdict method | Covered? (case / assertion name) |
|---|---|---|---|
| Selection | Was the right tool called? And no tool that shouldn't be? (a fuzzy search with an order ID in hand?) | deterministic check (trace scan against the expected tool set in `expect`) |  |
| Arguments | Are the arguments right? In bounds? (amount, order ID, recipient) | deterministic check (`amount_within_limit` etc., read from `tool_call` args, never from the reply) |  |
| Ordering | Are the dependencies in order? (read before write; verify identity before sending out; state check before any write retry) | deterministic check (step-sequence scan) |  |
| Error recovery | After a tool error: retry within budget, reroute, escalate, or double down on the error? (`tool_result` error + reply reports success = red line) | deterministic check + seeded-error probe (error script on the stubs) |  |
| Hallucinated tools | Called a tool that doesn't exist / fabricated a tool result? | deterministic check (every `tool_call` name against the registry) |  |

## Self-check

- [ ] At least one case per dimension, all five dimensions
- [ ] At least one seeded-error probe (mistake planted in setup; tests the defenses, not the capability, e.g. "this order is already refunded"), run in both stub configurations
- [ ] Escalation tested on both sides: cases where escalating is right, and just as many where it is wrong
- [ ] Every sev-1 red-line case has a deterministic sentry in `expect.assertions`; a judge alone does not count

Filled in → goes to: the coverage matrix's tool-call rows (`templates/coverage-matrix.md`) and each case's `expect` block.
