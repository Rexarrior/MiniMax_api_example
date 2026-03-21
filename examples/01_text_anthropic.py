#!/usr/bin/env python3
"""MiniMax text via Anthropic-compatible endpoint. See https://platform.minimax.io/docs/api-reference/text-anthropic-api"""

import os
import sys

from anthropic import Anthropic


def main() -> None:
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

    for block in message.content:
        t = getattr(block, "type", None)
        if t == "thinking":
            print(getattr(block, "thinking", ""), end="")
        elif t == "text":
            print(getattr(block, "text", ""), end="")


if __name__ == "__main__":
    main()
