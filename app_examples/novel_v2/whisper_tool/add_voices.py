#!/usr/bin/env python3
"""
Add voice entries to all narrator lines using the renamed voice files.
"""

import json
import re
import yaml
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
    slug = "_".join(words[:4])[:max_length]
    return slug


# Build text -> new_voice_filename mapping
text_to_voice = {}
for old_filename, text in voice_mapping.items():
    if not text:
        continue

    base_slug = slugify(text)

    # Find the new filename
    new_name = f"narr_{base_slug}.mp3"

    # Check if this exact name exists, if not find similar
    if not (VOICES_DIR / new_name).exists():
        # Try with counter suffix
        for i in range(100):
            test_name = f"narr_{base_slug}_{i}.mp3"
            if (VOICES_DIR / test_name).exists():
                new_name = test_name
                break

    text_to_voice[text.lower().strip().rstrip(".")] = new_name

print(f"Built mapping for {len(text_to_voice)} voice files")

# Get all narrator voice files (for verification)
voice_files = {f.name for f in VOICES_DIR.glob("narr_*.mp3")}
print(f"Found {len(voice_files)} narrator voice files on disk")

# Process all scene files
modified_count = 0
for scene_file in sorted(SCENES_DIR.glob("*.scn")):
    with open(scene_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    in_dialogue = False
    scene_modified = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Track dialogue section
        if "dialogue:" in line:
            in_dialogue = True
        elif in_dialogue and stripped and not line[0].isspace():
            if not stripped.startswith("-") and not stripped.startswith("#"):
                in_dialogue = False

        # Only process if we're in dialogue section
        if in_dialogue:
            # Match a narrator line
            m = re.match(r'^(\s+-\s+narrator:\s+")(.+)(",?)\s*$', line)
            if m:
                narrator_text = m.group(2)
                normalized_text = narrator_text.lower().strip().rstrip(".")

                # Find matching voice file
                voice_file = None
                if normalized_text in text_to_voice:
                    voice_file = text_to_voice[normalized_text]

                if voice_file and (VOICES_DIR / voice_file).exists():
                    # Add narrator line as-is, then voice line
                    new_lines.append(line)
                    list_indent = len(line) - len(line.lstrip())
                    voice_indent = " " * (list_indent + 2)
                    new_lines.append(f'{voice_indent}voice: "{voice_file}"\n')
                    scene_modified = True
                    i += 1
                    continue

        new_lines.append(line)
        i += 1

    if scene_modified:
        result = "\n".join(new_lines)
        with open(scene_file, "w", encoding="utf-8") as f:
            f.write(result)
        modified_count += 1
        print(f"  Modified: {scene_file.name}")

print(f"\nTotal files modified: {modified_count}")
