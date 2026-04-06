<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useGameStore } from '../../stores/gameStore'
import { useGame } from '../../composables/useGame'
import { useTypewriter } from '../../composables/useTypewriter'
import BackgroundLayer from '../media/BackgroundLayer.vue'
import CharacterSprite from '../media/CharacterSprite.vue'
import DialogueBox from './DialogueBox.vue'
import ChoiceMenu from './ChoiceMenu.vue'
import TypewriterText from './TypewriterText.vue'
import SpeakerName from './SpeakerName.vue'
import AudioControls from '../media/AudioControls.vue'
import SoundPromptModal from '../ui/SoundPromptModal.vue'
import { storeToRefs } from 'pinia'

const route = useRoute()
const gameStore = useGameStore()
const { currentDialogue, currentScene, hasChoices, isDialogueComplete } = storeToRefs(gameStore)

const { startStory } = useGame()
const { displayText, isTyping, startTyping, skipToEnd } = useTypewriter()

const showSoundPrompt = ref(true)

onMounted(async () => {
  const storyId = route.params.storyId as string
  if (storyId && !gameStore.isPlaying) {
    await startStory(storyId)
  }
})

watch(currentDialogue, (dialogue) => {
  if (dialogue) {
    startTyping(dialogue.text)
  }
}, { immediate: true })

function handleClick() {
  if (isTyping.value) {
    skipToEnd()
  } else if (hasChoices.value && isDialogueComplete.value) {
    // Wait for choice
  } else if (!isDialogueComplete.value) {
    gameStore.nextDialogue()
  } else if (!hasChoices.value) {
    gameStore.advanceDialogue()
  }
}

function handleChoice(index: number) {
  gameStore.makeChoice(index)
}

function handleSoundEnable() {
  showSoundPrompt.value = false
}

function handleSoundSkip() {
  showSoundPrompt.value = false
}
</script>

<template>
  <div 
    class="game-screen min-h-screen relative overflow-hidden bg-black"
    @click="handleClick"
  >
    <SoundPromptModal 
      v-if="showSoundPrompt"
      @enable="handleSoundEnable"
      @skip="handleSoundSkip"
    />

    <BackgroundLayer 
      :imageUrl="currentScene?.background_url ?? null"
      :videoUrl="currentScene?.background_video_url ?? null"
    />

    <CharacterSprite 
      v-if="currentDialogue?.character_image_url"
      :imageUrl="currentDialogue.character_image_url"
    />

    <AudioControls class="absolute top-4 right-4 z-30" />

    <div 
      v-if="currentScene?.title"
      class="absolute top-4 left-4 text-white text-xl font-semibold text-shadow"
    >
      {{ currentScene.title }}
    </div>

    <div class="absolute bottom-0 left-0 right-0">
      <SpeakerName 
        v-if="currentDialogue && currentDialogue.speaker !== 'narrator'"
        :name="currentDialogue.speaker"
      />

      <DialogueBox>
        <TypewriterText 
          :text="displayText"
          :isTyping="isTyping"
        />
        
        <ChoiceMenu 
          v-if="hasChoices && isDialogueComplete"
          :choices="currentScene?.choices ?? []"
          @select="handleChoice"
        />
        

        
        <div 
          v-if="!hasChoices && !isTyping && !isDialogueComplete"
          class="text-center text-gray-400 text-sm mt-2 animate-pulse"
        >
          Click to continue...
        </div>
      </DialogueBox>
    </div>
  </div>
</template>
