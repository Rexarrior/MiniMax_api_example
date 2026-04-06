<script setup lang="ts">
</script>

<template>
  <div class="dialogue-box bg-gradient-to-t from-black via-black/95 to-transparent pt-8 pb-6 px-4">
    <div class="max-w-4xl mx-auto">
      <div class="bg-gray-900 bg-opacity-90 rounded-xl p-6 border border-purple-900">
        <slot />
      </div>
    </div>
  </div>
</template>
