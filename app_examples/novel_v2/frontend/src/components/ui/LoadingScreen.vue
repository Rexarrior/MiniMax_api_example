<script setup lang="ts">
defineProps<{
  message?: string
}>()
</script>

<template>
  <div class="loading-screen min-h-screen flex flex-col items-center justify-center bg-black">
    <div class="animate-spin rounded-full h-16 w-16 border-4 border-purple-500 border-t-transparent mb-4"></div>
    <p class="text-gray-400 text-lg">{{ message || 'Loading...' }}</p>
  </div>
</template>
