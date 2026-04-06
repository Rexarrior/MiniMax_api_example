import pytest
from app.core.scene_adapter import SceneAdapter, SceneData, DialogueLine, Choice
from app.core.exceptions import SceneNotFoundError, StoryNotFoundError


class MockSceneAdapter(SceneAdapter):
    """Mock implementation for testing"""

    def __init__(self):
        self.scenes = {
            "demo": {
                "intro": SceneData(
                    id="intro",
                    title="Introduction",
                    background="forest",
                    music="ambient.mp3",
                    dialogues=[
                        DialogueLine(speaker="narrator", text="Welcome", mood=None),
                    ],
                    choices=[
                        Choice(text="Start", next_scene_id="scene1"),
                    ],
                    is_ending=False,
                )
            }
        }

    async def load_scene(self, story_id: str, scene_id: str) -> SceneData:
        if story_id not in self.scenes:
            raise StoryNotFoundError(f"Story not found: {story_id}")
        if scene_id not in self.scenes[story_id]:
            raise SceneNotFoundError(f"Scene not found: {scene_id}")
        return self.scenes[story_id][scene_id]

    async def list_stories(self):
        return []

    async def get_characters(self, story_id: str):
        return {}

    async def get_story_start_scene(self, story_id: str) -> str:
        if story_id not in self.scenes:
            raise StoryNotFoundError(f"Story not found: {story_id}")
        return "intro"


class TestSceneAdapter:
    @pytest.fixture
    def adapter(self):
        return MockSceneAdapter()

    @pytest.mark.asyncio
    async def test_load_scene(self, adapter):
        scene = await adapter.load_scene("demo", "intro")

        assert scene.id == "intro"
        assert scene.title == "Introduction"
        assert len(scene.dialogues) == 1
        assert len(scene.choices) == 1

    @pytest.mark.asyncio
    async def test_load_nonexistent_scene(self, adapter):
        with pytest.raises(SceneNotFoundError):
            await adapter.load_scene("demo", "nonexistent")

    @pytest.mark.asyncio
    async def test_load_scene_nonexistent_story(self, adapter):
        with pytest.raises(StoryNotFoundError):
            await adapter.load_scene("nonexistent", "intro")

    @pytest.mark.asyncio
    async def test_get_story_start_scene(self, adapter):
        start = await adapter.get_story_start_scene("demo")
        assert start == "intro"
