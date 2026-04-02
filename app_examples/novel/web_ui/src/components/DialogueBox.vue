<template>
  <div
    class="bg-black/60 backdrop-blur-md rounded-xl p-6 max-w-2xl w-full mx-4 shadow-2xl"
    @click="handleClick"
  >
    <div class="mb-2">
      <SpeakerName
        v-if="speaker !== 'narrator'"
        :text="speaker"
      />
      <span v-else class="text-gray-400 italic">Narrator</span>
    </div>
    <TypewriterText
      :text="text"
      :displayed-text="displayedText"
      :is-typing="isTyping"
      :is-narrator="speaker === 'narrator'"
    />
    <div v-if="!isTyping && hasMore" class="mt-4 text-right text-gray-400 text-sm">
      Click to continue...
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  speaker: string
  text: string
  displayedText: string
  isTyping: boolean
  hasMore: boolean
}>()

const emit = defineEmits<{
  advance: []
}>()

function handleClick() {
  emit('advance')
}
</script>