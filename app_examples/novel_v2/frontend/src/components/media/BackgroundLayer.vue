<script setup lang="ts">
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps<{
  imageUrl: string | null
  videoUrl: string | null
}>()

const imageLoaded = ref(false)
const videoRef = ref<HTMLVideoElement | null>(null)

watch(() => props.videoUrl, (newUrl) => {
  if (videoRef.value) {
    if (newUrl) {
      videoRef.value.src = newUrl
      videoRef.value.play()
    } else {
      videoRef.value.pause()
      videoRef.value.src = ''
    }
  }
})

watch(() => props.imageUrl, () => {
  imageLoaded.value = false
})

onUnmounted(() => {
  if (videoRef.value) {
    videoRef.value.pause()
  }
})
</script>

<template>
  <div class="background-layer absolute inset-0">
    <!-- Video Background (takes priority) -->
    <video
      v-if="videoUrl"
      ref="videoRef"
      class="absolute inset-0 w-full h-full object-cover"
      autoplay
      loop
      muted
      playsinline
    >
      <source :src="videoUrl" type="video/mp4" />
    </video>

    <!-- Image Background -->
    <img
      v-if="imageUrl && !videoUrl"
      :src="imageUrl"
      class="absolute inset-0 w-full h-full object-cover transition-opacity duration-500"
      :class="{ 'opacity-0': !imageLoaded }"
      @load="imageLoaded = true"
    />

    <!-- Fallback gradient when no background -->
    <div 
      v-if="!imageUrl && !videoUrl"
      class="absolute inset-0 bg-gradient-to-b from-gray-900 via-gray-800 to-black"
    ></div>

    <!-- Overlay for readability -->
    <div class="absolute inset-0 bg-black bg-opacity-30"></div>
  </div>
</template>