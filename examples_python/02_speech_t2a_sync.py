#!/usr/bin/env python3
"""Synchronous TTS: POST /v1/t2a_v2 → out/t2a_sync.mp3"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import minimax_http as mh


def main() -> None:
    model = os.environ.get("MODEL", "speech-2.8-hd")
    out = os.environ.get("OUT_FILE", str(mh.out_dir() / "t2a_sync.mp3"))

    body = {
        "model": model,
        "text": "Hello from MiniMax synchronous text to speech.",
        "stream": False,
        "language_boost": "auto",
        "output_format": "hex",
        "voice_setting": {
            "voice_id": "English_expressive_narrator",
            "speed": 1,
            "vol": 1,
            "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }

    d = mh.api_request("POST", "/v1/t2a_v2", body)
    mh.require_base_ok(d)
    hex_audio = d["data"]["audio"]
    mh.write_hex_mp3(hex_audio, Path(out))
    print("Wrote", out, file=sys.stderr)


if __name__ == "__main__":
    main()
