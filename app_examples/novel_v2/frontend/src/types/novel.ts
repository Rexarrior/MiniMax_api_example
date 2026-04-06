export interface DialogueLine {
  speaker: string
  text: string
  mood: string | null
  voice_url: string | null
  character_image_url: string | null
}

export interface Choice {
  text: string
  next_scene_id: string
}

export interface Scene {
  scene_id: string
  title: string
  background_url: string | null
  background_video_url: string | null
  dialogues: DialogueLine[]
  choices: Choice[]
  is_ending: boolean
  music_url: string | null
  current_character_image_url: string | null
  timestamp: number
}

export interface GameSession {
  session_id: string
  user_id: string | null
  story_id: string
  current_scene_id: string
  dialogue_index: number
  is_ending: boolean
  background_url: string | null
  music_url: string | null
  current_character_image_url: string | null
  choices: Choice[]
  dialogues: DialogueLine[]
  created_at: string
  updated_at: string
}

export interface Story {
  id: string
  title: string
  author: string
  description: string
  version: string
}

export interface GameState {
  status: 'idle' | 'loading' | 'playing' | 'ending' | 'error'
  sessionId: string | null
  storyId: string | null
  currentScene: Scene | null
  dialogueIndex: number
  isPlaying: boolean
  error: string | null
}

export interface Player {
  id: string | null
  name: string | null
  avatar: string | null
  isAuthenticated: boolean
}
