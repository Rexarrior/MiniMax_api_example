import { computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '../stores/gameStore'
import { useAudioStore } from '../stores/audioStore'
import { useSettingsStore } from '../stores/settingsStore'

export function useGame() {
  const router = useRouter()
  const gameStore = useGameStore()
  const audioStore = useAudioStore()
  const settingsStore = useSettingsStore()
  
  const isPlaying = computed(() => gameStore.isPlaying)
  const currentDialogue = computed(() => gameStore.currentDialogue)
  const currentScene = computed(() => gameStore.currentScene)
  const hasChoices = computed(() => gameStore.hasChoices)
  const isDialogueComplete = computed(() => gameStore.isDialogueComplete)
  const isEnding = computed(() => gameStore.isEnding)
  
  watch(
    () => gameStore.currentScene?.music_url,
    (newMusic) => {
      audioStore.playMusic(newMusic ?? null)
    }
  )
  
  watch(
    () => gameStore.currentDialogue?.voice_url,
    (voiceUrl) => {
      if (settingsStore.voiceEnabled && voiceUrl) {
        audioStore.playVoice(voiceUrl)
      }
    }
  )
  
  async function startStory(storyId: string) {
    await gameStore.startGame(storyId)
    if (gameStore.isPlaying) {
      router.push({ name: 'Game', params: { storyId } })
    }
  }
  
  function selectChoice(index: number) {
    gameStore.makeChoice(index)
  }
  
  function advanceDialogue() {
    if (!gameStore.isDialogueComplete) {
      gameStore.nextDialogue()
    } else if (!gameStore.hasChoices) {
      gameStore.advanceDialogue()
    }
  }
  
  function goToTitle() {
    audioStore.stopAll()
    gameStore.resetGame()
    router.push({ name: 'Title' })
  }
  
  function goToEnding() {
    router.push({ name: 'Ending' })
  }
  
  return {
    isPlaying,
    currentDialogue,
    currentScene,
    hasChoices,
    isDialogueComplete,
    isEnding,
    startStory,
    selectChoice,
    advanceDialogue,
    goToTitle,
    goToEnding,
  }
}