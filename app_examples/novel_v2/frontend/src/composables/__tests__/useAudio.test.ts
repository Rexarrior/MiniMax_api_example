import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useAudio } from '../useAudio'

// Create mock functions outside to ensure they're shared
const mockPlayMusic = vi.fn()
const mockStopMusic = vi.fn()
const mockStopAll = vi.fn()

// Mock the audio store
vi.mock('../../stores/audioStore', () => ({
  useAudioStore: () => ({
    isMuted: false,
    musicVolume: 0.7,
    voiceVolume: 1.0,
    currentMusic: null,
    isMusicPlaying: false,
    playMusic: mockPlayMusic,
    playVoice: vi.fn(),
    stopMusic: mockStopMusic,
    stopVoice: vi.fn(),
    setMusicVolume: vi.fn(),
    setVoiceVolume: vi.fn(),
    toggleMute: vi.fn(),
    stopAll: mockStopAll,
  }),
}))

describe('useAudio', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should return audio state from store', () => {
    const { isMuted, musicVolume, voiceVolume } = useAudio()
    
    expect(isMuted.value).toBe(false)
    expect(musicVolume.value).toBe(0.7)
    expect(voiceVolume.value).toBe(1.0)
  })

  it('should play background music via store', () => {
    const { playBackgroundMusic } = useAudio()
    
    playBackgroundMusic('test.mp3')
    
    expect(mockPlayMusic).toHaveBeenCalledWith('test.mp3', true)
  })

  it('should stop all audio via store', () => {
    const { stopAll } = useAudio()
    
    stopAll()
    
    expect(mockStopAll).toHaveBeenCalled()
  })
})