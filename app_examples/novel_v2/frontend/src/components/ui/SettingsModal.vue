<script setup lang="ts">
import { useSettingsStore } from '../../stores/settingsStore'
import { useAudioStore } from '../../stores/audioStore'
import { storeToRefs } from 'pinia'

const settingsStore = useSettingsStore()
const audioStore = useAudioStore()

const { cps, voiceEnabled } = storeToRefs(settingsStore)
const { musicVolume, isMuted } = storeToRefs(audioStore)

defineEmits<{
  (e: 'close'): void
}>()
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50">
    <div class="novel-card max-w-md w-full">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-purple-300">Settings</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white text-2xl">&times;</button>
      </div>

      <div class="space-y-6">
        <!-- Text Speed -->
        <div>
          <label class="block text-gray-300 mb-2">Text Speed: {{ cps }} CPS</label>
          <input 
            type="range" 
            :value="cps"
            @input="settingsStore.setCps(Number(($event.target as HTMLInputElement).value))"
            min="40" 
            max="60" 
            step="5"
            class="w-full"
          />
          <div class="flex justify-between text-gray-500 text-sm mt-1">
            <span>Slow</span>
            <span>Fast</span>
          </div>
        </div>

        <!-- Music Volume -->
        <div>
          <label class="block text-gray-300 mb-2">Music Volume</label>
          <input 
            type="range" 
            :value="musicVolume"
            @input="audioStore.setMusicVolume(Number(($event.target as HTMLInputElement).value))"
            min="0" 
            max="1" 
            step="0.1"
            class="w-full"
          />
        </div>

        <!-- Voice -->
        <div class="flex items-center justify-between">
          <label class="text-gray-300">Voice Acting</label>
          <button 
            @click="settingsStore.toggleVoice()"
            :class="[
              'px-4 py-2 rounded',
              voiceEnabled ? 'bg-purple-600' : 'bg-gray-600'
            ]"
          >
            {{ voiceEnabled ? 'On' : 'Off' }}
          </button>
        </div>

        <!-- Mute -->
        <div class="flex items-center justify-between">
          <label class="text-gray-300">Mute All</label>
          <button 
            @click="audioStore.toggleMute()"
            :class="[
              'px-4 py-2 rounded',
              isMuted ? 'bg-red-600' : 'bg-gray-600'
            ]"
          >
            {{ isMuted ? 'Muted' : 'Unmuted' }}
          </button>
        </div>
      </div>

      <button 
        @click="$emit('close')"
        class="mt-8 w-full novel-button"
      >
        Done
      </button>
    </div>
  </div>
</template>
