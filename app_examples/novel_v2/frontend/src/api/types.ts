import type { Scene, GameSession, Story } from '../types/novel'

export interface ApiResponse<T> {
  data: T | null
  error: string | null
  loading: boolean
}

export interface StartGameRequest {
  story_id: string
  user_id?: string
}

export interface ChoiceRequest {
  choice_index: number
}

export interface HealthResponse {
  status: string
  version: string
}

export interface StoriesResponse {
  stories: Story[]
}

export type { Scene, GameSession, Story }
