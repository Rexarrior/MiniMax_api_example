"""Tests for scene parser."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))
sys.path.insert(0, str(Path(__file__).parent.parent / "engine" / ".."))

from scene import parse_scene, Scene, DialogueLine, Choice


def test_parse_scene_basic():
    content = """
id: test_scene
title: "Test Scene"
background: "test location"

dialogue:
  - narrator: "Test narration"
  - character: hermit
    text: "Hello"
    mood: happy

choice:
  - text: "Option 1"
    next: next_scene_1
  - text: "Option 2"
    next: next_scene_2
"""
    scene = parse_scene("test_scene", content)

    assert scene.id == "test_scene"
    assert scene.title == "Test Scene"
    assert scene.background == "test location"
    assert len(scene.dialogues) == 2
    assert scene.dialogues[0].speaker == "narrator"
    assert scene.dialogues[0].text == "Test narration"
    assert scene.dialogues[1].speaker == "hermit"
    assert scene.dialogues[1].text == "Hello"
    assert scene.dialogues[1].mood == "happy"
    assert len(scene.choices) == 2
    assert scene.choices[0].text == "Option 1"
    assert scene.choices[0].next_scene == "next_scene_1"
    assert scene.choices[1].text == "Option 2"
    assert scene.choices[1].next_scene == "next_scene_2"


def test_parse_scene_narrator_only():
    content = """
id: narrator_scene
title: "Narrator Only"

dialogue:
  - narrator: "First line"
  - narrator: "Second line"
"""
    scene = parse_scene("narrator_scene", content)

    assert scene.id == "narrator_scene"
    assert len(scene.dialogues) == 2
    assert all(d.speaker == "narrator" for d in scene.dialogues)


def test_parse_scene_generate_fields():
    content = """
id: media_scene
title: "Media Scene"

generate_image: "a beautiful landscape"
generate_music: "peaceful ambient music"
"""
    scene = parse_scene("media_scene", content)

    assert scene.generate_image == "a beautiful landscape"
    assert scene.generate_music == "peaceful ambient music"


def test_parse_scene_next_scene():
    content = """
id: linear_scene
title: "Linear Scene"
next: following_scene
"""
    scene = parse_scene("linear_scene", content)

    assert scene.next_scene == "following_scene"
    assert len(scene.choices) == 0


def test_parse_scene_empty():
    content = """
id: empty_scene
title: "Empty Scene"
"""
    scene = parse_scene("empty_scene", content)

    assert scene.id == "empty_scene"
    assert scene.title == "Empty Scene"
    assert len(scene.dialogues) == 0
    assert len(scene.choices) == 0
