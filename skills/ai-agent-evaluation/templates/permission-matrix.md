# Action Permission Matrix

Source: repo/templates/ch08/action-permission-matrix.md (the repo holds the latest version; on conflict the repo wins).
Use when: before unlocking any write tool, and whenever a tool's conditions, guards, or rollback answers change.

> Notes: build rows on tool × condition (not one row per tool name), check one of the three columns, fill in the guard, answer both questions. **Once filled in, this merges into the spec and is part of the spec from then on** (`templates/spec.md`); before unlocking any write tool, change this first.

## Permission matrix

At least three rows per write tool (the conditions for autonomous, needs confirmation, forbidden). `escalate` is always autonomous. Needs-confirmation is scarce: if a trial run drops half the actions there, the matrix is badly designed; write finer conditions for what can be autonomous.

| Tool | Condition | Autonomous | Needs confirmation | Forbidden | Guard (assertion / diff / gate; test its miss rate and its false-stop rate once each) |
|---|---|---|---|---|---|
| *e.g. refund* | *amount ≤ <limit> and order not refunded* | *✅* |  |  | *`amount_within_limit`, diff; refund ledger checked before executing* |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

Review rule: a row without a guard is a wish, not a permission; add a precondition or an assertion, or demote the whole row to needs-confirmation.

## The two confirmation-and-rollback questions (answer per write tool)

| Tool | Who confirms? (no answer = no unlock) | How does it roll back? (nominally undoable ≠ actually recoverable) |
|---|---|---|
| *e.g. send_email* | *<role>* | *a sent email cannot be recalled → intercept up front* |
|  |  |  |
|  |  |  |

## Differ semantics

Every sandbox before/after change is either declared as expected, or it is a finding.

Filled in → goes to: the spec's action boundary section (`templates/spec.md`), and each red-line case's `expect.assertions` (the guard column).
