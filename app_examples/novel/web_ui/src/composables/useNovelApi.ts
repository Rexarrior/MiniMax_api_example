import { fetchScene, submitChoice, startGame, updateSessionIdFromResponse } from '@/api/novelApi'
import type { Scene } from '@/types/novel'

export function useNovelApi() {
  async function getScene(): Promise<Scene> {
    return fetchScene()
  }

  async function choose(choiceIndex: number): Promise<Scene> {
    return submitChoice(choiceIndex)
  }

  async function start(storyId: string): Promise<Scene> {
    const response = await startGame(storyId)
    updateSessionIdFromResponse(response.session_id)
    return response as unknown as Scene
  }

  return {
    getScene,
    choose,
    start
  }
}