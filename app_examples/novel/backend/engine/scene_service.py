"""Stateless scene service - loads scenes at startup, no threads."""

from __future__ import annotations

import logging
import os
import threading
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class DialogueLine:
    def __init__(self, speaker: str, text: str, mood: str | None = None):
        self.speaker = speaker
        self.text = text
        self.mood = mood


class Choice:
    def __init__(self, text: str, next_scene: str):
        self.text = text
        self.next_scene = next_scene


class Scene:
    def __init__(
        self,
        id: str,
        title: str,
        background: str | None = None,
        background_prompt: str | None = None,
        dialogues: list[DialogueLine] | None = None,
        choices: list[Choice] | None = None,
        music: str | None = None,
    ):
        self.id = id
        self.title = title
        self.background = background
        self.background_prompt = background_prompt
        self.dialogues = dialogues or []
        self.choices = choices or []
        self.music = music


def parse_scene_content(scene_id: str, content: str) -> Scene:
    try:
        data = yaml.safe_load(content) or {}
    except yaml.YAMLError as e:
        logger.error(f"Failed to parse YAML for scene {scene_id}: {e}")
        data = {}

    dialogues = []
    for d in data.get("dialogue", []):
        if "character" in d:
            speaker = d["character"]
            text = d.get("text", "")
            mood = d.get("mood")
        elif "narrator" in d:
            speaker = "narrator"
            text = d.get("narrator", "") or ""
            mood = None
        else:
            continue
        dialogues.append(DialogueLine(speaker=speaker, text=text, mood=mood))

    choices = []
    for c in data.get("choice", []):
        choices.append(Choice(text=c.get("text", ""), next_scene=c.get("next", "")))

    return Scene(
        id=scene_id,
        title=data.get("title", scene_id),
        background=data.get("background"),
        background_prompt=data.get("background_prompt"),
        dialogues=dialogues,
        choices=choices,
        music=data.get("music"),
    )


class SceneService:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, stories_dir: Path):
        self.stories_dir = stories_dir
        self.scenes: dict[str, dict[str, Scene]] = {}
        self._lock = threading.Lock()
        self._load_all_scenes()

    @classmethod
    def get_instance(cls, stories_dir: Path | None = None) -> "SceneService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    if stories_dir is None:
                        stories_dir = Path(
                            os.environ.get("STORIES_DIR", "/app/stories")
                        )
                    cls._instance = cls(stories_dir)
        return cls._instance

    def _load_all_scenes(self):
        """Load all scenes from all stories into memory."""
        if not self.stories_dir.exists():
            logger.warning(f"Stories dir does not exist: {self.stories_dir}")
            return

        for story_path in self.stories_dir.iterdir():
            if not story_path.is_dir():
                continue
            story_id = story_path.name
            self.scenes[story_id] = {}
            scenes_dir = story_path / "scenes"
            if not scenes_dir.exists():
                continue

            for scene_file in scenes_dir.glob("*.scn"):
                scene_id = scene_file.stem
                try:
                    content = scene_file.read_text(encoding="utf-8")
                    scene = parse_scene_content(scene_id, content)
                    self.scenes[story_id][scene_id] = scene
                    logger.info(f"Loaded scene {story_id}/{scene_id}")
                except Exception as e:
                    logger.error(f"Failed to load scene {story_id}/{scene_id}: {e}")

        logger.info(f"Loaded {len(self.scenes)} stories")

    def get_scene(self, story_id: str, scene_id: str) -> Scene | None:
        """Get a scene by story_id and scene_id."""
        return self.scenes.get(story_id, {}).get(scene_id)

    def get_start_scene_id(self, story_id: str) -> str | None:
        """Get the start scene ID for a story."""
        start_file = self.stories_dir / story_id / "start.txt"
        if start_file.exists():
            return start_file.read_text(encoding="utf-8").strip()
        return None

    def get_characters(self, story_id: str) -> dict[str, Any]:
        """Load characters for a story."""
        chars_file = self.stories_dir / story_id / "assets" / "characters.yaml"
        if chars_file.exists():
            try:
                return yaml.safe_load(chars_file.read_text(encoding="utf-8")) or {}
            except Exception as e:
                logger.error(f"Failed to load characters for {story_id}: {e}")
        return {}

    def get_stories(self) -> list[dict[str, Any]]:
        """Get list of all stories."""
        stories = []
        for story_path in self.stories_dir.iterdir():
            if not story_path.is_dir():
                continue
            meta_path = story_path / "meta.yaml"
            start_path = story_path / "start.txt"
            if not start_path.exists():
                continue
            meta = {}
            if meta_path.exists():
                try:
                    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
                except Exception:
                    pass
            stories.append(
                {
                    "id": story_path.name,
                    "title": meta.get("title", story_path.name),
                    "description": meta.get("description", ""),
                }
            )
        return stories
