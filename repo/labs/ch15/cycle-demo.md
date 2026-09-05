# ch15 One improvement cycle end to end (worked example: fuzzy search instead of exact lookup)

> Canonical, from the Bible's section 4: the customer already gave the order ID, and Mini still fuzzy-searches by
> name with `search_orders`, occasionally turning up a same-name customer's order. The offline set has no such mode
> (it only tests "can it find it", never "it was handed to you, do you use it").
> The reference answer for locating the bottleneck = the tool-description boundary (`get_order` vs `search_orders`),
> **not the prompt**.

## Step 1 Circle the pool and cluster

```
python labs/ch15/cluster.py          # by default circles the production output under labs/ch13/out/
```

A pile forms for "fuzzy search by name even with the order ID given", and the 10 harvested in Chapter 13 are in it too. Stratified sampling, then read and code every trace by hand.

## Step 2 Extend the atlas (six-column row structure)

| Name | Definition and criterion | Representative trace | Count | sev distribution | Suspected component |
|---|---|---|---|---|---|
| fuzzy search by name even with the order ID given | the prompt carries an `SH-` order ID, yet the trace calls `search_orders`; occasionally turns up a same-name customer's order | (the IDs in your pool) | (count them) | mostly sev-3, rising to sev-1 when it pulls someone else's order | tool description? prompt? |

## Step 3 Locate the bottleneck: write both candidates as falsifiable hypotheses

- H1 (prompt): the system prompt does not require "with an order ID present, exact lookup is mandatory".
- H2 (tool description): the **boundary** between `get_order` ("Look up an order by exact order ID") and
  `search_orders` ("Fuzzy-search orders by customer name or item name") never says when the latter should not be used.

Rejection rule (in writing before the run): rerun paired after the fix, and if the interval on the target mode's count
does not drop, that hypothesis is rejected, move to the next.
Pick the smaller blast radius first: **the tool description** (a tier-1 change; the prompt is the behavior surface, tier 2).

## Step 4 Fix on target: change only the tool description, not one word of the prompt

The two descriptions in `mini/tools.py` (the "edit the tool description" lever of the seven):

```
get_order:      "Look up an order by exact order ID (mandatory when the customer has given an SH- order ID)"
search_orders:  "Fuzzy-search orders by customer name or item name (use only when there is no order ID)"
```

## Step 5 Verify: paired, 5 passes, with intervals

```
python -m harness.runner --cases cases/cases-50 --repeat 5 --flags write_tools   # once before the fix, once after
python labs/ch15/cluster.py                                                      # look at the target mode's count
```

Look at the target mode's count (the intervals have to separate, ch6 discipline); then run the full regression and check
the sev tiers did not get worse.
Target mode didn't drop? Switch to H1 and redo steps 4 and 5. **A normal step in the cycle, not a setback.**

## Step 6 The finish

Use Chapter 6's report format to produce the full eval report (sev tiers, intervals, and cost accounting all present),
and put it on the desk side by side with that Pocket Eval decision sheet from Chapter 1.
