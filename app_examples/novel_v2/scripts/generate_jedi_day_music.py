#!/usr/bin/env python3
"""Generate missing music tracks for Jedi Day story."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Add examples_python to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "examples_python"))

import minimax_http as mh

# Paths
NOVEL_V2_ROOT = Path(__file__).parent.parent.parent.parent / "app_examples" / "novel_v2"
MUSIC_YAML_PATH = NOVEL_V2_ROOT / "stories" / "jedi_day" / "assets" / "music.yaml"
MUSIC_OUTPUT_DIR = NOVEL_V2_ROOT / "stories" / "jedi_day" / "assets" / "music"

# Tracks that are already generated (by matching prompt keywords)
EXISTING_TRACKS = {
    "peaceful_morning_temple": "temple_morning_ambient",
    "calm_meditation_ambient": "calm_meditation_ambient",
    "ominous_tension_build": "ominous_tension_build",
    "scholarly_contemplation": "scholarly_contemplation",
    "urgent_military_comm": "urgent_military_comm",
    "engine_hum_activity": "engine_hum_activity",
    "heroic_adventure_flight": "heroic_adventure_flight",
    "village_life_ambient": "village_life_ambient",
    "friendly_reunion_warm": "friendly_reunion_warm",
    "foreboding_jungle_danger": "foreboding_jungle_danger",
    "dark_ritual_ambience": "dark_ritual_ambience",
}

# Missing tracks to generate
MISSING_TRACKS = {
    "sinister_revelation": "sinister revelation, dark confession, dramatic tension, villain speech backing, menacing undercurrent",
    "epic_duel_orchestral": "epic duel orchestral, intense lightsaber battle music, percussion heavy, heroic climax, Star Wars action",
    "dramatic_collapse": "dramatic collapse, temple imploding, falling debris, dust clouds, epic destruction sequence",
    "triumphant_victory_fanfare": "triumphant victory fanfare, Wookiee celebration, heroic celebration, community cheering, joyful",
    "serene_resolution": "serene resolution, peaceful ending, sunset meditation, calm after storm, contemplative closure",
}


def slug_from_prompt(prompt: str) -> str:
    """Create a filename slug from prompt text."""
    # Take first ~50 chars of first sentence, replace special chars
    first_part = prompt.split(",")[0].strip()[:50]
    slug = ""
    for c in first_part.lower():
        if c.isalnum():
            slug += c
        elif c == " ":
            slug += "_"
        elif c in "-'":
            slug += c
    return slug


def generate_music_track(track_id: str, prompt: str, output_dir: Path) -> Path | None:
    """Generate a single music track."""
    print(f"\n{'='*60}")
    print(f"Generating: {track_id}")
    print(f"Prompt: {prompt}")
    print(f"{'='*60}")

    model = "music-2.5"
    # Wrap prompt as "Instrumental ambient music:" to satisfy API lyrics requirement
    lyrics = f"Instrumental ambient music: {prompt}"
    req = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "output_format": "hex",
        "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"},
        "lyrics": lyrics,
        "lyrics_optimizer": False,
    }

    try:
        d = mh.api_request("POST", "/v1/music_generation", req)
        mh.require_base_ok(d)

        hex_audio = (d.get("data") or {}).get("audio")
        if not hex_audio or not hex_audio.strip():
            print(f"ERROR: No audio in response for {track_id}")
            return None

        # Create filename
        slug = slug_from_prompt(prompt)
        # Truncate slug to fit reasonable filename length
        slug = slug[:80]
        filename = f"{slug}.mp3"
        dest = output_dir / filename

        # Write hex to mp3
        mh.write_hex_mp3(hex_audio, dest)
        print(f"SUCCESS: Wrote {dest}")
        return dest

    except Exception as e:
        print(f"ERROR generating {track_id}: {e}")
        return None


def main() -> None:
    print("Music Generation Script for Jedi Day")
    print(f"Output directory: {MUSIC_OUTPUT_DIR}")
    print(f"Missing tracks: {len(MISSING_TRACKS)}")

    # Ensure output directory exists
    MUSIC_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate each missing track
    results = {}
    for track_id, prompt in MISSING_TRACKS.items():
        result = generate_music_track(track_id, prompt, MUSIC_OUTPUT_DIR)
        results[track_id] = result

        # Rate limiting - wait between requests
        if result:
            print(f"Waiting 3 seconds before next request...")
            time.sleep(3)

    # Summary
    print(f"\n{'='*60}")
    print("GENERATION COMPLETE")
    print(f"{'='*60}")
    success = sum(1 for r in results.values() if r is not None)
    print(f"Successfully generated: {success}/{len(MISSING_TRACKS)}")

    for track_id, result in results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {track_id}")


if __name__ == "__main__":
    main()