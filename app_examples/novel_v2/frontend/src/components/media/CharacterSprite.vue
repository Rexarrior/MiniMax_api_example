<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  imageUrl: string | null
}>()

const imageLoaded = ref(false)

watch(() => props.imageUrl, () => {
  imageLoaded.value = false
})
</script>

<template>
  <div 
    v-if="imageUrl"
    class="character-sprite absolute bottom-32 left-1/2 transform -translate-x-1/2 max-w-xl"
  >
    <img
      :src="imageUrl"
      class="max-h-[60vh] w-auto object-contain transition-opacity duration-300"
      :class="{ 'opacity-0': !imageLoaded }"
      @load="imageLoaded = true"
    />
  </div>
</template>