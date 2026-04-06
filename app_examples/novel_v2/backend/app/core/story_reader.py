from abc import ABC, abstractmethod
from typing import Optional


class StoryReader(ABC):
    """Abstraction for reading story content - audio, voice, video"""

    @abstractmethod
    async def get_audio_url(self, story_id: str, audio_name: str) -> Optional[str]:
        """Get URL for background music"""
        pass

    @abstractmethod
    async def get_voice_url(
        self, story_id: str, character: str, voice_id: str
    ) -> Optional[str]:
        """Get URL for character voice line"""
        pass

    @abstractmethod
    async def get_video_url(self, story_id: str, video_name: str) -> Optional[str]:
        """Get URL for video asset"""
        pass

    @abstractmethod
    async def get_character_image_url(
        self, story_id: str, character: str, mood: Optional[str] = None
    ) -> Optional[str]:
        """Get URL for character image"""
        pass

    @abstractmethod
    async def get_background_url(
        self, story_id: str, background_name: str
    ) -> Optional[str]:
        """Get URL for background image"""
        pass

    @abstractmethod
    async def get_image_url(self, story_id: str, image_name: str) -> Optional[str]:
        """Get URL for any image by exact filename"""
        pass
