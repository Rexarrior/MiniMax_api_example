#!/usr/bin/env python3
"""CLI: one-shot web search via Mini-Agent + minimax_search MCP."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from websearch_agent import default_config_dir, ensure_websearch_env, run_query


def main() -> None:
    ensure_websearch_env()
    if len(sys.argv) < 2:
        print(
            'Usage: python app_examples/mini_agent_websearch/run_websearch_bot.py "your question"',
            file=sys.stderr,
        )
        sys.exit(2)

    if not os.environ.get("SERPER_API_KEY", "").strip():
        print(
            "Set SERPER_API_KEY in .env (https://serper.dev/) for web search.",
            file=sys.stderr,
        )
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    config_dir = default_config_dir()

    try:
        result = asyncio.run(run_query(query, config_dir))
        print(result)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
