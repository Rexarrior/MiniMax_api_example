<template>
  <div class="absolute inset-0 w-full h-full">
    <img
      v-if="url"
      :src="url"
      alt="Background"
      class="w-full h-full object-cover"
    />
    <div v-else class="w-full h-full bg-gradient-primary" />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  url?: string
}>()
</script>