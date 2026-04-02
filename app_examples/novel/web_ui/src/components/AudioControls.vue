<template>
  <button
    class="fixed top-4 right-4 w-12 h-12 flex items-center justify-center rounded-full bg-black/40 backdrop-blur-sm text-white text-xl hover:bg-black/60 transition-colors z-50"
    @click="emit('toggle')"
  >
    {{ isMuted ? '🔇' : '🔊' }}
  </button>
</template>

<script setup lang="ts">
defineProps<{
  isMuted: boolean
}>()

const emit = defineEmits<{
  toggle: []
}>()
</script>