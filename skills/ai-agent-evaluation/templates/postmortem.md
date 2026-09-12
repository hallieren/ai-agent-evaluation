# Agent Incident Postmortem

Source: repo/templates/ch16/incident-postmortem-template.md (the repo holds the latest version; on conflict the repo wins).
Use when: an incident or a stopped attempt needs a postmortem with the trace as the chain of evidence.

> Note: a postmortem with the trace as evidence. No trace and only recollection? Your first action item generates itself, get the system producing traces that can be reviewed. An attempt is not the same as nothing happened, only one layer of the depth still working is itself an incident.

- Incident / attempt: ________  Date: ____  Chair: ____  Owners present: ____

## The five columns

### 1. Timeline (rebuilt from the trace, with step numbers)

| Step | Type (model / tool_call / inbound ...) | What happened |
|---|---|---|
| *e.g. 2* | *inbound* | *a forged customer email claiming to be the order holder enters the context* |
|  |  |  |

### 2. `first_bad_step`

- Step ____: ________ (the first step that went wrong, not the last step that got stopped or the worst output)

### 3. Diff list

- Sandbox / world before-after changes: ____ (empty = an attempt; mark each one "declared in advance" or "a discovery")

### 4. How the defenses performed (layered interception)

| Defense layer | Intercepted? (stopped / zero interceptions / never triggered) | Evidence step |
|---|---|---|
| Input filter |  |  |
| Action boundary |  |  |
| Permission matrix |  |  |
| Human confirmation |  |  |

Question for the room: which defense layer should have caught this and did not. People are not a defense layer.

### 5. Action items (each in three parts: action → the equipment it points at → owner)

Self-check: every item should point at some piece of equipment (a template or a config in this skill); if it points at nothing, it is either a genuinely new wall (rare) or a variant of "be more careful next time", so delete it and rewrite.

| Action item | Equipment it points at (template / config name) | Owner | Deadline |
|---|---|---|---|
| *e.g. add variants of this phrasing to `cases/attacks`* | *templates/redline-set.md* |  |  |
|  |  |  |  |
|  |  |  |  |

## Closing checks

- [ ] The incident went into the failure mode atlas (a new row or an addition to one)
- [ ] The postmortem produced a case and it went into the eval set (a postmortem that produced no case is the same as no postmortem)

Filled in → goes to: templates/failure-mode-atlas.md (the new row), the eval set (the case), and the audit record where governance requires one.
