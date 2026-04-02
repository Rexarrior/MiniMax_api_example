"""FastAPI server for visual novel."""

from __future__ import annotations

import logging
import os
import sys
import threading
import time
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent.parent / "examples_python"))

from minimax_http import out_dir  # noqa: E402

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


class GameState:
    def __init__(self):
        self.story_id: str | None = None
        self.story_path: Path | None = None
        self.scene_id: str = ""
        self.title: str = ""
        self.choices: list[dict] = []
        self.is_ending: bool = False
        self.background_url: str | None = None
        self.music_url: str | None = None
        self.dialogues: list[dict] = []
        self.last_update: float = 0
        self.current_character_image_url: str | None = None
        self._game_thread: threading.Thread | None = None
        self._pending_choice: int | None = None
        self._pending_choice_time: float = 0
        self._lock = threading.Lock()

    def reset(self):
        with self._lock:
            self.story_id = None
            self.story_path = None
            self.scene_id = ""
            self.title = ""
            self.choices = []
            self.is_ending = False
            self.background_url = None
            self.music_url = None
            self.dialogues = []
            self.last_update = 0
            self.current_character_image_url = None
            self._pending_choice = None
            self._pending_choice_time = 0

    def update_scene(
        self,
        scene_id: str,
        title: str = "",
        dialogues: list[dict] | None = None,
        choices: list[dict] | None = None,
        is_ending: bool = False,
        background_url: str | None = None,
        music_url: str | None = None,
        current_character_image_url: str | None = None,
    ):
        with self._lock:
            self.scene_id = scene_id
            self.title = title
            self.dialogues = dialogues or []
            self.choices = choices or []
            self.is_ending = is_ending
            self.background_url = background_url
            self.music_url = music_url
            self.current_character_image_url = current_character_image_url
            self.last_update = time.time()

    def set_pending_choice(self, choice_idx: int):
        with self._lock:
            self._pending_choice = choice_idx
            self._pending_choice_time = time.time()

    def get_pending_choice(self) -> tuple[int | None, float]:
        with self._lock:
            choice = self._pending_choice
            t = self._pending_choice_time
            self._pending_choice = None
            self._pending_choice_time = 0
            return choice, t

    def to_dict(self) -> dict[str, Any]:
        with self._lock:
            return {
                "scene_id": self.scene_id,
                "title": self.title,
                "background_url": self.background_url,
                "dialogues": self.dialogues,
                "choices": self.choices,
                "is_ending": self.is_ending,
                "music_url": self.music_url,
                "timestamp": self.last_update,
                "current_character_image_url": self.current_character_image_url,
                "story_id": self.story_id,
            }


sessions: dict[str, GameState] = {}

DEFAULT_SESSION_ID = "default"


def get_session(session_id: str | None = None) -> GameState:
    sid = session_id or DEFAULT_SESSION_ID
    if sid not in sessions:
        sessions[sid] = GameState()
    return sessions[sid]


def get_stories() -> list[dict[str, Any]]:
    stories = []
    if not STORIES_DIR.exists():
        return stories
    for story_path in STORIES_DIR.iterdir():
        if not story_path.is_dir():
            continue
        meta_path = story_path / "meta.yaml"
        start_path = story_path / "start.txt"
        if not start_path.exists():
            continue
        meta = {}
        if meta_path.exists():
            import yaml

            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        stories.append(
            {
                "id": story_path.name,
                "title": meta.get("title", story_path.name),
                "description": meta.get("description", ""),
            }
        )
    return stories


def game_loop(story_path: Path, session_id: str = DEFAULT_SESSION_ID):
    from engine.story import Story
    from engine.scene import parse_scene
    from engine.choices import get_next_scene
    from engine.minimax_client import MiniMaxClient

    story = Story(story_path)
    mm_client = MiniMaxClient(stories_dir=STORIES_DIR)
    gs = get_session(session_id)

    def build_character_prompt(
        character_id: str, scene, story: Story, mood: str | None = None
    ) -> str | None:
        char_data = story.characters.get(character_id)
        if not char_data:
            return None
        appearance = char_data.get("appearance_prompt", "")
        if not appearance:
            desc = char_data.get("description", "")
            appearance = f"character: {desc}" if desc else None
        if not appearance:
            return None
        parts = [appearance]
        if scene.background_prompt:
            parts.append(scene.background_prompt)
        if mood:
            parts.append(mood)
        return ", ".join(parts)

    scene_id = story.get_start_scene()
    if not scene_id:
        logger.error("No start scene defined")
        gs.update_scene(
            scene_id="",
            title="Error",
            dialogues=[{"speaker": "system", "text": "No start scene defined"}],
        )
        return

    last_character_id = None
    last_music_url = None
    logger.info("Game loop started")

    while scene_id:
        try:
            scene_path = story.get_scene_path(scene_id)
            if not scene_path:
                logger.error(f"Scene not found: {scene_id}")
                break

            scene_content = scene_path.read_text(encoding="utf-8")
            scene = parse_scene(scene_id, scene_content)
            logger.info(f"→ Scene: {scene_id}")

            background_url = None
            if scene.background_prompt:
                img_path = mm_client.generate_background_image(
                    story.story_id,
                    scene_id,
                    scene.background_prompt,
                    skip_generation=True,
                )
                if img_path:
                    rel_path = img_path.relative_to(
                        STORIES_DIR / story.story_id / "assets"
                    )
                    background_url = f"/stories/{story.story_id}/assets/{rel_path}"
                    logger.info(f"  Background: {img_path.name}")

            char_images: dict[str, str] = {}
            for d in scene.dialogues:
                if d.speaker != "narrator":
                    img_key = f"{d.speaker}_{d.mood or ''}"
                    if img_key not in char_images:
                        prompt = build_character_prompt(d.speaker, scene, story, d.mood)
                        if prompt:
                            img_path = mm_client.generate_character_image(
                                story.story_id,
                                scene_id,
                                d.speaker,
                                prompt,
                                d.mood,
                                skip_generation=True,
                            )
                            if img_path:
                                rel_path = img_path.relative_to(
                                    STORIES_DIR / story.story_id / "assets"
                                )
                                char_images[img_key] = (
                                    f"/stories/{story.story_id}/assets/{rel_path}"
                                )
                                logger.info(
                                    f"  Character ready: {img_key} -> {img_path.name}"
                                )

            music_url = None
            if scene.music:
                music_file = story.dir / "assets" / "music" / scene.music
                if music_file.exists():
                    music_url = f"/stories/{story.story_id}/assets/music/{scene.music}"
                    logger.info(f"  Music: {scene.music}")

            logger.info(f"  Processing {len(scene.dialogues)} dialogues")
            voice_data: list[dict | None] = []
            for d in scene.dialogues:
                if d.speaker == "narrator":
                    voice_result = mm_client.generate_voice(
                        story.story_id,
                        "narrator",
                        d.text,
                        voice_id="English_Graceful_Lady",
                        speed=1.0,
                        pitch=0,
                        skip_generation=True,
                    )
                else:
                    char_data = story.characters.get(d.speaker, {})
                    voice_result = mm_client.generate_voice(
                        story.story_id,
                        d.speaker,
                        d.text,
                        voice_id=char_data.get(
                            "voice_id", "English_Insightful_Speaker"
                        ),
                        speed=char_data.get("speed", 1.0),
                        pitch=char_data.get("pitch", 0),
                        skip_generation=True,
                    )
                if voice_result:
                    logger.info(f"  Voice ready: {d.speaker}")
                voice_data.append(voice_result)

            dialogues = []
            current_char_image_url = None
            for i, d in enumerate(scene.dialogues):
                vd = voice_data[i]
                voice_url = (
                    f"/stories/{story.story_id}/assets/voices/{vd['path'].name}"
                    if vd
                    else None
                )
                voice_duration_ms = vd.get("duration_ms", 0) if vd else 0
                if d.speaker == "narrator":
                    char_img_url = (
                        char_images.get(last_character_id)
                        if last_character_id
                        else None
                    )
                    dialogues.append(
                        {
                            "speaker": "narrator",
                            "text": d.text,
                            "character_image_url": char_img_url,
                            "voice_url": voice_url,
                            "voice_duration_ms": voice_duration_ms,
                        }
                    )
                else:
                    name = story.characters.get(d.speaker, {}).get("name", d.speaker)
                    img_key = f"{d.speaker}_{d.mood or ''}"
                    char_img_url = char_images.get(img_key)
                    dialogues.append(
                        {
                            "speaker": name,
                            "text": d.text,
                            "mood": d.mood,
                            "character_image_url": char_img_url,
                            "voice_url": voice_url,
                            "voice_duration_ms": voice_duration_ms,
                        }
                    )
                    current_char_image_url = char_img_url
                    last_character_id = d.speaker

            choices = [
                {"index": i, "text": c.text} for i, c in enumerate(scene.choices)
            ]
            is_ending = len(scene.choices) == 0 and not scene.next_scene

            send_music_url = music_url if music_url != last_music_url else None
            if music_url:
                last_music_url = music_url

            gs.update_scene(
                scene_id=scene_id,
                title=scene.title,
                dialogues=dialogues,
                choices=choices,
                is_ending=is_ending,
                background_url=background_url,
                music_url=send_music_url,
                current_character_image_url=current_char_image_url,
            )
            logger.info(f"  Scene pushed to server (ending={is_ending})")

            if is_ending:
                logger.info("Game ended")
                break

            choice_idx = None
            choice_time = 0
            while choice_idx is None:
                choice_idx, choice_time = gs.get_pending_choice()
                if choice_idx is None:
                    time.sleep(0.1)

            logger.info(f"  Choice: {choice_idx}")
            scene_id = get_next_scene(scene, choice_idx)

        except Exception as e:
            logger.exception(f"Error in scene {scene_id}: {e}")
            break


@app.get("/api/stories")
def list_stories():
    return get_stories()


class StartGameRequest(BaseModel):
    story_id: str


@app.post("/api/game/start")
def start_game(
    req: StartGameRequest,
    x_session_id: str | None = Header(default=None, alias="X-Session-ID"),
    session_id: str | None = None,
):
    story_path = STORIES_DIR / req.story_id
    if not story_path.exists():
        raise HTTPException(status_code=404, detail=f"Story '{req.story_id}' not found")
    if not (story_path / "start.txt").exists():
        raise HTTPException(
            status_code=400, detail=f"Story '{req.story_id}' has no start.txt"
        )

    sid = session_id or x_session_id or DEFAULT_SESSION_ID
    gs = get_session(sid)
    gs.reset()
    gs.story_id = req.story_id
    gs.story_path = story_path

    thread = threading.Thread(target=game_loop, args=(story_path, sid), daemon=True)
    thread.start()
    gs._game_thread = thread

    return {"status": "ok", "story_id": req.story_id, "session_id": sid}


@app.get("/api/scene")
def get_scene(
    x_session_id: str | None = Header(default=None, alias="X-Session-ID"),
    session_id: str | None = None,
):
    sid = session_id or x_session_id or DEFAULT_SESSION_ID
    return get_session(sid).to_dict()


@app.get("/api/poll")
def poll(
    x_session_id: str | None = Header(default=None, alias="X-Session-ID"),
    session_id: str | None = None,
):
    sid = session_id or x_session_id or DEFAULT_SESSION_ID
    return get_session(sid).to_dict()


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
    gs.set_pending_choice(req.choice_index)
    return {"status": "ok", "choice_index": req.choice_index}


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=5000)
