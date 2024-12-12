<template>
  <div class="video-player">
    <video
      ref="videoRef"
      class="video-element"
      :src="src"
      controls
      @timeupdate="handleTimeUpdate"
      @ended="handleEnded"
      @play="handlePlay"
      @pause="handlePause"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  src?: string
}>()

const emit = defineEmits<{
  (e: 'timeupdate', time: number): void
  (e: 'ended'): void
  (e: 'play'): void
  (e: 'pause'): void
}>()

const videoRef = ref<HTMLVideoElement | null>(null)

// 处理视频时间更新
const handleTimeUpdate = () => {
  if (videoRef.value) {
    emit('timeupdate', videoRef.value.currentTime)
  }
}

// 处理视频播放结束
const handleEnded = () => {
  emit('ended')
}

// 处理视频播放
const handlePlay = () => {
  emit('play')
}

// 处理视频暂停
const handlePause = () => {
  emit('pause')
}

// 暴露给父组件的方法
defineExpose({
  play: () => videoRef.value?.play(),
  pause: () => videoRef.value?.pause(),
  getCurrentTime: () => videoRef.value?.currentTime || 0,
  getDuration: () => videoRef.value?.duration || 0,
  setCurrentTime: (time: number) => {
    if (videoRef.value) {
      videoRef.value.currentTime = time
    }
  }
})
</script>

<style lang="scss" scoped>
.video-player {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000;
  border-radius: 8px;
  overflow: hidden;

  .video-element {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
}
</style> 