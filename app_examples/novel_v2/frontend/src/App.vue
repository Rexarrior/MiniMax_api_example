<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAudioStore } from './stores/audioStore'
import { useGameStore } from './stores/gameStore'

const audioStore = useAudioStore()
const gameStore = useGameStore()

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape' && gameStore.isPlaying) {
    gameStore.resetGame()
  }
  if (e.key === 'm' && e.target === document.body) {
    audioStore.toggleMute()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  audioStore.stopAll()
})
</script>

<template>
  <div id="app" class="novel-app">
    <RouterView />
  </div>
</template>

<style>
.novel-app {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: #000;
}
</style>