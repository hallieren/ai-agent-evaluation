# Mini + harness: companion repo of *AI Agent Evaluation*

Shore & Summit is a synthetic teaching world assembled from common enterprise scenarios; it does not correspond to any real company, and every character in this book is fictional.

> This directory holds the companion code for *AI Agent Evaluation*. For the book-level guide, the chapter overview, and the three reading tracks, see the [book-level README](../README.md).

## Configuration (vendor-neutral)

The model is configured via environment variables; any OpenAI-compatible endpoint works:

```bash
export MODEL_BASE_URL=https://api.example.com/v1   # your provider's endpoint
export MODEL_NAME=<model name>
export MODEL_API_KEY=<api key>
```

No third-party dependencies to install (Python ≥ 3.10, pure stdlib).

## One-minute smoke test

```bash
cd repo
python world/world.py                 # sandbox resettability self-check
python -m harness.runner --cases cases/seed-20        # Chapter 1: Lv.0, full run
python viewer/trace_viewer.py traces/examples/t-0007.jsonl   # Chapter 2: read a trace
```

## Layout (§7 of the Lab interface contract, internal design doc)

```
mini/        the agent itself: loop, flags, tool registry; llm.py is the only file in the repo that touches a model API
world/       the Shore & Summit sandbox: seeded SQLite order DB, outbox stub, reset
harness/     runner, trace, assertions, judge, stats, report (+ differ, caseyaml)
cases/       seed-20, cases-50, redline, attacks
traces/      pregen-60.jsonl, examples/
synth/       the three synthetic-user personas: angry, vague, multi
viewer/      trace viewer (terminal)
templates/   chNN/: each chapter's Your Loot templates (Appendix A compiles them)
labs/        chNN/: step scripts for each chapter's Lab
ci/          gate script and config (ch14)
```

Lab ordering discipline: **write the eval first, then flip the flag**. Each chapter's entry point is `labs/chNN/README.md`.

Offline mode: with `MODEL_FAKE=1`, `mini/llm.py` takes replies from a scripted queue, for tests and teaching-trace generation,
not as an evaluation method (an eval must measure the real model).
