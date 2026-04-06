from fastapi import APIRouter, Depends, HTTPException
from app.services.game_service import GameService
from app.schemas.story import StoryListResponse, StoryMetadata
from app.api.deps import get_game_service

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("", response_model=StoryListResponse)
async def list_stories(service: GameService = Depends(get_game_service)):
    stories = await service.list_stories()
    return StoryListResponse(
        stories=[
            StoryMetadata(
                id=s.id,
                title=s.title,
                author=s.author,
                description=s.description,
                version=s.version,
            )
            for s in stories
        ]
    )


@router.get("/{story_id}")
async def get_story(story_id: str, service: GameService = Depends(get_game_service)):
    stories = await service.list_stories()
    for s in stories:
        if s.id == story_id:
            return StoryMetadata(
                id=s.id,
                title=s.title,
                author=s.author,
                description=s.description,
                version=s.version,
            )
    raise HTTPException(status_code=404, detail="Story not found")
