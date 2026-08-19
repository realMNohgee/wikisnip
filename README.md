# wikisnip 📚
![CI](https://github.com/realMNohgee/wikisnip/actions/workflows/ci.yml/badge.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Wikipedia summary lookup — no API key needed.** Zero dependencies, pure Python stdlib.

> Part of the **Trust & Reliability Layer for Agentic AI**

## Why it exists
LLM agents need fast, structured access to factual knowledge without paying for API credits. `wikisnip` wraps the Wikipedia API with a clean CLI: search, get summaries by title, or fetch random articles — all in text or JSON output.

## One tool, many domains

| Domain | What wikisnip does |
|---|---|
| **Agentic AI** | Ground LLM outputs with Wikipedia facts |
| **Research** | Quick fact-checking and topic overviews |
| **Education** | Pull concise summaries for study |
| **CLI productivity** | Look things up without leaving the terminal |
| **Data pipelines** | Structured JSON extraction from Wikipedia |

## Install

```bash
git clone git@github.com:realMNohgee/wikisnip.git
cd wikisnip
python3 wikisnip.py --help
```

## Quick start

```bash
# Search Wikipedia
python3 wikisnip.py search "quantum computing"

# Get a page summary (3 sentences)
python3 wikisnip.py summary "Python (programming language)" --sentences 5

# Random article
python3 wikisnip.py random

# JSON output
python3 wikisnip.py search "AI" --format json
```

## License

MIT — see [LICENSE](LICENSE).

---
🧰 **[Tool on Hermtica Marketplace](https://hermtica.com/marketplace)**
