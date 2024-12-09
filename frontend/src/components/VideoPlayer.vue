<template>
  <div class="video-player">
    <video
      ref="videoRef"
      class="video-js vjs-theme-cyber"
      controls
      preload="auto"
      :poster="poster"
      data-setup="{}"
    >
      <source :src="src" type="video/mp4" />
      <p class="vjs-no-js">
        要观看此视频，请启用JavaScript并考虑升级到支持HTML5视频的浏览器
      </p>
    </video>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import videojs from 'video.js'
import 'video.js/dist/video-js.css'
import '@videojs/themes/dist/cyber/index.css'

const props = defineProps<{
  src: string
  poster?: string
  autoplay?: boolean
  onTimeUpdate?: (currentTime: number) => void
  onEnded?: () => void
}>()

const emit = defineEmits<{
  (e: 'timeupdate', time: number): void
  (e: 'ended'): void
}>()

const videoRef = ref<HTMLVideoElement | null>(null)
let player: any = null

// 初始化视频播放器
onMounted(() => {
  if (!videoRef.value) return

  player = videojs(videoRef.value, {
    controls: true,
    autoplay: props.autoplay || false,
    preload: 'auto',
    fluid: true,
    playbackRates: [0.5, 1, 1.25, 1.5, 2],
    controlBar: {
      children: [
        'playToggle',
        'volumePanel',
        'currentTimeDisplay',
        'timeDivider',
        'durationDisplay',
        'progressControl',
        'playbackRateMenuButton',
        'fullscreenToggle'
      ]
    }
  })

  // 监听时间更新事件
  player.on('timeupdate', () => {
    const currentTime = player.currentTime()
    emit('timeupdate', currentTime)
    props.onTimeUpdate?.(currentTime)
  })

  // 监听播放结束事件
  player.on('ended', () => {
    emit('ended')
    props.onEnded?.()
  })
})

// 监听源地址变化
watch(() => props.src, (newSrc) => {
  if (player && newSrc) {
    player.src({ src: newSrc, type: 'video/mp4' })
  }
})

// 组件销毁时清理
onBeforeUnmount(() => {
  if (player) {
    player.dispose()
  }
})

// 暴露播放器方法
defineExpose({
  play: () => player?.play(),
  pause: () => player?.pause(),
  currentTime: (time?: number) => {
    if (time !== undefined && player) {
      player.currentTime(time)
    }
    return player?.currentTime() || 0
  }
})
</script>

<style lang="scss">
.video-player {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

  .video-js {
    width: 100%;
    height: 100%;
  }

  // 自定义控制栏样式
  .vjs-theme-cyber {
    --vjs-theme-cyber--primary: #00ff9d;
    --vjs-theme-cyber--secondary: #fff;

    .vjs-control-bar {
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(10px);
    }

    .vjs-play-progress {
      background: var(--vjs-theme-cyber--primary);
    }

    .vjs-slider-bar {
      background: rgba(255, 255, 255, 0.3);
    }

    .vjs-volume-level {
      background: var(--vjs-theme-cyber--primary);
    }
  }
}
</style> 