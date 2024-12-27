<template>
  <div class="realtime-log">
    <div 
      ref="logContainerRef"
      class="log-container"
      @scroll="handleScroll"
    >
      <div 
        v-for="log in logs" 
        :key="log.id"
        class="log-item"
        :class="[`level-${log.level}`, `type-${log.type}`]"
      >
        <div class="log-header">
          <div class="log-meta">
            <el-tag 
              size="small" 
              :type="getLogLevelType(log.level)"
              class="level-tag"
            >
              {{ getLogLevelText(log.level) }}
            </el-tag>
            <el-tag 
              size="small"
              :type="getLogTypeType(log.type)"
              class="type-tag"
            >
              {{ getLogTypeText(log.type) }}
            </el-tag>
            <span class="timestamp">{{ formatTime(log.timestamp) }}</span>
          </div>
          <div class="log-actions">
            <el-tooltip content="复制日志" placement="top">
              <el-button
                type="primary"
                link
                :icon="DocumentCopy"
                @click="copyLog(log)"
              />
            </el-tooltip>
            <el-tooltip content="查看详情" placement="top">
              <el-button
                type="primary"
                link
                :icon="InfoFilled"
                @click="viewLogDetail(log)"
              />
            </el-tooltip>
          </div>
        </div>
        <div class="log-content">
          {{ log.message }}
        </div>
      </div>

      <div v-if="logs.length === 0" class="empty-logs">
        <el-empty description="暂无日志" />
      </div>
    </div>

    <!-- 日志详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="日志详情"
      width="600px"
      destroy-on-close
    >
      <div v-if="currentLog" class="log-detail">
        <div class="detail-item">
          <span class="item-label">日志ID</span>
          <span class="item-value">{{ currentLog.id }}</span>
        </div>
        <div class="detail-item">
          <span class="item-label">时间</span>
          <span class="item-value">{{ formatDetailTime(currentLog.timestamp) }}</span>
        </div>
        <div class="detail-item">
          <span class="item-label">类型</span>
          <span class="item-value">
            <el-tag 
              size="small"
              :type="getLogTypeType(currentLog.type)"
            >
              {{ getLogTypeText(currentLog.type) }}
            </el-tag>
          </span>
        </div>
        <div class="detail-item">
          <span class="item-label">等级</span>
          <span class="item-value">
            <el-tag 
              size="small"
              :type="getLogLevelType(currentLog.level)"
            >
              {{ getLogLevelText(currentLog.level) }}
            </el-tag>
          </span>
        </div>
        <div class="detail-item">
          <span class="item-label">消息</span>
          <span class="item-value">{{ currentLog.message }}</span>
        </div>
        <div class="detail-item" v-if="currentLog.details">
          <span class="item-label">详细信息</span>
          <div class="item-value">
            <pre>{{ JSON.stringify(currentLog.details, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { DocumentCopy, InfoFilled } from '@element-plus/icons-vue'
import type { MonitorLog } from '@/types/monitor'
import dayjs from 'dayjs'

const props = defineProps<{
  logs: MonitorLog[]
  autoScroll?: boolean
}>()

const logContainerRef = ref<HTMLElement>()
const dialogVisible = ref(false)
const currentLog = ref<MonitorLog | null>(null)
const userScrolled = ref(false)

// 获取日志等级类型
const getLogLevelType = (level: MonitorLog['level']) => {
  const types = {
    info: 'info',
    warning: 'warning',
    error: 'danger',
    critical: 'danger'
  }
  return types[level] || 'info'
}

// 获取日志等级文本
const getLogLevelText = (level: MonitorLog['level']) => {
  const texts = {
    info: '信息',
    warning: '警告',
    error: '错误',
    critical: '严重'
  }
  return texts[level] || '未知'
}

// 获取日志类型样式
const getLogTypeType = (type: MonitorLog['type']) => {
  const types = {
    security: '',
    lab: 'success',
    system: 'info'
  }
  return types[type] || ''
}

// 获取日志类型文本
const getLogTypeText = (type: MonitorLog['type']) => {
  const texts = {
    security: '安全',
    lab: '实验',
    system: '系统'
  }
  return texts[type] || '未知'
}

// 格式化时间
const formatTime = (timestamp: string) => {
  return dayjs(timestamp).format('HH:mm:ss')
}

// 格式化详细时间
const formatDetailTime = (timestamp: string) => {
  return dayjs(timestamp).format('YYYY-MM-DD HH:mm:ss')
}

// 复制日志
const copyLog = async (log: MonitorLog) => {
  try {
    const text = `[${formatDetailTime(log.timestamp)}] [${getLogTypeText(log.type)}] [${getLogLevelText(log.level)}] ${log.message}`
    await navigator.clipboard.writeText(text)
    ElMessage.success('复制成功')
  } catch (error) {
    console.error('Failed to copy log:', error)
    ElMessage.error('复制失败')
  }
}

// 查看日志详情
const viewLogDetail = (log: MonitorLog) => {
  currentLog.value = log
  dialogVisible.value = true
}

// 处理滚动
const handleScroll = () => {
  if (!logContainerRef.value) return
  
  const { scrollTop, scrollHeight, clientHeight } = logContainerRef.value
  const atBottom = Math.abs(scrollHeight - scrollTop - clientHeight) < 1
  
  userScrolled.value = !atBottom
}

// 滚动到底部
const scrollToBottom = () => {
  if (!logContainerRef.value) return
  
  logContainerRef.value.scrollTop = logContainerRef.value.scrollHeight
}

// 监听日志变化
watch(
  () => props.logs,
  async () => {
    if (props.autoScroll && !userScrolled.value) {
      await nextTick()
      scrollToBottom()
    }
  },
  { deep: true }
)

// 监听自动滚动设置
watch(
  () => props.autoScroll,
  (newValue) => {
    if (newValue) {
      userScrolled.value = false
      scrollToBottom()
    }
  }
)
</script>

<style lang="scss" scoped>
.realtime-log {
  height: 100%;
  
  .log-container {
    height: 320px;
    overflow-y: auto;
    padding: 0 10px;
    
    &::-webkit-scrollbar {
      width: 6px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: var(--el-border-color);
      border-radius: 3px;
      
      &:hover {
        background: var(--el-border-color-darker);
      }
    }

    .log-item {
      padding: 8px 12px;
      margin-bottom: 8px;
      border-radius: 4px;
      background: var(--el-fill-color-light);
      transition: all 0.3s;
      
      &:hover {
        background: var(--el-fill-color);
      }

      .log-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;

        .log-meta {
          display: flex;
          align-items: center;
          gap: 8px;

          .level-tag,
          .type-tag {
            text-transform: uppercase;
          }

          .timestamp {
            color: var(--el-text-color-secondary);
            font-size: 12px;
          }
        }

        .log-actions {
          opacity: 0;
          transition: opacity 0.3s;
          display: flex;
          gap: 4px;
        }
      }

      .log-content {
        color: var(--el-text-color-regular);
        font-size: 13px;
        line-height: 1.5;
        word-break: break-all;
      }

      &:hover {
        .log-actions {
          opacity: 1;
        }
      }

      &.level-error,
      &.level-critical {
        border-left: 3px solid var(--el-color-danger);
      }

      &.level-warning {
        border-left: 3px solid var(--el-color-warning);
      }

      &.level-info {
        border-left: 3px solid var(--el-color-info);
      }
    }
  }

  .empty-logs {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.log-detail {
  .detail-item {
    margin-bottom: 16px;

    &:last-child {
      margin-bottom: 0;
    }

    .item-label {
      display: block;
      color: var(--el-text-color-secondary);
      font-size: 13px;
      margin-bottom: 4px;
    }

    .item-value {
      color: var(--el-text-color-primary);
      font-size: 14px;

      pre {
        margin: 0;
        padding: 12px;
        background: var(--el-fill-color-light);
        border-radius: 4px;
        font-family: monospace;
        font-size: 12px;
        overflow-x: auto;
      }
    }
  }
}
</style> 