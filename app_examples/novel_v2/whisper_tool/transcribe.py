#!/usr/bin/env python3
"""Transcribe first 10 seconds of each voice file and create a mapping."""

import os
import json
import subprocess
import whisper
from pathlib import Path

# Paths
VOICES_DIR = Path(
    "/Users/rexarrior/programming/my/minimax_explore/app_examples/novel_v2/stories/demo/assets/voices"
)
OUTPUT_FILE = Path(
    "/Users/rexarrior/programming/my/minimax_explore/app_examples/novel_v2/whisper_tool/voice_mapping.json"
)

# Load existing mapping if it exists
if OUTPUT_FILE.exists():
    with open(OUTPUT_FILE, "r") as f:
        mapping = json.load(f)
else:
    mapping = {}

print(f"Loading whisper model...")
model = whisper.load_model("base")  # Using base model for speed

# Get all voice files
voice_files = sorted(VOICES_DIR.glob("voice_narrator_*.mp3"))
print(f"Found {len(voice_files)} narrator voice files")

for voice_file in voice_files:
    filename = voice_file.name

    # Skip if already transcribed
    if filename in mapping:
        print(f"Skipping {filename} (already mapped)")
        continue

    print(f"Transcribing {filename}...")

    # Extract first 10 seconds using ffmpeg
    temp_wav = voice_file.with_suffix(".wav")
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(voice_file),
                "-t",
                "10",  # 10 seconds
                "-ar",
                "16000",  # 16kHz for whisper
                "-ac",
                "1",  # mono
                str(temp_wav),
            ],
            check=True,
            capture_output=True,
        )

        # Transcribe
        result = model.transcribe(str(temp_wav), fp16=False)
        text = result["text"].strip()

        mapping[filename] = text
        print(f"  -> '{text[:80]}...'")

    except subprocess.CalledProcessError as e:
        print(f"  Error extracting audio: {e}")
        mapping[filename] = None
    except Exception as e:
        print(f"  Error transcribing: {e}")
        mapping[filename] = None
    finally:
        # Clean up temp file
        if temp_wav.exists():
            os.remove(temp_wav)

# Save mapping
with open(OUTPUT_FILE, "w") as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

print(f"\nMapping saved to {OUTPUT_FILE}")
print(f"Total files mapped: {len([v for v in mapping.values() if v is not None])}")
