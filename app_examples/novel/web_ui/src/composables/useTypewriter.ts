import { ref, onUnmounted } from 'vue'

export interface TypewriterOptions {
  speed?: number
  onComplete?: () => void
}

export function useTypewriter(options: TypewriterOptions = {}) {
  const displayedText = ref('')
  const isTyping = ref(false)
  let timeoutId: ReturnType<typeof setTimeout> | null = null

  function typeText(text: string): Promise<void> {
    return new Promise((resolve) => {
      stop()
      displayedText.value = ''
      isTyping.value = true
      let index = 0
      const speed = options.speed ?? 30

      function type() {
        if (index < text.length) {
          displayedText.value += text[index]
          index++
          timeoutId = setTimeout(type, speed)
        } else {
          isTyping.value = false
          options.onComplete?.()
          resolve()
        }
      }

      type()
    })
  }

  function skip() {
    stop()
  }

  function stop() {
    if (timeoutId !== null) {
      clearTimeout(timeoutId)
      timeoutId = null
    }
    isTyping.value = false
  }

  function setText(text: string) {
    displayedText.value = text
  }

  onUnmounted(() => {
    stop()
  })

  return {
    displayedText,
    isTyping,
    typeText,
    skip,
    setText
  }
}