<template>
  <edge-animation
    :source="source"
    :target="target"
    :relation="relation"
    :type="type"
    :is-selected="isSelected"
  />
</template>

<script setup lang="ts">
import EdgeAnimation from './EdgeAnimation.vue'

const props = defineProps<{
  source: { x: number; y: number }
  target: { x: number; y: number }
  relation: string
  type: string
  isSelected: boolean
}>()
</script> 