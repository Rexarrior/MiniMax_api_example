import axios from 'axios'
import type { Scene, Story, PollResponse, StartGameResponse } from '@/types/novel'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

export async function getStories(): Promise<Story[]> {
  const response = await api.get<Story[]>('/stories')
  return response.data
}

export async function startGame(storyId: string): Promise<StartGameResponse> {
  const response = await api.post<StartGameResponse>('/game/start', { story_id: storyId })
  return response.data
}

export async function fetchScene(): Promise<Scene> {
  const response = await api.get<Scene>('/scene')
  return response.data
}

export async function pollScene(lastTimestamp: number): Promise<PollResponse> {
  const response = await api.get<PollResponse>('/poll', {
    params: { timestamp: lastTimestamp }
  })
  return response.data
}

export async function submitChoice(choiceIndex: number): Promise<void> {
  await api.post('/choice', { choice_index: choiceIndex })
}