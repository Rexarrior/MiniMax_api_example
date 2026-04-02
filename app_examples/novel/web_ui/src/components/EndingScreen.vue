<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-dark p-4">
    <h2 class="text-4xl font-bold text-white mb-8 text-center">The End</h2>
    <button
      class="px-8 py-4 bg-gradient-primary text-white text-xl font-semibold rounded-xl shadow-lg hover:opacity-90 transition-opacity"
      @click="handleRestart"
    >
      Play Again
    </button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/gameStore'
import { useAudioStore } from '@/stores/audioStore'

const router = useRouter()
const gameStore = useGameStore()
const audioStore = useAudioStore()

function handleRestart() {
  gameStore.reset()
  audioStore.stopMusic()
  router.push('/')
}
</script>