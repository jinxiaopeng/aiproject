<template>
  <div class="progress-tracker">
    <!-- 总体进度 -->
    <div class="overall-progress">
      <h3>学习进度</h3>
      <el-card class="progress-card">
        <div class="progress-stats">
          <div class="stat-item">
            <span class="label">完成挑战</span>
            <span class="value">{{ stats.completedChallenges }}</span>
          </div>
          <div class="stat-item">
            <span class="label">获得积分</span>
            <span class="value">{{ stats.totalPoints }}</span>
          </div>
          <div class="stat-item">
            <span class="label">学习时长</span>
            <span class="value">{{ formatTime(stats.totalTime) }}</span>
          </div>
        </div>
        <div class="level-progress">
          <div class="level-info">
            <span class="current-level">Level {{ stats.currentLevel }}</span>
            <span class="exp-info">{{ stats.currentExp }}/{{ stats.nextLevelExp }} EXP</span>
          </div>
          <el-progress 
            :percentage="(stats.currentExp / stats.nextLevelExp) * 100"
            :format="() => ''"
            :stroke-width="20"
            class="level-bar"
          />
        </div>
      </el-card>
    </div>

    <!-- 技能雷达图 -->
    <div class="skill-radar">
      <h3>技能分布</h3>
      <el-card class="radar-card">
        <div ref="radarChart" class="radar-chart"></div>
      </el-card>
    </div>

    <!-- 最近活动 -->
    <div class="recent-activities">
      <h3>最近活动</h3>
      <el-timeline>
        <el-timeline-item
          v-for="activity in recentActivities"
          :key="activity.id"
          :timestamp="activity.time"
          :type="activity.type"
        >
          {{ activity.content }}
          <template v-if="activity.achievement">
            <el-tag size="small" type="success" class="achievement-tag">
              {{ activity.achievement }}
            </el-tag>
          </template>
        </el-timeline-item>
      </el-timeline>
    </div>

    <!-- 成就系统 -->
    <div class="achievements">
      <h3>成就徽章</h3>
      <el-row :gutter="20">
        <el-col :span="8" v-for="badge in achievements" :key="badge.id">
          <el-card 
            class="badge-card"
            :class="{ 'badge-locked': !badge.unlocked }"
          >
            <div class="badge-icon">
              <el-icon :size="40">
                <component :is="badge.icon" />
              </el-icon>
            </div>
            <div class="badge-info">
              <h4>{{ badge.name }}</h4>
              <p>{{ badge.description }}</p>
              <el-progress 
                v-if="!badge.unlocked"
                :percentage="badge.progress"
                :format="percentageFormat"
              />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

// 总体统计数据
const stats = ref({
  completedChallenges: 15,
  totalPoints: 2500,
  totalTime: 3600 * 20, // 秒
  currentLevel: 5,
  currentExp: 450,
  nextLevelExp: 1000
})

// 格式化时间
const formatTime = (seconds: number) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}小时${minutes}分钟`
}

// 最近活动
const recentActivities = ref([
  {
    id: 1,
    content: '完成了"SQL注入基础"挑战',
    time: '2024-01-20 15:30',
    type: 'success',
    achievement: '初级黑客'
  },
  {
    id: 2,
    content: '开始学习"高级SQL注入"',
    time: '2024-01-20 14:20',
    type: 'primary'
  },
  {
    id: 3,
    content: '获得了100积分奖励',
    time: '2024-01-20 12:00',
    type: 'warning'
  }
])

// 成就系统
const achievements = ref([
  {
    id: 1,
    name: '初级黑客',
    description: '完成5个基础挑战',
    icon: 'Trophy',
    unlocked: true,
    progress: 100
  },
  {
    id: 2,
    name: 'SQL大师',
    description: '完成所有SQL注入相关挑战',
    icon: 'Database',
    unlocked: false,
    progress: 60
  },
  {
    id: 3,
    name: '不倦学者',
    description: '累计学习时间达到50小时',
    icon: 'Clock',
    unlocked: false,
    progress: 40
  }
])

const percentageFormat = (percentage: number) => {
  return `${percentage}%`
}

// 技能雷达图
const radarChart = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

onMounted(() => {
  if (radarChart.value) {
    chart = echarts.init(radarChart.value)
    const option = {
      radar: {
        indicator: [
          { name: 'SQL注入', max: 100 },
          { name: 'XSS攻击', max: 100 },
          { name: '密码学', max: 100 },
          { name: '网络安全', max: 100 },
          { name: '系统安全', max: 100 }
        ]
      },
      series: [{
        type: 'radar',
        data: [{
          value: [80, 60, 45, 70, 55],
          name: '技能分布',
          areaStyle: {
            color: 'rgba(0, 128, 255, 0.3)'
          },
          lineStyle: {
            color: '#0080ff'
          }
        }]
      }]
    }
    chart.setOption(option)
  }
})
</script>

<style scoped>
.progress-tracker {
  padding: 20px;
}

.overall-progress,
.skill-radar,
.recent-activities,
.achievements {
  margin-bottom: 30px;
}

h3 {
  margin-bottom: 20px;
  color: var(--el-text-color-primary);
}

.progress-card {
  padding: 20px;
}

.progress-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.stat-item .label {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 5px;
}

.stat-item .value {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.level-progress {
  margin-top: 20px;
}

.level-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.current-level {
  font-weight: bold;
  color: var(--el-color-success);
}

.exp-info {
  color: var(--el-text-color-secondary);
}

.radar-chart {
  height: 300px;
}

.achievement-tag {
  margin-left: 10px;
}

.badge-card {
  margin-bottom: 20px;
  text-align: center;
}

.badge-locked {
  opacity: 0.7;
}

.badge-icon {
  margin-bottom: 15px;
}

.badge-info h4 {
  margin: 10px 0;
  color: var(--el-text-color-primary);
}

.badge-info p {
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 10px;
}
</style> 