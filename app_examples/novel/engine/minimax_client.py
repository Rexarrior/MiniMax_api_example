"""MiniMax API client for visual novel assets."""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "examples_python"))
from minimax_http import (
    api_request,
    download_url_to_file,
    save_image_urls_from_response,
    save_music_mp3_from_response,
    out_dir,
)


class MiniMaxClient:
    def __init__(self, cache_dir: Path | None = None):
        if cache_dir is None:
            cache_dir = out_dir() / "novel_assets"
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _story_cache(self, story_id: str) -> Path:
        d = self.cache_dir / story_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def generate_image(self, story_id: str, prompt: str) -> Path | None:
        cache = self._story_cache(story_id) / "images"
        cache.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(c if c.isalnum() else "_" for c in prompt)[:50]
        cached = cache / f"{safe_name}.jpeg"
        if cached.exists():
            return cached
        try:
            resp = api_request(
                "POST",
                "/v1/image_generation",
                {"model": "image-01", "prompt": prompt},
            )
            paths = save_image_urls_from_response(resp, str(cache / safe_name))
            return paths[0] if paths else None
        except Exception:
            return None

    def generate_music(self, story_id: str, prompt: str) -> Path | None:
        cache = self._story_cache(story_id) / "music"
        cache.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(c if c.isalnum() else "_" for c in prompt)[:50]
        cached = cache / f"{safe_name}.mp3"
        if cached.exists():
            return cached
        try:
            resp = api_request(
                "POST",
                "/v1/music_generation",
                {"model": "music-2.5", "prompt": prompt},
            )
            path = save_music_mp3_from_response(resp, safe_name)
            return path
        except Exception:
            return None
