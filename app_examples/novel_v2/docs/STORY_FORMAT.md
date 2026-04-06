# Story Format

Stories are defined in YAML files with the following structure:

```yaml
id: story_id
title: Story Title
author: Author Name
version: 1.0
start_scene: scene_1

scenes:
  scene_1:
    background: images/background.png
    music: audio/bgm.mp3
    dialogues:
      - speaker: Character Name
        text: "Dialogue text here"
        voice: audio/voice_001.mp3
        image: images/character.png
        choices:
          - text: "Choice 1"
            next_scene: scene_2
          - text: "Choice 2"
            next_scene: scene_3
    next_scene: scene_2  # Auto-advance if no choices

  scene_2:
    # ... scene definition
```

## Scene Properties

| Property | Type | Description |
|----------|------|-------------|
| background | string | Path to background image |
| music | string | Path to background music |
| video | string | Path to video file (for cutscenes) |
| dialogues | array | List of dialogue entries |
| next_scene | string | Scene to auto-advance to |

## Dialogue Properties

| Property | Type | Description |
|----------|------|-------------|
| speaker | string | Character speaking |
| text | string | Dialogue text |
| voice | string | Path to voice audio file |
| image | string | Path to character sprite |
| choices | array | List of choice options |

## Choice Properties

| Property | Type | Description |
|----------|------|-------------|
| text | string | Choice button text |
| next_scene | string | Scene to go to when selected |
