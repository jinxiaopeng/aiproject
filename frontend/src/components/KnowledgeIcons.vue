<template>
  <div>
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import {
  Search,
  Refresh,
  ZoomIn,
  ZoomOut,
  FullScreen,
  Grid,
  ArrowDown,
  Close
} from '@element-plus/icons-vue'

defineExpose({
  Search,
  Refresh,
  ZoomIn,
  ZoomOut,
  FullScreen,
  Grid,
  ArrowDown,
  Close
})
</script> 