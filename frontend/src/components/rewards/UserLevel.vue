<!-- 用户等级和积分展示组件 -->
<template>
  <div class="user-level">
    <div class="level-card">
      <div class="level-header">
        <div class="level-info">
          <div class="level-badge">
            <el-icon :size="32">
              <component :is="currentRule?.icon || 'User'" />
            </el-icon>
            <span class="level-number">Lv.{{ userLevel?.level || 1 }}</span>
          </div>
          <div class="level-title">
            <h3>{{ currentRule?.title || '新手' }}</h3>
            <p>{{ getNextLevelText() }}</p>
          </div>
        </div>
        <div class="level-points">
          <span class="current-points">{{ userLevel?.currentPoints || 0 }}</span>
          <span class="total-points">/ {{ userLevel?.nextLevelPoints || 500 }}</span>
        </div>
      </div>

      <div class="level-progress">
        <el-progress 
          :percentage="getProgressPercentage()"
          :format="formatProgress"
          :stroke-width="10"
        />
      </div>

      <div class="level-rewards" v-if="currentRule?.rewards">
        <h4>当前等级特权</h4>
        <ul class="rewards-list">
          <li v-for="(reward, key) in currentRule.rewards" :key="key">
            <el-icon><Check /></el-icon>
            <span>{{ reward }}</span>
          </li>
        </ul>
      </div>

      <div class="point-history">
        <h4>最近积分记录</h4>
        <el-timeline>
          <el-timeline-item
            v-for="record in pointHistory"
            :key="record.id"
            :timestamp="formatDate(record.createdAt)"
            :type="getPointType(record.points)"
            :hollow="true"
            size="small"
          >
            <div class="history-item">
              <span class="history-description">{{ record.description }}</span>
              <span :class="['history-points', getPointType(record.points)]">
                {{ record.points > 0 ? '+' : '' }}{{ record.points }}
              </span>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import type { UserLevel, LevelRule, PointHistory } from '@/api/rewards'
import rewardsApi from '@/api/rewards'

export default defineComponent({
  name: 'UserLevel',
  setup() {
    const userLevel = ref<UserLevel | null>(null)
    const levelRules = ref<LevelRule[]>([])
    const pointHistory = ref<PointHistory[]>([])

    const currentRule = computed(() => {
      if (!userLevel.value || !levelRules.value.length) return null
      return levelRules.value.find(rule => rule.level === userLevel.value?.level)
    })

    const loadUserLevel = async () => {
      try {
        const response = await rewardsApi.getUserLevel()
        userLevel.value = response.data
      } catch (error) {
        console.error('加载用户等级失败:', error)
      }
    }

    const loadLevelRules = async () => {
      try {
        const response = await rewardsApi.getLevelRules()
        levelRules.value = response.data
      } catch (error) {
        console.error('加载等级规则失败:', error)
      }
    }

    const loadPointHistory = async () => {
      try {
        const response = await rewardsApi.getPointHistory(5)
        pointHistory.value = response.data
      } catch (error) {
        console.error('加载积分历史失败:', error)
      }
    }

    const getProgressPercentage = () => {
      if (!userLevel.value) return 0
      const { currentPoints, nextLevelPoints } = userLevel.value
      return Math.min(100, (currentPoints / nextLevelPoints) * 100)
    }

    const formatProgress = (percentage: number) => {
      return `${percentage.toFixed(1)}%`
    }

    const getNextLevelText = () => {
      if (!userLevel.value || !levelRules.value.length) return ''
      const nextRule = levelRules.value.find(rule => rule.level === userLevel.value!.level + 1)
      if (!nextRule) return '已达到最高等级'
      const remainingPoints = userLevel.value.nextLevelPoints - userLevel.value.currentPoints
      return `还需 ${remainingPoints} 积分升级到 ${nextRule.title}`
    }

    const getPointType = (points: number) => {
      return points > 0 ? 'success' : 'danger'
    }

    const formatDate = (dateStr: string) => {
      return dayjs(dateStr).format('MM-DD HH:mm')
    }

    onMounted(async () => {
      await Promise.all([
        loadUserLevel(),
        loadLevelRules(),
        loadPointHistory()
      ])
    })

    return {
      userLevel,
      currentRule,
      pointHistory,
      getProgressPercentage,
      formatProgress,
      getNextLevelText,
      getPointType,
      formatDate
    }
  }
})
</script>

<style scoped>
.user-level {
  max-width: 800px;
  margin: 0 auto;
}

.level-card {
  background: var(--el-bg-color);
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.level-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.level-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.level-badge {
  position: relative;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--el-color-primary-light-9);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--el-color-primary);
}

.level-number {
  position: absolute;
  bottom: -4px;
  right: -4px;
  background: var(--el-color-primary);
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
}

.level-title h3 {
  margin: 0 0 4px;
  font-size: 20px;
  color: var(--el-text-color-primary);
}

.level-title p {
  margin: 0;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.level-points {
  text-align: right;
}

.current-points {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.total-points {
  font-size: 16px;
  color: var(--el-text-color-secondary);
}

.level-progress {
  margin-bottom: 24px;
}

.level-rewards {
  margin-bottom: 24px;
}

.level-rewards h4 {
  margin: 0 0 12px;
  font-size: 16px;
  color: var(--el-text-color-primary);
}

.rewards-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.rewards-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  color: var(--el-text-color-regular);
}

.point-history h4 {
  margin: 0 0 16px;
  font-size: 16px;
  color: var(--el-text-color-primary);
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-description {
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.history-points {
  font-weight: bold;
}

.history-points.success {
  color: var(--el-color-success);
}

.history-points.danger {
  color: var(--el-color-danger);
}
</style> 