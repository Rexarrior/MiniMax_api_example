#!/usr/bin/env python3
"""
Add voice entries to all narrator lines using fuzzy matching.
Uses the whisper transcription to match narrator text to voice files.
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


# Build text -> new_voice_filename mapping using exact match
text_to_voice_exact = {}
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

    # Normalize text for exact matching
    normalized = text.lower().strip().rstrip(".")
    text_to_voice_exact[normalized] = new_name


# Build fuzzy matcher
def find_best_match(narrator_text):
    """Find best matching voice file using fuzzy matching."""
    narrator_lower = narrator_text.lower().strip()

    best_match = None
    best_ratio = 0

    # First try exact match
    if narrator_lower in text_to_voice_exact:
        return text_to_voice_exact[narrator_lower], 1.0

    # Try fuzzy matching
    for text_snippet, filename in text_to_voice_exact.items():
        ratio = SequenceMatcher(None, narrator_lower, text_snippet).ratio()
        if ratio > best_ratio and ratio >= 0.85:  # 85% threshold
            best_ratio = ratio
            best_match = filename

    return best_match, best_ratio


# Process all scene files
print("=== PROCESSING SCENE FILES ===")
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

                # Check if this narrator line already has a voice
                j = i + 1
                current_indent = len(line) - len(line.lstrip())
                has_voice = False

                while j < len(lines):
                    next_line = lines[j]
                    next_stripped = next_line.strip()
                    next_indent = len(next_line) - len(next_line.lstrip())

                    if next_stripped and next_indent <= current_indent:
                        break
                    if "voice:" in next_line:
                        has_voice = True
                        break
                    j += 1

                if not has_voice:
                    voice_file, ratio = find_best_match(narrator_text)
                    if voice_file:
                        new_lines.append(line)
                        list_indent = len(line) - len(line.lstrip())
                        voice_indent = " " * (list_indent + 2)
                        new_lines.append(f'{voice_indent}voice: "{voice_file}"\n')
                        scene_modified = True
                        print(
                            f"  {scene_file.name}: '{narrator_text[:40]}...' -> {voice_file}"
                        )
                        i += 1
                        continue

        new_lines.append(line)
        i += 1

    if scene_modified:
        result = "\n".join(new_lines)
        with open(scene_file, "w", encoding="utf-8") as f:
            f.write(result)

print("\n=== DONE ===")
