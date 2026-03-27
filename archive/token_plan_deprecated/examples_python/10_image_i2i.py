#!/usr/bin/env python3
"""Image-to-image: POST /v1/image_generation, model image-01-live + subject_reference."""

from __future__ import annotations

import json
import os
import sys

import minimax_http as mh


def main() -> None:
    body = {
        "model": "image-01-live",
        "prompt": os.environ.get(
            "PROMPT",
            "A girl looking into the distance from a library window, cinematic light.",
        ),
        "aspect_ratio": "16:9",
        "response_format": "url",
        "n": 1,
        "subject_reference": [
            {
                "type": "character",
                "image_file": os.environ.get(
                    "SUBJECT_IMAGE",
                    "https://cdn.hailuoai.com/prod/2025-08-12-17/video_cover/1754990600020238321-411603868533342214-cover.jpg",
                ),
            },
        ],
    }
    d = mh.api_request("POST", "/v1/image_generation", body)
    mh.require_base_ok(d)
    for p in mh.save_image_urls_from_response(d, "image_i2i"):
        print("Wrote", p, file=sys.stderr)
    view = mh.json_for_console(d)
    if os.environ.get("MINIMAX_RAW_JSON", "0") == "1":
        print(json.dumps(view, ensure_ascii=False))
    else:
        print(json.dumps(view, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
