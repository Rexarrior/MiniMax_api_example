from fastapi import APIRouter, Depends, HTTPException, Header
from app.services.game_service import GameService
from app.schemas.session import SessionCreate, SessionResponse
from app.schemas.scene import SceneResponse, ChoiceRequest
from app.core.exceptions import SessionNotFoundError, InvalidChoiceError
from app.api.deps import get_game_service

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/start", response_model=SessionResponse)
async def start_game(
    request: SessionCreate, service: GameService = Depends(get_game_service)
):
    return await service.start_game(request)


@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str, service: GameService = Depends(get_game_service)
):
    try:
        return await service.get_session(session_id)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/scene/{session_id}", response_model=SceneResponse)
async def get_scene(
    session_id: str,
    language: str = "en",
    service: GameService = Depends(get_game_service),
):
    try:
        return await service.get_scene(session_id, language=language)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/choice", response_model=SessionResponse)
async def make_choice(
    request: ChoiceRequest,
    x_session_id: str = Header(...),
    service: GameService = Depends(get_game_service),
):
    try:
        return await service.make_choice(x_session_id, request)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidChoiceError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/advance", response_model=SessionResponse)
async def advance_dialogue(
    x_session_id: str = Header(...), service: GameService = Depends(get_game_service)
):
    try:
        return await service.advance_dialogue(x_session_id)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
