from pydantic import BaseModel


class StoryMetadata(BaseModel):
    id: str
    title: str
    author: str
    description: str
    version: str


class StoryListResponse(BaseModel):
    stories: list[StoryMetadata]
