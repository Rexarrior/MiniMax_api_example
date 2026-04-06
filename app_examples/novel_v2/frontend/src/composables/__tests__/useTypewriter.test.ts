import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { useTypewriter } from '../useTypewriter'

// Mock settings store
vi.mock('../../stores/settingsStore', () => ({
  useSettingsStore: () => ({
    cps: 50,
  }),
}))

describe('useTypewriter', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('should initialize with empty text', () => {
    const { displayText, isTyping, fullText } = useTypewriter()
    
    expect(displayText.value).toBe('')
    expect(isTyping.value).toBe(false)
    expect(fullText.value).toBe('')
  })

  it('should start typing text', () => {
    const { startTyping, displayText, isTyping, fullText } = useTypewriter()
    
    startTyping('Hello')
    
    expect(fullText.value).toBe('Hello')
    expect(isTyping.value).toBe(true)
  })

  it('should skip to end', () => {
    const { startTyping, skipToEnd, displayText, isTyping } = useTypewriter()
    
    startTyping('Hello World')
    skipToEnd()
    
    expect(displayText.value).toBe('Hello World')
    expect(isTyping.value).toBe(false)
  })

  it('should reset state', () => {
    const { startTyping, reset, displayText, fullText, currentIndex } = useTypewriter()
    
    startTyping('Hello')
    reset()
    
    expect(displayText.value).toBe('')
    expect(fullText.value).toBe('')
    expect(currentIndex.value).toBe(0)
  })
})