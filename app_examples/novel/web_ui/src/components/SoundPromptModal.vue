<template>
  <Teleport to="body">
    <div class="fixed inset-0 flex items-center justify-center bg-black/70 z-50">
      <div class="bg-dark-surface rounded-xl p-8 max-w-sm w-full mx-4 shadow-2xl">
        <p class="text-white text-xl text-center mb-6">Enable sound?</p>
        <div class="flex gap-4 justify-center">
          <button
            class="px-6 py-3 bg-gradient-primary text-white rounded-lg hover:opacity-90 transition-opacity"
            @click="emit('enable')"
          >
            Yes
          </button>
          <button
            class="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-500 transition-colors"
            @click="emit('disable')"
          >
            No
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  enable: []
  disable: []
}>()
</script>