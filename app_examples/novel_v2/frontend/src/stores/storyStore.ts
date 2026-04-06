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
  async function fetchStories() {
    isLoading.value = true
    error.value = null
    try {
      stories.value = await novelApi.listStories()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to fetch stories'
    } finally {
      isLoading.value = false
    }
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
