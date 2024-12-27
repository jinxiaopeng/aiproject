<template>
  <div class="quick-actions">
    <el-row :gutter="16">
      <el-col :span="12" v-for="action in actions" :key="action.key">
        <el-button
          class="action-button"
          :type="action.type"
          :icon="action.icon"
          @click="handleAction(action.key)"
          :loading="loading === action.key"
        >
          {{ action.label }}
        </el-button>
      </el-col>
    </el-row>

    <!-- 确认对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentAction?.confirmTitle || '确认操作'"
      width="400px"
      destroy-on-close
    >
      <div class="confirm-content">
        {{ currentAction?.confirmMessage || '确认执行此操作？' }}
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            @click="confirmAction"
            :loading="confirming"
          >
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Refresh,
  Delete,
  Warning,
  Connection,
  Download,
  Setting
} from '@element-plus/icons-vue'

const emit = defineEmits<{
  (e: 'action', key: string): void
}>()

// 定义快速操作
const actions = [
  {
    key: 'refresh_all',
    label: '刷新所有',
    icon: Refresh,
    type: 'primary',
    confirmTitle: '刷新确认',
    confirmMessage: '确认刷新所有监控数据？'
  },
  {
    key: 'clear_alerts',
    label: '清理告警',
    icon: Delete,
    type: 'warning',
    confirmTitle: '清理确认',
    confirmMessage: '确认清理所有已处理的告警？此操作不可恢复。'
  },
  {
    key: 'test_connection',
    label: '测试连接',
    icon: Connection,
    type: 'info',
    confirmTitle: '连接测试',
    confirmMessage: '确认开始测试所有系统连接？'
  },
  {
    key: 'export_logs',
    label: '导出日志',
    icon: Download,
    type: 'success',
    confirmTitle: '导出确认',
    confirmMessage: '确认导出最近24小时的系统日志？'
  },
  {
    key: 'reset_warning',
    label: '重置警告',
    icon: Warning,
    type: 'danger',
    confirmTitle: '重置确认',
    confirmMessage: '确认重置所有警告状态���此操作将清除所有警告记录。'
  },
  {
    key: 'system_check',
    label: '系统检查',
    icon: Setting,
    type: 'info',
    confirmTitle: '检查确认',
    confirmMessage: '确认开始全面系统检查？此操作可能需要几分钟时间。'
  }
]

const loading = ref<string | null>(null)
const dialogVisible = ref(false)
const confirming = ref(false)
const currentAction = ref<typeof actions[0] | null>(null)

// 处理操作点击
const handleAction = (key: string) => {
  const action = actions.find(a => a.key === key)
  if (!action) return
  
  currentAction.value = action
  dialogVisible.value = true
}

// 确认操作
const confirmAction = async () => {
  if (!currentAction.value) return
  
  confirming.value = true
  loading.value = currentAction.value.key
  
  try {
    emit('action', currentAction.value.key)
    ElMessage.success('操作执行成功')
    dialogVisible.value = false
  } catch (error) {
    console.error('Failed to execute action:', error)
    ElMessage.error('操作执行失败')
  } finally {
    confirming.value = false
    loading.value = null
  }
}
</script>

<style lang="scss" scoped>
.quick-actions {
  .el-row {
    margin: -8px;
  }

  .el-col {
    padding: 8px;
  }

  .action-button {
    width: 100%;
    justify-content: flex-start;
    padding: 12px;
    border-radius: 4px;
    transition: all 0.3s;
    
    &:hover {
      transform: translateY(-2px);
    }

    .el-icon {
      margin-right: 8px;
      font-size: 16px;
    }
  }
}

.confirm-content {
  color: var(--el-text-color-regular);
  font-size: 14px;
  line-height: 1.5;
  padding: 16px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 