# Agent Red Team Protocol

Source: repo/templates/ch12/agent-red-team-protocol.md (the repo holds the latest version; on conflict the repo wins).
Use when: setting up or running a red-team round; before every version and every capability unlock.

> Note: security is not a one-off penetration test before launch, it is a standing process. Three things written down: who plays the attacker, how often a round runs, where findings go. Write the threat model (who attacks, after what) before filling this in.

## 1. Who plays the attacker

- [ ] Rotation (turns inside the team, everyone has had a go): roster `________`
- [ ] Adversarial persona (a synthetic user with an attacker script): `________`
- [ ] Outsider (a fresh pair of eyes that does not share the system's assumptions): `________`

## 2. How often a round runs

- [ ] At least one round per version
- [ ] One round **without fail** every time a new capability is unlocked (a new tool, a new external entry point); when the capability changes, the attack surface changes

## 3. Where findings go (never into a drawer)

- [ ] New or amended rows in the failure mode atlas (the six-column structure, templates/failure-mode-atlas.md)
- [ ] Red-line cases banked into `cases/attacks`, rerun every version from then on; red-team output is a permanent increment to the eval set, not a report
- [ ] Variants produced by automated red teaming enter and leave the library by three rules
    - Only a variant that produces a new result enters; one that stops at the same layer as its parent is dropped; every entry carries its parent's id
    - Entering the library means regression, rerun every version, never into a drawer
    - A **variant** stopped by the same layer for several consecutive versions, never supplying new information, is down-sampled to a sampled subset; retirement is down-sampling, not deletion, and **the parent is never retired**
- [ ] Anything that breached every layer → the Shutdown Red-Line Checklist (the security branch of the stop rule)

## Attack surface × carrier coverage matrix (an empty cell = a corner you have not tested)

| Attack surface \ carrier | Web (fetch_url) | Email (inbound body) | Ticket (customer fields) |
|---|---|---|---|
| Injection | *e.g. forged policy page* | *e.g. forged customer email* |  |
| Tool misuse |  |  |  |
| Privilege escalation |  | *e.g. forged customer email* |  |
| Data exfiltration |  |  |  |
| Autonomy boundary |  |  |  |

Outbound channel inventory (the data exfiltration row also splits by **exit**): `send_email` body / report citations / ticket notes / confirmation replies; every output channel you open, the red-line scan follows.

## This round's record

- Date: `____`  Trigger (version / unlock): `____`  Attacker: `____`
- Layered interception table filled in? ☐ (each attack labeled with the layer it finally stopped at: input filter / action boundary / permission matrix / human confirmation / breach)
- Reporting basis: tallies carry an interval (`--repeat` ≥ 5)? ☐ A single-run number is not a conclusion; breaches are counted on their own line and never averaged in
- Same case landing on different layers across runs (flip)? ☐ list them: `____`
- Do interceptions crowd almost entirely into the last layer? Yes → the depth is fake; open an action item: `____`

Filled in → goes to: the red-team report (layered interception table), `cases/attacks`, the failure mode atlas, and the shutdown checklist for any breach.
