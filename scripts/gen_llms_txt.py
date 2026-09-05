#!/usr/bin/env python3
"""Generate docs/llms.txt and docs/llms-full.txt (https://llmstxt.org).

llms.txt is an index (title, one-line summary, one link per page); llms-full.txt
is the whole book as plain markdown, for agents that want to read it in one go.
Both are build outputs: run this before mkdocs build, do not commit the results.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TITLE = "AI Agent Evaluation"
SUMMARY = ("Score the endpoint, attribute the path, account for the side effects. Eval before you build. "
           "A free book on evaluating LLM agents, with one template per chapter and zero-dependency labs.")
SITE = "https://hallieren.github.io/ai-agent-evaluation/"
RAW = "https://raw.githubusercontent.com/hallieren/ai-agent-evaluation/main/docs/"
SECTIONS = [  # (heading, glob under docs/)
    ("Chapters", "chapters/*.md"),
    ("Labs", "labs/*.md"),
    ("Templates and appendices", "appendices/*.md"),
]
DOCS = ROOT / "docs"


def title_and_blurb(md: str) -> tuple[str, str]:
    title, blurb = "", ""
    for line in md.splitlines():
        s = line.strip()
        if not title:
            if s.startswith("# "):
                title = s[2:].strip()
            continue
        if not s or line.startswith((" ", "\t")) or s.startswith(("!!!", "![", "---", "<!--", "|", "```", "#")):
            continue
        blurb = re.sub(r"[*_`>]", "", s)
        blurb = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", blurb)
        break
    return title, blurb[:200]


def main() -> None:
    index = [f"# {TITLE}", "", f"> {SUMMARY}", "",
             f"Site: {SITE}  ", f"Full text in one file: {SITE}llms-full.txt", ""]
    full = [f"# {TITLE}", "", f"> {SUMMARY}", ""]
    for heading, pattern in SECTIONS:
        files = sorted(DOCS.glob(pattern))
        if not files:
            continue
        index += [f"## {heading}", ""]
        for f in files:
            md = f.read_text(encoding="utf-8")
            md = re.sub(r"<!--.*?-->\n*", "", md, flags=re.S)
            title, blurb = title_and_blurb(md)
            rel = f.relative_to(DOCS).as_posix()
            index.append(f"- [{title}]({RAW}{rel}): {blurb}" if blurb else f"- [{title}]({RAW}{rel})")
            full += ["", "---", "", md.strip(), ""]
        index.append("")
    (DOCS / "llms.txt").write_text("\n".join(index).rstrip() + "\n", encoding="utf-8", newline="\n")
    (DOCS / "llms-full.txt").write_text("\n".join(full).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"wrote docs/llms.txt ({sum(1 for l in index if l.startswith('- '))} pages) and docs/llms-full.txt")


if __name__ == "__main__":
    main()
