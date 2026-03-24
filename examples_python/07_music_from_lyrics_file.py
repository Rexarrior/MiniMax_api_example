#!/usr/bin/env python3
"""
Generate music from a long lyrics file: split into several POST /v1/music_generation calls.

Официально «продолжение текста» есть у /v1/lyrics_generation (mode=edit), не у склейки аудио.
Длинное произведение здесь режется на части по лимиту символов в lyrics (music-2.0 ~3000).

Файл без тегов: добавляем [Verse] в начало и [Bridge] перед II–IV. Уже размеченный ([Verse]…)
не изменяем (см. --force-tag-plain). Склейка треков — локально (ffmpeg), не параметр API.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import minimax_http as mh
from _env import repo_root


def add_song_tags(raw: str) -> str:
    """Prepend [Verse]; before II, III, IV insert [Bridge]. Текст не меняется."""
    t = raw.strip()
    t = "[Verse]\n" + t
    t = re.sub(r"(\n{2,})(II|III|IV)(\n)", r"\1[Bridge]\n\2\3", t)
    return t


_TAG_AT_START = re.compile(
    r"^\s*\[(verse|intro|bridge|chorus|pre[\s-]?chorus)\]",
    re.IGNORECASE,
)


def ensure_song_tags(raw: str, *, force_plain: bool = False) -> str:
    """Если файл уже с тегами ([Verse]…), не трогаем; иначе — только разметка, без правки строк."""
    t = raw.strip()
    if not force_plain and _TAG_AT_START.match(t):
        return t
    return add_song_tags(raw)


def split_long_block(block: str, max_chars: int) -> list[str]:
    lines = block.split("\n")
    parts: list[str] = []
    cur: list[str] = []
    cur_len = 0
    for line in lines:
        extra = len(line) + (1 if cur else 0)
        if cur_len + extra <= max_chars:
            cur.append(line)
            cur_len += extra
        else:
            if cur:
                parts.append("\n".join(cur))
            cur = [line]
            cur_len = len(line)
    if cur:
        parts.append("\n".join(cur))
    return parts


def chunk_lyrics(tagged: str, max_chars: int, min_chars: int = 10) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n{2,}", tagged.strip()) if p.strip()]
    chunks: list[str] = []
    cur: list[str] = []
    cur_len = 0

    def flush() -> None:
        nonlocal cur, cur_len
        if cur:
            chunks.append("\n\n".join(cur))
            cur = []
            cur_len = 0

    for p in paras:
        sep = 2 if cur else 0
        if cur_len + sep + len(p) <= max_chars:
            cur.append(p)
            cur_len += sep + len(p)
            continue
        flush()
        if len(p) <= max_chars:
            cur = [p]
            cur_len = len(p)
        else:
            subs = split_long_block(p, max_chars)
            for piece in subs[:-1]:
                chunks.append(piece)
            if subs:
                cur = [subs[-1]]
                cur_len = len(subs[-1])
    flush()

    # склеить слишком короткий хвост с предыдущим
    fixed: list[str] = []
    for c in chunks:
        if len(c) < min_chars and fixed:
            fixed[-1] = fixed[-1] + "\n\n" + c
        else:
            fixed.append(c)
    return fixed


def default_max_lyrics(model: str) -> int:
    if "2.0" in model:
        return int(os.environ.get("MAX_LYRICS_CHARS", "2950"))
    return int(os.environ.get("MAX_LYRICS_CHARS", "3400"))


def try_concat_mp3(paths: list[Path], dest: Path) -> bool:
    ff = shutil.which("ffmpeg")
    if not ff or len(paths) < 2:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    lst = dest.parent / "_concat_list.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in paths), encoding="utf-8")
    r = subprocess.run(
        [ff, "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(dest)],
        capture_output=True,
        text=True,
    )
    lst.unlink(missing_ok=True)
    return r.returncode == 0


def main() -> None:
    root = repo_root()
    ap = argparse.ArgumentParser(description="Music generation from long lyrics file (multipart).")
    ap.add_argument(
        "lyrics_file",
        nargs="?",
        default=str(root / "my_liryc.txt"),
        help="Path to lyrics (default: repo my_liryc.txt)",
    )
    ap.add_argument("--model", default=os.environ.get("MODEL", "music-2.0"))
    ap.add_argument("--prompt", default=os.environ.get("MUSIC_PROMPT", ""))
    ap.add_argument("--max-chars", type=int, default=0, help="Override lyrics length limit per request")
    ap.add_argument("--write-tagged", action="store_true", help="Write <stem>_tagged.txt next to source")
    ap.add_argument("--concat", action="store_true", help="If ffmpeg exists, concat parts into one mp3")
    ap.add_argument(
        "--force-tag-plain",
        action="store_true",
        help="Всегда вставлять [Verse]/[Bridge], даже если файл уже начинается с [Verse]",
    )
    args = ap.parse_args()

    src = Path(args.lyrics_file).expanduser()
    if not src.is_file():
        raise SystemExit(f"Not found: {src}")

    raw = src.read_text(encoding="utf-8")
    tagged = ensure_song_tags(raw, force_plain=args.force_tag_plain)
    if args.write_tagged:
        out_tag = src.with_name(src.stem + "_tagged.txt")
        out_tag.write_text(tagged + "\n", encoding="utf-8")
        print("Wrote", out_tag, file=sys.stderr)

    max_c = args.max_chars or default_max_lyrics(args.model)
    parts = chunk_lyrics(tagged, max_c)
    print(f"model={args.model} parts={len(parts)} max_lyrics_chars={max_c}", file=sys.stderr)

    base_prompt = args.prompt or (
        "Epic dark symphonic metal, Russian male lead vocal, dramatic, solemn, "
        "orchestral metal, same song across segments"
    )

    slug = mh.slug(args.model)
    written: list[Path] = []
    total = len(parts)
    for i, lyrics in enumerate(parts, start=1):
        prompt = f"{base_prompt} (сегмент {i} из {total}, тот же трек и стиль)."
        req: dict = {
            "model": args.model,
            "prompt": prompt,
            "lyrics": lyrics,
            "stream": False,
            "output_format": "hex",
            "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"},
        }
        if "2.5" in args.model:
            req["lyrics_optimizer"] = False
        d = mh.api_request("POST", "/v1/music_generation", req)
        mh.require_base_ok(d)
        hex_audio = (d.get("data") or {}).get("audio")
        if not isinstance(hex_audio, str) or not hex_audio.strip():
            raise RuntimeError(mh.format_error_json(d))
        dest = mh.out_dir() / f"music_{slug}_part{i:02d}.mp3"
        mh.write_hex_mp3(hex_audio, dest)
        written.append(dest)
        print("Wrote", dest, file=sys.stderr)
        view = mh.json_for_console(d)
        if os.environ.get("MINIMAX_RAW_JSON", "0") == "1":
            print(json.dumps(view, ensure_ascii=False))
        else:
            print(json.dumps(view, indent=2, ensure_ascii=False))

    if args.concat and len(written) > 1:
        merged = mh.out_dir() / f"music_{slug}_all.mp3"
        if try_concat_mp3(written, merged):
            print("Wrote", merged, file=sys.stderr)
        else:
            print("ffmpeg not found or concat failed; parts are separate files.", file=sys.stderr)


if __name__ == "__main__":
    main()
