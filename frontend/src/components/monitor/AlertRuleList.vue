<template>
  <div class="alert-rule-list">
    <div class="alert-rule-list__header">
      <el-button type="primary" @click="handleCreate">
        创建规则
      </el-button>
      
      <div class="alert-rule-list__filters">
        <el-select
          v-model="filters.metricType"
          placeholder="监控指标"
          clearable
          @change="handleFilter"
        >
          <el-option
            v-for="item in metricTypeOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        
        <el-select
          v-model="filters.enabled"
          placeholder="规则状态"
          clearable
          @change="handleFilter"
        >
          <el-option label="已启用" :value="true" />
          <el-option label="已禁用" :value="false" />
        </el-select>
      </div>
    </div>

    <el-table
      v-loading="loading"
      :data="rules"
      border
      style="width: 100%"
    >
      <el-table-column prop="name" label="规则名称" min-width="150">
        <template #default="{ row }">
          <el-tooltip
            v-if="row.description"
            :content="row.description"
            placement="top"
          >
            <span>{{ row.name }}</span>
          </el-tooltip>
          <span v-else>{{ row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="metricType" label="监控指标" width="120">
        <template #default="{ row }">
          {{ getMetricTypeLabel(row.metricType) }}
        </template>
      </el-table-column>

      <el-table-column label="触发条件" width="200">
        <template #default="{ row }">
          {{ getOperatorLabel(row.operator) }} {{ row.threshold }}
        </template>
      </el-table-column>

      <el-table-column prop="duration" label="持续时间" width="100">
        <template #default="{ row }">
          {{ row.duration }}秒
        </template>
      </el-table-column>

      <el-table-column prop="cooldown" label="冷却时间" width="100">
        <template #default="{ row }">
          {{ row.cooldown }}秒
        </template>
      </el-table-column>

      <el-table-column prop="notifyMethods" label="通知方式" width="150">
        <template #default="{ row }">
          <el-tag
            v-for="method in row.notifyMethods"
            :key="method"
            size="small"
            class="mx-1"
          >
            {{ getNotifyMethodLabel(method) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column prop="enabled" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.enabled ? 'success' : 'info'">
            {{ row.enabled ? '已启用' : '已禁用' }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button
              size="small"
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              :type="row.enabled ? 'warning' : 'success'"
              @click="handleToggleStatus(row)"
            >
              {{ row.enabled ? '禁用' : '启用' }}
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <div class="alert-rule-list__pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '创建规则' : '编辑规则'"
      width="650px"
    >
      <alert-rule-form
        :initial-data="currentRule"
        @submit="handleFormSubmit"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import AlertRuleForm from './AlertRuleForm.vue'
import {
  getAlertRules,
  createAlertRule,
  updateAlertRule,
  deleteAlertRule,
  enableAlertRule,
  disableAlertRule
} from '@/api/alert_rules'
import type {
  AlertRule,
  AlertRuleCreate,
  AlertRuleBase
} from '@/types/alert'
import { MetricType } from '@/types/alert'

const loading = ref(false)
const rules = ref<AlertRule[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const currentRule = ref<Partial<AlertRuleBase>>({})

const filters = reactive({
  metricType: '',
  enabled: undefined as boolean | undefined
})

const metricTypeOptions = [
  { label: 'CPU使用率', value: MetricType.CPU },
  { label: '内存使用率', value: MetricType.MEMORY },
  { label: '磁盘使用率', value: MetricType.DISK },
  { label: '网络流量', value: MetricType.NETWORK },
  { label: '系统负载', value: MetricType.SYSTEM_LOAD },
  { label: '进程数', value: MetricType.PROCESS }
]

const getMetricTypeLabel = (type: string) => {
  return metricTypeOptions.find(option => option.value === type)?.label || type
}

const getOperatorLabel = (operator: string) => {
  const map: Record<string, string> = {
    '>': '大于',
    '>=': '大于等于',
    '<': '小于',
    '<=': '小于等于',
    '==': '等于',
    '!=': '不等于'
  }
  return map[operator] || operator
}

const getNotifyMethodLabel = (method: string) => {
  const map: Record<string, string> = {
    email: '邮件',
    web: '站内信',
    sms: '短信'
  }
  return map[method] || method
}

const loadRules = async () => {
  loading.value = true
  try {
    const { data } = await getAlertRules({
      page: currentPage.value,
      pageSize: pageSize.value,
      metricType: filters.metricType || undefined,
      enabled: filters.enabled
    })
    rules.value = data.items
    total.value = data.total
  } catch (error) {
    ElMessage.error('加载规则列表失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  dialogType.value = 'create'
  currentRule.value = {}
  dialogVisible.value = true
}

const handleEdit = (rule: AlertRule) => {
  dialogType.value = 'edit'
  currentRule.value = { ...rule }
  dialogVisible.value = true
}

const handleFormSubmit = async (data: AlertRuleBase) => {
  try {
    if (dialogType.value === 'create') {
      await createAlertRule(data)
      ElMessage.success('创建成功')
    } else {
      await updateAlertRule((currentRule.value as AlertRule).id, data)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadRules()
  } catch (error) {
    ElMessage.error(dialogType.value === 'create' ? '创建失败' : '更新失败')
  }
}

const handleDelete = async (rule: AlertRule) => {
  try {
    await ElMessageBox.confirm('确定要删除该规则吗？', '提示', {
      type: 'warning'
    })
    await deleteAlertRule(rule.id)
    ElMessage.success('删除成功')
    loadRules()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleToggleStatus = async (rule: AlertRule) => {
  try {
    if (rule.enabled) {
      await disableAlertRule(rule.id)
      ElMessage.success('已禁用')
    } else {
      await enableAlertRule(rule.id)
      ElMessage.success('已启用')
    }
    loadRules()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleFilter = () => {
  currentPage.value = 1
  loadRules()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadRules()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadRules()
}

onMounted(() => {
  loadRules()
})
</script>

<style lang="scss" scoped>
.alert-rule-list {
  padding: 20px;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  &__filters {
    display: flex;
    gap: 10px;
  }

  &__pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }

  :deep(.el-tag) {
    margin-right: 5px;
    
    &:last-child {
      margin-right: 0;
    }
  }
}
</style> 