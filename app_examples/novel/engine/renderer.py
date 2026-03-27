"""Terminal UI renderer for visual novel."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

try:
    import simpleaudio as sa
    HAS_SIMPLEAUDIO = True
except ImportError:
    HAS_SIMPLEAUDIO = False


class Renderer:
    def __init__(self):
        self._current_music: Optional[object] = None

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def print_title(self, title: str) -> None:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}\n")

    def print_dialogue(self, speaker: str, text: str, mood: str | None = None) -> None:
        mood_str = f" [{mood}]" if mood else ""
        print(f"\n[{speaker}]{mood_str}: {text}\n")

    def print_narrator(self, text: str) -> None:
        print(f"\n  {text}\n")

    def print_choices(self, choices: list[tuple[int, str]]) -> None:
        print("\nWhat do you do?\n")
        for idx, text in choices:
            print(f"  [{idx + 1}] {text}")
        print()

    def print_image(self, image_path: Path) -> None:
        if image_path and image_path.exists():
            print(f"\n[Image: {image_path.name}]\n")

    def play_music(self, music_path: Path) -> None:
        if not HAS_SIMPLEAUDIO or not music_path or not music_path.exists():
            return
        try:
            if self._current_music:
                self._current_music.stop()
            wave = sa.WaveObject.from_wave_file(str(music_path))
            self._current_music = wave.play()
        except Exception:
            pass

    def stop_music(self) -> None:
        if self._current_music:
            try:
                self._current_music.stop()
            except Exception:
                pass
            self._current_music = None

    def wait_for_choice(self, max_choices: int) -> int | None:
        while True:
            try:
                choice = input("Enter choice number: ").strip()
                idx = int(choice) - 1
                if 0 <= idx < max_choices:
                    return idx
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")
            except (EOFError, KeyboardInterrupt):
                return None

    def print_message(self, text: str) -> None:
        print(text)

    def print_ending(self, text: str) -> None:
        print(f"\n{'=' * 60}")
        print(f"  {text}")
        print(f"{'=' * 60}\n")
