"""MiniMax API client for visual novel assets."""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "examples_python"))
from minimax_http import (
    api_request,
    download_url_to_file,
    save_image_urls_from_response,
    save_music_mp3_from_response,
    generate_speech,
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
                    "audio_setting": {
                        "sample_rate": 44100,
                        "bitrate": 256000,
                        "format": "mp3",
                    },
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

    def generate_background_image(
        self, story_id: str, scene_id: str, prompt: str, skip_generation: bool = False
    ) -> Path | None:
        assets = self._get_assets_dir(story_id) / "images"
        assets.mkdir(parents=True, exist_ok=True)
        safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt)[:50]
        safe_scene = "".join(c if c.isalnum() else "_" for c in scene_id)[:30]
        cached = assets / f"bg_{safe_scene}_{safe_prompt}_0.jpeg"
        if cached.exists():
            return cached
        if skip_generation:
            return None
        try:
            resp = api_request(
                "POST",
                "/v1/image_generation",
                {"model": "image-01", "prompt": prompt},
            )
            paths = save_image_urls_from_response(
                resp, str(assets / f"bg_{safe_scene}_{safe_prompt}")
            )
            return paths[0] if paths else None
        except Exception:
            return None

    def generate_character_image(
        self,
        story_id: str,
        scene_id: str,
        character_id: str,
        prompt: str,
        mood: str | None = None,
        skip_generation: bool = False,
    ) -> Path | None:
        assets = self._get_assets_dir(story_id) / "images"
        assets.mkdir(parents=True, exist_ok=True)
        safe_prompt = "".join(c if c.isalnum() else "_" for c in prompt)[:40]
        safe_scene = "".join(c if c.isalnum() else "_" for c in scene_id)[:30]
        safe_char = "".join(c if c.isalnum() else "_" for c in character_id)[:20]
        safe_mood = "".join(c if c.isalnum() else "_" for c in (mood or ""))[:20]
        cached = (
            assets / f"char_{safe_scene}_{safe_char}_{safe_mood}_{safe_prompt}_0.jpeg"
        )
        if cached.exists():
            return cached
        if skip_generation:
            return None
        try:
            resp = api_request(
                "POST",
                "/v1/image_generation",
                {"model": "image-01", "prompt": prompt},
            )
            paths = save_image_urls_from_response(
                resp,
                str(
                    assets / f"char_{safe_scene}_{safe_char}_{safe_mood}_{safe_prompt}"
                ),
            )
            return paths[0] if paths else None
        except Exception:
            return None

    def _get_mp3_duration(self, mp3_path: Path) -> int:
        try:
            from mutagen import File as MutagenFile

            audio = MutagenFile(str(mp3_path))
            if audio and audio.info:
                return int(audio.info.length * 1000)
        except Exception:
            pass
        return 0

    def generate_voice(
        self,
        story_id: str,
        character_id: str,
        text: str,
        voice_id: str = "English_Graceful_Lady",
        speed: float = 1.0,
        pitch: int = 0,
        skip_generation: bool = False,
    ) -> dict | None:
        import hashlib

        assets = self._get_assets_dir(story_id) / "voices"
        assets.mkdir(parents=True, exist_ok=True)
        safe_char = "".join(c if c.isalnum() else "_" for c in character_id)[:20]
        text_hash = hashlib.md5(text.encode()).hexdigest()[:10]
        cached = assets / f"voice_{safe_char}_{text_hash}_{speed}_{pitch}.mp3"
        if cached.exists():
            duration_ms = self._get_mp3_duration(cached)
            return {"path": cached, "duration_ms": duration_ms, "cached": True}
        if skip_generation:
            return None
        try:
            result = generate_speech(text, voice_id, cached, speed, pitch)
            if result:
                return {
                    "path": result["path"],
                    "duration_ms": result.get("duration_ms", 0),
                    "cached": False,
                }
            return None
        except Exception:
            return None
