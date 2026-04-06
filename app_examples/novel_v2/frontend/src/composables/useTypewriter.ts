import { ref, computed, watch, onUnmounted } from 'vue'
import { useSettingsStore } from '../stores/settingsStore'

export function useTypewriter() {
  const settingsStore = useSettingsStore()
  
  const displayText = ref('')
  const isTyping = ref(false)
  const currentIndex = ref(0)
  const fullText = ref('')
  
  let animationFrame: number | null = null
  let lastTime = 0
  
  const charDelay = computed(() => 1000 / settingsStore.cps)
  
  function startTyping(text: string) {
    stopTyping()
    fullText.value = text
    displayText.value = ''
    currentIndex.value = 0
    isTyping.value = true
    lastTime = performance.now()
    tick()
  }
  
  function tick() {
    if (!isTyping.value) return
    
    const now = performance.now()
    const elapsed = now - lastTime
    
    if (elapsed >= charDelay.value) {
      if (currentIndex.value < fullText.value.length) {
        displayText.value += fullText.value[currentIndex.value]
        currentIndex.value++
        lastTime = now
      } else {
        isTyping.value = false
        return
      }
    }
    
    animationFrame = requestAnimationFrame(tick)
  }
  
  function stopTyping() {
    if (animationFrame !== null) {
      cancelAnimationFrame(animationFrame)
      animationFrame = null
    }
    isTyping.value = false
  }
  
  function skipToEnd() {
    stopTyping()
    displayText.value = fullText.value
    currentIndex.value = fullText.value.length
  }
  
  function reset() {
    stopTyping()
    displayText.value = ''
    fullText.value = ''
    currentIndex.value = 0
  }
  
  onUnmounted(() => {
    stopTyping()
  })
  
  return {
    displayText,
    isTyping,
    currentIndex,
    fullText,
    startTyping,
    stopTyping,
    skipToEnd,
    reset,
  }
}