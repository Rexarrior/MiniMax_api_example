# AGENTS.md — novel_v2 Visual Novel Project

## 1. Project Overview

- **Type**: Visual novel / text adventure game MVP
- **Tech Stack**: FastAPI + Vue 3 + PostgreSQL + TypeScript
- **Location**: `/Users/rexarrior/programming/my/minimax_explore/app_examples/novel_v2/`

## 2. Architecture Overview

The project follows a layered architecture with three main layers:

### API Layer
FastAPI routes in `backend/app/api/routes/`
- Handle HTTP requests/responses
- Input validation via Pydantic schemas
- Route matching and request dispatching

### Core Layer
Business logic abstractions in `backend/app/core/`
- Define abstract interfaces (GameEngine, SceneAdapter, StoryReader)
- Hide implementation details from API layer
- Enable easy swapping of implementations

### Data Layer
SQLAlchemy models and repositories in `backend/app/models/`, `backend/app/repositories/`
- Database models and schema definitions
- Data access patterns
- Persistence logic

## 3. Key Abstractions

### GameEngine (`backend/app/core/game_engine.py`)

Abstract interface that hides the game engine implementation. This abstraction allows the API layer to interact with game sessions without knowing the underlying storage mechanism.

```python
class GameEngine(ABC):
    @abstractmethod
    def start_session(self, story_id: str, user_id: str | None = None) -> GameSession: ...
    
    @abstractmethod
    def get_session(self, session_id: str) -> GameSession | None: ...
    
    @abstractmethod
    def make_choice(self, session_id: str, choice_index: int) -> GameSession: ...
    
    @abstractmethod
    def advance_dialogue(self, session_id: str) -> GameSession: ...
```

**Current Implementation**: `PostgresGameEngine` in `backend/app/adapters/postgres_game_engine.py`

The PostgresGameEngine stores game sessions in PostgreSQL and manages scene progression, dialogue state, and choice tracking.

### SceneAdapter (`backend/app/core/scene_adapter.py`)

Abstract interface for loading story scenes. This separates story content storage from game logic.

```python
class SceneAdapter(ABC):
    @abstractmethod
    def load_scene(self, story_id: str, scene_id: str) -> SceneData: ...
    
    @abstractmethod
    def list_stories(self) -> list[StoryMetadata]: ...
    
    @abstractmethod
    def get_characters(self, story_id: str) -> dict[str, Character]: ...
```

**Current Implementation**: `DiskSceneAdapter` in `backend/app/adapters/disk_scene_adapter.py`

The DiskSceneAdapter reads story files from the local filesystem, parsing YAML scene files and metadata.

### StoryReader (`backend/app/core/story_reader.py`)

Abstraction for reading story content including audio, voice, and video assets.

```python
class StoryReader(ABC):
    @abstractmethod
    def get_audio_url(self, story_id: str, audio_name: str) -> str | None: ...
    
    @abstractmethod
    def get_voice_url(self, story_id: str, character: str, voice_id: str) -> str | None: ...
    
    @abstractmethod
    def get_video_url(self, story_id: str, video_name: str) -> str | None: ...
```

**Current Implementation**: `DiskStoryReader`

Plays pre-recorded files from disk. Located in `backend/app/adapters/disk_story_reader.py`.

**Future Implementations**:
- `TTSStoryReader`: MiniMax/Google TTS integration for dynamic voice generation
- `StreamingStoryReader`: CDN-based streaming for video cutscenes

## 4. Data Models

### GameSession (SQLAlchemy)

| Field | Type | Description |
|-------|------|-------------|
| session_id | UUID | Primary key |
| user_id | VARCHAR | Nullable, for user tracking |
| story_id | VARCHAR | Current story identifier |
| current_scene_id | VARCHAR | Active scene identifier |
| dialogue_index | INTEGER | Current dialogue line index |
| is_ending | BOOLEAN | Whether scene is an ending |
| background_url | TEXT | Current background image URL (nullable) |
| music_url | TEXT | Current background music URL (nullable) |
| current_character_image_url | TEXT | Active character image URL (nullable) |
| choices_json | JSONB | Serialized choices array |
| dialogues_json | JSONB | Serialized dialogues array |
| created_at | TIMESTAMP | Session creation time |
| updated_at | TIMESTAMP | Last modification time |

## 5. API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/stories` | List all stories |
| GET | `/api/stories/{story_id}` | Get story metadata |
| POST | `/api/game/start` | Start new game session |
| GET | `/api/game/session/{session_id}` | Get session state |
| POST | `/api/game/choice` | Make a choice |
| POST | `/api/game/advance` | Advance dialogue |
| GET | `/api/media/{path}` | Serve media files |

## 6. Frontend Architecture

### Pinia Stores

- **gameStore**: Current scene, dialogue index, session state, game progression
- **audioStore**: Background music, voice volume, mute state, audio crossfade
- **storyStore**: Available stories list, current story metadata
- **settingsStore**: CPS (default 50), volume levels, voice enabled toggle

### Key Composables

- **useGame()**: Game loop, scene transitions, choice handling
- **useAudio()**: Audio playback with crossfade (1.5s default), volume management
- **useTypewriter()**: Typewriter effect at configurable CPS (default 50)
- **useMedia()**: Background and character image loading with preloading

### Media Playback

- **Audio**: HTML5 Audio with 1.5s crossfade between tracks for smooth transitions
- **Voice**: Pre-recorded MP3 files played via StoryReader abstraction
- **Video**: HTML5 video for cutscenes with standard playback controls
- **Text**: Typewriter effect at 50 CPS default, configurable range 40-60 CPS

## 7. Folder Structure Summary

```
novel_v2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/        # API endpoints
│   │   ├── core/              # Abstractions (GameEngine, SceneAdapter, StoryReader)
│   │   ├── adapters/          # Concrete implementations
│   │   ├── models/            # SQLAlchemy models
│   │   ├── repositories/      # Data access layer
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Business logic services
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── api/               # Axios client
│   │   ├── components/        # Vue components
│   │   ├── composables/       # Vue composables
│   │   ├── stores/            # Pinia stores
│   │   └── types/             # TypeScript types
│   └── tests/
├── stories/                   # Game stories (YAML + assets)
├── docs/                      # Documentation
└── tmp_docs/                  # Agent temp files (NOT COMMITTED)
```

## 8. Coding Conventions

### Python (Backend)

- Use type hints on ALL functions and variables
- Async/await for all I/O operations
- Pydantic for request/response validation
- SQLAlchemy 2.0 style (async session management)
- Follow: `backend/app/` package structure
- All new code must be fully typed

### TypeScript (Frontend)

- Use `interface` for object shapes, `type` for unions
- Vue 3 Composition API with `<script setup lang="ts">`
- Pinia for state management (no Vuex)
- Use composables for reusable logic
- Follow: `frontend/src/` structure
- Strict TypeScript mode enabled

## 9. Git Workflow

### tmp_docs Handling

- `tmp_docs/` is in `.gitignore`
- Agents can use it freely for temporary files and notes
- **Never commit contents of tmp_docs**

### Branch Strategy

- `main`: Stable, production-ready code
- `feature/*`: New features (e.g., `feature/tts-integration`)
- `fix/*`: Bug fixes (e.g., `fix/audio-crossfade`)

### Commit Messages

- Use clear, descriptive commit messages
- Prefix with type: `feat:`, `fix:`, `docs:`, `refactor:`

## 10. Testing Strategy

### Backend

```bash
cd backend
pytest tests/ -v
```

Run all tests with verbose output. Maintain high test coverage for core abstractions.

### Frontend

```bash
cd frontend
npm test          # Unit tests (Vitest)
npm run test:e2e  # E2E tests with Playwright
```

## 11. Common Commands

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up -d
```

## 12. Story Format

Stories are stored in `stories/{story_id}/` with the following structure:

### Directory Structure

```
stories/{story_id}/
├── meta.yaml          # Story metadata
├── start.txt          # Entry scene ID
├── scenes/
│   └── *.scn          # Scene files in YAML format
└── assets/
    ├── characters/    # Character images
    ├── music/         # Background music
    ├── voices/        # Character voice files
    └── videos/        # Cutscene videos
```

### Scene File Format

```yaml
id: scene_id
title: "Scene Title"
background: "image_filename.png"
music: music_filename.mp3

dialogue:
  - narrator: "Narration text"
  - character: char_id
    text: "Character dialogue"
    mood: emotion
    voice_url: voice_file.mp3
    character_image_url: char_mood.png

choice:
  - text: "Choice 1"
    next: next_scene_id
  - text: "Choice 2"
    next: other_scene_id
```

### meta.yaml Format

```yaml
id: story_id
title: "Story Title"
author: "Author Name"
version: "1.0"
description: "Story description"
```

## Development Guidelines

1. **Abstraction First**: When adding features, define the abstract interface in `core/` before implementing in `adapters/`
2. **Type Safety**: Both backend and frontend must maintain full type coverage
3. **Async Operations**: All I/O operations in backend must be async
4. **Media Abstraction**: Use StoryReader for all media access to enable future CDN/TTS integration
5. **State Management**: Frontend state flows through Pinia stores, not prop drilling
