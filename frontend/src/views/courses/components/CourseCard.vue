<template>
  <div class="course-card" @click="$emit('click', course.id)">
    <!-- 课程封面 -->
    <div class="course-cover">
      <img :src="course.cover_url" :alt="course.title">
      <div class="course-difficulty" :style="{ backgroundColor: getDifficultyColor(course.difficulty) }">
        {{ getDifficultyLabel(course.difficulty) }}
      </div>
    </div>

    <!-- 课程内容 -->
    <div class="course-content">
      <h3 class="course-title">{{ course.title }}</h3>
      <p class="course-description">{{ course.description }}</p>

      <!-- 课程信息 -->
      <div class="course-info">
        <div class="info-item">
          <el-icon><Timer /></el-icon>
          <span>{{ formatDuration(course.duration) }}</span>
        </div>
        <div class="info-item">
          <el-icon><User /></el-icon>
          <span>{{ formatNumber(course.student_count) }}人学习</span>
        </div>
        <div class="info-item">
          <el-icon><StarFilled /></el-icon>
          <span>{{ course.rating.toFixed(1) }}</span>
        </div>
      </div>

      <!-- 讲师信息 -->
      <div class="instructor-info">
        <img :src="course.instructor.avatar" :alt="course.instructor.name" class="instructor-avatar">
        <div class="instructor-detail">
          <div class="instructor-name">{{ course.instructor.name }}</div>
          <div class="instructor-title">{{ course.instructor.title }}</div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="course-actions">
        <el-button 
          type="primary" 
          @click.stop="handleStartClick"
        >
          开始学习
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Timer, User, StarFilled } from '@element-plus/icons-vue'
import type { Course } from '@/types/course'
import { courseDifficulties } from '../mock/data'

const props = defineProps<{
  course: Course
}>()

const emit = defineEmits<{
  (e: 'click', id: number): void
  (e: 'start', id: number): void
}>()

// 获取难度标签
const getDifficultyLabel = (difficulty: string) => {
  const diff = courseDifficulties.find(d => d.key === difficulty)
  return diff ? diff.label : difficulty
}

// 获取难度颜色
const getDifficultyColor = (difficulty: string) => {
  const diff = courseDifficulties.find(d => d.key === difficulty)
  return diff ? diff.color : '#999'
}

// 格式化时长
const formatDuration = (minutes: number) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`
}

// 格式化数字
const formatNumber = (num: number) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

const handleStartClick = () => {
  console.log('Start button clicked:', props.course.id)
  emit('start', props.course.id)
}
</script>

<style lang="scss" scoped>
.course-card {
  background: #1a2234;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  }

  .course-cover {
    position: relative;
    padding-top: 56.25%;
    overflow: hidden;

    img {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }

    &:hover img {
      transform: scale(1.05);
    }

    .course-difficulty {
      position: absolute;
      top: 8px;
      right: 8px;
      padding: 3px 10px;
      border-radius: 4px;
      font-size: 0.8rem;
      color: #fff;
    }
  }

  .course-content {
    padding: 12px;

    .course-title {
      font-size: 1.1rem;
      font-weight: 600;
      color: #fff;
      margin: 0 0 6px;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .course-description {
      color: #94A3B8;
      font-size: 0.85rem;
      line-height: 1.4;
      margin: 0 0 12px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .course-info {
      display: flex;
      gap: 12px;
      margin-bottom: 12px;

      .info-item {
        display: flex;
        align-items: center;
        gap: 4px;
        color: #94A3B8;
        font-size: 0.8rem;

        .el-icon {
          font-size: 0.9rem;
        }
      }
    }

    .instructor-info {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);

      .instructor-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        object-fit: cover;
      }

      .instructor-detail {
        .instructor-name {
          color: #fff;
          font-size: 0.85rem;
          font-weight: 500;
          margin-bottom: 2px;
        }

        .instructor-title {
          color: #94A3B8;
          font-size: 0.75rem;
        }
      }
    }

    .course-actions {
      display: flex;
      justify-content: center;

      .el-button {
        width: 100%;
        border-radius: 4px;
        height: 32px;
        font-size: 0.9rem;
      }
    }
  }
}
</style> 