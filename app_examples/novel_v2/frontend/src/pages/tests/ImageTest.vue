<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { novelApi } from '../../api/novelApi'
import type { Story, Scene } from '../../types/novel'

const stories = ref<Story[]>([])
const selectedStoryId = ref<string>('')
const scene = ref<Scene | null>(null)
const sessionId = ref<string | null>(null)
const error = ref<string>('')
const loading = ref(false)
const rawSceneData = ref<string>('')

const API_BASE = window.location.origin + '/api'

onMounted(async () => {
  try {
    stories.value = await novelApi.listStories()
    if (stories.value.length > 0) {
      selectedStoryId.value = stories.value[0].id
      // Auto-load first scene
      await loadScene()
    }
  } catch (e) {
    error.value = `Failed to load stories: ${e}`
  }
})

async function loadScene() {
  if (!selectedStoryId.value) return
  loading.value = true
  error.value = ''
  try {
    const session = await novelApi.startGame({ story_id: selectedStoryId.value })
    sessionId.value = session.session_id
    const sceneData = await novelApi.getScene(session.session_id)
    scene.value = sceneData
    rawSceneData.value = JSON.stringify(sceneData, null, 2)
  } catch (e) {
    error.value = `Failed to load scene: ${e}`
  } finally {
    loading.value = false
  }
}

function getImageUrl(path: string): string {
  if (!path) return ''
  if (path.startsWith('http')) return path
  // path is like /api/media/demo/assets/images/bg_xxx.jpeg
  return window.location.origin + path
}
</script>

<template>
  <div class="test-page">
    <h1>Image Asset Test</h1>

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
      <button @click="loadScene" :disabled="!selectedStoryId || loading">
        {{ loading ? 'Loading...' : 'Load Scene' }}
      </button>
    </div>

    <div class="assets-display" v-if="scene">
      <h2>Background Image</h2>
      <div class="image-container">
        <img
          v-if="scene.background_url"
          :src="getImageUrl(scene.background_url)"
          alt="Background"
          @error="(e) => (e.target as HTMLImageElement).style.display = 'none'"
        />
        <p v-else class="no-asset">No background image</p>
        <p class="url-display">URL: {{ scene.background_url || 'N/A' }}</p>
      </div>

      <h2>Character Image</h2>
      <div class="image-container">
        <img
          v-if="scene.current_character_image_url"
          :src="getImageUrl(scene.current_character_image_url)"
          alt="Character"
          @error="(e) => (e.target as HTMLImageElement).style.display = 'none'"
        />
        <p v-else class="no-asset">No character image</p>
        <p class="url-display">URL: {{ scene.current_character_image_url || 'N/A' }}</p>
      </div>
    </div>

    <div class="raw-data" v-if="rawSceneData">
      <h2>Raw Scene Data (JSON)</h2>
      <pre>{{ rawSceneData }}</pre>
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

.assets-display {
  margin-bottom: 30px;
}

.image-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin: 10px 0;
  background: #f9f9f9;
}

.image-container img {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
}

.no-asset {
  color: #888;
  font-style: italic;
}

.url-display {
  font-size: 12px;
  color: #666;
  word-break: break-all;
  margin-top: 10px;
}

.raw-data pre {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 20px;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 12px;
}
</style>
