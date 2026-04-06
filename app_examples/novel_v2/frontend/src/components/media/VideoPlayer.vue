<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  videoUrl: string | null
  isFullscreen?: boolean
}>()

const emit = defineEmits<{
  (e: 'ended'): void
  (e: 'exit'): void
}>()

const videoRef = ref<HTMLVideoElement | null>(null)

watch(() => props.videoUrl, (newUrl) => {
  if (videoRef.value) {
    if (newUrl) {
      videoRef.value.src = newUrl
      videoRef.value.play()
    } else {
      videoRef.value.pause()
    }
  }
})

function handleEnded() {
  emit('ended')
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    emit('exit')
  }
}
</script>

<template>
  <div 
    v-if="videoUrl"
    class="video-player fixed inset-0 z-50 bg-black"
    @keydown="handleKeydown"
    tabindex="0"
  >
    <video
      ref="videoRef"
      class="w-full h-full object-contain"
      @ended="handleEnded"
      controls
      autoplay
    >
      <source :src="videoUrl" type="video/mp4" />
      Your browser does not support the video tag.
    </video>

    <!-- Exit button -->
    <button
      @click="$emit('exit')"
      class="absolute top-4 right-4 bg-black bg-opacity-50 text-white px-4 py-2 rounded hover:bg-opacity-70"
    >
      Skip
    </button>
  </div>
</template>