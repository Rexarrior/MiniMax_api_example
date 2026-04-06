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

  // Crossfade duration in seconds
  const CROSSFADE_DURATION = 1.5

  // Computed
  const effectiveMusicVolume = computed(() => isMuted.value ? 0 : musicVolume.value)
  const effectiveVoiceVolume = computed(() => isMuted.value ? 0 : voiceVolume.value)

  // Actions
  function playMusic(url: string, fadeIn = true) {
    if (!url) return
    
    // If same music is playing, don't restart
    if (currentMusic.value === url && currentMusicHowl && isMusicPlaying.value) {
      return
    }

    // Fade out current music
    if (currentMusicHowl && isMusicPlaying.value) {
      const oldHowl = currentMusicHowl
      if (fadeIn) {
        // Start fading out
        const fadeStep = 0.1
        const steps = CROSSFADE_DURATION * 10
        let currentStep = 0
        const interval = setInterval(() => {
          currentStep++
          oldHowl.volume(effectiveMusicVolume.value * (1 - currentStep / steps))
          if (currentStep >= steps) {
            clearInterval(interval)
            oldHowl.stop()
          }
        }, 100)
      } else {
        oldHowl.stop()
      }
    }

    // Create new music instance
    currentMusicHowl = new Howl({
      src: [url],
      volume: fadeIn ? 0 : effectiveMusicVolume.value,
      loop: true,
      onplay: () => {
        isMusicPlaying.value = true
        currentMusic.value = url
        
        // Fade in
        if (fadeIn) {
          const fadeStep = 0.1
          const steps = CROSSFADE_DURATION * 10
          let currentStep = 0
          const interval = setInterval(() => {
            currentStep++
            currentMusicHowl!.volume(effectiveMusicVolume.value * (currentStep / steps))
            if (currentStep >= steps) {
              clearInterval(interval)
            }
          }, 100)
        }
      },
      onend: () => {
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
    if (currentMusicHowl) {
      currentMusicHowl.stop()
      currentMusicHowl = null
    }
    currentMusic.value = null
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
