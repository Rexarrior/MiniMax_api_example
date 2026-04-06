<script setup lang="ts">
defineProps<{
  name: string
}>()

function formatName(name: string): string {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}
</script>

<template>
  <div class="speaker-name px-4 py-2">
    <div class="max-w-4xl mx-auto">
      <span class="inline-block bg-purple-700 text-white px-4 py-1 rounded-full font-semibold text-sm">
        {{ formatName(name) }}
      </span>
    </div>
  </div>
</template>
