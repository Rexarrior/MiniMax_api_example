"""Tests for story loader."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from story import Story


def test_story_loads_demo():
    story_path = Path(__file__).parent.parent / "stories" / "demo"
    story = Story(story_path)

    assert story.title == "The Mysterious Forest"
    assert story.story_id == "demo"
    assert story.meta["author"] == "MiniMax Demo"
    assert story.meta["version"] == "1.0"


def test_story_characters():
    story_path = Path(__file__).parent.parent / "stories" / "demo"
    story = Story(story_path)

    assert "hermit" in story.characters
    assert story.characters["hermit"]["name"] == "Old Hermit"
    assert story.characters["hermit"]["default_mood"] == "neutral"


def test_story_music_cues():
    story_path = Path(__file__).parent.parent / "stories" / "demo"
    story = Story(story_path)

    assert "forest_ambient" in story.music_cues
    assert "prompt" in story.music_cues["forest_ambient"]


def test_story_get_start_scene():
    story_path = Path(__file__).parent.parent / "stories" / "demo"
    story = Story(story_path)

    start = story.get_start_scene()
    assert start == "intro"


def test_story_get_scene_path():
    story_path = Path(__file__).parent.parent / "stories" / "demo"
    story = Story(story_path)

    intro_path = story.get_scene_path("intro")
    assert intro_path is not None
    assert intro_path.name == "intro.scn"

    missing_path = story.get_scene_path("nonexistent")
    assert missing_path is None


def test_story_scene_index():
    story_path = Path(__file__).parent.parent / "stories" / "demo"
    story = Story(story_path)

    intro_path = story.get_scene_path("intro")
    forest_path = story.get_scene_path("forest_path")
    ending_magic = story.get_scene_path("ending_magic")

    assert intro_path is not None
    assert forest_path is not None
    assert ending_magic is not None
