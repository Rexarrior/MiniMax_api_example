#!/usr/bin/env python3
"""
Rename voice files based on their transcribed content and update YAML references.
Uses direct string replacement to preserve YAML formatting.
"""

import json
import re
import shutil
from pathlib import Path
from difflib import SequenceMatcher

# Paths
VOICES_DIR = Path(
    "/Users/rexarrior/programming/my/minimax_explore/app_examples/novel_v2/stories/demo/assets/voices"
)
SCENES_DIR = Path(
    "/Users/rexarrior/programming/my/minimax_explore/app_examples/novel_v2/stories/demo/scenes"
)
MAPPING_FILE = Path(
    "/Users/rexarrior/programming/my/minimax_explore/app_examples/novel_v2/whisper_tool/voice_mapping.json"
)

# Load voice mapping
with open(MAPPING_FILE, "r") as f:
    voice_mapping = json.load(f)


def slugify(text, max_length=20):
    """Create a short descriptive slug from text for filename."""
    cleaned = re.sub(r"[^a-z0-9\s]", "", text.lower())
    words = cleaned.split()
    if not words:
        return "unknown"
    # Take first 3-4 words max
    slug = "_".join(words[:4])[:max_length]
    return slug


# Create rename mapping: old_filename -> new_filename
rename_map = {}
used_names = set()

for old_filename, text in voice_mapping.items():
    if not text:
        continue

    base_slug = slugify(text)

    # Handle duplicates by adding hash suffix
    counter = 0
    while True:
        if counter == 0:
            new_name = f"narr_{base_slug}.mp3"
        else:
            new_name = f"narr_{base_slug}_{counter}.mp3"

        if new_name not in used_names and (VOICES_DIR / new_name).exists() == False:
            break
        counter += 1
        if counter > 100:
            new_name = f"narr_{base_slug}_{old_filename.split('_')[2][:6]}.mp3"
            break

    used_names.add(new_name)
    rename_map[old_filename] = new_name

print("=== RENAME MAPPING (first 10) ===")
for old, new in list(rename_map.items())[:10]:
    print(f"  {old}")
    print(f"    -> {new}")

# Rename files
print("\n=== RENAMING FILES ===")
renamed_count = 0
for old_filename, new_filename in rename_map.items():
    old_path = VOICES_DIR / old_filename
    new_path = VOICES_DIR / new_filename
    if old_path.exists():
        shutil.move(str(old_path), str(new_path))
        print(f"  {old_filename} -> {new_filename}")
        renamed_count += 1

print(f"\nRenamed {renamed_count} files")

# Now update scene YAML files using string replacement
print("\n=== UPDATING SCENE YAML FILES ===")

for scene_file in sorted(SCENES_DIR.glob("*.scn")):
    with open(scene_file, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Replace old filename with new filename for each mapping
    for old_filename, new_filename in rename_map.items():
        # Replace in voice: "filename" pattern
        content = content.replace(
            f'veoice: "{old_filename}"', f'voice: "{new_filename}"'
        )
        content = content.replace(
            f'voice: "{old_filename}"', f'voice: "{new_filename}"'
        )

    if content != original_content:
        with open(scene_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Updated: {scene_file.name}")

print("\n=== DONE ===")
