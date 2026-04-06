<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { novelApi } from '../../api/novelApi'
import type { Story } from '../../types/novel'

const stories = ref<Story[]>([])
const selectedStoryId = ref<string>('')
const error = ref<string>('')
const loading = ref(false)
const musicFiles = ref<string[]>([])
const selectedTrack = ref<string>('')
const audioRef = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)

const API_BASE = window.location.origin + '/api'

onMounted(async () => {
  try {
    stories.value = await novelApi.listStories()
    if (stories.value.length > 0) {
      selectedStoryId.value = stories.value[0].id
      await loadMusic()
    }
  } catch (e) {
    error.value = `Failed to load stories: ${e}`
  }
})

async function loadMusic() {
  if (!selectedStoryId.value) return
  loading.value = true
  error.value = ''
  musicFiles.value = []

  try {
    // Start a game session to get scene data with music URL
    const session = await novelApi.startGame({ story_id: selectedStoryId.value })
    const scene = await novelApi.getScene(session.session_id)
    
    if (scene.music_url) {
      // Extract filename from URL
      const urlParts = scene.music_url.split('/')
      const filename = urlParts[urlParts.length - 1]
      musicFiles.value = [filename]
      selectedTrack.value = filename
    }
  } catch (e) {
    error.value = `Error loading music: ${e}`
  } finally {
    loading.value = false
  }
}

const musicUrl = computed(() => {
  if (!selectedTrack.value || !selectedStoryId.value) return ''
  // music_url from API is like /api/media/demo/assets/music/file.mp3
  return window.location.origin + '/api/media/' + selectedStoryId.value + '/assets/music/' + selectedTrack.value
})

function playTrack() {
  if (!audioRef.value) return
  audioRef.value.play()
  isPlaying.value = true
}

function pauseTrack() {
  if (!audioRef.value) return
  audioRef.value.pause()
  isPlaying.value = false
}

function stopTrack() {
  if (!audioRef.value) return
  audioRef.value.pause()
  audioRef.value.currentTime = 0
  isPlaying.value = false
}
</script>

<template>
  <div class="test-page">
    <h1>Music/Soundtrack Test</h1>

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
      <button @click="loadMusic" :disabled="!selectedStoryId || loading">
        {{ loading ? 'Loading...' : 'List Music' }}
      </button>
    </div>

    <div v-if="musicFiles.length > 0" class="music-list">
      <h2>Available Tracks ({{ musicFiles.length }})</h2>
      <div class="track-items">
        <div
          v-for="track in musicFiles"
          :key="track"
          class="track-item"
          :class="{ selected: selectedTrack === track }"
          @click="selectedTrack = track"
        >
          {{ track }}
        </div>
      </div>
    </div>

    <div v-if="selectedTrack" class="music-player">
      <h2>Music Player</h2>
      <p class="url-display">URL: {{ musicUrl }}</p>

      <audio ref="audioRef" :src="musicUrl" @ended="isPlaying = false" />

      <div class="player-controls">
        <button @click="playTrack" :disabled="isPlaying">Play</button>
        <button @click="pauseTrack" :disabled="!isPlaying">Pause</button>
        <button @click="stopTrack">Stop</button>
      </div>

      <div class="player-status">
        Status: {{ isPlaying ? 'Playing' : 'Stopped' }}
      </div>
    </div>

    <div v-if="!loading && musicFiles.length === 0 && selectedStoryId" class="no-music">
      <p>No music files found in this story's assets/music folder.</p>
      <p class="hint">Check if the folder exists at: stories/{{ selectedStoryId }}/assets/music/</p>
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

.music-list {
  margin-bottom: 30px;
}

.track-items {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.track-item {
  padding: 10px 15px;
  background: #f0f0f0;
  border: 2px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
}

.track-item.selected {
  background: #4a90d9;
  color: white;
  border-color: #4a90d9;
}

.music-player {
  margin-top: 20px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}

.url-display {
  font-size: 12px;
  color: #666;
  word-break: break-all;
  margin-bottom: 15px;
}

.player-controls {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.player-controls button {
  padding: 10px 20px;
  background: #2e7d32;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.player-controls button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.player-controls button:nth-child(2) {
  background: #f57c00;
}

.player-controls button:nth-child(3) {
  background: #c62828;
}

.player-status {
  margin-top: 15px;
  font-weight: bold;
}

.no-music {
  color: #888;
  font-style: italic;
}

.hint {
  font-size: 12px;
  color: #999;
}
</style>
