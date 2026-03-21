#!/usr/bin/env python3
"""Image-to-video: POST /v1/video_generation with first_frame_image, print task_id."""

from __future__ import annotations

import os
import sys

import minimax_http as mh


def main() -> None:
    body = {
        "model": os.environ.get("MODEL", "MiniMax-Hailuo-2.3-Fast"),
        "first_frame_image": os.environ.get(
            "FIRST_FRAME_IMAGE",
            "https://cdn.hailuoai.com/prod/2024-09-18-16/user/multi_chat_file/9c0b5c14-ee88-4a5b-b503-4f626f018639.jpeg",
        ),
        "prompt": os.environ.get("VIDEO_PROMPT", "Subtle camera push in, natural motion."),
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
