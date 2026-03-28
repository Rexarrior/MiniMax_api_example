"""Web server for visual novel with polling support."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

try:
    from bottle import Bottle, static_file, request, response
    HAS_BOTTLE = True
except ImportError:
    HAS_BOTTLE = False

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "examples_python"))

from minimax_http import out_dir


class NovelWebServer:
    def __init__(self, story_path: Path, port: int = 8080):
        self.story_path = story_path
        self.port = port
        self._scene_id: str = ""
        self._title: str = ""
        self._choices: list[dict] = []
        self._is_ending: bool = False
        self._background_url: str | None = None
        self._music_url: str | None = None
        self._dialogues: list[dict] = []
        self._last_update: float = 0
        self._current_character_image_url: str | None = None
        self._app = Bottle()
        self._pending_choice: int | None = None
        self._pending_choice_time: float = 0
        self._setup_routes()

    def _setup_routes(self) -> None:
        self._app.route("/")(self._handle_index)
        self._app.route("/api/scene")(self._handle_scene)
        self._app.route("/api/choice", method="POST")(self._handle_choice)
        self._app.route("/api/poll")(self._handle_poll)
        self._app.route("/api/image/<filepath:path>")(self._handle_image)
        self._app.route("/api/audio/voices/<filepath:path>")(self._handle_voice)
        self._app.route("/<filename>")(self._serve_static)

    def _get_web_root(self) -> Path:
        return Path(__file__).parent.parent / "web_ui"

    def _get_assets_dir(self) -> Path:
        return self.story_path / "assets"

    def _serve_static(self, filename: str) -> static_file:
        if filename == "" or filename == "index.html":
            return static_file("index.html", root=str(self._get_web_root()))
        path = self._get_web_root() / filename
        if path.exists():
            return static_file(str(path), root=str(self._get_web_root()))
        return static_file(str(path), root=str(self._get_web_root()))

    def _handle_index(self) -> static_file:
        return static_file("index.html", root=str(self._get_web_root()))

    def _handle_scene(self) -> dict[str, Any]:
        response.content_type = "application/json"
        return {
            "scene_id": self._scene_id,
            "title": self._title,
            "background_url": self._background_url,
            "dialogues": self._dialogues,
            "choices": self._choices,
            "is_ending": self._is_ending,
            "music_url": self._music_url,
            "timestamp": self._last_update,
            "current_character_image_url": self._current_character_image_url,
        }

    def _handle_poll(self) -> dict[str, Any]:
        response.content_type = "application/json"
        return {
            "scene_id": self._scene_id,
            "background_url": self._background_url,
            "dialogues": self._dialogues,
            "choices": self._choices,
            "is_ending": self._is_ending,
            "music_url": self._music_url,
            "timestamp": self._last_update,
            "current_character_image_url": self._current_character_image_url,
        }

    def _handle_choice(self) -> dict[str, Any]:
        data = request.json or {}
        choice_idx = data.get("choice_index")
        if choice_idx is None:
            response.status = 400
            return {"error": "Missing choice_index"}
        self._pending_choice = choice_idx
        self._pending_choice_time = time.time()
        response.content_type = "application/json"
        return {"status": "ok", "choice_index": choice_idx}

    def _handle_image(self, filepath: str) -> static_file:
        img_path = self._get_assets_dir() / filepath
        if not img_path.exists():
            response.status = 404
            response.content_type = "application/json"
            return {"error": f"Image not found: {filepath}"}
        return static_file(filepath, root=str(self._get_assets_dir()))

    def _handle_voice(self, filepath: str) -> static_file:
        voice_path = self._get_assets_dir() / "voices" / filepath
        if not voice_path.exists():
            response.status = 404
            response.content_type = "application/json"
            return {"error": f"Voice not found: {filepath}"}
        return static_file(filepath, root=str(self._get_assets_dir() / "voices"))

    def update_scene(
        self,
        scene_id: str,
        title: str = "",
        dialogues: list[dict] = None,
        choices: list[dict] = None,
        is_ending: bool = False,
        background_url: str | None = None,
        music_url: str | None = None,
        current_character_image_url: str | None = None,
    ) -> None:
        self._scene_id = scene_id
        self._title = title
        self._dialogues = dialogues or []
        self._choices = choices or []
        self._is_ending = is_ending
        self._background_url = background_url
        self._music_url = music_url
        self._current_character_image_url = current_character_image_url
        self._last_update = time.time()

    def update_character_image(self, character_image_url: str | None) -> None:
        self._current_character_image_url = character_image_url
        self._last_update = time.time()

    def get_pending_choice(self) -> tuple[int | None, float]:
        choice = self._pending_choice
        t = self._pending_choice_time
        self._pending_choice = None
        self._pending_choice_time = 0
        return choice, t

    def run(self) -> None:
        import os
        os.chdir(str(self._get_web_root()))
        self._app.run(host="0.0.0.0", port=self.port, quiet=True)
