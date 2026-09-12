# ai-agent-evaluation (Skill)

A Claude Code Skill that distills the book *AI Agent Evaluation* into an evaluator's operating procedures: decision ladders, output contracts, a review grammar, 40 fill-in templates, and four stdlib Python scripts. The book stays the source of truth; where the two disagree, the book wins.

## What it does

When a task involves evaluating an AI agent or LLM system (can we ship, what counts as good, error analysis, eval sets, LLM judges, pass rates and version comparisons, sandboxes, tool calls, planners, memory, subagents, prompt injection, launches, release gates, improvement loops, postmortems), the agent loads `SKILL.md`, routes to one reference file, applies the invariants and decision procedures, and produces artifacts in the book's shapes (the report line with intervals clustered by case, the case schema, the spec, the gate table, the failure mode atlas). Asked to review an eval report, plan, judge, or gate, it answers with tagged one-line findings and a fixed closing line.

## Layout

```
SKILL.md        router, invariants, decision procedures, output contracts, review mode, self-deception table
references/     one file per situation (defining good, reading traces, eval sets, judging, numbers, harness,
                tool calls, plans and cost, memory, multi-agent, adversarial, going live, gates, improving,
                sustaining, failure taxonomy, high stakes, glossary)
templates/      40 fill-in artifacts, domain-neutral, each pointing at its source under repo/templates/
scripts/        evalstats.py, judge_align.py, coverage.py, snapshot_diff.py (Python >= 3.10, no dependencies)
evals/          test prompts and trigger queries used to check the skill
```

## Install

Install it as a Claude Code plugin (the repository is its own single-plugin marketplace):

```
/plugin marketplace add hallieren/ai-agent-evaluation
/plugin install ai-agent-evaluation@ai-agent-evaluation
```

Or symlink the folder directly (Claude Code reads skills from `~/.claude/skills/` personal or `.claude/skills/` project):

```bash
ln -s "$(pwd)/skills/ai-agent-evaluation" ~/.claude/skills/ai-agent-evaluation
```

Then ask anything eval-shaped ("can we ship this agent", "review this eval report", "how many cases do we need") and the skill triggers on its own. Scripts run from the skill folder:

```bash
python scripts/evalstats.py --selftest
python scripts/evalstats.py report verdicts.jsonl
```

## Testing

Across four scenarios (ship review, eval-from-zero, judge trust, CI gating), the with-skill runs passed nearly every graded assertion where a no-skill baseline passed far fewer. The task prompts with their assertions, and the should-trigger / should-not-trigger checks, are in [evals/](evals/).

## Source

Book: `docs/chapters/`, `docs/appendices/` in this repository. Templates: `repo/templates/chNN/`. Prose CC BY-NC-SA 4.0, code MIT (see the repository `LICENSE.md`).
