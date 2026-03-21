"""Minimal synchronous HTTP helpers for MiniMax REST API."""

from __future__ import annotations

import binascii
import copy
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import httpx

from _env import load_repo_dotenv, repo_root


def out_dir() -> Path:
    d = repo_root() / "out"
    d.mkdir(parents=True, exist_ok=True)
    return d


def api_base() -> str:
    return os.environ.get("MINIMAX_API_BASE", "https://api.minimax.io").rstrip("/")


def api_key() -> str:
    load_repo_dotenv()
    k = os.environ.get("MINIMAX_API_KEY", "")
    if not k:
        raise SystemExit("Set MINIMAX_API_KEY (see .env.example)")
    return k


def api_request(method: str, path: str, json_body: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.startswith("/"):
        path = "/" + path
    url = api_base() + path
    headers = {"Authorization": f"Bearer {api_key()}"}
    timeout = httpx.Timeout(300.0, connect=30.0)
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        if method.upper() == "GET":
            r = client.get(url, headers=headers)
        else:
            headers["Content-Type"] = "application/json"
            r = client.post(url, headers=headers, json=json_body)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected JSON root: {type(data)}")
    return data


def json_for_console(d: dict[str, Any]) -> dict[str, Any]:
    """Deep copy of API response safe for stdout/stderr: omits huge binary-ish strings."""
    out = copy.deepcopy(d)
    lyrics = out.get("lyrics")
    if isinstance(lyrics, str) and len(lyrics) > 1200:
        out["lyrics"] = f"<omitted {len(lyrics)} chars; see out/lyrics_*.txt>"
    data = out.get("data")
    if isinstance(data, dict):
        aud = data.get("audio")
        if isinstance(aud, str) and len(aud) > 120:
            data["audio"] = f"<omitted {len(aud)} hex chars; see out/*.mp3>"
        ib = data.get("image_base64")
        if isinstance(ib, str) and len(ib) > 120:
            data["image_base64"] = f"<omitted {len(ib)} base64 chars>"
        elif isinstance(ib, list):
            data["image_base64"] = [
                (
                    f"<omitted {len(x)} base64 chars>"
                    if isinstance(x, str) and len(x) > 120
                    else x
                )
                for x in ib
            ]
        for k, v in list(data.items()):
            if k == "image_base64" or k == "audio":
                continue
            if "base64" in k.lower() and isinstance(v, str) and len(v) > 120:
                data[k] = f"<omitted {len(v)} chars ({k})>"
    return out


def format_error_json(d: dict[str, Any]) -> str:
    return json.dumps(json_for_console(d), indent=2, ensure_ascii=False)


def require_base_ok(d: dict[str, Any]) -> None:
    if d.get("base_resp", {}).get("status_code") != 0:
        raise RuntimeError(format_error_json(d))


def write_hex_mp3(hex_audio: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(binascii.unhexlify(hex_audio.encode("ascii")))


def download_url_to_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": "minimax_explore/1"}
    with httpx.Client(timeout=httpx.Timeout(300.0, connect=30.0), follow_redirects=True) as client:
        r = client.get(url, headers=headers)
        r.raise_for_status()
        dest.write_bytes(r.content)


def poll_async_speech(task_id: str, max_rounds: int = 120, sleep_s: float = 2.0) -> tuple[str, str]:
    for _ in range(max_rounds):
        q = api_request("GET", f"/v1/query/t2a_async_query_v2?task_id={task_id}")
        require_base_ok(q)
        st = str(q.get("status", "")).lower()
        if st == "success":
            fid = q.get("file_id")
            if fid is None:
                raise RuntimeError(format_error_json(q))
            fid_s = str(fid)
            r = api_request("GET", f"/v1/files/retrieve?file_id={fid_s}")
            require_base_ok(r)
            url = (r.get("file") or {}).get("download_url") or ""
            if not url:
                raise RuntimeError(format_error_json(r))
            return str(url), fid_s
        if st in ("failed", "expired"):
            raise RuntimeError(format_error_json(q))
        time.sleep(sleep_s)
    raise TimeoutError("async speech task did not finish in time")


def poll_video_and_download(
    task_id: str,
    out_file: Path,
    max_rounds: int = 180,
    sleep_s: float = 3.0,
) -> None:
    for _ in range(max_rounds):
        q = api_request("GET", f"/v1/query/video_generation?task_id={task_id}")
        require_base_ok(q)
        st = str(q.get("status", "")).lower()
        if st == "success":
            fid = q.get("file_id")
            if fid is None:
                raise RuntimeError(format_error_json(q))
            r = api_request("GET", f"/v1/files/retrieve?file_id={fid}")
            require_base_ok(r)
            url = (r.get("file") or {}).get("download_url") or ""
            if not url:
                raise RuntimeError(format_error_json(r))
            download_url_to_file(str(url), out_file)
            return
        if st == "fail":
            raise RuntimeError(format_error_json(q))
        time.sleep(sleep_s)
    raise TimeoutError("video task did not finish in time")


def slug(s: str) -> str:
    t = re.sub(r"[^0-9a-zA-Z._-]+", "_", s).strip("_")
    return t or "artifact"


def save_music_mp3_from_response(d: dict[str, Any], model: str) -> Path | None:
    hex_audio = (d.get("data") or {}).get("audio")
    if not isinstance(hex_audio, str) or not hex_audio.strip():
        return None
    dest = out_dir() / f"music_{slug(model)}.mp3"
    write_hex_mp3(hex_audio, dest)
    return dest


def save_lyrics_txt_from_response(d: dict[str, Any]) -> Path:
    title = d.get("song_title") or "untitled"
    body = d.get("lyrics") or ""
    dest = out_dir() / f"lyrics_{slug(str(title))[:100]}.txt"
    dest.write_text(f"{title}\n\n{body}", encoding="utf-8")
    return dest


def save_image_urls_from_response(d: dict[str, Any], basename_prefix: str) -> list[Path]:
    urls = (d.get("data") or {}).get("image_urls") or []
    out: list[Path] = []
    for i, u in enumerate(urls):
        dest = out_dir() / f"{basename_prefix}_{i}.jpeg"
        download_url_to_file(str(u), dest)
        out.append(dest)
    return out


def save_video_task_id(task_id: str) -> Path:
    dest = out_dir() / "last_video_task_id.txt"
    dest.write_text(str(task_id).strip(), encoding="utf-8")
    return dest
