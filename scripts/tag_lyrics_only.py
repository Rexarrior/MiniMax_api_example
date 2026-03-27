#!/usr/bin/env python3
"""Tag my_liryc.txt without importing minimax_http (no httpx)."""
from __future__ import annotations

import re
import sys
from pathlib import Path


def add_song_tags(raw: str) -> str:
    t = raw.strip()
    t = "[Verse]\n" + t
    return re.sub(r"(\n{2,})(II|III|IV)(\n)", r"\1[Bridge]\n\2\3", t)


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    src = root / "my_liryc.txt"
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
    raw = src.read_text(encoding="utf-8")
    out = src.with_name(src.stem + "_tagged.txt")
    out.write_text(add_song_tags(raw) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
