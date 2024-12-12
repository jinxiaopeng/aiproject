<template>
  <div class="course-card" @click="handleClick">
    <!-- 课程封面 -->
    <div class="card-cover">
      <img :src="course.cover_url" :alt="course.title">
      <div class="card-overlay">
        <div class="overlay-content">
          <div class="difficulty">
            <el-tag :type="difficultyType" effect="dark" class="difficulty-tag">
              {{ difficultyLabel }}
            </el-tag>
          </div>
          
          <div class="hover-info">
            <div class="info-item">
              <el-icon><TimerIcon /></el-icon>
              <span>{{ formattedDuration }}</span>
            </div>
            <div class="info-item">
              <el-icon><ListIcon /></el-icon>
              <span>{{ course.lessons || 0 }}课时</span>
            </div>
            <div class="info-item">
              <el-icon><UserIcon /></el-icon>
              <span>{{ course.student_count || 0 }}人学习</span>
            </div>
          </div>
          
          <div class="hover-actions">
            <el-button 
              v-if="course.progress !== undefined"
              type="primary" 
              class="action-btn"
              @click.stop="$emit('continue', course.id)"
            >
              继续学习
            </el-button>
            <el-button 
              v-else
              type="primary" 
              class="action-btn"
              @click.stop="$emit('start', course.id)"
            >
              开始学习
            </el-button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 课程内容 -->
    <div class="card-content">
      <div class="content-main">
        <h3 class="course-title" :title="course.title">{{ course.title }}</h3>
        <p class="course-description">{{ course.description }}</p>
      </div>
      
      <div class="content-footer">
        <div class="course-meta">
          <div class="teacher-info" v-if="course.teacher">
            <el-avatar :size="24" :src="course.teacher.avatar" />
            <span class="teacher-name">{{ course.teacher.name }}</span>
          </div>
          
          <template v-if="course.progress !== undefined">
            <div class="progress-info">
              <div class="progress-text">
                已完成 {{ course.progress }}%
              </div>
              <el-progress
                :percentage="course.progress"
                :stroke-width="4"
                :show-text="false"
              />
            </div>
          </template>
          <template v-else>
            <div class="course-rating">
              <el-rate
                :model-value="course.rating"
                disabled
                :max="5"
                :colors="['#64ffda', '#64ffda', '#64ffda']"
              />
              <span class="rating-value">{{ course.rating?.toFixed(1) || '0.0' }}</span>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  Timer as TimerIcon,
  List as ListIcon,
  User as UserIcon
} from '@element-plus/icons-vue'

interface Teacher {
  name: string
  avatar: string
}

interface Course {
  id: number
  title: string
  description: string
  cover_url: string
  difficulty: string
  student_count?: number
  duration: number
  lessons?: number
  rating?: number
  progress?: number
  teacher?: Teacher
}

const props = defineProps<{
  course: Course
}>()

const emit = defineEmits<{
  (e: 'click', id: number): void
  (e: 'start', id: number): void
  (e: 'continue', id: number): void
}>()

// 计算难度标签
const difficultyLabel = computed(() => {
  const labels: Record<string, string> = {
    beginner: '入门',
    elementary: '初级',
    intermediate: '中级',
    advanced: '高级',
    expert: '专家'
  }
  return labels[props.course.difficulty] || props.course.difficulty
})

// 计算难度类型
const difficultyType = computed(() => {
  const types: Record<string, string> = {
    beginner: 'success',
    elementary: 'info',
    intermediate: 'warning',
    advanced: 'danger',
    expert: ''
  }
  return types[props.course.difficulty] || ''
})

// 格式化时长
const formattedDuration = computed(() => {
  const hours = Math.floor(props.course.duration / 60)
  const mins = props.course.duration % 60
  return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`
})

// 点击卡片
const handleClick = () => {
  emit('click', props.course.id)
}
</script>

<style lang="scss" scoped>
.course-card {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    pointer-events: none;
  }
  
  &:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.04);
    
    &::before {
      border-color: rgba(255, 255, 255, 0.2);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }
    
    .card-cover {
      img {
        transform: scale(1.05);
      }
      
      .card-overlay {
        opacity: 1;
        
        .overlay-content {
          transform: translateY(0);
        }
      }
    }
  }

  .card-cover {
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
      transition: transform 0.5s ease;
    }
    
    .card-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.8));
      opacity: 0;
      transition: opacity 0.3s ease;
      
      .overlay-content {
        height: 100%;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transform: translateY(20px);
        transition: transform 0.3s ease;
        
        .difficulty {
          .difficulty-tag {
            font-size: 0.85rem;
            padding: 0 0.75rem;
            height: 24px;
            line-height: 22px;
            backdrop-filter: blur(4px);
          }
        }
        
        .hover-info {
          .info-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            
            .el-icon {
              font-size: 1rem;
            }
          }
        }
        
        .hover-actions {
          .action-btn {
            width: 100%;
            border-radius: 6px;
            height: 40px;
            font-size: 1rem;
          }
        }
      }
    }
  }

  .card-content {
    padding: 1.5rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    
    .content-main {
      flex: 1;
      
      .course-title {
        font-size: 1.1rem;
        font-weight: 500;
        color: #fff;
        margin: 0 0 0.75rem;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .course-description {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        margin: 0;
        line-height: 1.6;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
    }
    
    .content-footer {
      margin-top: 1.5rem;
      padding-top: 1rem;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      
      .course-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .teacher-info {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          
          .teacher-name {
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.8);
          }
        }
        
        .progress-info {
          flex: 1;
          margin-left: 1rem;
          
          .progress-text {
            font-size: 0.85rem;
            color: rgba(255, 255, 255, 0.6);
            margin-bottom: 0.25rem;
          }
        }
        
        .course-rating {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          
          :deep(.el-rate) {
            --el-rate-icon-size: 14px;
            display: inline-flex;
          }
          
          .rating-value {
            font-size: 0.9rem;
            color: #64ffda;
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .course-card {
    .card-content {
      padding: 1.25rem;
      
      .content-main {
        .course-title {
          font-size: 1rem;
        }
      }
      
      .content-footer {
        margin-top: 1.25rem;
        
        .course-meta {
          flex-wrap: wrap;
          gap: 1rem;
          
          .progress-info,
          .course-rating {
            width: 100%;
            margin-left: 0;
          }
        }
      }
    }
  }
}
</style> 