#!/usr/bin/env python3
"""Read JSON from stdin, print console-safe JSON (redacts huge binary-ish fields)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import minimax_http as mh  # noqa: E402


def main() -> None:
    d = json.load(sys.stdin)
    v = mh.json_for_console(d)
    raw = os.environ.get("MINIMAX_RAW_JSON", "0") == "1"
    if raw:
        print(json.dumps(v, ensure_ascii=False))
    else:
        print(json.dumps(v, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
