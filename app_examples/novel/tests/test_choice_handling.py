"""Tests for choice handling."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from scene import Scene, DialogueLine, Choice
from choices import get_next_scene


def test_get_next_scene_from_choice():
    scene = Scene(
        id="test",
        title="Test",
        choices=[
            Choice(text="Option 1", next_scene="scene_1"),
            Choice(text="Option 2", next_scene="scene_2"),
            Choice(text="Option 3", next_scene="scene_3"),
        ],
    )

    assert get_next_scene(scene, 0) == "scene_1"
    assert get_next_scene(scene, 1) == "scene_2"
    assert get_next_scene(scene, 2) == "scene_3"


def test_get_next_scene_invalid_index():
    scene = Scene(
        id="test",
        title="Test",
        choices=[
            Choice(text="Option 1", next_scene="scene_1"),
        ],
    )

    assert get_next_scene(scene, 5) is None
    assert get_next_scene(scene, -1) is None
    assert get_next_scene(scene, None) is None


def test_get_next_scene_no_choices():
    scene = Scene(
        id="test",
        title="Test",
        choices=[],
        next_scene="fallback_scene",
    )

    assert get_next_scene(scene, None) == "fallback_scene"
    assert get_next_scene(scene, 0) is None


def test_get_next_scene_priority():
    scene = Scene(
        id="test",
        title="Test",
        choices=[
            Choice(text="Option 1", next_scene="choice_scene"),
        ],
        next_scene="fallback_scene",
    )

    assert get_next_scene(scene, 0) == "choice_scene"
    assert get_next_scene(scene, None) == "fallback_scene"
