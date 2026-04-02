<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-dark p-4">
    <h1 class="text-5xl font-bold text-white mb-12 text-center drop-shadow-lg">
      The Mysterious Forest
    </h1>
    <button
      class="px-8 py-4 bg-gradient-primary text-white text-xl font-semibold rounded-xl shadow-lg hover:opacity-90 transition-opacity"
      @click="handleStart"
    >
      Start Game
    </button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useNovelApi } from '@/composables/useNovelApi'

const router = useRouter()
const novelApi = useNovelApi()

async function handleStart() {
  try {
    await novelApi.start('demo')
    router.push('/play')
  } catch (e) {
    console.error('Failed to start game:', e)
  }
}
</script>