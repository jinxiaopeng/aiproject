<template>
  <div class="tracking-stats">
    <!-- 解题用时统计 -->
    <div class="stats-card">
      <h3>解题用时统计</h3>
      <el-table :data="timeStats" style="width: 100%">
        <el-table-column prop="challengeTitle" label="靶场名称" />
        <el-table-column prop="startTime" label="开始时间">
          <template #default="{ row }">
            {{ formatTime(row.startTime) }}
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="用时">
          <template #default="{ row }">
            {{ formatDuration(row.duration) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 'completed' ? 'success' : 'warning'">
              {{ row.status === 'completed' ? '已完成' : '进行中' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 完成度记录 -->
    <div class="stats-card">
      <h3>完成度记录</h3>
      <div class="completion-stats">
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ stats.totalAttempts }}</div>
              <div class="stat-label">总尝试次数</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ stats.successRate }}%</div>
              <div class="stat-label">成功率</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ stats.averageTime }}</div>
              <div class="stat-label">平均用时</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 得分统计 -->
    <div class="stats-card">
      <h3>得分统计</h3>
      <div class="score-chart">
        <el-progress
          type="dashboard"
          :percentage="stats.completionRate"
          :color="progressColor"
        >
          <template #default="{ percentage }">
            <div class="score-info">
              <div class="total-score">{{ stats.totalScore }}</div>
              <div class="score-label">总分</div>
            </div>
          </template>
        </el-progress>
      </div>
      <div class="score-details">
        <div class="score-item">
          <span class="label">本周得分</span>
          <span class="value">+{{ stats.weeklyScore }}</span>
        </div>
        <div class="score-item">
          <span class="label">排名</span>
          <span class="value">#{{ stats.ranking }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import dayjs from 'dayjs'

// 模拟数据
const timeStats = ref([
  {
    challengeTitle: 'SQL注入基础',
    startTime: '2023-12-19T10:00:00',
    duration: 3600,
    status: 'completed'
  },
  {
    challengeTitle: 'XSS攻防',
    startTime: '2023-12-19T14:00:00',
    duration: 1800,
    status: 'in_progress'
  }
])

const stats = ref({
  totalAttempts: 25,
  successRate: 85,
  averageTime: '45分钟',
  totalScore: 1250,
  weeklyScore: 350,
  ranking: 12,
  completionRate: 75
})

const progressColor = computed(() => {
  const rate = stats.value.completionRate
  if (rate < 30) return '#f56c6c'
  if (rate < 70) return '#e6a23c'
  return '#67c23a'
})

// 时间格式化
const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

// 时长格式化
const formatDuration = (seconds: number) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}小时${minutes}分钟`
}
</script>

<style scoped>
.tracking-stats {
  padding: 20px;
}

.stats-card {
  background: var(--el-bg-color);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stats-card h3 {
  margin: 0 0 20px 0;
  color: var(--el-text-color-primary);
}

.completion-stats {
  margin-top: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.stat-label {
  margin-top: 8px;
  color: var(--el-text-color-secondary);
}

.score-chart {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.score-info {
  text-align: center;
}

.total-score {
  font-size: 28px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.score-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.score-details {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.score-item {
  text-align: center;
}

.score-item .label {
  display: block;
  color: var(--el-text-color-secondary);
  margin-bottom: 5px;
}

.score-item .value {
  font-size: 18px;
  font-weight: bold;
  color: var(--el-color-success);
}
</style> 