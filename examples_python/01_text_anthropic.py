#!/usr/bin/env python3
"""MiniMax text via Anthropic-compatible endpoint. See https://platform.minimax.io/docs/api-reference/text-anthropic-api"""

from __future__ import annotations

import os
import sys

from anthropic import Anthropic

import minimax_http as mh
from _env import load_repo_dotenv


def main() -> None:
    load_repo_dotenv()
    key = os.environ.get("MINIMAX_API_KEY")
    if not key:
        print("Set MINIMAX_API_KEY (see .env.example)", file=sys.stderr)
        sys.exit(1)

    model = os.environ.get("MINIMAX_TEXT_MODEL", "MiniMax-M2.7")
    client = Anthropic(api_key=key, base_url="https://api.minimax.io/anthropic")

    message = client.messages.create(
        model=model,
        max_tokens=512,
        system="You are a helpful assistant.",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": "Say hi in one short sentence."}],
            }
        ],
    )

    parts: list[str] = []
    for block in message.content:
        t = getattr(block, "type", None)
        if t == "thinking":
            s = getattr(block, "thinking", "")
            print(s, end="")
            parts.append(s)
        elif t == "text":
            s = getattr(block, "text", "")
            print(s, end="")
            parts.append(s)

    out = mh.out_dir() / "last_text_reply.txt"
    out.write_text("".join(parts), encoding="utf-8")
    print(file=sys.stderr)
    print("Wrote", out, file=sys.stderr)


if __name__ == "__main__":
    main()
