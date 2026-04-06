import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

// Mock Howler
vi.mock('howler', () => ({
  Howl: vi.fn().mockImplementation(() => ({
    play: vi.fn(),
    stop: vi.fn(),
    volume: vi.fn(),
    on: vi.fn(),
  })),
}))

describe('audioStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should start with default values', async () => {
    const { useAudioStore } = await import('../audioStore')
    const audioStore = useAudioStore()
    
    expect(audioStore.isMuted).toBe(false)
    expect(audioStore.musicVolume).toBe(0.7)
    expect(audioStore.voiceVolume).toBe(1.0)
    expect(audioStore.sfxVolume).toBe(0.8)
  })

  it('should toggle mute', async () => {
    const { useAudioStore } = await import('../audioStore')
    const audioStore = useAudioStore()
    
    expect(audioStore.isMuted).toBe(false)
    
    audioStore.toggleMute()
    expect(audioStore.isMuted).toBe(true)
    
    audioStore.toggleMute()
    expect(audioStore.isMuted).toBe(false)
  })

  it('should set music volume', async () => {
    const { useAudioStore } = await import('../audioStore')
    const audioStore = useAudioStore()
    
    audioStore.setMusicVolume(0.5)
    expect(audioStore.musicVolume).toBe(0.5)
    
    // Should clamp to valid range
    audioStore.setMusicVolume(1.5)
    expect(audioStore.musicVolume).toBe(1)
    
    audioStore.setMusicVolume(-0.5)
    expect(audioStore.musicVolume).toBe(0)
  })

  it('should compute effective music volume when muted', async () => {
    const { useAudioStore } = await import('../audioStore')
    const audioStore = useAudioStore()
    
    audioStore.setMusicVolume(0.8)
    audioStore.toggleMute()
    
    expect(audioStore.effectiveMusicVolume).toBe(0)
  })
})