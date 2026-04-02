import axios from 'axios'
import type { Scene, Story, PollResponse, StartGameResponse } from '@/types/novel'

let cachedSessionId: string | null = null

function getCurrentUrl(): string {
  if (typeof window !== 'undefined') {
    return window.location.href
  }
  return ''
}

export function getSessionId(): string {
  if (cachedSessionId) return cachedSessionId
  
  const url = getCurrentUrl()
  const params = new URLSearchParams(url.split('?')[1] || '')
  let sessionId = params.get('session_id')
  if (!sessionId && typeof window !== 'undefined') {
    sessionId = 'session_' + Math.random().toString(36).substring(2, 15)
    const newUrl = new URL(url)
    newUrl.searchParams.set('session_id', sessionId)
    window.history.replaceState({}, '', newUrl.toString())
  }
  cachedSessionId = sessionId || 'default'
  return cachedSessionId
}

export function updateSessionIdHeader(sessionId: string): void {
  cachedSessionId = sessionId
}

function createApi() {
  return axios.create({
    baseURL: '/api',
    timeout: 30000,
    headers: {
      'X-Session-ID': getSessionId()
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

export async function submitChoice(choiceIndex: number): Promise<void> {
  await createApi().post('/choice', { choice_index: choiceIndex })
}