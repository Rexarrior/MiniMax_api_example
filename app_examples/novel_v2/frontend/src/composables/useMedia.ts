import { ref } from 'vue'

export function useMedia() {
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  function preloadImage(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = () => resolve()
      img.onerror = () => reject(new Error(`Failed to load image: ${url}`))
      img.src = url
    })
  }
  
  function preloadAudio(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const audio = new Audio()
      audio.oncanplaythrough = () => resolve()
      audio.onerror = () => reject(new Error(`Failed to load audio: ${url}`))
      audio.src = url
      audio.load()
    })
  }
  
  async function preloadMedia(urls: string[]): Promise<{ successful: string[]; failed: string[] }> {
    isLoading.value = true
    error.value = null

    const successful: string[] = []
    const failed: string[] = []

    const results = await Promise.allSettled(
      urls.map(async (url) => {
        try {
          if (url.match(/\.(jpg|jpeg|png|webp|gif)$/i)) {
            await preloadImage(url)
          } else if (url.match(/\.(mp3|ogg|wav)$/i)) {
            await preloadAudio(url)
          } else {
            // Unsupported file type - this is not an error, just skip it
            // Videos and other types are not preloaded by this function
            console.warn(`Unsupported media type for preloading: ${url}`)
            return // Early return for unsupported types
          }
          successful.push(url)
        } catch (e) {
          failed.push(url)
          throw e // Re-throw so Promise.allSettled captures the rejection
        }
      })
    )

    // Check for failures
    const errors = results
      .filter((r): r is PromiseRejectedResult => r.status === 'rejected')
      .map(r => r.reason?.message || 'Unknown error')

    if (errors.length > 0) {
      error.value = `Failed to preload ${errors.length} media file(s): ${errors.join(', ')}`
    }

    isLoading.value = false
    return { successful, failed }
  }
  
  return {
    isLoading,
    error,
    preloadImage,
    preloadAudio,
    preloadMedia,
  }
}