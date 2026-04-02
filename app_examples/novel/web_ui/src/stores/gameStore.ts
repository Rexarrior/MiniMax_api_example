import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Scene, Dialogue } from '@/types/novel'

export const useGameStore = defineStore('game', () => {
  const currentScene = ref<Scene | null>(null)
  const dialogues = ref<Dialogue[]>([])
  const currentDialogueIndex = ref(0)
  const isEnding = ref(false)
  const timestamp = ref(0)
  const isLoading = ref(false)

  const currentDialogue = computed(() => {
    return dialogues.value[currentDialogueIndex.value] || null
  })

  const hasNextDialogue = computed(() => {
    return currentDialogueIndex.value < dialogues.value.length - 1
  })

  function setScene(scene: Scene) {
    currentScene.value = scene
    dialogues.value = scene.dialogues || []
    currentDialogueIndex.value = 0
    isEnding.value = scene.is_ending
    timestamp.value = scene.timestamp
  }

  function nextDialogue() {
    if (hasNextDialogue.value) {
      currentDialogueIndex.value++
    }
  }

  function reset() {
    currentScene.value = null
    dialogues.value = []
    currentDialogueIndex.value = 0
    isEnding.value = false
    timestamp.value = 0
  }

  return {
    currentScene,
    dialogues,
    currentDialogueIndex,
    isEnding,
    timestamp,
    isLoading,
    currentDialogue,
    hasNextDialogue,
    setScene,
    nextDialogue,
    reset
  }
})