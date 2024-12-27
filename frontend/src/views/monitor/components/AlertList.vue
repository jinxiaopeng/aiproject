<template>
  <div class="alert-list">
    <el-table
      v-loading="loading"
      :data="alerts"
      style="width: 100%"
      :max-height="350"
    >
      <el-table-column prop="timestamp" label="时间" width="160">
        <template #default="{ row }">
          {{ formatTime(row.timestamp) }}
        </template>
      </el-table-column>

      <el-table-column prop="type" label="类型" width="120">
        <template #default="{ row }">
          <el-tag
            :type="getAlertTypeStyle(row.type).type"
            :effect="row.level === 'critical' ? 'dark' : 'light'"
            size="small"
          >
            {{ getAlertTypeStyle(row.type).label }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="level" label="等级" width="100">
        <template #default="{ row }">
          <el-tag
            :type="getAlertLevelStyle(row.level)"
            size="small"
            effect="dark"
          >
            {{ getAlertLevelText(row.level) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="source" label="来源" width="140">
        <template #default="{ row }">
          <el-tooltip
            v-if="row.details?.location"
            :content="row.details.location"
            placement="top"
          >
            <span>{{ row.source }}</span>
          </el-tooltip>
          <span v-else>{{ row.source }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="details" label="详情">
        <template #default="{ row }">
          <div class="alert-details">
            <div v-if="row.type === 'login'" class="detail-item">
              <span>用户: {{ row.details?.user }}</span>
              <span>IP: {{ row.details?.ip }}</span>
            </div>
            <div v-else-if="row.type === 'injection'" class="detail-item">
              <span>目标: {{ row.details?.target }}</span>
              <el-tooltip :content="row.details?.payload" placement="top">
                <span class="payload">Payload: {{ truncateText(row.details?.payload, 30) }}</span>
              </el-tooltip>
            </div>
            <div v-else class="detail-item">
              <span>{{ row.details?.action || '未知操作' }}</span>
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag
            :type="getStatusStyle(row.status)"
            size="small"
          >
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
            @click="handleAlert(row)"
          >
            处理
          </el-button>
          <el-button
            type="primary"
            link
            @click="viewDetail(row)"
          >
            详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 处理告警对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="处理告警"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="处理方式" prop="action">
          <el-select v-model="form.action" placeholder="请选择处理方式">
            <el-option
              v-for="action in getAvailableActions(currentAlert?.type)"
              :key="action.value"
              :label="action.label"
              :value="action.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="comment">
          <el-input
            v-model="form.comment"
            type="textarea"
            :rows="3"
            placeholder="请输入处理备注"
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
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import type { SecurityAlert, AlertAction } from '@/types/monitor'
import dayjs from 'dayjs'

const props = defineProps<{
  alerts: SecurityAlert[]
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'handle', action: AlertAction): void
}>()

// 表单相关
const dialogVisible = ref(false)
const submitting = ref(false)
const currentAlert = ref<SecurityAlert | null>(null)
const formRef = ref<FormInstance>()

const form = ref({
  action: '',
  comment: ''
})

const rules = {
  action: [{ required: true, message: '请选择处理方式', trigger: 'change' }]
}

// 格式化时间
const formatTime = (timestamp: string) => {
  return dayjs(timestamp).format('YYYY-MM-DD HH:mm')
}

// 截断文本
const truncateText = (text: string = '', length: number) => {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

// 获取告警类型样式
const getAlertTypeStyle = (type: SecurityAlert['type']) => {
  const styles = {
    login: { type: 'warning', label: '登录异常' },
    injection: { type: 'danger', label: 'SQL注入' },
    xss: { type: 'danger', label: 'XSS攻击' },
    file_access: { type: 'warning', label: '文件访问' },
    privilege: { type: 'danger', label: '权限提升' }
  }
  return styles[type] || { type: 'info', label: '未知' }
}

// 获取告警等级样式
const getAlertLevelStyle = (level: SecurityAlert['level']) => {
  const styles = {
    low: 'info',
    medium: 'warning',
    high: 'danger',
    critical: 'danger'
  }
  return styles[level] || 'info'
}

// 获取告警等级文本
const getAlertLevelText = (level: SecurityAlert['level']) => {
  const texts = {
    low: '低危',
    medium: '中危',
    high: '高危',
    critical: '严重'
  }
  return texts[level] || '未知'
}

// 获取状态样式
const getStatusStyle = (status: SecurityAlert['status']) => {
  const styles = {
    pending: 'warning',
    processing: 'info',
    resolved: 'success'
  }
  return styles[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: SecurityAlert['status']) => {
  const texts = {
    pending: '待处理',
    processing: '处理中',
    resolved: '已解决'
  }
  return texts[status] || '未知'
}

// 获取可用的处理动作
const getAvailableActions = (type?: SecurityAlert['type']) => {
  const commonActions = [
    { label: '标记已处理', value: 'mark_resolved' },
    { label: '通知管理员', value: 'notify_admin' }
  ]

  const typeActions = {
    login: [
      { label: '封禁IP', value: 'block_ip' },
      { label: '重置密码', value: 'reset_password' },
      { label: '禁用账号', value: 'disable_user' }
    ],
    injection: [
      { label: '封禁IP', value: 'block_ip' },
      { label: '加入黑名单', value: 'add_blacklist' }
    ],
    xss: [
      { label: '封禁IP', value: 'block_ip' },
      { label: '清理缓存', value: 'clear_cache' }
    ],
    file_access: [
      { label: '封禁IP', value: 'block_ip' },
      { label: '撤销��限', value: 'revoke_permission' }
    ],
    privilege: [
      { label: '禁用账号', value: 'disable_user' },
      { label: '重置权限', value: 'reset_privilege' }
    ]
  }

  return [...(type ? typeActions[type] || [] : []), ...commonActions]
}

// 处理告警
const handleAlert = (alert: SecurityAlert) => {
  currentAlert.value = alert
  form.value = {
    action: '',
    comment: ''
  }
  dialogVisible.value = true
}

// 提交处理
const submitHandle = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid && currentAlert.value) {
      submitting.value = true
      try {
        emit('handle', {
          type: form.value.action as AlertAction['type'],
          alertId: currentAlert.value.id,
          comment: form.value.comment,
          parameters: {
            ip: currentAlert.value.details?.ip,
            user: currentAlert.value.details?.user
          }
        })
        dialogVisible.value = false
        ElMessage.success('处理成功')
      } catch (error) {
        console.error('Failed to handle alert:', error)
        ElMessage.error('处理失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

// 查看详情
const viewDetail = (alert: SecurityAlert) => {
  // TODO: 实现查看详情功能
  console.log('View detail:', alert)
}
</script>

<style lang="scss" scoped>
.alert-list {
  .alert-details {
    .detail-item {
      display: flex;
      gap: 12px;
      color: var(--el-text-color-secondary);
      font-size: 13px;

      .payload {
        color: var(--el-color-danger);
        cursor: pointer;
      }
    }
  }

  :deep(.el-table) {
    --el-table-border-color: var(--el-border-color-lighter);
    
    .el-table__body-wrapper {
      &::-webkit-scrollbar {
        width: 6px;
        height: 6px;
      }
      
      &::-webkit-scrollbar-thumb {
        background: var(--el-border-color);
        border-radius: 3px;
        
        &:hover {
          background: var(--el-border-color-darker);
        }
      }
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 