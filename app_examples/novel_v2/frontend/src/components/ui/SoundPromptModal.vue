<script setup lang="ts">
defineEmits<{
  (e: 'enable'): void
  (e: 'skip'): void
}>()
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50">
    <div class="novel-card max-w-md text-center">
      <h2 class="text-2xl font-bold mb-4 text-purple-300">🔊 Enable Sound?</h2>
      <p class="text-gray-300 mb-6">
        This visual novel includes music and voice acting. Would you like to enable sound?
      </p>
      <div class="flex gap-4 justify-center">
        <button 
          @click="$emit('enable')"
          class="novel-button"
        >
          Enable Sound
        </button>
        <button 
          @click="$emit('skip')"
          class="novel-button-secondary"
        >
          Continue Without
        </button>
      </div>
    </div>
  </div>
</template>
