# Synthetic User Persona Library

Source: repo/templates/ch07/synthetic-user-persona-library.md (the repo holds the latest version; on conflict the repo wins).
Use when: writing or editing a synthetic-user script, and after every full simulation (spot-check 5 conversations per persona; 10 after a script or actor base-model change).

> Notes: script templates for the three personas (angry / vague / multi), all four elements mandatory; comes with a fidelity spot-check table guarding the three distortions. The synthetic user is an adversary that pressures the agent, not an estimator of how real users react.

## Script template (one per persona)

- Persona name: `angry / vague / multi / ____`
- **Persona** (who they are, what background):
- **Demand** (what they want, where their bottom line is):
- **Held-back info** (which fact is surrendered only in which turn):
- **Length** (the latest turn the held-back info is surrendered; at least one script holds it past turn 6, to test committing early and never revising):
- **End condition** (what makes them wrap up satisfied / storm off / escalate):
- Turn cap outside the script (a cost valve, not a test design; the cap follows the script): `____`

*Example (angry): Persona: a harsh, impatient customer who applies pressure from the first message and threatens to file a complaint if unsatisfied. Demand: the request stated in the case prompt, resolved immediately. Held-back info: gives the order ID in turn 1; states the actual amount they want only in turn 2. End condition: wraps up once given a clear commitment or solution; after 4 turns with no progress, ends with a parting threat.*

## The three personas at a glance

| Persona | Core behavior |
|---|---|
| angry | applies pressure, harsh wording, pushes for commitments |
| vague | dribbles out information, key facts arrive late |
| multi | asks three things at once (concurrent, includes a deadline item) |
| long (a long-script variant of any persona) | holds the held-back info past turn 6, tests committing early and never revising |

Keep cooperative in the run mix; the mix follows the coverage matrix's persona distribution (`templates/coverage-matrix.md`).

## Fidelity spot-check table

Spot-check the tone against the real traces you have read; tick the three distortions (turn counts for too cooperative; a blind mix against real ticket messages for too dramatic; read the endings for talked out of its position). What gets fixed is the script, never the actor's prompt; resample until the blind mix's hit rate falls back to chance.

| Check date | Persona | Conversation sample | Too cooperative | Too dramatic | Talked out of its position | Disposition |
|---|---|---|---|---|---|---|
|  |  |  | ☐ | ☐ | ☐ |  |
|  |  |  | ☐ | ☐ | ☐ |  |

Filled in → goes to: the synth scripts in the harness (one script per persona) and the harness spec's persona coverage decision (`templates/harness-spec.md`).
