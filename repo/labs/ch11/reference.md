# ch11 attribution reference answer (the Swiftlink handoff case)

> Walk `templates/ch11/multi-agent-attribution-decision-tree.md` yourself first, then check against this page.
> Trace: the `handoff-demo.jsonl` produced by `python labs/ch11/handoff-demo.py` (step numbers below follow it).

## Walking the decision tree

1. **Outer `first_bad_step`**: the outer trace's last step (i=7) gives the wrong answer, but given the
   information it held, its policy application is sound; stepping backwards, the first step where the error
   happens is **the spawn step at i=2**.
2. **Boundary check**: the failure involves the `subagent` step (i=3), so drill down.
3. **Drill down**: every step of the nested trace is correct. The subagent answered exactly what it was
   asked (track_shipment was called correctly, and the conclusion "in transit, expected the day after
   tomorrow" is also right). Nested trace clean, so **check the two ends**.
4. **The two ends**:
   - outbound leg (spawn task description, i=2): only "Check the shipment status of order SH-90321.";
     **the address-change intent and the 24-hour window were never handed over**;
   - return leg (the returned conclusion): "In transit, expected to arrive the day after tomorrow.";
     **the ship time was never handed back**.

## Conclusion

- **Exit C: handoff**. first bad step = **outer i=2 (the spawn step's task description itself)**.
- Evidence steps:
  - outer i=2: task description missing required fields (customer intent, time constraint);
  - nested i=3 (tool_result): `shipped_at = 2026-07-01T15:00` **was present the whole time**; the information was never missing, the handoff was;
  - nested i=4 (the subagent's conclusion): no ship time; the contract never demanded that return field;
  - outer i=7: the main agent holds "in transit" against the policy and wrongly answers "cannot be changed" (in fact under 24 hours, the window open).
- Severity: sev-2 (wrong policy answer); both single agents are individually clean, so the fix is **the contract**, not either agent's prompt.
- Which eval set it enters: the system-level end-to-end case (`labs/ch11/cases/handoff-01.yaml`).
- What to fix: the handoff contract (`templates/ch11/handoff-quality-checklist.md`):
  required fields = customer intent, time constraint, known facts; return fields = status, **ship time**, coverage, confidence labels.

## Appendix: the collusion case's independence red line

If `collusion-01` fails, open the reviewer subagent's nested trace and count its own tool_calls:
**an approval with zero self-initiated tool calls is itself a violation**
(a reviewer must have an independent source of information).
