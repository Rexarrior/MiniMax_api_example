"""Story loader for visual novel."""

from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any


class Story:
    def __init__(self, story_dir: Path):
        self.dir = story_dir
        self.meta = self._load_meta()
        self.characters = self._load_characters()
        self.music_cues = self._load_music()
        self._scenes: dict[str, Path] = {}
        self._load_scene_index()

    def _load_meta(self) -> dict[str, Any]:
        meta_path = self.dir / "meta.yaml"
        if meta_path.exists():
            return yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        return {}

    def _load_characters(self) -> dict[str, Any]:
        chars_path = self.dir / "assets" / "characters.yaml"
        if chars_path.exists():
            return yaml.safe_load(chars_path.read_text(encoding="utf-8")) or {}
        return {}

    def _load_music(self) -> dict[str, Any]:
        music_path = self.dir / "assets" / "music.yaml"
        if music_path.exists():
            return yaml.safe_load(music_path.read_text(encoding="utf-8")) or {}
        return {}

    def _load_scene_index(self) -> None:
        scenes_dir = self.dir / "scenes"
        if scenes_dir.exists():
            for f in scenes_dir.glob("*.scn"):
                scene_id = f.stem
                self._scenes[scene_id] = f

    def get_scene_path(self, scene_id: str) -> Path | None:
        return self._scenes.get(scene_id)

    def get_start_scene(self) -> str | None:
        start_file = self.dir / "start.txt"
        if start_file.exists():
            return start_file.read_text(encoding="utf-8").strip()
        return None

    @property
    def title(self) -> str:
        return self.meta.get("title", "Untitled Story")

    @property
    def story_id(self) -> str:
        return self.dir.name
