<!-- 日志查看组件 -->
<template>
  <div class="log-viewer">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>运行日志</span>
          <div class="header-actions">
            <el-switch
              v-model="autoScroll"
              active-text="自动滚动"
            />
            <el-button 
              type="text" 
              @click="refreshLogs"
              :loading="refreshing"
            >
              刷新
            </el-button>
          </div>
        </div>
      </template>

      <!-- 日志内容 -->
      <div 
        class="log-content" 
        ref="logContainer"
        @scroll="handleScroll"
      >
        <div 
          v-for="(log, index) in logs" 
          :key="index"
          class="log-line"
          :class="{ 'error': log.includes('[ERROR]') }"
        >
          {{ log }}
        </div>

        <div v-if="logs.length === 0" class="no-logs">
          暂无日志
        </div>
      </div>

      <!-- 日志控制 -->
      <div class="log-controls">
        <el-button-group>
          <el-button 
            type="primary" 
            :icon="Download"
            @click="downloadLogs"
          >
            下载日志
          </el-button>
          <el-button 
            type="danger" 
            :icon="Delete"
            @click="clearLogs"
          >
            清空日志
          </el-button>
        </el-button-group>

        <el-select 
          v-model="logLevel" 
          placeholder="日志级别"
          style="width: 120px"
        >
          <el-option label="全部" value="all" />
          <el-option label="错误" value="error" />
          <el-option label="警告" value="warning" />
          <el-option label="信息" value="info" />
        </el-select>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, Delete } from '@element-plus/icons-vue'
import { getRecentLogs } from '@/api/process'

const props = defineProps<{
  challengeId: string
  maxLines?: number
}>()

// 状态变量
const logs = ref<string[]>([])
const refreshing = ref(false)
const autoScroll = ref(true)
const logLevel = ref('all')
const logContainer = ref<HTMLElement | null>(null)

// 计算属性
const filteredLogs = computed(() => {
  if (logLevel.value === 'all') return logs.value
  
  return logs.value.filter(log => {
    switch (logLevel.value) {
      case 'error':
        return log.includes('[ERROR]')
      case 'warning':
        return log.includes('[WARN]')
      case 'info':
        return log.includes('[INFO]')
      default:
        return true
    }
  })
})

// 方法
async function refreshLogs() {
  if (refreshing.value) return
  refreshing.value = true
  
  try {
    const result = await getRecentLogs(props.challengeId, props.maxLines || 100)
    logs.value = result
    
    if (autoScroll.value) {
      scrollToBottom()
    }
  } catch (error) {
    ElMessage.error('获取日志失败')
  } finally {
    refreshing.value = false
  }
}

function scrollToBottom() {
  if (!logContainer.value) return
  
  setTimeout(() => {
    logContainer.value!.scrollTop = logContainer.value!.scrollHeight
  }, 0)
}

function handleScroll(event: Event) {
  const target = event.target as HTMLElement
  const { scrollTop, scrollHeight, clientHeight } = target
  
  // 如果用户手动滚动到接近底部，启用自动滚动
  if (scrollHeight - scrollTop - clientHeight < 50) {
    autoScroll.value = true
  } else {
    autoScroll.value = false
  }
}

function downloadLogs() {
  const content = filteredLogs.value.join('\n')
  const blob = new Blob([content], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = `challenge-${props.challengeId}-logs.txt`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

function clearLogs() {
  logs.value = []
  ElMessage.success('日志已清空')
}

// 自动刷新
let refreshTimer: number
onMounted(() => {
  refreshLogs()
  refreshTimer = setInterval(refreshLogs, 5000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.log-viewer {
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

.log-content {
  height: 400px;
  overflow-y: auto;
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 10px;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.5;
  border-radius: 4px;
}

.log-line {
  white-space: pre-wrap;
  word-break: break-all;
}

.log-line.error {
  color: #f56c6c;
}

.no-logs {
  text-align: center;
  color: #666;
  padding: 20px;
}

.log-controls {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 