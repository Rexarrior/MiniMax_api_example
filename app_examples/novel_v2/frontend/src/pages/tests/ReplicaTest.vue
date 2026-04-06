<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { novelApi } from '../../api/novelApi'
import type { Story, DialogueLine } from '../../types/novel'

const stories = ref<Story[]>([])
const selectedStoryId = ref<string>('')
const error = ref<string>('')
const loading = ref(false)
const dialogues = ref<DialogueLine[]>([])
const playingIndex = ref<number | null>(null)
const audioRefs = ref<Map<number, HTMLAudioElement>>(new Map())

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

async function loadScene() {
  if (!selectedStoryId.value) return
  loading.value = true
  error.value = ''
  dialogues.value = []

  try {
    const session = await novelApi.startGame({ story_id: selectedStoryId.value })
    const scene = await novelApi.getScene(session.session_id)
    dialogues.value = scene.dialogues
  } catch (e) {
    error.value = `Failed to load scene: ${e}`
  } finally {
    loading.value = false
  }
}

function getVoiceUrl(voicePath: string | null): string | null {
  if (!voicePath) return null
  if (voicePath.startsWith('http')) return voicePath
  return `${API_BASE}/media/${selectedStoryId.value}/${voicePath}`
}

function playVoice(index: number, voiceUrl: string | null) {
  if (!voiceUrl) return

  if (playingIndex.value === index) {
    const audio = audioRefs.value.get(index)
    if (audio) {
      audio.pause()
      audio.currentTime = 0
      playingIndex.value = null
    }
    return
  }

  const audio = new Audio(voiceUrl)
  audioRefs.value.set(index, audio)

  audio.onended = () => {
    playingIndex.value = null
  }

  audio.onerror = () => {
    error.value = `Failed to play voice: ${voiceUrl}`
    playingIndex.value = null
  }

  audio.play()
  playingIndex.value = index
}

function setAudioRef(el: HTMLAudioElement | null, index: number) {
  if (el) {
    audioRefs.value.set(index, el)
  }
}
</script>

<template>
  <div class="test-page">
    <h1>Voice/Replica Audio Test</h1>

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

    <div v-if="dialogues.length > 0" class="dialogues-list">
      <h2>Dialogues ({{ dialogues.length }})</h2>

      <div
        v-for="(dialogue, index) in dialogues"
        :key="index"
        class="dialogue-item"
      >
        <div class="dialogue-header">
          <span class="speaker">{{ dialogue.speaker || 'Narrator' }}</span>
          <button
            v-if="dialogue.voice_url"
            @click="playVoice(index, getVoiceUrl(dialogue.voice_url))"
            :class="{ playing: playingIndex === index }"
          >
            {{ playingIndex === index ? 'Stop' : 'Play Voice' }}
          </button>
          <span v-else class="no-voice">No voice file</span>
        </div>

        <div class="dialogue-text">"{{ dialogue.text }}"</div>

        <div class="dialogue-meta">
          <span v-if="dialogue.mood">Mood: {{ dialogue.mood }}</span>
          <span v-if="dialogue.voice_url">Voice URL: {{ dialogue.voice_url }}</span>
          <span v-else>Voice URL: N/A</span>
        </div>

        <audio
          v-if="dialogue.voice_url"
          :ref="(el) => setAudioRef(el as HTMLAudioElement, index)"
          :src="getVoiceUrl(dialogue.voice_url)"
          style="display: none;"
        />
      </div>
    </div>

    <div v-if="!loading && dialogues.length === 0 && selectedStoryId" class="no-dialogues">
      <p>Click "Load Scene" to fetch dialogues with voice URLs.</p>
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

.dialogues-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dialogue-item {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
}

.dialogue-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.speaker {
  font-weight: bold;
  font-size: 16px;
  min-width: 100px;
}

.dialogue-header button {
  padding: 6px 12px;
  background: #2e7d32;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.dialogue-header button.playing {
  background: #c62828;
}

.dialogue-header button:hover {
  opacity: 0.9;
}

.no-voice {
  color: #888;
  font-size: 12px;
  font-style: italic;
}

.dialogue-text {
  font-size: 15px;
  line-height: 1.5;
  margin-bottom: 10px;
  color: #333;
}

.dialogue-meta {
  display: flex;
  gap: 20px;
  font-size: 11px;
  color: #666;
}

.dialogue-meta span {
  word-break: break-all;
}

.no-dialogues {
  color: #888;
  font-style: italic;
}
</style>
