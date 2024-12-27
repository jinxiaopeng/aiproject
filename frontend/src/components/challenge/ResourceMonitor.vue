<!-- 资源监控组件 -->
<template>
  <div class="resource-monitor">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>资源监控</span>
          <div class="header-actions">
            <el-button 
              type="text" 
              @click="refreshStats"
              :loading="refreshing"
            >
              刷新
            </el-button>
          </div>
        </div>
      </template>

      <!-- 资源使用统计 -->
      <div class="stats-panel">
        <!-- CPU使用率 -->
        <div class="stat-item">
          <h4>CPU使用率</h4>
          <el-progress 
            type="dashboard" 
            :percentage="cpuUsage" 
            :color="getResourceColor(cpuUsage)"
          >
            <template #default>
              <div class="progress-label">
                <span>{{ cpuUsage }}%</span>
                <small v-if="cpuLimit">限制: {{ cpuLimit }}%</small>
              </div>
            </template>
          </el-progress>
        </div>

        <!-- 内存使用率 -->
        <div class="stat-item">
          <h4>内存使用率</h4>
          <el-progress 
            type="dashboard" 
            :percentage="memoryUsage" 
            :color="getResourceColor(memoryUsage)"
          >
            <template #default>
              <div class="progress-label">
                <span>{{ memoryUsage }}%</span>
                <small v-if="memoryLimit">限制: {{ formatMemory(memoryLimit) }}</small>
              </div>
            </template>
          </el-progress>
        </div>

        <!-- 运行时间 -->
        <div class="stat-item">
          <h4>运行时间</h4>
          <div class="runtime">
            {{ formatRuntime(runTime) }}
          </div>
        </div>
      </div>

      <!-- 告警信息 -->
      <div class="alerts-panel">
        <div class="alerts-header">
          <h4>告警记录</h4>
          <el-button 
            type="text" 
            @click="refreshAlerts"
            :loading="refreshingAlerts"
          >
            刷新
          </el-button>
        </div>

        <el-collapse v-model="activeAlerts">
          <el-collapse-item 
            v-for="alert in alerts" 
            :key="alert.id"
            :name="alert.id"
          >
            <template #title>
              <el-tag 
                :type="getAlertType(alert.severity)"
                size="small"
                class="alert-tag"
              >
                {{ alert.alert_type.toUpperCase() }}
              </el-tag>
              {{ alert.message }}
              <span class="alert-time">
                {{ formatAlertTime(alert.timestamp) }}
              </span>
            </template>
            
            <div class="alert-detail">
              <p>当前值: {{ alert.current_value.toFixed(2) }}%</p>
              <p>阈值: {{ alert.limit_value.toFixed(2) }}%</p>
              <p>时间: {{ formatDateTime(alert.timestamp) }}</p>
            </div>
          </el-collapse-item>
        </el-collapse>

        <div v-if="alerts.length === 0" class="no-alerts">
          暂无告警记录
        </div>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { ProcessStatus, ResourceAlert } from '@/api/process'
import { getChallengeProcessStatus, getChallengeAlerts } from '@/api/process'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const props = defineProps<{
  challengeId: string
  cpuLimit?: number
  memoryLimit?: number
}>()

// 状态变量
const stats = ref<ProcessStatus>({
  status: 'stopped',
  cpu_percent: 0,
  memory_percent: 0,
  run_time: 0
})

const alerts = ref<ResourceAlert[]>([])
const activeAlerts = ref<string[]>([])
const refreshing = ref(false)
const refreshingAlerts = ref(false)

// 计算属性
const cpuUsage = computed(() => Math.round(stats.value.cpu_percent || 0))
const memoryUsage = computed(() => Math.round(stats.value.memory_percent || 0))
const runTime = computed(() => stats.value.run_time || 0)

// 方法
function getResourceColor(usage: number) {
  if (usage > 80) return '#F56C6C'
  if (usage > 60) return '#E6A23C'
  return '#67C23A'
}

function getAlertType(severity: string) {
  switch (severity) {
    case 'error': return 'danger'
    case 'warning': return 'warning'
    default: return 'info'
  }
}

function formatMemory(bytes: number) {
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  
  return `${Math.round(size)}${units[unitIndex]}`
}

function formatRuntime(seconds: number) {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  return `${hours}h ${minutes}m ${secs}s`
}

function formatAlertTime(timestamp: string) {
  return formatDistanceToNow(new Date(timestamp), {
    addSuffix: true,
    locale: zhCN
  })
}

function formatDateTime(timestamp: string) {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

async function refreshStats() {
  if (refreshing.value) return
  refreshing.value = true
  
  try {
    const result = await getChallengeProcessStatus(props.challengeId)
    stats.value = result
  } catch (error) {
    ElMessage.error('获取资源统计失败')
  } finally {
    refreshing.value = false
  }
}

async function refreshAlerts() {
  if (refreshingAlerts.value) return
  refreshingAlerts.value = true
  
  try {
    const result = await getChallengeAlerts(props.challengeId)
    alerts.value = result
  } catch (error) {
    ElMessage.error('获取告警记录失败')
  } finally {
    refreshingAlerts.value = false
  }
}

// 自动刷新
let refreshTimer: number
let alertsTimer: number

onMounted(() => {
  refreshStats()
  refreshAlerts()
  refreshTimer = setInterval(refreshStats, 5000)
  alertsTimer = setInterval(refreshAlerts, 30000)  // 每30秒刷新一次告警
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
  if (alertsTimer) {
    clearInterval(alertsTimer)
  }
})
</script>

<style scoped>
.resource-monitor {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stats-panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.stat-item h4 {
  margin-bottom: 15px;
  color: #666;
}

.progress-label {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.progress-label small {
  margin-top: 5px;
  color: #999;
  font-size: 12px;
}

.runtime {
  font-size: 24px;
  color: #409EFF;
  margin-top: 20px;
}

.alerts-panel {
  margin-top: 30px;
}

.alerts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.alerts-header h4 {
  margin: 0;
  color: #666;
}

.alert-tag {
  margin-right: 10px;
}

.alert-time {
  margin-left: 10px;
  color: #999;
  font-size: 12px;
}

.alert-detail {
  padding: 10px;
  background: #f8f8f8;
  border-radius: 4px;
}

.alert-detail p {
  margin: 5px 0;
  color: #666;
}

.no-alerts {
  text-align: center;
  color: #999;
  padding: 20px;
}
</style> 