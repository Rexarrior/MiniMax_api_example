import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

// Mock the API
vi.mock('../../api/novelApi', () => ({
  novelApi: {
    startGame: vi.fn().mockResolvedValue({
      session_id: 'test-session-123',
      story_id: 'demo',
      current_scene_id: 'intro',
      dialogue_index: 0,
      is_ending: false,
      choices: [],
      dialogues: [
        { speaker: 'narrator', text: 'Hello', mood: null, voice_url: null, character_image_url: null },
        { speaker: 'hero', text: 'World', mood: null, voice_url: null, character_image_url: null }
      ],
    }),
    getScene: vi.fn().mockResolvedValue({
      scene_id: 'intro',
      title: 'Introduction',
      background_url: null,
      background_video_url: null,
      dialogues: [
        { speaker: 'narrator', text: 'Hello', mood: null, voice_url: null, character_image_url: null },
        { speaker: 'hero', text: 'World', mood: null, voice_url: null, character_image_url: null }
      ],
      choices: [],
      is_ending: false,
      music_url: null,
      current_character_image_url: null,
      timestamp: Date.now(),
    }),
    makeChoice: vi.fn().mockResolvedValue({
      session_id: 'test-session-123',
      story_id: 'demo',
      current_scene_id: 'scene1',
      dialogue_index: 0,
      is_ending: false,
    }),
    advanceDialogue: vi.fn().mockResolvedValue({
      session_id: 'test-session-123',
      dialogue_index: 1,
    }),
  },
}))

describe('gameStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('should start with idle status', async () => {
    const { useGameStore } = await import('../gameStore')
    const gameStore = useGameStore()
    
    expect(gameStore.status).toBe('idle')
    expect(gameStore.sessionId).toBeNull()
    expect(gameStore.currentScene).toBeNull()
  })

  it('should start a game session', async () => {
    const { useGameStore } = await import('../gameStore')
    const gameStore = useGameStore()
    
    await gameStore.startGame('demo')
    
    expect(gameStore.status).toBe('playing')
    expect(gameStore.sessionId).toBe('test-session-123')
    expect(gameStore.storyId).toBe('demo')
    expect(gameStore.currentScene).not.toBeNull()
  })

  it('should advance dialogue', async () => {
    const { useGameStore } = await import('../gameStore')
    const gameStore = useGameStore()
    
    await gameStore.startGame('demo')
    const initialIndex = gameStore.dialogueIndex
    
    await gameStore.nextDialogue()
    
    expect(gameStore.dialogueIndex).toBe(initialIndex + 1)
  })

  it('should reset game state', async () => {
    const { useGameStore } = await import('../gameStore')
    const gameStore = useGameStore()
    
    await gameStore.startGame('demo')
    gameStore.resetGame()
    
    expect(gameStore.status).toBe('idle')
    expect(gameStore.sessionId).toBeNull()
    expect(gameStore.storyId).toBeNull()
  })
})