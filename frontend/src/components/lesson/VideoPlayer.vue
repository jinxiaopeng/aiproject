<template>
  <div class="video-player">
    <div class="player-container" @mousemove="showControls" @mouseleave="hideControls">
      <!-- 视频元素 -->
      <video
        ref="videoRef"
        class="video-element"
        :src="src"
        @timeupdate="handleTimeUpdate"
        @loadedmetadata="handleMetadataLoaded"
        @ended="handleEnded"
        @waiting="handleWaiting"
        @playing="handlePlaying"
        @error="handleError"
      ></video>

      <!-- 加载动画 -->
      <div v-if="loading" class="loading-overlay">
        <el-icon class="loading-icon" :size="40"><Loading /></el-icon>
      </div>

      <!-- 播放器控制栏 -->
      <div
        class="player-controls"
        :class="{ 'controls-visible': controlsVisible || paused }"
      >
        <!-- 进度条 -->
        <div class="progress-bar" @click="handleProgressClick">
          <div class="progress-background"></div>
          <div
            class="progress-current"
            :style="{ width: `${progress}%` }"
          ></div>
          <div
            class="progress-handle"
            :style="{ left: `${progress}%` }"
          ></div>
        </div>

        <!-- 控制按钮组 -->
        <div class="controls-row">
          <div class="left-controls">
            <el-button
              class="control-btn"
              :icon="paused ? Play : Pause"
              @click="togglePlay"
            />
            <el-button
              class="control-btn"
              :icon="volume === 0 ? Mute : Voice"
              @click="toggleMute"
            />
            <el-slider
              v-model="volume"
              class="volume-slider"
              :min="0"
              :max="100"
              :show-tooltip="false"
              @input="handleVolumeChange"
            />
            <span class="time-display">
              {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
            </span>
          </div>

          <div class="right-controls">
            <el-button
              class="control-btn"
              :icon="isFullscreen ? FullscreenExit : FullScreen"
              @click="toggleFullscreen"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import {
  Play,
  Pause,
  FullScreen,
  FullscreenExit,
  Voice,
  Mute,
  Loading
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// Props
const props = defineProps<{
  src: string
  currentTime?: number
  courseId: number
  chapterId: number
}>()

// Emits
const emit = defineEmits<{
  (e: 'timeupdate', time: number): void
  (e: 'ended'): void
}>()

// Refs
const videoRef = ref<HTMLVideoElement>()
const controlsVisible = ref(true)
const controlsTimer = ref<number | null>(null)
const loading = ref(false)
const paused = ref(true)
const duration = ref(0)
const currentTime = ref(props.currentTime || 0)
const volume = ref(100)
const isFullscreen = ref(false)
const progress = ref(0)

// 计算进度百分比
const calculateProgress = () => {
  if (!videoRef.value || !duration.value) return 0
  return (currentTime.value / duration.value) * 100
}

// 格式化时间
const formatTime = (seconds: number) => {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  
  if (h > 0) {
    return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }
  return `${m}:${s.toString().padStart(2, '0')}`
}

// 控制栏显示/隐藏
const showControls = () => {
  controlsVisible.value = true
  if (controlsTimer.value) {
    window.clearTimeout(controlsTimer.value)
  }
  if (!paused.value) {
    controlsTimer.value = window.setTimeout(() => {
      controlsVisible.value = false
    }, 3000)
  }
}

const hideControls = () => {
  if (!paused.value) {
    controlsVisible.value = false
  }
}

// 播放控制
const togglePlay = () => {
  if (!videoRef.value) return
  
  if (videoRef.value.paused) {
    videoRef.value.play()
    paused.value = false
  } else {
    videoRef.value.pause()
    paused.value = true
  }
}

// 音量控制
const toggleMute = () => {
  if (!videoRef.value) return
  
  if (volume.value === 0) {
    volume.value = 100
  } else {
    volume.value = 0
  }
  handleVolumeChange(volume.value)
}

const handleVolumeChange = (value: number) => {
  if (!videoRef.value) return
  videoRef.value.volume = value / 100
}

// 全屏控制
const toggleFullscreen = async () => {
  if (!videoRef.value) return
  
  try {
    if (!document.fullscreenElement) {
      await videoRef.value.requestFullscreen()
      isFullscreen.value = true
    } else {
      await document.exitFullscreen()
      isFullscreen.value = false
    }
  } catch (error) {
    ElMessage.error('全屏模式不可用')
  }
}

// 进度控制
const handleProgressClick = (event: MouseEvent) => {
  if (!videoRef.value || !duration.value) return
  
  const progressBar = event.currentTarget as HTMLElement
  const rect = progressBar.getBoundingClientRect()
  const percentage = (event.clientX - rect.left) / rect.width
  const newTime = percentage * duration.value
  
  videoRef.value.currentTime = newTime
  currentTime.value = newTime
  progress.value = percentage * 100
}

// 记录视频进度
const recordProgress = async () => {
  if (!videoRef.value) return
  
  try {
    const progress = Math.round((currentTime.value / duration.value) * 100)
    await fetch('http://localhost:8001/learning/video/progress', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: 1, // TODO: 从用户状态获取
        course_id: props.courseId,
        chapter_id: props.chapterId,
        progress: progress,
        duration: Math.round(duration.value),
        current_time: Math.round(currentTime.value)
      })
    })
  } catch (error) {
    console.error('Failed to record progress:', error)
  }
}

// 记录学习行为
const recordBehavior = async (type: string) => {
  try {
    await fetch('http://localhost:8001/learning/behavior', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: 1, // TODO: 从用户状态获取
        course_id: props.courseId,
        behavior_type: type,
        content_id: props.chapterId,
        duration: Math.round(currentTime.value)
      })
    })
  } catch (error) {
    console.error('Failed to record behavior:', error)
  }
}

// 更新视频事件处理
const handleTimeUpdate = () => {
  if (!videoRef.value) return
  currentTime.value = videoRef.value.currentTime
  progress.value = calculateProgress()
  emit('timeupdate', currentTime.value)
  
  // 每30秒记录一次进度
  if (Math.floor(currentTime.value) % 30 === 0) {
    recordProgress()
  }
}

const handleMetadataLoaded = () => {
  if (!videoRef.value) return
  duration.value = videoRef.value.duration
  if (props.currentTime) {
    videoRef.value.currentTime = props.currentTime
  }
}

const handleEnded = () => {
  recordBehavior('video_complete')
  emit('ended')
}

const handleWaiting = () => {
  loading.value = true
}

const handlePlaying = () => {
  loading.value = false
}

const handleError = () => {
  ElMessage.error('视频加载失败')
  loading.value = false
}

// 生命周期钩子
onMounted(() => {
  // 监听全屏变化
  document.addEventListener('fullscreenchange', () => {
    isFullscreen.value = !!document.fullscreenElement
  })
})

onBeforeUnmount(() => {
  if (controlsTimer.value) {
    window.clearTimeout(controlsTimer.value)
  }
  document.removeEventListener('fullscreenchange', () => {})
})
</script>

<style scoped>
.video-player {
  width: 100%;
  background-color: #000;
  position: relative;
}

.player-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.video-element {
  width: 100%;
  height: 100%;
  display: block;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
}

.loading-icon {
  color: #fff;
  animation: rotate 2s linear infinite;
}

.player-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  padding: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.controls-visible {
  opacity: 1;
}

.progress-bar {
  position: relative;
  height: 4px;
  margin-bottom: 10px;
  cursor: pointer;
}

.progress-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.2);
}

.progress-current {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  background-color: var(--el-color-primary);
  transition: width 0.1s linear;
}

.progress-handle {
  position: absolute;
  top: 50%;
  width: 12px;
  height: 12px;
  background-color: var(--el-color-primary);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: left 0.1s linear;
}

.controls-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-controls,
.right-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-btn {
  background: transparent;
  border: none;
  color: #fff;
  padding: 8px;
  cursor: pointer;
}

.control-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.volume-slider {
  width: 80px;
  margin: 0 8px;
}

.time-display {
  color: #fff;
  font-size: 14px;
  min-width: 100px;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 