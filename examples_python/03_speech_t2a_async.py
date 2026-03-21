#!/usr/bin/env python3
"""Async TTS: create → query → files/retrieve → print download URL."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import minimax_http as mh


def main() -> None:
    model = os.environ.get("MODEL", "speech-2.8-hd")
    body = {
        "model": model,
        "text": "This is a short async MiniMax speech demo.",
        "language_boost": "auto",
        "voice_setting": {
            "voice_id": "English_expressive_narrator",
            "speed": 1,
            "vol": 1,
            "pitch": 0,
        },
        "audio_setting": {
            "audio_sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 2,
        },
    }

    create = mh.api_request("POST", "/v1/t2a_async_v2", body)
    mh.require_base_ok(create)
    task_id = create["task_id"]
    print(f"task_id={task_id}")

    url, file_id = mh.poll_async_speech(str(task_id))
    print(f"status=success file_id={file_id}")
    safe = mh.slug(model)
    dest = Path(os.environ.get("OUT_FILE", str(mh.out_dir() / f"t2a_async_{safe}.mp3")))
    mh.download_url_to_file(url, dest)
    print("Wrote", dest, file=sys.stderr)
    print(url)


if __name__ == "__main__":
    main()
