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
  
  async function preloadMedia(urls: string[]) {
    isLoading.value = true
    error.value = null
    
    try {
      await Promise.all(
        urls.map(async (url) => {
          if (url.match(/\.(jpg|jpeg|png|webp|gif)$/i)) {
            return preloadImage(url)
          } else if (url.match(/\.(mp3|ogg|wav)$/i)) {
            return preloadAudio(url)
          }
        })
      )
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to preload media'
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    isLoading,
    error,
    preloadImage,
    preloadAudio,
    preloadMedia,
  }
}