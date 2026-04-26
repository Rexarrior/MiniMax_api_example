import client from './client'
import type { Scene, GameSession, Story, StartGameRequest, ChoiceRequest } from './types'

class NovelApi {
  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await client.get('/health')
    return response.data
  }

  async listStories(): Promise<Story[]> {
    const response = await client.get('/stories')
    return response.data.stories
  }

  async getStory(storyId: string): Promise<Story> {
    const response = await client.get(`/stories/${storyId}`)
    return response.data
  }

  async startGame(request: StartGameRequest): Promise<GameSession> {
    const response = await client.post('/game/start', request)
    if (response.data.session_id) {
      localStorage.setItem('session_id', response.data.session_id)
    }
    return response.data
  }

  async getSession(sessionId: string): Promise<GameSession> {
    const response = await client.get(`/game/session/${sessionId}`)
    return response.data
  }

  async getScene(sessionId: string, language?: string): Promise<Scene> {
    const params = language ? `?language=${language}` : ''
    const response = await client.get(`/game/scene/${sessionId}${params}`)
    return response.data
  }

  async makeChoice(choiceIndex: number): Promise<GameSession> {
    const sessionId = localStorage.getItem('session_id')
    if (!sessionId) {
      throw new Error('No session ID')
    }
    const response = await client.post(
      '/game/choice',
      { choice_index: choiceIndex },
      { headers: { 'X-Session-ID': sessionId } }
    )
    return response.data
  }

  async advanceDialogue(): Promise<GameSession> {
    const sessionId = localStorage.getItem('session_id')
    if (!sessionId) {
      throw new Error('No session ID')
    }
    const response = await client.post(
      '/game/advance',
      {},
      { headers: { 'X-Session-ID': sessionId } }
    )
    return response.data
  }
}

export const novelApi = new NovelApi()
