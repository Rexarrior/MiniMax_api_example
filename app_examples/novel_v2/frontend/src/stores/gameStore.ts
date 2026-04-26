import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Scene, GameState, DialogueLine } from '../types/novel'
import { novelApi } from '../api/novelApi'
import { useSettingsStore } from './settingsStore'

export const useGameStore = defineStore('game', () => {
  // State
  const status = ref<GameState['status']>('idle')
  const sessionId = ref<string | null>(null)
  const storyId = ref<string | null>(null)
  const currentScene = ref<Scene | null>(null)
  const dialogueIndex = ref(0)
  const error = ref<string | null>(null)

  // Computed
  const isPlaying = computed(() => status.value === 'playing')
  const isLoading = computed(() => status.value === 'loading')
  const isEnding = computed(() => currentScene.value?.is_ending ?? false)

  const currentDialogue = computed<DialogueLine | null>(() => {
    if (!currentScene.value || dialogueIndex.value >= currentScene.value.dialogues.length) {
      return null
    }
    return currentScene.value.dialogues[dialogueIndex.value]
  })

  const hasChoices = computed(() => {
    return currentScene.value?.choices && currentScene.value.choices.length > 0
  })

  const isDialogueComplete = computed(() => {
    if (!currentScene.value) return true
    return dialogueIndex.value >= currentScene.value.dialogues.length
  })

  // Helper to get current language
  function getLanguage() {
    return useSettingsStore().language
  }

  // Actions
  async function startGame(newStoryId: string) {
    status.value = 'loading'
    error.value = null
    try {
      const lang = getLanguage()
      const session = await novelApi.startGame({ story_id: newStoryId, language: lang })
      sessionId.value = session.session_id
      storyId.value = newStoryId

      // Fetch initial scene with current language
      const scene = await novelApi.getScene(session.session_id, lang)
      currentScene.value = scene
      dialogueIndex.value = 0
      status.value = 'playing'
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to start game'
      status.value = 'error'
    }
  }

  async function refreshScene() {
    if (!sessionId.value) return
    try {
      const scene = await novelApi.getScene(sessionId.value, getLanguage())
      currentScene.value = scene
      // Always reset dialogueIndex when loading a new scene
      dialogueIndex.value = 0
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to refresh scene'
    }
  }

  async function makeChoice(choiceIndex: number) {
    if (!hasChoices.value) return
    status.value = 'loading'
    error.value = null
    try {
      const session = await novelApi.makeChoice(choiceIndex)
      const scene = await novelApi.getScene(session.session_id, getLanguage())
      currentScene.value = scene
      dialogueIndex.value = 0
      status.value = scene.is_ending ? 'ending' : 'playing'
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to make choice'
      status.value = 'error'
    }
  }

  async function advanceDialogue() {
    if (!sessionId.value) return

    try {
      const session = await novelApi.advanceDialogue()

      // Check if scene changed (server transitioned to new scene)
      if (session.current_scene_id !== currentScene.value?.scene_id) {
        // Scene changed - fetch new scene data
        await refreshScene()
        return
      }

      // Same scene - increment local dialogue index
      if (dialogueIndex.value < (currentScene.value?.dialogues.length ?? 0) - 1) {
        dialogueIndex.value++
      } else if (!currentScene.value?.choices || currentScene.value.choices.length === 0) {
        // No more dialogues and no choices - this is an ending
        status.value = 'ending'
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to advance dialogue'
    }
  }

  function nextDialogue() {
    if (dialogueIndex.value < (currentScene.value?.dialogues.length ?? 0)) {
      dialogueIndex.value++
    }
  }

  function resetGame() {
    status.value = 'idle'
    sessionId.value = null
    storyId.value = null
    currentScene.value = null
    dialogueIndex.value = 0
    error.value = null
    localStorage.removeItem('session_id')
  }

  return {
    // State
    status,
    sessionId,
    storyId,
    currentScene,
    dialogueIndex,
    error,
    // Computed
    isPlaying,
    isLoading,
    isEnding,
    currentDialogue,
    hasChoices,
    isDialogueComplete,
    // Actions
    startGame,
    refreshScene,
    makeChoice,
    advanceDialogue,
    nextDialogue,
    resetGame,
  }
})
