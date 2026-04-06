import { computed } from 'vue'
import { useAudioStore } from '../stores/audioStore'

export function useAudio() {
  const audioStore = useAudioStore()
  
  const isMuted = computed(() => audioStore.isMuted)
  const musicVolume = computed(() => audioStore.musicVolume)
  const voiceVolume = computed(() => audioStore.voiceVolume)
  const currentMusic = computed(() => audioStore.currentMusic)
  const isMusicPlaying = computed(() => audioStore.isMusicPlaying)
  
  function playBackgroundMusic(url: string | null, fadeIn = true) {
    if (url) {
      audioStore.playMusic(url, fadeIn)
    } else {
      audioStore.stopMusic()
    }
  }
  
  function playVoiceLine(url: string | null) {
    if (url) {
      audioStore.playVoice(url)
    }
  }
  
  function setMusicVol(volume: number) {
    audioStore.setMusicVolume(volume)
  }
  
  function setVoiceVol(volume: number) {
    audioStore.setVoiceVolume(volume)
  }
  
  function toggleMuteAll() {
    audioStore.toggleMute()
  }
  
  function stopAll() {
    audioStore.stopAll()
  }
  
  return {
    isMuted,
    musicVolume,
    voiceVolume,
    currentMusic,
    isMusicPlaying,
    playBackgroundMusic,
    playVoiceLine,
    setMusicVol,
    setVoiceVol,
    toggleMuteAll,
    stopAll,
  }
}