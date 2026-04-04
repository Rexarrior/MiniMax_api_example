<template>
  <div class="relative w-full h-full">
    <BackgroundLayer :url="gameStore.currentScene?.background_url" />
    <CharacterSprite :url="characterImage" />

    <SoundPromptModal
      v-if="showSoundPrompt"
      @enable="handleEnableSound"
      @disable="handleDisableSound"
    />

    <router-view
      v-if="!showSoundPrompt"
      class="relative z-10"
    />

    <AudioControls
      v-if="audioStore.soundEnabled && !showSoundPrompt"
      :is-muted="audioStore.isMuted"
      @toggle="audioStore.toggleMute"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import BackgroundLayer from '@/components/BackgroundLayer.vue'
import CharacterSprite from '@/components/CharacterSprite.vue'
import SoundPromptModal from '@/components/SoundPromptModal.vue'
import AudioControls from '@/components/AudioControls.vue'
import { useGameStore } from '@/stores/gameStore'
import { useAudioStore } from '@/stores/audioStore'

const gameStore = useGameStore()
const audioStore = useAudioStore()

const showSoundPrompt = ref(true)
const characterImage = ref<string | undefined>(undefined)

watch(() => gameStore.currentScene, (scene) => {
  if (scene?.current_character_image_url) {
    characterImage.value = scene.current_character_image_url
  }
  if (scene?.music_url) {
    audioStore.playMusic(scene.music_url)
  }
}, { immediate: true })

function handleEnableSound() {
  audioStore.enableSound()
  showSoundPrompt.value = false
  if (gameStore.currentScene?.music_url) {
    audioStore.playMusic(gameStore.currentScene.music_url)
  }
}

function handleDisableSound() {
  audioStore.disableSound()
  showSoundPrompt.value = false
}
</script>