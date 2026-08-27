# Tool-Call Eval Checklist (Chapter 8)

> Notes: walk your tool-call eval configuration through the five dimensions. You will find nearly every cell says "deterministic check" — tool calls have structured arguments; the judge does not get a turn.

| Dimension | Question | Recommended verdict method | Covered? (case / assertion name) |
|---|---|---|---|
| Selection | Was the right tool called? And no tool that shouldn't be? (fuzzy `search_orders` with an order ID in hand?) | deterministic check (trace scan) |  |
| Arguments | Are the arguments right? In bounds? (amount, order ID, recipient) | deterministic check (`amount_within_limit` etc.) |  |
| Ordering | Are the dependencies in order? (read before write; verify identity before sending out) | deterministic check (step-sequence scan) |  |
| Error recovery | After a tool error: retry, reroute, or double down on the error? | deterministic check + seeded-error probe |  |
| Hallucinated tools | Called a tool that doesn't exist / fabricated a tool result? | deterministic check (against the registry) |  |

## Self-check

- [ ] At least one case per dimension, all five dimensions
- [ ] At least one seeded-error probe (mistake planted in setup; tests the defenses, not the capability, e.g. "this order is already refunded")
