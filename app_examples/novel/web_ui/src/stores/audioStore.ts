import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAudioStore = defineStore('audio', () => {
  const bgMusic = ref<HTMLAudioElement | null>(null)
  const voiceAudio = ref<HTMLAudioElement | null>(null)
  const isMuted = ref(false)
  const soundEnabled = ref(false)

  function initAudio() {
    bgMusic.value = new Audio()
    bgMusic.value.loop = true
    voiceAudio.value = new Audio()
  }

  function enableSound() {
    if (!bgMusic.value) {
      initAudio()
    }
    soundEnabled.value = true
  }

  function disableSound() {
    soundEnabled.value = false
    stopMusic()
    stopVoice()
  }

  function playMusic(url: string) {
    if (!bgMusic.value) {
      initAudio()
    }
    bgMusic.value!.src = url
    if (soundEnabled.value && !isMuted.value) {
      bgMusic.value!.play().catch(() => {})
    }
  }

  function stopMusic() {
    if (bgMusic.value) {
      bgMusic.value.pause()
      bgMusic.value.currentTime = 0
    }
  }

  function playVoice(url: string): Promise<void> {
    return new Promise((resolve) => {
      if (!voiceAudio.value) {
        initAudio()
      }
      if (!soundEnabled.value || isMuted.value) {
        resolve()
        return
      }
      voiceAudio.value!.src = url
      voiceAudio.value!.onended = () => resolve()
      voiceAudio.value!.onerror = () => resolve()
      voiceAudio.value!.play().catch(() => resolve())
    })
  }

  function stopVoice() {
    if (voiceAudio.value) {
      voiceAudio.value.pause()
      voiceAudio.value.currentTime = 0
    }
  }

  function toggleMute() {
    isMuted.value = !isMuted.value
    if (bgMusic.value) {
      bgMusic.value.muted = isMuted.value
    }
    if (voiceAudio.value) {
      voiceAudio.value.muted = isMuted.value
    }
  }

  return {
    bgMusic,
    voiceAudio,
    isMuted,
    soundEnabled,
    initAudio,
    enableSound,
    disableSound,
    playMusic,
    stopMusic,
    playVoice,
    stopVoice,
    toggleMute
  }
})