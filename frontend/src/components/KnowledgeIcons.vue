<template>
  <component :is="icon" v-bind="$attrs" />
</template>

<script setup lang="ts">
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const props = defineProps<{
  name: keyof typeof ElementPlusIconsVue
}>()

const icon = ElementPlusIconsVue[props.name]
</script> 