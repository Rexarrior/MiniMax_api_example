<template>
  <div class="absolute inset-0 flex items-end justify-center pointer-events-none">
    <img
      v-if="url"
      :src="url"
      alt="Character"
      class="max-h-full object-contain object-bottom"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  url?: string
}>()
</script>