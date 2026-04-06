#!/usr/bin/env python3
"""Match narrator text in scenes with transcribed voice files and update everything."""

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

# Create reverse mapping: text snippet -> voice filename
text_to_voice = {}
for filename, text in voice_mapping.items():
    if text:
        # Normalize text for matching
        normalized = text.lower().strip().rstrip(".")
        text_to_voice[normalized] = filename

# Extract all narrator lines from scenes
narrator_lines = []
for scene_file in sorted(SCENES_DIR.glob("*.scn")):
    with open(scene_file, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        data = yaml.safe_load(content)
    except:
        continue

    if data is None or "dialogue" not in data:
        continue

    for d in data.get("dialogue", []):
        if "narrator" in d and isinstance(d["narrator"], str):
            narrator_lines.append({"text": d["narrator"], "scene": scene_file.name})

print(f"Found {len(narrator_lines)} narrator lines in scenes")
print(f"Found {len(text_to_voice)} voice files with transcriptions")


# Function to find best matching voice file
def find_best_match(narrator_text):
    narrator_lower = narrator_text.lower().strip()

    best_match = None
    best_ratio = 0

    for text_snippet, filename in text_to_voice.items():
        # Try exact substring match first
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


# Match and show results
print("\n=== MATCHING RESULTS ===")
matched_count = 0
unmatched = []

for item in narrator_lines:
    voice_file, ratio = find_best_match(item["text"])
    if voice_file:
        matched_count += 1
        print(f"MATCH ({ratio:.2f}): '{item['text'][:50]}...' -> {voice_file}")
    else:
        unmatched.append(item)
        print(f"UNMATCHED: '{item['text'][:50]}...'")

print(f"\nMatched: {matched_count}/{len(narrator_lines)}")
print(f"Unmatched: {len(unmatched)}")
