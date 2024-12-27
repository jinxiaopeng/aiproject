<template>
  <div class="system-monitor">
    <!-- 顶部统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6" v-for="stat in systemStats" :key="stat.title">
        <el-card shadow="hover" :body-style="{ padding: '20px' }">
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon :size="24">
                <component :is="stat.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-value">
                {{ stat.value }}
                <small>{{ stat.unit }}</small>
              </div>
              <el-progress
                :percentage="stat.percentage"
                :status="getProgressStatus(stat.percentage)"
                :stroke-width="4"
                :show-text="false"
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 主要监控区域 -->
    <el-row :gutter="20" class="main-content">
      <!-- 左侧：资源使用趋势 -->
      <el-col :span="16">
        <el-card class="trend-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>资源使用趋势</span>
              <div class="header-actions">
                <el-radio-group v-model="resourceType" size="small">
                  <el-radio-button label="cpu">CPU</el-radio-button>
                  <el-radio-button label="memory">内存</el-radio-button>
                  <el-radio-button label="disk">磁盘</el-radio-button>
                  <el-radio-button label="network">网络</el-radio-button>
                </el-radio-group>
                <el-select v-model="timeRange" size="small">
                  <el-option label="最近1小时" value="1h" />
                  <el-option label="最近6小时" value="6h" />
                  <el-option label="最近24小时" value="24h" />
                  <el-option label="最近7天" value="7d" />
                </el-select>
              </div>
            </div>
          </template>
          <div class="chart-container">
            <ResourceTrendChart 
              :data="trendData" 
              :type="resourceType"
              :loading="loading.trend"
            />
          </div>
        </el-card>

        <!-- 实验环境状态 -->
        <el-card class="env-status" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>实验环境状态</span>
              <el-button type="primary" :icon="Refresh" @click="refreshEnvStatus">
                刷新
              </el-button>
            </div>
          </template>
          <el-table
            :data="envList"
            style="width: 100%"
            :max-height="300"
            v-loading="loading.env"
          >
            <el-table-column prop="name" label="环境名称" />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="{ row }">
                <el-tag>{{ row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getEnvStatusType(row.status)">
                  {{ getEnvStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="cpu" label="CPU" width="120">
              <template #default="{ row }">
                <el-progress
                  :percentage="row.cpu"
                  :status="getProgressStatus(row.cpu)"
                  :stroke-width="4"
                />
              </template>
            </el-table-column>
            <el-table-column prop="memory" label="内存" width="120">
              <template #default="{ row }">
                <el-progress
                  :percentage="row.memory"
                  :status="getProgressStatus(row.memory)"
                  :stroke-width="4"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  :disabled="row.status === 'stopped'"
                  @click="restartEnv(row)"
                >
                  重启
                </el-button>
                <el-button
                  type="primary"
                  link
                  @click="viewEnvDetail(row)"
                >
                  详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 右侧：实时监控 -->
      <el-col :span="8">
        <!-- 系统负载 -->
        <el-card class="load-monitor" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>系统负载</span>
              <el-tag :type="getLoadStatus(systemLoad.current)">
                {{ getLoadStatusText(systemLoad.current) }}
              </el-tag>
            </div>
          </template>
          <div class="load-info">
            <div class="load-item">
              <span class="label">1分钟</span>
              <span class="value">{{ systemLoad.last1 }}</span>
            </div>
            <div class="load-item">
              <span class="label">5分钟</span>
              <span class="value">{{ systemLoad.last5 }}</span>
            </div>
            <div class="load-item">
              <span class="label">15分钟</span>
              <span class="value">{{ systemLoad.last15 }}</span>
            </div>
          </div>
          <div class="chart-container">
            <LoadChart :data="loadHistory" :loading="loading.load" />
          </div>
        </el-card>

        <!-- 网络流量 -->
        <el-card class="network-monitor" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>网络流量</span>
            </div>
          </template>
          <div class="network-stats">
            <div class="stat-row">
              <span class="label">入站流量</span>
              <span class="value">{{ formatNetworkSpeed(networkStats.inbound) }}</span>
            </div>
            <div class="stat-row">
              <span class="label">出站流量</span>
              <span class="value">{{ formatNetworkSpeed(networkStats.outbound) }}</span>
            </div>
            <div class="stat-row">
              <span class="label">连接数</span>
              <span class="value">{{ networkStats.connections }}</span>
            </div>
          </div>
          <div class="chart-container">
            <NetworkChart :data="networkHistory" :loading="loading.network" />
          </div>
        </el-card>

        <!-- 磁盘使用 -->
        <el-card class="disk-monitor" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>磁盘使用</span>
            </div>
          </template>
          <div class="disk-list">
            <div 
              v-for="disk in diskUsage" 
              :key="disk.path"
              class="disk-item"
            >
              <div class="disk-info">
                <span class="path">{{ disk.path }}</span>
                <span class="space">
                  {{ formatStorage(disk.used) }} / {{ formatStorage(disk.total) }}
                </span>
              </div>
              <el-progress
                :percentage="(disk.used / disk.total) * 100"
                :status="getProgressStatus((disk.used / disk.total) * 100)"
                :stroke-width="4"
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Monitor, Refresh, CPU, Connection, DataLine } from '@element-plus/icons-vue'
import ResourceTrendChart from './components/ResourceTrendChart.vue'
import LoadChart from './components/LoadChart.vue'
import NetworkChart from './components/NetworkChart.vue'

// 系统统计数据
const systemStats = ref([
  {
    title: 'CPU使用率',
    value: '45.2',
    unit: '%',
    percentage: 45.2,
    icon: CPU
  },
  {
    title: '内存使用率',
    value: '3.8',
    unit: 'GB',
    percentage: 62.5,
    icon: Monitor
  },
  {
    title: '磁盘使用率',
    value: '156.2',
    unit: 'GB',
    percentage: 78.1,
    icon: DataLine
  },
  {
    title: '网络带宽',
    value: '125',
    unit: 'Mbps',
    percentage: 25,
    icon: Connection
  }
])

// 资源类型和时间范围选择
const resourceType = ref('cpu')
const timeRange = ref('1h')

// 加载状态
const loading = ref({
  trend: false,
  env: false,
  load: false,
  network: false
})

// 系统负载数据
const systemLoad = ref({
  current: 2.5,
  last1: 2.5,
  last5: 2.8,
  last15: 3.0
})

// 网络统计数据
const networkStats = ref({
  inbound: 1024 * 1024 * 5, // 5MB/s
  outbound: 1024 * 1024 * 3, // 3MB/s
  connections: 128
})

// 磁盘使用数据
const diskUsage = ref([
  {
    path: '/',
    total: 1024 * 1024 * 1024 * 500, // 500GB
    used: 1024 * 1024 * 1024 * 350 // 350GB
  },
  {
    path: '/data',
    total: 1024 * 1024 * 1024 * 1000, // 1TB
    used: 1024 * 1024 * 1024 * 600 // 600GB
  }
])

// 图表数据
const trendData = ref([])
const loadHistory = ref([])
const networkHistory = ref([])

// 实验环境列表
const envList = ref([
  {
    name: 'Web渗透测试环境',
    type: 'Web安全',
    status: 'running',
    cpu: 35,
    memory: 45
  },
  {
    name: '系统安全实验环境',
    type: '系统安全',
    status: 'running',
    cpu: 25,
    memory: 60
  },
  {
    name: '网络攻防环境',
    type: '网络安全',
    status: 'stopped',
    cpu: 0,
    memory: 0
  }
])

// 获取进度条状态
const getProgressStatus = (percentage: number) => {
  if (percentage >= 90) return 'exception'
  if (percentage >= 80) return 'warning'
  return 'normal'
}

// 获取环境状态样式
const getEnvStatusType = (status: string) => {
  const types = {
    running: 'success',
    stopped: 'info',
    error: 'danger'
  }
  return types[status] || 'info'
}

// 获取环境状态文本
const getEnvStatusText = (status: string) => {
  const texts = {
    running: '运行中',
    stopped: '已停止',
    error: '异常'
  }
  return texts[status] || '未知'
}

// 获取负载状态
const getLoadStatus = (load: number) => {
  if (load >= 5) return 'danger'
  if (load >= 3) return 'warning'
  return 'success'
}

// 获取负载状态文本
const getLoadStatusText = (load: number) => {
  if (load >= 5) return '过载'
  if (load >= 3) return '较高'
  return '正常'
}

// 格式化网络速度
const formatNetworkSpeed = (bytes: number) => {
  if (bytes >= 1024 * 1024 * 1024) {
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB/s`
  }
  if (bytes >= 1024 * 1024) {
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB/s`
  }
  if (bytes >= 1024) {
    return `${(bytes / 1024).toFixed(2)} KB/s`
  }
  return `${bytes} B/s`
}

// 格式化存储空间
const formatStorage = (bytes: number) => {
  if (bytes >= 1024 * 1024 * 1024 * 1024) {
    return `${(bytes / (1024 * 1024 * 1024 * 1024)).toFixed(2)} TB`
  }
  if (bytes >= 1024 * 1024 * 1024) {
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`
  }
  if (bytes >= 1024 * 1024) {
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
  }
  if (bytes >= 1024) {
    return `${(bytes / 1024).toFixed(2)} KB`
  }
  return `${bytes} B`
}

// 刷新环境状态
const refreshEnvStatus = async () => {
  loading.value.env = true
  try {
    // TODO: 实现数据加载逻辑
  } catch (error) {
    console.error('Failed to refresh environment status:', error)
  } finally {
    loading.value.env = false
  }
}

// 重启环境
const restartEnv = async (env: any) => {
  try {
    // TODO: 实现重启逻辑
  } catch (error) {
    console.error('Failed to restart environment:', error)
  }
}

// 查看环境详情
const viewEnvDetail = (env: any) => {
  // TODO: 实现查看详情逻辑
}

// 自动刷新定时器
let refreshTimer: number | null = null

// 加载数据
const loadData = async () => {
  // TODO: 实现数据加载逻辑
}

onMounted(() => {
  loadData()
  // 每10秒自动刷新一次
  refreshTimer = window.setInterval(loadData, 10000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style lang="scss" scoped>
.system-monitor {
  padding: 20px;

  .stat-cards {
    margin-bottom: 20px;
  }

  .stat-card {
    display: flex;
    align-items: center;
    gap: 16px;

    .stat-icon {
      padding: 12px;
      border-radius: 8px;
      background: var(--el-color-primary-light-9);
      color: var(--el-color-primary);
    }

    .stat-info {
      flex: 1;

      .stat-title {
        font-size: 14px;
        color: var(--el-text-color-secondary);
        margin-bottom: 8px;
      }

      .stat-value {
        font-size: 24px;
        font-weight: bold;
        line-height: 1;
        margin-bottom: 8px;

        small {
          font-size: 14px;
          font-weight: normal;
          margin-left: 4px;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }

  .main-content {
    .trend-card {
      margin-bottom: 20px;

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        .header-actions {
          display: flex;
          gap: 12px;
        }
      }

      .chart-container {
        height: 300px;
      }
    }

    .env-status {
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
    }
  }

  .load-monitor {
    margin-bottom: 20px;

    .load-info {
      display: flex;
      justify-content: space-between;
      margin-bottom: 16px;

      .load-item {
        text-align: center;

        .label {
          display: block;
          font-size: 12px;
          color: var(--el-text-color-secondary);
          margin-bottom: 4px;
        }

        .value {
          font-size: 20px;
          font-weight: bold;
        }
      }
    }

    .chart-container {
      height: 200px;
    }
  }

  .network-monitor {
    margin-bottom: 20px;

    .network-stats {
      margin-bottom: 16px;

      .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;

        .label {
          color: var(--el-text-color-secondary);
        }

        .value {
          font-weight: bold;
        }
      }
    }

    .chart-container {
      height: 200px;
    }
  }

  .disk-monitor {
    .disk-list {
      .disk-item {
        margin-bottom: 16px;

        &:last-child {
          margin-bottom: 0;
        }

        .disk-info {
          display: flex;
          justify-content: space-between;
          margin-bottom: 8px;

          .path {
            color: var(--el-text-color-secondary);
          }

          .space {
            font-weight: bold;
          }
        }
      }
    }
  }
}
</style>