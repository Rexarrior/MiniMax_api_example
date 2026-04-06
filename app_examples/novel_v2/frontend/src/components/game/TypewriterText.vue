<script setup lang="ts">
defineProps<{
  text: string
  isTyping: boolean
}>()
</script>

<template>
  <div class="typewriter-text">
    <span class="text-white text-lg leading-relaxed whitespace-pre-wrap">
      {{ text }}
    </span>
    <span 
      v-if="isTyping" 
      class="inline-block w-2 h-5 bg-purple-400 ml-1 animate-pulse"
    ></span>
  </div>
</template>
