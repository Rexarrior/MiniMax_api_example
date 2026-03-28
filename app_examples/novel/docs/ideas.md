# Visual Novel Project - Ideas & Notes

## Goal

Develop a visual novel web application with AI-generated backgrounds and character images using MiniMax API. The project is located in `app_examples/novel/`.

## Instructions

- Fix image loading issues (images not displaying, no generation attempts)
- Add sound/music toggle button enabled by default
- Generate background images for ALL scenes (not just one)
- Generate character images (full-screen background with character) when characters speak
- When narrator speaks between character lines, keep the character image visible
- Character prompts should combine character appearance + scene background
- Create separate `--generate-assets` flag for pre-generating images before gameplay
- Commit all changes including generated assets

## Discoveries

**Bug found and fixed in `minimax_http.py:185`:**
- `save_image_urls_from_response` was saving images to `out/` instead of the specified path
- Fixed by changing `out_dir() / f"{basename_prefix}_0.jpeg"` to `Path(f"{basename_prefix}_0.jpeg")`

**Bug found and fixed in `minimax_client.py:32`:**
- Cache check looked for `{safe_name}.jpeg` but `save_image_urls_from_response` saves as `{safe_name}_0.jpeg`
- Fixed by changing cache check to look for `{safe_name}_0.jpeg`

**Music autoplay and persistence:**
- Music now persists across scene transitions (only stops at ending)
- Music won't restart if same track is already playing
- Added `currentMusicSrc` tracking to avoid unnecessary src changes
- If music is paused (browser policy, tab switch, etc.), tries to resume when same scene reloads
- Added sound toggle button (enabled by default) as workaround for autoplay policies

**Character image architecture:**
- When character speaks: background changes to character image (character + their scene background combined)
- When narrator speaks: keeps last character's image visible
- When choices appear: character image hides

## Accomplished

- Fixed image loading bug (path issue in `minimax_http.py`)
- Fixed cache check mismatch in `minimax_client.py`
- Added `background_prompt` field to all 20 scene files
- Added `appearance_prompt` for hermit in `characters.yaml`
- Added `generate_background_image()` method in `minimax_client.py`
- Added `generate_character_image()` method in `minimax_client.py`
- Updated `scene.py` to parse `background_prompt` field
- Updated `web_server.py` with `current_character_image_url` and `update_character_image()`
- Updated `run_novel.py` with `generate_all_assets()` function and `--generate-assets` flag
- Created web UI with character layer and sound button
- All 20 backgrounds generated and saved
- 4 character images generated (hermit in 4 different scenes)
- Music generated
- Added TTS voice feature with per-character voice settings
- Voice lines generated for all dialogue (characters + narrator)
- Text typing syncs with voice duration
- All changes committed to git

## Voice/TTS Feature

### Voice Settings (in `characters.yaml`)
Each character can have voice settings:
- `voice_id`: MiniMax TTS voice ID (e.g., `English_Insightful_Speaker`, `English_Graceful_Lady`)
- `speed`: Speech speed [0.5, 2.0], default 1.0
- `pitch`: Pitch adjustment [-12, 12], default 0

**Current voice assignments:**
- `hermit`: `English_Insightful_Speaker`, speed=0.9, pitch=-2 (wise elderly voice)
- `narrator`: `English_Graceful_Lady`, speed=1.0, pitch=0

### Available English Voice IDs
- `English_Graceful_Lady` - graceful female voice
- `English_Insightful_Speaker` - insightful male voice
- `English_radiant_girl` - youthful female voice
- `English_Persuasive_Man` - persuasive male voice
- `English_Lucky_Robot` - robot voice

### Text-Voice Sync
- Voice duration (ms) is returned from TTS API
- Character typing speed calculated as: `voice_duration_ms / text_length`
- Text displays character-by-character synced with voice playback
- Falls back to default typing speed (30ms/char) if no voice

### Voice File Cache
- Cache key includes text hash + speed + pitch: `voice_{char}_{text_hash}_{speed}_{pitch}.mp3`
- Stored in `stories/{story_id}/assets/voices/`

## Bug Fixes

### Music autoplay and scene transitions (fixed)
- Previously: Music would stop when transitioning to scenes without `generate_music`
- Previously: Music would restart even when same track was already playing
- Fixed: Music persists across scene transitions unless new scene has DIFFERENT music
- Fixed: No longer calls `pause()` when scene has no music_url

## Relevant files / directories

### Core Engine Files
- `app_examples/novel/engine/scene.py` - Scene dataclass and parser (added `background_prompt` field)
- `app_examples/novel/engine/minimax_client.py` - MiniMax API client (added `generate_background_image`, `generate_character_image`, `generate_voice` methods)
- `app_examples/novel/engine/web_server.py` - Bottle web server with polling API (added `current_character_image_url` support and `/api/audio/voices/` route)
- `app_examples/novel/engine/story.py` - Story loader
- `app_examples/novel/engine/renderer.py` - Terminal renderer

### Main Entry Point
- `app_examples/novel/run_novel.py` - Entry point with `--web` and `--generate-assets` modes

### Web UI Files
- `app_examples/novel/web_ui/index.html` - HTML with `#character-layer` div and `#sound-btn`
- `app_examples/novel/web_ui/style.css` - CSS for character layer (opacity transitions) and sound button
- `app_examples/novel/web_ui/app.js` - JavaScript with sound toggle, character image display logic

### Story Content Files
- `app_examples/novel/stories/demo/assets/characters.yaml` - Character definitions with `appearance_prompt`
- `app_examples/novel/stories/demo/scenes/` - All 20 `.scn` files with `background_prompt` fields

### Generated Assets (Committed)
- `app_examples/novel/stories/demo/assets/images/` - 20 background images (bg_*.jpeg) + 4 character images (char_*.jpeg)
- `app_examples/novel/stories/demo/assets/music/` - Generated music files
- `app_examples/novel/stories/demo/assets/voices/` - Generated voice lines (voice_*.mp3)

### Shared Library
- `examples_python/minimax_http.py` - Fixed `save_image_urls_from_response` to save to correct path, added `generate_speech()` TTS helper

## Next Steps

1. **Test the application:**
   ```bash
   cd app_examples/novel && python run_novel.py --generate-assets  # First time only
   cd app_examples/novel && python run_novel.py --web
   # Open http://localhost:8080
   ```

2. **Potential improvements:**
   - Add more characters (currently only "hermit" has `appearance_prompt`)
   - Add `generate_music` to other scenes (currently only `intro.scn` has music)
   - Add character portraits/sprites overlay mode (current implementation replaces background)
   - Add scene transitions/effects
   - Mobile responsive improvements
   - Emotion-aware voice settings (use TTS emotion parameter based on dialogue mood)
   - Custom voice cloning for characters
