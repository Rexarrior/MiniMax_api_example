from app.core.scene_adapter import (
    SceneAdapter,
    SceneData,
    StoryMetadata,
    Character,
    DialogueLine,
    Choice,
)
from app.core.exceptions import StoryNotFoundError, SceneNotFoundError
from pathlib import Path
from typing import Optional
import yaml
import os


class DiskSceneAdapter(SceneAdapter):
    def __init__(self, stories_dir: str):
        self.stories_dir = Path(stories_dir)

    async def load_scene(self, story_id: str, scene_id: str) -> SceneData:
        story_path = self.stories_dir / story_id
        if not story_path.exists():
            raise StoryNotFoundError(f"Story not found: {story_id}")

        scene_path = story_path / "scenes" / f"{scene_id}.scn"
        if not scene_path.exists():
            raise SceneNotFoundError(f"Scene not found: {scene_id} in story {story_id}")

        with open(scene_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        dialogues = []
        for d in data.get("dialogue", []):
            if "narrator" in d:
                # Support both 'voice' (path) and 'voice_url' fields for narrator
                narrator_voice = d.get("voice") or d.get("voice_url")
                dialogues.append(
                    DialogueLine(
                        speaker="narrator",
                        text=d["narrator"],
                        mood=None,
                        voice_url=narrator_voice,
                        character_image_url=None,
                    )
                )
            elif "character" in d:
                char_data = d["character"]
                # Handle both 'image' and 'image_prompt' keys for character image
                char_image = None
                char_voice = None
                if isinstance(char_data, str):
                    # character is just an ID string - text/mood are at same level as 'character' in d
                    char_image = None
                    char_voice = None
                    speaker = char_data
                    text = d.get("text", "")
                    mood = d.get("mood")
                else:
                    # character is a dict with id, text, mood, image
                    char_image = char_data.get("image") or char_data.get("image_prompt")
                    # Support both 'voice' (path) and 'voice_url' fields
                    char_voice = char_data.get("voice") or char_data.get("voice_url")
                    speaker = char_data.get("id", "")
                    text = char_data.get("text", d.get("text", ""))
                    mood = char_data.get("mood", d.get("mood"))
                dialogues.append(
                    DialogueLine(
                        speaker=speaker,
                        text=text,
                        mood=mood,
                        voice_url=char_voice,
                        character_image_url=char_image,
                    )
                )

        choices = []
        for c in data.get("choice", []):
            choices.append(Choice(text=c["text"], next_scene_id=c["next"]))

        return SceneData(
            id=data.get("id", scene_id),
            title=data.get("title", ""),
            background=data.get("background"),
            music=data.get("music"),
            dialogues=dialogues,
            choices=choices,
            is_ending=data.get("is_ending", False),
            next_scene_id=data.get("next"),
        )

    async def list_stories(self) -> list[StoryMetadata]:
        stories = []
        for story_dir in self.stories_dir.iterdir():
            if not story_dir.is_dir():
                continue
            meta_path = story_dir / "meta.yaml"
            if meta_path.exists():
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = yaml.safe_load(f)
                stories.append(
                    StoryMetadata(
                        id=story_dir.name,
                        title=meta.get("title", story_dir.name),
                        author=meta.get("author", "Unknown"),
                        description=meta.get("description", ""),
                        version=meta.get("version", "1.0"),
                    )
                )
        return stories

    async def get_characters(self, story_id: str) -> dict[str, Character]:
        story_path = self.stories_dir / story_id
        chars_path = story_path / "assets" / "characters.yaml"

        if not chars_path.exists():
            return {}

        with open(chars_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        characters = {}
        for char_id, char_data in data.items():
            characters[char_id] = Character(
                id=char_id,
                name=char_data.get("name", char_id),
                default_mood=char_data.get("default_mood", "neutral"),
                description=char_data.get("description", ""),
            )
        return characters

    async def get_story_start_scene(self, story_id: str) -> str:
        story_path = self.stories_dir / story_id
        start_path = story_path / "start.txt"

        if start_path.exists():
            with open(start_path, "r", encoding="utf-8") as f:
                return f.read().strip()

        return "intro"
