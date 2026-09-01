# Handoff Quality Checklist (Chapter 11)

> Note: one per main agent ↔ subagent interface. The contract makes the handoff checkable: a spawn missing required fields, or a return missing confidence labels, is caught by deterministic checks, and never needs a judge.

- Subagent: `________` (e.g. the Swiftlink logistics subagent)

## 1. Required fields (at spawn)

- [ ] Task goal (including the **intent**, not just the action; "check the shipment status" ≠ "the customer wants an address change")
- [ ] Constraints and time windows (e.g. the 24-hour post-shipment intercept window)
- [ ] Known facts (what the main agent has already looked up, so the subagent does not re-query it)
- This contract's field list:

## 2. Return fields

- [ ] Conclusion
- [ ] Evidence (which tool call supports it)
- [ ] Coverage (what was checked, what was not; "not found" ≠ "does not exist")
- This contract's field list:

## 3. Confidence labels

- [ ] Every conclusion labeled `verified / inferred / unknown` (is "expected the day after tomorrow" the system's own words, or the subagent's estimate?)

## Two hard checks

- [ ] **Independence check** (reviewer-type subagents): does its input come 100% from the party under review? Does its nested trace contain tool calls of its own? An approval with zero self-initiated tool calls is itself a violation.
- [ ] **Duplicated-work check**: are known facts handed over with the task? What did the subagent re-query that the main agent had already looked up?

## ch12 addition

- [ ] Does the handed-over context carry unquarantined external content (an `inbound` source)?
