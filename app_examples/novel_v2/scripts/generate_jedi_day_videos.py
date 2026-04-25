#!/usr/bin/env python3
"""Generate 3 epic Star Wars style videos for Jedi Day story."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "examples_python"))
import minimax_http as mh

# Output directory
VIDEO_DIR = Path(__file__).parent.parent.parent.parent / "app_examples" / "novel_v2" / "stories" / "jedi_day" / "assets" / "videos"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

# 3 epic video prompts for Jedi Day
VIDEO_PROMPTS = [
    {
        "name": "jedi_temple_aerial",
        "prompt": "Epic aerial shot of ancient Jedi temple on distant planet, massive spires glowing with blue force energy, young padawans training on courtyards, cinematic Star Wars style, dramatic lighting, IMAX quality"
    },
    {
        "name": "lightsaber_clash",
        "prompt": "Intense close-up of two lightsabers clashing, blue and red blades creating sparks and energy ripples, dramatic combat in dark throne room, epic orchestral moment, Star Wars battle scene"
    },
    {
        "name": "starship_battle",
        "prompt": "Cinematic space battle scene, Rebel starfighters weaving through explosion debris, Star Destroyer looming in background, laser fire illuminating cosmic dust, epic dogfight, Star Wars space opera"
    },
]


def generate_video(name: str, prompt: str, output_path: Path) -> bool:
    """Generate a single video."""
    print(f"\n{'='*60}")
    print(f"Generating video: {name}")
    print(f"Prompt: {prompt[:80]}...")
    print(f"{'='*60}")

    # Start generation
    body = {
        "model": "MiniMax-Hailuo-2.3",
        "prompt": prompt,
        "duration": 6,
        "resolution": "768P",
        "prompt_optimizer": True,
    }

    try:
        # Submit task
        d = mh.api_request("POST", "/v1/video_generation", body)
        mh.require_base_ok(d)

        task_id = d.get("task_id")
        if not task_id:
            print(f"ERROR: No task_id for {name}")
            return False

        print(f"Task submitted: {task_id}")

        # Poll for completion (up to 3 minutes)
        max_rounds = 60
        for i in range(max_rounds):
            time.sleep(3)
            q = mh.api_request("GET", f"/v1/query/video_generation?task_id={task_id}")
            mh.require_base_ok(q)

            st = str(q.get("status", "")).lower()
            print(f"  [{i+1}/{max_rounds}] Status: {st}")

            if st == "success":
                fid = q.get("file_id")
                if not fid:
                    print(f"ERROR: No file_id for {name}")
                    return False

                # Get download URL
                r = mh.api_request("GET", f"/v1/files/retrieve?file_id={fid}")
                mh.require_base_ok(r)
                url = (r.get("file") or {}).get("download_url") or ""
                if not url:
                    print(f"ERROR: No download_url for {name}")
                    return False

                # Download video
                mh.download_url_to_file(str(url), output_path)
                print(f"SUCCESS: Downloaded {output_path.name} ({output_path.stat().st_size} bytes)")
                return True

            if st == "fail":
                print(f"ERROR: Generation failed for {name}")
                return False

        print(f"ERROR: Timeout waiting for {name}")
        return False

    except Exception as e:
        print(f"ERROR generating {name}: {e}")
        return False


def main() -> None:
    print("Video Generation Script for Jedi Day")
    print(f"Output directory: {VIDEO_DIR}")
    print(f"Generating {len(VIDEO_PROMPTS)} videos")

    results = {}
    for vp in VIDEO_PROMPTS:
        output_path = VIDEO_DIR / f"{vp['name']}.mp4"
        result = generate_video(vp['name'], vp['prompt'], output_path)
        results[vp['name']] = result

        # Small delay between submissions
        if result:
            time.sleep(2)

    # Summary
    print(f"\n{'='*60}")
    print("GENERATION COMPLETE")
    print(f"{'='*60}")
    success = sum(1 for r in results.values() if r)
    print(f"Successfully generated: {success}/{len(VIDEO_PROMPTS)}")
    for name, result in results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {name}")


if __name__ == "__main__":
    main()