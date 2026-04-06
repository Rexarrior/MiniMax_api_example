#!/usr/bin/env python3
"""
Update scene YAML files with correct voice file names.
This creates a proper mapping between narrator text and voice files,
then updates the YAML files.
"""

import json
import re
import yaml
import hashlib
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

# Create reverse mapping: text snippet -> voice filename
text_to_voice = {}
for filename, text in voice_mapping.items():
    if text:
        normalized = text.lower().strip().rstrip(".")
        text_to_voice[normalized] = filename


def find_best_match(narrator_text):
    narrator_lower = narrator_text.lower().strip()

    best_match = None
    best_ratio = 0

    for text_snippet, filename in text_to_voice.items():
        if narrator_lower in text_snippet or text_snippet in narrator_lower:
            ratio = 0.95
        else:
            ratio = SequenceMatcher(None, narrator_lower, text_snippet).ratio()

        if ratio > best_ratio:
            best_ratio = ratio
            best_match = filename

    if best_ratio >= 0.6:
        return best_match, best_ratio
    return None, best_ratio


def slugify(text, max_length=30):
    """Create a short slug from text for filename."""
    # Take first max_length chars of cleaned text
    cleaned = re.sub(r"[^a-z0-9\s]", "", text.lower())
    words = cleaned.split()
    slug = "_".join(words)[:max_length]
    return slug


# Build final mapping: scene -> narrator_text -> voice_file
final_mapping = {}

for scene_file in sorted(SCENES_DIR.glob("*.scn")):
    with open(scene_file, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        data = yaml.safe_load(content)
    except:
        continue

    if data is None or "dialogue" not in data:
        continue

    scene_key = scene_file.name
    final_mapping[scene_key] = {}

    for d in data.get("dialogue", []):
        if "narrator" in d and isinstance(d["narrator"], str):
            narrator_text = d["narrator"]
            voice_file, ratio = find_best_match(narrator_text)
            if voice_file:
                final_mapping[scene_key][narrator_text] = voice_file
                print(f"MATCH ({ratio:.2f}): {scene_file.name} -> {voice_file}")

# Now update all scene files
print("\n=== UPDATING SCENE FILES ===")

for scene_file in sorted(SCENES_DIR.glob("*.scn")):
    with open(scene_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    scene_key = scene_file.name
    mapping = final_mapping.get(scene_key, {})

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this is a narrator line that needs updating
        m = re.match(r'^(\s+-\s+narrator:\s+")(.+)(")(\s*)$', line)
        if m:
            narrator_text = m.group(2)
            if narrator_text in mapping:
                voice_file = mapping[narrator_text]

                # Find if there's already a voice line after this
                j = i + 1
                has_voice = False
                current_indent = len(line) - len(line.lstrip())

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

                if has_voice:
                    # Update existing voice line
                    # Replace the voice filename
                    new_lines.append(line)
                    i += 1
                    while i < j:
                        voice_line = lines[i]
                        if "voice:" in voice_line:
                            # Replace the filename in this line
                            indent = len(voice_line) - len(voice_line.lstrip())
                            new_voice_line = f'{" " * indent}voice: "{voice_file}"\n'
                            new_lines.append(new_voice_line)
                            print(f"  Updated voice in {scene_file.name}: {voice_file}")
                        else:
                            new_lines.append(voice_line)
                        i += 1
                    continue
                else:
                    # Add new voice line
                    new_lines.append(line)
                    list_indent = len(line) - len(line.lstrip())
                    voice_indent = " " * (list_indent + 2)
                    new_lines.append(f'{voice_indent}voice: "{voice_file}"\n')
                    print(f"  Added voice to {scene_file.name}: {voice_file}")
                    i += 1
                    continue

        new_lines.append(line)
        i += 1

    # Write back
    with open(scene_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

print("\n=== DONE ===")
