# Multi-Agent Attribution Decision Tree (Chapter 11)

> Note: the fixed attribution order for system-level failures. There are always three suspects: the main agent, the subagent, and **the handoff itself**. The default "everyone debugs their own module" is exactly what systematically misses the third.

## The decision tree

1. **Outer `first_bad_step`**: locate the first bad step in the outer trace.
2. **Boundary check**: does it land on a `subagent` step?
   - No → **Exit A: main agent**.
   - Yes → 3.
3. **Drill down**: open the nested trace; given the task description it received, did the subagent err?
   - Yes → **Exit B: subagent**.
   - Nested trace clean → **check the two ends** (the spawn task description, and how the returned result was used) → **Exit C: handoff** (as in the Swiftlink case: first bad step in the spawn step's task description, both single agents individually clean).
   - The subagent spawned a grandchild agent → **recurse** down the nesting chain; record the conclusion as a "drill-down path" (which layer, which step), not a single step number; add a "maximum nesting depth" column to the report.

## Parallel-spawn check card (event ordering)

When the main agent spawns several subagents at once, the before/after diff cannot see the interleaving; add an event-ordering check:

- [ ] Same object (order / ticket / memory entry), two initiators, written one after the other? → flag a race
- [ ] Race failures are probabilistic: absent in one run ≠ absent, reproduce with `--repeat` (ch6 discipline)

## The three exits

| Exit | Which eval set it enters | What to fix |
|---|---|---|
| A main agent | the main agent's single-agent eval set | prompt / tool descriptions |
| B subagent | that subagent's single-agent eval set | the subagent's prompt / its tools |
| C handoff | a system-level end-to-end case | the contract (required fields / return fields / confidence labels) or the architecture |

## Attribution conclusion (one per system-level failure)

- trace_id: `________`  outer first_bad_step: `________`
- Conclusion: ☐ main ☐ sub ☐ handoff (combinations allowed)  Evidence steps: `________`
- Which eval set it enters: `________`  What to fix (prompt / contract / architecture): `________`
- Independence red line: a reviewer-type subagent whose nested trace holds zero self-initiated tool calls is itself in violation (the wrong-plan collusion case).
