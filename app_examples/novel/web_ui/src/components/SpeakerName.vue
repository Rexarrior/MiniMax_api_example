<template>
  <span class="text-white font-medium">{{ text }}</span>
</template>

<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>