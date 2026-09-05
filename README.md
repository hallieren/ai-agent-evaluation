# AI Agent Evaluation

[![smoke](https://github.com/hallieren/ai-agent-evaluation/actions/workflows/smoke.yml/badge.svg)](https://github.com/hallieren/ai-agent-evaluation/actions/workflows/smoke.yml)

> Score the endpoint, attribute the path, account for the side effects. Eval before you build. Written for engineers pushing agents toward production, the ones asked "can we ship?" with no evidence in hand. Sixteen chapters, one wall and one template each; the companion repo runs with zero dependencies (pure stdlib, Python ≥ 3.10).

*Shore & Summit is a synthetic teaching world assembled from common enterprise scenarios; it does not correspond to any real company, and every character in this book is fictional.*

The book is released chapter by chapter. All 16 chapters are live, and the appendices land one at a time, roughly weekly, each as it clears our own practice pass. Each released chapter is paired with an applied essay on the author's Substack: [hallieren.substack.com](https://hallieren.substack.com). Unreleased items below are marked 🚧 coming.

## How to read

```bash
uvx --from mkdocs-material mkdocs serve   # local site at http://127.0.0.1:8000
```

Or read the hosted site at <https://hallieren.github.io/ai-agent-evaluation/>, or the links below directly (GitHub renders them). The reading guide and the three reading paths are in [docs/index.md](docs/index.md); companion code is in [repo/](repo/README.md).

## Chapters

| # | Chapter | Templates | Lab |
|---|---|---|---|
| **Part I · Quick Wins** | | | |
| 1 | [The Two-Hour Pocket Eval](docs/chapters/ch01-pocket-eval.md) | [Templates](docs/appendices/ch01-templates.md) | [Lab](docs/labs/ch01.md) |
| 2 ★ | [Endpoints, Paths, and Cost](docs/chapters/ch02-defining-good.md) | [Templates](docs/appendices/ch02-templates.md) | [Lab](docs/labs/ch02.md) |
| **Part II · From Reading Traces to Trustworthy Numbers** | | | |
| 3 ★ | [Error Analysis](docs/chapters/ch03-error-analysis.md) | [Templates](docs/appendices/ch03-templates.md) | [Lab](docs/labs/ch03.md) |
| 4 | [Building Eval Sets](docs/chapters/ch04-eval-sets.md) | [Templates](docs/appendices/ch04-templates.md) | [Lab](docs/labs/ch04.md) |
| 5 ★ | [The Judgment Ladder](docs/chapters/ch05-judgment-ladder.md) | [Templates](docs/appendices/ch05-templates.md) | [Lab](docs/labs/ch05.md) |
| 6 | [Variance and Significance](docs/chapters/ch06-variance.md) | [Templates](docs/appendices/ch06-templates.md) | [Lab](docs/labs/ch06.md) |
| 7 | [Harness and Sandbox](docs/chapters/ch07-harness.md) | [Templates](docs/appendices/ch07-templates.md) | [Lab](docs/labs/ch07.md) |
| **Part III · Agent-Specific Battlegrounds** | | | |
| 8 ★ | [Dangerous Tools](docs/chapters/ch08-dangerous-tools.md) | [Templates](docs/appendices/ch08-templates.md) | [Lab](docs/labs/ch08.md) |
| 9 | [Planning and Cost](docs/chapters/ch09-planning-and-cost.md) | [Templates](docs/appendices/ch09-templates.md) | [Lab](docs/labs/ch09.md) |
| 10 | [Memory](docs/chapters/ch10-memory.md) | [Templates](docs/appendices/ch10-templates.md) | [Lab](docs/labs/ch10.md) |
| 11 ★ | [Subagents](docs/chapters/ch11-multi-agent.md) | [Templates](docs/appendices/ch11-templates.md) | [Lab](docs/labs/ch11.md) |
| 12 ★ | [Attacks](docs/chapters/ch12-adversarial.md) | [Templates](docs/appendices/ch12-templates.md) | [Lab](docs/labs/ch12.md) |
| **Part IV · Shipping and Sustaining** | | | |
| 13 ★ | [Online Eval](docs/chapters/ch13-online-eval.md) | [Templates](docs/appendices/ch13-templates.md) | [Lab](docs/labs/ch13.md) |
| 14 | [Regression and Gates](docs/chapters/ch14-release-engineering.md) | [Templates](docs/appendices/ch14-templates.md) | [Lab](docs/labs/ch14.md) |
| 15 | [The Improvement Loop](docs/chapters/ch15-improvement-loop.md) | [Templates](docs/appendices/ch15-templates.md) | [Lab](docs/labs/ch15.md) |
| 16 | [Eval Culture](docs/chapters/ch16-eval-culture.md) | [Templates](docs/appendices/ch16-templates.md) | [Lab](docs/labs/ch16.md) |

★ = heavyweight chapter.

**Appendices** (🚧 coming): A Template Pack · B Repo Map & Migration · C High-Stakes Domains · D Failure-Mode Taxonomy · E Glossary

Prose CC BY-NC-SA 4.0 · code MIT ([LICENSE.md](LICENSE.md)) · [Contributing](CONTRIBUTING.md)
