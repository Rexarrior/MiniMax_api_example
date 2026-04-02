export interface Dialogue {
  speaker: 'narrator' | string
  text: string
  voice_url?: string
  character_image_url?: string
}

export interface Choice {
  index: number
  text: string
  next?: string
}

export interface Scene {
  scene_id: string
  title: string
  background_url?: string
  dialogues: Dialogue[]
  choices: Choice[]
  is_ending: boolean
  music_url?: string
  timestamp: number
  current_character_image_url?: string
}

export interface Story {
  id: string
  title: string
  description: string
}

export interface PollResponse {
  scene: Scene | null
  timestamp: number
}

export interface StartGameResponse {
  success: boolean
  scene: Scene
}