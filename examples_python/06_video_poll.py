#!/usr/bin/env python3
"""Poll GET /v1/query/video_generation, then download video to out/."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import minimax_http as mh


def main() -> None:
    task_id = os.environ.get("TASK_ID") or (sys.argv[1] if len(sys.argv) > 1 else "")
    if not task_id:
        print("Usage: TASK_ID=<id> python 06_video_poll.py   or   python 06_video_poll.py <task_id>", file=sys.stderr)
        sys.exit(1)

    out = os.environ.get("OUT_FILE", str(mh.out_dir() / f"video_{task_id}.mp4"))
    mh.poll_video_and_download(str(task_id), Path(out))
    print("Wrote", out, file=sys.stderr)


if __name__ == "__main__":
    main()
