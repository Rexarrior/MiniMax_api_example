"""Entry point for visual novel - supports terminal and web modes."""

import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "engine"))

from story import Story
from scene import parse_scene, Scene
from choices import get_next_scene
from renderer import Renderer
from minimax_client import MiniMaxClient


def run_terminal(story_path: Path) -> None:
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


def generate_all_assets(story_path: Path) -> None:
    from web_server import NovelWebServer

    story = Story(story_path)
    mm_client = MiniMaxClient()

    def build_character_prompt(character_id: str, scene: Scene, story: Story) -> str | None:
        char_data = story.characters.get(character_id)
        if not char_data:
            return None
        appearance = char_data.get("appearance_prompt", "")
        if not appearance:
            desc = char_data.get("description", "")
            appearance = f"character: {desc}" if desc else None
        if not appearance:
            return None
        bg_prompt = scene.background_prompt or scene.title or ""
        if bg_prompt:
            return f"{appearance}, {bg_prompt}"
        return appearance

    print("Generating assets...")
    scenes_visited = set()
    scene_queue = [story.get_start_scene()]

    while scene_queue:
        scene_id = scene_queue.pop(0)
        if not scene_id or scene_id in scenes_visited:
            continue
        scenes_visited.add(scene_id)

        scene_path = story.get_scene_path(scene_id)
        if not scene_path:
            continue

        scene_content = scene_path.read_text(encoding="utf-8")
        scene = parse_scene(scene_id, scene_content)

        if scene.background_prompt:
            print(f"  Generating background for {scene_id}...")
            mm_client.generate_background_image(story.story_id, scene_id, scene.background_prompt)

        for d in scene.dialogues:
            if d.speaker != "narrator":
                prompt = build_character_prompt(d.speaker, scene, story)
                if prompt:
                    print(f"  Generating character {d.speaker} for {scene_id}...")
                    mm_client.generate_character_image(story.story_id, scene_id, d.speaker, prompt)

        if scene.generate_music:
            print(f"  Generating music for {scene_id}...")
            mm_client.generate_music(story.story_id, scene.generate_music)

        for d in scene.dialogues:
            if d.speaker == "narrator":
                print(f"  Generating voice for narrator in {scene_id}...")
                mm_client.generate_voice(
                    story.story_id, "narrator", d.text,
                    voice_id="English_Graceful_Lady", speed=1.0, pitch=0
                )
            else:
                char_data = story.characters.get(d.speaker, {})
                print(f"  Generating voice for {d.speaker} in {scene_id}...")
                mm_client.generate_voice(
                    story.story_id, d.speaker, d.text,
                    voice_id=char_data.get("voice_id", "English_Insightful_Speaker"),
                    speed=char_data.get("speed", 1.0),
                    pitch=char_data.get("pitch", 0)
                )

        for c in scene.choices:
            if c.next_scene and c.next_scene not in scenes_visited:
                scene_queue.append(c.next_scene)
        if scene.next_scene and scene.next_scene not in scenes_visited:
            scene_queue.append(scene.next_scene)

    print("Asset generation complete!")


def run_web(story_path: Path, port: int = 8080) -> None:
    from web_server import NovelWebServer

    story = Story(story_path)
    mm_client = MiniMaxClient()
    server = NovelWebServer(story_path, port)

    def build_character_prompt(character_id: str, scene: Scene, story: Story) -> str | None:
        char_data = story.characters.get(character_id)
        if not char_data:
            return None
        appearance = char_data.get("appearance_prompt", "")
        if not appearance:
            desc = char_data.get("description", "")
            appearance = f"character: {desc}" if desc else None
        if not appearance:
            return None
        bg_prompt = scene.background_prompt or scene.title or ""
        if bg_prompt:
            return f"{appearance}, {bg_prompt}"
        return appearance

    def game_loop():
        scene_id = story.get_start_scene()
        if not scene_id:
            return

        last_character_id = None
        last_music_url = None

        while scene_id:
            scene_path = story.get_scene_path(scene_id)
            if not scene_path:
                break

            scene_content = scene_path.read_text(encoding="utf-8")
            scene = parse_scene(scene_id, scene_content)

            background_url = None
            if scene.background_prompt:
                img_path = mm_client.generate_background_image(story.story_id, scene_id, scene.background_prompt)
                if img_path:
                    background_url = f"/api/image/images/{img_path.name}"

            char_images: dict[str, str] = {}
            for d in scene.dialogues:
                if d.speaker != "narrator" and d.speaker not in char_images:
                    prompt = build_character_prompt(d.speaker, scene, story)
                    if prompt:
                        img_path = mm_client.generate_character_image(story.story_id, scene_id, d.speaker, prompt)
                        if img_path:
                            char_images[d.speaker] = f"/api/image/images/{img_path.name}"

            music_url = None
            if scene.music:
                music_url = f"/api/image/music/{scene.music}"
            elif scene.generate_music:
                music_path = mm_client.generate_music(story.story_id, scene.generate_music)
                if music_path:
                    music_url = f"/api/image/music/{music_path.name}"

            voice_data: list[dict | None] = []
            for d in scene.dialogues:
                if d.speaker == "narrator":
                    voice_result = mm_client.generate_voice(
                        story.story_id, "narrator", d.text,
                        voice_id="English_Graceful_Lady", speed=1.0, pitch=0
                    )
                else:
                    char_data = story.characters.get(d.speaker, {})
                    voice_result = mm_client.generate_voice(
                        story.story_id, d.speaker, d.text,
                        voice_id=char_data.get("voice_id", "English_Insightful_Speaker"),
                        speed=char_data.get("speed", 1.0),
                        pitch=char_data.get("pitch", 0)
                    )
                voice_data.append(voice_result)

            dialogues = []
            current_char_image_url = None
            for i, d in enumerate(scene.dialogues):
                vd = voice_data[i]
                voice_url = f"/api/audio/voices/{vd['path'].name}" if vd else None
                voice_duration_ms = vd.get("duration_ms", 0) if vd else 0
                if d.speaker == "narrator":
                    char_img_url = char_images.get(last_character_id) if last_character_id else None
                    dialogues.append({
                        "speaker": "narrator",
                        "text": d.text,
                        "character_image_url": char_img_url,
                        "voice_url": voice_url,
                        "voice_duration_ms": voice_duration_ms,
                    })
                else:
                    name = story.characters.get(d.speaker, {}).get("name", d.speaker)
                    char_img_url = char_images.get(d.speaker)
                    dialogues.append({
                        "speaker": name,
                        "text": d.text,
                        "mood": d.mood,
                        "character_image_url": char_img_url,
                        "voice_url": voice_url,
                        "voice_duration_ms": voice_duration_ms,
                    })
                    current_char_image_url = char_img_url
                    last_character_id = d.speaker

            choices = [{"index": i, "text": c.text} for i, c in enumerate(scene.choices)]
            is_ending = len(scene.choices) == 0 and not scene.next_scene

            send_music_url = music_url if music_url != last_music_url else None
            if music_url:
                last_music_url = music_url

            server.update_scene(
                scene_id=scene_id,
                title=scene.title,
                dialogues=dialogues,
                choices=choices,
                is_ending=is_ending,
                background_url=background_url,
                music_url=send_music_url,
                current_character_image_url=current_char_image_url,
            )

            if is_ending:
                break

            choice_idx = None
            choice_time = 0
            while choice_idx is None:
                choice_idx, choice_time = server.get_pending_choice()
                if choice_idx is None:
                    import time
                    time.sleep(0.1)

            scene_id = get_next_scene(scene, choice_idx)

    thread = threading.Thread(target=game_loop, daemon=True)
    thread.start()

    print(f"Visual Novel server running at http://localhost:{port}")
    print("Open this URL in your browser to play.")
    server.run()


def main():
    story_path = Path(__file__).parent / "stories" / "demo"
    port = 8080
    web_mode = False
    generate_assets_only = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--web":
            web_mode = True
        elif arg == "--generate-assets":
            generate_assets_only = True
        elif arg == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            i += 1
        elif not arg.startswith("-"):
            story_path = Path(arg)
        i += 1

    if generate_assets_only:
        generate_all_assets(story_path)
    elif web_mode:
        run_web(story_path, port)
    else:
        run_terminal(story_path)


if __name__ == "__main__":
    main()
