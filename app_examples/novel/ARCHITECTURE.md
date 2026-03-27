# Mini-Visual Novel Architecture Plan

## 1. Project Overview

**Location**: `app_examples/novel/`
**Type**: Interactive text quest game (mini-visual novel)
**Stack**: Python 3.10+ / ncurses-style terminal UI / MiniMax API integration

### Core Features
- Text-based adventure with branching choices
- Procedural image generation via MiniMax (image-01)
- Procedural music generation via MiniMax (music-2.5)
- Modular story format (scenes, assets in separate files)
- Group-based scene management

---

## 2. Story Script Format

### Directory Structure
```
app_examples/novel/
├── stories/
│   └── demo/              # Story package
│       ├── meta.yaml      # Story metadata
│       ├── start.txt      # Entry scene ID
│       ├── scenes/
│       │   ├── intro.scn  # Scene files
│       │   ├── forest.scn
│       │   └── ending.scn
│       └── assets/
│           ├── characters.yaml  # Character definitions
│           └── music.yaml       # Music cues
├── engine/                # Game engine
│   ├── __init__.py
│   ├── story.py           # Story loader
│   ├── scene.py           # Scene parser & runner
│   ├── renderer.py        # Terminal UI renderer
│   ├── choices.py         # Choice handling
│   └── minimax_client.py  # MiniMax API wrapper
├── run_novel.py           # Entry point
└── requirements.txt
```

### Scene Format (`.scn` files)
```yaml
# intro.scn
id: intro
title: "The Beginning"
background: "dark forest clearing"

dialogue:
  - narrator: "You wake up in a strange place..."
  
  - character: hermit
    text: "Who goes there?"
    mood: curious

choice:
  - text: "I'm a traveler"
    next: forest_path
  - text: "I should go back"
    next: ending_early

generate_image: "dark forest clearing with mysterious fog"
generate_music: "ambient mysterious forest atmosphere"
```

### Asset Formats

**`meta.yaml`**:
```yaml
title: "Demo Story"
author: "MiniMax"
version: "1.0"
description: "A short demo visual novel"
```

**`assets/characters.yaml`**:
```yaml
hermit:
  name: "Old Hermit"
  default_mood: neutral
  description: "A mysterious old man living in the forest"
```

**`assets/music.yaml`**:
```yaml
intro_theme:
  prompt: "ambient mysterious forest atmosphere"
forest_theme:
  prompt: "peaceful forest with birds chirping"
```

---

## 3. Engine Components

### `minimax_client.py`
- `generate_image(prompt: str) -> Path` - generates and downloads image
- `generate_music(prompt: str) -> Path` - generates and downloads music
- Uses existing `minimax_http.py` patterns
- Caches assets in `out/novel_assets/`

### `story.py`
- `StoryLoader` - loads story package from directory
- `get_scene(scene_id: str) -> Scene`
- `list_scenes() -> list[str]`

### `scene.py`
- `Scene` - parsed scene object
- `parse_scene(content: str) -> Scene`
- `execute_scene(scene: Scene, renderer: Renderer)`

### `renderer.py`
- `Renderer` - terminal UI with ncurses
- `clear()`, `print_text()`, `print_dialogue()`
- `show_image(image_path: Path)`
- `play_music(music_path: Path)` - uses simple audio playback
- `present_choices(choices: list[Choice]) -> int`

### `choices.py`
- `Choice` - choice option with text and next scene ID
- `handle_choice(scene: Scene) -> str` - returns next scene ID

---

## 4. Game Flow

```
1. Load story from stories/demo/
2. Read start.txt to get entry scene ID
3. Loop:
   a. Load current scene
   b. Generate image (if specified) via MiniMax
   c. Generate music (if specified) via MiniMax
   d. Display background image (as ASCII or file path)
   e. Play background music
   f. Display dialogues sequentially
   g. Show choices (if any)
   h. Wait for player choice
   i. Load next scene
4. Exit when reaching terminal scene (no choices)
```

---

## 5. MiniMax API Integration

### Image Generation
- Endpoint: `POST /v1/image_generation`
- Model: `image-01`
- Use `save_image_urls_from_response()` pattern
- Cache in `out/novel_assets/{story_id}/images/`

### Music Generation
- Endpoint: `POST /v1/music_generation`
- Model: `music-2.5`
- Use `save_music_mp3_from_response()` pattern
- Cache in `out/novel_assets/{story_id}/music/`

### Text Generation (optional narration)
- Endpoint: `POST /v1/text/chatcompletion_v2`
- Model: `MiniMax-Text-01`
- Can be used for dynamic narration

---

## 6. Terminal Audio Playback

For simplicity, use `pygame` or `simpleaudio` to play MP3 files:
```python
import simpleaudio as sa
wave_obj = sa.WaveObject.from_wave_file(music_path)
wave_obj.play()
```

---

## 7. Implementation Plan

### Phase 1: Core Engine
1. Create directory structure
2. Implement `minimax_client.py` - API wrapper
3. Implement `story.py` - story loader
4. Implement `scene.py` - scene parser
5. Implement `choices.py` - choice handling
6. Implement `renderer.py` - terminal UI

### Phase 2: Demo Story
1. Create `stories/demo/` structure
2. Write `meta.yaml`
3. Write 3-4 connected scenes
4. Add character definitions
5. Add music cues

### Phase 3: Integration
1. Connect engine to MiniMax APIs
2. Add asset caching
3. Test full game loop

---

## 8. Testing Plan

### Unit Tests
- `test_scene_parser.py` - verify scene YAML parsing
- `test_story_loader.py` - verify story loading
- `test_choice_handling.py` - verify choice routing

### Integration Tests
- `test_full_game_loop.py` - run through demo story

### Manual Testing
- Run `python run_novel.py` and play through demo

---

## 9. Dependencies

```
httpx
pyyaml
simpleaudio  # for MP3 playback
pillow       # for image display (optional ASCII conversion)
```

Add to `requirements.txt`.
