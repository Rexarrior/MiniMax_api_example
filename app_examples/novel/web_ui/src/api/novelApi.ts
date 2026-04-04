import axios from 'axios'
import type { Scene, Story, PollResponse, StartGameResponse } from '@/types/novel'

let cachedSessionId: string | null = null

function getSessionIdFromUrl(): string | null {
  if (typeof window === 'undefined') return null
  const params = new URLSearchParams(window.location.search)
  return params.get('session_id')
}

export function getSessionId(): string {
  if (cachedSessionId) {
    return cachedSessionId
  }
  
  const urlSessionId = getSessionIdFromUrl()
  if (urlSessionId) {
    cachedSessionId = urlSessionId
    return cachedSessionId
  }
  
  const newId = 'session_' + Math.random().toString(36).substring(2, 15)
  cachedSessionId = newId
  
  if (typeof window !== 'undefined') {
    const url = new URL(window.location.href)
    url.searchParams.set('session_id', newId)
    window.history.replaceState({}, '', url.toString())
  }
  
  return cachedSessionId
}

export function updateSessionIdFromResponse(sessionId: string): void {
  cachedSessionId = sessionId
  if (typeof window !== 'undefined') {
    const url = new URL(window.location.href)
    url.searchParams.set('session_id', sessionId)
    window.history.replaceState({}, '', url.toString())
  }
}

export function updateSessionIdHeader(sessionId: string): void {
  cachedSessionId = sessionId
}

function createApi() {
  const sessionId = getSessionId()
  return axios.create({
    baseURL: '/api',
    timeout: 30000,
    headers: {
      'X-Session-ID': sessionId
    }
  })
}

export async function getStories(): Promise<Story[]> {
  const response = await createApi().get<Story[]>('/stories')
  return response.data
}

export async function startGame(storyId: string): Promise<StartGameResponse> {
  const response = await createApi().post<StartGameResponse>('/game/start', { story_id: storyId })
  return response.data
}

export async function fetchScene(): Promise<Scene> {
  const response = await createApi().get<Scene>('/scene')
  return response.data
}

export async function pollScene(lastTimestamp: number): Promise<PollResponse> {
  const response = await createApi().get<PollResponse>('/poll', {
    params: { timestamp: lastTimestamp }
  })
  return response.data
}

export async function submitChoice(choiceIndex: number): Promise<Scene> {
  const response = await createApi().post<Scene>('/choice', { choice_index: choiceIndex })
  return response.data
}