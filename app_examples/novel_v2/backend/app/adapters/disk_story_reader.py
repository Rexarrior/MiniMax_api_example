from app.core.story_reader import StoryReader
from pathlib import Path
from typing import Optional


class DiskStoryReader(StoryReader):
    """
    Story reader that reads pre-recorded audio files from disk.
    Currently used for:
    - Background music (mp3)
    - Voice lines (mp3)
    - Character images (png/jpg)
    - Background images (png/jpg)
    - Videos (mp4/webm)

    Future implementations could use TTS APIs or CDN-based streaming.
    """

    def __init__(self, stories_dir: str, media_base_url: str = "/api/media"):
        self.stories_dir = Path(stories_dir)
        self.media_base_url = media_base_url

    def _get_url(self, story_id: str, *parts: str) -> str:
        """Build a media URL from parts"""
        return f"{self.media_base_url}/{story_id}/" + "/".join(parts)

    async def get_audio_url(self, story_id: str, audio_name: str) -> Optional[str]:
        """Get URL for background music"""
        # Check if audio_name already has an extension
        base_name = audio_name
        for ext in [".mp3", ".ogg", ".wav"]:
            if audio_name.lower().endswith(ext):
                base_name = audio_name[: -len(ext)]
                break

        for ext in [".mp3", ".ogg", ".wav"]:
            path = (
                self.stories_dir / story_id / "assets" / "music" / f"{base_name}{ext}"
            )
            if path.exists():
                return self._get_url(story_id, "assets", "music", f"{base_name}{ext}")
        return None

    async def get_voice_url(
        self, story_id: str, character: str, voice_id: str
    ) -> Optional[str]:
        """Get URL for character voice line"""
        path = self.stories_dir / story_id / "assets" / "voices" / voice_id
        if path.exists():
            return self._get_url(story_id, "assets", "voices", voice_id)

        mp3_path = self.stories_dir / story_id / "assets" / "voices" / f"{voice_id}.mp3"
        if mp3_path.exists():
            return self._get_url(story_id, "assets", "voices", f"{voice_id}.mp3")

        return None

    async def get_video_url(self, story_id: str, video_name: str) -> Optional[str]:
        """Get URL for video asset"""
        for ext in [".mp4", ".webm"]:
            path = (
                self.stories_dir / story_id / "assets" / "videos" / f"{video_name}{ext}"
            )
            if path.exists():
                return self._get_url(story_id, "assets", "videos", f"{video_name}{ext}")
        path = self.stories_dir / story_id / "assets" / "videos" / video_name
        if path.exists():
            return self._get_url(story_id, "assets", "videos", video_name)
        return None

    async def get_character_image_url(
        self, story_id: str, character: str, mood: Optional[str] = None
    ) -> Optional[str]:
        """Get URL for character image.

        If character_image_url is already a full filename (starts with 'char_' or 'bg_'),
        treat it as an exact filename match and resolve directly.
        Otherwise, build filename from character and mood.
        """
        images_dir = self.stories_dir / story_id / "assets" / "images"

        if not images_dir.exists():
            return None

        # If character looks like a full filename (starts with 'char_' or 'bg_'),
        # try to find it directly
        if character and character.startswith(("char_", "bg_")):
            for ext in [".png", ".jpg", ".jpeg", ".webp"]:
                path = images_dir / f"{character}{ext}"
                if path.exists():
                    return self._get_url(
                        story_id, "assets", "images", f"{character}{ext}"
                    )
            # Try without extension
            path = images_dir / character
            if path.exists():
                return self._get_url(story_id, "assets", "images", character)

        # Otherwise build from character and mood
        if mood:
            for ext in [".png", ".jpg", ".jpeg", ".webp"]:
                path = images_dir / f"{character}_{mood}{ext}"
                if path.exists():
                    return self._get_url(
                        story_id, "assets", "images", f"{character}_{mood}{ext}"
                    )

        for ext in [".png", ".jpg", ".jpeg", ".webp"]:
            path = images_dir / f"{character}{ext}"
            if path.exists():
                return self._get_url(story_id, "assets", "images", f"{character}{ext}")

            path = images_dir / f"{character}_{mood}{ext}" if mood else None
            if path and path.exists():
                return self._get_url(
                    story_id, "assets", "images", f"{character}_{mood}{ext}"
                )

        return None

    async def get_background_url(
        self, story_id: str, background_name: str
    ) -> Optional[str]:
        """Get URL for background image"""
        images_dir = self.stories_dir / story_id / "assets" / "images"

        for ext in [".png", ".jpg", ".jpeg", ".webp"]:
            path = images_dir / f"{background_name}{ext}"
            if path.exists():
                return self._get_url(
                    story_id, "assets", "images", f"{background_name}{ext}"
                )

        path = images_dir / background_name
        if path.exists():
            return self._get_url(story_id, "assets", "images", background_name)

        return None

    async def get_image_url(self, story_id: str, image_name: str) -> Optional[str]:
        """Get URL for any image by exact filename (without extension check)"""
        images_dir = self.stories_dir / story_id / "assets" / "images"

        # If image_name has extension, try directly
        for ext in ["", ".png", ".jpg", ".jpeg", ".webp"]:
            path = images_dir / f"{image_name}{ext}" if ext else images_dir / image_name
            if path.exists():
                return self._get_url(
                    story_id,
                    "assets",
                    "images",
                    f"{image_name}{ext}" if ext else image_name,
                )

        return None
