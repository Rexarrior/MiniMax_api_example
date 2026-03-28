#!/usr/bin/env python3
"""Generate all assets for a story (images and music)."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "examples_python"))
sys.path.insert(0, str(Path(__file__).parent.parent / "engine"))

from story import Story
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

        import yaml
        data = yaml.safe_load(content) or {}

        generate_image = data.get("generate_image")
        generate_music = data.get("generate_music")

        if generate_image:
            img_path = mm_client.generate_image(story.story_id, generate_image)
            if img_path:
                print(f"  [IMAGE] {scene_id}: {img_path.name}")
                generated_count += 1
            else:
                print(f"  [IMAGE] {scene_id}: FAILED")

        if generate_music:
            music_path = mm_client.generate_music(story.story_id, generate_music)
            if music_path:
                print(f"  [MUSIC] {scene_id}: {music_path.name}")
                generated_count += 1
            else:
                print(f"  [MUSIC] {scene_id}: FAILED")

        if not generate_image and not generate_music:
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
