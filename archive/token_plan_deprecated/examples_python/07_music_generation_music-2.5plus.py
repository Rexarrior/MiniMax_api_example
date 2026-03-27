#!/usr/bin/env python3
"""Архив: music-2.5+ с INSTRUMENTAL=1 (is_instrumental) — вне таблицы Token Plan.

Запуск из корня репозитория:
  MODEL=music-2.5+ INSTRUMENTAL=1 PYTHONPATH=examples_python \\
    python3 archive/token_plan_deprecated/examples_python/07_music_generation_music-2.5plus.py
"""

from __future__ import annotations

import json
import os
import sys

import minimax_http as mh


def main() -> None:
    model = os.environ.get("MODEL", "music-2.5+")
    instrumental = os.environ.get("INSTRUMENTAL", "0") == "1"
    req: dict = {
        "model": model,
        "prompt": "Indie folk, melancholic, short demo clip.",
        "stream": False,
        "output_format": "hex",
        "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"},
    }
    if instrumental and "2.5+" in model:
        req["is_instrumental"] = True
    else:
        req["lyrics"] = (
            "Exegi monumentum aere perennius\n"
            "Regalique situ pyramidum altius\n"
            "Quod non imber edax, non aquilo impotens\n"
        )
        req["lyrics_optimizer"] = False

    d = mh.api_request("POST", "/v1/music_generation", req)
    mh.require_base_ok(d)
    mp3 = mh.save_music_mp3_from_response(d, model)
    if mp3:
        print("Wrote", mp3, file=sys.stderr)
    view = mh.json_for_console(d)
    if os.environ.get("MINIMAX_RAW_JSON", "0") == "1":
        print(json.dumps(view, ensure_ascii=False))
    else:
        print(json.dumps(view, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
