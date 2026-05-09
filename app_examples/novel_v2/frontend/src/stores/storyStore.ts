import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Story } from '../types/novel'
import { novelApi } from '../api/novelApi'

export const useStoryStore = defineStore('story', () => {
  // State
  const stories = ref<Story[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const storyCount = computed(() => stories.value.length)

  // Actions
  async function fetchStories(retries = 3, delay = 1000) {
    isLoading.value = true
    error.value = null
    let lastError: Error | null = null

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        stories.value = await novelApi.listStories()
        isLoading.value = false
        return
      } catch (e) {
        lastError = e instanceof Error ? e : new Error('Failed to fetch stories')
        if (attempt < retries) {
          // Exponential backoff: 1s, 2s, 4s
          await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, attempt)))
        }
      }
    }

    error.value = lastError?.message ?? 'Failed to fetch stories'
    isLoading.value = false
  }

  function getStoryById(id: string): Story | undefined {
    return stories.value.find(s => s.id === id)
  }

  return {
    // State
    stories,
    isLoading,
    error,
    // Computed
    storyCount,
    // Actions
    fetchStories,
    getStoryById,
  }
})
