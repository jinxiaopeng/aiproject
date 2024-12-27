<template>
  <div class="video-player">
    <video
      ref="videoRef"
      class="video-element"
      :src="src"
      :poster="poster || '/images/courses/web-security-basic.jpg'"
      controls
      preload="metadata"
      @timeupdate="handleTimeUpdate"
      @loadedmetadata="handleMetadataLoaded"
      @ended="handleEnded"
    ></video>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Props
const props = defineProps<{
  src: string
  poster?: string
  currentTime?: number
}>()

// Emits
const emit = defineEmits<{
  (e: 'timeupdate', time: number): void
  (e: 'ended'): void
}>()

// Refs
const videoRef = ref<HTMLVideoElement>()
const currentTime = ref(props.currentTime || 0)

// 暴露视频引用给父组件
defineExpose({
  videoElement: videoRef
})

// 视频事件处理
const handleTimeUpdate = () => {
  if (!videoRef.value) return
  currentTime.value = videoRef.value.currentTime
  emit('timeupdate', currentTime.value)
}

const handleMetadataLoaded = () => {
  if (!videoRef.value || !props.currentTime) return
  videoRef.value.currentTime = props.currentTime
}

const handleEnded = () => {
  emit('ended')
}

// 初始化
onMounted(() => {
  if (videoRef.value && props.currentTime) {
    videoRef.value.currentTime = props.currentTime
  }
})
</script>

<style lang="scss" scoped>
.video-player {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.video-element {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}
</style> 