#!/usr/bin/env python3
"""Generate all assets for a story (images, music, and voices)."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "examples_python"))
sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from story import Story
from scene import parse_scene
from minimax_client import MiniMaxClient


def generate_story_assets(story_path: Path, force: bool = False) -> None:
    story = Story(story_path)
    mm_client = MiniMaxClient()

    print(f"Generating assets for story: {story.title}")
    print(f"Story ID: {story.story_id}")

    scenes_dir = story_path / "scenes"
    generated_count = 0
    skipped_count = 0

    for scene_file in scenes_dir.glob("*.scn"):
        scene_id = scene_file.stem
        content = scene_file.read_text(encoding="utf-8")
        scene = parse_scene(scene_id, content)

        if scene.background_prompt:
            img_path = mm_client.generate_background_image(
                story.story_id, scene_id, scene.background_prompt
            )
            if img_path:
                print(f"  [IMAGE] {scene_id}: {img_path.name}")
                generated_count += 1
            else:
                print(f"  [IMAGE] {scene_id}: FAILED")

        for d in scene.dialogues:
            if d.speaker == "narrator":
                voice_result = mm_client.generate_voice(
                    story.story_id,
                    "narrator",
                    d.text,
                    voice_id="English_Graceful_Lady",
                    speed=1.0,
                    pitch=0,
                )
            else:
                char_data = story.characters.get(d.speaker, {})
                voice_result = mm_client.generate_voice(
                    story.story_id,
                    d.speaker,
                    d.text,
                    voice_id=char_data.get("voice_id", "English_Insightful_Speaker"),
                    speed=char_data.get("speed", 1.0),
                    pitch=char_data.get("pitch", 0),
                )
                if d.image_prompt and char_data.get("appearance_prompt"):
                    img_parts = [char_data["appearance_prompt"]]
                    if scene.background_prompt:
                        img_parts.append(scene.background_prompt)
                    img_parts.append(d.image_prompt)
                    combined_prompt = ", ".join(img_parts)
                    img_path = mm_client.generate_character_image(
                        story.story_id, scene_id, d.speaker, combined_prompt, d.mood
                    )
                    if img_path:
                        print(
                            f"  [DIALOG_IMAGE] {scene_id}/{d.speaker}: {img_path.name}"
                        )
                        generated_count += 1
            if voice_result:
                print(f"  [VOICE] {scene_id}/{d.speaker}: {voice_result['path'].name}")
                generated_count += 1
            else:
                print(f"  [VOICE] {scene_id}/{d.speaker}: FAILED")

        if scene.generate_music:
            music_path = mm_client.generate_music(story.story_id, scene.generate_music)
            if music_path:
                print(f"  [MUSIC] {scene_id}: {music_path.name}")
                generated_count += 1
            else:
                print(f"  [MUSIC] {scene_id}: FAILED")

        if scene.is_video and scene.video_prompt:
            video_path = mm_client.generate_video(
                story.story_id, scene_id, scene.video_prompt, scene.video_duration
            )
            if video_path:
                print(f"  [VIDEO] {scene_id}: {video_path.name}")
                generated_count += 1
            else:
                print(f"  [VIDEO] {scene_id}: FAILED")

        if (
            not scene.background_prompt
            and not scene.generate_music
            and not scene.dialogues
            and not scene.is_video
        ):
            skipped_count += 1

    print(f"\nDone! Generated: {generated_count}, Skipped (no assets): {skipped_count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate visual novel assets")
    parser.add_argument(
        "story_path",
        nargs="?",
        default=None,
        help="Path to story directory (default: stories/demo)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even if cached",
    )
    args = parser.parse_args()

    if args.story_path:
        story_path = Path(args.story_path)
    else:
        script_dir = Path(__file__).parent.parent
        story_path = script_dir / "stories" / "demo"

    if not story_path.exists():
        print(f"Error: Story path does not exist: {story_path}")
        sys.exit(1)

    generate_story_assets(story_path, args.force)


if __name__ == "__main__":
    main()
