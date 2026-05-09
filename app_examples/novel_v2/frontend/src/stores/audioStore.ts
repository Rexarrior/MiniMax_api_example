import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { Howl } from 'howler'

export const useAudioStore = defineStore('audio', () => {
  // State
  const isMuted = ref(false)
  const musicVolume = ref(0.7)
  const voiceVolume = ref(1.0)
  const sfxVolume = ref(0.8)
  const currentMusic = ref<string | null>(null)
  const isMusicPlaying = ref(false)

  // Howl instances
  let currentMusicHowl: Howl | null = null
  let currentVoiceHowl: Howl | null = null

  // Track pending music URL to prevent race conditions
  let pendingMusicUrl: string | null = null

  // Store fade intervals so they can be cleared
  let fadeInterval: ReturnType<typeof setInterval> | null = null

  // Crossfade duration in seconds
  const CROSSFADE_DURATION = 1.5

  // Computed
  const effectiveMusicVolume = computed(() => isMuted.value ? 0 : musicVolume.value)
  const effectiveVoiceVolume = computed(() => isMuted.value ? 0 : voiceVolume.value)

  function clearFadeInterval() {
    if (fadeInterval !== null) {
      clearInterval(fadeInterval)
      fadeInterval = null
    }
  }

  // Actions
  function playMusic(url: string, fadeIn = true) {
    if (!url) return

    // If same music is playing or pending, don't restart
    if ((currentMusic.value === url || pendingMusicUrl === url) && currentMusicHowl && isMusicPlaying.value) {
      return
    }

    // Stop any existing fade interval
    clearFadeInterval()

    // Fade out current music
    if (currentMusicHowl && isMusicPlaying.value) {
      const oldHowl = currentMusicHowl
      if (fadeIn) {
        // Start fading out
        const steps = CROSSFADE_DURATION * 10
        let currentStep = 0
        fadeInterval = setInterval(() => {
          currentStep++
          oldHowl.volume(effectiveMusicVolume.value * (1 - currentStep / steps))
          if (currentStep >= steps) {
            clearFadeInterval()
            oldHowl.stop()
          }
        }, 100)
      } else {
        oldHowl.stop()
      }
    }

    // Mark this URL as pending
    pendingMusicUrl = url

    // Create new music instance
    currentMusicHowl = new Howl({
      src: [url],
      volume: fadeIn ? 0 : effectiveMusicVolume.value,
      loop: true,
      onplay: () => {
        isMusicPlaying.value = true
        currentMusic.value = url
        pendingMusicUrl = null

        // Fade in
        if (fadeIn) {
          const steps = CROSSFADE_DURATION * 10
          let currentStep = 0
          fadeInterval = setInterval(() => {
            currentStep++
            if (currentMusicHowl) {
              currentMusicHowl.volume(effectiveMusicVolume.value * (currentStep / steps))
            }
            if (currentStep >= steps) {
              clearFadeInterval()
            }
          }, 100)
        }
      },
      onend: () => {
        isMusicPlaying.value = false
      },
      onloaderror: () => {
        // Clean up on error
        pendingMusicUrl = null
        isMusicPlaying.value = false
      },
    })

    currentMusicHowl.play()
  }

  function playVoice(url: string) {
    if (!url || isMuted.value) return

    // Stop any current voice
    if (currentVoiceHowl) {
      currentVoiceHowl.stop()
    }

    currentVoiceHowl = new Howl({
      src: [url],
      volume: effectiveVoiceVolume.value,
      onend: () => {
        currentVoiceHowl = null
      },
    })

    currentVoiceHowl.play()
  }

  function stopMusic() {
    clearFadeInterval()
    if (currentMusicHowl) {
      currentMusicHowl.stop()
      currentMusicHowl = null
    }
    currentMusic.value = null
    pendingMusicUrl = null
    isMusicPlaying.value = false
  }

  function stopVoice() {
    if (currentVoiceHowl) {
      currentVoiceHowl.stop()
      currentVoiceHowl = null
    }
  }

  function setMusicVolume(volume: number) {
    musicVolume.value = Math.max(0, Math.min(1, volume))
    if (currentMusicHowl) {
      currentMusicHowl.volume(effectiveMusicVolume.value)
    }
  }

  function setVoiceVolume(volume: number) {
    voiceVolume.value = Math.max(0, Math.min(1, volume))
  }

  function setSfxVolume(volume: number) {
    sfxVolume.value = Math.max(0, Math.min(1, volume))
  }

  function toggleMute() {
    isMuted.value = !isMuted.value
    if (currentMusicHowl) {
      currentMusicHowl.volume(effectiveMusicVolume.value)
    }
  }

  function stopAll() {
    stopMusic()
    stopVoice()
  }

  return {
    // State
    isMuted,
    musicVolume,
    voiceVolume,
    sfxVolume,
    currentMusic,
    isMusicPlaying,
    // Computed
    effectiveMusicVolume,
    effectiveVoiceVolume,
    // Actions
    playMusic,
    playVoice,
    stopMusic,
    stopVoice,
    setMusicVolume,
    setVoiceVolume,
    setSfxVolume,
    toggleMute,
    stopAll,
  }
})
