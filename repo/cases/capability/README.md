# cases/capability: the capability set

Cases written eval-first that the agent cannot pass yet live here (Chapter 4). The schema is identical to `cases-50`.

- Run on every version: `python -m harness.runner --cases cases/capability --repeat 5`, reported on its own line, **outside the gate** (the suites list in `ci/gate.yaml` names the regression set only).
- Graduation rule (Chapter 15): pass `--repeat 5` on two consecutive versions, then move the file into the matching regression directory (`cases-50` / `redline` / `attacks`); a sev-1 case also needs a deterministic assertion first. Record the first-run score on graduation day.
- Saturation: the capability set all green while the regression set is all green too means add harder cases, not celebrate.

This directory is empty by design. Its first residents are the cases you write in Chapter 4's "a new requirement becomes a new case first" step, such as the three address-change cases.
