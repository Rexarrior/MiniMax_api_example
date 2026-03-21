#!/usr/bin/env python3
"""Text-to-image: POST /v1/image_generation, model image-01."""

from __future__ import annotations

import json
import os
import sys

import minimax_http as mh


def main() -> None:
    body = {
        "model": "image-01",
        "prompt": os.environ.get(
            "PROMPT",
            "A man in a white t-shirt, full-body, standing outdoors, photorealistic, soft daylight.",
        ),
        "aspect_ratio": "16:9",
        "response_format": "url",
        "n": 1,
        "prompt_optimizer": False,
    }
    d = mh.api_request("POST", "/v1/image_generation", body)
    mh.require_base_ok(d)
    for p in mh.save_image_urls_from_response(d, "image_t2i"):
        print("Wrote", p, file=sys.stderr)
    view = mh.json_for_console(d)
    if os.environ.get("MINIMAX_RAW_JSON", "0") == "1":
        print(json.dumps(view, ensure_ascii=False))
    else:
        print(json.dumps(view, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
