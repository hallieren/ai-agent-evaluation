# Contributing

Three kinds of contribution, each handled differently.

## Errata and clarity fixes

Open a PR directly. Typos, factual errors, and unclear wording all qualify. For substantive prose changes, anything that alters an argument, a definition, or a book-wide concept (the three-part frame, the judgment ladder, the three axes), open an issue first. Book-wide concepts thread through every chapter, and a rewrite in one place has to land everywhere it echoes.

### Prose style

- Define a term inline at first use, before any forward reference relies on it.
- No bare "see Chapter X": every cross-chapter reference carries a one-line semantic gloss of what it points to (e.g., "the judgment ladder (escalating from assertions to LLM judges to humans, Chapter 5)").
- When the text announces "N things / three questions / four steps," render them as an N-item list, not a paragraph. Keep lists as lists.

## Code fixes (repo/)

Before opening a PR, pass the offline smoke (no API key needed):

```bash
cd repo
python world/world.py
python viewer/trace_viewer.py traces/examples/t-0007.jsonl
python -m compileall -q .
```

Constraint: zero third-party dependencies (pure stdlib, Python ≥ 3.10) is a deliberate design choice. PRs that introduce a dependency will not be accepted.

## New cases / templates

Cases go in the matching directory under `repo/cases/`, following the existing YAML fields; templates go in `repo/templates/chNN/`. After changing `repo/templates/` or `repo/labs/*/README.md`, regenerate the site pages (CI checks that the two stay in sync):

```bash
python3 scripts/gen_companion_pages.py   # generates docs/appendices/chNN-templates.md and docs/labs/chNN.md from repo/
uvx --with mkdocs-material mkdocs build  # or mkdocs serve for a local preview
```

Before submitting a case, read the coverage matrix in [Chapter 4, Building Eval Sets](docs/chapters/ch04-eval-sets.md), and say which empty cell your case fills.

## Licensing

By submitting, you agree that prose contributions are licensed under CC BY-NC-SA 4.0 and code contributions under MIT. For prose contributions you additionally grant the author the right to relicense your contribution, including in commercially published editions of this book. Code under MIT needs no additional grant.
