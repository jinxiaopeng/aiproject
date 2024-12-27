<template>
  <div class="security-monitor">
    <!-- 顶部统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6" v-for="stat in securityStats" :key="stat.title">
        <el-card shadow="hover" :body-style="{ padding: '20px' }">
          <div class="stat-card">
            <div class="stat-icon" :class="stat.level">
              <el-icon :size="24">
                <component :is="stat.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-desc">{{ stat.description }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 实时安全事件监控 -->
    <el-row :gutter="20" class="main-content">
      <el-col :span="16">
        <el-card class="security-events" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>实时安全事件</span>
              <div class="header-actions">
                <el-select v-model="eventType" size="small" placeholder="事件类型">
                  <el-option label="全部事件" value="all" />
                  <el-option label="漏洞利用" value="exploit" />
                  <el-option label="异常访问" value="access" />
                  <el-option label="敏感操作" value="sensitive" />
                </el-select>
                <el-select v-model="eventLevel" size="small" placeholder="危险等级">
                  <el-option label="全部等级" value="all" />
                  <el-option label="高危" value="high" />
                  <el-option label="中危" value="medium" />
                  <el-option label="低危" value="low" />
                </el-select>
                <el-button type="primary" :icon="Refresh" @click="refreshEvents">
                  刷新
                </el-button>
              </div>
            </div>
          </template>
          
          <el-table
            :data="securityEvents"
            style="width: 100%"
            :max-height="480"
            v-loading="loading.events"
          >
            <el-table-column prop="time" label="时间" width="160" />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getEventTypeStyle(row.type)">
                  {{ getEventTypeText(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="level" label="等级" width="100">
              <template #default="{ row }">
                <el-tag :type="getEventLevelStyle(row.level)">
                  {{ getEventLevelText(row.level) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusStyle(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button
                  v-if="row.status === 'pending'"
                  type="primary"
                  link
                  @click="handleEvent(row)"
                >
                  处理
                </el-button>
                <el-button
                  type="primary"
                  link
                  @click="viewEventDetail(row)"
                >
                  详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 右侧面板 -->
      <el-col :span="8">
        <!-- 威胁分布 -->
        <el-card class="threat-distribution" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>威胁分布</span>
              <el-radio-group v-model="threatTimeRange" size="small">
                <el-radio-button label="day">今日</el-radio-button>
                <el-radio-button label="week">本周</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <ThreatDistributionChart 
              :data="threatData" 
              :loading="loading.threat" 
            />
          </div>
        </el-card>

        <!-- 实时告警 -->
        <el-card class="realtime-alerts" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>实时告警</span>
              <el-switch
                v-model="autoScroll"
                active-text="自动滚动"
              />
            </div>
          </template>
          <div class="alert-list" ref="alertListRef">
            <div 
              v-for="alert in realtimeAlerts" 
              :key="alert.id"
              class="alert-item"
              :class="alert.level"
            >
              <div class="alert-time">{{ alert.time }}</div>
              <div class="alert-content">{{ alert.content }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 处理事件对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="处理安全事件"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="处理方式" prop="action">
          <el-select v-model="form.action" placeholder="请选择处理方式">
            <el-option
              v-for="action in availableActions"
              :key="action.value"
              :label="action.label"
              :value="action.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="处理说明" prop="comment">
          <el-input
            v-model="form.comment"
            type="textarea"
            rows="3"
            placeholder="请输入处理说明"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitHandle" :loading="submitting">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Shield, Warning, CircleClose, InfoFilled, Refresh } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import ThreatDistributionChart from './components/ThreatDistributionChart.vue'

// 统计数据
const securityStats = ref([
  {
    title: '安全评分',
    value: '95',
    description: '系统安全状态良好',
    icon: Shield,
    level: 'success'
  },
  {
    title: '待处理事件',
    value: '3',
    description: '需要及时处理',
    icon: Warning,
    level: 'warning'
  },
  {
    title: '高危漏洞',
    value: '1',
    description: '已发现高危漏洞',
    icon: CircleClose,
    level: 'danger'
  },
  {
    title: '防护建议',
    value: '5',
    description: '可优化防护措施',
    icon: InfoFilled,
    level: 'info'
  }
])

// 事件筛选
const eventType = ref('all')
const eventLevel = ref('all')
const threatTimeRange = ref('day')
const autoScroll = ref(true)

// 加载状态
const loading = ref({
  events: false,
  threat: false
})

// 数据列表
const securityEvents = ref([])
const threatData = ref([])
const realtimeAlerts = ref([])

// 对话框控制
const dialogVisible = ref(false)
const submitting = ref(false)
const currentEvent = ref(null)
const formRef = ref<FormInstance>()

// 表单数据
const form = ref({
  action: '',
  comment: ''
})

// 表单规则
const rules = {
  action: [
    { required: true, message: '请选择处理方式', trigger: 'change' }
  ],
  comment: [
    { required: true, message: '请输入处理说明', trigger: 'blur' }
  ]
}

// 可用的处理动作
const availableActions = ref([
  { label: '确认处理', value: 'confirm' },
  { label: '标记误报', value: 'false_positive' },
  { label: '暂不处理', value: 'ignore' },
  { label: '上报处理', value: 'escalate' }
])

// 获取事件类型样式
const getEventTypeStyle = (type: string) => {
  const styles = {
    exploit: 'danger',
    access: 'warning',
    sensitive: 'info'
  }
  return styles[type] || 'info'
}

// 获取事件类型文本
const getEventTypeText = (type: string) => {
  const texts = {
    exploit: '漏洞利用',
    access: '异常访问',
    sensitive: '敏感操作'
  }
  return texts[type] || '未知类型'
}

// 获取事件等级样式
const getEventLevelStyle = (level: string) => {
  const styles = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return styles[level] || 'info'
}

// 获取事件等级文本
const getEventLevelText = (level: string) => {
  const texts = {
    high: '高危',
    medium: '中危',
    low: '低危'
  }
  return texts[level] || '未知'
}

// 获取状态样式
const getStatusStyle = (status: string) => {
  const styles = {
    pending: 'warning',
    processing: 'info',
    resolved: 'success',
    ignored: 'info'
  }
  return styles[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const texts = {
    pending: '待处理',
    processing: '处理中',
    resolved: '已解决',
    ignored: '已忽略'
  }
  return texts[status] || '未知'
}

// 刷新事件列表
const refreshEvents = async () => {
  loading.value.events = true
  try {
    // TODO: 实现数据加载逻辑
  } catch (error) {
    console.error('Failed to refresh events:', error)
  } finally {
    loading.value.events = false
  }
}

// 处理事件
const handleEvent = (event: any) => {
  currentEvent.value = event
  dialogVisible.value = true
}

// 查看事件详情
const viewEventDetail = (event: any) => {
  // TODO: 实现查看详情逻辑
}

// 提交处理
const submitHandle = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        // TODO: 实现提交处理逻辑
        dialogVisible.value = false
      } catch (error) {
        console.error('Failed to handle event:', error)
      } finally {
        submitting.value = false
      }
    }
  })
}

// 自动刷新定时器
let refreshTimer: number | null = null

onMounted(() => {
  refreshEvents()
  // 每30秒自动刷新一次
  refreshTimer = window.setInterval(refreshEvents, 30000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style lang="scss" scoped>
.security-monitor {
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

      &.success {
        background: var(--el-color-success-light-9);
        color: var(--el-color-success);
      }

      &.warning {
        background: var(--el-color-warning-light-9);
        color: var(--el-color-warning);
      }

      &.danger {
        background: var(--el-color-danger-light-9);
        color: var(--el-color-danger);
      }

      &.info {
        background: var(--el-color-info-light-9);
        color: var(--el-color-info);
      }
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
      }

      .stat-desc {
        font-size: 12px;
        color: var(--el-text-color-secondary);
      }
    }
  }

  .main-content {
    .security-events {
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
    }
  }

  .threat-distribution {
    margin-bottom: 20px;

    .chart-container {
      height: 280px;
    }
  }

  .realtime-alerts {
    .alert-list {
      height: 300px;
      overflow-y: auto;

      .alert-item {
        padding: 12px;
        border-bottom: 1px solid var(--el-border-color-lighter);

        &:last-child {
          border-bottom: none;
        }

        &.high {
          border-left: 4px solid var(--el-color-danger);
        }

        &.medium {
          border-left: 4px solid var(--el-color-warning);
        }

        &.low {
          border-left: 4px solid var(--el-color-info);
        }

        .alert-time {
          font-size: 12px;
          color: var(--el-text-color-secondary);
          margin-bottom: 4px;
        }

        .alert-content {
          font-size: 14px;
          line-height: 1.4;
        }
      }
    }
  }
}
</style>