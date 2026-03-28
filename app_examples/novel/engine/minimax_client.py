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
    def __init__(self, stories_dir: Path | None = None):
        if stories_dir is None:
            stories_dir = Path(__file__).parent.parent / "stories"
        self.stories_dir = stories_dir

    def _get_assets_dir(self, story_id: str) -> Path:
        return self.stories_dir / story_id / "assets"

    def generate_image(self, story_id: str, prompt: str) -> Path | None:
        assets = self._get_assets_dir(story_id) / "images"
        assets.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(c if c.isalnum() else "_" for c in prompt)[:50]
        cached = assets / f"{safe_name}_0.jpeg"
        if cached.exists():
            return cached
        try:
            resp = api_request(
                "POST",
                "/v1/image_generation",
                {"model": "image-01", "prompt": prompt},
            )
            paths = save_image_urls_from_response(resp, str(assets / safe_name))
            return paths[0] if paths else None
        except Exception:
            return None

    def generate_music(self, story_id: str, prompt: str) -> Path | None:
        assets = self._get_assets_dir(story_id) / "music"
        assets.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(c if c.isalnum() else "_" for c in prompt)[:50]
        cached = assets / f"{safe_name}.mp3"
        if cached.exists():
            return cached
        lyrics = f"Instrumental ambient music: {prompt}"
        try:
            resp = api_request(
                "POST",
                "/v1/music_generation",
                {
                    "model": "music-2.5",
                    "prompt": prompt,
                    "lyrics": lyrics,
                    "lyrics_optimizer": False,
                    "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"},
                },
            )
            hex_audio = (resp.get("data") or {}).get("audio")
            if not isinstance(hex_audio, str) or not hex_audio.strip():
                return None
            import binascii
            cached.write_bytes(binascii.unhexlify(hex_audio.encode("ascii")))
            return cached
        except Exception:
            return None

    def generate_background_image(self, story_id: str, scene_id: str, prompt: str) -> Path | None:
        assets = self._get_assets_dir(story_id) / "images"
        assets.mkdir(parents=True, exist_ok=True)
        safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt)[:50]
        safe_scene = "".join(c if c.isalnum() else "_" for c in scene_id)[:30]
        cached = assets / f"bg_{safe_scene}_{safe_prompt}_0.jpeg"
        if cached.exists():
            return cached
        try:
            resp = api_request(
                "POST",
                "/v1/image_generation",
                {"model": "image-01", "prompt": prompt},
            )
            paths = save_image_urls_from_response(resp, str(assets / f"bg_{safe_scene}_{safe_prompt}"))
            return paths[0] if paths else None
        except Exception:
            return None

    def generate_character_image(self, story_id: str, scene_id: str, character_id: str, prompt: str) -> Path | None:
        assets = self._get_assets_dir(story_id) / "images"
        assets.mkdir(parents=True, exist_ok=True)
        safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt)[:50]
        safe_scene = "".join(c if c.isalnum() else "_" for c in scene_id)[:30]
        safe_char = "".join(c if c.isalnum() else "_" for c in character_id)[:30]
        cached = assets / f"char_{safe_scene}_{safe_char}_{safe_prompt}_0.jpeg"
        if cached.exists():
            return cached
        try:
            resp = api_request(
                "POST",
                "/v1/image_generation",
                {"model": "image-01", "prompt": prompt},
            )
            paths = save_image_urls_from_response(resp, str(assets / f"char_{safe_scene}_{safe_char}_{safe_prompt}"))
            return paths[0] if paths else None
        except Exception:
            return None
