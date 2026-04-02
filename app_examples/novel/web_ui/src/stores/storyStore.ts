import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Story } from '@/types/novel'
import { getStories } from '@/api/novelApi'

export const useStoryStore = defineStore('story', () => {
  const stories = ref<Story[]>([])
  const currentStoryId = ref<string | null>(null)
  const isLoading = ref(false)

  async function fetchStories() {
    isLoading.value = true
    try {
      stories.value = await getStories()
    } finally {
      isLoading.value = false
    }
  }

  function setCurrentStory(storyId: string) {
    currentStoryId.value = storyId
  }

  return {
    stories,
    currentStoryId,
    isLoading,
    fetchStories,
    setCurrentStory
  }
})