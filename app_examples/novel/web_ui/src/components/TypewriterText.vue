<template>
  <span
    :class="[
      'leading-relaxed whitespace-pre-wrap',
      isNarrator ? 'text-gray-400 italic' : 'text-white'
    ]"
  >{{ displayedText }}<span v-if="isTyping" class="animate-pulse">|</span></span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  text: string
  displayedText: string
  isTyping: boolean
  isNarrator: boolean
}>()

const isNarrator = computed(() => props.isNarrator)
</script>