<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-dark p-8">
    <h1 class="text-5xl font-bold text-white mb-12 text-center drop-shadow-lg">
      Visual Novel
    </h1>
    <div v-if="storyStore.isLoading" class="text-white text-xl">
      Loading stories...
    </div>
    <div v-else-if="error" class="text-red-400 text-xl mb-4">
      {{ error }}
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
      <button
        v-for="story in storyStore.stories"
        :key="story.id"
        class="p-6 bg-gradient-to-br from-purple-800 to-indigo-900 rounded-xl shadow-lg hover:opacity-90 hover:scale-105 transition-all text-left"
        @click="handleSelectStory(story.id)"
      >
        <h2 class="text-2xl font-bold text-white mb-2">{{ story.title }}</h2>
        <p class="text-gray-300 text-sm">{{ story.description }}</p>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStoryStore } from '@/stores/storyStore'
import { useNovelApi } from '@/composables/useNovelApi'
import { getSessionId } from '@/api/novelApi'

const router = useRouter()
const storyStore = useStoryStore()
const novelApi = useNovelApi()
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    await storyStore.fetchStories()
  } catch (e) {
    error.value = 'Failed to load stories'
    console.error(e)
  }
})

async function handleSelectStory(storyId: string) {
  try {
    await novelApi.start(storyId)
    router.push({ path: '/play', query: { session_id: getSessionId() } })
  } catch (e) {
    error.value = 'Failed to start game'
    console.error('Failed to start game:', e)
  }
}
</script>