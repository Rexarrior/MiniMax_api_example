import { fetchScene, pollScene, submitChoice, startGame } from '@/api/novelApi'
import type { Scene } from '@/types/novel'

export function useNovelApi() {
  async function getScene(): Promise<Scene> {
    return fetchScene()
  }

  async function poll(lastTimestamp: number): Promise<{ scene: Scene | null; timestamp: number }> {
    return pollScene(lastTimestamp)
  }

  async function choose(choiceIndex: number): Promise<void> {
    return submitChoice(choiceIndex)
  }

  async function start(storyId: string): Promise<Scene> {
    const response = await startGame(storyId)
    return response.scene
  }

  return {
    getScene,
    poll,
    choose,
    start
  }
}