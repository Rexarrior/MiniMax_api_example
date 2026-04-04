"""Stateless FastAPI server for visual novel - no threads, no polling."""

from __future__ import annotations

import logging
import os
import threading
import time
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger(__name__)

app = FastAPI(title="Visual Novel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STORIES_DIR = Path(os.environ.get("STORIES_DIR", "/app/stories"))

from engine.scene_service import SceneService

scene_service: SceneService | None = None


def get_scene_service() -> SceneService:
    global scene_service
    if scene_service is None:
        scene_service = SceneService.get_instance(STORIES_DIR)
    return scene_service


class GameSession:
    def __init__(self):
        self.story_id: str | None = None
        self.current_scene_id: str = ""
        self.scene_title: str = ""
        self.dialogues: list[dict] = []
        self.choices: list[dict] = []
        self.is_ending: bool = False
        self.background_url: str | None = None
        self.music_url: str | None = None
        self.current_character_image_url: str | None = None
        self.last_update: float = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.current_scene_id,
            "title": self.scene_title,
            "background_url": self.background_url,
            "dialogues": self.dialogues,
            "choices": self.choices,
            "is_ending": self.is_ending,
            "music_url": self.music_url,
            "timestamp": self.last_update,
            "current_character_image_url": self.current_character_image_url,
            "story_id": self.story_id,
        }


sessions: dict[str, GameSession] = {}
sessions_lock = threading.Lock()

DEFAULT_SESSION_ID = "default"


def get_session(session_id: str | None = None) -> GameSession:
    sid = session_id or DEFAULT_SESSION_ID
    with sessions_lock:
        if sid not in sessions:
            sessions[sid] = GameSession()
        return sessions[sid]


def build_scene_response(
    story_id: str, scene, scene_service: SceneService
) -> dict[str, Any]:
    """Build API response from a Scene object."""
    bg_url = None
    if scene.background_prompt:
        img_path = (
            scene_service.stories_dir
            / story_id
            / "assets"
            / "images"
            / f"bg_{scene.background_prompt[:50]}.jpg"
        )
        if not img_path.exists():
            img_path = scene_service.stories_dir / story_id / "assets" / "images"
            for f in img_path.glob(
                f"bg_{scene.background_prompt[:30].replace(' ', '_')}*"
            ):
                if f.suffix in (".jpg", ".jpeg", ".png"):
                    img_path = f
                    break
        if img_path.exists():
            rel_path = img_path.relative_to(
                scene_service.stories_dir / story_id / "assets"
            )
            bg_url = f"/stories/{story_id}/assets/{rel_path}"

    music_url = None
    if scene.music:
        music_path = (
            scene_service.stories_dir / story_id / "assets" / "music" / scene.music
        )
        if music_path.exists():
            music_url = f"/stories/{story_id}/assets/music/{scene.music}"

    dialogues = []
    for d in scene.dialogues:
        dialogues.append(
            {
                "speaker": d.speaker,
                "text": d.text,
                "mood": d.mood,
                "voice_url": None,
                "voice_duration_ms": 0,
                "character_image_url": None,
            }
        )

    choices = []
    for i, c in enumerate(scene.choices):
        choices.append({"index": i, "text": c.text})

    is_ending = len(scene.choices) == 0

    return {
        "scene_id": scene.id,
        "title": scene.title,
        "background_url": bg_url,
        "dialogues": dialogues,
        "choices": choices,
        "is_ending": is_ending,
        "music_url": music_url,
        "timestamp": time.time(),
        "current_character_image_url": None,
        "story_id": story_id,
    }


@app.on_event("startup")
async def startup():
    get_scene_service()
    logger.info("Scene service loaded")


@app.get("/api/stories")
def list_stories():
    return get_scene_service().get_stories()


class StartGameRequest(BaseModel):
    story_id: str


@app.post("/api/game/start")
def start_game(
    req: StartGameRequest,
    x_session_id: str | None = Header(default=None, alias="X-Session-ID"),
    session_id: str | None = None,
):
    service = get_scene_service()
    story_path = STORIES_DIR / req.story_id

    if not story_path.exists():
        raise HTTPException(status_code=404, detail=f"Story '{req.story_id}' not found")
    if not (story_path / "start.txt").exists():
        raise HTTPException(
            status_code=400, detail=f"Story '{req.story_id}' has no start.txt"
        )

    start_scene_id = service.get_start_scene_id(req.story_id)
    if not start_scene_id:
        raise HTTPException(
            status_code=400, detail=f"No start scene for '{req.story_id}'"
        )

    scene = service.get_scene(req.story_id, start_scene_id)
    if not scene:
        raise HTTPException(
            status_code=404, detail=f"Scene '{start_scene_id}' not found"
        )

    sid = session_id or x_session_id or DEFAULT_SESSION_ID
    gs = get_session(sid)

    response_data = build_scene_response(req.story_id, scene, service)

    gs.story_id = req.story_id
    gs.current_scene_id = scene.id
    gs.scene_title = scene.title
    gs.dialogues = response_data["dialogues"]
    gs.choices = response_data["choices"]
    gs.is_ending = response_data["is_ending"]
    gs.background_url = response_data["background_url"]
    gs.music_url = response_data["music_url"]
    gs.current_character_image_url = response_data["current_character_image_url"]
    gs.last_update = time.time()

    logger.info(f"Started game {req.story_id} session {sid}, scene {scene.id}")

    return {**response_data, "status": "ok", "session_id": sid}


class ChoiceRequest(BaseModel):
    choice_index: int


@app.post("/api/choice")
def make_choice(
    req: ChoiceRequest,
    x_session_id: str | None = Header(default=None, alias="X-Session-ID"),
    session_id: str | None = None,
):
    sid = session_id or x_session_id or DEFAULT_SESSION_ID
    gs = get_session(sid)

    if gs.story_id is None:
        raise HTTPException(status_code=400, detail="No game in progress")

    service = get_scene_service()
    current_scene = service.get_scene(gs.story_id, gs.current_scene_id)
    if not current_scene:
        raise HTTPException(status_code=404, detail="Current scene not found")

    if req.choice_index < 0 or req.choice_index >= len(current_scene.choices):
        raise HTTPException(status_code=400, detail="Invalid choice index")

    next_scene_id = current_scene.choices[req.choice_index].next_scene
    next_scene = service.get_scene(gs.story_id, next_scene_id)
    if not next_scene:
        raise HTTPException(
            status_code=404, detail=f"Next scene '{next_scene_id}' not found"
        )

    response_data = build_scene_response(gs.story_id, next_scene, service)

    gs.current_scene_id = next_scene.id
    gs.scene_title = next_scene.title
    gs.dialogues = response_data["dialogues"]
    gs.choices = response_data["choices"]
    gs.is_ending = response_data["is_ending"]
    gs.background_url = response_data["background_url"]
    gs.music_url = response_data["music_url"]
    gs.current_character_image_url = response_data["current_character_image_url"]
    gs.last_update = time.time()

    logger.info(f"Choice {req.choice_index} -> scene {next_scene.id}")

    return response_data


@app.get("/api/scene")
def get_scene(
    x_session_id: str | None = Header(default=None, alias="X-Session-ID"),
    session_id: str | None = None,
):
    sid = session_id or x_session_id or DEFAULT_SESSION_ID
    gs = get_session(sid)
    return gs.to_dict()


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=5000)
