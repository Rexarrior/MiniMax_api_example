#!/usr/bin/env python3
"""Text-to-video: POST /v1/video_generation, print task_id."""

from __future__ import annotations

import os
import sys

import minimax_http as mh


def main() -> None:
    body = {
        "model": os.environ.get("MODEL", "MiniMax-Hailuo-2.3"),
        "prompt": os.environ.get("VIDEO_PROMPT", "A calm ocean at sunset, gentle waves."),
        "duration": int(os.environ.get("DURATION", "6")),
        "resolution": os.environ.get("RESOLUTION", "768P"),
        "prompt_optimizer": True,
    }
    d = mh.api_request("POST", "/v1/video_generation", body)
    mh.require_base_ok(d)
    tid = d["task_id"]
    p = mh.save_video_task_id(str(tid))
    print("Wrote", p, file=sys.stderr)
    print(tid)


if __name__ == "__main__":
    main()
