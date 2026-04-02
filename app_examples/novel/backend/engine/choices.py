"""Choice handling for visual novel."""

from __future__ import annotations

from engine.scene import Scene, Choice


def get_next_scene(scene: Scene, choice_index: int | None) -> str | None:
    if choice_index is None:
        return scene.next_scene
    if 0 <= choice_index < len(scene.choices):
        return scene.choices[choice_index].next_scene
    return None
