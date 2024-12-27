<template>
  <div class="system-stats">
    <el-card class="stats-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon><Operation /></el-icon>
            系统状态
          </h3>
          <el-tag 
            :type="getStatusType()" 
            effect="dark"
          >
            {{ getStatusText() }}
          </el-tag>
        </div>
      </template>
      
      <div class="stats-content">
        <div class="stats-grid">
          <div class="stats-item">
            <div class="item-label">运行时间</div>
            <div class="item-value">{{ formatUptime(stats.uptime) }}</div>
            <div class="item-desc">系统稳定运行</div>
          </div>
          <div class="stats-item">
            <div class="item-label">总用户数</div>
            <div class="item-value">{{ stats.total_users }}</div>
            <div class="item-desc">注册用户</div>
          </div>
          <div class="stats-item success">
            <div class="item-label">在线会话</div>
            <div class="item-value">{{ stats.active_sessions }}</div>
            <div class="item-desc">当前在线</div>
          </div>
          <div class="stats-item warning">
            <div class="item-label">响应时间</div>
            <div class="item-value">{{ stats.avg_response_time }}ms</div>
            <div class="item-desc">平均响应</div>
          </div>
        </div>

        <el-divider />
        
        <div class="performance">
          <h4>性能指标</h4>
          <div class="metrics-list">
            <div class="metric-item">
              <div class="metric-header">
                <span class="metric-name">CPU使用率</span>
                <span class="metric-value" :class="getMetricClass(stats.metrics.cpu_usage)">
                  {{ stats.metrics.cpu_usage }}%
                </span>
              </div>
              <el-progress 
                :percentage="stats.metrics.cpu_usage" 
                :color="getMetricColor(stats.metrics.cpu_usage)"
                :stroke-width="8"
              />
            </div>
            <div class="metric-item">
              <div class="metric-header">
                <span class="metric-name">内存使用</span>
                <span class="metric-value" :class="getMetricClass(stats.metrics.memory_usage)">
                  {{ stats.metrics.memory_usage }}%
                </span>
              </div>
              <el-progress 
                :percentage="stats.metrics.memory_usage" 
                :color="getMetricColor(stats.metrics.memory_usage)"
                :stroke-width="8"
              />
            </div>
            <div class="metric-item">
              <div class="metric-header">
                <span class="metric-name">磁盘使用</span>
                <span class="metric-value" :class="getMetricClass(stats.metrics.disk_usage)">
                  {{ stats.metrics.disk_usage }}%
                </span>
              </div>
              <el-progress 
                :percentage="stats.metrics.disk_usage" 
                :color="getMetricColor(stats.metrics.disk_usage)"
                :stroke-width="8"
              />
            </div>
          </div>
        </div>

        <el-divider />
        
        <div class="network">
          <h4>网络状态</h4>
          <div class="network-stats">
            <div class="network-item">
              <div class="item-header">
                <el-icon><Upload /></el-icon>
                <span>上行带宽</span>
              </div>
              <div class="item-value">{{ formatBandwidth(stats.network.outbound) }}</div>
            </div>
            <div class="network-item">
              <div class="item-header">
                <el-icon><Download /></el-icon>
                <span>下行带宽</span>
              </div>
              <div class="item-value">{{ formatBandwidth(stats.network.inbound) }}</div>
            </div>
            <div class="network-item">
              <div class="item-header">
                <el-icon><Connection /></el-icon>
                <span>连接数</span>
              </div>
              <div class="item-value">{{ stats.network.connections }}</div>
            </div>
            <div class="network-item">
              <div class="item-header">
                <el-icon><Warning /></el-icon>
                <span>错误率</span>
              </div>
              <div class="item-value" :class="getErrorRateClass()">
                {{ stats.network.error_rate }}%
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { 
  Operation,
  Upload,
  Download,
  Connection,
  Warning
} from '@element-plus/icons-vue'

interface SystemStats {
  uptime: number
  total_users: number
  active_sessions: number
  avg_response_time: number
  metrics: {
    cpu_usage: number
    memory_usage: number
    disk_usage: number
  }
  network: {
    inbound: number
    outbound: number
    connections: number
    error_rate: number
  }
}

const props = defineProps<{
  stats: SystemStats
}>()

// 获取状态类型
const getStatusType = () => {
  const { cpu_usage, memory_usage } = props.stats.metrics
  const { error_rate } = props.stats.network
  
  if (cpu_usage > 90 || memory_usage > 90 || error_rate > 5) return 'danger'
  if (cpu_usage > 70 || memory_usage > 70 || error_rate > 2) return 'warning'
  return 'success'
}

// 获取状态文本
const getStatusText = () => {
  const { cpu_usage, memory_usage } = props.stats.metrics
  const { error_rate } = props.stats.network
  
  if (cpu_usage > 90 || memory_usage > 90 || error_rate > 5) return '系统告警'
  if (cpu_usage > 70 || memory_usage > 70 || error_rate > 2) return '负载较高'
  return '运行正常'
}

// 格式化运行时间
const formatUptime = (seconds: number) => {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  
  if (days > 0) return `${days}天${hours}小时`
  if (hours > 0) return `${hours}小时${minutes}分`
  return `${minutes}分钟`
}

// 获取指标样式类
const getMetricClass = (value: number) => {
  if (value >= 90) return 'danger'
  if (value >= 70) return 'warning'
  return 'normal'
}

// 获取指标颜色
const getMetricColor = (value: number) => {
  if (value >= 90) return '#F56C6C'
  if (value >= 70) return '#E6A23C'
  return '#67C23A'
}

// 格式化带宽
const formatBandwidth = (bytes: number) => {
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

// 获取错误率样式类
const getErrorRateClass = () => {
  const rate = props.stats.network.error_rate
  if (rate > 5) return 'danger'
  if (rate > 2) return 'warning'
  return 'normal'
}
</script>

<style lang="scss" scoped>
.system-stats {
  .stats-card {
    background: var(--el-bg-color);
    border: none;
    
    :deep(.el-card__header) {
      padding: 15px 20px;
      border-bottom: 1px solid var(--el-border-color-light);
    }
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--el-text-color-primary);

      .el-icon {
        font-size: 18px;
        color: var(--el-color-warning);
      }
    }
  }

  .stats-content {
    padding: 10px 0;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    padding: 10px 0;

    .stats-item {
      text-align: center;
      
      .item-label {
        font-size: 13px;
        color: var(--el-text-color-secondary);
        margin-bottom: 5px;
      }
      
      .item-value {
        font-size: 24px;
        font-weight: bold;
        color: var(--el-text-color-primary);
      }

      .item-desc {
        font-size: 12px;
        color: var(--el-text-color-secondary);
        margin-top: 4px;
      }

      &.success .item-value {
        color: var(--el-color-success);
      }

      &.warning .item-value {
        color: var(--el-color-warning);
      }

      &.danger .item-value {
        color: var(--el-color-danger);
      }
    }
  }

  .performance {
    padding: 10px 0;

    h4 {
      margin: 0 0 12px;
      font-size: 14px;
      color: var(--el-text-color-regular);
    }

    .metrics-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .metric-item {
      .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;

        .metric-name {
          font-size: 13px;
          color: var(--el-text-color-secondary);
        }

        .metric-value {
          font-size: 13px;
          font-weight: 500;

          &.normal { color: var(--el-color-success); }
          &.warning { color: var(--el-color-warning); }
          &.danger { color: var(--el-color-danger); }
        }
      }
    }
  }

  .network {
    padding: 10px 0;

    h4 {
      margin: 0 0 12px;
      font-size: 14px;
      color: var(--el-text-color-regular);
    }

    .network-stats {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }

    .network-item {
      padding: 12px;
      border-radius: 6px;
      background: var(--el-fill-color-light);

      .item-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        color: var(--el-text-color-secondary);
        font-size: 13px;

        .el-icon {
          font-size: 16px;
        }
      }

      .item-value {
        font-size: 18px;
        font-weight: 600;
        color: var(--el-text-color-primary);

        &.normal { color: var(--el-color-success); }
        &.warning { color: var(--el-color-warning); }
        &.danger { color: var(--el-color-danger); }
      }
    }
  }
}
</style> 