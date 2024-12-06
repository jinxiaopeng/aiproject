<template>
  <el-icon v-if="name === 'share'"><el-icon-share /></el-icon>
  <el-icon v-else-if="name === 'histogram'"><el-icon-histogram /></el-icon>
  <el-icon v-else-if="name === 'document'"><el-icon-document /></el-icon>
  <el-icon v-else-if="name === 'setting'"><el-icon-setting /></el-icon>
  <el-icon v-else-if="name === 'search'"><el-icon-search /></el-icon>
  <el-icon v-else-if="name === 'refresh'"><el-icon-refresh /></el-icon>
  <el-icon v-else-if="name === 'full-screen'"><el-icon-full-screen /></el-icon>
  <el-icon v-else-if="name === 'arrow-down'"><el-icon-arrow-down /></el-icon>
  <el-icon v-else-if="name === 'close'"><el-icon-close /></el-icon>
  <el-icon v-else-if="name === 'zoom-in'"><el-icon-zoom-in /></el-icon>
  <el-icon v-else-if="name === 'zoom-out'"><el-icon-zoom-out /></el-icon>
</template>

<script setup lang="ts">
defineProps<{
  name: 'share' | 'histogram' | 'document' | 'setting' | 'search' | 'refresh' | 
        'full-screen' | 'arrow-down' | 'close' | 'zoom-in' | 'zoom-out'
}>()
</script> 