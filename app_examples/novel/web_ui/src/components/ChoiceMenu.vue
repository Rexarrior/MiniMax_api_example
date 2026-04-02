<template>
  <div class="flex flex-col gap-3 w-full max-w-md mx-4">
    <button
      v-for="(choice, index) in choices"
      :key="index"
      class="bg-dark-surface/80 backdrop-blur-sm text-white py-3 px-6 rounded-lg border border-white/20 hover:bg-white/20 hover:border-primary-start transition-all duration-200 text-left"
      @click="emit('select', index)"
    >
      {{ choice.text }}
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Choice } from '@/types/novel'

defineProps<{
  choices: Choice[]
}>()

const emit = defineEmits<{
  select: [index: number]
}>()
</script>