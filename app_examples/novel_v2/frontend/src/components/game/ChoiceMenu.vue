<script setup lang="ts">
import type { Choice } from '../../types/novel'

defineProps<{
  choices: Choice[]
}>()

const emit = defineEmits<{
  (e: 'select', index: number): void
}>()

function handleSelect(index: number) {
  emit('select', index)
}
</script>

<template>
  <div class="choice-menu mt-4 space-y-2">
    <button
      v-for="(choice, index) in choices"
      :key="index"
      @click.stop="handleSelect(index)"
      class="w-full p-3 bg-gray-800 hover:bg-purple-700 
             text-left text-white rounded-lg
             transition-colors duration-200
             border border-gray-700 hover:border-purple-500"
    >
      <span class="text-purple-400 mr-2">[{{ index + 1 }}]</span>
      {{ choice.text }}
    </button>
  </div>
</template>
