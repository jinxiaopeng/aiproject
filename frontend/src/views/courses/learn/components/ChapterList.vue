<template>
  <div class="chapter-list">
    <div
      v-for="chapter in chapters"
      :key="chapter.id"
      class="chapter-item"
      :class="{ active: chapter.id === currentChapterId }"
      @click="$emit('select', chapter.id)"
    >
      <div class="chapter-info">
        <div class="title">{{ chapter.title }}</div>
        <div class="duration">{{ formatDuration(chapter.duration) }}</div>
      </div>
      <div class="status">{{ chapter.progress === 100 ? '已完成' : '进行中' }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Chapter {
  id: number
  title: string
  description: string
  video_url: string
  duration: number
  progress: number
}

defineProps<{
  chapters: Chapter[]
  currentChapterId: number
}>()

const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  return `${minutes}分钟`
}
</script>

<style lang="scss" scoped>
.chapter-list {
  .chapter-item {
    padding: 12px;
    cursor: pointer;
    border-radius: 4px;
    transition: background-color 0.3s;

    &:hover {
      background-color: var(--el-fill-color-light);
    }

    &.active {
      background-color: var(--el-color-primary-light-9);
    }

    .chapter-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;

      .title {
        font-weight: 500;
        color: var(--el-text-color-primary);
      }

      .duration {
        font-size: 13px;
        color: var(--el-text-color-secondary);
      }
    }

    .status {
      font-size: 12px;
      color: var(--el-color-success);
    }
  }
}
</style> 