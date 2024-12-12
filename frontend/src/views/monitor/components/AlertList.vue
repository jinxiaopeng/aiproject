<template>
  <div class="alert-list-container">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <div class="filter-group">
        <!-- 预警类型筛选 -->
        <el-select v-model="filters.type" placeholder="预警类型" clearable class="filter-item">
          <el-option
            v-for="item in alertTypes"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
            <template #default="{ label }">
              <el-tag :type="getAlertTypeTag(item.value)" size="small" class="type-tag">
                {{ label }}
              </el-tag>
            </template>
          </el-option>
        </el-select>

        <!-- 处理状态筛选 -->
        <el-select v-model="filters.status" placeholder="处理状态" clearable multiple class="filter-item">
          <el-option
            v-for="item in statusOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
            <template #default="{ label }">
              <el-tag :type="getStatusTag(item.value)" size="small" class="status-tag">
                {{ label }}
              </el-tag>
            </template>
          </el-option>
        </el-select>

        <!-- 时间范围选择 -->
        <el-date-picker
          v-model="dateRange"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
          :shortcuts="dateShortcuts"
          class="filter-item"
        />
      </div>

      <div class="action-group">
        <el-button-group>
          <el-tooltip content="切换视图">
            <el-button :icon="viewMode === 'table' ? ListIcon : GridIcon" @click="toggleViewMode" />
          </el-tooltip>
          <el-tooltip content="刷新列表">
            <el-button :icon="Refresh" :loading="loading" @click="refreshList" />
          </el-tooltip>
        </el-button-group>
      </div>
    </div>

    <!-- 表格视图 -->
    <div v-if="viewMode === 'table'" class="table-view">
      <el-table
        v-loading="loading"
        :data="alertList"
        :max-height="tableMaxHeight"
        border
        stripe
        @sort-change="handleSortChange"
      >
        <el-table-column label="时间" width="180" sortable="custom" prop="time">
          <template #default="{ row }">
            <div class="time-cell">
              <span class="date">{{ formatDate(row.time, 'YYYY-MM-DD') }}</span>
              <span class="time">{{ formatDate(row.time, 'HH:mm:ss') }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="预警类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getAlertTypeTag(row.type)" size="small">
              {{ getAlertTypeLabel(row.type) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="预警内容">
          <template #default="{ row }">
            <div class="content-cell">
              <el-icon :class="getAlertIcon(row.type)" />
              <span>{{ row.content }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button-group>
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
              <el-dropdown>
                <el-button type="primary" link>
                  更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="handleExport(row)">
                      <el-icon><download /></el-icon>导出
                    </el-dropdown-item>
                    <el-dropdown-item @click="handleShare(row)">
                      <el-icon><share /></el-icon>分享
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 卡片视图 -->
    <div v-else class="card-view">
      <el-row :gutter="16">
        <el-col 
          v-for="item in alertList" 
          :key="item.id"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
        >
          <div class="alert-card" :class="item.status">
            <div class="card-header">
              <el-tag :type="getAlertTypeTag(item.type)" size="small">
                {{ getAlertTypeLabel(item.type) }}
              </el-tag>
              <el-tag :type="getStatusTag(item.status)" size="small">
                {{ getStatusLabel(item.status) }}
              </el-tag>
            </div>
            <div class="card-body">
              <div class="time-info">
                <el-icon><clock /></el-icon>
                <span>{{ formatDate(item.time, 'YYYY-MM-DD HH:mm:ss') }}</span>
              </div>
              <div class="content">{{ item.content }}</div>
            </div>
            <div class="card-footer">
              <el-button-group>
                <el-button 
                  v-if="item.status === 'pending'"
                  type="primary" 
                  link
                  @click="handleAlert(item)"
                >
                  处理
                </el-button>
                <el-button 
                  type="primary" 
                  link
                  @click="viewDetail(item)"
                >
                  详情
                </el-button>
              </el-button-group>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 分页器 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[12, 24, 48, 96]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import {
  List as ListIcon,
  Grid as GridIcon,
  Timer as ClockIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  ArrowDown as ArrowDownIcon
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import type { Alert } from '@/api/monitor'

const props = defineProps<{
  timeRange: string
}>()

const emit = defineEmits<{
  (e: 'refresh'): void
}>()

// 视图模式
const viewMode = ref('table')
const tableMaxHeight = computed(() => window.innerHeight - 300)

// 列表数据
const loading = ref(false)
const alertList = ref<Alert[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)

// 筛选条件
const filters = ref({
  type: '',
  status: []
})

const dateRange = ref([])

// 预警类型选项
const alertTypes = [
  { label: '登录预警', value: 'login', color: '#f56c6c', icon: 'el-icon-user' },
  { label: '操作预警', value: 'operation', color: '#e6a23c', icon: 'el-icon-warning' },
  { label: '安全预警', value: 'security', color: '#f56c6c', icon: 'el-icon-shield' }
]

// 状态选项
const statusOptions = [
  { label: '待处理', value: 'pending', color: '#f56c6c' },
  { label: '处理中', value: 'processing', color: '#e6a23c' },
  { label: '已处理', value: 'handled', color: '#67c23a' },
  { label: '已忽略', value: 'ignored', color: '#909399' }
]

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近24小时',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24)
      return [start, end]
    }
  },
  {
    text: '最近3天',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 3)
      return [start, end]
    }
  },
  {
    text: '最近7天',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  }
]

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取数据
    // 模拟数据
    alertList.value = [
      {
        id: 1,
        type: 'login',
        status: 'pending',
        time: '2023-12-12 10:30:00',
        content: '检测到异常登录行为，IP地址: 192.168.1.100，尝试次数: 5次'
      },
      {
        id: 2,
        type: 'operation',
        status: 'processing',
        time: '2023-12-12 09:15:00',
        content: '用户admin执行了敏感操作：批量删除用户数据'
      },
      {
        id: 3,
        type: 'security',
        status: 'handled',
        time: '2023-12-12 08:00:00',
        content: '系统检测到可疑的网络扫描行为'
      }
    ]
    total.value = 100
    loading.value = false
  } catch (error) {
    console.error('Failed to load alerts:', error)
    ElMessage.error('加载预警列表失败')
    loading.value = false
  }
}

// 切换视图模式
const toggleViewMode = () => {
  viewMode.value = viewMode.value === 'table' ? 'card' : 'table'
}

// 处理预警
const handleAlert = async (row: Alert) => {
  try {
    // TODO: 调用API处理预警
    ElMessage.success('处理成功')
    loadData()
    emit('refresh')
  } catch (error) {
    console.error('Failed to handle alert:', error)
    ElMessage.error('处理失败')
  }
}

// 查看详情
const viewDetail = (row: Alert) => {
  // TODO: 实现查看详情功能
}

// 导出
const handleExport = (row: Alert) => {
  // TODO: 实现导出功能
}

// 分享
const handleShare = (row: Alert) => {
  // TODO: 实现分享功能
}

// 刷新列表
const refreshList = () => {
  currentPage.value = 1
  loadData()
}

// 按类型筛选
const filterByType = (type: string) => {
  filters.value.type = type
  currentPage.value = 1
  loadData()
}

// 处理排序变化
const handleSortChange = (sort: any) => {
  // TODO: 处理排序
  loadData()
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadData()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadData()
}

// 工具函数
const formatDate = (date: string, format: string) => {
  return dayjs(date).format(format)
}

const getAlertTypeTag = (type: string): string => {
  const types: Record<string, string> = {
    login: 'danger',
    operation: 'warning',
    security: 'error'
  }
  return types[type] || 'info'
}

const getStatusTag = (status: string): string => {
  const types: Record<string, string> = {
    pending: 'danger',
    processing: 'warning',
    handled: 'success',
    ignored: 'info'
  }
  return types[status] || 'info'
}

const getAlertTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    login: '登录预警',
    operation: '操作预警',
    security: '安全预警'
  }
  return labels[type] || type
}

const getStatusLabel = (status: string): string => {
  const labels: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    handled: '已处理',
    ignored: '已忽略'
  }
  return labels[status] || status
}

const getAlertIcon = (type: string): string => {
  const icons: Record<string, string> = {
    login: 'el-icon-user',
    operation: 'el-icon-warning',
    security: 'el-icon-shield'
  }
  return icons[type] || 'el-icon-warning'
}

// 监听属性变化
watch(() => props.timeRange, (newVal) => {
  currentPage.value = 1
  loadData()
})

// 暴露方法
defineExpose({
  filterByType,
  refreshList
})

// 初始化
onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.alert-list-container {
  .toolbar {
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;

    .filter-group {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;

      .filter-item {
        min-width: 160px;
      }
    }

    .action-group {
      display: flex;
      gap: 12px;
      align-items: center;
    }
  }

  .table-view {
    .time-cell {
      display: flex;
      flex-direction: column;
      line-height: 1.4;

      .date {
        color: var(--el-text-color-primary);
      }

      .time {
        font-size: 12px;
        color: var(--el-text-color-secondary);
      }
    }

    .content-cell {
      display: flex;
      align-items: center;
      gap: 8px;

      .alert-icon {
        font-size: 16px;
      }
    }
  }

  .card-view {
    .alert-card {
      background: var(--el-bg-color);
      border: 1px solid var(--el-border-color-light);
      border-radius: 8px;
      margin-bottom: 16px;
      transition: all 0.3s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: var(--el-box-shadow-light);
      }

      &.pending {
        border-left: 4px solid var(--el-color-danger);
      }

      &.processing {
        border-left: 4px solid var(--el-color-warning);
      }

      &.handled {
        border-left: 4px solid var(--el-color-success);
      }

      &.ignored {
        border-left: 4px solid var(--el-color-info);
      }

      .card-header {
        padding: 12px 16px;
        border-bottom: 1px solid var(--el-border-color-light);
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .card-body {
        padding: 16px;

        .time-info {
          display: flex;
          align-items: center;
          gap: 8px;
          color: var(--el-text-color-secondary);
          margin-bottom: 8px;
        }

        .content {
          color: var(--el-text-color-primary);
          line-height: 1.5;
        }
      }

      .card-footer {
        padding: 12px 16px;
        border-top: 1px solid var(--el-border-color-light);
        display: flex;
        justify-content: flex-end;
      }
    }
  }

  .pagination-container {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }
}
</style> 