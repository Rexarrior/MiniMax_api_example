<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { novelApi } from '../../api/novelApi'
import type { Story } from '../../types/novel'

const stories = ref<Story[]>([])
const selectedStoryId = ref<string>('')
const error = ref<string>('')
const loading = ref(false)
const videos = ref<string[]>([])
const selectedVideo = ref<string>('')

const API_BASE = 'http://localhost:8000/api'

onMounted(async () => {
  try {
    stories.value = await novelApi.listStories()
    if (stories.value.length > 0) {
      selectedStoryId.value = stories.value[0].id
    }
  } catch (e) {
    error.value = `Failed to load stories: ${e}`
  }
})

async function loadVideos() {
  if (!selectedStoryId.value) return
  loading.value = true
  error.value = ''
  videos.value = []

  try {
    const response = await fetch(`${API_BASE}/media/${selectedStoryId.value}/videos/`)
    if (response.ok) {
      const text = await response.text()
      const parser = new DOMParser()
      const doc = parser.parseFromString(text, 'text/html')
      const links = doc.querySelectorAll('a')
      videos.value = Array.from(links)
        .map(link => link.href)
        .filter(href => href.endsWith('.mp4') || href.endsWith('.webm') || href.endsWith('.ogg'))
        .map(href => href.split('/').pop() || '')
    } else {
      error.value = `Failed to fetch videos directory: ${response.status}`
    }
  } catch (e) {
    error.value = `Error loading videos: ${e}`
  } finally {
    loading.value = false
  }
}

const videoUrl = computed(() => {
  if (!selectedVideo.value || !selectedStoryId.value) return ''
  return `${API_BASE}/media/${selectedStoryId.value}/videos/${selectedVideo.value}`
})
</script>

<template>
  <div class="test-page">
    <h1>Video Asset Test</h1>

    <div class="error" v-if="error">{{ error }}</div>

    <div class="controls">
      <label>
        Select Story:
        <select v-model="selectedStoryId">
          <option v-for="story in stories" :key="story.id" :value="story.id">
            {{ story.title }}
          </option>
        </select>
      </label>
      <button @click="loadVideos" :disabled="!selectedStoryId || loading">
        {{ loading ? 'Loading...' : 'List Videos' }}
      </button>
    </div>

    <div v-if="videos.length > 0" class="video-list">
      <h2>Available Videos ({{ videos.length }})</h2>
      <div class="video-items">
        <div
          v-for="video in videos"
          :key="video"
          class="video-item"
          :class="{ selected: selectedVideo === video }"
          @click="selectedVideo = video"
        >
          {{ video }}
        </div>
      </div>
    </div>

    <div v-if="selectedVideo" class="video-player">
      <h2>Video Player</h2>
      <p class="url-display">URL: {{ videoUrl }}</p>
      <video :src="videoUrl" controls playsinline style="max-width: 100%;">
        Your browser does not support the video tag.
      </video>
    </div>

    <div v-if="!loading && videos.length === 0 && selectedStoryId" class="no-videos">
      <p>No videos found in this story's assets/videos folder.</p>
      <p class="hint">Check if the folder exists at: stories/{{ selectedStoryId }}/assets/videos/</p>
    </div>
  </div>
</template>

<style scoped>
.test-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.error {
  color: red;
  padding: 10px;
  background: #ffe6e6;
  border-radius: 4px;
  margin-bottom: 20px;
}

.controls {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  align-items: center;
}

.controls select {
  padding: 8px 12px;
  font-size: 14px;
}

.controls button {
  padding: 8px 16px;
  background: #4a90d9;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.controls button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.video-list {
  margin-bottom: 30px;
}

.video-items {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.video-item {
  padding: 10px 15px;
  background: #f0f0f0;
  border: 2px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
}

.video-item.selected {
  background: #4a90d9;
  color: white;
  border-color: #4a90d9;
}

.video-player {
  margin-top: 20px;
}

.url-display {
  font-size: 12px;
  color: #666;
  word-break: break-all;
  margin-bottom: 15px;
}

.no-videos {
  color: #888;
  font-style: italic;
}

.hint {
  font-size: 12px;
  color: #999;
}
</style>
