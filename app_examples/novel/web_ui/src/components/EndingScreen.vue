<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-dark p-4">
    <h2 class="text-4xl font-bold text-white mb-8 text-center">The End</h2>
    <button
      class="px-8 py-4 bg-gradient-primary text-white text-xl font-semibold rounded-xl shadow-lg hover:opacity-90 transition-opacity"
      @click="handleRestart"
    >
      Play Again
    </button>
  </div>
</template>

<script setup lang="ts">
function handleRestart() {
  window.location.href = '/?session_id=' + Math.random().toString(36).substring(2, 15)
}
</script>