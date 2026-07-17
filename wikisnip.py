#!/usr/bin/env python3
"""wikisnip — Wikipedia summary lookup. Zero dependencies, pure Python stdlib."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

WIKI_API = "https://en.wikipedia.org/w/api.php"


def _api_request(params):
    """Make a Wikipedia API request, return parsed JSON."""
    params["format"] = "json"
    url = WIKI_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "wikisnip/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Error: could not reach Wikipedia API: {e}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code} from Wikipedia API", file=sys.stderr)
        sys.exit(1)


def cmd_search(args):
    """Search Wikipedia and return top results."""
    data = _api_request({
        "action": "opensearch",
        "search": args.query,
        "limit": 5,
        "namespace": 0,
    })
    query, titles, descriptions, urls = data

    if not titles:
        if args.format == "json":
            print(json.dumps([]))
        else:
            print(f"No results found for '{args.query}'.")
        sys.exit(1)

    results = []
    for i, title in enumerate(titles):
        results.append({
            "title": title,
            "description": descriptions[i] if descriptions[i] else "(no description)",
            "url": urls[i],
        })

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        for i, r in enumerate(results):
            print(f"{i + 1}. {r['title']}")
            if r["description"]:
                print(f"   {r['description']}")
            print()


def cmd_summary(args):
    """Get a Wikipedia page extract."""
    data = _api_request({
        "action": "query",
        "prop": "extracts",
        "exintro": "",
        "explaintext": "",
        "titles": args.title,
        "exsentences": args.sentences,
        "redirects": "",
    })

    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            print(f"Error: page '{args.title}' not found.", file=sys.stderr)
            sys.exit(1)

        extract = page.get("extract", "")

        # Check for disambiguation
        if "may refer to:" in extract[:500] or "may refer to:" in (extract or ""):
            print(f"Warning: '{args.title}' may be a disambiguation page.",
                  file=sys.stderr)

        if not extract:
            print(f"Error: no extract available for '{args.title}'.",
                  file=sys.stderr)
            sys.exit(1)

        if args.format == "json":
            print(json.dumps({"title": page.get("title", args.title),
                              "extract": extract}, indent=2))
        else:
            print(f"=== {page.get('title', args.title)} ===\n")
            print(extract)


def cmd_random(args):
    """Fetch a random Wikipedia article summary."""
    data = _api_request({
        "action": "query",
        "prop": "extracts",
        "exintro": "",
        "explaintext": "",
        "generator": "random",
        "grnnamespace": 0,
        "grnlimit": 1,
    })

    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        title = page.get("title", "Unknown")
        extract = page.get("extract", "")

        if args.format == "json":
            print(json.dumps({"title": title, "extract": extract}, indent=2))
        else:
            print(f"=== {title} ===\n")
            print(extract)
        return

    print("Error: could not fetch a random article.", file=sys.stderr)
    sys.exit(1)


def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")

    p = argparse.ArgumentParser(
        description="wikisnip — Wikipedia summary lookup (no API key needed)."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sp_search = sub.add_parser("search", parents=[common],
                               help="Search Wikipedia")
    sp_search.add_argument("query", help="Search query")

    sp_summary = sub.add_parser("summary", parents=[common],
                                help="Get page summary")
    sp_summary.add_argument("title", help="Page title")
    sp_summary.add_argument("--sentences", type=int, default=3,
                            help="Number of sentences (default: 3)")

    sp_random = sub.add_parser("random", parents=[common],
                               help="Random article summary")

    args = p.parse_args()

    if args.cmd == "search":
        cmd_search(args)
    elif args.cmd == "summary":
        cmd_summary(args)
    elif args.cmd == "random":
        cmd_random(args)


if __name__ == "__main__":
    main()
