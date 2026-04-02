import { ref, onUnmounted } from 'vue'

export function usePolling(callback: () => Promise<void>, interval = 500) {
  const isPolling = ref(false)
  let timerId: ReturnType<typeof setInterval> | null = null

  function start() {
    if (isPolling.value) return
    isPolling.value = true
    timerId = setInterval(callback, interval)
  }

  function stop() {
    isPolling.value = false
    if (timerId !== null) {
      clearInterval(timerId)
      timerId = null
    }
  }

  onUnmounted(() => {
    stop()
  })

  return {
    isPolling,
    start,
    stop
  }
}