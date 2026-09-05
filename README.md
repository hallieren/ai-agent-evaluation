# AI Agent Evaluation

[![smoke](https://github.com/hallieren/ai-agent-evaluation/actions/workflows/smoke.yml/badge.svg)](https://github.com/hallieren/ai-agent-evaluation/actions/workflows/smoke.yml) [![docs](https://github.com/hallieren/ai-agent-evaluation/actions/workflows/docs.yml/badge.svg)](https://github.com/hallieren/ai-agent-evaluation/actions/workflows/docs.yml)

> Score the endpoint, attribute the path, account for the side effects. Eval before you build. Written for engineers pushing agents toward production, the ones asked "can we ship?" with no evidence in hand. Sixteen chapters, one wall and one template each; the companion repo runs with zero dependencies (pure stdlib, Python ≥ 3.10).

*Shore & Summit is a synthetic teaching world assembled from common enterprise scenarios; it does not correspond to any real company, and every character in this book is fictional.*

All 16 chapters and the five appendices are live. Each chapter is paired with an applied essay on the author's Substack: [hallieren.substack.com](https://hallieren.substack.com).

## How to read

- **Online**: <https://hallieren.github.io/ai-agent-evaluation/> (full-text search, dark mode, previous/next chapter).
- **On GitHub**: the chapter links below render directly. The reading guide and the three reading paths are in [docs/index.md](docs/index.md); companion code is in [repo/](repo/README.md).
- **Offline**: [EPUB](https://hallieren.github.io/ai-agent-evaluation/ai-agent-evaluation.epub), or build it yourself with `./scripts/build_epub.sh` (needs pandoc).
- **Locally**: `uvx --from mkdocs-material mkdocs serve` and open <http://127.0.0.1:8000>.

## Hand it to your agent

Every chapter's Lab opens with a prompt you paste into Claude Code, Codex, or any coding agent; it runs the chapter's steps and stops where the judgment is yours. The one-time setup prompt is on the [home page](docs/index.md). Agents can read the whole book from [llms.txt](https://hallieren.github.io/ai-agent-evaluation/llms.txt) (index) and [llms-full.txt](https://hallieren.github.io/ai-agent-evaluation/llms-full.txt) (full text).

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

**Appendices** [A Template Pack](docs/appendices/appendix-a-template-pack.md) · [B Repo Map and Migration](docs/appendices/appendix-b-repo-and-migration.md) · [C High-Stakes Domains](docs/appendices/appendix-c-high-stakes.md) · [D Failure-Mode Taxonomy](docs/appendices/appendix-d-failure-taxonomy.md) · [E Glossary](docs/appendices/appendix-e-glossary.md)

Prose CC BY-NC-SA 4.0 · code MIT ([LICENSE.md](LICENSE.md)) · [Contributing](CONTRIBUTING.md) · [How to cite](CITATION.cff)
