# 创建新文件
<template>
  <div class="admin-dashboard">
    <el-row :gutter="20">
      <!-- 统计卡片 -->
      <el-col :span="6" v-for="stat in stats" :key="stat.title">
        <el-card class="stat-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon :size="20" :color="stat.color">
                <component :is="stat.icon" />
              </el-icon>
              <span>{{ stat.title }}</span>
            </div>
          </template>
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-change" :class="stat.trend">
            {{ stat.change }}% 
            <el-icon>
              <component :is="stat.trend === 'up' ? 'ArrowUp' : 'ArrowDown'" />
            </el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户活跃度趋势</span>
            </div>
          </template>
          <v-chart class="chart" :option="userTrendOption" autoresize />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>挑战完成情况</span>
            </div>
          </template>
          <v-chart class="chart" :option="challengeOption" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- 用户列表 -->
    <el-card class="user-list">
      <template #header>
        <div class="card-header">
          <span>最近活跃用户</span>
        </div>
      </template>
      <el-table :data="activeUsers" style="width: 100%">
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="lastActive" label="最近活动时间" />
        <el-table-column prop="completedChallenges" label="完成挑战数" />
        <el-table-column prop="score" label="总分" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  Monitor,
  User,
  Trophy,
  Star,
  ArrowUp,
  ArrowDown
} from '@element-plus/icons-vue'

// 统计数据
const stats = ref([
  {
    title: '总用户数',
    value: '156',
    change: 8.5,
    trend: 'up',
    icon: User,
    color: '#409EFF'
  },
  {
    title: '今日活跃',
    value: '32',
    change: 5.2,
    trend: 'up',
    icon: Monitor,
    color: '#67C23A'
  },
  {
    title: '挑战完成',
    value: '89',
    change: 8.1,
    trend: 'up',
    icon: Trophy,
    color: '#E6A23C'
  },
  {
    title: '平均分数',
    value: '72.5',
    change: 3.2,
    trend: 'down',
    icon: Star,
    color: '#F56C6C'
  }
])

// 用户趋势图表配置
const userTrendOption = ref({
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '活跃用户',
      type: 'line',
      smooth: true,
      data: [20, 32, 25, 34, 28, 45, 38],
      itemStyle: {
        color: '#409EFF'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            {
              offset: 0,
              color: 'rgba(64,158,255,0.2)'
            },
            {
              offset: 1,
              color: 'rgba(64,158,255,0)'
            }
          ]
        }
      }
    }
  ]
})

// 挑战完成情况图表配置
const challengeOption = ref({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    right: 10,
    top: 'center'
  },
  series: [
    {
      name: '挑战完成情况',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '16',
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 35, name: 'Web安全' },
        { value: 25, name: '密码学' },
        { value: 18, name: '逆向工程' },
        { value: 15, name: '二进制' },
        { value: 12, name: '其他' }
      ]
    }
  ]
})

// 活跃用户数据
const activeUsers = ref([
  {
    username: 'user1',
    lastActive: '2024-01-20 15:30',
    completedChallenges: 5,
    score: 380
  },
  {
    username: 'user2',
    lastActive: '2024-01-20 14:20',
    completedChallenges: 3,
    score: 250
  },
  {
    username: 'user3',
    lastActive: '2024-01-20 13:45',
    completedChallenges: 7,
    score: 520
  }
])

onMounted(() => {
  // 这里可以添加初始化逻辑，比如从API获取数据
})
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  background: #1a1d21;
  min-height: 100vh;
}

.stat-card {
  margin-bottom: 20px;
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.stat-card :deep(.el-card__header) {
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #e5eaf3;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  margin: 10px 0;
  color: #e5eaf3;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.stat-change.up {
  color: #67C23A;
}

.stat-change.down {
  color: #F56C6C;
}

.chart-row {
  margin: 20px 0;
}

.chart-card {
  height: 360px;
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.chart-card :deep(.el-card__header) {
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
}

.chart {
  height: 280px;
}

.user-list {
  margin-top: 20px;
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.user-list :deep(.el-card__header) {
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
}

.user-list :deep(.el-table) {
  background: transparent;
  color: #e5eaf3;
}

.user-list :deep(.el-table tr) {
  background: transparent;
}

.user-list :deep(.el-table th) {
  background: rgba(0, 0, 0, 0.2);
  color: #e5eaf3;
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
}

.user-list :deep(.el-table td) {
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
}

:deep(.el-table--enable-row-hover .el-table__body tr:hover > td) {
  background-color: rgba(65, 184, 131, 0.1);
}
</style> 