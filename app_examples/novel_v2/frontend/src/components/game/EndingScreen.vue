<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useGameStore } from '../../stores/gameStore'
import { storeToRefs } from 'pinia'

const router = useRouter()
const gameStore = useGameStore()
const { currentScene } = storeToRefs(gameStore)

function goToTitle() {
  gameStore.resetGame()
  router.push({ name: 'Title' })
}

function replayStory() {
  const storyId = gameStore.storyId
  gameStore.resetGame()
  if (storyId) {
    gameStore.startGame(storyId)
    router.push({ name: 'Game', params: { storyId } })
  }
}
</script>

<template>
  <div class="ending-screen min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-gray-900 to-black p-8">
    <div class="text-center max-w-2xl">
      <h1 class="text-5xl font-bold text-purple-400 mb-4 text-shadow">
        The End
      </h1>
      
      <p v-if="currentScene?.title" class="text-2xl text-gray-300 mb-8">
        {{ currentScene.title }}
      </p>

      <div class="novel-card mb-12">
        <p class="text-xl text-gray-300 italic">
          Thank you for playing!
        </p>
      </div>

      <div class="flex gap-4 justify-center">
        <button 
          @click="replayStory"
          class="novel-button"
        >
          Play Again
        </button>
        <button 
          @click="goToTitle"
          class="novel-button-secondary"
        >
          Back to Title
        </button>
      </div>
    </div>
  </div>
</template>
