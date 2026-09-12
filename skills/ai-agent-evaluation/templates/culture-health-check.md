# Eval Culture Health Check

Source: repo/templates/ch16/eval-culture-health-check.md (the repo holds the latest version; on conflict the repo wins).
Use when: checking whether the three habits are alive by going through records, not by asking how it feels.

> Note: a list of questions organized by the three habits. Every one has to be answerable by **going through the records**, not by "I think so"; anything whose record location you cannot name counts as a no.

## Habit one: read traces every week

- [ ] Over the last four weeks, is there a trace-reading record for every week? (Go through: the meeting records; two consecutive weeks of zero output = the meeting is already dead)
- [ ] Does the rotation cover everyone, PMs and new hires included? (Go through: the rotation table)
- [ ] In the last month, has anyone read a path problem out of a `pass` trace? (Go through: the meeting output)
- [ ] Does the batch read hold randomly drawn traces, or only what the signals circled? (Go through: the sampling script or the meeting records)

## Habit two: every incident enters the eval set

- [ ] Is there a postmortem record for the most recent incident or attempt? (Go through: the filed postmortem, templates/postmortem.md)
- [ ] Did the case the postmortem produced enter the eval set? (Go through: the cases commit history; a postmortem that produced no case is the same as no postmortem)
- [ ] Do the action items all point at specific equipment, with an owner and a deadline? (Go through: column 5 of the postmortem)

## Habit three: every new feature has a case before it has code

- [ ] For the last three feature reviews, did the cases exist at review time? (Go through: review records vs. case commit times)
- [ ] Is there an instance of a feature being held out of review for "no case"? (Go through: the review records)

## Infrastructure liveness (assets in use, not merely present)

- [ ] Number of people who added a case to the eval set in the last month: ____ (Go through: the commit history; ≤ 1 person = a danger sign; fewer than half the team = a few people's overtime)
- [ ] Of those, how many are not engineers: ____ (zero = the product–model interface is not connected)
- [ ] When was the gate's most recent interception? (Go through: the ci/gate interception records; never intercepting = the gate is a formality, or nobody is committing)
- [ ] Do the people named on the RACI table know it themselves? (Ask them, then go through their most recent related records)
- [ ] Ask a random colleague which case corresponds to the most recent incident (no case ID = infrastructure, not culture)

## Conclusion

- Danger signs counted: ____  The first one to fix: ____  Owner: ____

Filled in → goes to: the team's quarterly record and the first action item's owner; repeat the check each quarter.
