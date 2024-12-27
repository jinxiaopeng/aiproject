<!-- 靶场进程控制组件 -->
<template>
  <div class="process-control">
    <!-- 进程状态展示 -->
    <div class="status-panel">
      <el-tag :type="statusType">{{ processStatus }}</el-tag>
      <span v-if="processInfo.pid" class="pid">PID: {{ processInfo.pid }}</span>
      <span v-if="processInfo.port" class="port">Port: {{ processInfo.port }}</span>
    </div>

    <!-- 控制按钮 -->
    <div class="control-panel">
      <el-button 
        type="primary" 
        @click="startProcess"
        :loading="starting"
        :disabled="isRunning"
      >
        启动靶场
      </el-button>
      
      <el-button 
        type="danger" 
        @click="stopProcess"
        :loading="stopping"
        :disabled="!isRunning"
      >
        停止靶场
      </el-button>

      <el-button 
        type="warning" 
        @click="refreshStatus"
        :loading="refreshing"
      >
        刷新状态
      </el-button>
    </div>

    <!-- 资源使用信息 -->
    <div class="resource-info" v-if="isRunning">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-progress 
            type="dashboard" 
            :percentage="cpuUsage" 
            :color="cpuColor"
          >
            <template #default>
              <div>CPU</div>
              <div>{{ cpuUsage }}%</div>
            </template>
          </el-progress>
        </el-col>
        <el-col :span="12">
          <el-progress 
            type="dashboard" 
            :percentage="memoryUsage" 
            :color="memoryColor"
          >
            <template #default>
              <div>内存</div>
              <div>{{ memoryUsage }}%</div>
            </template>
          </el-progress>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { ProcessStatus } from '@/api/process'
import { 
  startChallengeProcess, 
  stopChallengeProcess,
  getChallengeProcessStatus 
} from '@/api/process'

const props = defineProps<{
  challengeId: string
}>()

// 状态变量
const processInfo = ref<ProcessStatus>({
  status: 'stopped',
  pid: undefined,
  port: undefined,
  cpu_percent: 0,
  memory_percent: 0,
  run_time: 0
})

const starting = ref(false)
const stopping = ref(false)
const refreshing = ref(false)

// 计算属性
const isRunning = computed(() => processInfo.value.status === 'running')

const statusType = computed(() => {
  switch (processInfo.value.status) {
    case 'running': return 'success'
    case 'stopped': return 'info'
    case 'error': return 'danger'
    default: return 'warning'
  }
})

const processStatus = computed(() => {
  switch (processInfo.value.status) {
    case 'running': return '运行中'
    case 'stopped': return '已停止'
    case 'error': return '错误'
    default: return '未知'
  }
})

const cpuUsage = computed(() => Math.round(processInfo.value.cpu_percent || 0))
const memoryUsage = computed(() => Math.round(processInfo.value.memory_percent || 0))

const cpuColor = computed(() => {
  const usage = cpuUsage.value
  if (usage > 80) return '#F56C6C'
  if (usage > 60) return '#E6A23C'
  return '#67C23A'
})

const memoryColor = computed(() => {
  const usage = memoryUsage.value
  if (usage > 80) return '#F56C6C'
  if (usage > 60) return '#E6A23C'
  return '#67C23A'
})

// 方法
async function startProcess() {
  if (starting.value) return
  starting.value = true
  
  try {
    const result = await startChallengeProcess(props.challengeId)
    processInfo.value = result
    ElMessage.success('靶场启动成功')
  } catch (error) {
    ElMessage.error('靶场启动失败')
  } finally {
    starting.value = false
  }
}

async function stopProcess() {
  if (stopping.value) return
  stopping.value = true
  
  try {
    const result = await stopChallengeProcess(props.challengeId)
    processInfo.value = result
    ElMessage.success('靶场已停止')
  } catch (error) {
    ElMessage.error('停止失败')
  } finally {
    stopping.value = false
  }
}

async function refreshStatus() {
  if (refreshing.value) return
  refreshing.value = true
  
  try {
    const result = await getChallengeProcessStatus(props.challengeId)
    processInfo.value = result
  } catch (error) {
    ElMessage.error('获取状态失败')
  } finally {
    refreshing.value = false
  }
}

// 自动刷新状态
let refreshTimer: number
onMounted(() => {
  refreshStatus()
  refreshTimer = setInterval(refreshStatus, 5000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.process-control {
  padding: 20px;
}

.status-panel {
  margin-bottom: 20px;
}

.pid, .port {
  margin-left: 15px;
  color: #666;
}

.control-panel {
  margin-bottom: 30px;
}

.control-panel .el-button {
  margin-right: 15px;
}

.resource-info {
  margin-top: 30px;
}
</style>