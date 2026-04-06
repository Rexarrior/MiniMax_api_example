<script setup lang="ts">
import { onMounted } from 'vue'
import { useStoryStore } from '../../stores/storyStore'
import { useGame } from '../../composables/useGame'
import { storeToRefs } from 'pinia'

const storyStore = useStoryStore()
const { startStory } = useGame()
const { stories, isLoading, error } = storeToRefs(storyStore)

onMounted(async () => {
  await storyStore.fetchStories()
})
</script>

<template>
  <div class="title-screen min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-gray-900 to-black p-8">
    <!-- Logo/Title -->
    <div class="text-center mb-12">
      <h1 class="text-6xl font-bold text-purple-400 mb-4 text-shadow">
        Visual Novel
      </h1>
      <p class="text-gray-400 text-xl">An Interactive Story Experience</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent"></div>
      <p class="mt-4 text-gray-400">Loading stories...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="novel-card text-center max-w-md">
      <p class="text-red-400 mb-4">{{ error }}</p>
      <button @click="storyStore.fetchStories()" class="novel-button">
        Retry
      </button>
    </div>

    <!-- Story List -->
    <div v-else class="novel-card max-w-2xl w-full">
      <h2 class="text-2xl font-semibold mb-6 text-purple-300">Choose Your Story</h2>
      
      <div v-if="stories.length === 0" class="text-center text-gray-500 py-8">
        No stories available
      </div>

      <div v-else class="space-y-4">
        <button
          v-for="story in stories"
          :key="story.id"
          @click="startStory(story.id)"
          class="w-full p-4 bg-gray-800 hover:bg-gray-700 rounded-lg text-left transition-colors group"
        >
          <h3 class="text-xl font-semibold text-white group-hover:text-purple-300 transition-colors">
            {{ story.title }}
          </h3>
          <p class="text-gray-400 text-sm mt-1">{{ story.author }}</p>
          <p class="text-gray-500 text-sm mt-2 line-clamp-2">{{ story.description }}</p>
        </button>
      </div>
    </div>

    <!-- Settings hint -->
    <p class="mt-8 text-gray-600 text-sm">
      Press M to mute/unmute
    </p>
  </div>
</template>
