<script setup lang="ts">
import { ref } from 'vue'
import { useAudioStore } from '../../stores/audioStore'
import { storeToRefs } from 'pinia'
import SettingsModal from '../ui/SettingsModal.vue'

const audioStore = useAudioStore()
const { isMuted, musicVolume } = storeToRefs(audioStore)

const showSettings = ref(false)
</script>

<template>
  <div class="audio-controls">
    <!-- Settings Button -->
    <button
      @click="showSettings = true"
      class="p-2 bg-black bg-opacity-50 rounded-full text-white hover:bg-opacity-70 transition-colors"
      title="Settings"
    >
      <svg v-if="isMuted" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
      </svg>
      <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
      </svg>
    </button>

    <!-- Volume indicator -->
    <div class="ml-2 text-white text-sm">
      <span v-if="isMuted">Muted</span>
      <span v-else>{{ Math.round(musicVolume * 100) }}%</span>
    </div>

    <!-- Settings Modal -->
    <SettingsModal 
      v-if="showSettings"
      @close="showSettings = false"
    />
  </div>
</template>