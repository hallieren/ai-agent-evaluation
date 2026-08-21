# AI Agent Evaluation

[![smoke](https://github.com/hallieren/ai-agent-evaluation/actions/workflows/smoke.yml/badge.svg)](https://github.com/hallieren/ai-agent-evaluation/actions/workflows/smoke.yml)

> Score the endpoint, attribute the path, account for the side effects. Eval before you build. Written for engineers pushing agents toward production, the ones asked "can we ship?" with no evidence in hand. Sixteen chapters, one wall and one template each; the companion repo runs with zero dependencies (pure stdlib, Python ≥ 3.10).

*Shore & Summit is a synthetic teaching world assembled from common enterprise scenarios; it does not correspond to any real company, and every character in this book is fictional.*

The book is released chapter by chapter. Chapters 1 through 3 are live, and the remaining chapters and appendices land one at a time, roughly weekly, each as it clears our own practice pass. Unreleased chapters below are marked 🚧 coming.

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
| 5 ★ | The Judgment Ladder | 🚧 coming | |
| 6 | Variance and Significance | 🚧 coming | |
| 7 | Harness and Sandbox | 🚧 coming | |
| **Part III · Agent-Specific Battlegrounds** | | | |
| 8 ★ | Dangerous Tools | 🚧 coming | |
| 9 | Planning and Cost | 🚧 coming | |
| 10 | Memory | 🚧 coming | |
| 11 ★ | Subagents | 🚧 coming | |
| 12 ★ | Attacks | 🚧 coming | |
| **Part IV · Shipping and Sustaining** | | | |
| 13 ★ | Online Eval | 🚧 coming | |
| 14 | Regression and Gates | 🚧 coming | |
| 15 | The Improvement Loop | 🚧 coming | |
| 16 | Eval Culture | 🚧 coming | |

★ = heavyweight chapter.

**Appendices** (🚧 coming): A Template Pack · B Repo Map & Migration · C High-Stakes Domains · D Failure-Mode Taxonomy · E Glossary

Prose CC BY-NC-SA 4.0 · code MIT ([LICENSE.md](LICENSE.md)) · [Contributing](CONTRIBUTING.md)
