<template>
  <div class="graph-controls">
    <el-button-group>
      <el-button @click="$emit('zoom-in')" :icon="ZoomIn" />
      <el-button @click="$emit('zoom-out')" :icon="ZoomOut" />
      <el-button @click="$emit('reset')" :icon="Refresh" />
      <el-button @click="$emit('center')" :icon="FullScreen" />
    </el-button-group>
  </div>
</template>

<script setup lang="ts">
import { ZoomIn, ZoomOut, Refresh, FullScreen } from '@element-plus/icons-vue'

// Emits
const emit = defineEmits<{
  (e: 'zoom-in'): void
  (e: 'zoom-out'): void
  (e: 'reset'): void
  (e: 'center'): void
}>()
</script>

<style scoped>
.graph-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 10;
}
</style> 