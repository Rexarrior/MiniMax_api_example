#!/usr/bin/env python3
"""POST /v1/lyrics_generation."""

from __future__ import annotations

import json
import os
import sys

import minimax_http as mh


def main() -> None:
    body = {
        "mode": os.environ.get("MODE", "write_full_song"),
        "prompt": os.environ.get(
            "PROMPT",
            "A cheerful love song about a summer day at the beach",
        ),
    }
    d = mh.api_request("POST", "/v1/lyrics_generation", body)
    mh.require_base_ok(d)
    txt = mh.save_lyrics_txt_from_response(d)
    print("Wrote", txt, file=sys.stderr)
    view = mh.json_for_console(d)
    if os.environ.get("MINIMAX_RAW_JSON", "0") == "1":
        print(json.dumps(view, ensure_ascii=False))
    else:
        print(json.dumps(view, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
