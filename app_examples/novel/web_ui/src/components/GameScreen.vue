<template>
  <div class="min-h-screen flex flex-col items-center justify-end pb-24 px-4 relative">
    <div v-if="isLoading" class="text-white text-xl">Loading...</div>
    <DialogueBox
      v-else-if="currentDialogue && !showChoices"
      :speaker="currentDialogue.speaker"
      :text="currentDialogue.text"
      :displayed-text="displayedText"
      :is-typing="isTyping"
      :has-more="hasNextDialogue"
      @advance="handleAdvance"
    />
    <ChoiceMenu
      v-if="showChoices"
      :choices="gameStore.currentScene?.choices || []"
      @select="handleSelectChoice"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, watch, ref, onMounted, onUnmounted } from 'vue'
import DialogueBox from './DialogueBox.vue'
import ChoiceMenu from './ChoiceMenu.vue'
import { useGameStore } from '@/stores/gameStore'
import { useAudioStore } from '@/stores/audioStore'

const gameStore = useGameStore()
const audioStore = useAudioStore()

const showChoices = ref(false)
const isLoading = ref(true)

let displayedText = ref('')
let isTyping = ref(false)
let typeTimer: ReturnType<typeof setTimeout> | null = null
let pollTimer: ReturnType<typeof setInterval> | null = null

const currentDialogue = computed(() => {
  return gameStore.dialogues[gameStore.currentDialogueIndex] || null
})

const hasNextDialogue = computed(() => {
  return gameStore.currentDialogueIndex < gameStore.dialogues.length - 1
})

async function fetchScene() {
  try {
    const response = await fetch('/api/scene')
    const data = await response.json()
    if (data.dialogues && data.dialogues.length > 0) {
      gameStore.setScene(data)
      isLoading.value = false
      if (pollTimer) {
        clearInterval(pollTimer)
        pollTimer = null
      }
    }
  } catch (err) {
    console.error('Failed to fetch scene:', err)
  }
}

function startPolling() {
  pollTimer = setInterval(fetchScene, 500)
}

function typeText(text: string, voiceUrl?: string) {
  if (typeTimer) clearTimeout(typeTimer)
  displayedText.value = ''
  isTyping.value = true
  let index = 0
  
  function type() {
    if (index < text.length) {
      displayedText.value += text[index]
      index++
      typeTimer = setTimeout(type, 30)
    } else {
      isTyping.value = false
    }
  }
  
  if (voiceUrl) {
    audioStore.playVoice(voiceUrl).finally(() => {
      type()
    })
  } else {
    type()
  }
}

watch(currentDialogue, (dialogue) => {
  if (dialogue) {
    showChoices.value = false
    typeText(dialogue.text, dialogue.voice_url)
  }
}, { immediate: true })

watch(() => gameStore.currentScene, (scene) => {
  if (scene && scene.dialogues && scene.dialogues.length > 0) {
    isLoading.value = false
  }
}, { immediate: true })

onMounted(() => {
  fetchScene()
  startPolling()
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
  if (typeTimer) clearTimeout(typeTimer)
})

function handleAdvance() {
  if (isTyping.value) {
    if (typeTimer) clearTimeout(typeTimer)
    displayedText.value = currentDialogue.value?.text || ''
    isTyping.value = false
  } else if (hasNextDialogue.value) {
    gameStore.nextDialogue()
  } else if ((gameStore.currentScene?.choices?.length || 0) > 0) {
    showChoices.value = true
  }
}

async function handleSelectChoice(index: number) {
  showChoices.value = false
  try {
    await fetch('/api/choice', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ choice_index: index })
    })
  } catch (e) {
    console.error('Failed to submit choice:', e)
  }
}
</script>