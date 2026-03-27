"""Entry point for visual novel."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "engine"))

from story import Story
from scene import parse_scene
from choices import get_next_scene
from renderer import Renderer
from minimax_client import MiniMaxClient


def main():
    story_path = Path(__file__).parent / "stories" / "demo"
    if len(sys.argv) > 1:
        story_path = Path(sys.argv[1])

    story = Story(story_path)
    renderer = Renderer()
    mm_client = MiniMaxClient()

    renderer.print_title(story.title)

    scene_id = story.get_start_scene()
    if not scene_id:
        renderer.print_message("Error: No start scene defined.")
        return

    while scene_id:
        scene_path = story.get_scene_path(scene_id)
        if not scene_path:
            renderer.print_message(f"Error: Scene '{scene_id}' not found.")
            break

        scene_content = scene_path.read_text(encoding="utf-8")
        scene = parse_scene(scene_id, scene_content)

        if scene.background:
            renderer.print_message(f"Location: {scene.background}")

        if scene.generate_image:
            img_path = mm_client.generate_image(story.story_id, scene.generate_image)
            renderer.print_image(img_path)

        if scene.generate_music:
            music_path = mm_client.generate_music(story.story_id, scene.generate_music)
            renderer.play_music(music_path)

        for dialogue in scene.dialogues:
            if dialogue.speaker == "narrator":
                renderer.print_narrator(dialogue.text)
            else:
                renderer.print_dialogue(
                    story.characters.get(dialogue.speaker, {}).get("name", dialogue.speaker),
                    dialogue.text,
                    dialogue.mood,
                )

        if scene.choices:
            choice_texts = [(i, c.text) for i, c in enumerate(scene.choices)]
            renderer.print_choices(choice_texts)
            choice_idx = renderer.wait_for_choice(len(scene.choices))
            if choice_idx is None:
                renderer.print_message("\nGoodbye!")
                break
            scene_id = get_next_scene(scene, choice_idx)
        elif scene.next_scene:
            scene_id = scene.next_scene
        else:
            renderer.print_ending("The End")
            break

    renderer.stop_music()


if __name__ == "__main__":
    main()
