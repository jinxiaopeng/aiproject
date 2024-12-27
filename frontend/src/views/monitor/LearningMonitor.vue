<template>
  <div class="monitor-page">
    <el-card class="monitor-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <h3>学习监控</h3>
          <el-button type="primary" :icon="RefreshIcon" @click="fetchLearningStats" :loading="loading">
            刷新
          </el-button>
        </div>
      </template>
      
      <div class="monitor-content">
        <div class="learning-monitor">
          <div class="overview-section">
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="stat-item">
                  <div class="stat-value">{{ stats.video_stats.completion_rate }}%</div>
                  <div class="stat-label">视频完成率</div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item">
                  <div class="stat-value">{{ stats.challenge_stats.completion_rate }}%</div>
                  <div class="stat-label">实验完成率</div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item">
                  <div class="stat-value">{{ stats.challenge_stats.total_score }}</div>
                  <div class="stat-label">总得分</div>
                </div>
              </el-col>
            </el-row>
          </div>

          <div class="trend-section">
            <h4>学习趋势</h4>
            <el-table :data="stats.daily_stats" style="width: 100%" v-loading="loading">
              <el-table-column prop="date" label="日期" width="180" />
              <el-table-column prop="study_time" label="学习时长(分钟)">
                <template #default="scope">
                  {{ Math.round(scope.row.study_time / 60) }}
                </template>
              </el-table-column>
              <el-table-column prop="videos_completed" label="完成视频数" />
              <el-table-column prop="challenges_completed" label="完成实验数" />
              <el-table-column prop="score_gained" label="获得分数" />
            </el-table>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Refresh as RefreshIcon } from '@element-plus/icons-vue'
import { learningAPI } from '@/api/learning'
import { ElMessage } from 'element-plus'

const activeTab = ref('network')

interface DailyStat {
  date: string
  study_time: number
  videos_completed: number
  challenges_completed: number
  score_gained: number
}

interface VideoStats {
  total: number
  completed: number
  completion_rate: number
}

interface ChallengeStats {
  total: number
  completed: number
  completion_rate: number
  total_score: number
}

interface Stats {
  daily_stats: DailyStat[]
  video_stats: VideoStats
  challenge_stats: ChallengeStats
}

const loading = ref(false)
const stats = ref<Stats>({
  daily_stats: [],
  video_stats: {
    total: 0,
    completed: 0,
    completion_rate: 0
  },
  challenge_stats: {
    total: 0,
    completed: 0,
    completion_rate: 0,
    total_score: 0
  }
})

const fetchLearningStats = async () => {
  try {
    loading.value = true
    const { data } = await learningAPI.getUserStats(1, 7)
    stats.value = data
  } catch (error) {
    console.error('获取学习统计数据失败:', error)
    ElMessage.error('获取学习统计数据失败')
  } finally {
    loading.value = false
  }
}

let refreshTimer: number | null = null

onMounted(() => {
  fetchLearningStats()
  refreshTimer = window.setInterval(fetchLearningStats, 5 * 60 * 1000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style lang="scss" scoped>
.monitor-page {
  padding: 20px;
  
  .monitor-card {
    margin-bottom: 20px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h3 {
      margin: 0;
    }
  }
  
  .monitor-content {
    min-height: 500px;
  }

  .learning-monitor {
    .overview-section {
      margin-bottom: 20px;
    }

    .trend-section {
      h4 {
        margin-bottom: 15px;
      }
    }

    .stat-item {
      text-align: center;
      padding: 20px;
      background-color: var(--el-bg-color-overlay);
      border-radius: 4px;
      
      .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: var(--el-color-primary);
      }
      
      .stat-label {
        margin-top: 8px;
        color: var(--el-text-color-secondary);
      }
    }
  }
}
</style>