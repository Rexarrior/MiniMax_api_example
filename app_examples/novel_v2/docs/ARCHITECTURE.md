# Novel V2 Architecture

## Overview

This is a visual novel/text adventure game MVP built with:
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy
- **Frontend**: Vue 3 + TypeScript + Pinia + TailwindCSS
- **Architecture**: Clean Architecture with clear separation of concerns

## Architecture Layers

### 1. API Layer (`backend/app/api/`)
- FastAPI routes handle HTTP requests
- Request/response schemas via Pydantic
- Dependency injection for services

### 2. Core Layer (`backend/app/core/`)
Contains business logic abstractions:
- `GameEngine`: Manages game sessions and state transitions
- `SceneAdapter`: Loads story scenes from storage
- `StoryReader`: Reads story assets (audio, voice, video, images)

### 3. Data Layer (`backend/app/models/`, `backend/app/repositories/`)
- SQLAlchemy models for persistence
- Repository pattern for data access

### 4. Adapter Layer (`backend/app/adapters/`)
Implementations of core abstractions:
- `PostgresGameEngine`: Game engine with PostgreSQL session storage
- `DiskSceneAdapter`: Scene loading from YAML files
- `DiskStoryReader`: Asset reading from disk filesystem

## Frontend Architecture

### State Management (Pinia Stores)
- `gameStore`: Current game session, scene, dialogue state
- `audioStore`: Music, voice, SFX playback with Howler.js
- `storyStore`: Available stories list
- `settingsStore`: User preferences (CPS, volume, etc.)

### Composables
- `useGame`: Game flow logic (start, advance, choice)
- `useAudio`: Audio playback wrapper
- `useTypewriter`: Text animation with configurable CPS
- `useMedia`: Asset preloading

### Components
- `GameScreen`: Main gameplay view
- `DialogueBox`: Text display with typewriter effect
- `ChoiceMenu`: Interactive choice buttons
- `BackgroundLayer`: Image/video background
- `CharacterSprite`: Character image overlay

## Media Pipeline

### Audio
- Background music with 1.5s crossfade
- Voice lines played on dialogue
- Volume controls per category

### Video
- HTML5 video for cutscenes
- Fullscreen support

### Images
- Background images (16:9 aspect)
- Character sprites (variable size)
- Preloading for smooth transitions

## Data Flow

1. Player selects story → `startGame()` in gameStore
2. Backend creates session, returns initial scene
3. Scene data stored in gameStore
4. Player advances dialogue → typewriter effect plays
5. Player makes choice → POST to backend → new scene loaded
6. Repeat until ending reached
