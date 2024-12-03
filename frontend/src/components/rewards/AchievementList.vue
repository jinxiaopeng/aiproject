<!-- 成就列表组件 -->
<template>
  <div class="achievement-list">
    <div class="achievement-grid">
      <div 
        v-for="achievement in achievements" 
        :key="achievement.id"
        class="achievement-item"
        :class="{ 'completed': achievement.completed }"
      >
        <div class="achievement-icon">
          <el-icon :size="32">
            <component :is="achievement.achievementType.icon || 'Trophy'" />
          </el-icon>
        </div>
        <div class="achievement-info">
          <h4>{{ achievement.achievementType.name }}</h4>
          <p>{{ achievement.achievementType.description }}</p>
          <div class="achievement-progress">
            <el-progress 
              :percentage="getProgressPercentage(achievement)"
              :status="achievement.completed ? 'success' : ''"
            />
          </div>
          <div class="achievement-meta">
            <span class="points">
              <el-icon><Medal /></el-icon>
              {{ achievement.achievementType.points }} 积分
            </span>
            <span v-if="achievement.completed" class="completion-date">
              {{ formatDate(achievement.completedAt) }} 完成
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-overlay">
      <el-skeleton :rows="3" animated />
    </div>

    <el-empty 
      v-if="!loading && achievements.length === 0"
      description="暂无成就"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import type { UserAchievement } from '@/api/rewards'
import rewardsApi from '@/api/rewards'

export default defineComponent({
  name: 'AchievementList',
  setup() {
    const achievements = ref<UserAchievement[]>([])
    const loading = ref(true)

    const loadAchievements = async () => {
      try {
        const response = await rewardsApi.getUserAchievements()
        achievements.value = response.data
      } catch (error) {
        console.error('加载成就失败:', error)
        ElMessage.error('加载成就失败')
      } finally {
        loading.value = false
      }
    }

    const getProgressPercentage = (achievement: UserAchievement) => {
      if (achievement.completed) return 100
      // 根据不同成就类型计算进度
      switch (achievement.achievementType.name) {
        case 'first_course':
          return achievement.progress * 100
        case 'course_master':
          return (achievement.progress / 10) * 100
        case 'quick_learner':
          return (achievement.progress / 7) * 100
        case 'knowledge_seeker':
          return (achievement.progress / 6000) * 100 // 100小时 = 6000分钟
        default:
          return achievement.progress
      }
    }

    const formatDate = (dateStr?: string) => {
      if (!dateStr) return ''
      return dayjs(dateStr).format('YYYY-MM-DD')
    }

    onMounted(() => {
      loadAchievements()
    })

    return {
      achievements,
      loading,
      getProgressPercentage,
      formatDate
    }
  }
})
</script>

<style scoped>
.achievement-list {
  position: relative;
  min-height: 200px;
}

.achievement-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.achievement-item {
  background: var(--el-bg-color);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  gap: 16px;
  transition: all 0.3s ease;
  border: 1px solid var(--el-border-color-light);
}

.achievement-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.achievement-item.completed {
  border-color: var(--el-color-success-light);
  background: var(--el-color-success-light-9);
}

.achievement-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--el-color-primary-light-9);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--el-color-primary);
}

.achievement-item.completed .achievement-icon {
  background: var(--el-color-success-light-9);
  color: var(--el-color-success);
}

.achievement-info {
  flex: 1;
}

.achievement-info h4 {
  margin: 0 0 8px;
  font-size: 16px;
  color: var(--el-text-color-primary);
}

.achievement-info p {
  margin: 0 0 12px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.achievement-progress {
  margin-bottom: 12px;
}

.achievement-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.points {
  display: flex;
  align-items: center;
  gap: 4px;
}

.completion-date {
  font-style: italic;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--el-bg-color);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
</style> 