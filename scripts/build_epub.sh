#!/usr/bin/env bash
# Build the whole book as one EPUB for offline reading: 16 chapters, 16 template pages, appendices A to E. Requires pandoc.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build
files=(docs/chapters/ch*.md docs/appendices/appendix-*.md docs/appendices/ch*-templates.md)
pandoc "${files[@]}" \
  --metadata title="AI Agent Evaluation" --metadata author="Hallie Ren" --metadata lang=en \
  --toc --toc-depth=2 --resource-path=docs:docs/chapters:docs/appendices \
  -o build/ai-agent-evaluation.epub
echo "OK: build/ai-agent-evaluation.epub"
